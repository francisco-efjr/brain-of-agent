---
name: flaky-causa-e-correcao
description: Mede se o plugin diagnostica um spec de Playwright intermitente pela causa (espera fixa, dependência entre testes, seletor frágil, asserção sem espera) e recusa a correção cosmética de subir retries.
tags: [qa-testing, flaky-triage]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Identifica ao menos três causas (espera fixa, dependência de ordem via variável compartilhada, seletor frágil, isVisible sem espera), diz que retries mascara o problema, propõe medir a taxa antes e depois com repetição, propõe correções concretas, oferece quarentena com ticket, dono e prazo e declara que não executou nada."
model: sonnet
---
Esse spec do Playwright passa no meu notebook e falha umas 2 a cada 10 vezes no CI. Já coloquei `retries: 3` e continua instável. O que eu faço?

```ts
import { test, expect } from '@playwright/test';

let pedidoId: string;

test('cria pedido', async ({ page }) => {
  await page.goto('https://loja.exemplo.test/checkout');
  await page.locator('div.btn-primary:nth-child(3)').click();
  await page.waitForTimeout(3000);
  pedidoId = await page.locator('.order-id').innerText();
  expect(await page.locator('.success').isVisible()).toBe(true);
});

test('mostra o pedido no histórico', async ({ page }) => {
  await page.goto(`https://loja.exemplo.test/pedidos/${pedidoId}`);
  await expect(page.locator('.status')).toHaveText('Pago');
});
```
