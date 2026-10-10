# Webhooks, retries, filas, jobs, rate limit e cache

Fontes: brain-of-agent `automacao-api` (Webhooks, Mensageria) e `backend-e-contratos` (MIT, incorporado e adaptado); OWASP API Security Top 10 2023, item sobre webhooks sem assinatura = CRITICAL em V-24 (AP4); V-33 (rate limit); V-17 e V-18 (retry, timeouts); V-35 (operações longas). **Filas, outbox, backoff com jitter e cache de aplicação não têm fonte primária validada nesta cadeia (lacunas registradas em `fontes.md` do playbook): o que não vem do brain é conhecimento estável do domínio e está rotulado Inferido.** Confira a documentação do seu broker/biblioteca na versão instalada.

## Sumário

1. Receptor de webhook
2. Emissor de webhook
3. Retries, timeouts e backoff
4. Filas e jobs: consumidor idempotente e DLQ
5. Outbox
6. Ordem e consistência eventual
7. Rate limiting
8. Cache de aplicação
9. Testes

## 1. Receptor de webhook

Regras (brain, V-24):

- **HMAC sobre o corpo cru** (bytes recebidos). Reserializar o JSON antes de verificar muda os bytes e invalida a assinatura.
- Timestamp **dentro do conteúdo assinado**, com tolerância (ex.: 5 min) contra replay.
- Comparação em tempo constante (`hmac.compare_digest`, `crypto.timingSafeEqual`).
- Dedupe **persistente** por ID de evento (a mesma entrega pode chegar mais de uma vez).
- Responder 2xx rápido e processar de forma assíncrona; o emissor reenvia em timeout ou 5xx.
- Ordem não garantida: use versão/timestamp do evento ou consulte o estado atual no emissor; trate estado terminal.
- Rotação de segredo: aceitar o atual e o anterior só durante a janela combinada.
- Cabeçalhos e conteúdo assinado variam por provedor: reproduza o esquema do provedor real (o exemplo abaixo é genérico).

```python
import hashlib
import hmac
import json
import time

from fastapi import FastAPI, HTTPException, Request

app = FastAPI()
TOLERANCIA_S = 300

def assinatura_valida(segredos: list[bytes], corpo: bytes, ts_header: str, recebida: str) -> bool:
    try:
        ts = int(ts_header)
    except ValueError:
        return False
    if abs(time.time() - ts) > TOLERANCIA_S:
        return False
    for segredo in segredos:                       # atual e, na rotação, o anterior
        esperada = hmac.new(segredo, f"{ts}.".encode() + corpo, hashlib.sha256).hexdigest()
        if hmac.compare_digest(esperada, recebida):
            return True
    return False

@app.post("/webhooks/pagamentos", status_code=202)
async def receber(request: Request):
    corpo = await request.body()                   # bytes crus, antes de qualquer parse
    if not assinatura_valida(SEGREDOS, corpo,
                             request.headers.get("x-timestamp", ""),
                             request.headers.get("x-assinatura", "")):
        raise HTTPException(status_code=401)       # use o handler RFC 9457 do projeto
    evento = json.loads(corpo)
    if registrar_evento_unico(evento["id"]):       # INSERT ... ON CONFLICT DO NOTHING (ver seção 4)
        enfileirar(evento)                         # processamento fora da requisição
    return {}                                      # duplicata também recebe 2xx
```

Express: use `express.raw({ type: 'application/json' })` **nessa rota** para obter o `Buffer`; calcule `crypto.createHmac('sha256', segredo).update(`${ts}.`).update(corpoCru).digest()` e compare com `crypto.timingSafeEqual`, conferindo antes que os dois buffers têm o mesmo tamanho (a função lança erro se diferirem). Um `express.json()` global antes da rota destrói o corpo cru.

## 2. Emissor de webhook

Assine o corpo exato enviado, inclua ID de evento estável e timestamp, trate 2xx como entregue, retente com backoff e limite (seção 3), exponha reenvio manual e rotação de segredo. Documente a ordem como **não garantida**. Teste recebendo seu próprio webhook em ambiente de teste, nunca contra o endpoint de produção de um cliente.

## 3. Retries, timeouts e backoff

Do brain (`backend-e-contratos`):

- **Orçamento de timeout por salto.** Se o usuário espera no máximo 5 s, dê a cada dependência uma fração, não 5 s para cada uma em sequência.
- Limite o número de tentativas; aplique backoff com jitter quando justificável; não repita erro permanente; respeite `Retry-After` e a orientação do fornecedor.
- Circuit breaker limita tentativas durante a falha; **não repara** inconsistência já criada.
- Retry automático só é seguro depois de entender a semântica e garantir idempotência: aceitação desconhecida (timeout depois de enviar) é o caso perigoso.

| Resultado | Repetir? |
| --- | --- |
| Erro de conexão, timeout | sim, se a operação for idempotente ou tiver chave |
| 429 | sim, esperando `Retry-After` quando houver |
| 502, 503, 504 | sim, com backoff |
| 500 | depende; se idempotente, com limite baixo |
| 400, 401, 403, 404, 422 | não (permanente até o chamador mudar algo) |
| 409 | não repetir às cegas; leia o motivo (conflito de estado) |
| gRPC `UNAVAILABLE` | pode repetir com backoff (V-17) |
| gRPC `ABORTED` | repetir em nível superior (ler-modificar-gravar de novo) |
| gRPC `FAILED_PRECONDITION` | não repetir até o estado mudar |

Backoff exponencial com jitter completo (técnica conhecida como *full jitter*; Inferido):

```python
import random

def espera_s(tentativa: int, base: float = 0.2, teto: float = 10.0) -> float:
    """Sorteia entre 0 e min(teto, base * 2**tentativa): espalha retries simultâneos."""
    return random.uniform(0.0, min(teto, base * (2 ** tentativa)))
```

gRPC: toda chamada tem deadline; o servidor propaga o prazo restante às chamadas que faz; o cliente não sabe se a operação completou depois de `DEADLINE_EXCEEDED`, então operação com efeito precisa ser idempotente (brain).

Go: `http.Client` sempre com `Timeout`, `defer resp.Body.Close()` após checar o erro, `http.NewRequestWithContext` propagando o contexto da requisição (V-18).

## 4. Filas e jobs: consumidor idempotente e DLQ

Kafka, RabbitMQ e SQS entregam **pelo menos uma vez** (brain; Inferido para o broker específico): duplicidade é normal.

```sql
CREATE TABLE processed_events (
  consumer     text        NOT NULL,
  event_id     text        NOT NULL,
  processed_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (consumer, event_id)
);
```

```python
def processar(conn, consumidor: str, evento: dict):
    with conn.transaction():                       # efeito e marca na MESMA transação
        novo = conn.execute(
            "INSERT INTO processed_events (consumer, event_id) VALUES (%s, %s) "
            "ON CONFLICT DO NOTHING RETURNING 1", (consumidor, evento["id"])).fetchone()
        if not novo:
            return                                 # duplicata: nenhum efeito
        aplicar_efeito(conn, evento)               # se lançar, a marca também é desfeita
```

- **Mensagem envenenada**: após `N` tentativas vai para a **DLQ** com o motivo registrado (exceção, tentativa, ID); as mensagens seguintes **continuam sendo processadas** (a DLQ não pode bloquear o fluxo). Alerta e rotina de reprocessamento fazem parte do desenho.
- **Job** reexecutado (crash, deploy, retry do agendador): a mesma garantia de idempotência por ID do job/lote; evite jobs que "recomeçam do zero" com efeito externo.
- **Aceitar não é concluir**: o endpoint que enfileira responde 202 com URL de monitoramento (V-35), não 201 do resultado.
- Schema registry: verifique no CI a compatibilidade do schema novo com o registrado; no Confluent o modo padrão é `BACKWARD` (Verificado em 2026-10-10 na doc da Confluent; confira o modo configurado).

## 5. Outbox

Problema: gravar no banco e publicar no broker são duas ações; falha entre elas perde ou duplica evento (brain). Solução: grave o evento numa tabela `outbox` **na mesma transação** do efeito e publique depois do commit por um relay.

```sql
CREATE TABLE outbox (
  id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  aggregate_id text        NOT NULL,
  type         text        NOT NULL,
  payload      jsonb       NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now(),
  published_at timestamptz
);
-- na transação do efeito:  INSERT INTO outbox (aggregate_id, type, payload) VALUES (...);
-- relay (laço periódico):
--   SELECT id, type, payload FROM outbox WHERE published_at IS NULL
--     ORDER BY id LIMIT 100 FOR UPDATE SKIP LOCKED;
--   publicar no broker; depois:  UPDATE outbox SET published_at = now() WHERE id = ANY(:ids);
```

O relay pode publicar e cair antes do `UPDATE`: publica de novo. Por isso o consumidor é idempotente (seção 4). Ordem estrita por agregado exige uma chave de partição por `aggregate_id`. DDL proposto, a executar apenas em banco de teste.

## 6. Ordem e consistência eventual

- Kafka garante ordem só dentro da partição (mesma chave); SQS Standard não garante ordem (FIFO garante por `MessageGroupId` e deduplica em janela de 5 minutos); RabbitMQ perde ordem com vários consumidores ou reenfileiramento (brain; Inferido).
- Teste `pedido.cancelado` chegando antes de `pedido.pago`.
- Em testes, espere a condição com polling e prazo, nunca `sleep` fixo (ver `api-test-suite`).

## 7. Rate limiting

Regras (V-33, Classe B; o blog usado é Classe C, tratar como heurística):

- A chave do limite vem de **credencial validada** (identidade + plano + endpoint), nunca de header livre como `x-api-key` não verificado (burlável).
- 429 com corpo padronizado (RFC 9457) e `Retry-After`; limite por cliente, não global.
- Janela deslizante (ou *token bucket*) em armazenamento compartilhado; janela fixa permite rajada de até 2x na virada (Inferido).
- Política de falha do armazenamento por rota: aberta em formulário de contato, fechada em login e pagamento.
- Cabeçalhos `RateLimit-Policy` (quota `q`, unidades `qu`, janela `w`, partição `pk`) e `RateLimit` (restante `r`, tempo `t`, `pk`) vêm de um **draft** (rev. 11, 23/05/2026, expira em 24/11/2026): use só se o projeto aceitar draft e marque na spec.

```python
import time

def permitir(redis, chave: str, limite: int, janela_s: int) -> tuple[bool, int]:
    """Janela fixa simples. Devolve (permitido, segundos até renovar)."""
    bucket = int(time.time()) // janela_s
    k = f"rl:{chave}:{bucket}"
    pipe = redis.pipeline(transaction=True)        # INCR + EXPIRE juntos
    pipe.incr(k)
    pipe.expire(k, janela_s)
    n, _ = pipe.execute()
    return n <= limite, janela_s - (int(time.time()) % janela_s)
```

Resposta ao exceder: `429`, `Retry-After: <segundos>`, `Content-Type: application/problem+json`, `type` documentado. Teste: exceder, ver 429, esperar o `Retry-After`, ver a requisição passar. Só em ambiente isolado; nunca gere carga contra ambiente compartilhado.

## 8. Cache de aplicação (Inferido; sem fonte V, só HTTP caching tem fonte: V-36)

- Padrão *cache-aside*: ler do cache; em falha, ler da origem e gravar com TTL. Defina o TTL pelo custo de dado velho, não por padrão.
- **Chave com escopo de usuário/tenant** quando a resposta depende dele; chave sem tenant vaza dado entre clientes.
- Invalidação na escrita (apagar ou atualizar a chave no mesmo fluxo); aceitar janela de inconsistência declarada.
- Proteção contra *stampede*: bloqueio de carga única por chave, TTL com jitter, ou servir velho enquanto revalida.
- Não cache decisões de autorização por mais tempo que a vida do token/permissão.
- Cache HTTP: `Cache-Control: private` para dado por usuário, `no-store` para sensível, ETag + `If-None-Match` para revalidar (RFC 9111, V-36, Verificado em resumo de seções).

## 9. Testes

| Cenário | Esperado |
| --- | --- |
| assinatura válida | 2xx, efeito uma vez |
| 1 byte do corpo alterado | 401, nada processado |
| timestamp fora da tolerância | recusado |
| mesmo `event_id` duas vezes | um efeito |
| segredo anterior dentro/fora da janela de rotação | aceito/recusado |
| `pedido.cancelado` antes de `pedido.pago` | estado final correto |
| mensagem envenenada | vai à DLQ com motivo; as seguintes são processadas |
| falha entre commit e publicação (outbox) | evento publicado uma vez ou mais; efeito uma vez |
| 429 e recuperação | `Retry-After` presente; volta a passar |
| fornecedor lento | falha dentro do orçamento de timeout; sem retry de erro permanente |
