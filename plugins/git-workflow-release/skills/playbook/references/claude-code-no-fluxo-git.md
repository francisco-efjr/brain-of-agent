# Claude Code no fluxo de git

O que a documentação oficial diz sobre o ciclo de trabalho, checkpoints, skills com efeito colateral, hooks, worktrees e CLAUDE.md, e como este plugin se apoia nisso. Fontes por ID em [fontes.md](fontes.md). A documentação muda: confira `claude --version` e as páginas citadas (a pesquisa viu Claude Code 2.1.296 no repositório; o CLI local da fábrica é 2.1.128).

## Sumário

1. Ciclo oficial: explorar, planejar, implementar, commitar
2. Checkpoints não substituem git
3. Skills com efeito colateral: `disable-model-invocation` e `allowed-tools`
4. Instrução versus garantia (permissões e hooks)
5. Worktrees do Claude Code
6. PR, `--from-pr` e tarefas agendadas
7. `/goal`, Stop hook e execução sem supervisão
8. Plugins oficiais para não duplicar
9. Dicas de usuário avançado
10. CLAUDE.md curto e AGENTS.md
11. Notas para Windows

## 1. Ciclo oficial (V-01, classe A)

Prompt-base (redação própria):

```text
1. Explorar sem editar: leia os arquivos afetados e diga o que entendeu.
2. Planejar (pule se o diff cabe em uma frase): arquivos que mudam, riscos, como verificar.
3. Implementar e rodar a verificação declarada (teste, build, lint). Corrija até passar.
4. Mostrar evidência: comando executado, código de saída e a linha relevante da saída.
5. Commitar localmente. Push, PR e merge só com minha confirmação.
Critério de parada: se a verificação falhar duas vezes pela mesma causa, pare e reporte.
```

Use modo plano quando há incerteza, vários arquivos ou código desconhecido. Dê um critério que passa ou falha; peça evidência, não afirmação. A página cita um skill embutido `/code-review` para revisar o diff. Ressalva: o ciclo foi pensado para sessão interativa; sem supervisão o critério de parada precisa ser explícito (seção 7).

## 2. Checkpoints não substituem git (V-02)

Os checkpoints rastreiam só mudanças feitas pelas ferramentas de edição de arquivo do Claude: "This isn't a replacement for git". `/rewind` não desfaz o que comandos Bash ou processos externos alteraram. Regra: **antes de mudança ampla, crie branch ou commit de segurança** (snippet S-08).

## 3. Skills com efeito colateral (V-04)

- `disable-model-invocation: true` faz a skill só rodar por `/comando` explícito. A doc usa `/commit` e `/deploy` como exemplos. Os comandos oficiais `commit` e `commit-push-pr` **não** usam essa flag (V-05, V-06) e acionam push e PR sem confirmação: por isso este plugin separa commit de PR.
- `allowed-tools` concede permissão "durante o turno"; não restringe quais ferramentas existem. Aceita string separada por espaço ou vírgula, ou lista YAML. Pré-aprove só leitura e o comando exato necessário; deixe `git push`, `gh pr create`, `gh pr merge`, `git tag` e `git reset` **fora**, para que cada um peça confirmação. Revise o `allowed-tools` de skills de repositórios desconhecidos.
- Injeção `!` com crase executa o comando antes do envio e, se **falha, aborta a invocação inteira**. Por isso as skills deste plugin injetam apenas `git branch --show-current` e `git status --short` (funcionam em qualquer repositório) e mandam o modelo rodar `git log`, `git describe`, `git symbolic-ref` e `git diff HEAD` como passos, onde a falha é tratada. Rótulo: Verificado na doc para o aborto; Inferido como desenho do plugin (não testado dentro do Claude Code).
- O texto combinado de `description` e `when_to_use` é truncado em 1.536 caracteres na listagem; mantenha `SKILL.md` abaixo de 500 linhas.
- `context: fork` roda a skill em subagente que não vê o histórico.

**Limitação de desenho a conhecer:** skills com `disable-model-invocation: true` não são chamáveis pelo modelo pela ferramenta Skill. Por isso o `playbook` (que é model-invocable) roteia o pedido e lê o `SKILL.md` da tarefa como roteiro; passos locais e reversíveis que a pessoa pediu explicitamente podem ser executados, e passos externos ou destrutivos param e pedem confirmação. Detalhes no `SKILL.md` do playbook.

## 4. Instrução versus garantia (V-04, V-07)

| Camada | Natureza | Observação |
| --- | --- | --- |
| Regra `deny` de permissão | Garantia (mais forte) | A doc indica o sistema de permissões para impor allow ou deny rígido |
| Hook `PreToolUse` | Guardrail de melhor esforço | Exit 2 bloqueia e o stderr vai para o Claude; `permissionDecision` aceita allow, deny, ask, defer; `if` usa sintaxe de permissão e é "best-effort"; contornável |
| CLAUDE.md | Pedido | Curto; testes mostram que regras demais diluem |
| Skill | Pedido | `allowed-tools` pré-aprova, não impede |

Hook e `deny` prontos em [ferramentas-e-mcp.md](ferramentas-e-mcp.md). Plugins ignoram `hooks`, `mcpServers` e `permissionMode` no frontmatter de agentes (regra das bases da fábrica): a restrição real de um agente é o campo `tools`.

## 5. Worktrees do Claude Code (V-12, classe A)

- `claude --worktree <nome>` cria `.claude/worktrees/<nome>/` na branch `worktree-<nome>`; coloque `.claude/worktrees/` no `.gitignore`. Exige ao menos um commit.
- `.worktreeinclude` (sintaxe gitignore) copia arquivos ignorados necessários (ex.: `.env.local`) para o worktree; só copia o que também está ignorado.
- `worktree.baseRef`: `fresh` (padrão, parte do default remoto) ou `head`. `isolation: worktree` no frontmatter de subagente. `--worktree "#1234"` cria worktree a partir de PR.
- Saída: sessão **sem nome** e limpa é removida sozinha; sessão **nomeada** ou com trabalho pendente pergunta. O Claude Code segura `git worktree lock` enquanto o agente roda.
- A aprovação "sempre permitir" vai para `.claude/settings.local.json` do checkout principal. `${CLAUDE_PROJECT_DIR}` não segue o worktree, o `cwd` do JSON do hook sim. No Windows, junções são removidas só como link. Verificações de isolamento bloqueiam edição no checkout principal.
- Repositório grande: `worktree.sparsePaths` (V-13).

Checklist (próprio):

```text
Início: repositório com pelo menos 1 commit; nome curto da tarefa; .claude/worktrees/ no .gitignore.
Preparo: instalar dependências no worktree; copiar .env via .worktreeinclude; rodar o baseline de testes.
Limite: até 3 sessões ativas (Suposição), cada uma com escopo de arquivos disjunto.
Saída: (1) há mudanças não commitadas? (2) há commits sem push? (3) a branch já foi mesclada?
       Mesclada e limpa: remover. Caso contrário: manter e anotar `claude --worktree <nome> --resume`.
Nunca remover com --force sem confirmação.
```

O limite de 3 vem de opinião de prática (HN e ykdojo, classe C): Suposição.

## 6. PR, `--from-pr` e tarefas agendadas (V-06)

- Receita de PR em 3 prompts: resumir as mudanças, pedir para criar o PR, refinar a descrição; peça para destacar riscos.
- `claude --from-pr <n>` retoma a sessão ligada ao PR; a sessão é ligada ao PR criado por `gh pr create` ou `glab mr create`.
- Tarefas agendadas precisam declarar o que é sucesso e onde postar o resultado. Tarefa agendada que faz push ou posta comentário é ação externa: trate como tal.

## 7. `/goal`, Stop hook e execução sem supervisão (V-01; G6)

O critério de sucesso pode virar `/goal` (condição reavaliada a cada turno) ou Stop hook (bloqueio determinístico até o check passar). As páginas `goal` e `hooks#stop` não foram lidas pelos pesquisadores: leia antes de adotar.

`--dangerously-skip-permissions` e equivalentes removem a confirmação que protege push, merge e tag: **risco alto**; só em sandbox descartável ou repositório confiável e trivial, sem credenciais de escrita remota. Padrão deste plugin: permissões normais, allowlist em settings e `deny` (ver [ferramentas-e-mcp.md](ferramentas-e-mcp.md), seção 16).

## 8. Plugins oficiais para não duplicar (V-11)

O repositório `anthropics/claude-code/plugins` tinha 13 diretórios na data da pesquisa: `agent-sdk-dev`, `claude-opus-4-5-migration`, `code-review`, `commit-commands`, `explanatory-output-style`, `feature-dev`, `frontend-design`, `hookify`, `learning-output-style`, `plugin-dev`, `pr-review-toolkit`, `ralph-wiggum`, `security-guidance`. Licença proprietária (só destilação). `ralph-wiggum` e `hookify` não foram lidos: não os recomende. Este plugin **complementa** (política de commit, release, conflitos, branches e histórico) e usa nomes próprios (`commit-convencional`) para não colidir com `/commit`, `/code-review` e `/commit-push-pr`. Revalide a cada versão.

Falhas dos originais que este plugin corrige: `commit` e `commit-push-pr` sem `disable-model-invocation`; `commit-push-pr` com `Bash(git checkout --branch:*)` (a flag `--branch` não existe: `git checkout --branch x` falha com "unknown option", testado em git 2.54.0; use `git switch -c` ou `git checkout -b`); `git diff HEAD` injetado, que falha em repositório sem commits.

## 9. Dicas de usuário avançado (V-14, classe B)

`claude --worktree`; `/batch` distribui migração em agentes de worktree; `/loop` agenda tarefa local por até 3 dias; `/simplify`; "Prove to me this works" comparando `main` e a branch; "Grill me on these changes and don't make a PR until I pass your test"; `claude --name`. A própria página avisa que o produto muda: confira a versão.

## 10. CLAUDE.md curto e AGENTS.md (V-36)

CLAUDE.md curto; pergunta de corte: "remover isto faria o Claude errar?". AGENTS.md (formato mantido pela Agentic AI Foundation, sem licença declarada) tem seções de exemplo "Testing instructions" e "PR instructions"; o mais próximo do arquivo vence e o pedido no chat prevalece. Como o Claude Code consome AGENTS.md não foi verificado (G7). Mantenha uma fonte de verdade. Regras prontas: [claude-md-snippets.md](claude-md-snippets.md).

## 11. Notas para Windows

- Git Bash e PowerShell coexistem: aspas em caminhos com espaço; `/dev/null` no Bash, `$null` no PowerShell.
- Hook em PowerShell: formato `command` + `args` e `hookEventName` não confirmados (G7, G14).
- Fim de linha: `git config core.autocrlf` e `.gitattributes` evitam diffs falsos; Inferido, conhecimento estável.
- `rebase -i` abre editor; sem terminal interativo, entregue os comandos para a pessoa rodar.
