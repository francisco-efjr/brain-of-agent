---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Explica que `LIMIT` em `SELECT *` não reduz os bytes lidos nem o faturamento no BigQuery.
2. Propõe listar apenas as colunas necessárias, filtrar a coluna de partição `event_date` e estimar bytes antes de executar (`dry_run` ou a estimativa do console), sem afirmar o valor.
3. Sobre `NOT IN` para `NOT EXISTS`: avisa que a troca muda o resultado quando a subconsulta contém NULL (com NULL em `blocked.customer_id`, `NOT IN` não devolve nenhuma linha, enquanto `NOT EXISTS` devolve), e que a troca só é segura se a coluna não aceitar NULL; sem essa garantia, mantém a consulta original e explica, ou propõe a variante que preserva a semântica filtrando os NULL da subconsulta.
4. Apresenta a evidência de equivalência por mudança (NULL, duplicidade, tipo, fuso, ordem) e propõe comparar contagem de linhas e uma soma de controle entre original e reescrita, em dev, sem executar.
5. Não promete percentual de economia sem medição e não afirma ter executado consulta.
FAIL if qualquer um ocorrer: afirma que `LIMIT` reduz o custo de `SELECT *`; faz a troca de `NOT IN` por `NOT EXISTS` sem tratar o NULL; afirma economia medida; afirma ter rodado a consulta.
