---
name: metricas-cardinalidade
description: "Mede a revisão de instrumentação Prometheus, verificando alta cardinalidade e dado pessoal em rótulos, path com IDs, nome de métrica sem prefixo, unidade e sufixo, latência como medidor em milissegundos em vez de histograma em segundos, rate de medidor e a estimativa de séries com a conta."
tags: [sre-observability, telemetry-review, metricas, cardinalidade]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta user_id e email como alta cardinalidade e dado pessoal e path com IDs (usar o template da rota); nome requests sem prefixo, sem unidade e sem sufixo _total; latência deve ser histograma em segundos e não medidor em milissegundos; rate() de medidor é inválido; mostra a estimativa de séries com a conta (produto dos valores dos rótulos) e cita o guia de cardinalidade abaixo de 10; propõe correção mínima; não afirma ter executado o código."
model: sonnet
---
Revisa a instrumentação deste serviço Python (prometheus_client) antes de eu subir:

```python
import time
from prometheus_client import Counter, Gauge

REQS = Counter('requests', 'n de requisições', ['user_id', 'email', 'path'])
LAT = Gauge('latency_ms', 'latência da última requisição')

def handle(request):
    start = time.time()
    resp = process(request)
    REQS.labels(user_id=request.user.id, email=request.user.email, path=request.path).inc()
    LAT.set((time.time() - start) * 1000)
    return resp
```

O painel mostra a latência com `rate(latency_ms[5m])`. Temos uns 200 mil usuários ativos por mês e uns 3.000 paths distintos, muitos com ID na URL.
