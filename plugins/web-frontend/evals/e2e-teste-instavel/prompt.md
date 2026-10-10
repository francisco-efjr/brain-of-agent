---
name: e2e-teste-instavel
description: Mede se o plugin estabiliza um teste Playwright instável trocando seletores por papel e rótulo, removendo sleep e networkidle, usando asserção web-first, propondo diagnóstico com repetição e trace e recusando aumentar retries ou usar force.
tags: [web-frontend, e2e-tests, playwright, flaky, locators]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Reescreve com getByLabel e getByRole por nome, sem waitForTimeout nem networkidle, com expect web-first sobre o total, explica por que nth e toBe sobre textContent são frágeis (incluindo o espaço não separável da moeda), propõe repeat-each, workers=1 e trace retain-on-failure e não aumenta retries nem usa force."
model: sonnet
---
Este teste de Playwright falha mais ou menos uma vez a cada cinco execuções no CI e eu já estava aumentando os retries. Arruma pra mim? A causa que eu conheço: o botão "Atualizar frete" só aparece depois que o CEP carrega, então a ordem dos botões muda.

```ts
// e2e/carrinho.spec.ts
import { test, expect } from '@playwright/test';

test('aplica cupom e mostra o total', async ({ page }) => {
  await page.goto('/carrinho');
  await page.waitForLoadState('networkidle');
  await page.fill('#cupom', 'CAFE10');
  await page.locator('.btn-primary').nth(1).click();
  await page.waitForTimeout(3000);
  expect(await page.textContent('.total')).toBe('R$ 64,80');
});
```

```html
<!-- trecho da página /carrinho -->
<main>
  <h1>Carrinho</h1>
  <button class="btn-primary" type="button">Atualizar frete</button> <!-- só aparece após o CEP carregar -->
  <label for="cupom">Cupom</label>
  <input id="cupom" name="cupom">
  <button class="btn-primary" type="button">Aplicar cupom</button>
  <button class="btn-primary" type="button">Finalizar compra</button>
  <p>Total: <strong class="total">R$ 64,80</strong></p>
</main>
```
