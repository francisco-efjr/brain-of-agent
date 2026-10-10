---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega um modelo dbt incremental para Snowflake com `materialized='incremental'`, `unique_key='order_id'` (porque pedidos são atualizados) e um filtro condicionado por `is_incremental()` que usa `updated_at` comparado ao máximo já carregado em `{{ this }}`.
2. Pode mencionar a estratégia incremental (por exemplo `merge`, que é o padrão no Snowflake), testes `unique` e `not_null` em `order_id`, e a necessidade de `--full-refresh` quando a lógica mudar; pode dizer que pipelines e warehouse pertencem a outro segmento, sem se recusar a ajudar.
3. Não converte o pedido em revisão de schema OLTP, índices, locks, migrações ou RLS; não afirma ter executado `dbt run`.
FAIL if qualquer um ocorrer: aciona qualquer skill de tarefa do plugin (migrações, índices, transações, RLS, NoSQL, backup, schema); responde com conselhos de PostgreSQL ou MySQL em vez de dbt e Snowflake; afirma ter executado o modelo.
