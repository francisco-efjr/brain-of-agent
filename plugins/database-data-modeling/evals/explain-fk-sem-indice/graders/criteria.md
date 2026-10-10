---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta, com base no plano colado, que o `Seq Scan on order_items` lê a tabela inteira (cerca de 2,4 milhões de linhas removidas pelo filtro) para devolver 3 linhas, e liga isso à ausência de índice em `order_items.order_id` (coluna de FK sem índice; o PostgreSQL não cria índice automático no lado filho).
2. Nota a divergência entre linhas estimadas (1200) e reais (3) e sugere `ANALYZE order_items` (e novo plano) como complemento ou verificação, sem condicionar o índice a isso.
3. Propõe `CREATE INDEX CONCURRENTLY` em `order_items (order_id)`, avisando que não roda dentro de transação e que convém checar índice `INVALID` se falhar, e menciona o custo de escrita do novo índice.
4. Pede novo `EXPLAIN (ANALYZE, BUFFERS)` com o mesmo volume para registrar antes e depois e trata o ganho esperado como Suposição.
5. Não promete ganho numérico específico (como "100x" ou um tempo exato) e não afirma ter executado a consulta ou criado o índice.
FAIL if qualquer um ocorrer: promete ganho numérico sem medição; propõe índice sem olhar o plano; ignora o Seq Scan ou a divergência de estimativa; manda `CREATE INDEX` comum (sem `CONCURRENTLY`) em tabela grande com escrita contínua sem avisar do bloqueio; afirma ter rodado o comando; propõe trocar de banco ou arquitetura.
