---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Recomenda um índice composto coerente com a query: colunas de igualdade primeiro (`cliente_id`, `status`) e a coluna de ordenação (`criado_em`, preferencialmente `DESC`) por último, ou uma variante justificada (índice parcial `WHERE status = 'pago'`, `INCLUDE` de colunas para varredura só de índice).
2. Explica como confirmar o uso do índice com `EXPLAIN (ANALYZE, BUFFERS)` e o que procurar no plano (Index Scan/Index Only Scan, ausência de Sort e Seq Scan).
3. Menciona `CREATE INDEX CONCURRENTLY` (ou o custo de bloqueio de escrita do `CREATE INDEX` comum) e o custo de escrita/espaço do índice.
4. Resposta direta e proporcional, sem tratar o pedido como tema de design, UI, Figma ou motion.
FAIL if qualquer um ocorrer: aciona qualquer skill ou agente do kit de design engineering; recomenda índice incoerente (por exemplo `criado_em` primeiro); inventa números de desempenho; transforma a pergunta em auditoria.
