---
name: metrica-fan-out-count-distinct
description: "Mede se a revisão de uma consulta de receita encontra o fan-out de junção que infla a soma, o COUNT DISTINCT que o esconde, a coluna inexistente marcada como UNVERIFIED, a divergência da definição governada, o fuso e o NOT IN com NULL, sem executar nada."
tags: [data-engineering, analytics-reviewer, metrics, fan-out, sql-review]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Marca discount_amount como UNVERIFIED, aponta que SUM de orders.amount após a junção com order_items multiplica o valor por item e que COUNT DISTINCT mascara o problema, compara com a definição governada de receita, aponta fuso e NOT IN com NULL, dá veredito crítico ou revisar e propõe verificações de sanidade sem executar."
model: sonnet
---
Revisa essa consulta de receita mensal antes de eu mandar o dashboard para a diretoria. Quero saber se os números estão certos.

Schema (BigQuery, dataset `loja`):

```text
orders(order_id STRING PK, customer_id STRING, amount NUMERIC  -- valor total do pedido, status STRING, created_at TIMESTAMP)
order_items(order_item_id STRING PK, order_id STRING, sku STRING, quantity INT64, unit_price NUMERIC)
customers(customer_id STRING PK, segment STRING)
excluded_statuses(status STRING)  -- coluna aceita NULL
```

Definição oficial da métrica, do documento de finanças: "Receita = soma de quantity x unit_price dos itens de pedidos com status 'pago' ou 'enviado', em BRL, agrupada por mês no fuso America/Sao_Paulo."

```sql
select
  c.segment,
  date_trunc(date(o.created_at), month) as mes,
  sum(o.amount) as receita,
  count(distinct o.order_id) as pedidos,
  sum(o.amount - o.discount_amount) as receita_liquida
from `loja.orders` o
join `loja.order_items` i on i.order_id = o.order_id
join `loja.customers` c on c.customer_id = o.customer_id
where o.status not in (select status from `loja.excluded_statuses`)
  and o.created_at >= '2026-01-01'
group by 1, 2
```
