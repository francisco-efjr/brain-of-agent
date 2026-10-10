---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Recomenda um índice B-tree composto cujas colunas iniciais atendem ao filtro e à ordenação (por exemplo `(customer_id, status, created_at DESC)` ou variação equivalente), e relaciona a recomendação ao Seq Scan, às 9,4 milhões de linhas e às mais de 9 milhões de linhas removidas pelo filtro.
2. Menciona, de forma curta, o cuidado de produção com a criação (por exemplo `CREATE INDEX CONCURRENTLY`) e o custo de escrita do novo índice, ou sugere confirmar o ganho com novo EXPLAIN ANALYZE depois de criar.
3. Responde diretamente, sem converter a pergunta em ADR, revisão de arquitetura, system design ou análise de fronteiras.
FAIL if qualquer um ocorrer: aciona qualquer skill ou agente do plugin architecture-design; propõe mudar de banco, cache ou arquitetura para resolver uma consulta lenta; afirma ter executado a query ou criado o índice.
