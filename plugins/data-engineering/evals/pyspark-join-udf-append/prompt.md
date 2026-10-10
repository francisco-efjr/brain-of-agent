---
name: pyspark-join-udf-append
description: "Mede se o plugin pede o plano antes de ajustar configuração, identifica duas causas possíveis de duplicação (append sem idempotência e join com chave não única), troca UDF por função nativa, evita collect em volume e cita a versão do Spark sem inventar números."
tags: [data-engineering, spark-streaming-review, pyspark, idempotency]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Pede EXPLAIN ou UI antes de configuração, explicita o tipo de join, aponta fan-out por chave não única e append como causas de duplicação, substitui a UDF por função nativa, evita collect, propõe escrita idempotente e auditoria de PK, cita a versão e não afirma ganho medido."
model: sonnet
---
Esse job PySpark está lento e às vezes duplica linhas na tabela de destino. Cluster com Spark 3.5. O que eu mudo?

```python
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

orders = spark.table("raw.orders")
customers = spark.table("raw.customers")

normalize_country = F.udf(lambda c: c.strip().upper() if c else None, StringType())

result = (
    orders.join(customers, "customer_id")
    .withColumn("country", normalize_country("country"))
)

print(result.collect()[:5])
result.write.mode("append").saveAsTable("mart.orders")
```
