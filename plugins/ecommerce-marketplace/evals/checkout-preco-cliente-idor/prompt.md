---
name: checkout-preco-cliente-idor
description: "Caso de disparo da revisão de checkout. Endpoint Express com total vindo do cliente, rota de pedido sem checar o dono e cupom concatenado em SQL. Mede se a revisão aponta os três defeitos com trecho, severidade e correção mínima, sem inventar execução."
tags: [ecommerce-marketplace, checkout-seguro, security, idor, injection]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta total vindo do corpo da requisição (recalcular no servidor), IDOR em GET /orders/:id (checar dono) e injeção SQL no cupom (parametrizar), cada um com trecho ou linha, severidade e correção mínima; rotula o que não verificou e não afirma ter executado nada."
model: sonnet
---
Revisa esse endpoint do meu checkout antes do deploy de amanhã. Loja pequena, Node 20 com Express e Postgres (biblioteca `pg`), pagamento pela Stripe em modo de teste. Ainda não rodei os testes. Quero os problemas por ordem de gravidade e o que eu corrijo primeiro.

```js
// src/routes/checkout.js
const express = require('express');
const router = express.Router();
const db = require('../db');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

router.post('/checkout', async (req, res) => {
  const { items, couponCode, total, address } = req.body;

  let discount = 0;
  if (couponCode) {
    const r = await db.query(
      "SELECT value FROM coupons WHERE code = '" + couponCode + "' AND active = true"
    );
    if (r.rows.length) discount = r.rows[0].value;
  }

  const order = await db.query(
    'INSERT INTO orders (user_id, total, discount, address, status) VALUES ($1,$2,$3,$4,$5) RETURNING id',
    [req.session.userId, total, discount, address, 'pending']
  );

  const intent = await stripe.paymentIntents.create({
    amount: Math.round(total * 100),
    currency: 'brl',
    metadata: { orderId: order.rows[0].id },
  });

  res.json({ orderId: order.rows[0].id, clientSecret: intent.client_secret });
});

router.get('/orders/:id', async (req, res) => {
  const r = await db.query('SELECT * FROM orders WHERE id = $1', [req.params.id]);
  if (!r.rows.length) return res.status(404).json({ error: 'not found' });
  res.json(r.rows[0]);
});

module.exports = router;
```
