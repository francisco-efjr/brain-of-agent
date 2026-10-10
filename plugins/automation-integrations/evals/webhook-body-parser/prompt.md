---
name: webhook-body-parser
description: "Mede se o plugin revisa um handler de webhook Stripe e encontra corpo reencodado, ausência de deduplicação e trabalho pesado antes do 2xx, sem inventar testes executados."
tags: [automation-integrations, reviewing-webhook-receivers, webhook, stripe, positivo]
runs: 3
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
expected_outcome: "Reporta pelo menos corpo reencodado quebrando a assinatura, ausência de dedupe por ID do evento e envio de e-mail antes do 2xx, propõe fila e fila de mortas e um roteiro de replay, e diz que prazos são do provedor."
---
Pode revisar meu endpoint de webhook da Stripe? Ele recebe `checkout.session.completed`, grava o pedido e manda e-mail de confirmação. Em produção às vezes o cliente recebe dois e-mails e já tive um pedido duplicado. Quando a assinatura dava erro em desenvolvimento eu cheguei a comentar a verificação para testar, depois voltei. Aqui está (Express 4, Node 20, Postgres):

```js
const express = require('express');
const crypto = require('crypto');
const app = express();
app.use(express.json());

app.post('/webhooks/stripe', async (req, res) => {
  const sig = req.headers['stripe-signature'];
  const payload = JSON.stringify(req.body);
  const expected = crypto
    .createHmac('sha256', process.env.STRIPE_WEBHOOK_SECRET)
    .update(payload)
    .digest('hex');
  if (!sig.includes(expected)) {
    return res.status(400).send('assinatura inválida');
  }
  const event = req.body;
  if (event.type === 'checkout.session.completed') {
    const s = event.data.object;
    await enviarEmailPedido(s.customer_email, s.id);   // chama o SendGrid, leva uns 2s
    await db.query('INSERT INTO pedidos (session_id, status) VALUES ($1, $2)', [s.id, 'pago']);
  }
  res.status(200).send('ok');
});

app.listen(3000);
```

Quero saber o que está errado e como deixar confiável, incluindo o que fazer quando algo falha no meio.
