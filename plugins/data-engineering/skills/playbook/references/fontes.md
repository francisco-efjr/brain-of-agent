# Fontes e bibliografia

Quando abrir: precisar da origem de uma recomendação, da licença de uma fonte, ou saber o que o plugin não cobre.
Consulta: todas as fontes foram reabertas por um validador em 2026-10-10 (exceto onde dito "não reaberto"); metadados do GitHub (estrelas, push) são da API ou da página nessa data e mudam. Nenhum código de terceiros foi baixado ou executado.
Classe: A = oficial (Anthropic) ou doc/norma/repositório oficial do mantenedor da tecnologia; B = praticante ou repositório reconhecido, ou doc oficial de tecnologia sem alinhamento direto ao uso com agente; C = sinal fraco, usado como corroboração ou anti-padrão. A nota entre parênteses é a pontuação da rubrica de fonte (0 a 10).
Licença: "documentação; destilado" significa que o plugin usa redação própria. Nenhum trecho literal de terceiros é reproduzido neste plugin. Conteúdo do brain-of-agent é do autor (MIT).

## Sumário
1. Top 20 (por relevância)
2. Demais fontes usadas
3. Fontes internas (brain-of-agent)
4. Rebaixadas, rejeitadas e não recomendadas
5. Mapa V-nn → fonte
6. Lacunas conhecidas
7. Limites da verificação

## 1. Top 20
| # | Título | URL | Classe | Licença | Consulta |
| --- | --- | --- | --- | --- | --- |
| 1 | Claude Code best practices | https://code.claude.com/docs/en/best-practices | A (9) | documentação; destilado | 2026-10-10 |
| 2 | Claude Code skills e sub-agents (docs) e `anthropics/skills` | https://code.claude.com/docs/en/skills · https://code.claude.com/docs/en/sub-agents · https://github.com/anthropics/skills | A (8) | docs: destilado; repositório com licença `null` na API (180.246★), não copiar | 2026-10-10 |
| 3 | Effective context engineering for AI agents (Anthropic, 29/09/2025) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | A (8) | destilado | 2026-10-10 |
| 4 | Code execution with MCP (Anthropic, 04/11/2025) | https://www.anthropic.com/engineering/code-execution-with-mcp | A (8) | destilado | 2026-10-10 |
| 5 | Building effective agents (Anthropic, 19/12/2024) | https://www.anthropic.com/engineering/building-effective-agents | A (8) | destilado | 2026-10-10 |
| 6 | `dbt-labs/dbt-agent-skills` | https://github.com/dbt-labs/dbt-agent-skills | A (8) | Apache-2.0 (731★, 63 forks, push 2026-10-08) | 2026-10-10 |
| 7 | Airflow best practices (stable = 3.3.2) | https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html | A (8) | documentação; destilado | 2026-10-10 |
| 8 | `astronomer/agents` (authoring, testing e debugging de DAGs) | https://github.com/astronomer/agents | B (6) | Apache-2.0 (451★, push 2026-10-07) | 2026-10-10 |
| 9 | Spark SQL performance tuning (latest = 4.2.0) | https://spark.apache.org/docs/latest/sql-performance-tuning.html | A (8) | documentação; destilado | 2026-10-10 |
| 10 | BigQuery: otimizar entrada e computação | https://docs.cloud.google.com/bigquery/docs/best-practices-performance-input · https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute | A (8) | documentação; destilado | 2026-10-10 |
| 11 | Flink: garantias de entrega de conectores (master) | https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/datastream/guarantees/ | A (8) | documentação; destilado | 2026-10-10 |
| 12 | rmoff, "Claude Code isn't going to replace data engineers (yet)" (11/03/2026) | https://rmoff.net/2026/03/11/claude-code-isnt-going-to-replace-data-engineers-yet/ | B (6) | post; destilado | 2026-10-10 |
| 13 | Hamel Husain e Shreya Shankar, AI Evals FAQ; harness de evals do dbt-agent-skills; rmoff, avaliação de skills de dbt | https://hamel.dev/blog/posts/evals-faq/ · https://github.com/dbt-labs/dbt-agent-skills/blob/main/evals/README.md · https://rmoff.net/2026/03/13/evaluating-claudes-dbt-skills-building-an-eval-from-scratch | A (8, cruzamento) | harness Apache-2.0; posts destilados | 2026-10-10 |
| 14 | Segurança de agente em dados: `idk-arsh/data-agent-rules`, `pugyy/dw-harness`, relato de Johann Rehberger (CVE-2025-55284, 11/08/2025) | https://github.com/idk-arsh/data-agent-rules · https://github.com/pugyy/dw-harness · https://embracethered.com/blog/posts/2025/claude-code-exfiltration-via-dns-requests/ | B (6 por cruzamento; repositórios C) | MIT (repositórios); post destilado | 2026-10-10 |
| 15 | `AltimateAI/data-engineering-skills` | https://github.com/AltimateAI/data-engineering-skills | B (6; 5 para SQL) | MIT na página (128★), arquivos sem licença própria; destilado | 2026-10-10 |
| 16 | `dbt-labs/dbt-project-evaluator` | https://github.com/dbt-labs/dbt-project-evaluator | B (7) | Apache-2.0 (578★, página) | 2026-10-10 |
| 17 | Guias de estilo e estrutura do dbt | https://docs.getdbt.com/best-practices/how-we-style/1-how-we-style-our-dbt-models · https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview | B (7) | documentação; destilado | 2026-10-10 |
| 18 | Open Data Contract Standard (Bitol) v3.2.0 | https://github.com/bitol-io/open-data-contract-standard | B (7) | Apache-2.0 (1,2 mil★, página) | 2026-10-10 |
| 19 | Databricks: expectations (Lakeflow pipelines) | https://docs.databricks.com/aws/en/ldp/expectations | B (7) | documentação; destilado | 2026-10-10 |
| 20 | Claude cookbook "How to make SQL queries" e `anthropics/claude-cookbooks` | https://platform.claude.com/cookbook/misc-how-to-make-sql-queries · https://github.com/anthropics/claude-cookbooks | B (7) | MIT (53.322★, push 2026-10-10 pela API); cookbook de 03/03/2024 | 2026-10-10 |

## 2. Demais fontes usadas
| Título | URL | Classe | Licença | Usada em |
| --- | --- | --- | --- | --- |
| `dagster-io/skills` (plugin `dagster`) e doc de assets | https://github.com/dagster-io/skills · https://dagster.io/docs/concepts/assets/software-defined-assets | B (6) | Apache-2.0 (211★) | V-15; Dagster |
| Delta Lake: otimizações OSS | https://docs.delta.io/optimizations-oss/ | B (7) | documentação; destilado | V-21 |
| Kimball: técnicas de modelagem dimensional | https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/ | B (6) | página; destilado | V-27 |
| OpenLineage docs (1.53.0) | https://openlineage.io/docs/ | B (6) | documentação; destilado | V-28 |
| `flyersworder/agentic-data-contracts` | https://github.com/flyersworder/agentic-data-contracts | B (5) | MIT (10★); só o desenho | V-24 |
| `adityawrk/analytics-with-claude-code` | https://github.com/adityawrk/analytics-with-claude-code | C (3) | MIT (6★); só o padrão, texto reescrito | V-12 |
| Data mesh, Zhamak Dehghani (03/12/2020) | https://martinfowler.com/articles/data-mesh-principles.html | B (5) | artigo; destilado | V-29 |
| `PatrickJS/awesome-cursorrules` (arquivo PySpark) | https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/pyspark-etl-best-practices-cursorrules-prompt-file.mdc | B (5) | CC0-1.0 (40.891★); só subconjunto verificado | V-17 |
| `reason-machines/data-skills` | https://github.com/reason-machines/data-skills | C (1) | não identificada; anti-padrão | V-30 |
| GitHub Actions: uso seguro de `pull_request_target` | https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target | A (via brain-of-agent; não reaberto nesta cadeia) | documentação | [ferramentas-e-mcp.md](ferramentas-e-mcp.md) |

## 3. Fontes internas (brain-of-agent)
| Arquivo | Uso | Licença |
| --- | --- | --- |
| `brains/qa/references/dados-ambientes-ci.md` (commit 0d025fb do repositório `francisco-efjr/brain-of-agent`, snapshot de 09/10/2026) | Dados de teste, isolamento e limpeza, manifesto de execução, falhas controladas, gates de CI, quarentena, oráculo de migração | MIT (conteúdo próprio do autor); adaptado com atribuição em [seguranca-contexto-e-evals.md](seguranca-contexto-e-evals.md), [dbt.md](dbt.md), [spark-streaming-lakehouse.md](spark-streaming-lakehouse.md), [qualidade-contratos-linhagem.md](qualidade-contratos-linhagem.md) e nos templates `manifesto-de-execucao.md` e `plano-de-migracao-gated.md` |
| Estilo da casa (`house-style.md`): keyword `<SEGMENTO>-COMPLETO`, rótulos epistêmicos, proporcionalidade | Estrutura do playbook | MIT (do autor) |
Os demais arquivos do brain citados na síntese (`design-de-testes.md`, `dominios.md`, templates do segmento fullstack, contexto portátil) não foram incorporados nesta versão: o plugin faz remissão ao plugin `qa-testing` para estratégia geral de testes e `database-data-modeling` para OLTP. Material do gstack (MIT, Garry Tan) inspira apenas o estilo de causa raiz do agente `pipeline-debugger`, sem cópia.

## 4. Rebaixadas, rejeitadas e não recomendadas
| Item | Decisão | Motivo |
| --- | --- | --- |
| `wshobson/agents` como fonte de skills de dados | Rejeitada | Pista não confirmada: a página não lista plugin de dados, Airflow ou dbt |
| `reason-machines/data-skills` e índices gerados por bot | Anti-padrão | Geração sem revisão; nomes suspeitos |
| `ScalefreeCOM/datavault4dbt-agent-skills` | Fora do plugin base | Só Data Vault 2; referência opcional |
| `Unknown-333/awesome-data-engineering-skills` | Mapa de lacunas apenas | Catálogo sem conteúdo lido; instalação por script |
| `jensvanbellen/dbt-claude-skills` | Rebaixada | 0★; instalação por script |
| `borghei/claude-skills` | Rebaixada | MIT + Commons Clause (restritiva) |
| Weld, Querio, AI Builder Club | Não usadas como fonte técnica | Marketing; `state:modified+` sem `--state` do Weld está errado |
| Hooks e scripts de `idk-arsh/data-agent-rules` e `pugyy/dw-harness`; comandos `curl -o`, `uvx --from git+`, `pip install` de READMEs | Proibidos | Código de terceiros não revisado |
| "38 testes passam, 10 em warn" (rmoff) e "98,7%" (Anthropic) como evidência de eficácia | Não citar | O primeiro não bate com o log do post; o segundo é de outro contexto |
| Regras Snowflake e partes do PySpark de awesome-cursorrules | Rebaixadas | Erros técnicos conferidos |

## 5. Mapa V-nn → fonte
| Item | Tema | Fontes (linhas da seção 1/2) |
| --- | --- | --- |
| V-01 | Verificação executável, plan mode, CLAUDE.md | #1 |
| V-02 | Formato de skill e subagente | #2 |
| V-03 | Contexto enxuto | #3, #4 |
| V-04 | Workflow vs agente | #5 |
| V-05 | Aceitação de pipeline | #12 |
| V-06 | Método de eval | #13 |
| V-07 | Regras dbt da dbt Labs | #6 |
| V-08 | Ciclo dbt | #15 (Altimate) |
| V-09 | Testes dbt e evaluator | #15, #16 |
| V-10 | Convenções dbt | #17 |
| V-11 | Upgrade com gates | #6 (`upgrading-dbt`) |
| V-12 | `analytics-reviewer` | demais fontes (adityawrk) |
| V-13, V-14 | Airflow | #7, #8 |
| V-15 | Dagster | demais fontes |
| V-16 | Spark | #9 |
| V-17 | PySpark | demais fontes (awesome-cursorrules) |
| V-18 | BigQuery | #10 |
| V-19 | Semântica de SQL | #15 |
| V-20 | Streaming | #11 |
| V-21 | Delta | demais fontes |
| V-22 | Qualidade | #19 |
| V-23 | ODCS | #18 |
| V-24 | Política block/warn/log | demais fontes |
| V-25 | Segurança | #14 |
| V-26 | Text-to-SQL | #20 |
| V-27 | Kimball | demais fontes |
| V-28 | OpenLineage | demais fontes, #6 (Mermaid) |
| V-29 | Data mesh | demais fontes |
| V-30 | Triagem de terceiros | demais fontes (anti-padrão) |

## 6. Lacunas conhecidas
O plugin não cita fonte inexistente nessas áreas; responde com princípios gerais rotulados Inferido e manda conferir a doc oficial.
| ID | Lacuna | Candidata a ler |
| --- | --- | --- |
| L-01 | Observabilidade de dados (frescor, volume, anomalia, SLO de pipeline) | Google SRE Workbook "Data Processing Pipelines"; docs do Elementary |
| L-02 | BI e dashboards, métricas governadas | Docs oficiais de Looker, Metabase, Superset, dbt Semantic Layer/MetricFlow |
| L-03 | Great Expectations, Soda, dbt-expectations | docs.greatexpectations.io, docs.soda.io |
| L-04 | dbt oficial: data tests, unit tests, snapshots, contracts, source freshness, materialização, página de estilo de SQL (404) | docs.getdbt.com |
| L-05 | Iceberg: manutenção, metadata tables, `writeTo` | Docs do Iceberg |
| L-06 | Delta: `VACUUM`, liquid clustering; Unity Catalog | docs.delta.io, docs.databricks.com |
| L-07 | Snowflake oficial (performance, dynamic tables, streams, tasks) e Redshift | Docs dos fornecedores |
| L-08 | Streaming atual: `KafkaSink`/`KafkaSource`, consumidor Kafka, Debezium | Docs do Flink, Kafka, Debezium |
| L-09 | Kimball: grain, dimensões conformadas, aditividade | Páginas e livros do Kimball Group |
| L-10 | OpenLineage: tipos de evento, facets, namespaces | Especificação |
| L-11 | Sinal social: Reddit bloqueado, X e YouTube sem leitura; só Hacker News | Threads de r/dataengineering, palestras Coalesce/Airflow Summit |
| L-12 | Ecossistema oficial de plugins; `awesome-copilot/instructions` | `anthropics/claude-plugins-official` |
| L-13 | Estado do CVE-2025-55284 no changelog do Claude Code | Changelog |
| L-14 | Prefect: nenhum item validado | Docs do Prefect |

## 7. Limites da verificação
- Notas de prompt dos itens V são autoatribuídas pelo validador (mesma família de modelos do pesquisador): independência parcial. Média 81,9; fracas recorrentes: exemplos (D5) e casos de borda (D11), reforçados neste plugin.
- Páginas muito longas (skills, sub-agents, Hamel) lidas só até cerca de 100 mil caracteres.
- Estrelas, forks e `pushed_at` mudam; para vários repositórios a API devolveu 403 e os números vêm da página.
- Defaults numéricos: Spark 4.2.0, Airflow 3.3.2, Flink master, ODCS 3.2.0, OpenLineage 1.53.0, Dagster 1.13.26. Confira a versão instalada.
