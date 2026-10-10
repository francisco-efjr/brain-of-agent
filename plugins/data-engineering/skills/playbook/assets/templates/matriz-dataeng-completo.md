# Matriz do modo DATAENG-COMPLETO: [OBJETO/REPOSITÓRIO]

Uso: modo DATAENG-COMPLETO, ativado só por pedido explícito do usuário na mensagem. O modo não amplia permissões: continua sem produção, sem escrita destrutiva, sem disparar DAG ou backfill, sem instalar ferramenta; a confirmação por ação é mantida.
Pedido do usuário (cole a frase): "[FRASE QUE ATIVOU O MODO]"
Escopo autorizado: [IMPLEMENTAÇÃO EM ... | SOMENTE ANÁLISE]. Fora do escopo: [LISTA].

## 1. Registro de leitura das referências (`skills/playbook/references/`)
Estado: `lido` (inteiro), `parcial` (diga o que faltou), `ausente` (arquivo não existe na instalação).
| Lote | Arquivo | Estado | Decisões extraídas relevantes ao objeto |
| --- | --- | --- | --- |
| a | `checklist-completo.md` | [ESTADO] | [DECISÕES] |
| a | `padroes-e-antipadroes.md` | [ESTADO] | [DECISÕES] |
| b | `dbt.md` | [ESTADO] | [DECISÕES] |
| b | `orquestracao.md` | [ESTADO] | [DECISÕES] |
| c | `spark-streaming-lakehouse.md` | [ESTADO] | [DECISÕES] |
| c | `sql-e-warehouses.md` | [ESTADO] | [DECISÕES] |
| d | `qualidade-contratos-linhagem.md` | [ESTADO] | [DECISÕES] |
| d | `seguranca-contexto-e-evals.md` | [ESTADO] | [DECISÕES] |
| e | `decisoes-e-tradeoffs.md` | [ESTADO] | [DECISÕES] |
| e | `claude-md-snippets.md` | [ESTADO] | [DECISÕES] |
| e | `ferramentas-e-mcp.md` | [ESTADO] | [DECISÕES] |
| e | `fontes.md` | [ESTADO] | [DECISÕES] |

## 2. Matriz de aplicabilidade (14 áreas)
Cada área: `aplica`, `não aplica (motivo)` ou `lacuna de informação`.
| # | Área | Aplicabilidade | Skill/agente acionado | Evidência coletada (comando e saída, ou `arquivo:linha`) | Status (Concluído, Parcial, Impedido) |
| --- | --- | --- | --- | --- | --- |
| 1 | Ingestão e orquestração | [APLICA/NÃO/LACUNA] | `airflow-dag-workflow` | [EVIDÊNCIA] | [STATUS] |
| 2 | Transformação dbt/SQL | [ ] | `dbt-model-workflow` | [ ] | [ ] |
| 3 | Batch Spark | [ ] | `spark-streaming-review` | [ ] | [ ] |
| 4 | Streaming | [ ] | `spark-streaming-review` | [ ] | [ ] |
| 5 | Warehouse e custo | [ ] | `sql-review` | [ ] | [ ] |
| 6 | Lakehouse e manutenção | [ ] | `spark-streaming-review` | [ ] | [ ] |
| 7 | Qualidade | [ ] | `data-contracts-quality` | [ ] | [ ] |
| 8 | Contratos, linhagem e governança | [ ] | `data-contracts-quality` | [ ] | [ ] |
| 9 | Modelagem dimensional | [ ] | `data-pipeline-architect` + `dbt-model-workflow` | [ ] | [ ] |
| 10 | Acesso do agente a dados (text-to-SQL) | [ ] | `text-to-sql-safe` | [ ] | [ ] |
| 11 | Segurança de dados do agente | [ ] | `data-pipeline-reviewer` | [ ] | [ ] |
| 12 | Observabilidade de dados (lacuna L-01) | [ ] | playbook (princípios, Inferido) | [ ] | [ ] |
| 13 | BI e dashboards (lacuna L-02) | [ ] | `analytics-reviewer` | [ ] | [ ] |
| 14 | Avaliação das próprias skills | [ ] | `eval-judge` | [ ] | [ ] |

## 3. Implementação e achados
| Item | Ação (analisado, alterado, proposto) | Arquivos | Verificação (comando e saída) | Rótulo |
| --- | --- | --- | --- | --- |
| [ITEM] | [AÇÃO] | [ARQUIVOS] | [EVIDÊNCIA] | [Verificado/Inferido/...] |
Auditoria não altera o produto. Em implementação, só dentro do escopo autorizado.

## 4. Revalidação final
Agente `data-pipeline-reviewer` em contexto limpo, somente leitura, contra esta matriz. Resultado: [VEREDITO E ACHADOS]. Declaração: revisão feita pelo mesmo modelo não é validação externa.

## 5. Gate
- Concluído: escopo autorizado feito, critérios pertinentes verificados, exclusões justificadas, risco residual explícito.
- Parcial: falta leitura, acesso, execução ou revalidação material.
- Impedido: descreva a condição.
Resultado: [CONCLUÍDO|PARCIAL|IMPEDIDO] porque [MOTIVO].

## 6. Handoff
Use `handoff-checkpoint-dados.md`.
