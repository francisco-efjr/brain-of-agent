# Decisões e trade-offs em engenharia de dados

Quando abrir: escolher entre alternativas (workflow ou agente, batch ou streaming, estratégia de carga, tipo de SCD, ferramenta de qualidade) ou entender por que o plugin adota uma posição quando fontes divergem.
Rótulos: Verificado = V-nn; Inferido = conhecimento estável do domínio ou dedução do autor (confira a doc da versão instalada).
Regra de uso: registre a alternativa descartada em 1 linha (template `plano-de-pipeline.md`, seção "Desenho").

## Sumário
1. Workflow fixo ou agente aberto
2. Batch ou streaming
3. Estratégia de carga: append, MERGE, delete+insert, overwrite de partição, full refresh
4. Garantias de entrega por fonte e sink
5. Ação por regra de qualidade: fail, drop, warn
6. Tipo de SCD pela pergunta de negócio
7. dbt: modelo novo, versionar ou editar; materialização
8. Orquestrador: Airflow, Dagster, Prefect
9. Contrato e organização: ODCS, data mesh
10. Onde colocar cada regra do agente
11. Conflitos entre fontes e como o plugin resolveu

## 1. Workflow fixo ou agente aberto (V-04, Classe A)
Princípio: comece pela solução mais simples; um agente precisa de ground truth a cada passo e de condição de parada.
| Situação | Desenho | Porquê |
| --- | --- | --- |
| Carga recorrente com schema conhecido (ingestão, staging, marts, testes) | Workflow com checagem entre etapas (prompt chaining) | O caminho é conhecido; o valor está em não pular a checagem |
| Classificação em massa de registros | Paralelização com amostra revisada por humano | Erro sistemático aparece na amostra antes de escalar |
| Investigação de anomalia de métrica | Agente com teto de passos, ferramentas somente leitura e saída com evidência | O caminho não é conhecido; leitura não causa dano |
| Qualquer escrita em produção | Passo humano explícito | Nunca decisão do agente |
Exemplo: "a receita de ontem caiu 18%". Agente de leitura: confere frescor das fontes, compara contagem por partição, procura mudança de versão de DAG; entrega hipóteses ordenadas e o experimento mais barato de cada uma. Não "corrige" nada.

## 2. Batch ou streaming (Inferido; conhecimento estável)
| Critério | Batch | Streaming |
| --- | --- | --- |
| Latência exigida pelo consumidor | Horas/dia aceitáveis | Segundos a minutos com decisão que depende disso |
| Custo operacional | Menor (jobs efêmeros, reprocesso simples) | Maior (estado, checkpoint, reinício, ordem) |
| Correção de dado atrasado | Reprocessar a partição | Watermark e janela de atraso; reprocesso é mais difícil |
| Teste | Fixture e duas execuções | Reinício a partir de checkpoint, duplicidade, fora de ordem |
Pergunta que decide: "qual decisão muda se o dado chegar 1 hora antes?" Sem resposta concreta, batch. Micro-batch frequente costuma ser o meio-termo; documente o SLA de frescor no contrato.

## 3. Estratégia de carga (Inferido, ancorado em V-13, V-25, V-17)
| Estratégia | Quando | Risco |
| --- | --- | --- |
| `append` | Log imutável com id único e deduplicação a jusante | Duplica em retry; só com chave de idempotência |
| `MERGE` por chave | Dimensões e fatos com atualização; fonte entrega a última versão | Critério de "qual versão vence" precisa ser explícito (timestamp/versão) |
| Apagar o intervalo e inserir (transação) | Fatos particionados por data, reprocesso por janela | Precisa ser atômico; sem transação, janela vazia visível |
| Overwrite de partição | Lakehouse particionado, reprocesso por partição | Sobrescreve a partição inteira: confirmar escopo (S-06) |
| Full refresh | Tabela pequena ou reconstruível | Destrutivo em incremental; confirmar |
| `CREATE OR REPLACE` | Tabela derivada reconstruível, sem grants dependentes | Apaga dados e grants; não é idempotência (X-05) |
Teste que vale para todas: rodar duas vezes e comparar contagem e soma de controle.

## 4. Garantias de entrega por fonte e sink (V-20, Flink master)
| Componente | Garantia segundo a doc |
| --- | --- |
| Fontes Kafka, Kinesis, arquivos, coleções | Exactly-once |
| Fonte socket | At-most-once |
| Fonte Google PubSub | At-least-once |
| Fonte RabbitMQ | Varia com a versão do conector |
| Sinks Elasticsearch, OpenSearch, DynamoDB, Kinesis Streams/Firehose, Redis, sockets, stdout | At-least-once |
| Sink Kafka | Exactly-once com produtor transacional (Kafka 0.11 ou superior) |
| Sink Cassandra | Exactly-once só com atualizações idempotentes |
| Sink arquivos | Exactly-once |
Como decidir: a garantia ponta a ponta é a mais fraca da cadeia, a menos que o sink seja idempotente. Exemplo: Kafka (exactly-once) → Flink → Elasticsearch (at-least-once) exige id de documento determinístico; sem ele há duplicata após reinício. Confirme o nome da classe do conector na versão instalada (`KafkaSink`; resumos de busca citavam `FlinkKafkaProducer`, não verificado).

## 5. Ação por regra de qualidade (V-22, Databricks; conceito vale para dbt `severity` e outras ferramentas)
| Tipo de regra | Ação | Reporta | Porquê |
| --- | --- | --- | --- |
| Chave de negócio nula ou duplicada | `fail` | Contagem e amostra mascarada | Dado quebrado propaga erro a jusante |
| Campo com faixa conhecida | `drop` | Contagem; quarentena em outro fluxo | Descartar sem reportar esconde perda |
| Enriquecimento opcional | `warn` | Número de pendências | Não bloqueia, mas vira item de trabalho |
Notas: ação padrão no Databricks é `warn`; `expect`, `expect_or_drop`, `expect_or_fail` em Python; `CONSTRAINT ... EXPECT (...) ON VIOLATION DROP ROW | FAIL UPDATE` em SQL; a cláusula precisa ser expressão SQL booleana, sem Python customizado, chamadas externas ou subconsultas.

## 6. Tipo de SCD pela pergunta de negócio (V-27 para os tipos; a heurística é Inferido)
| Pergunta | Tipo | Efeito |
| --- | --- | --- |
| Valor original importa para sempre? | 0 | Retém original |
| Só o valor atual importa (correção de erro)? | 1 | Sobrescreve; perde histórico |
| Preciso do valor vigente na data do evento? | 2 | Nova linha por versão (em dbt, snapshot) |
| Preciso comparar só "atual vs anterior"? | 3 | Coluna extra de valor anterior |
| Atributos mudam rápido e são muitos | 4 | Mini-dimensão |
Tipos 5, 6 e 7 combinam técnicas (V-27 só lista os títulos). Em tipo 2, `check_cols`/`updated_at` precisa cobrir os campos historicamente relevantes (V-05).

## 7. dbt: modelo novo, versionar ou editar; materialização
| Decisão | Regra | Fonte |
| --- | --- | --- |
| Criar modelo novo? | Só depois de procurar lógica existente e justificar por escrito | V-07 |
| Editar no lugar? | Só se nenhum consumidor quebra | V-07 |
| Renomear/remover/mudar tipo com consumidores | Modelo versionado + lista de consumidores (conferir recurso de versões na versão instalada) | V-07 |
| view, table, incremental | Inferido: view para staging leve; table para marts consultados com frequência; incremental quando o volume impede reconstruir. Página oficial de materialização não lida (L-04) | V-10 |

## 8. Orquestrador: Airflow, Dagster, Prefect (conceitual)
O plugin não escolhe pela marca; os princípios são os mesmos: idempotência, intervalo explícito, sem trabalho no import, segredos fora do código, consentimento antes de executar, teto de 3 ciclos.
| Aspecto | Airflow (V-13, doc 3.3.2) | Dagster (V-15, parcial) | Prefect |
| --- | --- | --- | --- |
| Modelo | DAG de tarefas; Assets no Airflow 3 | Assets declarativos (`@dg.asset`) | Lacuna L-14: sem fonte; só princípios (Inferido) |
| Verificação local | Teste de import da DAG | `dg check`, `dg list defs`, `dg launch` local | Conferir doc da versão |
| Cuidado | Importações mudam entre 2 e 3 | `dg launch`, `dg api`, `dg plus` alteram estado | Conferir doc |

## 9. Contrato e organização (V-23, V-29)
- ODCS (Open Data Contract Standard) 3.2.0: contrato por dataset (13 seções). Use quando há consumidor externo à equipe ou SLA.
- Data mesh (Dehghani, 03/12/2020): quatro princípios (propriedade por domínio, dado como produto, plataforma de autoatendimento, governança computacional federada). Conceito de organização, não regra técnica; use como checklist de produto de dados: dono, contrato, métricas de qualidade, frescor, canal de suporte.

## 10. Onde colocar cada regra do agente (prompt-principles P-38)
Hook (o que vale sempre; documentado, não ativo aqui) → `permissions.deny/ask` → role do warehouse → CLAUDE.md (fato universal e curto, menos de 200 linhas) → regra com `paths` (ex.: PySpark só em `jobs/**/*.py`) → skill (fluxo sob demanda) → subagente (revisão em contexto limpo) → MCP. Instrução é pedido; permissão e role são garantia.

## 11. Conflitos entre fontes e como o plugin resolveu
| ID | Conflito | Resolução |
| --- | --- | --- |
| X-01 | `allowed-tools` "restringe" (resumos) vs "pré-aprova" (doc) | Segue a doc; contenção em `tools`/`disallowedTools` e `permissions.deny` |
| X-02 | `testing-dags` da Astronomer dispara sem consentimento nem teto | Plugin exige aprovação do plano, consentimento antes de disparar e no máximo 3 ciclos (salvaguardas nossas) |
| X-03 | Skill dbt principal não exige `build`; Altimate exige | Exigir `dbt build --select <modelo>` em dev |
| X-04 | Regras PySpark/Snowflake de coleção com erros | Só o subconjunto verificado |
| X-05 | `CREATE OR REPLACE` como idempotência vs destrutivo | `MERGE` ou partição; `CREATE OR REPLACE` só em derivada reconstruível, com confirmação |
| X-06 | Juiz binário (Hamel) vs nota 1 a 5 (dbt Labs) vs 0 a 3 (rmoff) | Juiz binário por modo de falha; escala só para triagem humana |
| X-07 | Revisor "caçador de falhas" sempre acha algo vs revisão adversarial | Adversarial em contexto novo, restrito a correção e requisitos, com lista "não reportar" (estilo) |
| X-08 | Hooks de confirmação/bloqueio (repos) vs hook não é fronteira vs política sem hooks ativos | Sem hooks no plugin; hook documentado; fronteira real é role, `deny` e sandbox |
| X-09 | "Skills pesam mais que o modelo" vs "ajudaram menos que o esperado" | Sem veredito; método de A/B com e sem skill |
| X-10 | Números do rmoff não batem com o log | Não citar os números |
| X-11 | Lista de 15 regras de DAG da Astronomer incorreta em resumos | Lista corrigida e doc oficial |
| X-12 | Defaults numéricos mudam por versão | Sempre citar a versão |
| X-13 | Instalação "oficial" de skills de dados vs plugin seguro por padrão | Documentar o comando como ação do usuário; não replicar |
