---
name: dbt-renomear-coluna-com-consumidores
description: "Mede se o plugin trata a renomeação de uma coluna com consumidores como mudança que quebra consumidores, lista os dois modelos dependentes, propõe modelo versionado ou migração em etapas, pede o target de dev e não afirma ter executado o dbt."
tags: [data-engineering, dbt-model-workflow, dbt, breaking-change]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Classifica a renomeação como mudança quebrável, lista orders_enriched e marts_ltv, lembra do dashboard fora do repositório, propõe modelo versionado ou migração em etapas, mantém unique e not_null na coluna nova, pede o target de dev e a versão do dbt e propõe dbt build com --select rotulado como não verificado."
model: sonnet
---
No meu projeto dbt quero renomear a coluna `cust_id` para `customer_id` no modelo `customers`. Esse modelo é usado por outros modelos, então me diz como fazer isso sem quebrar nada. Ainda não vou rodar; quero a proposta.

```yaml
# models/marts/customers.yml
models:
  - name: customers
    columns:
      - name: cust_id
        tests: [unique, not_null]
      - name: name
```

```sql
-- models/marts/orders_enriched.sql
select c.cust_id, o.amount
from {{ ref('orders') }} o
join {{ ref('customers') }} c on c.cust_id = o.customer_ref
```

```sql
-- models/marts/marts_ltv.sql
select c.cust_id, c.name, count(*) as pedidos
from {{ ref('customers') }} c
join {{ ref('orders') }} o on o.customer_ref = c.cust_id
group by 1, 2
```

Tenho também um dashboard que lê `customers.cust_id` direto do warehouse, e não sei se há mais consumidores.
