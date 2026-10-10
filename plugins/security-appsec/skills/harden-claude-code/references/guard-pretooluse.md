# Guard PreToolUse com falha fechada (documentado, não ativado)

Fontes (conferidas em 2026-10-10): documentação de hooks e guia de hooks do Claude Code, https://code.claude.com/docs/en/hooks e https://code.claude.com/docs/en/hooks-guide (V-06); teste de guard com marcador (V-07, dev.to, classe B); desenho de guard `careful` do gstack (MIT, via brain-of-agent, **Inferido (brain)**). Redação própria. Nenhum hook é entregue pelo plugin: este arquivo é para o usuário copiar conscientemente. Confira na documentação da versão instalada o esquema de entrada e de registro.

## Sumário

1. Semântica que importa
2. Esqueleto do guard (falha fechada, duas camadas)
3. Registro
4. Teste do marcador
5. Variante "ask" estilo careful: o que adotar e o que não portar
6. Limites

## 1. Semântica que importa (V-06)

- `exit 2` bloqueia a chamada e envia o stderr ao Claude como motivo (vale mesmo se o JSON disser allow).
- JSON com `permissionDecision: "deny"` e `exit 0` também nega; `exit 0` sem decisão deixa o fluxo normal de permissão seguir.
- `exit 1` e outros códigos são erros **não bloqueantes**. Timeout em PreToolUse **não bloqueia**. Por padrão o hook falha aberto.
- `"onFailure": "block"` (Claude Code 2.1.295 ou superior) faz falha, timeout e saída inválida bloquearem. Confira a versão antes de depender disso.
- O campo `if` do hook é de melhor esforço para Bash. Saída acima de 10.000 caracteres vai para arquivo e o Claude não é instruído a lê-lo. O stdout deve conter só JSON: eco de perfil de shell quebra o parse.
- Decisão de hook não contorna regras de `deny`/`ask` do sistema de permissões.
- Em plugin, `hooks` no frontmatter de subagente é ignorado; o guard vive nas configurações do projeto ou do usuário.

## 2. Esqueleto do guard (falha fechada, duas camadas)

Camada 1 nega o que é catastrófico e simples de reconhecer; camada 2 pede confirmação (`ask`) para o que é destrutivo mas às vezes legítimo. Qualquer exceção bloqueia. Salve como `.claude/hooks/guard.py` (o nome é livre). As expressões regulares são heurísticas e contornáveis; ajuste ao seu projeto.

```python
#!/usr/bin/env python3
"""PreToolUse (Bash): falha fechada. Erro, entrada inesperada ou exceção => exit 2."""
import json, os, re, sys, time

NEGAR = [  # (padrão, motivo) - catastróficos
    (r"\brm\s+(-\w+\s+)*-\w*[rR]\w*\s+(/|~|\$HOME)/?(\s|$)", "remoção recursiva da raiz ou da home"),
    (r"\b(curl|wget)\b[^|;&\n]*\|\s*(sudo\s+)?(sh|bash)\b", "execução de script remoto por pipe"),
]
CONFIRMAR = [  # exigem confirmação humana
    (r"\brm\s+(-\w+\s+)*-\w*[rR]", "remoção recursiva"),
    (r"\bgit\s+push\b.*(--force(?![-\w])|(?<!\S)-f(?!\S))", "git push --force"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard"),
    (r"\b(drop\s+(table|database)|truncate)\b", "SQL destrutivo"),
    (r"\bkubectl\s+delete\b", "kubectl delete"),
    (r"\bdocker\s+(rm\s+-f|system\s+prune)\b", "docker rm -f / system prune"),
]
EXCECOES_RM = r"\brm\s+(-\w+\s+)*-\w+\s+(\./)?(node_modules|dist|build|\.next|__pycache__|\.cache|coverage)/?(\s|$)"

for _fluxo in (sys.stdin, sys.stdout, sys.stderr):        # evita texto corrompido no Windows
    try:
        _fluxo.reconfigure(encoding="utf-8")
    except Exception:
        pass

def bloquear(motivo):
    print(f"Bloqueado pelo guard: {motivo}. Peça confirmação ao usuário.", file=sys.stderr)
    sys.exit(2)

try:
    if os.environ.get("GUARD_SIMULATE_ERROR") == "1":      # só para o teste do marcador
        raise RuntimeError("erro simulado")
    if os.environ.get("GUARD_SIMULATE_HANG") == "1":       # só para o teste de timeout
        time.sleep(60)
    cmd = json.load(sys.stdin)["tool_input"]["command"]
    for padrao, motivo in NEGAR:
        if re.search(padrao, cmd, re.I):
            bloquear(motivo)
    # A exceção vale só para o padrão de rm e só em comando simples (sem ; && || | ou quebra de linha),
    # para que "rm -rf node_modules && git push --force" continue pedindo confirmação.
    rm_inofensivo = bool(re.search(EXCECOES_RM, cmd)) and not re.search(r"[;&|\n]", cmd)
    for padrao, motivo in CONFIRMAR:
        if motivo == "remoção recursiva" and rm_inofensivo:
            continue
        if re.search(padrao, cmd, re.I):
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": f"Comando potencialmente destrutivo: {motivo}"}}))
            sys.exit(0)
except SystemExit:
    raise
except Exception as e:                                     # qualquer falha nega
    print(f"Hook falhou ({type(e).__name__}); bloqueando por segurança.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
```

Notas: a decisão `ask` aninhada em `hookSpecificOutput` segue o desenho observado no `careful` (**Inferido (brain)**: um `permissionDecision` no nível raiz foi relatado como ignorado; confirme na doc). `GUARD_SIMULATE_*` só pioram o resultado (bloqueio), então não abrem brecha. O stdout só tem JSON ou nada. Comandos compostos (`;`, `&&`, `|`) podem escapar aos padrões simples: o guard é aviso, não política.

## 3. Registro

Em `.claude/settings.json` (ou `.local.json`); o usuário edita. Confirme na documentação de hooks da versão o local exato de `onFailure`, a variável de caminho do projeto e a unidade de `timeout` (**Inferido** a partir de V-06).

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard.py\"",
            "timeout": 5,
            "onFailure": "block"
          }
        ]
      }
    ]
  }
}
```

No Windows, o executável pode ser `python` ou `py -3` em vez de `python3`; prefira executar dentro do WSL2/dev container onde o sandbox também existe. Sem `onFailure` (versões anteriores à 2.1.295), a única garantia de falha fechada é o `try/except` com `exit 2` do próprio script, e timeout continua sem bloquear.

## 4. Teste do marcador (V-07)

Provar que o guard bloqueia quando falha, em diretório descartável:

1. Registre o guard e adicione temporariamente um padrão de teste em `NEGAR` que case com um comando inócuo, por exemplo `GUARD_TEST_MARKER`.
2. Peça ao Claude: `touch marcador.txt  # GUARD_TEST_MARKER`. Esperado: bloqueado e `marcador.txt` não existe.
3. Falha interna: inicie a sessão com `GUARD_SIMULATE_ERROR=1` e peça `touch marcador2.txt`. Esperado: bloqueado (o `except` devolve `exit 2`); se `marcador2.txt` existir, o guard falha aberto: corrija antes de habilitar.
4. Timeout: com `GUARD_SIMULATE_HANG=1` e `"timeout": 5`, peça `touch marcador3.txt`. Com `onFailure: "block"` deve bloquear; sem o campo, o comando passa (comportamento documentado): nesse caso não dependa do guard para política.
5. Saída inválida: troque temporariamente o final por `print("lixo")` e repita; confirme o comportamento.
6. Remova o padrão de teste, os marcadores e as variáveis, e só então habilite o guard no projeto real.
7. Combine com `permissions.deny` e sandbox. Hook sozinho é consultivo diante da aprovação do usuário no prompt (relato do HN em V-07, **Inferido**).

Registre o resultado de cada passo como Verificado (feito pelo usuário) ou Não verificável. O experimento do dev.to tratava de *mods* e não de hooks; o comportamento de falha aberta dos hooks foi confirmado separadamente na documentação oficial.

## 5. Variante "ask" estilo careful: o que adotar e o que não portar

Adote (Inferido (brain), gstack `careful`, MIT): tabela de padrões destrutivos (`rm -r`, `DROP TABLE`, `TRUNCATE`, `git push --force`, `git reset --hard`, `git checkout .`, `git restore .`, `kubectl delete`, `docker rm -f`, `docker system prune`); exceções seguras para limpeza de artefatos (`node_modules`, `.next`, `dist`, `__pycache__`, `.cache`, `build`, `.turbo`, `coverage`); hard deny só para `rm -r` de `/`, `~` ou `$HOME` e force-push na branch padrão, e só em comandos simples; `--force-with-lease` nunca entra no hard deny; padrões do projeto são somente aditivos (a configuração pode acrescentar regras, nunca suprimir as de base); o próprio `careful` se descreve como aviso de melhor esforço, não como política.

Não porte: a gravação de analytics em diretório de estado do gstack, o carregamento por skill com hooks em frontmatter (não é entregue por plugin) e qualquer dependência do launcher do gstack.

## 6. Limites

- Regex não é parser de shell: `bash -c "rm -rf ..."`, variáveis, aliases e codificações passam. O guard reduz acidentes, não impede um atacante determinado.
- Hooks rodam com os privilégios do usuário: revise o script como código, versione, e proteja `.claude/hooks/` de edição não revisada (arquivo crítico).
- Hook que bloqueia demais é desligado pelo time: comece em `ask`, meça, e só então endureça.
