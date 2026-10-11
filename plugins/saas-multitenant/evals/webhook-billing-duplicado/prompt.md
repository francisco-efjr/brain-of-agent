---
name: webhook-billing-duplicado
description: Mede se o plugin diagnostica um webhook Stripe com parser JSON antes da verificação, sem deduplicação, que concede acesso por checkout.session.completed e estende validade em invoice.paid, e propõe o handler seguro com corpo bruto, assinatura, event.id único, fila, worker que busca o estado atual, tabela status para acesso e testes de duplicado e fora de ordem, sem pedir chave.
tags: [saas-multitenant, stripe-billing-lifecycle, webhook, idempotency]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Explica a cobrança dupla e o acesso errado pela falta de deduplicação por event.id, pelo parser JSON antes da assinatura e pela concessão por eventos isolados; propõe corpo bruto com assinatura, tabela com event.id UNIQUE, fila, worker que busca o objeto atual, acesso por tabela status para acesso, testes de duplicado e fora de ordem, trata past_due como decisão de produto e não pede nem escreve chave real."
model: sonnet
---
Estamos em Node com Express e Stripe Billing. O cliente reclamou de cobrança dupla e de acesso errado ao plano Pro (um tenant ficou com o Pro depois que a assinatura foi cancelada, e outro foi liberado antes de pagar). Esse é o nosso webhook. Me explica o que está errado e como deixar correto. Não tenho como rodar nada aqui agora.

```js
const app = express();
app.use(express.json());

app.post('/stripe/webhook', async (req, res) => {
  const event = req.body;
  const obj = event.data.object;

  if (event.type === 'checkout.session.completed') {
    await db.tenant.update({
      where: { stripeCustomerId: obj.customer },
      data: { plan: 'pro' },
    });
  }

  if (event.type === 'invoice.paid') {
    await db.tenant.update({
      where: { stripeCustomerId: obj.customer },
      data: { paidUntil: addMonths(new Date(), 1) },
    });
  }

  res.sendStatus(200);
});
```

Também temos a página `/sucesso`, para onde o Checkout redireciona; ela já marca `plan = 'pro'` quando o `session_id` aparece na URL.
