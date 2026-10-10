---
name: explain-fk-sem-indice
description: "Mede se o plugin lê um EXPLAIN ANALYZE colado, aponta divergência de estimativa e FK sem índice, propõe índice com CONCURRENTLY e pede novo plano, sem prometer ganho numérico."
tags: [database-data-modeling, query-plan-and-indexing, postgresql, explain]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Nota a divergência entre linhas estimadas e reais, identifica o Seq Scan em order_items por falta de índice na FK, propõe índice em order_items(order_id) com CONCURRENTLY fora de transação, pede novo EXPLAIN e trata o ganho como suposição."
model: sonnet
---
Essa consulta que lista os itens de um pedido está levando 4 segundos no Postgres 15 (a tabela `order_items` tem uns 2,4 milhões de linhas e recebe escrita o dia todo). Qual índice eu crio?

```sql
SELECT o.id, oi.sku, oi.quantity
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
WHERE o.id = 987654;
```

DDL:

```sql
CREATE TABLE orders (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id bigint NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE order_items (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  order_id bigint NOT NULL REFERENCES orders(id),
  sku text NOT NULL,
  quantity int NOT NULL
);
```

Saída do `EXPLAIN (ANALYZE, BUFFERS)` que rodei na réplica:

```
Nested Loop  (cost=0.43..61238.50 rows=1200 width=40) (actual time=0.05..4101.30 rows=3 loops=1)
  Buffers: shared hit=8 read=26212
  ->  Index Scan using orders_pkey on orders o  (cost=0.43..8.45 rows=1 width=8) (actual time=0.02..0.03 rows=1 loops=1)
        Index Cond: (id = 987654)
        Buffers: shared hit=4
  ->  Seq Scan on order_items oi  (cost=0.00..61230.00 rows=1200 width=36) (actual time=0.03..4101.20 rows=3 loops=1)
        Filter: (order_id = 987654)
        Rows Removed by Filter: 2399997
        Buffers: shared hit=4 read=26212
Planning Time: 0.210 ms
Execution Time: 4101.52 ms
```
