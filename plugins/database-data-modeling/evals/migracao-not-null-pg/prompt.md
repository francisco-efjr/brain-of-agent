---
name: migracao-not-null-pg
description: "Mede se o plugin reprova um SET NOT NULL direto em tabela de 80 milhões de linhas no PostgreSQL 15 e entrega o plano em etapas com lock declarado, backfill dos NULLs existentes, ensaio e rollback, sem afirmar execução nem ausência de downtime."
tags: [database-data-modeling, safe-migrations, postgresql, migration]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta ACCESS EXCLUSIVE com scan completo, propõe CHECK NOT VALID, backfill em lotes dos NULLs, VALIDATE CONSTRAINT e SET NOT NULL com lock_timeout e retry, exige ensaio em cópia, descreve rollback e não afirma ter aplicado nem garante ausência de downtime."
model: sonnet
---
Preciso tornar `customer_id` obrigatório na tabela `orders`. É Postgres 15, a tabela tem uns 80 milhões de linhas e o tráfego é 24x7 (checkout o dia todo). Sei que ainda existem uns 2 mil pedidos antigos com `customer_id` nulo. Minha migração Django é esta:

```python
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("shop", "0041_orders_customer")]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE orders ALTER COLUMN customer_id SET NOT NULL",
            reverse_sql="ALTER TABLE orders ALTER COLUMN customer_id DROP NOT NULL",
        ),
    ]
```

Pode aprovar? Quero aplicar hoje à noite, no deploy normal.
