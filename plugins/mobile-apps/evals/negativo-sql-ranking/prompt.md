---
name: negativo-sql-ranking
description: Caso negativo distante que mede sobredisparo, verificando que um pedido de SQL com window function, fora do segmento mobile, não aciona nenhuma skill do plugin e recebe resposta técnica direta.
tags: [mobile-apps, negative, sql]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Responde com uma query PostgreSQL correta usando window function para ranking por região, com explicação curta de empates, sem acionar skill do plugin."
model: sonnet
---
Escreva uma query PostgreSQL com window function para ranking de vendas por região. A tabela é `vendas(id, regiao, vendedor_id, valor, vendido_em)` e quero, para cada região, os vendedores ordenados pelo total vendido no mês de setembro de 2026, com a posição de cada um.
