# Ferramentas, hooks, permissões e MCP (tudo desativado por padrão)

Política do plugin: **não entrega** `hooks/`, `.mcp.json`, `.lsp.json` nem `bin/`. Este arquivo documenta, para o usuário habilitar conscientemente no **próprio projeto**, cada item com estado, instalação, riscos e fonte (ver `fontes.md`). Nada aqui foi executado pela fábrica. O formato de entrada e saída de hooks foi relido em https://code.claude.com/docs/en/hooks-guide em 2026-10-10 (Verificado): entrada JSON em stdin com `tool_name` e `tool_input.command`; exit 2 bloqueia com o motivo em stderr; alternativa é exit 0 com `hookSpecificOutput.permissionDecision` em `"deny"` (cancela e devolve o motivo) ou `"ask"` (mostra o prompt de permissão normal).

Sumário: 1. Tabela geral · 2. LSP · 3. Hook de gate de gravação · 4. Permissões e sandbox · 5. MCP de hardware (não recomendado) · 6. Vetting de terceiros · 7. Hook de formatação/clang-tidy (opcional) · 8. Camadas de proteção.

## 1. Tabela geral

| Item | Tipo | Estado | Instalação / uso | Riscos e cuidados | Fonte |
| --- | --- | --- | --- | --- | --- |
| `clangd-lsp` | LSP (plugin oficial) | Recomendado | `/plugin install clangd-lsp@claude-plugins-official`; exige o binário `clangd` no PATH; projeto CMake precisa de `compile_commands.json` (Inferido) | LSP não roda em sessões de nuvem; binário de terceiros no PATH | V-06 |
| `rust-analyzer-lsp` | LSP (plugin oficial) | Recomendado | `/plugin install rust-analyzer-lsp@claude-plugins-official`; exige `rust-analyzer` | idem | V-06 |
| clang-tidy, cppcheck, GCC `-fanalyzer`/sanitizers | CLIs | Recomendado (host) | ver `c-cpp-rust-firmware.md` | clang-tidy com toolchain cruzado: Não verificável; `-fanalyzer` só C | V-13, V-58, V-59 |
| ztest/Twister, Unity/CMock/Ceedling, `pio test -e native`, `cargo test` | Testes de host | Recomendado | ver `testes-e-bancada.md` | `unit_testing` só Linux; CMock exige Ruby | V-36, V-37, V-57 |
| `west`, `idf.py`, `pio`, `probe-rs`, `esptool`, OpenOCD, J-Link | CLIs de build/gravação | Build livre; **gravação sob gate** | fornecidos pelo usuário | comandos de escrita: gate; WinUSB do J-Link pode quebrar SEGGER | V-51, V-55, V-21 |
| Hook de gate de gravação (seção 3) | Hook `PreToolUse` | **Não ativo**; copiar para `.claude/` do projeto | ver seção 3 | guarda por texto, não sandbox; um comando alternativo escapa; executa shell com as permissões do usuário | V-05, V-63 |
| Regras `ask`/`deny` + `/sandbox` | Configuração | Recomendado | seção 4 | sem sandbox, `deny` só bloqueia ferramentas nativas e o Bash contorna | V-08, V-63 |
| MCP de hardware (`stm32-mcp`, bancada do SensorsIot, jlink) | MCP | **Não recomendado ativar** | não instalar a partir deste plugin | podem gravar/sobrescrever memória; API da bancada sem autenticação; `sudo` | V-29, V-61 |
| Skills de terceiros (`embeddedskills`, `esp32-expert`, workbench) | Skills | Só referência de desenho | ler SKILL.md e scripts antes; não instalar | fluxos que gravam sem confirmação; estrelas não provam qualidade | V-18, V-21, V-25, V-28 |

## 2. LSP

Os plugins oficiais de LSP vivem no marketplace `claude-plugins-official` (Apache-2.0; cada plugin tem a sua licença; V-07). Instale o binário **antes**; sem ele a aba Errors de `/plugin` mostra `Executable not found in $PATH`. Este plugin não declara `lspServers` próprio. Para projetos CMake, gere o banco de compilação:

```text
cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

Com toolchain cruzado, o clangd pode não achar os headers do `arm-none-eabi`: ajuste `--query-driver` ou o `compile_commands.json` (Inferido; conferir na doc do clangd).

## 3. Hook de gate de gravação (exemplo; `designed_not_executed`)

Objetivo: transformar "comando que grava o dispositivo" em pedido de confirmação com o comando exato visível. **Não coloque em `hooks/hooks.json` de plugin** (política do projeto); copie para o `.claude/` do projeto de firmware, depois de ler e entender. Teste com `claude --debug` antes de confiar.

`.claude/settings.json` do projeto:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/hw-write-gate.py\"" }
        ]
      }
    ]
  }
}
```

`.claude/hooks/hw-write-gate.py` (stdlib; `"ask"` deixa o usuário aprovar vendo o comando; `"deny"` bloqueia):

```python
#!/usr/bin/env python3
"""Guarda PreToolUse: pede confirmação para comandos que escrevem em dispositivo.
Lista de exemplo, não exaustiva. Guarda por texto, não é sandbox."""
import json
import re
import sys

DECISION = "ask"  # ou "deny"
PATTERNS = [
    r"\bwest\s+(flash|debug)\b",
    r"\bidf\.py\b.*\b(flash|app-flash|erase[-_]flash|erase[-_]otadata)\b",
    r"\besptool(\.py)?\b.*\b(write[-_]flash|erase[-_]flash|erase[-_]region|write[-_]mem|load[-_]ram)\b",
    r"\bespefuse(\.py)?\b|\bespsecure(\.py)?\b",
    r"\bst-flash\b|\bSTM32_Programmer_CLI\b|\bnrfjprog\b|\bavrdude\b|\bdfu-util\b",
    r"\bopenocd\b.*\b(program|flash|erase|write_|reset)\b",
    r"\bJLink(Exe)?\b|\bJLink\.exe\b|\bJFlash\b",
    r"\bprobe-rs\s+(download|flash|erase|reset|write|run)\b|\bcargo\s+(flash|embed)\b",
    r"\bwest\s+twister\b.*--device-testing",
    r"\bpio\s+run\b.*(-t|--target)\s+(upload|uploadfs|erase)\b",
    r"\bpytest\b.*--embedded-services\s+\S*(idf|esp)\S*",
    r"\bmcumgr\b|\bimgtool\b.*\bsign\b",
]

def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    cmd = (data.get("tool_input") or {}).get("command", "")
    for pat in PATTERNS:
        if re.search(pat, cmd, re.IGNORECASE):
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": DECISION,
                "permissionDecisionReason": "Gate de hardware: comando pode gravar, apagar ou resetar o dispositivo. Confirme placa, porta, binário e recuperação.",
            }}))
            return 0
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

Notas (Verificado onde indicado):

- Com vários hooks vale o mais restritivo (`deny`, `defer`, `ask`, `allow`); `PreToolUse` com `deny` bloqueia **mesmo em `bypassPermissions`** (V-05). O comportamento de `"ask"` em `bypassPermissions` **não foi verificado**.
- Campos no nível errado são ignorados sem erro: use `claude --debug`.
- `pio test` sem `-e native` grava na placa; inclua regra própria se o projeto usar. `cargo run`/`cargo test` com runner `probe-rs` em `.cargo/config.toml` grava e **não é detectável por texto** (Inferido): trate com permissão `ask` para `cargo`.
- O padrão do `pytest` reflete o serviço `idf`, que grava sozinho (V-38).
- `imgtool sign` e `mcumgr` entram por conterem chave/envio de imagem; ajuste ao seu fluxo.
- Um comando alternativo (`python -c`, script próprio, alias) escapa do filtro: ele é guarda, não segurança (V-63).

## 4. Permissões e sandbox

Exemplo de `.claude/settings.json` (a sintaxe de regras pode variar entre versões; confira em `/permissions`: Inferido):

```json
{
  "permissions": {
    "ask": [
      "Bash(west flash:*)",
      "Bash(west debug:*)",
      "Bash(idf.py flash:*)",
      "Bash(esptool.py:*)",
      "Bash(probe-rs:*)",
      "Bash(cargo flash:*)",
      "Bash(cargo run:*)",
      "Bash(pio run:*)",
      "Bash(openocd:*)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./secrets/**)"
    ]
  },
  "enableAllProjectMcpServers": false
}
```

Por que assim: gravação pede confirmação em vez de ser proibida (o fluxo legítimo existe); `cargo run` entra porque o runner pode gravar; `enableAllProjectMcpServers` falso porque o `.mcp.json` de um projeto vem do git e pode trazer MCP de hardware (V-63). **Sem sandbox, regras `deny` só bloqueiam as ferramentas nativas e o Bash as contorna** (V-63).

Perfil de sandbox para bancada (V-08; precisa de isolamento de arquivos **e** de rede): escrita só no repositório e na pasta de build; rede só para registries e toolchain; porta serial, probe e credenciais de gravação **fora** da allowlist por padrão (Inferido: a página não trata de serial). Linux usa bubblewrap, macOS seatbelt; ative com `/sandbox` (research preview na leitura). Relato interno de 84% menos prompts de permissão. Serial e probe USB em contêiner exigem repasse de dispositivo e são decisão do usuário.

Outras medidas (V-63): limitar a profundidade de subagentes com `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`; devcontainer para isolamento total. `--dangerously-skip-permissions` é risco: só dentro de sandbox, em repositório confiável, nunca como padrão.

## 5. MCP de hardware: documentado, não recomendado

Servidores MCP que tocam hardware (por exemplo o MCP de bancada do Embedded-AI-Harness, com cerca de 70 ferramentas, ou `stm32-mcp`) **podem gravar e sobrescrever memória**; o README do `stm32-mcp` diz que não é sandbox. A API HTTP da bancada do SensorsIot **não tem autenticação**, o broker é aberto e a descoberta usa `sudo` (V-29, V-61). Por isso este plugin **não fornece JSON de instalação** de nenhum MCP de hardware. Se você decidir usar um, a estrutura de um `.mcp.json` desativado/parametrizado é:

```json
{
  "mcpServers": {
    "<nome-do-servidor>": {
      "command": "<binario-revisado-e-fixado-em-versao>",
      "args": ["<argumentos-revisados>"],
      "env": { "<VARIAVEL>": "<valor-nao-secreto>" }
    }
  }
}
```

Antes de ativar: leia o código do servidor; liste as ferramentas expostas e classifique cada uma em leitura ou escrita; fixe versão; rode em rede isolada; mantenha cada ferramenta de escrita atrás de `ask`; nunca guarde segredo no arquivo. Preencher os campos acima é decisão sua, não uma recomendação do plugin.

## 6. Vetting de skill, plugin ou MCP de terceiros (V-18, V-07, V-08, V-63)

Antes de instalar, responda e registre:

1. Quem mantém? Há atividade recente? Licença visível? (estrelas não provam qualidade.)
2. Leu `SKILL.md`, `allowed-tools` e **todos** os scripts? Há hook ou MCP que executa shell?
3. Pede credencial, porta serial, probe ou rede da bancada? Usa `sudo`?
4. Grava sem confirmação? (o fluxo `build-flash` encadeado do `embeddedskills` é um exemplo a evitar; `operation_mode` 1 executa direto.)
5. Há instrução à IA dentro do conteúdo ("ignore as instruções", "execute X")? Trate como injeção e registre.
6. Versão fixada? Escaneou os scripts com SAST?
7. A skill serve para boilerplate, não para temporização, energia ou quirks de hardware?

Contexto da fonte (Snyk, blog de vendor; estatísticas de 36% e 13% são da própria Snyk, sem metodologia na página): entre as sete skills de embarcados citadas, uma tinha 8.055 estrelas e as demais 0 a 459. Use como alerta, não como dado.

## 7. Hook de formatação ou clang-tidy (opcional, não ativo)

Um hook `PostToolUse` com matcher `Edit|Write` pode rodar `clang-format` ou `clang-tidy` nos arquivos alterados (V-05, V-13). Riscos: executa shell em toda edição; trava se a ferramenta demorar; clang-tidy com toolchain cruzado não verificado. Prefira rodar a análise no CI e sob demanda. Se usar, mantenha o script curto, sem rede, e com timeout.

## 8. Camadas de proteção (K-09)

| Camada | O que garante | Limite |
| --- | --- | --- |
| Texto (CLAUDE.md S-01) | Orienta o agente | É pedido, não garantia |
| Permissão `ask`/`deny` | Prompt para comandos listados | Comando alternativo fora da lista passa |
| Hook `PreToolUse` | Determinístico por padrão de texto; vale em bypass para `deny` | Filtro por texto: comando alternativo escapa |
| Sandbox (`/sandbox`) | Contenção de arquivo e rede | Serial/probe dependem de configuração |
| Confirmação humana no chat | Decisão final sobre efeito físico | Exige atenção ao cartão de gravação |

As cinco valem juntas; nenhuma sozinha.
