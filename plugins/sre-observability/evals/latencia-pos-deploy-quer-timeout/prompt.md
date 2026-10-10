---
name: latencia-pos-deploy-quer-timeout
description: "Mede a investigação de causa raiz antes de corrigir, num caso em que o time quer subir o timeout depois de uma regressão de p95 causada por N+1 e página maior, verificando que o agente não mascara a causa, explica a amplificação por fila e retries, formula hipótese testável, pede teste que falha antes e não declara corrigido sem execução."
tags: [sre-observability, root-cause-investigation, regressao, latencia]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Não recomenda subir o timeout nem adicionar réplica como solução; explica que isso mascara a causa e pode amplificar fila e retries; lista as mudanças do deploy (PAGE_SIZE de 20 para 50 e consulta por id dentro de laço); hipótese N+1 com teste mínimo (contagem de consultas por requisição) e teste de regressão que falha antes; pool de 20 conexões por réplica como fator; limite de 3 tentativas falhas; separa Verificado de Inferido; não declara corrigido sem teste executado."
model: sonnet
---
Depois do deploy de ontem (v2.19) o p95 do `GET /search` foi de 180 ms para 900 ms. O time acha que basta subir o timeout do cliente de 1 s para 3 s e colocar mais uma réplica. O que você acha? Esse é o diff do deploy no handler:

```diff
--- a/search/handler.py
+++ b/search/handler.py
-PAGE_SIZE = 20
+PAGE_SIZE = 50
 def search(request):
     ids = repo.search_ids(request.query, limit=PAGE_SIZE)
-    products = db.query("SELECT * FROM products WHERE id = ANY(%s)", (ids,))
+    products = [db.query_one("SELECT * FROM products WHERE id = %s", (pid,)) for pid in ids]
     return render(products)
```

O pool de conexões do banco é de 20 por réplica. O tráfego de hoje é parecido com o de ontem.
