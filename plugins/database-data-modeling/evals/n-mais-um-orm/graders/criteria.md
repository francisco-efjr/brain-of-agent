---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica o padrão N+1: uma consulta para os pedidos, mais uma por pedido para `o.customer` e outra por pedido para `o.items.all()` (cerca de 401 consultas para 200 pedidos), como causa provável da lentidão, antes de falar de índice ou de plano.
2. Propõe a correção com carregamento antecipado do ORM: `select_related("customer")` para a FK e `prefetch_related("items")` para a relação reversa (ou equivalente com `Prefetch`), mostrando o código ajustado.
3. Pede a medição: contar as consultas por requisição antes e depois (por exemplo `assertNumQueries`, `django.db.connection.queries` ou um profiler de SQL) e, só se a lentidão persistir, o `EXPLAIN (ANALYZE, BUFFERS)` da consulta restante em réplica ou desenvolvimento; pode mencionar índice em `status`/`created_at` e em `OrderItem.order_id` como verificação posterior (a FK do Django cria índice por padrão).
4. Trata o ganho esperado como Suposição e não promete número; não afirma ter executado a view nem medido tempo.
FAIL if qualquer um ocorrer: propõe criar índices ou trocar de banco sem mencionar o N+1; promete ganho numérico sem medição; afirma ter medido ou executado; ignora o `prefetch_related` para a relação reversa.
