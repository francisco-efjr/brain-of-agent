# ux-ui-design: relatório de validação estrutural

Data: 2026-10-10 · Plugin: `plugins/ux-ui-design` · Papel: validador estrutural (não é o validador de qualidade)

## 1. Resultado das verificações

| Verificação | Comando | Resultado |
| --- | --- | --- |
| Verificador da fábrica | `python tools/verify_plugin.py plugins/ux-ui-design` | PASS (sem avisos). Contagem: 10 skills, 5 agentes, 0 comandos, 12 evals, 114 arquivos |
| Validador oficial | `claude plugin validate plugins/ux-ui-design` | Validation passed (Verificado) |
| JSON do manifesto | parse de `.claude-plugin/plugin.json` | válido |

Rodadas: a verificação foi executada antes e depois da correção. Os dois validadores passaram nas duas rodadas.

## 2. Correções feitas

1. `plugins/ux-ui-design/README.md`, linha da "Biblioteca de prompts": o texto dizia "37 planejados" e "casos de eval" sem número. Como os 37 prompts e os 12 casos já existem, o texto foi trocado por "37 prompts, em cinco grupos A a E, em três arquivos de `skills/prompts/references/`" e "12 casos de eval". Nenhum erro de validador havia sido apontado; a correção é de consistência com o estado real.

Nenhum erro de frontmatter, nome diferente da pasta, link relativo quebrado, campo desconhecido, JSON inválido ou grader inválido foi encontrado. Os 10 skills têm `name` igual à pasta; os 5 agentes têm `tools` restritas a Read, Grep e Glob, exceto `ui-designer`, que também tem Write e Edit (previsto no SYNTHESIS). Todos os links relativos de `skills/playbook/SKILL.md` e do README apontam para arquivos existentes.

## 3. Conferência com o SYNTHESIS (`docs/research/ux-ui-design/SYNTHESIS.md`)

Presentes conforme previsto:
- 10 skills de tarefa e núcleo: `playbook`, `prompts`, `design-brief`, `ui-audit`, `heuristic-eval`, `a11y-checklist`, `ux-writing`, `design-tokens`, `user-research-plan`, `design-init` (com `disable-model-invocation: true`, como previsto).
- 5 agentes: `design-evaluator`, `ui-designer`, `a11y-reviewer`, `ux-researcher`, `design-system-auditor`.
- 12 referências em `skills/playbook/references/` (R-01 a R-12) e 12 templates em `skills/playbook/assets/templates/` (T-01 a T-12).
- 37 prompts (PR-01 a PR-37), conferidos por contagem de identificadores nos arquivos de referência.
- Evals: 12 pastas, com `graders/` em cada uma; `evals/.gitignore` com `results/`; `evals/README.md` com status `designed_not_executed`.

Divergências e pendências (não bloqueiam a validação estrutural):
- Árvore de prompts: o SYNTHESIS previa cinco arquivos (`prompt-library.md`, `prompts-auditoria.md`, `prompts-a11y-plataforma.md`, `prompts-pesquisa-e-escrita.md`, `prompts-design-system.md`). Existem três: `prompt-library.md` (grupos A e, pelo conteúdo, B e C), `prompts-pesquisa-e-escrita.md` e `prompts-design-system.md`. Os PR-09 a PR-23 estão no `prompt-library.md`. Isso é uma consolidação, não uma falta de conteúdo. Rótulo: Verificado (contagem de PR) e Inferido (agrupamento por arquivo).
- Calibração few-shot do `design-evaluator` (cenários A, B e C de 4.5.1 do SYNTHESIS): não encontrada no agente. O próprio SYNTHESIS marca como "a escrever e testar pelo dono do plugin". Pendência de qualidade.
- Seção `## Gotchas` do `design-evaluator` existe (linha 89), mas sem casos reais; o SYNTHESIS prevê preenchê-la após as primeiras execuções. Pendência de conteúdo.
- Evals não executados (`designed_not_executed`). `claude plugin eval` exige versão 2.1.269 ou superior; esta conferência não os executou.

## 4. Referências cruzadas a outros plugins

O README e o playbook citam componentes de outros plugins da fábrica. Todos existem no repositório (Verificado por busca de `name:` nos SKILL.md):
- `web-frontend:playbook`, `web-frontend:design-ui`, `web-frontend:a11y-review`: existem em `plugins/web-frontend/skills/`.
- `mobile-apps:playbook`: existe em `plugins/mobile-apps/skills/playbook/`.
- `qa-testing`: plugin existe; citado apenas como lugar de automação em CI.

Essas referências dependem de os plugins estarem instalados; o `SKILL.md` de `a11y-checklist` e `design-brief` já dizem "se instalado".

## 5. Pendências para o validador de qualidade

1. Escrever a calibração few-shot do `design-evaluator` (cenários sintéticos A, B e C) e testá-la. Rótulo: Suposição (sem teste feito).
2. Preencher `## Gotchas` do `design-evaluator` após as primeiras execuções reais de evals.
3. Executar os 12 casos de eval com `claude plugin eval` em versão 2.1.269 ou superior, e só então registrar taxas. Até lá, nenhum resultado pode ser alegado.
4. Decidir se o agrupamento atual de prompts (três arquivos) é o definitivo ou se volta à árvore de cinco arquivos do SYNTHESIS.

## 6. Limites desta validação

Esta é uma verificação estrutural: frontmatter, links, nomes, manifesto, presença de componentes previstos e contagem de identificadores. Não avalia a qualidade do conteúdo, não executou evals e não renderizou nenhuma página. Os rótulos acima seguem a fundação: Verificado para o que foi rodado, Inferido para agrupamentos, Suposição para o que depende de teste futuro, Não verificável para o que nenhuma ferramenta confirmou.
