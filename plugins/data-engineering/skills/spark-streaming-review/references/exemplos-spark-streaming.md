# Exemplos para `spark-streaming-review`

Redação própria, destilada de V-16 (Spark 4.2.0), V-17 (subconjunto verificado das regras PySpark), V-20 (Flink master), V-21 (Delta OSS) e do brain-of-agent (`dados-ambientes-ci.md`, MIT, do autor). Trechos de código e planos são ilustrativos e não foram executados. Onde a fonte validada não cobre o assunto (Structured Streaming, Kafka consumidor, `VACUUM`, Iceberg), o rótulo é Inferido: confira na documentação da versão instalada.

## Sumário

1. PySpark: antes e depois (caso E-04)
2. Ler um plano de execução
3. Tabela fonte, estado, sink, garantia
4. Teste de reinício a partir de checkpoint
5. Flink e Kafka: sink transacional (Inferido)
6. Manutenção de tabelas Delta

## 1. PySpark: antes e depois

Antes (Spark 3.5, sintomas: lento e às vezes duplica):

```python
orders = spark.table("raw.orders")
customers = spark.table("raw.customers")
normalize = F.udf(lambda c: c.strip().upper() if c else None)
result = orders.join(customers, "customer_id").withColumn("country", normalize("country"))
rows = result.collect()
result.write.mode("append").saveAsTable("mart.orders")
```

Problemas, cada um com o motivo:
- `join` sem `how=`: inner por omissão, pedidos sem cliente somem sem aviso (regra 1).
- UDF Python para normalizar texto: serializa linha a linha entre JVM e Python e bloqueia otimização; existe função nativa (regra 3).
- `collect()` sem uso: traz o resultado inteiro ao driver; risco de falta de memória e tempo perdido.
- `append` cego: a reexecução do mesmo lote (retry, backfill) duplica linhas (regra 5, K-04).
- Nada verifica unicidade da PK depois da escrita (regra 6).

Depois (rascunho; confirme o tamanho da dimensão antes de usar `broadcast`):

```python
from delta.tables import DeltaTable
from pyspark.sql import Window, functions as F

orders = (spark.table("raw.orders")
          .filter((F.col("order_date") >= start) & (F.col("order_date") < end)))   # intervalo explícito
customers = spark.table("raw.customers").select("customer_id", "country")

joined = orders.join(F.broadcast(customers), on="customer_id", how="left")        # left: decisão de negócio
batch = joined.select(
    F.col("order_id").cast("string").alias("order_id"),
    F.col("customer_id").cast("string").alias("customer_id"),
    F.upper(F.trim(F.col("country"))).alias("country"),                           # nativo, sem UDF
    F.col("amount").cast("decimal(18,2)").alias("amount"),
    F.col("updated_at"),
)

# uma linha por chave: o MERGE falha ou fica ambíguo com duas linhas de origem para a mesma chave
w = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc())
latest = batch.withColumn("rn", F.row_number().over(w)).filter("rn = 1").drop("rn")

(DeltaTable.forName(spark, "mart.orders").alias("t")
    .merge(latest.alias("s"), "t.order_id = s.order_id")
    .whenMatchedUpdateAll(condition="s.updated_at > t.updated_at")                # critério explícito, ordem não importa
    .whenNotMatchedInsertAll()
    .execute())

alvo = spark.table("mart.orders").filter((F.col("order_date") >= start) & (F.col("order_date") < end))
assert alvo.groupBy("order_id").count().filter("count > 1").count() == 0         # auditoria da PK
assert alvo.filter(F.col("order_id").isNull()).count() == 0
```
Notas: a API de merge acima é a do Delta (Python); em Iceberg ou Hudi use `MERGE INTO` em SQL conforme a documentação do formato. `F.broadcast` só depois de medir a tabela de clientes (limiar automático de 10 MB em 4.2.0). Os asserts rodam em job de verificação em dev, não no caminho crítico de produção, se o custo for alto. Nenhum ganho de tempo está afirmado: meça antes e depois.

## 2. Ler um plano de execução

Peça `EXPLAIN FORMATTED <consulta>` (SQL) ou `df.explain("formatted")` (PySpark), ou a captura da aba SQL da UI. Trecho ilustrativo do plano do "antes":

```text
AdaptiveSparkPlan isFinalPlan=false
+- Project [...]
   +- BatchEvalPython [<lambda>(country)]
      +- SortMergeJoin [customer_id], [customer_id], Inner
         :- Exchange hashpartitioning(customer_id, 200)
         :  +- FileScan parquet raw.orders [...] PartitionFilters: [], PushedFilters: []
         +- Exchange hashpartitioning(customer_id, 200)
            +- FileScan parquet raw.customers [...]
```

O que procurar:

| Sinal no plano | Leitura | Ação candidata |
| --- | --- | --- |
| `BatchEvalPython` / `ArrowEvalPython` | UDF Python (ou pandas UDF) no caminho | função nativa; se não houver, avaliar pandas UDF |
| `SortMergeJoin` com um lado pequeno | broadcast não aplicado (tamanho desconhecido ou acima do limiar) | `ANALYZE TABLE` para estatísticas; broadcast só se confirmado |
| `Exchange hashpartitioning(..., 200)` | shuffle; 200 é o default de `spark.sql.shuffle.partitions` em 4.2.0 | reduzir shuffles antes de ajustar partições; AQE junta partições pequenas |
| `PartitionFilters: []` com tabela particionada | filtro de partição não aplicado | filtrar a coluna de partição diretamente, sem função sobre ela |
| `isFinalPlan=false` | plano inicial com AQE; o final só existe após a execução | consultar a UI depois de rodar |

Skew aparece na UI como uma tarefa muito mais lenta/maior que as demais na etapa do join; AQE trata skew de join quando a partição passa de fator 5.0 vezes a mediana e do limiar de 256 MB (defaults de 4.2.0). Com 3.x, valores podem diferir: confirme.

## 3. Tabela fonte, estado, sink, garantia

Garantias da documentação do Flink (master, V-20): fontes Kafka, Kinesis, arquivos e coleções são exactly-once; sockets, at-most-once; Google PubSub, at-least-once; RabbitMQ varia com a versão do conector. Sinks Elasticsearch, OpenSearch, DynamoDB, Kinesis Streams e Firehose, Redis, sockets e stdout são at-least-once; Kafka é exactly-once com produtor transacional; Cassandra é exactly-once só com atualizações idempotentes; arquivos são exactly-once.

| Pipeline | Fonte | Estado | Sink | Garantia fim a fim | Verificação |
| --- | --- | --- | --- | --- | --- |
| pedidos -> busca | Kafka | checkpoint Flink | Elasticsearch | at-least-once; efetivamente-uma-vez só com `_id` determinístico | reiniciar do checkpoint; contar documentos por `_id` |
| pedidos -> tópico enriquecido | Kafka | checkpoint Flink | Kafka transacional | exactly-once, desde que o consumidor leia só confirmados | reiniciar; consumidor com `read_committed` não vê duplicata (Inferido) |
| cliques -> lake | Kafka | checkpoint Spark Structured Streaming | Delta via `foreachBatch` + `MERGE` por chave | idempotente por chave (um micro-lote pode reexecutar após falha) | reiniciar; `count(*)` = `count(distinct chave)` (Inferido: Structured Streaming não foi pesquisado, L-08) |

Regra de ouro: a garantia ponta a ponta é a mais fraca da cadeia, a menos que o sink seja idempotente. Escreva a coluna "Verificação" mesmo que ainda não tenha sido executada, e rotule como "Não verificado".

## 4. Teste de reinício a partir de checkpoint

Roteiro para o usuário executar em dev (a skill não executa):
1. Gerar tráfego conhecido: N mensagens com chaves determinísticas, incluindo duplicadas e fora de ordem (brain: mensagem duplicada/fora de ordem, payload parcial, resposta perdida após processar).
2. Derrubar o job no meio (kill do processo/cancelar com savepoint conforme o motor).
3. Reiniciar do checkpoint (ou savepoint) com o mesmo código.
4. Contar no destino: `count(*)` e `count(distinct chave)` devem coincidir com o esperado; nenhuma chave perdida; nenhuma duplicada.
5. Registrar versão do motor, do conector, configuração de checkpoint e resultado no manifesto de execução (`manifesto-de-execucao.md`).
Aceite: contagens e chaves iguais ao oráculo; qualquer desvio reprova a afirmação "exactly-once".

## 5. Flink e Kafka: sink transacional (Inferido)

A pesquisa não abriu a documentação do conector Kafka (V-20: o nome `KafkaSink` em vez de `FlinkKafkaProducer` não foi verificado). Se for confirmado na versão instalada, o padrão é:

```java
KafkaSink<String> sink = KafkaSink.<String>builder()
    .setBootstrapServers(servers)
    .setRecordSerializer(serializer)
    .setDeliveryGuarantee(DeliveryGuarantee.EXACTLY_ONCE)   // transações do Kafka
    .setTransactionalIdPrefix("pedidos-enriquecidos")       // único por job
    .build();
```
Condições (Inferido, conferir): checkpointing ligado; `transaction.timeout.ms` do produtor maior que o intervalo de checkpoint mais o tempo de reinício, e dentro do limite do broker; consumidores com `isolation.level=read_committed`. Sem isso, EXACTLY_ONCE na configuração não vira exactly-once na prática.

## 6. Manutenção de tabelas Delta

Fonte: V-21 (docs.delta.io/optimizations-oss, versão do Delta importa). `VACUUM` e liquid clustering não estão nessa página.

```sql
-- inspeção (leitura)
DESCRIBE DETAIL mart.orders;                 -- numFiles, sizeInBytes
-- compactação limitada por partição (idempotente)
OPTIMIZE mart.orders WHERE order_date >= '2026-10-01';
-- Z-ORDER: só após medir filtros reais; não é idempotente
OPTIMIZE mart.orders WHERE order_date >= '2026-10-01' ZORDER BY (customer_id);
```
Orientações: separar o job de compactação do job de carga; auto compaction existe a partir do Delta 3.1.0 (alvo de 128 MB) e optimized write é desligado por padrão (V-21); `delta.dataSkippingNumIndexedCols` limita as colunas com estatísticas. Para `VACUUM`: registrar a retenção atual do time travel e quem depende dele, preferir o modo `DRY RUN` quando a plataforma o oferece (Inferido) para listar o que seria apagado, e deixar a execução ao usuário com autorização explícita.
