---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Recomenda um índice B-tree composto cujas colunas iniciais atendem ao filtro por igualdade e à ordenação (por exemplo `(tenant_id, created_at DESC)` ou variação equivalente), e relaciona a recomendação ao Seq Scan, às 18 milhões de linhas e às mais de 17 milhões de linhas removidas pelo filtro.
2. Menciona de forma curta o cuidado de produção na criação (por exemplo `CREATE INDEX CONCURRENTLY`) e o custo de escrita do novo índice, ou sugere confirmar o ganho com novo `EXPLAIN ANALYZE` depois de criar.
3. Responde diretamente, sem transformar a pergunta em revisão de contrato de API, ADR, plano de endpoint ou auditoria de segurança.
4. Se mencionar o plugin de modelagem de banco de dados, faz isso em uma frase, sem exigir que esteja instalado.
FAIL if qualquer um ocorrer: aciona skill de tarefa do plugin backend-api (api-contract-design, api-security-review, idempotency-and-resilience, api-test-suite, backend-debugging, agent-tool-design, stack-conventions); propõe trocar de banco, adicionar cache ou mudar a arquitetura para resolver uma consulta lenta; afirma ter executado a query ou criado o índice.
