---
name: completo-ativacao-explicita
description: "Caso positivo do modo completo. O usuário pede explicitamente ECOMMERCE-COMPLETO para auditar uma loja (descrição, árvore e trechos). Mede leitura das referências em lotes com registro de lido, parcial ou ausente, matriz de aplicabilidade por área, auditoria sem alterar o produto, rótulos epistêmicos, Não verificável para fiscal e plataformas não lidas, e relatório final com limitações."
tags: [ecommerce-marketplace, playbook, ecommerce-completo, audit, matrix]
max_turns: 24
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 900
runs: 3
expected_outcome: "Ativa o modo completo por pedido explícito, lê as referências do playbook em lotes registrando lido, parcial ou ausente, monta matriz de aplicabilidade por área (aplicável, não aplicável, não verificável, com justificativa), audita sem alterar o produto, não amplia permissões, rotula Verificado, Inferido e Não verificável e entrega relatório com achados, limitações e próximos passos."
model: sonnet
---
ECOMMERCE-COMPLETO: audite este repositório de loja. É só auditoria, não altere nada. Colei a descrição, a árvore e os arquivos principais porque você não tem acesso ao repositório.

Descrição: loja de cosméticos no Brasil, backend Node 20 com Express e Postgres, storefront em Next.js, pagamento por Stripe (cartão) e Mercado Pago (Pix), frete pelo Melhor Envio. Está em produção há 8 meses, ainda em modo de teste no Mercado Pago. Equipe de 3 pessoas. Não tenho CI nem testes automatizados.

```text
.
├── package.json
├── server.js
├── src/
│   ├── routes/checkout.js
│   ├── routes/webhooks.js
│   ├── services/stock.js
│   ├── services/shipping.js
│   └── db.js
├── scripts/importar-estoque.js
└── web/ (Next.js, páginas de produto e checkout)
```

```js
// server.js
app.use(express.json());
app.use('/api', require('./src/routes/checkout'));
app.use('/api/webhooks', require('./src/routes/webhooks'));

// src/routes/checkout.js (trecho)
router.post('/checkout', async (req, res) => {
  const { items, total, couponCode } = req.body;
  const order = await createOrder(req.session.userId, items, total, couponCode);
  const pix = await mp.createPixPayment({ amount: total, orderId: order.id });
  res.json({ orderId: order.id, qr: pix.qr_code });
});

// src/routes/webhooks.js (trecho)
router.post('/mercadopago', async (req, res) => {
  const { type, data } = req.body;
  if (type === 'payment') {
    await db.query("UPDATE orders SET status = 'paid' WHERE payment_id = $1", [data.id]);
    await require('../services/stock').decrement(data.id);
  }
  res.sendStatus(200);
});

// scripts/importar-estoque.js (trecho)
for (const row of planilha) {
  await db.query('UPDATE products SET stock = $1 WHERE sku = $2', [row.estoque, row.sku]);
}
```

Quero o relatório final com o que você leu, o que ficou fora, a cobertura por área e os achados priorizados.
