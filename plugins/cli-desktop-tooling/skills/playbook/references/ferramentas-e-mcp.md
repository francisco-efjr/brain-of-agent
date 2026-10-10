# Ferramentas, permissões, hooks e MCP recomendados (todos DESATIVADOS)

Sumário: 1. Regra do arquivo · 2. Ferramentas · 3. Bloco de permissões · 4. Hook de guardrail em PowerShell · 5. Configuração do hook · 6. Hook de auditoria · 7. Claude em CI · 8. MCP · 9. Validar o próprio plugin · 10. Riscos e limites

## 1. Regra do arquivo

Nada aqui é ativado pelo plugin: ele não traz `hooks/hooks.json`, `.mcp.json`, `.lsp.json` nem `bin/`. Cada item mostra comando ou JSON pronto, quem executa, o risco e a fonte. Instalar ferramenta altera o ambiente do usuário e executa código de terceiros: só com autorização explícita e nomeada (V-26, V-58, V-61). Os exemplos de código e JSON abaixo são da fábrica e **não foram executados**; testar antes de usar. A sintaxe de `settings.json` e de hooks muda por versão do Claude Code: confira a página oficial da versão instalada (`claude --version`; versões mínimas em `fontes.md`, seção 2).

## 2. Ferramentas

| Ferramenta | Para quê | Comando ou uso (conferir na versão instalada) | Quem executa | Risco | Fonte |
| --- | --- | --- | --- | --- | --- |
| `claude plugin validate`, `details`, `eval` | Validar, medir custo e avaliar o próprio plugin | `claude plugin validate <caminho> --strict`; `claude plugin details cli-desktop-tooling`; `claude plugin eval .` | Usuário | Evals gastam tokens (casos x execuções x 2 braços); exigem Claude Code 2.1.269 ou posterior | V-01, V-50 |
| PSScriptAnalyzer | Análise estática de PowerShell | `Install-PSResource PSScriptAnalyzer` ou `Install-Module PSScriptAnalyzer`; depois `Invoke-ScriptAnalyzer -Path <arquivo>` | Usuário | Altera o ambiente; módulo de terceiros (MIT) | V-58 |
| Pester | Testes de PowerShell | `Install-Module -Name Pester -Force -SkipPublisherCheck`; `Invoke-Pester -Output Detailed` | Usuário | Mesmo risco (Apache-2.0); o Windows traz o 3.4.0; `Should -Be` contra `Should-Be` | V-58 |
| ShellCheck | Análise estática de shell | `shellcheck <arquivo>` | Usuário | Binário de terceiros (GPL-3.0, não embutir) | V-61 |
| `signtool` | Assinar e verificar no Windows | `signtool sign /fd SHA256 /tr <url> /td SHA256 ...`; `signtool verify /pa` | Usuário | Chave privada; senha nunca em argumento | V-44 |
| `winget validate`, `wingetcreate`, `YAMLCreate.ps1`, Windows Sandbox | Validar manifesto e testar instalação | `winget validate`; `Tools\SandboxTest.ps1` | Usuário | O PR ao `winget-pkgs` é público; as duas ferramentas oferecem enviar o PR | V-43 |
| `@electron/fuses` | Ler e aplicar fuses | `flipFuses` no gancho `afterPack`/`postPackage` | Usuário | `npx` executa código de terceiros; a fábrica só lê e recomenda | V-48 |
| `windeployqt`, `macdeployqt` | Implantação do Qt | `windeployqt --release --qmldir <dir>`; `macdeployqt ... -sign-for-notarization=<identidade>` | Usuário | A assinatura padrão do `macdeployqt` é ad hoc | V-38 |
| Sparkle `generate_keys`, `generate_appcast` | Chaves EdDSA e appcast | Executados pelo usuário | Usuário | Gera segredo (chaveiro do login) | V-49 |
| `pytest-textual-snapshot`, `cargo-insta`, `teatest` | Snapshot e golden de TUI | `snap_compare`; `cargo insta review`; `teatest` | Usuário | Dependências novas; `teatest` está em `x/exp` | V-30, V-31, V-32 |
| Ruler | Fonte única de regras para vários agentes | `ruler apply --dry-run` antes de aplicar | Usuário | Beta; escreve arquivos de agentes (`.bak` por padrão) | V-28 |

## 3. Bloco de permissões (para `.claude/settings.json` do projeto do usuário)

Destilado de V-51 e V-27. Regras equivalentes para a ferramenta PowerShell do Claude Code: **Não verificado**. Grave o arquivo só com pedido do usuário.

```json
{
  "permissions": {
    "deny": ["Read(./.env)", "Read(./secrets/**)", "Bash(rm -rf *)", "Bash(git push --force *)"],
    "ask": ["Bash(git push *)"]
  },
  "enableAllProjectMcpServers": false
}
```

Notas: a ordem de avaliação é deny, ask, allow (o primeiro que casa decide); regra de Bash casa o texto escrito e não é fronteira (contornos como `git -C . push` e comando composto); `Bash(command:rm *)` é ignorada com aviso; `denyRead` do sandbox não bloqueia a ferramenta Read; no Windows nativo não há sandbox. Para isolar Bash, use WSL2 ou contêiner (V-51). Tabelas de deny mais amplas (chaves SSH/GPG, credenciais de nuvem, `.npmrc`, `.pypirc`, configuração de shell) vêm de V-27 (sem licença, só destilado).

`--dangerously-skip-permissions` e `bypassPermissions` **não** são recomendados: pulam prompts, inclusive em `.git` e `.claude`. Se alguém insistir, só em contêiner ou VM descartável, com repositório confiável, e `permissions.disableBypassPermissionsMode` disponível para travar o modo (V-51).

## 4. Hook de guardrail em PowerShell (exemplo próprio de V-08, não executado)

Guardrail, **não fronteira de segurança**. Lê o evento do stdin, bloqueia remoção recursiva forçada e sai com 2.

```powershell
$evento = [Console]::In.ReadToEnd() | ConvertFrom-Json
$cmd = $evento.tool_input.command
if ($cmd -match '(?i)Remove-Item\b.*-Recurse.*-Force|\brm\s+-rf\b') {
  [Console]::Error.WriteLine('Bloqueado: remoção recursiva forçada. Use Move-Item para uma pasta .trash/ ou peça confirmação ao usuário.')
  exit 2
}
exit 0
```

**Contornos conhecidos (a regex não pega):** `rm -fr`, `rm -r -f`, `Remove-Item -Force -Recurse` em outra ordem, `rd /s /q`, `del /s`, `git clean -fdx`, comando montado por variável ou por `Invoke-Expression`, alias (`ri`, `rd`). Por isso o hook é camada extra, e a mensagem sempre traz a alternativa. Política em código, nunca só em prosa (V-08).

## 5. Configuração do hook (esboço Inferido de V-08 e V-52)

Evento `PreToolUse`, matcher exato `Bash`, handler `command`, `shell: powershell`. `onFailure: "block"` exige v2.1.295 ou posterior; sem ele, timeout em `PreToolUse` não bloqueia. Confira o esquema na página de hooks da versão instalada antes de usar.

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [ { "type": "command", "shell": "powershell", "command": "<caminho do script acima>", "onFailure": "block" } ] }
    ]
  }
}
```

Pontos de atenção:
- No Windows o Claude Code pode expor uma ferramenta `PowerShell` separada de `Bash`: o matcher `Bash` não a cobre. Use `Bash|PowerShell` só depois de conferir o nome da ferramenta na versão instalada (**Não verificado**).
- Só `exit 2` (ou JSON `hookSpecificOutput.permissionDecision: "deny"`) bloqueia; `exit 1` e saída sem JSON válido não bloqueiam; `permissionDecision` fora de `hookSpecificOutput` é ignorado sem erro (`claude --debug` mostra "unrecognized keys").
- Matcher fora de letras, dígitos, `_`, `-`, espaço, `,` e `|` vira regex sem âncora: `Edit.*` também casa `NotebookEdit`; use `^Edit$`.
- `PreToolUse` dispara antes da checagem de modo de permissão: um `deny` bloqueia mesmo em `bypassPermissions`. A decisão `allow` de um hook não vence `deny` nem `ask`.
- Hooks rodam com os privilégios do usuário e fora do sandbox. Hook de plugin só depois da revisão de V-02. Hooks migrados sem apagar o original rodam duas vezes.
- Teste com `claude --debug`; seção de privilégios dos hooks (final da página) não foi lida.

## 6. Hook de auditoria

`PostToolUse` gravando `tool_input.command` em arquivo de log (V-08: não `PreToolUse`). Use `ConvertFrom-Json` no lugar de `jq`. Não registre segredos; o log vai para um caminho fora do repositório.

## 7. Claude em CI (V-09, derivado da documentação, não executado)

`git diff main | claude --bare -p "<instrução de revisão enxuta>" --allowedTools "Read" --output-format json`, com `ANTHROPIC_API_KEY` (o modo `--bare` não usa o login da assinatura e gera cobrança de API), falha do job se `plugin_errors` ou `mcp_server_errors` vier não vazio, e exit 143 tratado como cancelamento. A diff entra por stdin para a ferramenta não precisar de permissão de Bash. A chave fica no cofre do CI, nunca no repositório. Sem `--bare`, `-p` roda hooks e MCP do projeto, mesmo em pasta não confiável.

## 8. MCP

Nenhum servidor MCP é recomendado como ativo por este segmento: o validador não aprovou nenhum específico de CLI ou desktop; V-12 prefere a CLI simples (por exemplo `psql`) a MCP onde ela é confiável; V-51 e V-02 lembram que MCP roda fora do sandbox, que a Anthropic não audita servidores MCP e que plugins podem trazer servidores. Para construir um servidor, `/automation-integrations:playbook` e `mcp-server-dev` (V-55, estudo). Driver de teste de Electron (Playwright e similares): sem fonte validada, Suposição.

Se o usuário pedir um MCP mesmo assim: leia a origem e o código antes; prefira HTTP remoto com autenticação para serviço em nuvem e pacote MCPB para algo que toca a máquina (V-55); mantenha `enableAllProjectMcpServers: false`; registre o risco (processo local com acesso total do usuário).

## 9. Validar o próprio plugin (usuário executa)

1. `python "C:\Users\Francisco Edson\dev-segments\tools\verify_plugin.py" "<pasta do plugin>"` (estrutura, determinístico).
2. `claude plugin validate "<pasta do plugin>" --strict`.
3. `claude --plugin-dir "<pasta>"` e `/reload-plugins`; aba Errors de `/plugin` limpa.
4. `claude plugin details cli-desktop-tooling`: custo "Every turn" abaixo de 2.000 tokens como meta de fábrica (V-50).
5. `claude plugin eval .` só com autorização de gasto; casos marcados `designed_not_executed` até rodar. O CLI local registrado na especificação da fábrica (2.1.128) é anterior a 2.1.269: atualize antes.

## 10. Riscos e limites

Comandos acima não foram executados pela fábrica. Hooks, MCP e regras de Bash têm contornos; a fronteira real é sandbox, deny rules e ambiente isolado. Não instale nada nem edite `settings.json` sem pedido do usuário.
