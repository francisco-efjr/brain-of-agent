# Modelo de dados e handler de webhook (Stripe)

Esqueletos escritos para esta skill, em TypeScript (Express, `stripe` para Node, `pg`) e PostgreSQL. Nada foi executado nesta pesquisa. Confirme métodos e campos na versão instalada do SDK e na versão de API do projeto (PAD-13). Base: V-02, V-03, V-04, V-05, V-34, V-39. Conferido em 2026-10-10. Nenhuma chave real: valores vêm de variáveis de ambiente.

## 1. DDL

```sql
-- Global (sem tenant no momento do recebimento): acessada só pela role do módulo de webhook.
CREATE TABLE stripe_events (
  event_id     text PRIMARY KEY,                 -- evt_...; PK garante o UNIQUE da deduplicação
  type         text NOT NULL,
  object_ref   text,                             -- id do objeto principal (sub_, in_, cus_); sem payload completo (evita PII)
  received_at  timestamptz NOT NULL DEFAULT now(),
  attempts     integer NOT NULL DEFAULT 0,
  next_attempt_at timestamptz NOT NULL DEFAULT now(),
  processed_at timestamptz,
  last_error   text
);
CREATE INDEX stripe_events_pending_idx ON stripe_events (next_attempt_at) WHERE processed_at IS NULL;

-- Tabelas de tenant (com RLS conforme a skill tenant-rls-migration).
CREATE TABLE tenant_billing_state (
  tenant_id              uuid PRIMARY KEY REFERENCES tenants (id),
  stripe_subscription_id text UNIQUE,
  status                 text NOT NULL,          -- espelho do status da Stripe
  access                 text NOT NULL CHECK (access IN ('full', 'limited', 'none')),   -- derivado da tabela status -> acesso
  price_id               text,
  quantity               integer,
  current_period_end     timestamptz,
  cancel_at_period_end   boolean NOT NULL DEFAULT false,
  fetched_at             timestamptz NOT NULL,   -- instante em que o estado foi lido na Stripe
  updated_at             timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE tenant_features (
  tenant_id   uuid NOT NULL REFERENCES tenants (id),
  feature_key text NOT NULL,                     -- igual ao lookup_key da feature na Stripe (V-05)
  source      text NOT NULL CHECK (source IN ('stripe_entitlement', 'override')),
  updated_at  timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, feature_key)
);

-- tenants.stripe_customer_id text UNIQUE (um Customer por tenant; metadata.tenant_id no Customer, V-39).
```

## 2. Handler: verifica, grava, responde

```ts
import express from 'express';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);          // fixe a versão de API conforme a política do projeto
const app = express();

// A rota recebe o corpo BRUTO. Nenhum parser JSON global pode rodar antes dela
// (monte express.json() depois, ou exclua esta rota). A rota fica fora da proteção CSRF (V-03).
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(                          // verifica Stripe-Signature; tolerância padrão de 5 min
      req.body,                                                      // Buffer
      req.header('stripe-signature') ?? '',
      process.env.STRIPE_WEBHOOK_SECRET!,
    );
  } catch {
    return res.status(400).send('invalid signature');               // não detalhe o motivo
  }

  try {
    // Deduplicação: duplicado cai no ON CONFLICT e responde 200 sem agir.
    await db.query(
      `INSERT INTO stripe_events (event_id, type, object_ref)
       VALUES ($1, $2, $3) ON CONFLICT (event_id) DO NOTHING`,
      [event.id, event.type, objectRef(event)],
    );
  } catch (e) {
    return res.sendStatus(500);                                      // falha transitória: a Stripe reenvia
  }
  return res.sendStatus(200);                                        // 2xx antes da lógica pesada (V-03)
});
```

A tabela `stripe_events` é também a fila (padrão outbox): gravar e responder em uma operação evita o buraco "gravou mas não enfileirou". Se preferir fila externa, grave a linha e enfileire na mesma transação ou use um varredor que reenfileira linhas com `processed_at IS NULL` antigas.

Eventos "thin" (V-03): a Stripe os recomenda para integrações novas e snapshot se uma ferramenta de terceiros exigir o payload completo. Com thin, o worker lê o objeto na API de qualquer forma; confira na documentação do SDK o método de parse correspondente à sua versão.

Em Python, o equivalente é `stripe.Webhook.construct_event(request.get_data(), cabecalho, segredo)`; capture a exceção de assinatura inválida e a de payload inválido (os nomes das classes variam por versão do SDK: confira) e responda 400.

## 3. Worker: busca o estado atual e reconcilia o tenant

O worker não confia no payload nem na ordem: ao receber qualquer evento de billing de um Customer, ele relê as assinaturas do Customer e recalcula o estado. Reprocessar o mesmo evento é seguro.

```ts
type Policy = { pastDue: 'full' | 'limited' | 'none'; paused: 'none' | 'limited' };   // decisão de produto, escrita no spec

function accessFor(status: Stripe.Subscription.Status, p: Policy): 'full' | 'limited' | 'none' {
  switch (status) {
    case 'trialing':
    case 'active':   return 'full';
    case 'past_due': return p.pastDue;                 // padrão sugerido (Inferido): liberar com aviso e prazo
    case 'paused':   return p.paused;                  // Suposição: suspender
    default:         return 'none';                    // incomplete, incomplete_expired, unpaid, canceled
  }
}

async function reconcileCustomer(customerId: string, policy: Policy) {
  const tenant = await db.oneOrNone('SELECT id FROM tenants WHERE stripe_customer_id = $1', [customerId]);
  if (!tenant) throw new UnmappedCustomer(customerId);              // registrar e alertar; nunca descartar em silêncio

  await db.tx(async (tx) => {
    await tx.query("SELECT set_config('app.tenant_id', $1, true)", [tenant.id]);   // contexto por transação (V-34)
    await tx.query('SELECT pg_advisory_xact_lock(hashtext($1))', [tenant.id]);     // serializa por tenant (nosso design, Inferido)

    // Lê DEPOIS de obter o bloqueio: o estado gravado é sempre o mais recente.
    const subs = await stripe.subscriptions.list({ customer: customerId, status: 'all', limit: 10 });
    const current = pickCurrent(subs.data);                        // regra do produto para múltiplas assinaturas
    const fetchedAt = new Date();

    await tx.query(
      `INSERT INTO tenant_billing_state
         (tenant_id, stripe_subscription_id, status, access, price_id, quantity, current_period_end, cancel_at_period_end, fetched_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
       ON CONFLICT (tenant_id) DO UPDATE SET
         stripe_subscription_id = EXCLUDED.stripe_subscription_id, status = EXCLUDED.status, access = EXCLUDED.access,
         price_id = EXCLUDED.price_id, quantity = EXCLUDED.quantity, current_period_end = EXCLUDED.current_period_end,
         cancel_at_period_end = EXCLUDED.cancel_at_period_end, fetched_at = EXCLUDED.fetched_at, updated_at = now()
       WHERE tenant_billing_state.fetched_at <= EXCLUDED.fetched_at`,
      [tenant.id, current?.id ?? null, current?.status ?? 'canceled', accessFor(current?.status ?? 'canceled', policy),
       /* price_id, quantity, current_period_end, cancel_at_period_end lidos do item da assinatura na sua versão de API */
       null, null, null, false, fetchedAt],
    );
  });
}
```

Notas:
- `pickCurrent` e a leitura de `price_id`, `quantity` e `current_period_end` dependem da sua versão de API (campos mudaram de lugar entre versões); leia o objeto Subscription da versão fixada.
- O bloqueio consultivo (`pg_advisory_xact_lock`) evita dois workers gravarem estados fora de ordem; o `WHERE ... fetched_at <=` é a segunda proteção. Ambos são design nosso (Inferido), não texto da Stripe.
- Entitlements: depois de gravar o estado, liste os entitlements ativos do Customer (API de active entitlements, conferir o nome do método na sua versão) e sincronize `tenant_features` (inserir os presentes, remover os ausentes com `source = 'stripe_entitlement'`, preservar `override`). O resumo do evento traz no máximo 10; pagine acima disso (V-05).

## 4. Laço do worker com retry, backoff e DLQ

```ts
export async function processNext(policy: Policy): Promise<boolean> {
  const ev = await db.tx(async (tx) => {
    const row = await tx.oneOrNone(
      `SELECT event_id, type, object_ref FROM stripe_events
        WHERE processed_at IS NULL AND next_attempt_at <= now() AND attempts < 10
        ORDER BY received_at LIMIT 1 FOR UPDATE SKIP LOCKED`);
    if (!row) return null;
    try {
      await handle(row, policy);                                    // resolve customerId e chama reconcileCustomer
      await tx.query('UPDATE stripe_events SET processed_at = now() WHERE event_id = $1', [row.event_id]);
    } catch (e) {
      // Atraso exponencial com jitter; depois de 10 tentativas a linha fica "morta" e gera alerta (DLQ lógica).
      await tx.query(
        `UPDATE stripe_events SET attempts = attempts + 1, last_error = $2,
                next_attempt_at = now() + (power(2, attempts + 1) * interval '1 second') * (0.5 + random())
          WHERE event_id = $1`, [row.event_id, String(e).slice(0, 500)]);
    }
    return row;
  });
  return ev !== null;
}
```

Observações: erro de mapeamento (`UnmappedCustomer`) entra no mesmo caminho e dispara alerta sem apagar o evento. Linhas com `attempts >= 10` e `processed_at IS NULL` são o alerta de DLQ. Para reprocessar um evento já processado (reenvio manual por 15 dias no Dashboard ou 30 na CLI, V-03), a deduplicação por `event_id` o ignora; reprocesse limpando `processed_at` de propósito, o que é seguro porque a reconciliação é idempotente.

O laço roda em processo separado da rota HTTP (cron, worker ou fila), para a resposta 200 não depender da lógica.

## 5. Criação idempotente do Customer (onboarding)

```ts
const customer = await stripe.customers.create(
  { email: owner.email, name: tenant.name, metadata: { tenant_id: tenant.id } },    // ID interno em metadata (V-39)
  { idempotencyKey: `tenant-${tenant.id}-create-customer` },                         // mesma chave em todo retry (V-04)
);
await db.query('UPDATE tenants SET stripe_customer_id = $1 WHERE id = $2 AND stripe_customer_id IS NULL', [customer.id, tenant.id]);
```

A sequência do onboarding (signup, organização, membro dono, Customer, features iniciais) é idempotente e retomável: falha no meio não deixa tenant órfão nem Customer duplicado (ordem Inferida; skill `tenant-data-lifecycle`).

## 6. Reconciliação periódica

Job diário que, para os tenants com Customer, chama `reconcileCustomer` com taxa limitada e registra divergências (estado local diferente do lido). Cobre evento perdido, endpoint fora do ar por mais de 3 dias, mudança manual no Dashboard e falha de entitlement (V-05, V-06). Alerta quando a divergência passa do limite definido pelo time (limite é Suposição).

## 7. Eventos a assinar

Assine só o que usa (V-03). Conjunto típico, a ajustar: `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`, `customer.subscription.trial_will_end`, `invoice.paid`, `invoice.payment_failed`, `invoice.finalization_failed`, `entitlements.active_entitlement_summary.updated`; riscos se o SaaS guarda esses dados: `charge.dispute.created`, `charge.refunded`, `radar.early_fraud_warning.created`; `customer.updated` se espelha dados do Customer. `checkout.session.completed` apenas liga Customer ao tenant.
