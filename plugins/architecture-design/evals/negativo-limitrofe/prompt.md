---
name: negativo-limitrofe
description: Caso negativo limítrofe que mede sobredisparo, verificando que uma pergunta de índice SQL, vizinha mas fora do segmento, não aciona nenhuma skill do plugin e recebe resposta técnica direta.
tags: [architecture-design, negative, database]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Responde a pergunta de índice com um índice composto adequado e explicação do plano, sem acionar skill do plugin e sem transformar a pergunta em ADR ou revisão de arquitetura."
model: sonnet
---
Essa query está lenta em produção (uns 4 segundos) e preciso criar um índice. Segue o EXPLAIN ANALYZE:

```sql
SELECT id, total_cents, created_at
FROM orders
WHERE customer_id = 8841 AND status = 'paid'
ORDER BY created_at DESC
LIMIT 20;
```

```text
Limit  (actual time=3980.112..3980.120 rows=20 loops=1)
  ->  Sort  (Sort Key: created_at DESC, Sort Method: top-N heapsort)
        ->  Seq Scan on orders  (actual time=0.031..3921.554 rows=1840 loops=1)
              Filter: ((customer_id = 8841) AND (status = 'paid'::text))
              Rows Removed by Filter: 9412330
Planning Time: 0.2 ms
Execution Time: 3980.2 ms
```

A tabela `orders` tem uns 9,4 milhões de linhas, PostgreSQL 15, e hoje só existe o índice da chave primária. Qual índice devo criar?
