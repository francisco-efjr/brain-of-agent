---
name: idempotencia-pagamento
description: Mede se o plugin diagnostica cobrança duplicada por retry de cliente mobile e propõe idempotência atômica no banco, com política de códigos declarada, testes de concorrência e migração apenas proposta, sem afirmar execução.
tags: [backend-api, idempotency-and-resilience, mobile]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Explica a causa (retry após timeout com operação já aceita), propõe chave de idempotência com escopo, hash do corpo, resposta persistida e restrição única no banco, define replay, corpo divergente, em processamento e ausente, trata o gateway, lista teste de concorrência, propõe a migração sem executar e diz o que não executou."
model: sonnet
---
Nosso `POST /payments` (Express + Postgres) cobrou duas vezes quando o app mobile tentou de novo depois de um timeout. Os apps Android e iOS reenviam a mesma requisição se não recebem resposta em 10 segundos. Código atual:

```js
app.post('/payments', async (req, res) => {
  const p = await db.query(
    'insert into payments(user_id, amount) values($1, $2) returning *',
    [req.user.id, req.body.amount]
  );
  await gateway.charge(p.rows[0]);
  res.status(201).json(p.rows[0]);
});
```

Corrija para isso não acontecer de novo. Não tenho o repositório aberto aqui; use só o que escrevi.
