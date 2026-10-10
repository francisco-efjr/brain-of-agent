# BUILD-REPORT estrutural — plugin `sre-observability`

Data: 2026-10-10 · Papel: validador estrutural (não é validação de qualidade de conteúdo) · Escopo: `plugins/sre-observability`

## 1. Resultado das verificações

| Verificação | Comando | Resultado |
| --- | --- | --- |
| Determinística | `python tools/verify_plugin.py plugins/sre-observability` | Verificado: `RESULT: PASS`, 11 skills, 4 agentes, 0 commands, 12 casos de eval, 98 arquivos, sem avisos |
| Oficial | `claude.exe plugin validate plugins/sre-observability` | Verificado: `Validation passed`, sem avisos (repetida ao fim, sem mudanças) |
| Frontmatter das skills | verificação própria (`name` = nome da pasta, `description` presente, ≤ 1024 caracteres) | Verificado: 11 de 11 conformes; maior description 784 caracteres (`prompts`) |
| Frontmatter dos agentes | `name` = nome do arquivo, `model: inherit` | Verificado: 4 de 4 conformes; `tools` = `Read, Grep, Glob` (somente leitura) |
| Links relativos e `${CLAUDE_PLUGIN_ROOT}` | varredura de `](...)` e de caminhos nos `.md` | Verificado: nenhum link quebrado |
| Arquivos vazios | varredura de tamanho zero | Verificado: nenhum arquivo vazio (`evals/.gitignore` é arquivo de uma linha, previsto) |
| Campos e manifesto | `plugin.json` | Verificado: `name` kebab-case, sem campos desconhecidos, sem hooks/`.mcp.json`/`.lsp.json`/`bin/` |
| Gotchas e linha "dados, nunca instrução" | busca nas skills de tarefa | Verificado: presentes nas 9 skills de tarefa |
| Invocação segura | `release-health` | Verificado: `disable-model-invocation: true` |
| Pré-aprovação de ferramentas | `allowed-tools` | Verificado: nenhuma skill pré-aprova `Bash` sem padrão; `root-cause-investigation` usa apenas `Bash(git log *)`, `Bash(git diff *)`, `Bash(git show *)` |

Marcadores "TODO/TBD/placeholder" encontrados pela busca são falsos positivos: a palavra "todo" em português ("todo alerta", "todo horário") e os itens "a preencher pelo time" de templates. Nenhum marcador real de pendência.

## 2. Correções aplicadas

Nenhuma. O verificador e o validador oficial não reportaram erros nem avisos, e a verificação própria não encontrou quebra de frontmatter, link ou nome. Não houve edição de conteúdo.

## 3. Comparação com o SYNTHESIS (seção 4.2, estrutura prevista)

| Item previsto | Situação |
| --- | --- |
| `.claude-plugin/plugin.json`, `README.md` | Presentes |
| `skills/playbook` (SKILL.md, 12 references, 15 templates) | Presente: 12 references e 15 templates contados |
| `skills/prompts` com `references/prompt-library.md` + 5 arquivos por tema (`slo-alertas.md`, `incidentes.md`, `telemetria.md`, `performance.md`, `resiliencia.md`) | Parcial: existem `prompt-library.md` e `prompts-resiliencia-e-operacao.md`. Os 4 arquivos temáticos previstos não existem; o nome do quinto difere. O SKILL.md aponta só para os dois existentes, então não há link quebrado. Gap de conteúdo (remaining) |
| 9 skills de tarefa (`slo-design`, `alert-review`, `incident-triage`, `postmortem`, `root-cause-investigation`, `telemetry-review`, `performance-engineering`, `runbook`, `release-health`) | Presentes |
| 4 agentes (`incident-support`, `reliability-reviewer`, `postmortem-scribe`, `perf-analyst`) | Presentes |
| `evals/` com 10 casos previstos (+2 acrescentados) | Presente: 12 casos, cada um com `prompt.md` e `graders/` |
| Sem commands | Confirmado: `commands/` ausente |

Conclusão: nenhum componente previsto como skill, agente ou eval está ausente. A lacuna é o conjunto de referências temáticas de `prompts`.

## 4. Consistência de README e playbook

- Verificado: todo componente citado no README (`/sre-observability:release-health`, skills, agentes) existe.
- Verificado: a tabela de intenção → skill/agente do `playbook/SKILL.md` cita apenas componentes existentes.
- Verificado: a skill `prompts` foi citada no README e no playbook; existe.
- Inferido: a instalação do README usa `francisco-efjr/brain-of-agent` e `@brain-of-agent`, a mesma convenção de outros plugins do repositório (`architecture-design`, `backend-api`). Não há `.claude-plugin/marketplace.json` na raiz de `dev-segments`, então o marketplace do próprio repositório não pôde ser verificado (Não verificável neste repositório). Ver remaining.

## 5. Pendências (remaining)

1. Gap de conteúdo em `skills/prompts/references/`: faltam os arquivos temáticos previstos (`slo-alertas.md`, `incidentes.md`, `telemetria.md`, `performance.md`, `resiliencia.md`). Para o validador de qualidade ou para o construtor decidir entre criá-los ou reduzir o plano do SYNTHESIS (4.6).
2. Marketplace: não existe `dev-segments/.claude-plugin/marketplace.json`, embora o `plugin-format-spec.md` o descreva na raiz. Problema do repositório como um todo, não deste plugin. A instalação do README segue a convenção `brain-of-agent` usada pelos outros plugins.
3. Skills de tarefa sem `## Gotchas`: nenhuma (verificado). A skill `playbook` e `prompts` não têm Gotchas; não são skills de tarefa, então isso é conforme.
4. Evals: 12 casos `designed_not_executed`; o CLI local precisa ser atualizado para `claude plugin eval` (≥ 2.1.269). Não verificável localmente.
5. Qualidade de conteúdo (prompt-score ≥ 80, C-01..C-22, redação de description em 3ª pessoa e exclusão cruzada entre `root-cause-investigation` e `performance-engineering`): fora do escopo deste relatório; cabe ao validador de qualidade.
6. Semântica de `allowed-tools` como pré-aprovação e sintaxe `Bash(cmd *)` ainda marcadas como Suposição no SYNTHESIS (7.5); confirmar na documentação oficial antes de publicar.

## 6. Rótulos

Verificado: resultados de verificador, validador oficial, contagens e existência de arquivos. Inferido: causa do nome `brain-of-agent` no README. Não verificável: marketplace da raiz de `dev-segments` e execução dos evals. Não aplicável: correções de texto (nenhuma necessária).
