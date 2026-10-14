---
name: negativo-revisao-sql
description: "Caso negativo que mede sobredisparo: um pedido de revisão de query SQL com JOIN e GROUP BY não tem relação com validação funcional no navegador e não deve acionar nenhuma skill do plugin qa-playwright nem abrir o ciclo de inventário, exploração e matriz."
tags: [qa-playwright, negative, sql]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Revisa a query de verdade: aponta que o WHERE sobre a tabela da direita anula o LEFT JOIN e que o segundo JOIN multiplica linhas e infla COUNT e SUM, e sugere correção; não aciona skill do qa-playwright e não propõe inventário F-NN, exploração com Playwright nem matriz."
model: sonnet
---
Pode revisar essa query antes de eu colocar no relatório mensal? Ela deveria listar todos os clientes com a quantidade de pedidos pagos e a receita de cada um, do maior para o menor.

```sql
SELECT c.id, c.nome, COUNT(p.id) AS pedidos, SUM(p.total) AS receita
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
LEFT JOIN itens i ON i.pedido_id = p.id
WHERE p.status = 'pago'
GROUP BY c.id, c.nome
ORDER BY receita DESC;
```

Tabelas: `clientes(id, nome)`, `pedidos(id, cliente_id, total, status)`, `itens(id, pedido_id, produto_id, qtd)`. Banco: PostgreSQL 16.
