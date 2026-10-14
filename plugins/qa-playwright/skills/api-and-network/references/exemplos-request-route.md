# Exemplos: `request`, `route` e `clock`

Trechos de redação própria para o sistema-demo de tarefas (dados sintéticos). Nomes de campos, códigos de status e textos de aviso do demo **não estão verificados**: só `/api/tarefas`, o `DELETE 200` (X-20) e o mock 500 (X-12) vêm de execução. Confira os valores reais na fonte de verdade antes de assertar. As assinaturas valem para o Playwright 1.64 (V-51, V-52, V-53); confirme na versão fixada.

## 1. Padrão híbrido: dado via API, ação na UI, verificação via API

```ts
import { test, expect } from './fixtures';

test.describe('F-08 Tarefas pela API refletem a UI @ui', () => {   // híbrido com `page`: @ui; @api fica para spec só com `request`
  test('feliz: tarefa criada pela API aparece na UI e some depois de excluída', async ({ page, request }, testInfo) => {
    const titulo = `Tarefa API ${testInfo.testId.slice(-8)}`;      // dado único por teste (V-33)

    // Dado via API (o formato do corpo e o status vêm da fonte de verdade)
    const criada = await request.post('/api/tarefas', { data: { titulo } });
    expect(criada.ok()).toBeTruthy();

    // Ação na UI
    await page.goto('/tarefas');
    const item = page.getByRole('listitem').filter({ hasText: titulo });
    await expect(item).toHaveCount(1);
    await item.getByRole('button', { name: 'Excluir' }).click();
    await expect(item).toHaveCount(0);

    // Verificação via API
    const lista = await request.get('/api/tarefas');
    expect(JSON.stringify(await lista.json())).not.toContain(titulo);
  });
});
```

Se o `baseURL` tiver caminho (por exemplo `http://127.0.0.1:4174/api/v1/`), escreva `request.get('tarefas')`, sem `/` inicial: com `/` o caminho substitui o prefixo.

## 2. Erro 500 no servidor (mock realista)

```ts
test('F-06 erro 500 ao adicionar: avisa e não mostra o item @ui', async ({ page, app }) => {
  // Registrar a rota ANTES da ação que dispara a requisição
  await page.route('**/api/tarefas', async (route) => {
    if (route.request().method() === 'POST') {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ erro: 'falha' }),
      });
    } else {
      await route.fallback();            // GET segue para o servidor real
    }
  });
  await app.abrir('/tarefas');
  const antes = await page.getByRole('listitem').count();
  await page.getByRole('textbox', { name: 'Nova tarefa' }).fill('Comprar pão');
  await page.getByRole('button', { name: 'Adicionar' }).click();
  await expect(page.getByRole('alert')).toBeVisible();                 // texto do aviso: conferir na fonte
  await expect(page.getByRole('listitem')).toHaveCount(antes);
});
```

O mesmo cenário na exploração, pela CLI (X-12):

```bash
npx playwright cli -s=F-06 route "**/api/tarefas" --status 500 --body '{"erro":"falha"}'
npx playwright cli -s=F-06 route-list
npx playwright cli -s=F-06 unroute
```

## 3. Alterar a resposta real, abortar e simular timeout

```ts
// Alterar: a resposta real mais um item extra
await page.route('**/api/tarefas', async (route) => {
  const resposta = await route.fetch();
  const itens = await resposta.json();
  await route.fulfill({ response: resposta, json: [...itens, { id: 999, titulo: 'Extra de teste' }] });
});

// Bloquear o recurso
await page.route('**/api/tarefas', (route) => route.abort());

// Simular timeout de rede
await page.route('**/api/tarefas', (route) => route.abort('timedout'));
```

Após cada cenário de falha, confira o **efeito** (lista intacta, aviso visível, contador coerente), não só que o erro apareceu.

## 4. Offline e reconexão

```ts
test('F-06 offline: avisa e recupera ao reconectar @ui', async ({ page, context, app }) => {
  await app.abrir('/tarefas');
  await context.setOffline(true);
  await page.getByRole('textbox', { name: 'Nova tarefa' }).fill('Comprar pão');
  await page.getByRole('button', { name: 'Adicionar' }).click();
  await expect(page.getByRole('alert')).toBeVisible();
  await context.setOffline(false);
  // Em seguida: repetir a ação e afirmar o efeito (item adicionado, contador somado)
});
```

Na CLI: `network-state-set offline` e `network-state-set online` (X-13). Em PWA com service worker, o SW pode servir cache: combine `offline` com cuidado (V-63).

## 5. Tempo: sessão que expira, sem esperar

```ts
test('F-03 sessão expira depois de 30 min @ui', async ({ page }) => {
  await page.clock.install({ time: new Date('2026-01-15T09:00:00') });   // primeira chamada de clock
  await page.goto('/painel');
  await page.clock.fastForward('30:00');
  await expect(page).toHaveURL(/\/login/);
});
```

`install` precisa ser a primeira chamada de clock (V-53). Use `setFixedTime` para data fixa e `pauseAt` com `runFor` para tick controlado. O clock sobrescreve `Date`, timers e `requestAnimationFrame`: pode afetar biblioteca de animação. A rota `/painel`, o redirecionamento e o prazo de 30 minutos são de exemplo.

## 6. Observação de rede sem mock

```ts
const resposta = page.waitForResponse((r) => r.url().includes('/api/tarefas') && r.request().method() === 'DELETE');
await item.getByRole('button', { name: 'Excluir' }).click();     // a espera nasce ANTES da ação
expect((await resposta).status()).toBe(200);
```

A espera é registrada antes do clique: registrar depois perde o evento (V-59).

## 7. Limites que ficam fora

Contrato (Pact), schema OpenAPI e carga (k6) não são do Playwright (V-51): use `backend-api:api-test-suite`. HAR guarda cabeçalhos e tokens: remova antes de commitar.
