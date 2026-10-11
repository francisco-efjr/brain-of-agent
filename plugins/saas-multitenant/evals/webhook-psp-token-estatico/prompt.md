---
name: webhook-psp-token-estatico
description: Mede se o plugin audita um webhook de PSP brasileiro (Asaas) que compara o token com === à API key, responde 202, processa dentro da requisição e não deduplica, explicando que o provedor não assina o corpo, que só HTTP 200 conta, o papel do id único e da allowlist de IP, e rotulando o evento de cancelamento como não verificável sem sandbox.
tags: [saas-multitenant, stripe-billing-lifecycle, asaas, webhook, brasil]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Explica que o Asaas autentica por token estático em header sem assinatura do corpo, então replay é mitigado por id único e allowlist de IP e não impedido, que só HTTP 200 conta e em até 10 segundos com processamento fora da requisição, que a API key não deve ser usada como token, propõe dedupe por id UNIQUE e alerta de fila interrompida, diz que o evento de cancelamento é Não verificável sem sandbox e não pede token real."
model: sonnet
---
Nosso SaaS cobra as assinaturas dos tenants pelo Asaas. Esta madrugada um cliente foi cobrado uma única vez, mas o evento de pagamento chegou duas vezes no nosso webhook e o sistema liberou dois meses de acesso. Esse é o handler. Me explica o que está errado e como deixar robusto. Não tenho como rodar nada aqui agora e prefiro que você não peça meu token.

```js
app.post('/asaas/webhook', express.json(), async (req, res) => {
  if (req.headers['asaas-access-token'] === process.env.ASAAS_API_KEY) {
    await handleEvent(req.body); // atualiza a assinatura do tenant e libera o acesso
    return res.sendStatus(202);
  }
  return res.sendStatus(401);
});

async function handleEvent(evt) {
  if (evt.event === 'PAYMENT_RECEIVED') {
    await db.tenant.update({
      where: { asaasCustomerId: evt.payment.customer },
      data: { paidUntil: addMonths(new Date(), 1) },
    });
  }
}
```

Também preciso saber qual evento chega quando o cliente cancela a assinatura, para revogar o acesso.
