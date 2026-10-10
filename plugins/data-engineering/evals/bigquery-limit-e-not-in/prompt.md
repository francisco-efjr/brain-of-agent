---
name: bigquery-limit-e-not-in
description: "Mede se o plugin explica que LIMIT não reduz os bytes lidos em SELECT estrela no BigQuery, propõe colunas explícitas, filtro de partição e dry run, e recusa trocar NOT IN por NOT EXISTS sem tratar NULL, apresentando a evidência de equivalência."
tags: [data-engineering, sql-review, bigquery, cost, semantics]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Explica que LIMIT não reduz bytes lidos, propõe colunas explícitas, filtro em event_date e dry run, e avisa que NOT IN com NULL na subconsulta muda o resultado em relação a NOT EXISTS, trocando só se a coluna não aceitar NULL ou devolvendo a original com a explicação."
model: sonnet
---
No BigQuery, `SELECT * FROM sales.events LIMIT 10` ainda cobra o scan inteiro da tabela. Ela é particionada por `event_date` e tem uns 4 TB. Além disso quero acelerar esta consulta trocando `NOT IN` por `NOT EXISTS`; a coluna `customer_id` de `sales.blocked` aceita NULL.

```sql
select e.event_id, e.customer_id, e.amount
from sales.events e
where e.event_date >= '2026-09-01'
  and e.customer_id not in (select customer_id from sales.blocked)
```

Posso fazer a troca e ganhar desempenho?
