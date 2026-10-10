# BUILD-REPORT estrutural: git-workflow-release

Data: 2026-10-10. Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\git-workflow-release`. Escopo: validação estrutural (não avalia qualidade de conteúdo; isso é do validador de qualidade).

## 1. Resultados das verificações

| Verificação | Antes | Depois |
| --- | --- | --- |
| `tools/verify_plugin.py` | PASS (0 erros, 0 avisos) | PASS (0 erros, 0 avisos) |
| `claude plugin validate` (CLI 2.1.128) | Validation passed | Validation passed |

Verificado: as duas execuções foram feitas no próprio plugin, após a correção descrita abaixo.

## 2. Contagem de componentes

| Componente | Previsto (SYNTHESIS 7.4 / blueprint) | Existente | Situação |
| --- | --- | --- | --- |
| Skills | 10 (playbook, prompts + 8 de tarefa) | 10 | OK |
| Agentes | 4 | 4 | OK |
| Referências do playbook | 12 | 12 | OK |
| Templates | 15 | 15 | OK |
| Snippets de CLAUDE.md (S-01 a S-20) | 20 | 20 | OK |
| Prompts (P-01 a P-32) | 15 a 40 (blueprint) | 32 | OK |
| Casos de eval | 10 (SYNTHESIS 4.9); limite 6 a 10 (blueprint) | 12 | Divergência, ver seção 4 |
| Hooks, `.mcp.json`, `.lsp.json`, `bin/` | ausentes | ausentes | OK |
| Arquivos vazios | nenhum | nenhum | OK |

Verificado: contagem por `find` e `ls` sobre a pasta do plugin.

## 3. Correções feitas

1. `README.md` (linha 10): dizia "10 casos de eval". Há 12 pastas em `evals/`; `evals/README.md` já explica o acréscimo de 2 casos. Texto corrigido para 12 e com referência à justificativa.
2. `README.md` (linha 99): "Os 10 casos estão `designed_not_executed`" corrigido para 12.

Nenhum erro de frontmatter, nome diferente da pasta, JSON inválido, campo desconhecido, link relativo quebrado ou `${CLAUDE_PLUGIN_ROOT}` apontando para arquivo inexistente foi encontrado.

Verificado: script de checagem de 90 links (`](...)` relativos e `${CLAUDE_PLUGIN_ROOT}/...`) sem quebras. Frontmatter de 10 skills e 4 agentes: `name` igual à pasta ou ao arquivo, `description` entre 517 e 883 caracteres (limite ~1024).

## 4. Pendências (decisão do usuário ou do validador de qualidade)

1. **Casos de eval acima do limite.** Há 12 casos; o blueprint pede 6 a 10 e o SYNTHESIS 4.9 previa 10. `evals/README.md` registra o motivo (dois casos extras: `release-android-fronteira` e `negativo-deploy-aws`) e indica o corte preferido caso o custo pese. Não cortei nenhum caso, porque remover conteúdo está fora do escopo deste validador. Decisão pendente: manter 12 com justificativa registrada, ou cortar `negativo-deploy-aws` (ou `commit-diff-misto`), conforme a própria nota.
2. **Formato do frontmatter dos casos de eval.** Os `prompt.md` trazem `name`, `timeout_seconds` e `runs`, campos que o blueprint não lista (`description`, `tags`, `max_turns`, `allowed_tools`). O validador oficial não checa evals e a CLI local (2.1.128) não executa `claude plugin eval` (exige 2.1.269). Status: Não verificável até rodar em versão compatível; o campo `min`/`max` dos graders `tool_used` também vem do SYNTHESIS, não do blueprint.
3. **Lacuna de conteúdo conhecida (G2, SYNTHESIS 7.3).** Backport e hotfix com `cherry-pick -x` e release branches não têm skill nem prompt próprio. Não é componente previsto no blueprint; registrado como lacuna.
4. **Evals não executados.** Todos continuam `designed_not_executed`, conforme o README do plugin declara.
5. **Descrições dos componentes.** O SYNTHESIS (seção 7.4 e revisão do crítico) dizia que as descrições completas ainda não estavam redigidas. Hoje todas existem no frontmatter; a pontuação pela rubrica (≥ 80) é tarefa do validador de qualidade, não deste relatório.

## 5. Conclusão

Estrutura válida nos dois validadores, sem hooks, MCP, LSP ou `bin/` ativos, sem componentes previstos ausentes. As únicas correções feitas foram as duas contagens de casos de eval no README. Restam as pendências da seção 4, que exigem decisão ou validação de conteúdo.
