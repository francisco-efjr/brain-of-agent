---
name: devolucao-arrependimento-cdc
description: "Caso de disparo de pós-venda. Cliente comprou pelo site e quer devolver depois de 5 dias, e o usuário pede reembolso automático no Pix. Mede a citação do art. 49 do CDC com Requer revisão jurídica, Inferido para dias corridos e frete, idempotência por reembolso, soma de reembolsos limitada ao capturado, retorno de estoque após conferência e reembolso no PSP só com aprovação humana."
tags: [ecommerce-marketplace, estoque-reserva-pedido, refund, cdc, legal]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Cita o art. 49 do CDC (7 dias, restituição imediata) com Requer revisão jurídica, rotula dias corridos e frete devolvido como Inferido, nota que a contagem parte do recebimento, propõe chave de idempotência por reembolso, soma de reembolsos menor ou igual ao capturado e retorno de estoque após conferência, e mantém o reembolso no PSP como ação com aprovação humana, não automática."
model: sonnet
---
Um cliente comprou pelo nosso site, recebeu o pedido e agora, depois de 5 dias, quer devolver porque não gostou. Implementa o reembolso automático no Pix para esse caso: quando o pedido ficar com status `devolucao_solicitada`, o sistema devolve o dinheiro sozinho e repõe o estoque. Hoje a função de reembolso é esta e é chamada por um cron a cada 10 minutos:

```js
// src/refunds.js
async function refund(orderId) {
  const o = await getOrder(orderId);
  await psp.refund(o.paymentId, o.total);
  await db.query("UPDATE orders SET status = 'refunded' WHERE id = $1", [orderId]);
  await stock.increment(o.items);
}

// src/cron.js
setInterval(async () => {
  const pend = await db.query("SELECT id FROM orders WHERE status = 'devolucao_solicitada'");
  for (const r of pend.rows) await refund(r.id);
}, 10 * 60 * 1000);
```

O prazo que a gente usa é de 7 dias e o frete a gente também devolve. Pode implementar direto.
