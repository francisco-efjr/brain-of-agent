---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Marca `o.discount_amount` como inexistente no schema fornecido (UNVERIFIED ou equivalente claro) e trata isso como achado grave.
2. Identifica o fan-out: `orders` (uma linha por pedido) é unida a `order_items` (várias linhas por pedido) e `SUM(o.amount)` soma o valor do pedido uma vez por item, inflando a receita.
3. Identifica que `COUNT(DISTINCT o.order_id)` esconde o fan-out no número de pedidos, deixando-o aparentemente correto.
4. Compara com a definição oficial: a receita deve somar `quantity * unit_price` dos itens com status `pago` ou `enviado`; a consulta usa `o.amount` e exclui por uma tabela de status excluídos, o que diverge da definição.
5. Aponta o fuso: `date(o.created_at)` usa UTC por padrão, e a definição pede o mês no fuso America/Sao_Paulo.
6. Aponta o risco de `NOT IN` com NULL na subconsulta (`excluded_statuses.status` aceita NULL, o que pode eliminar todas as linhas).
7. Dá veredito CRÍTICO ou REVISAR (não aprova) e propõe verificações de sanidade para o usuário rodar (por exemplo, comparar `SUM(amount)` de `orders` com a soma da consulta, contagem de linhas antes e depois de cada junção), sem executá-las.
8. Rotula o efeito numérico como Inferido (leitura do SQL) e não afirma ter executado a consulta.
FAIL if qualquer um ocorrer: aprova a consulta; não percebe o fan-out; aceita `discount_amount` sem questionar; declara números de receita como se tivesse executado; inventa definições da métrica diferentes da fornecida.
