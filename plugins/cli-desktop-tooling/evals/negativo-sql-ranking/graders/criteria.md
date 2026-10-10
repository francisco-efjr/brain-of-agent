---
type: llm
---

PASS if a resposta final traz uma query PostgreSQL correta para o pedido, agrupando por mês (por exemplo com date_trunc('month', criado_em)), somando valor por cliente e mês, e usando uma window function (ROW_NUMBER, RANK ou DENSE_RANK) com PARTITION BY mês e ORDER BY receita decrescente, filtrando posições até 10. A resposta é direta e não discute CLI, app desktop, assinatura, instaladores nem scripts de shell.
FAIL if a resposta ignora window functions, usa sintaxe que não existe no PostgreSQL, ou desvia para temas de CLI, desktop ou ferramentas de desenvolvedor.
