---
name: cupom-percentual-fixo-arredondamento
description: "Caso de disparo de preços e promoções. Cupom percentual e cupom fixo cumulativos, item fora da promoção, frete grátis com limite e parcelamento, com cálculo em float no front. Mede cálculo no servidor, inteiros em centavos, ordem explícita com os dois resultados, limite do frete antes ou depois do desconto e parcelas que somam o total."
tags: [ecommerce-marketplace, precos-promocoes, rounding, coupon, float]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Move o cálculo para o servidor com inteiros em centavos, explicita a ordem percentual versus fixo mostrando 164,00 e 166,00 para o exemplo, define se o limite do frete grátis é medido antes ou depois do desconto, rateia o desconto com soma igual ao total, parcela em 3x somando o total com regra de resto rotulada como decisão de projeto, e propõe testes parametrizados com oráculo independente."
model: sonnet
---
Preciso implementar o cálculo do carrinho no meu endpoint `/cart/price`. As regras que o pessoal de marketing passou:

- Dois cupons cumulativos: `PRIMEIRA10` (10%) e `VALE20` (R$ 20,00 fixos). Os dois valem só para os itens que participam da promoção.
- Frete grátis em compras acima de R$ 170,00 (o frete normal é R$ 24,90).
- Parcelamento em até 3x sem juros.

Exemplo real: carrinho com o item A (R$ 100,00), o item B (R$ 60,00) e o item C (R$ 40,00, em liquidação, fora da promoção). Cliente aplica os dois cupons e escolhe 3x.

Hoje o cálculo está no front e o servidor só confia no número que chega:

```js
// front: cart.js
function calc(items, coupons) {
  let subtotal = items.reduce((s, i) => s + i.price * i.qty, 0);
  if (coupons.includes('PRIMEIRA10')) subtotal = subtotal * 0.9;
  if (coupons.includes('VALE20')) subtotal = subtotal - 20;
  const frete = subtotal > 170 ? 0 : 24.9;
  return { subtotal, frete, total: subtotal + frete, parcela: (subtotal + frete) / 3 };
}

// server: routes/cart.js
router.post('/cart/price', (req, res) => {
  res.json(req.body.pricing); // confia no que o front calculou
});
```

Implementa o cálculo certo no servidor e escreve os testes.
