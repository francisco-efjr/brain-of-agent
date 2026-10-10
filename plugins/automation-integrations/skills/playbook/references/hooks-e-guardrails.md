# Hooks e guardrails do Claude Code

Para projetar, escrever e testar hooks de guardrail. Este plugin **não ativa** nenhum hook: entregue script e trecho de configuração e deixe o usuário habilitar. Edição de `settings.json` ou de qualquer configuração persistente só depois de pergunta e resposta afirmativa. Checklist: H-01..H-08 em `checklist-completo.md`.

Sumário: 1. O que hook garante e o que não · 2. Eventos, exit codes e matcher · 3. Receita passo a passo · 4. Script de exemplo testado · 5. Configuração (documentada, desativada) · 6. Padrões de bloqueio e limites · 7. Hook sob demanda · 8. Plugins e subagentes · 9. Gotchas · 10. Como desativar

## 1. O que hook garante e o que não (V-02, V-03, V-21)

- Instrução em CLAUDE.md ou skill é **pedido**; hook e permissão são **mecanismo**. O que deve valer sempre vira hook; o que nunca pode ocorrer vira hook, permissão ou configuração gerenciada (V-03).
- Hook **reduz erro** e dá mensagem acionável. Não é fronteira de segurança: uma injeção de prompt pode contorná-lo e regex tem bypass (V-21). Dano irrecuperável exige sandbox, devcontainer, VM ou permissão deny. Repita essa ressalva em toda entrega de hook (H-08).
- Cada hook `PreToolUse` soma latência (hooks de log podem ser assíncronos) e roda com o shell completo do usuário (V-02, blog de apoio).

## 2. Eventos, exit codes e matcher (V-02; conferir na versão instalada)

Exit codes: `0` = sucesso; `2` = bloqueia **nos eventos bloqueáveis**; qualquer outro código (inclusive `1`) = erro não bloqueante, **a ação segue**.

| Comportamento do exit 2 | Eventos |
| --- | --- |
| Bloqueia | `PreToolUse`, `UserPromptSubmit`, `UserPromptExpansion`, `Stop`, `SubagentStop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `ConfigChange` (exceto `policy_settings`), `PreCompact`, `PreModelSwitch`, `Elicitation`, `ElicitationResult`, `PostToolBatch`, `WorktreeCreate/Remove` |
| Não bloqueia | `PostToolUse`, `PostToolUseFailure`, `PermissionDenied`, `Notification`, `SessionStart` |
| Não honrado | `PermissionRequest`: use o objeto `decision` |

A doc lista 33 eventos; um blog de apoio fala em 27. A doc prevalece e muda: confira a página atual e `claude --version` (V-02, ~62% da página não lido na consulta; schemas de `SubagentStop`, `WorktreeCreate`, `PermissionRequest`, tipos `http`/`mcp_tool`/`prompt`: Não verificável aqui).

**Matcher:** `*`, vazio ou ausente = tudo. Só letras, dígitos, `_`, `-`, espaço, `,` e `|` = lista exata (`Edit|Write`). Qualquer outro caractere = regex JavaScript **não ancorada**. Para MCP use `mcp__servidor__.*`; `mcp__servidor` sozinho **não casa**.

**Decisão estruturada em `PreToolUse`:** `hookSpecificOutput.permissionDecision` ∈ `allow | deny | ask | defer`, com `permissionDecisionReason` (V-02). Forma ilustrativa (confirme `hookEventName` no schema da versão): 

```json
{ "hookSpecificOutput": { "hookEventName": "PreToolUse", "permissionDecision": "deny",
    "permissionDecisionReason": "Use git stash antes de reset --hard." } }
```

**`onFailure`:** `"block"` (v2.1.295+; padrão `continue`) faz falha, timeout ou saída inválida **bloquearem**. Não vale para `Stop`, `SubagentStop`, `TaskCompleted`, `TeammateIdle` nem hooks assíncronos. Use `block` em regra de segurança; sem a versão mínima, rotule Não verificado.

## 3. Receita passo a passo

1. **Comportamento:** o que impedir e por quê (uma frase). Entrada do usuário: versão do Claude Code, onde o hook viveria (projeto, usuário, skill).
2. **Evento e matcher mais estreitos** (H-01): `PreToolUse` + `Bash` para comandos; `Edit|Write` para arquivos; `mcp__servidor__.*` para MCP.
3. **Script nomeado** que diz o que bloqueia (`guard_destructive_git.py`), lê o JSON do stdin (H-02).
4. **Bloqueio** com exit 2 e stderr acionável: "faça X em vez de Y" (H-03).
5. **`timeout` e `onFailure`** explícitos (H-04).
6. **Nada além do JSON no stdout** (H-05): mensagem do perfil do shell quebra o parse.
7. **Testes** (H-06): comando perigoso bloqueado e um parecido inofensivo liberado; cole saída e exit code.
8. **Como desativar** (H-07) e a ressalva de sandbox (H-08).
9. **Entrega:** script + trecho JSON; **pergunte** antes de editar qualquer `settings.json`.

## 4. Script de exemplo testado

Este é o exemplo curto, baseado em regex. A versão mais robusta (tokeniza com `shlex`, analisa `bash -c`, `env -i`, `find -delete`, alvos `..` e não bloqueia texto entre aspas) está em `${CLAUDE_PLUGIN_ROOT}/skills/writing-hook-guardrails/references/guard-bash.md`, com 37 casos de teste; prefira-a para uso real.

Redação própria, stdlib. As regex foram corrigidas após revisão: a versão ingênua não bloqueava `rm -rf /` (`\b` após `/` não casa) e bloqueava `--force-with-lease`, a própria alternativa sugerida. Testadas localmente com o script abaixo (execução do script em Python 3, não do hook dentro do Claude Code: Verificado para o script, Não verificado para o hook).

```python
import json, re, sys

data = json.load(sys.stdin)                       # JSON do evento no stdin
cmd = (data.get("tool_input") or {}).get("command", "")

RULES = [
    (r"\bgit\s+reset\s+--hard\b",
     "Use git stash ou um branch de backup antes."),
    # --force e -f, mas NÃO --force-with-lease (a alternativa sugerida)
    (r"\bgit\s+push\b.*(\s--force(?![-\w])|\s-f\b)",
     "Use --force-with-lease em branch próprio e peça autorização."),
    # rm com -r e -f em qualquer ordem/forma, mirando /, ~ ou $HOME
    (r"\brm\s+(-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*|-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*|(-[rR]\s+-f|-f\s+-[rR]))\s+(/|~|\$HOME)",
     "Remova apenas caminhos dentro do projeto."),
]
for pattern, alternativa in RULES:
    if re.search(pattern, cmd):
        print(f"Bloqueado ({pattern}). {alternativa}", file=sys.stderr)
        sys.exit(2)                               # exit 2 bloqueia PreToolUse
sys.exit(0)                                       # nada além de JSON no stdout
```

**Casos de teste (H-06), resultado observado ao rodar o script com JSON simulado em 2026-10-10:**

| Comando simulado | Exit | |
| --- | --- | --- |
| `rm -rf /` · `rm -fr ~` · `rm -r -f $HOME` · `rm -rf /etc` · `rm -rf $HOME/x` | 2 | bloqueado |
| `git push --force origin main` · `git push -f` · `git reset --hard HEAD~1` | 2 | bloqueado |
| `rm -rf ./build` · `git push --force-with-lease` · `git reset --soft HEAD~1` · `ls -la` | 0 | liberado |

Como reproduzir: `echo '{"tool_input":{"command":"rm -rf /"}}' | python guard.py; echo $?`.

**Limites conhecidos (documente na entrega):** não pega `rm -rf "$HOME"` (aspas), `rm --recursive --force /`, variáveis expandidas depois, nem `python -c "import shutil; shutil.rmtree('/')"`; `rm -rf` em **qualquer caminho absoluto** dentro do projeto gera falso positivo (aceitável como guardrail; ajuste a regra). Windows: o comando `python` pode não existir no PATH; use `py` ou `python3` conforme o ambiente. Esses limites são a razão do H-08: o hook é um aviso, não um muro.

## 5. Configuração (apenas documentada; o usuário habilita)

Forma exec com `args` (recomendada, V-02). Em plugin, o arquivo é `hooks/hooks.json` com a chave `hooks` no topo e `${CLAUDE_PLUGIN_ROOT}` vale em `command` e `args`; **este plugin não o distribui**. Em projeto, o mesmo bloco vai em `.claude/settings.json` (ou `settings.local.json`; Inferido, confirme a hierarquia na doc).

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python",
            "args": ["<CAMINHO-DO-SCRIPT>/guard.py"],
            "timeout": 10, "onFailure": "block" }
        ]
      }
    ]
  }
}
```
`onFailure` exige v2.1.295+; sem isso, remova o campo e aceite que falha do hook não bloqueia. Schema final dos eventos não foi lido por completo: valide na doc e na versão instalada (Inferido). `${user_config.*}` não vale em hook de shell; use a forma exec com `args` ou a variável `CLAUDE_PLUGIN_OPTION_<KEY>`.

## 6. Padrões de bloqueio e alternativas (V-24 cc-safety-net, V-29 gstack; redação própria)

| Padrão | Por quê | Alternativa na mensagem |
| --- | --- | --- |
| `git reset --hard`, `git clean -f`, `git push --force` (não `--force-with-lease`) | Perde trabalho não commitado ou histórico remoto | stash/backup; `--force-with-lease` em branch próprio com autorização |
| `rm -rf` fora do projeto (/, ~, $HOME) | Dano irrecuperável | remover só caminhos do projeto |
| Leitura de `~/.ssh`, `.env`, `~/.aws`, credenciais de CLI | Segredo no contexto = exfiltrável | usar variável de ambiente injetada; pedir ao usuário |
| Execução via wrapper (`bash -c`, `python -c`) | Contorna regra por comando | tratar o texto do wrapper também (regex acima já procura em toda a linha) |
| Escrita fora de um diretório combinado | Edição fora do escopo | `/freeze`-like: restringir `Edit\|Write` a um diretório |

cc-safety-net (MIT, B) inspecionou esses padrões, inclusive dentro de wrappers; sua instalação recomendada usa `@latest` — não a use (A-06). gstack `/careful` avisa antes de comandos destrutivos e **nega** de forma definitiva recursivos em raiz/home e force-push no branch padrão; `/freeze` limita edições a um diretório; `/guard` junta os dois (V-29, B, nota 72). Padrão útil: nível "aviso" para comandos destrutivos comuns e nível "negação" para casos irrecuperáveis.

## 7. Hook sob demanda (V-05, V-22, V-29)

Skill com `hooks` no frontmatter registra o hook ao ser invocada; vale da invocação até o fim da sessão (V-05). Use para guardrails que só fazem sentido numa atividade (ex.: congelar edições a um diretório durante uma refatoração), evitando latência permanente. Combine com `disable-model-invocation: true` quando a skill muda o comportamento da sessão.

## 8. Plugins e subagentes (V-02, C-01)

Hooks de plugin, de settings e de política gerenciada **também rodam dentro de subagentes**, com `agent_id` e `agent_type` no input (V-02, Verificado). Uma restrição mais estreita sobre `hooks`/`mcpServers` no frontmatter de agente distribuído por plugin é **Não verificável**: os agentes deste plugin não declaram `hooks`, `mcpServers` nem `permissionMode`.

## 9. Gotchas

- `exit 1` não bloqueia; `PostToolUse` nunca bloqueia.
- `mcp__servidor` não casa; `mcp__servidor__.*` casa.
- Perfil do shell que imprime algo (banner, `echo`) polui o stdout e quebra o JSON.
- Hook lento em `PreToolUse` atrasa **toda** chamada da ferramenta casada; mantenha timeout curto, ou torne hooks de log assíncronos.
- `enableAllProjectMcpServers` em settings commitado é outro assunto: ver `seguranca-de-integracoes.md`.
- Regex que procura em toda a linha também casa texto inofensivo: `git commit -m "docs: git push --force"` é bloqueado pelo script acima. Inclua esse caso em H-06 e decida se o falso positivo é aceitável.

## 10. Como desativar

Remova o bloco `hooks` do arquivo de settings (ou da skill) e reinicie a sessão; em plugin, desabilite o plugin. Registre isso no runbook/README da entrega (H-07).

Fonte: V-02, V-03, V-05, V-21, V-22, V-24, V-29. Verificado em 2026-10-10 (itens V); script testado localmente.
