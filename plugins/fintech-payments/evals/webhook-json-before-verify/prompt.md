---
name: webhook-json-before-verify
description: "Mede se o plugin revisa um endpoint de webhook do Stripe e encontra a assinatura calculada sobre corpo reserializado, o middleware de JSON antes da rota, o dedupe em memória e a mudança de estado sem releitura, propondo inbox com unicidade, fila e testes hostis."
tags: [fintech-payments, webhook-handler, stripe]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta JSON.stringify(req.body) quebrando a verificação e o express.json global, dedupe em memória perdido em reinício, processamento no handler em vez de fila, ausência de releitura do recurso e ordem não garantida, e sugere testes hostis, declarando o que é específico da Stripe."
model: sonnet
---
Revise meu endpoint de webhook do Stripe (Express). Está em produção e às vezes marca pedido como pago duas vezes.

```js
const express = require('express');
const Stripe = require('stripe');
const stripe = new Stripe(process.env.STRIPE_KEY);
const app = express();
app.use(express.json());
const seen = new Set();

app.post('/webhook', async (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event;
  try {
    event = stripe.webhooks.constructEvent(JSON.stringify(req.body), sig, process.env.WH_SECRET);
  } catch (e) {
    return res.status(400).send('bad signature');
  }
  if (seen.has(event.id)) return res.sendStatus(200);
  seen.add(event.id);
  if (event.type === 'checkout.session.completed') {
    await db.orders.update({ status: 'paid' }, { where: { id: event.data.object.client_reference_id } });
  }
  res.sendStatus(200);
});
```

Roda em duas instâncias atrás de um balanceador. Não tenho o repositório aberto aqui; use só o que escrevi.
