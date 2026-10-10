---
name: resiliencia-webhook-pagamento
description: Mede se o plugin identifica dual write, propõe outbox com consumidor idempotente, limita o retry a uma camada com jitter e evita prometer exactly-once.
tags: [architecture-design, resilience, outbox, idempotency]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Identifica a janela entre gravar o pedido e publicar o evento, propõe outbox na mesma transação e consumidor idempotente com chave estável, retry em uma só camada com jitter, e testes de duplicata, queda após commit e timeout, sem prometer exactly-once."
model: sonnet
---
Estamos com pedidos de envio duplicados e, em outros casos, pedidos pagos que nunca geram envio. Segue o código simplificado dos dois serviços (TypeScript). O cliente HTTP do serviço de envio já tem retry(3) embutido no SDK.

```ts
// payments/webhook-handler.ts
export async function handlePaymentWebhook(req: Request) {
  const evt = await req.json();
  await retry(5, async () => {
    await db.orders.update({ id: evt.orderId }, { status: 'PAID' });
    await broker.publish('order.paid', { orderId: evt.orderId, correlationId: evt.correlationId });
  });
  return new Response('ok');
}

// shipping/consumer.ts
export async function onOrderPaid(msg: { orderId: string; correlationId: string }) {
  await retry(5, () => shippingClient.createShipment(msg.orderId));
  seenIds.add(msg.correlationId); // Set em memória do processo
}
```

O gateway de pagamento reenvia o webhook quando não recebe 200 em 5 segundos. O broker entrega pelo menos uma vez. Como a gente corrige isso direito?
