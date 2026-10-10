---
name: negativo-limitrofe-dbt
description: "Caso negativo limítrofe: pedido de modelo dbt incremental no Snowflake (engenharia de dados), vizinho do segmento de bancos. Mede se nenhuma skill de tarefa do plugin é acionada e se o pedido é atendido como dbt."
tags: [database-data-modeling, negative, boundary, data-engineering]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um modelo dbt incremental para Snowflake com is_incremental e unique_key sem acionar skills de tarefa do plugin de bancos de dados transacionais."
model: sonnet
---
Crie um modelo dbt incremental no Snowflake para a tabela fato de pedidos (`fct_orders`). A origem é `stg_orders` (colunas `order_id`, `customer_id`, `status`, `total_amount`, `updated_at`), pedidos podem ser atualizados depois de criados, e eu quero reprocessar só o que mudou desde a última execução.
