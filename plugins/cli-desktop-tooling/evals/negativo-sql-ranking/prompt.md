---
name: negativo-sql-ranking
description: Caso negativo. Pedido de SQL sem relação com CLI ou desktop. Nenhuma skill do plugin deve disparar e a resposta deve ser a query.
tags: [cli-desktop-tooling, negativo]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: Resposta direta com SQL PostgreSQL usando window functions, sem acionar skills do plugin.
model: sonnet
---

Escreve uma query SQL em PostgreSQL com window functions para ranquear os 10 clientes com maior receita em cada mês. A tabela é pedidos(id, cliente_id, valor, criado_em).
