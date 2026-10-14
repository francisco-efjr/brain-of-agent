---
type: llm
---
PASS se todos os itens abaixo são observáveis na resposta final:
1. Revisa a query de fato e aponta que o `WHERE p.status = 'pago'` age sobre a tabela da direita do `LEFT JOIN` e elimina os clientes sem pedido pago (vira `INNER JOIN` na prática), contrariando o pedido de listar todos os clientes.
2. Aponta que o `LEFT JOIN itens` multiplica as linhas de `pedidos` (uma por item), o que infla `COUNT(p.id)` e `SUM(p.total)`; sugere remover o join com `itens` (a query não usa colunas dele) ou agregar antes, ou usar `COUNT(DISTINCT p.id)` com a ressalva de que o `SUM` continua inflado.
3. Propõe uma versão corrigida da query (por exemplo, mover o filtro de status para o `ON` do join e retirar `itens`) e, se quiser, trata `receita` nula dos clientes sem pedido (`COALESCE`).
4. Não abre ciclo de validação funcional: não propõe inventário de funcionalidades com IDs F-NN, exploração de app no navegador, specs Playwright, matriz de resultado nem relatório de rodada.
5. Resposta proporcional ao pedido: uma revisão de query, sem plano de testes de sistema.
FAIL se qualquer um ocorrer: elogia a query sem apontar o `WHERE` que anula o `LEFT JOIN` e a multiplicação de linhas pelo join com `itens`; conduz a conversa para Playwright, matriz ou ciclo de QA funcional; declara ter executado a query ou ter verificado resultado sem acesso ao banco.
