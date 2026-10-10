# Exemplos de testes de UI com Playwright (TypeScript)

Adaptado de `brains/qa/references/automacao-web.md` (brain-of-agent, MIT, conteúdo próprio do autor do plugin), com os princípios de V-20, V-21, V-41 e V-56. Domínio fictício de pedidos (`/api/pedidos`). Versões não verificadas por mim: confirme `npx playwright --version` e a API na documentação da versão instalada antes de copiar opções.

## Sumário

1. Configuração
2. Login uma vez (`storageState`)
3. Fixture, page object e teste de negócio
4. Mock de rede para estado difícil
5. Acessibilidade com axe por rota e estado
6. Regressão visual determinística
7. Teste de estabilidade e causas de intermitência
8. Antes e depois: teste frágil corrigido
9. Modelo de `MIGRATION_RULES.md`

## 1. Configuração

```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

const CI = !!process.env.CI;
const AUTH = 'playwright/.auth/usuario.json';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: CI,                 // test.only reprova no CI
  retries: CI ? 2 : 0,            // retry mostra o flaky no relatório; mais de 2 esconde defeito
  workers: CI ? 4 : undefined,
  reporter: CI ? [['blob'], ['github']] : [['html', { open: 'never' }]],
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    locale: 'pt-BR',
    timezoneId: 'America/Sao_Paulo',
    actionTimeout: 10_000,        // o padrão é sem limite: ação travada consome o teste inteiro
    trace: 'on-first-retry',      // CI; no diagnóstico de flaky use --trace=retain-on-failure
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    { name: 'chromium', use: { ...devices['Desktop Chrome'], storageState: AUTH }, dependencies: ['setup'] },
    { name: 'mobile', use: { ...devices['Pixel 7'], storageState: AUTH }, dependencies: ['setup'] },
  ],
  webServer: process.env.BASE_URL
    ? undefined
    : { command: 'npm run start', url: 'http://localhost:3000', reuseExistingServer: !CI },
});
```

`.gitignore`: `playwright/.auth/`, `test-results/`, `playwright-report/`, `blob-report/`. Escolha de navegadores pelos dados de acesso do produto; o WebKit do Playwright não é o Safari real.

## 2. Login uma vez (`storageState`)

```ts
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

setup('autentica o usuário de teste', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('E-mail').fill(process.env.E2E_USER!);      // variáveis fornecidas pelo usuário
  await page.getByLabel('Senha').fill(process.env.E2E_PASSWORD!);
  await page.getByRole('button', { name: 'Entrar' }).click();
  await expect(page.getByRole('heading', { name: 'Painel' })).toBeVisible();
  await page.context().storageState({ path: 'playwright/.auth/usuario.json' });
});
```

Login pela tela é testado em um teste próprio, não repetido em 300. Um arquivo de estado por perfil (`admin.json`, `cliente.json`). A conta de teste e as variáveis são do usuário; você nunca digita credenciais.

## 3. Fixture, page object e teste de negócio

```ts
// pages/pedido-page.ts
import type { Locator, Page } from '@playwright/test';

export class PedidoPage {
  readonly status: Locator;
  readonly aviso: Locator;
  private readonly dialogo: Locator;

  constructor(private readonly page: Page) {
    this.status = page.getByTestId('status-pedido');
    this.aviso = page.getByRole('status');
    this.dialogo = page.getByRole('dialog', { name: 'Cancelar pedido?' });
  }

  async abrir(id: string) {
    await this.page.goto(`/pedidos/${id}`);
  }

  async cancelar(motivo: string) {                 // método de intenção, não "clicarBotao"
    await this.page.getByRole('button', { name: 'Cancelar pedido' }).click();
    await this.dialogo.getByLabel('Motivo').selectOption(motivo);
    await this.dialogo.getByRole('button', { name: 'Confirmar cancelamento' }).click();
  }
}
```

```ts
// fixtures.ts
import { test as base, expect, request, type APIRequestContext } from '@playwright/test';
import { PedidoPage } from './pages/pedido-page';

type Pedido = { id: string; status: string };

export const test = base.extend<{ api: APIRequestContext; pedidoPendente: Pedido; pedidoPage: PedidoPage }>({
  api: async ({ baseURL }, use) => {
    const api = await request.newContext({
      baseURL,
      extraHTTPHeaders: { Authorization: `Bearer ${process.env.E2E_API_TOKEN}` },
    });
    await use(api);
    await api.dispose();
  },
  pedidoPendente: async ({ api }, use) => {
    const r = await api.post('/api/pedidos', { data: { itens: [{ sku: 'CAFE-250G', quantidade: 2 }], pagamento: 'BOLETO' } });
    expect(r.status(), await r.text()).toBe(201);
    const pedido = (await r.json()) as Pedido;
    await use(pedido);
    await api.delete(`/api/pedidos/${pedido.id}`);   // limpeza no teardown
  },
  pedidoPage: async ({ page }, use) => {
    await use(new PedidoPage(page));
  },
});
export { expect };
```

```ts
// tests/pedidos/cancelamento.spec.ts
import { test, expect } from '../../fixtures';

test('cancela pedido pendente e registra o status no back-end', async ({ page, api, pedidoPendente, pedidoPage }) => {
  await pedidoPage.abrir(pedidoPendente.id);

  // registre a espera ANTES da ação que dispara a resposta
  const cancelamento = page.waitForResponse(
    (r) => r.url().endsWith(`/api/pedidos/${pedidoPendente.id}/cancelamento`) && r.request().method() === 'POST',
  );
  await pedidoPage.cancelar('Desisti da compra');
  expect((await cancelamento).status()).toBe(200);

  await expect(pedidoPage.aviso).toHaveText('Pedido cancelado');
  await expect(pedidoPage.status).toHaveText('Cancelado');
  await expect                                       // estado fora da tela: expect.poll
    .poll(async () => (await (await api.get(`/api/pedidos/${pedidoPendente.id}`)).json()).status)
    .toBe('CANCELADO');
});
```

Asserções ficam no teste; o page object expõe locators. Rodar: `BASE_URL=https://hml.exemplo.com.br npx playwright test --project=chromium`. Variáveis exigidas: `E2E_USER`, `E2E_PASSWORD`, `E2E_API_TOKEN`.

## 4. Mock de rede para estado difícil

```ts
test('bloqueia a compra quando o cálculo de frete falha', async ({ page }) => {
  await page.route('**/api/frete**', (route) =>
    route.fulfill({ status: 503, json: { erro: 'indisponível' } }),
  );
  await page.goto('/carrinho');
  await page.getByLabel('CEP').fill('01310-100');
  await expect(page.getByRole('alert')).toHaveText('Não foi possível calcular o frete. Tente novamente.');
  await expect(page.getByRole('button', { name: 'Finalizar compra' })).toBeDisabled();
});
```

Use para 500, timeout, lista vazia, 10 mil itens, resposta lenta e terceiros fora do seu controle. Valide o formato contra o contrato real (OpenAPI). Bloqueie analytics e chat numa fixture automática; nunca o terceiro que está em teste.

## 5. Acessibilidade com axe por rota e estado

```ts
// tests/acessibilidade.spec.ts — pacote @axe-core/playwright (confirme nome e versão no npm)
import { test, expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']; // wcag22aa se a versão do axe listar

async function varrer(page: Page) {
  return (await new AxeBuilder({ page }).withTags(TAGS).analyze()).violations;
}
const resumo = (v: Awaited<ReturnType<typeof varrer>>) =>
  v.map((x) => `[${x.impact}] ${x.id}: ${x.help}\n  ${x.nodes.map((n) => n.target.join(' ')).join('\n  ')}`).join('\n');

for (const rota of ['/', '/login', '/cadastro']) {
  test(`sem violações WCAG 2.2 AA em ${rota}`, async ({ page }) => {
    await page.goto(rota);
    await expect(page.getByRole('main')).toBeVisible();   // conteúdo real, não o esqueleto de carregamento
    const violacoes = await varrer(page);
    expect(violacoes, resumo(violacoes)).toEqual([]);
  });
}

test('cadastro em estado de erro continua acessível', async ({ page }) => {
  await page.goto('/cadastro');
  await page.getByRole('button', { name: 'Criar conta' }).click();
  await expect(page.getByText('Informe seu e-mail')).toBeVisible();
  const violacoes = await varrer(page);
  expect(violacoes, resumo(violacoes)).toEqual([]);
});
```

axe-core é MPL-2.0: use o pacote, não copie o código. Em legado, congele as violações atuais como linha de base (regra mais seletor) e falhe só com violação nova, em vez de desligar regras.

## 6. Regressão visual determinística

```ts
test('resumo do pedido mantém a aparência', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 900 });         // viewport fixo
  await page.emulateMedia({ colorScheme: 'light', reducedMotion: 'reduce' });
  await page.goto('/pedidos/exemplo');                              // dados fixos (fixture ou mock)
  await page.evaluate(() => document.fonts.ready);                  // fontes carregadas
  await page.mouse.move(-1, -1);                                    // mouse fora, sem hover
  await expect(page.getByTestId('resumo-pedido')).toHaveScreenshot('resumo-pedido.png', {
    mask: [page.getByTestId('numero-pedido'), page.getByTestId('data-pedido')], // só o que muda a cada execução
    maxDiffPixelRatio: 0.01,                                        // tolerância explícita
  });
});
```

Baseline: gere e compare no mesmo ambiente do CI, com a mesma versão do pacote. O nome do arquivo inclui navegador e plataforma, então baseline gerada no Windows não vale no Linux. Com Docker (a tag da imagem acompanha a versão do Playwright; confira a lista de tags na documentação):

```bash
docker run --rm --ipc=host -v "$PWD":/work -w /work mcr.microsoft.com/playwright:v<VERSÃO>-noble npx playwright test tests/visual
```

Atualizar baseline (`--update-snapshots`) só pela regra do SKILL: abrir esperado, real e diff, classificar, pedir autorização.

## 7. Teste de estabilidade e causas de intermitência

```bash
npx playwright test tests/pedidos/cancelamento.spec.ts --repeat-each=30 --workers=1 --retries=0 --trace=retain-on-failure
npx playwright test tests/pedidos/cancelamento.spec.ts --repeat-each=10 --workers=4 --retries=0
```

| Causa | Sintoma | Correção |
| --- | --- | --- |
| Corrida clique x navegação | lê URL ou texto da página antiga | `await expect(page).toHaveURL(/\/pedidos\/\d+$/)` e ancore em algo exclusivo da nova página |
| Animação | "element intercepts pointer events" | espere o estado final (`await expect(dialogo).toBeHidden()`); `contextOptions: { reducedMotion: 'reduce' }` com o app respeitando `prefers-reduced-motion`; nunca `force: true` |
| Hidratação (SPA ou Next.js) | clique sem efeito, formulário faz GET nativo, `fill` apagado | botão desabilitado até hidratar (trecho abaixo); o auto-wait de "habilitado" resolve |
| Estado compartilhado | carrinho com itens de outro teste | dados por teste via fixture; conta por `testInfo.parallelIndex` |
| Dependência de ordem | passa na suíte, falha sozinho | cada teste cria seus dados; `mode: 'serial'` só para jornada de fato sequencial |
| Dados de outro teste | `toHaveCount(3)` vira 4 em paralelo | filtre pelo dado único que o teste criou |
| Relógio e fuso | falha perto da meia-noite ou só no CI (UTC) | `timezoneId: 'America/Sao_Paulo'` e `page.clock` (controla só o navegador, não o servidor) |
| Rede de terceiros | `goto` lento, widget de chat cobre o botão | bloqueie analytics e chat numa fixture automática |

```tsx
// App (Next.js ou React): só habilita depois de hidratar
const [hidratado, setHidratado] = useState(false);
useEffect(() => setHidratado(true), []);   // sincroniza com o ciclo de vida do navegador
return <button type="submit" disabled={!hidratado}>Entrar</button>;
```

Dado único e relógio fixo:

```ts
const nome = `Produto e2e ${randomUUID().slice(0, 8)}`;             // import { randomUUID } from 'node:crypto'
await expect(page.getByRole('row').filter({ hasText: nome })).toHaveCount(1);

await page.clock.setFixedTime(new Date('2026-03-31T23:59:30-03:00'));
await page.goto('/agenda');
await expect(page.getByRole('heading', { level: 1 })).toHaveText('31 de março de 2026');
```

## 8. Antes e depois: teste frágil corrigido

```ts
// Antes: espera fixa, posição, leitura única e formato de moeda
await page.waitForTimeout(3000);
await page.locator('.btn-primary').nth(2).click();
expect(await page.textContent('.total')).toBe('R$ 64,80');
```

```ts
// Depois: papel e nome, asserção que repete, esperado calculado
await page.getByRole('button', { name: 'Finalizar compra' }).click();
await expect(page.getByTestId('total')).toHaveText('R$ 64,80');   // normaliza o espaço não separável
```

Problemas removidos: sleep que esconde a condição real; `nth(2)` que quebra com nova ordenação; classe de estilo como seletor; leitura instantânea de `textContent()` que compara "Carregando..." quando a API demora; `toBe` com NBSP. Se o botão "Finalizar compra" casar com dois elementos, o locator estrito falha: resolva a ambiguidade pelo contexto (`getByRole('region', { name: 'Resumo' })`), não com `.first()`.

## 9. Modelo de `MIGRATION_RULES.md` (ideia de comunidade, V-40)

```markdown
# Regras de migração Cypress -> Playwright
1. Um spec por vez, lotes de 5 por sessão nova. Parar e perguntar ao encontrar helper que não está no mapa abaixo.
2. Mapa: cy.visit -> page.goto; cy.findByRole -> page.getByRole; cy.intercept(...).as + cy.wait -> page.waitForResponse registrado antes da ação; cy.session -> projeto setup + storageState.
3. Proibido: waitForTimeout, networkidle, force: true, nth() para desambiguar.
4. Aceite por spec: 3 execuções verdes (--repeat-each=3), teste de sanidade (quebrar o app de propósito e ver o teste falhar), diff visual quando houver captura.
5. Nenhum spec antigo é apagado antes de o novo passar em CI por 5 execuções.
```

Fonte: ideia de relato de comunidade (V-40, Classe C); documente e adapte, não automatize às cegas.
