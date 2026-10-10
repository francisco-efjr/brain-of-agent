---
name: negativo-sql-ranking
description: Caso negativo distante. Pedido de SQL sem relação com jogos; mede se nenhuma skill do plugin game-development dispara, nenhuma referência do playbook é lida e a resposta é uma query PostgreSQL correta sobre ranking com window function.
tags: [game-development, negative, no-trigger, sql]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Responde diretamente com uma query PostgreSQL de ranking de vendas por região usando window function (RANK, DENSE_RANK ou ROW_NUMBER com PARTITION BY região), sem acionar skills do plugin e sem ler referências do playbook."
model: sonnet
---
Escreva uma query PostgreSQL com window function para ranking de vendas por região. Tenho a tabela `vendas(id, regiao, vendedor, valor, data_venda)` e quero o top 3 vendedores de cada região no último trimestre.
