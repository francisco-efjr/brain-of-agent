# BUILD-REPORT estrutural: database-data-modeling

Data: 2026-10-10 · Papel: validador estrutural · Escopo: `plugins/database-data-modeling` · Rótulos: Verificado (ferramenta executada nesta etapa), Inferido, Suposição, Não verificável.

## 1. Resultado das verificações

| Verificação | Antes | Depois | Rótulo |
| --- | --- | --- | --- |
| `python tools/verify_plugin.py plugins/database-data-modeling` | RESULT: PASS (10 skills, 5 agents, 0 commands, 14 evals, 109 arquivos) | RESULT: PASS (mesmos contadores) | Verificado |
| `claude.exe plugin validate plugins/database-data-modeling` (CLI 2.1.128) | Falha: `root: Unrecognized key: "displayName"` | Validation passed, sem avisos | Verificado |
| Links relativos e `${CLAUDE_PLUGIN_ROOT}` nos `.md` do plugin | Sem quebras | Sem quebras | Verificado (script de checagem local) |
| `name` do frontmatter igual ao nome da pasta (skills) e ao arquivo (agentes) | Conforme | Conforme | Verificado |
| Campos de frontmatter fora da lista suportada | Nenhum | Nenhum | Verificado |
| `description` ausente ou acima de 1024 caracteres | Nenhum | Nenhum | Verificado |
| Agentes sem `Write`/`Edit`; `tools: Read, Grep, Glob` | Conforme | Conforme | Verificado |
| `evals/.gitignore` com `results/` | Presente | Presente | Verificado |
| Grader `skill-fired` cita apenas skills existentes | Conforme | Conforme | Verificado |
| JSON do manifesto | Válido | Válido | Verificado |

## 2. Correções aplicadas

1. **`.claude-plugin/plugin.json`**: removido o campo `displayName`. O validador oficial da CLI local (2.1.128) o rejeita como chave desconhecida. A spec em `docs/foundation/plugin-format-spec.md` ainda o recomenda; essa divergência está registrada em "Pendências" abaixo.
2. **`skills/playbook/SKILL.md`, seção 12 (Fronteiras)**: 13 linhas citavam `/plugin:playbook` de plugins que não existem em `plugins/` nesta data. Cada uma recebeu a marca `(previsto)`. Os plugins existentes (`product-discovery-specs`, `architecture-design`, `web-frontend`, `backend-api`, `mobile-apps`, `llm-ai-agents`, `devops-cloud-infra`, `security-appsec`, `qa-testing`, `code-quality-refactoring`, `ux-ui-design`) foram mantidos sem marca.

Nenhum conteúdo de skill, referência, template ou eval foi reescrito.

## 3. Comparação com o SYNTHESIS (componentes previstos)

| Componente previsto (SYNTHESIS, seção 4) | Estado | Rótulo |
| --- | --- | --- |
| `playbook` + 12 referências em `references/` | Presentes (12 arquivos) | Verificado |
| `playbook/assets/templates/` (9 templates) | Presentes (9 arquivos) | Verificado |
| `prompts` + `prompt-library.md` e divisão de segurança/sistema | Presentes (2 arquivos de biblioteca) | Verificado |
| 8 skills de tarefa (`db-schema-and-sql`, `safe-migrations`, `query-plan-and-indexing`, `transactions-and-isolation`, `rls-tenant-review`, `nosql-data-modeling`, `backup-restore-runbook`, `db-agent-safety` com `disable-model-invocation: true`) | Presentes, com referências | Verificado |
| 5 agentes somente leitura | Presentes | Verificado |
| 10 casos de eval (E-01 a E-10) | Presentes como 14 casos (inclui 2 negativos e 2 de segurança recomendados pelo crítico) | Verificado; número acima do intervalo 6–10 do blueprint, Inferido como aceitável |
| Snippets de CLAUDE.md (20 previstos) | Arquivo presente; contagem exata de S-nn não conferida | Não verificável nesta etapa |
| Bibliografia `fontes.md` (41 itens previstos) | Arquivo presente; contagem exata não conferida | Não verificável nesta etapa |
| Arquivos vazios ou placeholder | Nenhum. Os arquivos menores são graders curtos por desenho | Verificado |

Pendência de conteúdo (não estrutural): a checagem de qualidade de conteúdo (prompt-score, profundidade das fontes) fica com o validador de qualidade.

## 4. README e tabela intenção → skill/agente

- README: a tabela de componentes cita apenas skills e agentes existentes (10 skills, 5 agentes). As referências e templates listados existem. Verificado.
- Playbook: a tabela de fronteiras foi ajustada (seção 2 deste relatório). A tabela de intenção do playbook cita apenas componentes existentes. Verificado.
- Observação: o README ainda diz que o plugin foi escrito "em paralelo" e pede para rodar o verificador "no marketplace". É texto de construção; não é erro estrutural. Inferido como resíduo de construção.

## 5. Pendências (remaining)

1. **Spec vs CLI**: `plugin-format-spec.md` recomenda `displayName`, mas a CLI 2.1.128 rejeita. Corrigir a spec (ou a recomendação) em etapa de documentação.
2. **Marketplace ausente**: não existe `dev-segments/.claude-plugin/marketplace.json` na raiz. Sem ele, os comandos `/plugin marketplace add` e `/plugin install database-data-modeling@dev-segments` do README não funcionam. Verificado por listagem.
3. **Vizinhos previstos**: 13 plugins citados na fronteira ainda não existem em `plugins/` (`data-engineering`, `data-science-ml`, `sre-observability`, `technical-writing-docs`, `game-development`, `systems-embedded-iot`, `cli-desktop-tooling`, `blockchain-web3`, `automation-integrations`, `git-workflow-release`, `saas-multitenant`, `fintech-payments`, `ecommerce-marketplace`). Ao criá-los, remover a marca `(previsto)`.
4. **Evals**: a CLI local (2.1.128) não roda `claude plugin eval` (exige 2.1.269). Os campos `runs` e `timeout_seconds` do `prompt.md` não estão na spec; o validador oficial não os rejeitou. Não verificável quanto ao runner.
5. **Cobertura de agentes em evals**: os cinco agentes não têm caso próprio (declarado no `evals/README.md`).
6. **Validação de conteúdo**: a qualidade (prompt-score, fontes, licenças) não foi avaliada nesta etapa. Responsabilidade do validador de qualidade.
7. **Versões**: a verificação foi feita com CLI 2.1.128. Comportamento em versões mais novas não verificado.

## 6. Como reproduzir

```text
python "C:\Users\Francisco Edson\dev-segments\tools\verify_plugin.py" "C:\Users\Francisco Edson\dev-segments\plugins\database-data-modeling"
"/c/Users/Francisco Edson/.local/bin/claude.exe" plugin validate "C:\Users\Francisco Edson\dev-segments\plugins\database-data-modeling"
```

Resultado nesta etapa: PASS no verificador e "Validation passed" no validador oficial.
