# Spark, streaming e lakehouse

Quando abrir: job Spark/PySpark lento, errado ou duplicando; garantias de entrega em Kafka/Flink; compactação e manutenção Delta; dúvida sobre Iceberg.
Rótulos: Verificado = V-16, V-17, V-20, V-21 (conferidos em 2026-10-10 contra Spark 4.2.0 "latest", Flink master e docs.delta.io); Inferido = conhecimento estável ou dedução; Lacuna = sem fonte. Defaults numéricos mudam por versão: cite sempre a versão e confira a instalada.

## Sumário
1. Tuning de Spark SQL: ler o plano primeiro
2. Defaults de Spark 4.2.0
3. Regras de PySpark
4. Streaming: garantias por fonte, estado e sink
5. Testes de pipeline: reinício, duplicidade, fora de ordem
6. Delta Lake: manutenção
7. Iceberg e lacunas

## 1. Tuning de Spark SQL: ler o plano primeiro
Fonte: V-16 (spark.apache.org, Classe A). Sequência:
1. Peça `EXPLAIN` (ou `EXPLAIN FORMATTED`) e/ou a aba SQL da UI antes de tocar em configuração. Sem plano, qualquer ajuste é chute.
2. Mantenha estatísticas (`ANALYZE TABLE ... COMPUTE STATISTICS`) para o otimizador escolher joins.
3. Broadcast só de dimensão pequena e confirmada. Hints de join não são garantia.
4. AQE ligado: junta partições pequenas, troca a estratégia de join e divide skew.
5. Procure skew na etapa de join (uma tarefa muito mais longa que as outras).
6. Reduza shuffle antes de ajustar o número de partições.
7. Cite a versão do Spark ao recomendar qualquer valor.
Exemplo de resposta a "o job está lento": (a) pergunte versão e cole do plano; (b) aponte, no plano, `SortMergeJoin` com dimensão pequena como candidata a broadcast; (c) sugira `ANALYZE TABLE` se as estatísticas faltam; (d) só então proponha valor de configuração, com a versão citada; (e) rotule o ganho como "não medido".

## 2. Defaults de Spark 4.2.0
Verificados na página "latest" em 2026-10-10 (V-16); confira a versão instalada.
| Propriedade | Default |
| --- | --- |
| `spark.sql.shuffle.partitions` | 200 |
| `spark.sql.files.maxPartitionBytes` | 128 MB |
| `spark.sql.files.openCostInBytes` | 4 MB |
| `spark.sql.autoBroadcastJoinThreshold` | 10 MB |
| AQE (`spark.sql.adaptive.enabled`) | ligado |
| `spark.sql.adaptive.advisoryPartitionSizeInBytes` | 64 MB |
| Skew: fator / limiar | 5.0 / 256 MB |
| `spark.sql.broadcastTimeout` | 300 s |

## 3. Regras de PySpark
As oito regras verificadas, com motivo e exemplo, estão em [padroes-e-antipadroes.md](padroes-e-antipadroes.md) (seção 2): join com `how=`; broadcast só de dimensão pequena; função nativa; schema declarado; merge idempotente com critério; auditoria de PK; sessão injetada; configuração como dado.
Exemplo de revisão. Código:
```python
result = orders.join(customers, "customer_id")
result = result.withColumn("country", normalize_udf("country"))
rows = result.collect()
result.write.mode("append").saveAsTable("mart.orders")
```
Achados esperados: (1) join sem `how=`; (2) UDF Python onde `F.upper(F.trim(...))` serve; (3) `collect()` traz tudo ao driver sem necessidade (não é pré-requisito para escrever); (4) `append` cego duplica em retry: usar `MERGE` por chave com critério de versão; (5) sem auditoria de unicidade e nulos da PK após a escrita; (6) sem versão do Spark, nenhuma configuração deve ser recomendada. Caso de borda: o usuário não tem o plano. Peça `EXPLAIN`; entregue os achados de código e marque o tuning como "não verificado".
Não afirme que `printSchema()` dispara job (não dispara).

## 4. Streaming: garantias por fonte, estado e sink
Fonte: V-20 (Flink master, Classe A; a doc não define formalmente as semânticas e a branch master muda; configuração do consumidor Kafka não foi lida).
| Componente | Garantia (doc) |
| --- | --- |
| Fontes Kafka, Kinesis, arquivos, coleções | Exactly-once |
| Socket | At-most-once |
| Google PubSub | At-least-once |
| RabbitMQ | Varia com a versão do conector |
| Sinks Elasticsearch, OpenSearch, DynamoDB, Kinesis Streams e Firehose, Redis, sockets, stdout | At-least-once |
| Sink Kafka | Exactly-once com produtor transacional (Kafka 0.11 ou superior) |
| Sink Cassandra | Exactly-once só com atualizações idempotentes |
| Sink arquivos | Exactly-once |
Procedimento: para cada pipeline, preencha a tabela fonte / estado / sink / garantia (template `plano-de-pipeline.md`). Sink sem transação precisa ser idempotente (id determinístico por documento ou chave natural). Confirme o nome da classe do conector na versão instalada: resumos citavam `FlinkKafkaProducer`, hoje `KafkaSink` (não verificado nesta cadeia).
Exemplo (E-05): "Flink lê Kafka e grava no Elasticsearch; o time diz que é exactly-once porque há checkpoint." Resposta: fonte Kafka = exactly-once; estado Flink com checkpoint; sink Elasticsearch = at-least-once; garantia ponta a ponta = at-least-once, a menos que o `_id` do documento seja determinístico (reescrever o mesmo documento é idempotente). Teste: matar o job, reiniciar do checkpoint, contar documentos duplicados por chave de negócio. Pergunte a versão do Flink e do conector.
Spark Structured Streaming (Inferido; não coberto por V): idempotência no sink via `foreachBatch` com `MERGE` por chave; watermark para atraso de dados; checkpoint em armazenamento durável. Confirme na doc do Spark da versão instalada.

## 5. Testes de pipeline: reinício, duplicidade, fora de ordem
Adaptado de "Virtualização e falhas controladas" (brain-of-agent, MIT) para CDC, streaming e APIs de origem.
| Falha simulada | O que observar além do erro visível |
| --- | --- |
| Timeout antes de processar | Tentativa limitada; nada gravado pela metade |
| Resposta perdida após processar | Reconciliação por identidade; sem duplicata |
| 429 / limite de capacidade | Respeito ao contrato de retry; sem tempestade de requisições |
| Payload parcial ou inválido | Tratamento explícito; não virar valor padrão perigoso em silêncio |
| Mensagem duplicada / fora de ordem | Idempotência e transição de estado válida; o registro novo não é sobrescrito pelo velho |
| Reinício a partir de checkpoint | Sem perda, sem duplicidade (contagem por chave) |
| Indisponibilidade prolongada | Backlog, recuperação, alerta |
Declare o que a simulação não prova (um broker de teste não prova ACLs nem desempenho de produção). Virtualizador de API estrito: requisição inesperada falha com diagnóstico.

## 6. Delta Lake: manutenção
Fonte: V-21 (docs.delta.io, otimizações OSS; Classe B). `VACUUM` e liquid clustering não estão na página: lacuna.
| Operação | Fato verificado | Regra do plugin |
| --- | --- | --- |
| `OPTIMIZE` | Idempotente; pode ser limitado por predicado de partição | Rodar em job separado do de carga; limitar por partição em tabelas grandes |
| Auto compaction | Disponível a partir da 3.1.0; alvo de 128 MB | Conferir a versão instalada |
| Optimized write | Desligado por padrão | Decisão consciente |
| Z-ORDER | Em colunas de predicado com alta cardinalidade; não idempotente | Só depois de medir os filtros reais |
| `delta.dataSkippingNumIndexedCols` | Limita as colunas com estatísticas | Ajustar com medição |
| `VACUUM` | Fora da fonte lida | Registrar a retenção atual antes; nunca executar sem autorização do usuário (remove arquivos; Inferido: pode quebrar leitores e time travel) |
Exemplo de resposta a "muitos arquivos pequenos na tabela `events`": proponha job de compactação separado com `OPTIMIZE events WHERE event_date >= current_date() - 7` (predicado de partição; sintaxe a conferir na versão), sem Z-ORDER até medir; peça a retenção atual; não proponha `VACUUM` agora.

## 7. Iceberg e lacunas
Iceberg (L-05): sem fonte aprovada. As regras `__partitions` e `byName()` de uma coleção não conferem com a doc do Iceberg; o caminho documentado de escrita é `writeTo(...)`. Para manutenção (expire de snapshots, reescrita de arquivos, remoção de órfãos), aponte a doc oficial do Iceberg da versão instalada e rotule qualquer orientação como Inferido.
Outras lacunas: consumidor Kafka (isolation level, transações), Debezium/CDC (L-08), Unity Catalog (L-06), liquid clustering. Diga que não há fonte e não invente.
