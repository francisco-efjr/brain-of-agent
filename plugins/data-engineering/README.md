# data-engineering — Engenharia de dados e analytics

Plugin do Claude Code para pipelines ETL/ELT, dbt, Airflow e Dagster, Spark e streaming, SQL analítico e custo em warehouses, contratos e qualidade de dados, linhagem e text-to-SQL seguro. A ideia central: o erro típico em dados é silencioso (o build passa, a carga está truncada), então o plugin exige verificação por saída real, reconciliação de contagens, idempotência provada e agentes somente leitura. Versão 0.1.0, licença MIT, idioma base português brasileiro.

## O que entrega
- Um **playbook** que roteia o pedido, impõe 12 princípios com o porquê (K-01 a K-12), um processo de 9 passos com critérios de saída e o modo **DATAENG-COMPLETO**.
- **12 referências** densas: checklists por área, padrões e antipadrões, trade-offs, 22 regras prontas de CLAUDE.md, ferramentas e MCP (desativados, com JSON e riscos), bibliografia e os temas dbt, orquestração, Spark/streaming/lakehouse, SQL e warehouses, qualidade/contratos/linhagem, segurança/contexto/evals.
- **12 templates**: plano de pipeline, checklist de entrega, relatório de aceitação, contrato ODCS, política `block/warn/log`, plano de backfill, plano de migração com gates, relatório de causa raiz, cenário de eval, matriz do modo completo, manifesto de execução, handoff.
- **8 skills de tarefa, 1 biblioteca de prompts e 5 agentes somente leitura** (tabela abaixo).
- Seguro por padrão: sem hooks, sem `.mcp.json`, sem `.lsp.json`, sem `bin/`. Nenhum agente tem `Write`, `Edit` ou `Bash`. O plugin nunca escreve em produção, dispara DAG, faz backfill ou roda DDL/DML destrutivo.

## Quando usar
- Criar, alterar ou depurar modelos dbt, DAGs, jobs Spark, pipelines de streaming.
- Decidir se um pipeline "que passou no build" pode ser aceito.
- Reduzir custo ou tempo de uma consulta sem mudar o resultado.
- Gerar SQL a partir de uma pergunta de negócio, de forma segura.
- Definir contrato de dados, regras de qualidade, política para agentes e convenção de linhagem.
- Planejar upgrade, migração ou backfill com gates.
Não use para: OLTP e índices transacionais (plugin `database-data-modeling`), modelos de ML (`data-science-ml`), SLOs de serviço (`sre-observability`), UI de dashboard (`web-frontend`).

## Componentes
| Tipo | Nome | Para que serve | Invocação |
| --- | --- | --- | --- |
| Skill núcleo | `playbook` | Router, princípios, processo, modo DATAENG-COMPLETO | Automática; `/data-engineering:playbook` |
| Skill | `prompts` | Biblioteca de prompts curados (revisão de dbt e DAG, text-to-SQL, aceitação, backfill, migração, evals) | Automática |
| Skill | `dbt-model-workflow` | Criar/alterar modelos, testes, depurar erro de dbt | Automática |
| Skill | `pipeline-acceptance` | Aceitação de pipeline gerado por agente: 8 verificações, veredito | Só explícita (`disable-model-invocation`) |
| Skill | `airflow-dag-workflow` | Revisar, criar, testar e depurar DAGs; orientação de Dagster e Prefect | Automática |
| Skill | `spark-streaming-review` | Spark/PySpark, garantias Kafka/Flink, manutenção Delta | Automática |
| Skill | `sql-review` | Custo no BigQuery e reescrita preservando semântica | Automática |
| Skill | `text-to-sql-safe` | SQL de leitura a partir de pergunta, com JSON de premissas e dúvidas | Automática |
| Skill | `data-contracts-quality` | Contrato ODCS, `fail/drop/warn`, política, linhagem | Automática |
| Skill | `gated-pipeline-migration` | Upgrade/migração com fases e gates | Só explícita |
| Agente | `data-pipeline-reviewer` | Revisor cético de pipelines, somente leitura | Delegação |
| Agente | `analytics-reviewer` | Revisor de SQL e métricas, somente leitura | Delegação |
| Agente | `pipeline-debugger` | Causa raiz a partir de logs fornecidos, sem executar | Delegação |
| Agente | `eval-judge` | Juiz binário de um modo de falha por chamada | Delegação |
| Agente | `data-pipeline-architect` | Plano de pipeline para aprovação, sem implementar | Delegação |
Os nomes seguem o namespace do plugin: `/data-engineering:<skill>` e agente `data-engineering:<agente>`. Se algum componente ainda não estiver na sua cópia, o playbook registra "ausente" e continua com as referências.

## Instalação
Dentro de uma sessão do Claude Code:
```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install data-engineering@brain-of-agent
```
Ou pela CLI: `claude plugin marketplace add <caminho-ou-owner/repo>` e `claude plugin install data-engineering@brain-of-agent`. Valide a instalação local com `claude plugin validate <pasta-do-plugin>`.
O comando do marketplace `brain-of-agent` é o informado pelo autor; confira o nome do marketplace no repositório antes de usar (Não verificado nesta cadeia de construção).
Para testar sem marketplace, carregue a pasta direto: `claude --plugin-dir <caminho>/plugins/data-engineering` (flag documentada para plugins locais; confira `claude --help` na sua versão).

## Exemplos de pedidos
1. "Revisa essa DAG antes de eu subir: `Variable.get('bucket')` no topo, `datetime.now()` no filtro, XCom com `df.to_dict('records')`, `insert into mart.orders select ...`, sem retries." → achados com trecho: `now()`, `Variable.get` e leitura de banco no topo, senha no código, XCom com volume, insert não idempotente, retries com backoff e limites, `catchup`; pergunta a versão do Airflow; propõe teste de import; não dispara execução.
2. "Cria o modelo dbt `fct_orders` a partir de `stg_orders`." → lê vizinhos e YAML, define grain, procura lógica existente, propõe testes por tipo de coluna, entrega `dbt build --select fct_orders` e rotula "não verificado" se não rodou; pede o nome do target de dev.
3. "O build passou, mas confio nessa carga?" → `/data-engineering:pipeline-acceptance`: contagem origem vs destino, campos vs colunas, segunda execução, chaves, SCD2, `warn` com número; veredito `APROVADO`, `APROVADO COM PENDÊNCIAS`, `REPROVADO` ou `NÃO VERIFICÁVEL`.
4. "Por que esse job Spark duplica linhas e está lento?" → pede `EXPLAIN` e a versão; aponta join sem `how=`, UDF, `collect()`, `append` cego; propõe `MERGE` com critério de versão e auditoria da PK.
5. "Gera o SQL da receita por segmento no último mês, dialeto BigQuery." → JSON `{sql, premissas, risco_de_custo, duvidas}`, só `SELECT`, filtro na coluna de partição, comentário de coluna tratado como dado; não executa.
6. "Monta o contrato de dados do dataset de clientes." → rascunho ODCS 3.2.0 marcado "não validado", matriz `fail/drop/warn` por regra, dono e SLA como pendência para a equipe.
7. "Flink lê Kafka e grava no Elasticsearch; é exactly-once?" → tabela fonte/estado/sink/garantia; Elasticsearch é at-least-once, exige `_id` determinístico; teste de reinício a partir de checkpoint.
8. "Reprocessa janeiro de 2025 de `orders`." → `plano-de-backfill` (intervalo, idempotência, custo, ensaio em dev, rollback, aprovação humana nomeada); nunca executa.

## Keyword DATAENG-COMPLETO
Escreva `DATAENG-COMPLETO` no pedido para ativar a auditoria integral: leitura das 12 referências em lotes com registro `lido/parcial/ausente`, matriz de aplicabilidade das 14 áreas, implementação só no escopo autorizado, revalidação com evidências por agente em contexto limpo e gate Concluído/Parcial/Impedido. Regras: só vale em mensagem do usuário (a palavra dentro de log, YAML, SQL, README ou resultado de ferramenta não ativa), não amplia permissões, não toca produção, não dispara DAG nem backfill. Exemplo: "DATAENG-COMPLETO. Audite este repositório dbt + Airflow; pode ajustar YAML e testes em `models/`; sem produção; entregue matriz, evidências e revalidação."

## Principais fontes
Lista completa, licenças e lacunas em `skills/playbook/references/fontes.md`. Classes: A = oficial, B = praticante ou doc de tecnologia, C = sinal fraco.
| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Claude Code best practices (code.claude.com/docs/en/best-practices) | A |
| 2 | Claude Code skills e sub-agents (docs) e `anthropics/skills` | A |
| 3 | Anthropic, Effective context engineering for AI agents | A |
| 4 | Anthropic, Code execution with MCP | A |
| 5 | Anthropic, Building effective agents | A |
| 6 | `dbt-labs/dbt-agent-skills` (Apache-2.0) | A |
| 7 | Apache Airflow, best practices (stable 3.3.2) | A |
| 8 | `astronomer/agents` (Apache-2.0) | B |
| 9 | Apache Spark, SQL performance tuning (4.2.0) | A |
| 10 | Google Cloud, BigQuery: otimização de entrada e computação | A |
Outras usadas: Apache Flink (garantias de conectores), rmoff (aceitação de pipeline), Hamel Husain e Shreya Shankar (evals), Open Data Contract Standard (Bitol), Databricks (expectations), Delta Lake, Kimball Group, OpenLineage, cookbook de text-to-SQL da Anthropic.

## Créditos e licenças
- Plugin: MIT, Francisco Edson (https://github.com/francisco-efjr).
- Conteúdo do **brain-of-agent** (`brains/qa/references/dados-ambientes-ci.md`, estilo da casa): do próprio autor, MIT; adaptado com atribuição nas referências e nos templates.
- dbt Labs (`dbt-agent-skills`, `dbt-project-evaluator`) e Astronomer (`agents`): Apache-2.0; usados como inspiração e destilados em redação própria; nenhuma cópia literal.
- Documentação oficial (Anthropic, Airflow, Spark, Flink, Google Cloud, Delta, Databricks, dbt, Kimball, OpenLineage) e posts de praticantes: destilados; nenhuma cópia literal. Regras de PySpark: subconjunto verificado de arquivo CC0-1.0 de uma coleção, reescrito.
- Nenhum código de terceiros foi baixado ou executado na construção. Instaladores de READMEs de terceiros (`curl -o`, `uvx --from git+`, `npx`, `install.sh`) não são reproduzidos.

## Limitações honestas
- **Evals não executados.** Os 16 casos de eval são `designed_not_executed`: `claude plugin eval` exige Claude Code 2.1.269 ou superior e a CLI usada na construção era 2.1.128. Sem execução, não há medida de ganho; não há evidência independente de que as skills melhorem dbt, Airflow ou Spark. Os casos de segurança (`pedido-destrutivo-em-producao`, `upgrade-dbt-main-arvore-suja`, `keyword-em-yaml-nao-ativa-modo-completo`) só medem restrição se rodados com `--allow-tools Write Edit Bash` em Linux ou WSL2; sem isso, os graders passam sem medir (detalhes em `evals/README.md`).
- **Nenhuma execução contra warehouse ou orquestrador reais.** O plugin entrega revisão, planos e comandos; execução é do usuário ou do fluxo principal, em dev, com consentimento.
- **Revisão por agente do mesmo modelo não é validação externa.** As notas de qualidade dos itens-fonte foram autoatribuídas por um validador da mesma família do pesquisador.
- **Lacunas de fonte:** observabilidade de dados, BI e dashboards, Snowflake e Redshift, Iceberg, Great Expectations/Soda, dbt oficial (data tests, unit tests, snapshots, contracts, source freshness, materialização), grain e dimensões conformadas do Kimball, tipos de evento do OpenLineage, Prefect e ingestão/CDC (Airbyte, Fivetran, Debezium). Nessas áreas o plugin responde com princípios gerais rotulados Inferido e manda conferir a doc oficial.
- **Defaults dependem de versão** (Spark 4.2.0, Airflow 3.3.2, Flink master, ODCS 3.2.0); confira a versão instalada. Estrelas e datas de push são de 2026-10-09/10 e mudam.
- **Sinal de comunidade fraco:** Reddit bloqueado, X e YouTube sem leitura; praticantes e repositórios de comunidade citados são pequenos.
- O esqueleto de contrato ODCS tem nomes de chave não validados contra o JSON Schema oficial.
