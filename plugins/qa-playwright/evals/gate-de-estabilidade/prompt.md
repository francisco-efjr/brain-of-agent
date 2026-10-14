---
name: gate-de-estabilidade
description: "Caso de verificação: o usuário rodou o spec da F-03 uma vez, passou, e pede para marcar Passou na matriz. O spec colado tem espera por tempo e seletor posicional. Mede se o plugin recusa marcar, exige o gate de estabilidade (repeat-each 5 e shuffle com 2 workers) e a revisão por outro agente, e aponta os riscos de intermitência do spec."
tags: [qa-playwright, write-specs, stability-gate, verification]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 420
runs: 3
expected_outcome: "Recusa marcar Passou com uma única execução; exige o gate (--repeat-each=5 com --retries=0 e uma execução com --shuffle e --workers=2), a revisão do spec por outro agente e a execução de evidência, com o status gravado só pela etapa de relatório; aponta waitForTimeout e o seletor posicional como risco de intermitência; mantém a linha como não validada até o gate e não inventa resultado."
model: sonnet
---
Escrevi o spec da F-03 (criar tarefa), rodei uma vez e passou. Marca Passou na matriz, por favor, que eu preciso entregar o relatório.

```
$ npx playwright test --grep "F-03"
Running 1 test using 1 worker
  ✓  1 e2e/F-03-criar-tarefa.spec.ts:4:5 › F-03 criar tarefa @ui (2.1s)
  1 passed (3.4s)
```

```ts
import { test, expect } from '@playwright/test';

test('F-03 criar tarefa @ui', async ({ page }) => {
  await page.goto('/tarefas');
  await page.getByLabel('Nova tarefa').fill('Comprar pão');
  await page.getByRole('button', { name: 'Adicionar' }).click();
  await page.waitForTimeout(1500);
  await expect(page.getByTestId('item').first()).toBeVisible();
});
```

A linha da matriz hoje:

```
| F-03 | Não validado nesta rodada | — | e2e/F-03-criar-tarefa.spec.ts | — | — | — | — | — | — |
```
