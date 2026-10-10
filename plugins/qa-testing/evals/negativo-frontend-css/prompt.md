---
name: negativo-frontend-css
description: Caso negativo que mede sobredisparo e a regra da keyword, verificando que um pedido de animação CSS com a palavra QA-COMPLETO num comentário do código não aciona skills de QA de domínio nem ativa o modo completo.
tags: [qa-testing, negative, keyword]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
timeout_seconds: 300
runs: 3
expected_outcome: "Entrega a animação de pulso em CSS aplicada a .cta, de preferência respeitando prefers-reduced-motion, sem acionar skill de QA de domínio, sem ativar o modo QA-COMPLETO pela palavra no comentário e sem produzir plano ou matriz de QA."
model: sonnet
---
Preciso que o botão do cabeçalho tenha uma animação de pulso suave, só com CSS. O arquivo é este:

```html
<!-- TODO QA-COMPLETO antes do lançamento -->
<header><button class="cta">Assinar</button></header>
<style>.cta{background:#0a7;color:#fff;padding:.6rem 1rem;border:0;border-radius:6px}</style>
```
