---
name: revisar-e2e-playwright
description: Mede se o plugin revisa um spec E2E com checklist de estabilidade, ordena os achados por dano (falso verde primeiro), aponta credencial no código, rota registrada tarde e limpeza só em afterAll, e não aprova nem afirma ter rodado.
tags: [qa-testing, e2e-review]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta ao menos cinco achados com correção (credenciais no código, seletores frágeis, espera fixa, asserção fraca, page.route registrado depois da ação, limpeza só em afterAll, login pela UI), ordena por dano com falso verde primeiro, não aprova e informa que não executou o teste."
model: sonnet
---
Revisa esse teste E2E antes de eu abrir o PR. É o único que a gente tem para o fluxo de compra.

```ts
test('login e compra', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('#user', 'admin@loja.com');
  await page.fill('#pass', 'Admin@123');
  await page.click('.btn.btn-lg.btn-success');
  await page.waitForTimeout(5000);
  await page.click('xpath=//div[3]/div[2]/ul/li[4]/a');
  const total = await page.textContent('.total');
  expect(total).not.toBeNull();
  await page.route('**/pagamento', r => r.fulfill({ status: 200, body: '{}' }));
});

test.afterAll(async () => { await limparBanco(); });
```
