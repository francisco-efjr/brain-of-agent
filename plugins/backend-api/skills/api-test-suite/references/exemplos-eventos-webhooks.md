# Testes de mensageria, eventos e webhooks

Origem: brain-of-agent, `brains/qa/references/automacao-api.md` (autor Francisco Edson / francisco-efjr, licença MIT; conteúdo próprio do usuário, incorporado e adaptado). Código de exemplo: confira as APIs das bibliotecas na versão instalada no projeto (as versões não foram reverificadas nesta cadeia: **Inferido**). Exemplos nunca devem rodar contra produção; credenciais entram por variável de ambiente.

Para Kafka, RabbitMQ, SQS e receptores de webhook. Combine com `idempotency-and-resilience` (desenho do consumidor idempotente, DLQ, outbox, HMAC). Fatos de brokers (ordem, janela de deduplicação do SQS FIFO) vêm do brain e não foram reverificados: **Inferido**; o modo `BACKWARD` padrão do Confluent foi Verificado em 2026-10-10.

## Sumário

- Mensageria e eventos
- Webhooks

## Mensageria e eventos

Kafka, RabbitMQ e SQS entregam **pelo menos uma vez**: duplicidade é normal e
o consumidor precisa ser idempotente.

- **Produtor:** publica no destino certo, com chave, headers e schema
  corretos, **uma vez**, e só depois do commit no banco — sem padrão outbox,
  falha entre gravar e publicar perde ou duplica evento (injete essa falha). No
  teste, consuma desde o início (`auto.offset.reset=earliest`, grupo exclusivo)
  e filtre pelo ID criado; com `latest`, a mensagem publicada antes da
  atribuição de partições se perde e o teste fica intermitente.
- **Consumidor:** efeito correto; mesma mensagem duas vezes → um efeito;
  mensagem envenenada vai para a DLQ após N tentativas com o motivo registrado,
  **e as seguintes continuam sendo processadas**.
- **Ordem:** Kafka garante ordem só dentro da partição (mesma chave); SQS
  Standard não garante (FIFO garante por `MessageGroupId` e deduplica em
  janela de 5 minutos); RabbitMQ perde ordem com vários consumidores ou
  reenfileiramento. Teste `pedido.cancelado` chegando antes de `pedido.pago`.
- **Schema registry:** verifique no CI, antes do deploy, a compatibilidade do
  schema novo com o registrado (no Confluent o modo padrão é `BACKWARD`: o
  schema novo lê dados gravados com o anterior).
- **Consistência eventual:** espere pela condição com polling e prazo máximo,
  nunca com `sleep` fixo — curto falha no CI lento, longo desperdiça minutos.

```python
import time


def esperar_ate(condicao, timeout=15.0, intervalo=0.2, descricao="condição"):
    limite = time.monotonic() + timeout
    while not (resultado := condicao()):
        if time.monotonic() >= limite:
            raise AssertionError(f"{descricao} não ocorreu em {timeout} s")
        time.sleep(intervalo)  # intervalo de polling, não espera fixa pelo resultado
    return resultado

# uso: esperar_ate(lambda: repo.buscar(pedido_id).status == "PAGO", descricao="pedido pago")
```

Java: Awaitility, `await().atMost(Duration.ofSeconds(15)).untilAsserted(() ->
assertThat(repo.status(id)).isEqualTo("PAGO"))`. Vitest: `vi.waitFor(fn, {
timeout: 15_000 })`. Playwright: `expect.poll(fn, { timeout: 15_000 })`.
Provar que algo **não** aconteceu exige um marco: espere um evento posterior
processado pelo mesmo consumidor e então confira a ausência.

## Webhooks

- **Assinatura HMAC** sobre o **corpo cru** (bytes recebidos), com timestamp
  dentro do conteúdo assinado e comparação em tempo constante
  (`hmac.compare_digest`). Reserializar o JSON antes de verificar muda os bytes.
- **Casos:** assinatura válida → 2xx; um byte alterado → 401 e nada
  processado; timestamp fora da tolerância (ex.: 5 min) → recusado (replay);
  mesmo ID de evento duas vezes → um efeito; na rotação de segredo, o antigo só
  vale na janela combinada.
- **Retries e ordem:** o emissor reenvia em timeout ou 5xx; responda 2xx
  rápido e processe de forma assíncrona. Eventos chegam fora de ordem: use a
  versão ou o timestamp do evento, ou consulte o estado atual no emissor.

```python
import hashlib, hmac, json, time


def assinar(segredo: bytes, corpo: bytes, ts: int) -> str:
    return hmac.new(segredo, f"{ts}.".encode() + corpo, hashlib.sha256).hexdigest()


corpo, ts = json.dumps({"id": "evt_teste_1", "tipo": "pagamento.aprovado"}).encode(), int(time.time())
r = api.post("/webhooks/pagamentos", content=corpo, headers={"Content-Type": "application/json",
             "X-Timestamp": str(ts), "X-Assinatura": assinar(SEGREDO_DE_TESTE, corpo, ts)})
```

Cabeçalhos e conteúdo assinado variam por provedor; reproduza o do provedor
real. Muitos têm CLI para disparar eventos de teste (ex.:
`stripe trigger payment_intent.succeeded`).
