---
name: idempotency-new-key-per-retry
description: "Mede se o plugin identifica que gerar uma Idempotency-Key nova a cada tentativa anula a idempotência, propõe chave por intenção persistida antes da chamada, trata timeout como estado desconhecido, cobre o cliente Android que reenvia e prova com contagem de linhas."
tags: [fintech-payments, payment-idempotency, payments]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta a chave nova por tentativa como causa da cobrança duplicada, propõe gerar a chave uma vez por intenção e persisti-la antes da chamada, reusar chave e corpo no retry, consultar o provedor após timeout, usar constraint de unicidade, tratar o reenvio pelo app Android e testar com contagem de linhas, sem afirmar ter executado nada."
model: sonnet
---
Meus clientes reclamam de cobrança duplicada quando o gateway dá timeout. Além do servidor, o app Android também reenvia o POST do checkout quando a rede cai e volta. Segue a função de cobrança do backend (Node). Corrija e me diga como provar que funciona.

```js
async function charge(order) {
  for (let i = 0; i < 3; i++) {
    try {
      return await psp.post('/charges', { amount: order.total, currency: 'BRL' },
        { headers: { 'Idempotency-Key': crypto.randomUUID() } });
    } catch (e) { if (e.code === 'ETIMEDOUT') continue; throw e; }
  }
}
```

Não tenho o repositório aberto aqui; use só o que escrevi.
