---
name: webhook-corpo-bruto-stripe
description: "Caso de disparo do webhook de pagamento. Pedido para implementar o webhook da Stripe em um Express que já usa express.json globalmente. Mede verificação sobre o corpo bruto, dedupe por ID de evento com restrição única, resposta 2xx rápida com fila, estado atual pela API e pedido pago só após evento verificado."
tags: [ecommerce-marketplace, webhook-pagamento, stripe, idempotency, signature]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega handler que verifica a assinatura sobre o corpo bruto (rota com raw body registrada antes do json global), usa constructEvent com segredo por variável de ambiente, grava event.id com restrição única, responde 2xx rápido e processa em fila, busca o estado atual na API e confere valor e moeda antes de marcar pago; sugere stripe listen sem executar; propõe testes que contam linhas."
model: sonnet
---
Preciso implementar o webhook de pagamento da Stripe no meu backend. Quando chegar `payment_intent.succeeded`, o pedido tem que ficar como pago. Estou só em modo de teste. Meu `server.js` hoje é assim:

```js
// server.js
const express = require('express');
const app = express();

app.use(express.json());
app.use(require('./src/routes/checkout'));

app.listen(3000);
```

A tabela é `orders (id, total_cents, currency, status, payment_intent_id)` no Postgres, e o `payment_intent_id` é gravado quando o checkout cria a cobrança. Já existe uma função `markOrderPaid(orderId)` em `src/orders.js`. Não tenho fila ainda, mas posso usar o que for simples. Escreve o handler, o ajuste no `server.js` e os testes, e me diz como testar localmente.
