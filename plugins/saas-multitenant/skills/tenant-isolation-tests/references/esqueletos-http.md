# Esqueletos de teste HTTP, jobs e webhooks

Esqueletos escritos para esta skill; adapte à stack e confirme as APIs na versão instalada (PAD-13). Nada foi executado nesta pesquisa. Conferido em 2026-10-10. Dados são sintéticos; nenhum segredo real aparece: valores vêm de variáveis de ambiente.

## 1. Seeds e helpers (TypeScript; Vitest ou Jest + supertest)

```ts
// tests/isolation/seed.ts
export const TENANTS = {
  A: { id: '11111111-1111-4111-8111-111111111111', name: 'Acme Ltda' },
  B: { id: '22222222-2222-4222-8222-222222222222', name: 'Acme Ltd' },   // nome parecido de propósito
} as const;

export const ROLES = ['owner', 'admin', 'member', 'viewer', 'billing'] as const;

// Cria tenants, usuários por papel e objetos pelo MESMO caminho que a aplicação usa
// (repositório/serviço), dentro do contexto de cada tenant. Idempotente: apaga só as linhas da fixture.
export async function seed(db: TestDb) {
  for (const t of Object.values(TENANTS)) {
    await db.withTenant(t.id, async (tx) => {
      await tx.tenant.upsert(t);
      for (const role of ROLES) await tx.user.upsert({ email: `${role}@${slug(t.name)}.test`, role });
      await tx.invoice.upsert({ id: idOf(t, 'inv-1'), number: 'INV-001' });
      await tx.invoice.upsert({ id: idOf(t, 'inv-2'), number: 'INV-002' });   // mesmo número nos dois tenants
    });
  }
}

// Token emitido pelo caminho real de login/IdP de teste, nunca por atalho que a produção não aceita.
export async function tokenFor(tenant: keyof typeof TENANTS, role: (typeof ROLES)[number]): Promise<string> {
  return loginViaTestIdp(`${role}@${slug(TENANTS[tenant].name)}.test`);
}
```

`withTenant`, `loginViaTestIdp`, `slug` e `idOf` são helpers do projeto de teste: escreva-os lendo a aplicação; não os invente como se existissem na biblioteca.

## 2. Linhas da matriz em HTTP

```ts
import request from 'supertest';
import { app } from '../../src/app';

describe('isolamento por ID', () => {
  it('tenant A recebe 404 para fatura do tenant B, igual a um ID inexistente', async () => {
    const tokenA = await tokenFor('A', 'member');
    const cross = await request(app).get(`/invoices/${idOf(TENANTS.B, 'inv-1')}`).set('Authorization', `Bearer ${tokenA}`);
    const missing = await request(app).get('/invoices/00000000-0000-4000-8000-000000000000').set('Authorization', `Bearer ${tokenA}`);
    expect(cross.status).toBe(404);
    expect(cross.body).toEqual(missing.body);                 // não distingue "é de outro" de "não existe"
  });

  it('controle positivo: tenant A lê a própria fatura', async () => {
    const tokenA = await tokenFor('A', 'member');
    const own = await request(app).get(`/invoices/${idOf(TENANTS.A, 'inv-1')}`).set('Authorization', `Bearer ${tokenA}`);
    expect(own.status).toBe(200);
    expect(own.body.number).toBe('INV-001');
  });
});

describe('escalada no corpo', () => {
  it('member não troca papel nem tenant pelo corpo', async () => {
    const tokenA = await tokenFor('A', 'member');
    const res = await request(app).patch('/me').set('Authorization', `Bearer ${tokenA}`)
      .send({ role: 'owner', tenantId: TENANTS.B.id });
    expect([200, 400, 403]).toContain(res.status);            // aceita ignorar ou recusar
    const me = await request(app).get('/me').set('Authorization', `Bearer ${tokenA}`);
    expect(me.body.role).toBe('member');
    expect(me.body.tenantId).toBe(TENANTS.A.id);
  });
});

describe.each([
  ['viewer', 'POST', '/invoices', 403],
  ['member', 'DELETE', '/invoices/__own__', 403],
  ['admin', 'DELETE', '/invoices/__own__', 204],
])('papel %s em %s %s', (role, method, path, expected) => {
  it(`responde ${expected}`, async () => { /* resolve __own__ para um ID do tenant A e chama pela API */ });
});

describe('busca e exportação', () => {
  it('a busca por "Acme" do tenant A não devolve nada do tenant B', async () => {
    const tokenA = await tokenFor('A', 'admin');
    const res = await request(app).get('/search').query({ q: 'Acme' }).set('Authorization', `Bearer ${tokenA}`);
    const ids = res.body.items.map((i: { id: string }) => i.id);
    expect(ids.length).toBeGreaterThan(0);                    // controle positivo
    expect(ids.every((id: string) => id.startsWith('a'))).toBe(true);   // adapte: regra de pertencimento ao tenant A
  });
});
```

Para exportação CSV, anexos e URL assinada: baixe como A o recurso de B (deve falhar com 404), peça URL assinada do próprio recurso, avance o relógio falso além da validade e verifique a recusa; verifique que a URL do tenant A não abre o objeto B alterando o caminho (V-49).

## 3. Limite de plano com corrida

```ts
it('dois convites simultâneos no limite não passam de 5 assentos', async () => {
  await fillSeatsTo(TENANTS.A.id, 4);                          // 4 de 5 ocupados
  const token = await tokenFor('A', 'admin');
  const [r1, r2] = await Promise.all([
    request(app).post('/invites').set('Authorization', `Bearer ${token}`).send({ email: 'x1@acme-ltda.test' }),
    request(app).post('/invites').set('Authorization', `Bearer ${token}`).send({ email: 'x2@acme-ltda.test' }),
  ]);
  expect([r1.status, r2.status].sort()).toEqual([201, 409]);   // adapte ao código de erro do produto
  expect(await seatCount(TENANTS.A.id)).toBe(5);
});
```

Se o teste falhar por intermitência, a contagem de assentos tem corrida: use bloqueio de linha do tenant ou restrição no banco (decisão da skill `saas-feature-spec`).

## 4. Jobs em lote

```ts
it('o relatório noturno de cada tenant contém só faturas dele', async () => {
  await runNightlyReport();                                    // processa os dois tenants
  const a = await loadReport(TENANTS.A.id);
  const b = await loadReport(TENANTS.B.id);
  expect(a.invoiceIds.length).toBeGreaterThan(0);
  expect(a.invoiceIds.every((id) => belongsTo(TENANTS.A, id))).toBe(true);
  expect(b.invoiceIds.every((id) => belongsTo(TENANTS.B, id))).toBe(true);
});
```

## 5. Cache com permissão

```ts
it('relatório em cache do tenant A não é entregue ao tenant B com o mesmo report_id', async () => { /* aquece como A; pede como B; espera 404 */ });
it('usuário que perde a permissão antes do TTL passa a ser negado', async () => { /* aquece; revoga o papel; relê; espera 403 ou 404 */ });
```

## 6. SCIM e SSO (doubles locais)

```ts
it('desativar via SCIM revoga a sessão na hora', async () => {
  const session = await loginAs('A', 'member');
  const res = await request(app).patch(`/scim/v2/Users/${session.userId}`)
    .set('Authorization', `Bearer ${process.env.SCIM_TOKEN_TENANT_A}`)
    .send({ schemas: ['urn:ietf:params:scim:api:messages:2.0:PatchOp'], Operations: [{ op: 'Replace', path: 'active', value: false }] });
  expect(res.status).toBe(200);
  expect((await request(app).get('/me').set('Authorization', `Bearer ${session.token}`)).status).toBe(401);
  // usuário preservado e grupos mantidos (V-55): não houve DELETE
  expect(await userExists(session.userId)).toBe(true);
});

it('token SCIM do tenant A não toca usuário do tenant B', async () => {
  const res = await request(app).get(`/scim/v2/Users/${userIdOf('B', 'member')}`)
    .set('Authorization', `Bearer ${process.env.SCIM_TOKEN_TENANT_A}`);
  expect(res.status).toBe(404);
});
```

`SCIM_TOKEN_TENANT_A` é um token de teste gerado pela fixture; nunca um token de produção.

## 7. Webhook de billing: duplicado, fora de ordem, assinatura inválida

Com Stripe, o SDK de Node expõe um gerador de cabeçalho de teste (confirme na versão instalada):

```ts
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY_TEST!);     // chave de teste, via ambiente
const secret = process.env.STRIPE_WEBHOOK_SECRET_TEST!;

function signed(payload: object) {
  const body = JSON.stringify(payload);
  const header = stripe.webhooks.generateTestHeaderString({ payload: body, secret });
  return { body, header };
}

it('evento duplicado não duplica efeito', async () => {
  const { body, header } = signed(fixtureEvent('evt_dup_1', 'invoice.paid', { customer: 'cus_A' }));
  await request(app).post('/webhooks/stripe').set('Stripe-Signature', header).set('Content-Type', 'application/json').send(body).expect(200);
  await request(app).post('/webhooks/stripe').set('Stripe-Signature', header).set('Content-Type', 'application/json').send(body).expect(200);
  await drainWebhookQueue();
  expect(await countRows('stripe_events', { event_id: 'evt_dup_1' })).toBe(1);   // conte no banco, não só a resposta
  expect(await billingEffectsFor('cus_A')).toHaveLength(1);
});

it('assinatura inválida é recusada', async () => {
  const { body } = signed(fixtureEvent('evt_bad_1', 'invoice.paid', { customer: 'cus_A' }));
  await request(app).post('/webhooks/stripe').set('Stripe-Signature', 't=1,v1=deadbeef').send(body).expect(400);
});

it('corpo alterado depois de assinado é recusado', async () => {
  const { body, header } = signed(fixtureEvent('evt_tamper_1', 'invoice.paid', { customer: 'cus_A' }));
  await request(app).post('/webhooks/stripe').set('Stripe-Signature', header).send(body.replace('cus_A', 'cus_B')).expect(400);
});

it('invoice.paid antes de customer.subscription.created converge para o estado correto', async () => {
  await deliver('invoice.paid');                      // chega primeiro
  await deliver('customer.subscription.created');     // chega depois
  await drainWebhookQueue();
  expect(await accessStateOf(TENANTS.A.id)).toBe(expectedStateFromStripeFixture());
});
```

O worker busca o objeto atual na API do provedor; nos testes, substitua o cliente por um double que devolve o objeto da fixture. `fixtureEvent`, `deliver`, `drainWebhookQueue`, `countRows` e `billingEffectsFor` são helpers do projeto de teste.

Em Python, sem gerador de cabeçalho no SDK de testes, calcule o cabeçalho com a regra documentada de assinatura (HMAC-SHA256 de `"{t}.{corpo}"` com o segredo; formato `t=<timestamp>,v1=<assinatura>`; confirme na documentação de webhooks vigente):

```py
import hashlib, hmac, time

def stripe_test_header(body: bytes, secret: str, ts: int | None = None) -> str:
    ts = ts or int(time.time())
    sig = hmac.new(secret.encode(), f"{ts}.".encode() + body, hashlib.sha256).hexdigest()
    return f"t={ts},v1={sig}"
```

Para PSP com token estático (Asaas): teste que o token errado recebe a recusa, que o `id` repetido não gera efeito, que a resposta é exatamente 200 e que o processamento ocorre fora da requisição (V-50). O que chega em cancelamento é Não verificável sem sandbox (V-51).
