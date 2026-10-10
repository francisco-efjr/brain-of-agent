---
name: negativo-backend-indice-sql
description: "Caso negativo de sobredisparo: pergunta de backend sobre índice composto no PostgreSQL para uma query lenta de pedidos não deve acionar nenhuma skill do kit de design engineering e deve receber resposta técnica direta."
tags: [design-engineering-kit, negative, backend, postgresql]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Recomenda índice composto adequado à query (igualdade em cliente_id e status, ordenação por criado_em), sugere EXPLAIN ANALYZE e criação sem bloqueio, não aciona nenhuma skill do kit e não transforma a pergunta em assunto de design."
model: sonnet
---
Tenho a tabela `pedidos (id, cliente_id, status, criado_em, total)` com uns 20 milhões de linhas no PostgreSQL. Esta query está lenta:

```sql
SELECT id, total, criado_em
FROM pedidos
WHERE cliente_id = $1 AND status = 'pago'
ORDER BY criado_em DESC
LIMIT 20;
```

Qual índice eu crio? E como confirmo que ele está sendo usado?
