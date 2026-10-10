# Exemplos: revisão de métricas e teste de redação de logs

Rótulos: Verificado = visto no material colado; Inferido = conhecimento estável do domínio, conferir na versão da biblioteca; Suposição = valores estimados.

## 1. Antes e depois de uma métrica (caso do eval `metricas-cardinalidade`)

Código recebido (fictício):

```python
from prometheus_client import Counter, Gauge
REQS = Counter('requests', 'n', ['user_id', 'email', 'path'])
LAT = Gauge('latency_ms', 'latencia')
# ... a cada request: REQS.labels(uid, email, request.path).inc(); LAT.set(elapsed_ms)
# consulta no painel: rate(latency_ms[5m])
```

| ID | Severidade | Evidência | Por quê | Correção mínima |
| --- | --- | --- | --- | --- |
| TL-01 | blocker | `labelnames=['user_id','email',...]` | Alta cardinalidade e dado pessoal; e-mail em backend de métricas | Remover `user_id` e `email` dos rótulos; o identificador interno pode ir a log ou trace estruturado; o e-mail sai da telemetria (se for indispensável, só pseudonimizado e com base legal definida pelo time) |
| TL-02 | major | rótulo `path` com `request.path` | URL com ID cria uma série por recurso | Usar a rota normalizada (`/pedidos/{id}`) como `route` |
| TL-03 | major | nome `requests` | Sem prefixo de aplicação; contador deve terminar em `_total` | `checkout_http_requests_total` (nesta biblioteca o sufixo `_total` é acrescentado na exposição; Inferido) |
| TL-04 | major | `Gauge('latency_ms')` com `.set()` | Medidor guarda só o último valor; unidade fora do padrão (milissegundos) | Histograma `checkout_http_request_duration_seconds` com buckets em torno do SLO |
| TL-05 | major | `rate(latency_ms[5m])` | `rate()` de medidor não faz sentido | `histogram_quantile(0.95, sum by (le, route) (rate(checkout_http_request_duration_seconds_bucket[5m])))` |

Correção proposta (rascunho não executado):

```python
from prometheus_client import Counter, Histogram
REQS = Counter('checkout_http_requests', 'Requisições HTTP', ['method', 'route', 'status'])
LAT = Histogram('checkout_http_request_duration_seconds', 'Latência', ['route'],
                buckets=(0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2))
# status em classes ("2xx", "5xx") se a cardinalidade de códigos for alta
```

## 2. Estimativa de séries (mostrar a conta)

Premissas fornecidas pelo usuário (Suposição se vierem de memória): 20 mil usuários ativos por mês, 40 rotas, 4 métodos úteis.

```text
Antes:  user_id (20.000) x path (distinto por ID, >> 40) -> acima de 800.000 séries só no contador
        (email é 1:1 com user_id: não multiplica, mas replica o problema e expõe dado pessoal)
Depois: method (4) x route (40) x status (3 classes)     -> 480 séries no contador
        histograma: route (40) x (7 buckets + Inf + _sum + _count = 10) -> 400 séries
```

Mostre sempre a premissa. Guia do Prometheus: abaixo de ~10 valores por rótulo e reavaliar métricas com mais de 100 séries; 480 séries passam do guia, então decida se `method` e `status` precisam mesmo ser rótulos juntos.

## 3. Teste de redação de logs (rascunho em Python/pytest)

Princípios: lista de campos proibidos num só lugar; o teste compara a lista da política com a do código e prova que valores falsos não saem. Os valores são obviamente falsos (não use formatos de chave real).

```python
# logging_redact.py
import json

FORBIDDEN = {"password", "token", "authorization", "cookie", "set-cookie",
             "apikey", "api_key", "email", "phone", "cpf"}

def redact(obj):
    if isinstance(obj, dict):
        return {k: "[REDACTED]" if k.lower() in FORBIDDEN else redact(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    return obj

def emit(event: dict) -> str:
    return json.dumps(redact(event))
```

```python
# test_logging_redact.py
import json
from logging_redact import FORBIDDEN, emit

POLICY = {"password", "token", "authorization", "cookie", "set-cookie",
          "apikey", "api_key", "email", "phone", "cpf"}   # espelha a política de logging do time

def test_codigo_cobre_toda_a_politica():
    assert POLICY <= FORBIDDEN, f"faltam no código: {sorted(POLICY - FORBIDDEN)}"

def test_valores_falsos_nao_saem():
    event = {"Authorization": "FAKE-SECRET-0001", "user": {"Email": "fake@example.test"},
             "headers": [{"Cookie": "FAKE-SECRET-0002"}], "msg": "ok", "request_id": "r-1"}
    line = emit(event)
    for fake in ("FAKE-SECRET-0001", "fake@example.test", "FAKE-SECRET-0002"):
        assert fake not in line
    assert json.loads(line)["request_id"] == "r-1"
```

Limites declaráveis: o teste prova a redação por chave; não detecta segredo dentro de texto livre (`msg`). Se houver mensagens livres com dado, peça um segundo teste (scanner de padrões) e marque o risco residual. Rode com `pytest -q` e cole a saída real; sem execução, o rótulo é **rascunho não executado**.

## 4. Health check por dependência (padrão)

```text
GET /health/ready  -> consulta cada dependência crítica com timeout curto (exemplo da fonte: 800 ms),
                      responde 503 com o nome da dependência que falhou
GET /health/live   -> só prova que o processo responde (sem consultar dependência)
```

Readiness igual a liveness reinicia containers saudáveis quando o banco oscila (falha frequente do brain `entrega-e-operacao`). O valor de 800 ms é do exemplo-fonte; derive do SLO.
