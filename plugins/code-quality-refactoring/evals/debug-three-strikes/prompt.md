---
name: debug-three-strikes
description: "Mede a escalada da depuração: depois de três correções que só mascararam o sintoma, o agente deve parar, resumir o que cada tentativa revelou, propor hipótese testável ou instrumentação e oferecer opções, sem empilhar uma quarta correção às cegas."
tags: [code-quality-refactoring, debug-causa-raiz, escalation]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Para antes de uma quarta correção, resume o que as três tentativas mostraram (mascaram o sintoma), recomenda desfazer os remendos, formula hipótese com comando que a confirma ou instrumentação e apresenta opções ao usuário."
model: sonnet
---
Tenho um 500 intermitente no `POST /orders` do nosso app Express e já tentei três correções sem sucesso. Tenta mais uma, por favor.

Erro original no log (acontece em umas 40% das requisições logo depois do login):

```text
TypeError: Cannot read properties of undefined (reading 'id')
    at /app/routes/orders.js:41:38
```

`routes/orders.js` (original):

```js
router.post('/orders', async (req, res) => {
  const userId = req.session.user.id;            // linha 41
  const order = await Order.create({ userId, items: req.body.items });
  res.status(201).json(order);
});
```

O que eu já tentei:
1. Troquei por `req.session?.user?.id`. O 500 mudou para `null value in column "user_id" violates not-null constraint`.
2. Envolvi tudo em try/catch e passei a devolver `200 { ok: false }`. Os clientes agora reclamam que pedidos "somem" e o log não mostra mais erro nenhum.
3. Coloquei retry de 3 tentativas em volta do `Order.create`. Mesmo erro, só que 3 vezes mais lento.

Contexto: em produção rodamos 2 réplicas do container atrás de um balanceador round-robin. Trecho do `app.js`:

```js
app.use(session({ secret: process.env.SESSION_SECRET, resave: false, saveUninitialized: false }));
```
