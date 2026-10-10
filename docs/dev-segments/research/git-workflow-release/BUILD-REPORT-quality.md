# BUILD-REPORT de qualidade: git-workflow-release

Data: 2026-10-10. Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\git-workflow-release`. Papel: validador de qualidade de prompt e conteúdo técnico (rubrica D1 a D12, nota 0 a 100).

**Declaração de independência:** o validador é um modelo de linguagem da mesma família dos construtores. As notas abaixo são estimativas de leitura, não medição; nenhum eval foi executado. Recomenda-se leitura humana dos pontos de segurança (hook, `deny`, `allowed-tools`).

## 1. Método

Leitura integral dos 10 `SKILL.md`, dos 4 agentes, da biblioteca de 32 prompts (todos lidos, mais de 10 amostrados em detalhe), dos 12 casos de eval (3 lidos por inteiro: `commit-diff-misto`, `triagem-pr-injecao`, `negativo-deploy-aws`; os demais por `prompt.md` e `criteria.md` selecionados), de `ferramentas-e-mcp.md`, `claude-md-snippets.md`, `releases-e-versionamento.md` e `fontes.md`. Verificação técnica por WebFetch e por comandos locais (git 2.54.0, Windows). Nenhum critério de reprovação automática foi encontrado: sem instrução de inventar execução, sem ação externa sem confirmação, sem segredos, frontmatter válido, literal de terceiros só como destilação com atribuição.

## 2. Notas antes e depois

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 90 | 93 | Releases imutáveis passaram a condicionais (opção do repositório); rótulo de `disable-model-invocation` promovido a Verificado na doc; mapa de referências ganhou hotfix e backport |
| `skills/commit-convencional/SKILL.md` | 92 | 92 | Sem mudança necessária (`git add *` e `git commit *` pré-aprovados são intencionais; a instrução proíbe `-A`, `--amend` e `--no-verify`) |
| `skills/criar-pr/SKILL.md` | 92 | 92 | Sem mudança |
| `skills/resolver-conflitos/SKILL.md` | 93 | 93 | Sem mudança |
| `skills/rebase-seguro/SKILL.md` | 92 | 92 | Sem mudança |
| `skills/bisect-regressao/SKILL.md` | 89 | 92 | Removida a pré-aprovação de `git bisect start *` (contradizia a confirmação do passo 5 e troca os arquivos do disco); texto de segurança atualizado |
| `skills/encerrar-branch/SKILL.md` | 92 | 92 | Sem mudança |
| `skills/release-cut/SKILL.md` | 89 | 92 | Imutabilidade da Release declarada como dependente da opção do repositório (3 trechos), com instrução de pedir conferência à pessoa |
| `skills/triagem-contribuicao/SKILL.md` | 93 | 93 | Sem mudança |
| `skills/prompts/SKILL.md` | 91 | 91 | Sem mudança |
| `agents/revisor-diff.md` | 94 | 94 | Sem mudança |
| `agents/revisor-plano.md` | 94 | 94 | Sem mudança |
| `agents/auditor-release.md` | 90 | 93 | Item 8 do checklist: imutabilidade só com a opção ligada; ficou Não verificável sem acesso |
| `agents/auditor-politica-repo.md` | 93 | 93 | Sem mudança |
| `skills/prompts/references/prompt-library.md` (32 prompts) | 90 | 91 | P-19 (imutabilidade condicional); P-26 ("somente leitura" agora ressalva o `git fetch`) |
| `evals/` (12 casos, README, graders) | 86 | 91 | `arm: both` nos 2 graders `no-plugin-skill` (graders `tool_used` sobre `Skill` ficam fora da nota em rodada com duas frentes); README com regras de concessão de ferramentas, sandbox e WSL2, Git 2.31, `--trust-plugin`, formato oficial Verificado |

Média antes: 91,3. Média depois: 92,4. Mínimo depois: 91. Nenhum artefato abaixo de 80.

Arquivos de apoio também ajustados: `README.md` (limitações atualizadas com o que foi conferido), `skills/playbook/references/releases-e-versionamento.md` (imutabilidade; nova seção 12 de hotfix e backport), `ferramentas-e-mcp.md` (T-01, T-02, T-12), `claude-md-snippets.md` (S-18), `fontes.md` (V-40), `release-checklist.md` e `release-notes-and-release-yml.md` (imutabilidade).

## 3. Fidelidade técnica: o que foi conferido

| Afirmação | Resultado | Fonte |
| --- | --- | --- |
| Releases imutáveis travam tag e ativos após publicar | **Corrigido**: é opção que se habilita por repositório ou organização; o plugin dizia incondicionalmente. Título, notas e status de pré-lançamento continuam editáveis | docs.github.com, "immutable releases" |
| `allowed-tools` só pré-aprova; aceita string separada por espaço ou vírgula e lista YAML | Verificado | code.claude.com/docs/en/skills |
| `disable-model-invocation: true` impede o modelo de carregar a skill; `/nome` continua valendo | Verificado (antes estava Inferido) | idem |
| Injeção `!` que falha aborta a skill; `${CLAUDE_PLUGIN_ROOT}` funciona no corpo e em regras Bash de `allowed-tools` | Verificado | idem |
| Hook: `command` + `args` sem shell, `if` com sintaxe de permissão, `hookSpecificOutput.hookEventName`, `permissionDecision` allow/deny/ask/defer, exit 2 bloqueia, `onFailure: "block"` a partir de 2.1.295, timeout não bloqueia por padrão | Verificado (antes estava Não verificado) | code.claude.com/docs/en/hooks |
| Regra `Bash(prefixo *)`; `deny` vale para subcomandos de comando composto; não casa `git -C`, `git -c`, `bash -c`, caminho absoluto | Verificado (antes Inferido) | code.claude.com/docs/en/permissions |
| Formato de eval (`prompt.md`, campos, graders `llm`/`tool_used`, `min`/`max`, `arm`), Claude Code 2.1.269+, Git 2.31+, Bash/Write/Edit removidos sem `--allow-tools`, sem sandbox no Windows nativo | Verificado; pendência 2 do relatório estrutural resolvida | code.claude.com/docs/en/plugin-evals |
| Frontmatter dos casos usa só campos válidos (`name`, `description`, `tags`, `runs`, `expected_outcome`, `model`, `max_turns`, `timeout_seconds`, `allowed_tools`) | Verificado: nenhuma chave desconhecida | idem |
| `claude --worktree <nome>`, `.claude/worktrees/`, `.worktreeinclude` só copia o que também é ignorado, `--resume` | Verificado | code.claude.com/docs/en/worktrees |
| Agentes de plugin ignoram `hooks`, `mcpServers`, `permissionMode`; `tools` não aceita padrão `Bash(git diff *)` | Verificado: não há como restringir Bash por padrão no agente, então "revisor sem Write/Edit" é a garantia técnica e "Bash só leitura" é instrução | code.claude.com/docs/en/sub-agents |
| claude-code-action tem as entradas `allowed_non_write_users`, `allowed_bots`, `use_commit_signing`, `ssh_signing_key` | Verificado | `action.yml` no GitHub |
| `git checkout --branch` não existe | Verificado de novo localmente (git 2.54.0: "unknown option") | teste local |
| `git cherry-pick -x` acrescenta a linha "(cherry picked from commit ...)"; `-m`, `--no-commit` existem | Verificado localmente | teste local |
| Plugin `name` sem prefixo reservado; `claude plugin validate` | Passou | CLI local |

## 4. Componentes completados

- Lacuna G2 (hotfix e backport): nova seção 12 em `releases-e-versionamento.md` com roteiro de 7 passos, rotulado Inferido onde não há fonte A ou B, e README ajustado. Não é componente previsto no blueprint; a skill `release-cut` continua sem automatizar release branches, e isso está declarado.
- Nenhum componente previsto estava ausente (10 skills, 4 agentes, 12 referências, 15 templates, 20 snippets, 32 prompts).

## 5. Direitos autorais e segurança

- Sem cópia literal de terceiros além de poucas palavras citadas; atribuições presentes no README, em `fontes.md` e na biblioteca (CC BY 3.0, MIT, CC-BY, Apache-2.0). Fixture dos evals usa domínio reservado `.invalid`.
- Nenhum segredo (varredura por padrões de chave, token e `AKIA`). Nenhum hook, `.mcp.json`, `.lsp.json` ou `bin/` ativo.
- Fluxos externos (push, PR, merge, tag, Release, apagar branch, remover worktree) exigem confirmação com o comando exato em todas as skills de tarefa; `--force`, `--no-verify` e `git add -A` aparecem só como proibições com alternativa.
- Revisores e auditores: `tools: Read, Grep, Glob, Bash`, sem Write ou Edit. Evals com PASS/FAIL observáveis e 2 casos negativos (`negativo-keyword-em-log`, `negativo-deploy-aws`).
- Execução sem supervisão (`--dangerously-skip-permissions`) aparece só como risco em `ferramentas-e-mcp.md`, seção 16, restrita a sandbox descartável.

## 6. Pendências

1. **Casos de eval acima do limite do blueprint (12 contra 6 a 10).** Decisão do usuário: manter com a justificativa de `evals/README.md` ou cortar `negativo-deploy-aws` ou `commit-diff-misto`. Não cortei.
2. **Bash dos agentes revisores não pode ser restringido por padrão** (limite da plataforma, Verificado). A contenção é instrução mais regras `deny` do chamador. Decisão: aceitar o risco residual ou orientar o uso de `deny` no repositório alvo.
3. **Nada foi executado dentro do Claude Code:** evals (`designed_not_executed`, requer 2.1.269+; o CLI local é 2.1.128 e o Windows nativo não sustenta casos com Bash), o hook `git-guard.ps1` e o roteamento do playbook para skills `disable-model-invocation` são Não verificáveis na prática.
4. **Marketplace:** o README e `publish/ORCHESTRATOR.md` usam o marketplace `brain-of-agent`, enquanto o blueprint cita `@dev-segments`. Decidir o nome final antes de publicar.
5. **Lacunas de conteúdo mantidas e declaradas:** release de monorepo, Changesets, commits assinados e SLSA, `git rerere`, Git LFS e submódulos, servidor MCP do GitHub, GitLab e demais hosts, `/goal` e Stop hook.
6. **Configuração de releases imutáveis** não é legível sem acesso de administrador; o plugin trata como Não verificável e pede conferência à pessoa.
7. **Ressalva da própria validação:** as notas D1 a D12 são autoatribuídas por modelo da mesma família; calibre com leitura humana e com a primeira rodada de evals.

## 7. Verificações finais

| Verificação | Resultado |
| --- | --- |
| `python tools/verify_plugin.py plugins/git-workflow-release` | PASS (0 erros) |
| `claude plugin validate plugins/git-workflow-release` | Validation passed |
