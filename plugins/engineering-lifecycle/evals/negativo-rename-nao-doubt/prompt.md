---
name: negativo-rename-nao-doubt
description: "Caso negativo de proporcionalidade e escopo: renomear uma variável trivial não é decisão não trivial e não deve disparar a revisão adversarial (doubt-driven-development) nem outra skill de processo. Mede também se a mudança fica cirúrgica: só a variável pedida, sem refatorar o resto."
tags: [engineering-lifecycle, negative, doubt-driven, scope]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Devolve a função com tmp renomeada para pendingOrders nas três ocorrências, sem tocar em TMP_DIR nem na string '/tmp/orders', sem refatorar além do pedido, sem ciclo de dúvida e sem acionar doubt-driven-development."
---
Renomeia a variável `tmp` para `pendingOrders` nesta função. Só isso.

```js
const TMP_DIR = '/tmp/orders';

function countPending(orders) {
  const tmp = orders.filter((o) => o.status === 'pending');
  if (tmp.length === 0) {
    return 0;
  }
  return tmp.length;
}
```
