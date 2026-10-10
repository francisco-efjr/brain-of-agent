# Template de hook de guardrail

Entregue **script + configuração + testes + como desativar**; não ative nada nem edite `settings.json` sem autorização. Hook reduz erro, **não é fronteira de segurança** (H-08): dano irrecuperável exige sandbox, devcontainer ou permissão. Detalhes e eventos: `references/hooks-e-guardrails.md`. Fonte: V-02, V-21, V-24.

## Ficha

| Campo | Preenchimento |
| --- | --- |
| Comportamento a impedir e por quê | |
| Evento e matcher mais estreitos (H-01) | ex.: `PreToolUse` + `Bash` |
| Versão do Claude Code (para `onFailure` v2.1.295+) | |
| Onde viveria (projeto / usuário / skill) | |
| Interpretador no PATH (`python`, `python3`, `py`) | |
| Falsos positivos aceitos | |

## Esqueleto do script (stdlib; edite `RULES`)

Este esqueleto em regex é o mínimo. Para uso real prefira `${CLAUDE_PLUGIN_ROOT}/skills/writing-hook-guardrails/references/guard-bash.md` (tokeniza com `shlex`, trata `bash -c`, `env`, `find -delete` e alvos `..`, com 37 casos de teste).

```python
import json, re, sys

data = json.load(sys.stdin)
cmd = (data.get("tool_input") or {}).get("command", "")

RULES = [
    # (regex, mensagem com a ALTERNATIVA)
    (r"\bgit\s+reset\s+--hard\b", "Use git stash ou um branch de backup antes."),
    (r"\bgit\s+push\b.*(\s--force(?![-\w])|\s-f\b)", "Use --force-with-lease em branch próprio e peça autorização."),
    (r"\brm\s+(-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*|-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*|(-[rR]\s+-f|-f\s+-[rR]))\s+(/|~|\$HOME)", "Remova apenas caminhos dentro do projeto."),
]
for pattern, alternativa in RULES:
    if re.search(pattern, cmd):
        print(f"Bloqueado ({pattern}). {alternativa}", file=sys.stderr)
        sys.exit(2)     # exit 2 bloqueia PreToolUse; exit 1 NÃO bloqueia
sys.exit(0)             # nada além de JSON no stdout
```

## Casos de teste (H-06) — cole exit code e stderr reais

| Comando simulado | Esperado | Obtido |
| --- | --- | --- |
| `rm -rf /` · `rm -fr ~` · `rm -r -f $HOME` · `rm -rf /etc` | exit 2 | |
| `git push --force origin main` · `git push -f` · `git reset --hard HEAD~1` | exit 2 | |
| `rm -rf ./build` · `git push --force-with-lease` · `git reset --soft HEAD~1` · `ls -la` | exit 0 | |
| Falso positivo conhecido: `git commit -m "docs: git push --force"` | exit 2 (aceitar ou ajustar) | |
| [comando parecido do SEU projeto que deve passar] | exit 0 | |

Reproduzir: `echo '{"tool_input":{"command":"rm -rf /"}}' | python guard.py; echo $?`

## Configuração (apenas documentada)

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [ { "type": "command", "command": "python", "args": ["<CAMINHO>/guard.py"], "timeout": 10, "onFailure": "block" } ] }
    ]
  }
}
```

## Checklist H-01..H-08

- [ ] H-01 evento e matcher estreitos · [ ] H-02 script nomeado, JSON do stdin · [ ] H-03 exit 2 + stderr acionável (ou `permissionDecision`) · [ ] H-04 `timeout` e `onFailure` explícitos · [ ] H-05 nada além do JSON no stdout · [ ] H-06 testes com perigoso e parecido inofensivo · [ ] H-07 como desativar · [ ] H-08 ressalva de sandbox na entrega

## Como desativar

Remover o bloco `hooks` do arquivo de settings (ou da skill) e reiniciar a sessão. Limites conhecidos do script: aspas em `"$HOME"`, `rm --recursive --force`, expansão posterior de variáveis e `python -c` com chamadas de biblioteca não são pegos.
