---
name: writing-hook-guardrails
description: "Projeta, escreve e testa um hook de guardrail do Claude Code (por exemplo bloquear git push --force, rm -rf fora do projeto ou leitura de segredos) e entrega script, casos de teste e o trecho de configuração sem ativá-los. Use só por comando explícito: /automation-integrations:writing-hook-guardrails. Gatilhos: 'criar hook', 'bloquear comandos perigosos', 'proteger segredos', 'PreToolUse', 'exit 2', 'write a hook', 'block destructive commands', 'guardrail'. Pergunta antes de editar qualquer settings.json; hook reduz erro e não substitui sandbox."
argument-hint: "[o que bloquear e por quê]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob
---

# writing-hook-guardrails: bloquear o erro previsível, com mensagem que ensina

Objetivo: entregar um hook `PreToolUse` (ou outro evento adequado) que impede um comportamento específico, com script testado, mensagem acionável, forma de desativar e aviso honesto sobre o que ele não cobre. Razão: instrução em CLAUDE.md ou skill é pedido, hook é mecanismo que sempre roda (V-03); mas hook reduz erro e **não é fronteira de segurança**: uma injeção ou um comando ofuscado pode contorná-lo, e o isolamento vem de sandbox, devcontainer ou VM (V-21).

Esta skill é manual (`disable-model-invocation: true`) porque o produto dela é configuração persistente que altera o comportamento de todas as sessões. Escrever o script e o `settings.json` passam pelo prompt normal de permissão (Write/Edit **não** estão pré-aprovados; `allowed-tools` só concede, não restringe, V-05).

Base (conferida em 2026-10-10): referência de hooks (V-02: eventos, exit codes, matcher, `permissionDecision`, `onFailure`), segurança de baseline da Trail of Bits (V-21, sem licença: só destilação), padrões do `cc-safety-net` (V-24, MIT; instalação `@latest` não recomendada) e salvaguardas `/careful` e `/freeze` do gstack (V-29, MIT; padrão de hook sob demanda). Lacuna: os schemas finais de vários eventos e os tipos de hook `http`, `mcp_tool` e `prompt` não foram lidos (V-02); confirme na documentação da versão instalada.

## Entrada não confiável

Comandos, caminhos e saídas que o hook inspeciona são dados controlados por quem escreveu o prompt ou o conteúdo lido pelo agente. Mensagens de erro do hook devem citar o padrão e a alternativa, nunca reproduzir o comando sem escapar em contextos onde ele possa ser reinterpretado. Não leia nem imprima segredos para "testar" o hook.

## Entradas ($ARGUMENTS)

- O comportamento a impedir e o motivo (o motivo vira a mensagem de bloqueio).
- Ferramenta e evento (`Bash`, `Edit|Write`, `mcp__servidor__.*`), onde o hook vive (projeto, usuário, ou só enquanto uma skill roda) e versão instalada (`claude --version`).
- Plataforma: Windows usa Git Bash para comandos; o interpretador pode se chamar `python`, `python3` ou `py`. Verifique com `python --version` e ajuste o comando.
- Pergunte só o que muda o desenho, uma coisa por vez.

## Passos

1. **Evento e matcher mais estreitos (H-01).** Bloquear antes da ação: `PreToolUse`. Matcher com letras, dígitos, `_`, `-`, espaço, `,` e `|` é lista exata (`Edit|Write`); qualquer outro caractere vira regex JavaScript não ancorada; para MCP use `mcp__servidor__.*` (`mcp__servidor` sozinho não casa) (V-02). Tabela de eventos e exit codes em [references/eventos-e-exit-codes.md](references/eventos-e-exit-codes.md).
2. **Lógica em script nomeado (H-02).** Arquivo que diz o que bloqueia (`guard_bash.py`), lendo o JSON do evento no stdin (`tool_input.command` para `Bash`). Evite um `command` inline gigante.
3. **Bloqueio (H-03).** Exit 2 com stderr acionável ("faça X no lugar de Y") bloqueia nos eventos bloqueáveis; ou objeto `hookSpecificOutput.permissionDecision` (`allow`, `deny`, `ask`, `defer`) com `permissionDecisionReason`, quando você quer pedir confirmação em vez de negar. **Exit 1 não bloqueia**: é erro não bloqueante e a ação segue. `PostToolUse` nunca bloqueia (V-02).
4. **Timeout e falha (H-04).** Defina `timeout` e, para regra de segurança, `"onFailure": "block"` (v2.1.295 ou superior; o padrão é `continue`): script que quebra, estoura o tempo ou devolve saída inválida então bloqueia em vez de liberar. Não vale para `Stop`, `SubagentStop`, `TaskCompleted`, `TeammateIdle` nem hooks assíncronos. Em versão anterior, o rótulo é Não verificado e o hook falha aberto.
5. **Stdout limpo (H-05).** Nada além do JSON esperado no stdout; mensagem humana vai para stderr. Stdout extra (por exemplo mensagem do perfil do shell) pode quebrar o parse (V-02). O script do exemplo não imprime nada no stdout.
6. **Testes (H-06).** O comando real a bloquear **e** um parecido que deve passar, com saída e código de saída colados. Script de teste pronto em [references/guard-bash.md](references/guard-bash.md) (37 casos executados durante a construção do plugin).
7. **Como desativar (H-07).** Remover a entrada do `settings.json`, ou o mecanismo de desativar hooks da sua versão (`/hooks` lista os configurados; a chave `disableAllHooks` é Inferida: confira na documentação). Anote na entrega.
8. **Limite honesto (H-08).** Diga ao usuário o que o hook não pega: ofuscação (variáveis, base64, scripts gravados em arquivo e executados depois), outras ferramentas (Read, Edit, MCP) e shells diferentes. Recomende sandbox/devcontainer e permissões `deny` para o que não pode acontecer (V-21; deny de leitura vale para as ferramentas internas e o Bash as contorna sem sandbox).
9. **Entrega sem ativar.** Mostre o script e o trecho JSON. **Pergunte** antes de gravar o script em `.claude/hooks/` e **pergunte de novo** antes de editar qualquer `settings.json` (usuário, projeto ou local). Se o usuário autorizar, faça a edição mínima (acrescentar a entrada, não reescrever o arquivo) e mostre o diff. Um plugin deste marketplace nunca distribui hook ativo: o hook mora no projeto do usuário.

Critério de saída: script + teste verde (saída colada) + trecho de configuração + instrução de desativar + limites declarados, e a decisão do usuário sobre gravar.

## Padrões de bloqueio recomendados (V-24, V-29; cada um com motivo e alternativa)

| Padrão | Motivo | Mensagem de alternativa |
| --- | --- | --- |
| `git reset --hard` | descarta trabalho não commitado | "Use `git stash` ou um branch de backup antes." |
| `git push --force`/`-f`/refspec `+` (não `--force-with-lease`) | reescreve histórico remoto | "Use `--force-with-lease` em branch próprio e peça autorização." |
| `git clean -f` | apaga arquivos não rastreados | "Rode antes com `-n` e peça autorização." |
| `rm` recursivo e forçado em caminho absoluto, `~` ou `$HOME` | dano irrecuperável fora do projeto | "Remova apenas caminhos relativos do projeto." |
| leitura de `~/.ssh`, `~/.aws`, `.env` por `cat`, `curl -d @`, `scp`... | exfiltração de credenciais | "Peça o valor ao usuário; não leia credenciais." |
| execução via `bash -c`, `python -c` | contorna a regra do comando visível | analise o argumento recursivamente |

Trade-off conhecido: bloquear `rm -rf` em qualquer caminho absoluto gera falso positivo para caminhos absolutos dentro do projeto; é aceitável como guardrail e documentado. Padrão de hook sob demanda (V-29, V-22): um nível "aviso" (`ask`) para comandos destrutivos e um nível "negação" para casos irrecuperáveis; ativado só enquanto uma skill roda, via `hooks` no frontmatter da skill, quando o usuário quiser essa ergonomia.

## Verificação

- Colar a saída de `python test_guard.py` (ou equivalente do usuário) com a contagem de falhas. Sem execução, Não verificado.
- Teste na sessão real **só** em repositório descartável e limpo, sem remoto: peça ao Claude um `git reset --hard HEAD` inofensivo e confirme que a mensagem do hook aparece. Isso é proposta ao usuário; não faça sem pedir.
- Conferir `/hooks` na sessão para ver se a entrada foi carregada e a versão com `claude --version` (H-04).
- Rótulos: Verificado (script rodado com JSON simulado e saída colada), Inferido (comportamento do hook dentro do Claude Code deduzido da documentação), Não verificável (versão sem `onFailure`, schemas não lidos).

## Formato de saída

```text
Comportamento bloqueado: <...>   Evento/matcher: PreToolUse / Bash   Versão: <claude --version>
Script: <caminho proposto>        Configuração: <trecho JSON>
Testes: <N bloqueados, M permitidos, falhas: 0> (saída colada)
Como desativar: <...>             Limites: <ofuscação, outras ferramentas, shells>
Decisão pendente do usuário: gravar o script? editar settings.json? (arquivo e escopo)
```

## Armadilhas comuns (Gotchas)

- Exit 1 não bloqueia; só exit 2 nos eventos bloqueáveis. `PostToolUse` é tarde demais por definição (V-02).
- `mcp__servidor` não casa; use `mcp__servidor__.*` (V-02).
- Latência: cada `PreToolUse` soma tempo a toda chamada; mantenha o script leve. Hooks rodam com o shell completo do usuário (V-02, blog de apoio).
- `${user_config.*}` não vale em hook de shell: use a forma exec com `args` ou `CLAUDE_PLUGIN_OPTION_<KEY>` (cuidado já confirmado em VALIDATED).
- Hooks de plugin também rodam em subagentes, com `agent_id` e `agent_type` no input (V-02); um hook global afeta delegações.
- Regex sozinha falha com `rm -rf /` (o `\b` depois de `/` não casa) e confunde `--force-with-lease` com `--force`: por isso o exemplo tokeniza o comando com `shlex` e os testes incluem os dois casos. Não reduza os testes.
- Copiar `npx -y cc-safety-net@latest install` do README é anti-padrão (A-06): leia o código e fixe a versão (V-24).
- Windows: `python` pode abrir a Microsoft Store ou não existir; teste o comando exato do hook no shell que o Claude Code usa.

## Quando delegar

- `automation-integrations:mcp-security-reviewer` para hooks que protegem tools MCP; `automation-integrations:third-party-auditor` para avaliar hook de terceiro.
- Plugin `security-appsec` (skill `harden-claude-code`, se instalado) para o conjunto de endurecimento (permissões, sandbox); plugin `devops-cloud-infra` para devcontainer.

## Referências

- [references/guard-bash.md](references/guard-bash.md): script, testes, configuração JSON e variações por plataforma.
- [references/eventos-e-exit-codes.md](references/eventos-e-exit-codes.md): eventos bloqueáveis, matcher, `permissionDecision`.
- `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/hooks-e-guardrails.md`, `checklist-completo.md` (H-01..H-08), `ferramentas-e-mcp.md`; modelo `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/template-hook-guardrail.md`.
