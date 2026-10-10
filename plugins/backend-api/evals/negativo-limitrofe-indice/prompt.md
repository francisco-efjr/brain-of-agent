---
name: negativo-limitrofe-indice
description: Caso negativo limítrofe que mede sobredisparo, verificando que uma pergunta de índice PostgreSQL, vizinha mas fora do segmento, não aciona skills de tarefa do plugin e recebe resposta técnica direta, com no máximo um apontamento para o plugin de banco de dados.
tags: [backend-api, negative, database, boundary]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Recomenda índice composto com tenant_id primeiro e created_at em ordem descendente, explica pelo plano (Seq Scan e linhas removidas), cita criação sem bloqueio e custo de escrita, sugere reconferir com novo EXPLAIN ANALYZE, e não aciona skills de tarefa do plugin."
model: sonnet
---
Essa query do endpoint de auditoria está lenta (uns 2 segundos) e preciso criar um índice. Segue o EXPLAIN ANALYZE:

```sql
SELECT id, actor_id, action, created_at
FROM audit_logs
WHERE tenant_id = 312 AND created_at >= now() - interval '7 days'
ORDER BY created_at DESC
LIMIT 50;
```

```text
Limit  (actual time=2201.4..2201.4 rows=50 loops=1)
  ->  Sort  (Sort Key: created_at DESC, Sort Method: top-N heapsort  Memory: 34kB)
        ->  Seq Scan on audit_logs  (actual time=0.041..2150.8 rows=212340 loops=1)
              Filter: ((tenant_id = 312) AND (created_at >= (now() - '7 days'::interval)))
              Rows Removed by Filter: 17804112
Planning Time: 0.3 ms
Execution Time: 2201.9 ms
```

A tabela `audit_logs` tem uns 18 milhões de linhas, PostgreSQL 16, e hoje só existe o índice da chave primária. Qual índice devo criar?
