# Idempotência e webhooks de pagamento

Base: V-01, V-02, V-03, V-04, V-05, V-37, V-43, V-44, V-47, V-50, V-51, V-53, V-54, V-57, V-58, V-66, V-67, V-68 e o capítulo "Microsserviços e eventos" do brain-of-agent (MIT). Valores de provedor datados de 2026-10-10: confirme na documentação vigente antes de codificar. Redação própria; nenhum trecho literal de terceiros.

## Sumário

1. Contrato de idempotência
2. Tabela de retry
3. Quatro desfechos e reserva atômica
4. Fingerprint, retenção e tombstone
5. Matriz de chave de idempotência por provedor
6. Idempotência no Pix
7. Webhook: modelo mental e handler de 7 passos
8. Inbox imutável, digest e quarentena
9. Matriz de autenticação de webhook por provedor
10. Provedor sem assinatura documentada (regra V-50)
11. Retentativas, retenção e pausa de fila por provedor
12. Outbox, DLQ, backoff e jitter
13. Roteiro de testes hostis
14. Gotchas

## 1. Contrato de idempotência

- **A chave identifica a intenção de negócio, não a tentativa.** Gere uma vez (UUID v4 ou string com entropia, sem dado pessoal), persista **antes** da chamada externa e reuse em todo retry. Limites: Stripe até 255 caracteres, Adyen até 64 (V-01, Verificado).
- **Mesma chave com corpo diferente é erro** e deve ser registrada, nunca aceita em silêncio.
- **GET e DELETE não levam chave** (V-01).
- **Idempotência do provedor não substitui a do seu sistema.** O provedor protege a chamada; você precisa evitar a segunda cobrança também na sua base (constraint de unicidade) e no seu ledger.
- **Exactly-once entre sistemas não existe**: o alvo é efeito único com entrega repetida (ao menos uma vez + idempotência). Prometer exactly-once é item da lista de rejeição (`padroes-e-antipadroes.md`).
- Idempotência é **sempre explícita** em endpoint de dinheiro: o Clean-Backend removeu a regra de seus prompts porque o modelo a aplicava sempre, mas registra que em modelo menor ela faltou de forma insegura (V-28). Por isso o inventário de mutações é o primeiro passo da skill `payment-idempotency`.

## 2. Tabela de retry

| Situação | Ação | Fonte |
| --- | --- | --- |
| Timeout ou conexão cortada | Mesma chave, mesmo corpo, backoff exponencial com jitter; se o estado ficar `indeterminate`, consultar o provedor antes de insistir | V-01, V-12 |
| Duplicata concorrente (original em andamento) | Retentar só se o provedor sinalizar erro transitório (Adyen: `transient-error: true`; ausente ou `false` não retenta). Convenção interna do rascunho IETF: 409 em andamento | V-01, V-58 |
| Mesma chave, corpo diferente | Não retentar; registrar conflito (rascunho IETF: 422; Stripe v1 devolve erro de parâmetros diferentes) | V-01, V-58 |
| Falha de validação ou conflito de concorrência no Stripe | Não são salvos; é seguro corrigir e repetir | V-01 |
| 5xx depois de a execução começar (Stripe v1) | O resultado, inclusive 500, fica salvo para a chave; repetir devolve o mesmo resultado | V-01 |
| Armazém de idempotência do provedor fora (Adyen 503 com código 703) | Pausar e tentar de novo, ou enviar sem a chave perdendo a proteção — a segunda opção só com confirmação humana | V-01 |
| Erro 4xx de negócio (cartão recusado, saldo insuficiente) | Falha final: não retentar com a mesma chave; nova tentativa de negócio é nova intenção com nova chave | V-02 (Inferido) |

## 3. Quatro desfechos e reserva atômica

Estados (V-02): `started` (reservada, chamada em curso), `succeeded`, `failed_final` (falha anterior à execução ou erro definitivo) e `indeterminate` (timeout ou resposta perdida; resolve consultando o provedor, nunca com chave nova).

Esquema ilustrativo em PostgreSQL (design do plugin, **Inferido** a partir de V-02; adapte ao seu SGBD e confira o dialeto):

```sql
CREATE TABLE idempotency_keys (
  scope        text        NOT NULL,  -- conta/tenant + operação, ex.: 'acct_42:charge'
  key          text        NOT NULL,
  fingerprint  text        NOT NULL,  -- hash canônico versionado do corpo
  state        text        NOT NULL CHECK (state IN ('started','succeeded','failed_final','indeterminate')),
  provider_ref text,                  -- id devolvido pelo provedor (persistir sempre)
  response     jsonb,                 -- resposta a reexibir (sem dado sensível)
  created_at   timestamptz NOT NULL DEFAULT now(),
  expires_at   timestamptz NOT NULL,
  PRIMARY KEY (scope, key)
);
-- Reserva atômica: quem inserir primeiro executa; os demais leem.
INSERT INTO idempotency_keys (scope, key, fingerprint, state, expires_at)
VALUES ($1, $2, $3, 'started', now() + interval '14 days')
ON CONFLICT (scope, key) DO NOTHING
RETURNING 1;
```

Decisão após o `INSERT`: se retornou linha, esta requisição é a dona e pode chamar o provedor; se não, leia a linha existente e aplique: `fingerprint` diferente → conflito; `started` → em andamento (409 ou espera); `succeeded` → devolva `response`; `indeterminate` → consulte o provedor pela referência; `failed_final` → devolva o erro salvo. **Nunca** "SELECT, depois INSERT" sem constraint (corrida).

Fluxo com efeito externo: persistir intenção e chave, **commit**, chamar o provedor (sem lock de banco aberto), persistir resultado e o id do provedor, emitir efeitos de saída por outbox. Lease com fencing token se houver reprocessamento por worker.

## 4. Fingerprint, retenção e tombstone

- **Fingerprint canônico versionado**: serialização determinística (chaves ordenadas, números normalizados, sem campos voláteis como timestamp de cliente) + versão do algoritmo no hash. Mudar o algoritmo sem versão faz toda retentativa legítima parecer conflito.
- **Retenção própria ≥ janela de retry do cliente e ≥ retenção do provedor em uso** (reter menos é item da lista de rejeição). Guarde a retenção **por provedor**: Stripe poda chaves após no mínimo 24 h; Adyen valida 7 a 14 dias (V-01, K1). Não existe janela universal.
- **Tombstone**: depois da expiração, mantenha identidade mínima (scope, key, fingerprint, provider_ref) para que a expiração não apague a identidade da operação (V-02).
- **Reexibir resposta sensível** exige reautorização; não grave PAN, token ou PII em `response`.

## 5. Matriz de chave de idempotência por provedor (V-68, datada de 2026-10-10)

| Provedor | Cabeçalho | Obrigatório | Retenção | Corpo diferente, mesma chave | Status |
| --- | --- | --- | --- | --- | --- |
| Stripe | `Idempotency-Key` | não informado | podada após pelo menos 24 h | erro de parâmetros | Verificado |
| Adyen | `idempotency-key` | não informado | 7 a 14 dias | duplicata em andamento: 422 ou 409, código 704 | Verificado |
| Mercado Pago | `X-Idempotency-Key` | sim, em Payments e Refunds; também no envio de documentação de chargeback | não documentado | não documentado | Verificado (parcial) |
| Pagar.me | não confirmado | não confirmado | não documentado | não documentado | Não verificável |
| Asaas | não encontrado nas páginas lidas | não confirmado | não documentado | não documentado | Não verificável |
| Rascunho IETF | `Idempotency-Key` | não é norma | política do servidor | 422 | Verificado (rascunho de 2021, expirado) |

Regra: **célula sem fonte fica "não documentado" e vira pergunta ao fornecedor, nunca valor assumido.** Mercado Pago: três datas aparecem no anúncio de obrigatoriedade (04-01-2024 no cabeçalho, 09/01/2024 no corpo, 2023/01/04 na URL) e o formato DD/MM ou MM/DD é ambíguo — registre as três e não decida (V-57, V-70). O Asaas recomenda consultar as cobranças existentes antes de recriar (V-52), o que cobre parte do caso sem garantia documentada.

## 6. Idempotência no Pix

No Pix a chave é o identificador da própria spec: `txid` da cobrança (26 a 35 caracteres, enviado pelo recebedor), `EndToEndId` do pagamento e `id` da devolução (1 a 35, único por `e2eid`). Enviar o `txid` próprio **é** a idempotência da cobrança; se o PSP gerar o `txid`, a idempotência não está garantida (Manual v2.10.0, seção 5.3; V-44, Verificado). Timeout ao criar cobrança: consulte pelo `txid` antes de reenviar; timeout em pagamento: consulte pelo `EndToEndId` (V-48; o limite de 30 s é herdado do brain, **Não verificado**). Detalhes em `pix-boleto-cartao-br.md`.

## 7. Webhook: modelo mental e handler de 7 passos

Webhook é **fato não confiável, entregue ao menos uma vez, possivelmente fora de ordem** (V-05). Ele é um aviso para você ler o recurso, não uma ordem para mudar estado.

Handler de 7 passos (V-03, Verificado para Stripe; o padrão vale para qualquer provedor, com o esquema de assinatura do provedor):

1. **Corpo bruto**: capture os bytes exatos. Parse de JSON antes de verificar e middleware global de JSON registrado antes da rota do webhook são os anti-padrões clássicos.
2. **Verificar assinatura e tolerância** (comparação em tempo constante, segredo por endpoint e por modo).
3. **Gravar o evento** na inbox sob chave única do ID do evento (seção 8).
4. **Responder 2xx** antes de lógica pesada (Stripe: 3xx conta como falha; Mercado Pago: 200 ou 201 em menos de 22 s).
5. **Processar em fila**.
6. **Reler o recurso** na API autenticada antes de agir; a transição passa pela máquina de estados com chave idempotente.
7. **Marcar processado** (ou falha com motivo e tentativas).

Exemplo ilustrativo (Node, Express, SDK da Stripe; confira a versão do SDK instalada):

```js
// A rota do webhook vem ANTES de qualquer express.json() global e recebe Buffer.
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, req.header('stripe-signature'), process.env.STRIPE_WEBHOOK_SECRET);
  } catch { return res.sendStatus(400); }          // assinatura inválida: sem efeito
  const inserted = await inbox.insertIfAbsent('stripe', event.id, digest(req.body), req.body);
  if (inserted === 'digest_mismatch') return res.sendStatus(202); // quarentena, alertar
  await queue.wake();                               // a fila só desperta; a varredura lê a inbox
  res.sendStatus(200);
});
```

Regras de ordem: não ordene por `created`; a ordem de entrega não é garantida (Stripe). Evento fora de ordem **converge** porque o handler relê o estado atual e a máquina de estados rejeita transição obsoleta. Deduplique por ID do evento, e por `data.object.id` com `event.type` quando houver dois eventos para o mesmo efeito.

## 8. Inbox imutável, digest e quarentena

```sql
CREATE TABLE webhook_inbox (
  provider    text NOT NULL,
  event_id    text NOT NULL,
  digest      text NOT NULL,          -- hash do corpo bruto
  payload     bytea NOT NULL,         -- retenção curta; sem PAN; avalie criptografar
  received_at timestamptz NOT NULL DEFAULT now(),
  status      text NOT NULL DEFAULT 'received' CHECK (status IN ('received','processed','failed','quarantined')),
  attempts    int  NOT NULL DEFAULT 0,
  PRIMARY KEY (provider, event_id)
);
```

- Mesmo `event_id` com `digest` diferente **não é duplicata**: vai para `quarantined` com alerta (V-05).
- A fila é **despertador**; a fonte de trabalho é a varredura das linhas `received` e `failed` prontas. Assim, perda de mensagem na fila não perde evento.
- Evidência por evento: identidade, digests, versão de chave, tentativas, correlation ID, com redação de segredos.
- ID desconhecido ou recurso inexistente na releitura: quarentena, não erro 500 em loop.

## 9. Matriz de autenticação de webhook por provedor (V-66, datada de 2026-10-10)

| Provedor | Onde está a autenticação | Regra | Status |
| --- | --- | --- | --- |
| Stripe | header `Stripe-Signature` | esquema `v1`: HMAC-SHA256 sobre `timestamp.payload`; tolerância padrão 5 min (nunca 0); ignorar outros esquemas; rotação com dois segredos por até 24 h | Verificado |
| Adyen | `additionalData.hmacSignature` no corpo (webhooks padrão) ou header `hmacsignature` (outros tipos, com `protocol` HmacSHA256) | HMAC-SHA256 em Base64; chave em hexadecimal convertida para bytes; padrão: concatenar `pspReference`, `originalReference`, `merchantAccountCode`, `merchantReference`, `value`, `currency`, `eventCode`, `success` separados por `:` (vazio = string vazia); com header: corpo bruto; aceitar a chave anterior por um tempo ao rotacionar | Verificado |
| Mercado Pago | header `x-signature` (`ts=...,v1=...`) com `x-request-id` e `data.id` | manifesto e algoritmo **não documentados na página**; use o SDK oficial | Não verificável |
| Paymob | callback | HMAC-SHA512; pedido só vira pago por callback verificado, nunca por redirecionamento | Verificado |
| Asaas | header `asaas-access-token` | token compartilhado de 32 a 255 caracteres, sem HMAC; não autentica o corpo | Verificado |
| Efí (Pix) | TLS mútuo (mTLS) | recusar a requisição sem certificado; TLS 1.2 no mínimo; no modo skip-mTLS, IP e HMAC na URL por conta do integrador | Verificado |
| Pagar.me | não documentado | tratar como não autenticado e reler pela API (seção 10) | Verificado (lacuna) |

Notas por provedor:
- **Stripe**: segredo separado por endpoint e por modo (teste e produção); rota isenta de CSRF; allowlist de IP como defesa em profundidade (leia a lista vigente, não copie); retries automáticos por até 3 dias em produção; reenvio manual de até 15 dias no Dashboard e 30 pela CLI.
- **Mercado Pago**: responda 200 ou 201; espera de 22 s e retry a cada 15 minutos (janela estendida após a terceira tentativa); notificações de QR não são verificáveis com o segredo (não reverificado).
- **Asaas** (V-51): rejeitar POST sem o cabeçalho esperado (comportamento sem ele não é descrito: **Inferido**); comparar o token em tempo constante (**Inferido**); persistir o evento com `id` único antes do 2xx; entrega "at least once"; após 15 falhas consecutivas a fila pode ser interrompida e eventos novos deixam de ser enviados até a reativação; eventos guardados por 14 dias.
- **Efí** (V-53): a Efí faz duas requisições, uma sem certificado (deve ser recusada) e outra com; registro `PUT /v2/webhook/:chave` (sucesso 201); timeout de 60 s; retentativas em intervalos de 5, 5, 10, 20, 40, 80 e 160 minutos (a contagem "até 9 novas tentativas" é **ambígua** na página); depois, `POST /v2/gn/webhook/reenviar`. Não fixe no código o IP exibido na página.
- **Pix (callback do BCB)**: ver `pix-boleto-cartao-br.md` (checklist de notificação V-54, **Inferido**).

Princípio: token compartilhado é autenticação mínima; mTLS ou HMAC sobre o corpo é preferível; **nenhum** provedor sem assinatura recebe ação financeira sem releitura pela API autenticada (V-50).

## 10. Provedor sem assinatura documentada (regra V-50)

1. Registre numa tabela (`assets/templates/tabela-provedores-webhook.md`) onde está a assinatura, o que se assina, o algoritmo e a janela. Se a documentação não traz, escreva "não documentado" e **não invente** o algoritmo (nem header, nem HMAC).
2. Sem assinatura documentada: trate o endpoint como não autenticado, aceite apenas o identificador do recurso, releia o estado pela API autenticada, não mude estado financeiro com base no corpo e aplique allowlist de IP ou domínio publicada pelo provedor, lida na hora da configuração (Pagar.me exige TLS 1.2 ou 1.3 e publica faixas na página de Segurança; não copie as faixas).
3. Deduplique por identificador do evento ou do recurso, responda 2xx rápido e processe em fila.
4. Peça ao fornecedor, por escrito, o método de autenticação antes do go-live. A ausência na documentação não prova ausência no produto.

Vale para Pagar.me (V-37) e, até leitura do manifesto, para o `x-signature` do Mercado Pago (use o SDK).

## 11. Retentativas, retenção e pausa de fila por provedor (V-67, datada de 2026-10-10)

| Provedor | Retentativa e retenção | Status |
| --- | --- | --- |
| Asaas | fila pode pausar após 15 falhas consecutivas; eventos guardados 14 dias | Verificado (relido) |
| Efí | intervalos de 5 a 160 minutos, reenvio manual disponível | Verificado (relido) |
| Stripe | até 3 dias em produção | Verificado (V-03, não relido na rodada 3) |
| Mercado Pago | 22 s de espera, retry a cada 15 minutos | Verificado (V-04, não relido) |
| Pagar.me, Pix em outros PSPs | sem dado | Não verificável |

Regra operacional (**Inferido**): a **cadência da conciliação deve ser menor que a menor janela de reenvio ou retenção entre os provedores em uso**, para que nenhum evento perdido saia da janela antes de ser conferido. Alerte quando a fila de um provedor estiver pausada; o limiar é do projeto (**Suposição**, sem fonte).

## 12. Outbox, DLQ, backoff e jitter (brain-of-agent, MIT, adaptado)

| Tema | Caso | Esperado |
| --- | --- | --- |
| Entrega ao menos uma vez | publicar a mesma mensagem duas vezes | efeito aplicado uma vez (chave de idempotência, tabela de mensagens processadas) |
| Ordenação | `PedidoCancelado` antes de `PedidoCriado` | ordem só por partição ou chave; consumidor trata fora de ordem por versão e estado |
| Mensagem venenosa | payload inválido | vai para a DLQ após N tentativas com o motivo; a fila não trava; há reprocessamento da DLQ |
| Retry | dependência responde 503 três vezes | backoff exponencial com jitter; só operações idempotentes repetem |
| Outbox | banco grava, broker cai antes de publicar | o evento sai depois pela outbox; nunca grava sem publicar nem publica sem gravar |
| Timeouts em cascata | serviço C lento | timeout de quem chama maior que o de quem é chamado somado aos retries; senão A desiste enquanto C executa e o retry duplica |

Prazo em toda chamada de E/S (inclusive banco) e circuit breaker antes de retry (V-28). Chaos engineering só em ambiente de teste, com hipótese escrita e condição de aborto; em produção, só com autorização explícita.

## 13. Roteiro de testes hostis (resumo; detalhes na skill `webhook-handler`)

Oráculo: estado no banco, não a resposta HTTP. Assinaturas geradas **localmente** com dados sintéticos; nunca enviar evento a provedor real.

| Caso | Esperado |
| --- | --- |
| Assinatura válida | aceito uma vez, um efeito |
| Assinatura forjada ou corpo alterado | 4xx, nenhum efeito, nenhuma linha na inbox |
| Mesmo evento duas vezes | um só efeito |
| Eventos fora de ordem | estado final converge |
| ID de evento ou recurso desconhecido | quarentena |
| Mesmo ID, digest diferente | quarentena com alerta |
| Crash depois do efeito, antes de marcar processado | reprocessamento não duplica o efeito |
| Evento envenenado | DLQ com motivo; fila segue |
| Replay fora da tolerância | rejeitado (Stripe: 5 minutos) |
| Rotação de segredo | evento assinado com a chave anterior é aceito na janela |
| Fila fora do ar | varredura da inbox recupera depois |

Para provar que o teste vale, desligue a proteção (constraint, verificação) e confirme que o teste falha.

## 14. Gotchas

- O post de 2017 (Brandur Leach) justifica o padrão, mas não trata de armazenamento, expiração nem concorrência.
- Cache em memória, `Set` local e lock distribuído não são proteção suficiente; sobrevivem mal a restart e a várias instâncias.
- "2xx em 200 ms" (wshobson) não tem fonte; Stripe e Mercado Pago dão regras próprias.
- O payload padrão do Adyen traz a assinatura no corpo; os de outros tipos, no header.
- Não instale PagoKit nem seus hooks (executam Node). A Paymob exige callback verificado, nunca redirecionamento — vale para todos.
- Backoff sem jitter sincroniza clientes e cria tempestade de retries.
- Para padrões genéricos de API e filas (sem dinheiro), `/backend-api:playbook` e `/automation-integrations:playbook` aprofundam.
