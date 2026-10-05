# Automação web e E2E

Como escolher a ferramenta, escrever, estabilizar e revisar testes de navegador
(Playwright, Cypress, Selenium, WebdriverIO). Leia ao criar ou revisar suíte
E2E, page objects ou ao investigar teste intermitente. Versões de referência:
Playwright 1.63, Cypress 16, Selenium 4.50, WebdriverIO 9 (outubro de 2026).

## Sumário
- [Escolha de ferramenta](#escolha-de-ferramenta)
- [Estrutura de projeto](#estrutura-de-projeto)
- [Localizadores](#localizadores)
- [Esperas e asserções web-first](#esperas-e-asserções-web-first)
- [Isolamento, login e dados](#isolamento-login-e-dados)
- [Fixtures, Page Objects e componentes](#fixtures-page-objects-e-componentes)
- [Mock de rede](#mock-de-rede)
- [Asserções significativas e soft assertions](#asserções-significativas-e-soft-assertions)
- [Regressão visual](#regressão-visual)
- [Depuração](#depuração)
- [Paralelismo, sharding, retries e timeouts](#paralelismo-sharding-retries-e-timeouts)
- [Teste intermitente: diagnóstico e causas](#teste-intermitente-diagnóstico-e-causas)
- [Exemplo completo em Playwright TypeScript](#exemplo-completo-em-playwright-typescript)
- [Exemplo em Playwright Python](#exemplo-em-playwright-python)
- [Cypress: exemplo e armadilhas](#cypress-exemplo-e-armadilhas)
- [Selenium 4](#selenium-4)
- [Emulação mobile e matriz de navegadores](#emulação-mobile-e-matriz-de-navegadores)
- [Teste de componente](#teste-de-componente)
- [Revisão de PR de testes E2E](#revisão-de-pr-de-testes-e2e)

## Escolha de ferramenta

| Critério | Playwright | Cypress | Selenium 4 | WebdriverIO 9 |
| --- | --- | --- | --- | --- |
| Linguagens | TS/JS, Python, Java, .NET | só JS/TS | Java, Python, C#, Ruby, JS | só JS/TS |
| Navegadores | Chromium, Chrome/Edge (`channel`), Firefox e WebKit em builds próprios | Chrome, Edge, Firefox; WebKit experimental; Electron obsoleto | qualquer um com driver, inclusive Safari real | os do WebDriver/BiDi + apps nativos via Appium |
| Multi-aba e multi-origem | nativo | uma aba (abas só via plugin); outra origem com `cy.origin` | nativo (troca de janela) | nativo |
| iframes | nativo (`frameLocator`, `contentFrame()`) | limitado: mesma origem consulta, sem comando de "entrar" | `switch_to.frame` | `switchFrame` |
| Espera | auto-wait em ações + asserções que repetem | queries e asserções repetem; ações não | manual (`WebDriverWait`) | auto-wait em comandos + `expect-webdriverio` |
| Paralelismo | workers e sharding nativos e gratuitos | balanceamento oficial no Cypress Cloud (pago); fora dele, divisão manual ou plugin | Grid ou runner da linguagem | nativo (`maxInstances`) |
| Diferenciais | trace viewer, UI mode, teste de API no mesmo runner, visual | time-travel no runner, teste de componente maduro | maior base instalada, Grid, Safari real | mesma API para web e mobile |
| Vence quando | projeto novo, sem restrição forte | time JS de front que quer DX e teste de componente | time Java/C#, Grid existente, Safari real obrigatório | uma suíte JS cobrindo web e app nativo |

- O WebKit do Playwright não é o Safari. Fluxo crítico para iPhone (e todo
  navegador de iOS no Brasil roda WebKit) precisa de Safari real em
  dispositivo ou nuvem antes do release.
- Migrar suíte estável só por moda raramente se paga. Migre quando a dor
  (intermitência, tempo de CI, falta de multi-aba) custa mais que reescrever.

## Estrutura de projeto

```text
e2e/                                   # TypeScript
├── playwright.config.ts
├── fixtures.ts             # test.extend: api, dados, page objects
├── pages/                  # page objects e componentes (cabecalho, tabela)
├── support/                # clientes de API e fábricas de dados
├── tests/
│   ├── auth.setup.ts       # login uma vez → playwright/.auth/*.json
│   └── pedidos/cancelamento.spec.ts
└── playwright/.auth/       # no .gitignore: guarda cookies de sessão
```

```text
e2e/                                   # Python (pytest-playwright)
├── pytest.ini              # addopts com --base-url, --tracing etc.
├── conftest.py             # estado autenticado, api, dados
├── pages/pedido_page.py
└── tests/test_cancelamento_pedido.py
```

Organize testes por capacidade de negócio (pedidos, pagamento), não por tela.
URL, usuário e token vêm de variável de ambiente; nada de `config.prod.ts`
com segredo versionado.

## Localizadores

| Ordem | Playwright | Use para |
| --- | --- | --- |
| 1 | `getByRole('button', { name: 'Finalizar compra' })` | quase tudo; se não encontra, provavelmente há defeito de acessibilidade |
| 2 | `getByLabel('CPF')` | campos de formulário |
| 3 | `getByPlaceholder('00000-000')` | só sem rótulo (e falta de rótulo é bug) |
| 4 | `getByText('Pedido cancelado')` | conteúdo não interativo |
| 5 | `getByTestId('status-pedido')` | sem semântica estável: célula, gráfico, texto traduzido |

```ts
// Encadeie e filtre para chegar ao elemento pelo contexto, não pela posição
const linha = page.getByRole('row').filter({ hasText: 'CAFE-250G' });
await linha.getByRole('button', { name: 'Remover' }).click();
page.getByRole('listitem').filter({ has: page.getByRole('heading', { name: 'Plano Pro' }) });
page.getByRole('button', { name: 'Salvar', exact: true }); // não casa "Salvar rascunho"
page.getByRole('link').filter({ visible: true });          // 1.51+; na 1.63 também locator.visible()
```

- Locator do Playwright é estrito: ação em locator que casa dois elementos
  falha. É um aviso de ambiguidade; corrigir com `.first()` esconde o problema.
- Evite `nth()`/`first()` (a ordem muda com ordenação e dados novos), XPath
  absoluto (quebra com qualquer `div` a mais), classes geradas (`.css-1x2y3z`,
  `.sc-bdVaJa`, utilitárias do Tailwind) e IDs gerados (`:r5:`,
  `#react-select-3-input`).
- Suíte que roda em vários idiomas: texto quebra; use `data-testid` ou leia
  as strings do mesmo arquivo de i18n do app.
- Cypress: `cy.findByRole('button', { name: 'Finalizar compra' })` com
  `@testing-library/cypress`; senão `cy.get('[data-cy=status-pedido]')` ou
  `cy.contains('button', 'Finalizar compra')`.
- Selenium não localiza por papel: prefira `By.ID`, `By.NAME` e
  `By.CSS_SELECTOR, "[data-testid='status-pedido']"`; XPath relativo por texto
  (`//button[normalize-space()='Finalizar compra']`) só quando não houver
  alternativa. `element.accessible_name` e `aria_role` servem para verificar
  acessibilidade.

## Esperas e asserções web-first

Antes de agir, o Playwright espera o elemento estar anexado, visível,
estável (sem animar), recebendo eventos (sem sobreposição) e habilitado. Ele
não sabe se *seus dados* chegaram — isso é papel da asserção.

```ts
// Frágil: lê uma vez; se a API não respondeu, compara "Carregando…"
expect(await page.getByTestId('total').textContent()).toBe('R$ 64,80');
// Robusto: repete até bater ou estourar o timeout do expect (5 s por padrão)
await expect(page.getByTestId('total')).toHaveText('R$ 64,80');

// Espere a resposta registrando ANTES da ação que a dispara
const resposta = page.waitForResponse(
  (r) => r.url().includes('/api/pedidos') && r.request().method() === 'POST',
);
await page.getByRole('button', { name: 'Finalizar compra' }).click();
expect((await resposta).status()).toBe(201);

// Estado fora da tela (fila, e-mail, back-end assíncrono): expect.poll
await expect
  .poll(async () => (await (await api.get(`/api/pedidos/${id}`)).json()).status, {
    timeout: 15_000,
  })
  .toBe('PAGO');
```

- `isVisible()`, `textContent()`, `count()` e `page.url()` são instantâneos;
  dentro de `expect(...)` comum viram corrida. Prefira `toBeVisible`,
  `toHaveText`, `toHaveCount`, `toHaveURL`, `toHaveValue`, `toBeEnabled`.
- `Intl` formata `R$ 64,80` com espaço não separável (U+00A0). `toHaveText`
  com string normaliza espaços; `toBe` sobre `textContent()` falha.
- `waitForTimeout`/`sleep` é anti-padrão duplo: lento quando o sistema está
  rápido e insuficiente quando está lento. Esconde a condição real que o
  teste deveria esperar. Também evite `waitForLoadState('networkidle')`: o
  Playwright o desaconselha e polling ou analytics o tornam imprevisível.

## Isolamento, login e dados

- **Contexto por teste.** Cada teste do Playwright recebe um contexto novo
  (cookies, storage e cache limpos) em milissegundos. Não reaproveite `page`
  entre testes com `beforeAll`.
- **Login uma vez.** Um projeto `setup` faz login pela tela e salva
  `storageState`; os demais projetos dependem dele e já começam logados. Um
  arquivo por perfil (`admin.json`, `cliente.json`). Login pela tela é testado
  em um teste próprio, não repetido em 300.
- **Dados via API por teste.** Cada teste cria o que precisa (pedido, usuário)
  por API ou fábrica, com valor único, e limpa no teardown da fixture. Massa
  compartilhada é a causa nº 1 de falha que só acontece em paralelo.
- **Conta por worker** quando criar usuário é caro: use
  `testInfo.parallelIndex` (estável entre reinícios de worker) para escolher
  `e2e+0@…`, `e2e+1@…`. `workerIndex` muda quando o worker reinicia.
- **Recurso global** (configuração da conta, feature flag): na 1.63, testes
  com o mesmo `lock` nunca rodam juntos — `test('…', { lock: 'config-loja' }, …)`.

## Fixtures, Page Objects e componentes

Fixture (`test.extend`) entrega a cada teste exatamente o que ele declara, com
preparo e limpeza no mesmo lugar e composição por dependência (ver exemplo
completo). Escopo `worker` para o que é caro e pode ser compartilhado com
segurança; `{ auto: true }` para o que todo teste deve ter (bloquear
terceiros, coletar log).

Page Object bem feito:
- **Métodos de intenção**: `cancelar(motivo)`, não `clicarBotaoCancelar()`.
  O teste lê como a regra; a mecânica muda num lugar só.
- **Seletores em um lugar**, criados no construtor (locators são preguiçosos:
  não consultam o DOM até o uso).
- **Asserções no teste.** O page object expõe locators somente leitura para
  o teste verificar; esconder `expect` dentro dele oculta o que o teste prova.
- **Componentes** para partes repetidas (tabela, seletor de data, cabeçalho),
  recebendo um `Locator` raiz para que duas tabelas na mesma tela não colidam.
- Evite página-base com 50 métodos, herança em cadeia, `if` por ambiente e
  espera fixa dentro de método.

Screenplay (Serenity/JS, Serenity BDD) modela atores com habilidades que
executam tarefas e fazem perguntas. Compensa em suítes grandes com muitos
perfis e canais (web, API, mobile); para a maioria dos times, fixtures + page
objects bastam e custam menos abstração.

## Mock de rede

Use para estados difíceis de produzir (500, timeout, lista vazia, 10 mil
itens, resposta lenta para ver o carregamento), terceiros fora do seu
controle (frete, mapa) e telas de teste visual determinístico.

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
// Alterar a resposta real: const r = await route.fetch(); await route.fulfill({ response: r, json: {...} })
// HAR: await page.routeFromHAR('hars/catalogo.har', { url: '**/api/catalogo/**', update: false })
```

Perigos: mock que diverge do contrato real deixa a suíte verde e produção
quebrada — valide o formato contra OpenAPI ou contrato (ver
`automacao-api.md`). Mockar o próprio back-end transforma o "E2E" em teste de
front; dê esse nome e mantenha alguns fluxos críticos sem mock. HAR envelhece
e pode conter token e dado pessoal: sanitize antes de versionar (LGPD).

## Asserções significativas e soft assertions

- `await expect(page.locator('.toast')).toBeVisible()` passa até com toast de
  erro. Verifique texto, valor e efeito persistido (consulta por API).
- Calcule o esperado de forma independente (2 × R$ 24,90 + frete de R$ 15,00
  do mock = R$ 64,80), nunca copie da tela.
- Asserção negativa passa cedo demais: `not.toBeVisible()` é verdadeira antes
  de a resposta chegar. Primeiro espere o sinal positivo de conclusão, depois
  verifique a ausência.
- `expect` sem `await` vira promessa solta e o teste pode passar sem verificar.
  Ative `eslint-plugin-playwright` (`missing-playwright-await`,
  `no-wait-for-timeout`, `prefer-web-first-assertions`).
- Listas: `toHaveText(['Café', 'Filtro'])`; estrutura acessível:
  `toMatchAriaSnapshot`.

Soft assertion continua o teste e reprova no fim — útil para vários campos
independentes da mesma tela; nunca para pré-condição (se o login falhou,
seguir só gera ruído).

```ts
const nota = page.getByRole('region', { name: 'Resumo do pedido' });
await expect.soft(nota.getByTestId('subtotal')).toHaveText('R$ 49,80');
await expect.soft(nota.getByTestId('frete')).toHaveText('R$ 15,00');
await expect(nota.getByTestId('total')).toHaveText('R$ 64,80');
```

## Regressão visual

```ts
await expect(page.getByTestId('resumo-pedido')).toHaveScreenshot('resumo-pedido.png', {
  mask: [page.getByTestId('numero-pedido'), page.getByTestId('data-pedido')],
  maxDiffPixelRatio: 0.01, // até 1% dos pixels diferentes
});
```

- Mascare o que muda a cada execução: datas, IDs, avatares, carrossel,
  anúncio. Animações e cursor já são desligados por padrão em
  `toHaveScreenshot`.
- Tolerância: `maxDiffPixels`/`maxDiffPixelRatio` para quantidade e
  `threshold` (0–1, padrão 0.2) para diferença de cor por pixel. Prefira
  print de componente a página inteira: menos ruído, diff legível.
- Renderização muda com SO e fontes; o nome do arquivo inclui a plataforma.
  Gere e compare no mesmo container, com a mesma versão do pacote:
  `docker run --rm --ipc=host -v "$PWD":/work -w /work mcr.microsoft.com/playwright:v1.63.0-noble npx playwright test tests/visual --update-snapshots=changed`.
- Vale para design system, checkout, páginas impressas e e-mails. Não vale
  para tela que muda toda semana: o time aprende a aprovar diff sem olhar.

## Depuração

- **Trace viewer**: `npx playwright show-trace caminho/trace.zip` mostra cada
  ação com DOM antes/depois, rede, console e linha do código. É a primeira
  ferramenta para falha de CI.
- **UI mode**: `npx playwright test --ui` (modo watch, linha do tempo,
  seletor de locator). **Inspector**: `--debug` ou `await page.pause()`.
- **Codegen**: `npx playwright codegen http://localhost:3000` serve para
  descobrir locators e rascunhar. Não aceite o código cru: é roteiro linear,
  sem fixture nem dado via API, com asserções rasas (`toBeVisible`) e às vezes
  `nth()`. O mesmo vale para os Test Agents (1.56+): o *healer* pode "consertar"
  o teste adaptando-o a uma regressão real — revise como PR de pessoa.
- **Vídeo e print**: `video: 'retain-on-failure'`, `screenshot:
  'only-on-failure'`. Vídeo ajuda em animação; para o resto, trace é melhor.

## Paralelismo, sharding, retries e timeouts

| Ajuste | Valor típico | Por quê |
| --- | --- | --- |
| `timeout` (teste) | 30 s (padrão) | fluxo E2E típico; fluxo longo usa `test.slow()` (triplica), não aumento global |
| `expect.timeout` | 5 s (padrão); 10 s em ambiente lento | maior que isso esconde lentidão que é defeito |
| `actionTimeout` | 10–15 s | padrão é sem limite: ação travada consome o teste inteiro e a mensagem piora |
| `navigationTimeout` | 15–30 s | |
| `globalTimeout` | ex.: 60 min no CI | job travado não segura a fila |
| `retries` | 0 local; 1–2 no CI | retry mostra o *flaky* no relatório; mais que 2 esconde defeito |
| `workers` | 50% dos núcleos (padrão); fixe no CI | container pode reportar núcleos errados; back-end de teste costuma saturar antes da máquina |

- `fullyParallel: true` paraleliza dentro do arquivo; exige testes de fato
  independentes. Sharding entre máquinas:
  `npx playwright test --shard=1/4` com `reporter: 'blob'` e depois
  `npx playwright merge-reports --reporter html ./all-blob-reports`.
- Acompanhe a taxa de *flaky*. Quando estabilizar, `--fail-on-flaky-tests`
  impede que o retry vire tapete. Na 1.62+, `retryStrategy: 'isolated'` roda
  os retries no fim, num worker só, separando falha do teste de interferência.
- Mais workers gerando 5xx no ambiente não é teste intermitente: é
  capacidade. Reduza workers ou escale o ambiente.

## Teste intermitente: diagnóstico e causas

1. **Reproduza isolado e sequencial**:
   `npx playwright test tests/pedidos/cancelamento.spec.ts --repeat-each=30 --workers=1 --retries=0 --trace=retain-on-failure`.
   Depois com `--workers=4`. Só falha em paralelo → estado compartilhado ou
   capacidade do ambiente.
2. **Meça a taxa** com o script da skill (vale para qualquer runner):
   `python scripts/repetir_teste.py -n 30 -- npx playwright test caminho.spec.ts`.
   Com zero falhas, 3/n é uma aproximação do limite superior unilateral de
   95% para a taxa, sob tentativas independentes e probabilidade estável.
   Não é garantia de ausência de defeito: 30 execuções limpas ainda são
   compatíveis com taxa perto de 10%; cerca de 150 sem falhas estreitam esse
   limite para perto de 2%. Mudança de carga, dados ou ambiente muda a população.
3. **Abra o trace da falha**: a ação anterior ao erro, o DOM naquele
   instante, a rede (requisição pendente ou 5xx) e o console. Prefira
   `retain-on-failure` a `on-first-retry` no diagnóstico: este grava a
   reexecução, que pode ter passado.
4. **Compare as falhas**: mesma linha e mensagem → corrida naquele passo;
   linhas diferentes → ambiente lento ou instável. Agrupe por mensagem.
5. **Corrija a causa**, reexecute o passo 2 e só então feche. Retry e sleep
   não são correção.

| Causa | Sintoma | Correção |
| --- | --- | --- |
| Corrida clique × navegação | lê URL ou texto da página antiga | `await expect(page).toHaveURL(/\/pedidos\/\d+$/)` e ancore em algo exclusivo da nova página |
| Animação | "element intercepts pointer events", clique no lugar errado | espere o estado final (`await expect(dialogo).toBeHidden()`); `contextOptions: { reducedMotion: 'reduce' }` com o app respeitando `prefers-reduced-motion`; nunca `force: true` |
| Hidratação (SPA/Next.js) | clique sem efeito, formulário faz GET nativo, `fill` apagado | botão desabilitado até hidratar (abaixo): o auto-wait de "habilitado" resolve |
| Estado compartilhado | carrinho com itens de outro teste | dados por teste via fixture; conta por `parallelIndex` |
| Dependência de ordem | passa na suíte, falha sozinho (`arquivo.spec.ts:12`) | cada teste cria seus dados; `mode: 'serial'` só para jornada de fato sequencial |
| Dados de outro teste | `toHaveCount(3)` vira 4 em paralelo | filtre pelo dado único que o teste criou |
| Relógio e fuso | falha perto da meia-noite ou só no CI (UTC) | `timezoneId: 'America/Sao_Paulo'` e `page.clock` (controla só o navegador, não o servidor) |
| Rede de terceiros | `goto` lento, widget de chat cobre o botão | bloqueie analytics/chat numa fixture automática; nunca o terceiro que está em teste |

```tsx
// App (Next.js/React): só habilita depois de hidratar
const [hidratado, setHidratado] = useState(false);
useEffect(() => setHidratado(true), []);
return <button type="submit" disabled={!hidratado}>Entrar</button>;
```

```ts
// Dado único e relógio fixo
const nome = `Produto e2e ${randomUUID().slice(0, 8)}`; // import { randomUUID } from 'node:crypto'
await expect(page.getByRole('row').filter({ hasText: nome })).toHaveCount(1);

await page.clock.setFixedTime(new Date('2026-03-31T23:59:30-03:00'));
await page.goto('/agenda');
await expect(page.getByRole('heading', { level: 1 })).toHaveText('31 de março de 2026');

// Fixture que bloqueia terceiros (dentro de test.extend)
context: async ({ context }, use) => {
  await context.route(/googletagmanager|hotjar|intercom|clarity\.ms/, (r) => r.abort());
  await use(context);
},
```

## Exemplo completo em Playwright TypeScript

```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

const CI = !!process.env.CI;
const AUTH = 'playwright/.auth/usuario.json';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: CI,
  retries: CI ? 2 : 0,
  workers: CI ? 4 : undefined,
  reporter: CI ? [['blob'], ['github']] : [['html', { open: 'never' }]],
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    locale: 'pt-BR',
    timezoneId: 'America/Sao_Paulo',
    actionTimeout: 10_000,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    { name: 'chromium', use: { ...devices['Desktop Chrome'], storageState: AUTH }, dependencies: ['setup'] },
    { name: 'webkit', use: { ...devices['Desktop Safari'], storageState: AUTH }, dependencies: ['setup'] },
    { name: 'mobile', use: { ...devices['Pixel 7'], storageState: AUTH }, dependencies: ['setup'] },
  ],
  webServer: process.env.BASE_URL
    ? undefined
    : { command: 'npm run start', url: 'http://localhost:3000', reuseExistingServer: !CI },
});
```

```ts
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

setup('autentica usuário padrão', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('E-mail').fill(process.env.E2E_USER!);
  await page.getByLabel('Senha').fill(process.env.E2E_PASSWORD!);
  await page.getByRole('button', { name: 'Entrar' }).click();
  await expect(page.getByRole('heading', { name: 'Painel' })).toBeVisible();
  await page.context().storageState({ path: 'playwright/.auth/usuario.json' });
});
```

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

  async cancelar(motivo: string) {
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
    const resposta = await api.post('/api/pedidos', {
      data: { itens: [{ sku: 'CAFE-250G', quantidade: 2 }], pagamento: 'BOLETO' },
    });
    expect(resposta.status(), await resposta.text()).toBe(201);
    const pedido = (await resposta.json()) as Pedido;
    await use(pedido);
    await api.delete(`/api/pedidos/${pedido.id}`); // limpeza
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

test('cancela pedido pendente pago com boleto e registra o status no back-end', async ({
  page, api, pedidoPendente, pedidoPage,
}) => {
  await pedidoPage.abrir(pedidoPendente.id);
  const cancelamento = page.waitForResponse(
    (r) => r.url().endsWith(`/api/pedidos/${pedidoPendente.id}/cancelamento`) && r.request().method() === 'POST',
  );
  await pedidoPage.cancelar('Desisti da compra');
  expect((await cancelamento).status()).toBe(200);

  await expect(pedidoPage.aviso).toHaveText('Pedido cancelado');
  await expect(pedidoPage.status).toHaveText('Cancelado');
  await expect
    .poll(async () => (await (await api.get(`/api/pedidos/${pedidoPendente.id}`)).json()).status)
    .toBe('CANCELADO');
});
```

Rodar: `BASE_URL=https://hml.exemplo.com.br npx playwright test --project=chromium`.
Variáveis exigidas: `E2E_USER`, `E2E_PASSWORD`, `E2E_API_TOKEN`.

## Exemplo em Playwright Python

```python
# conftest.py
import os
from typing import Generator

import pytest
from playwright.sync_api import APIRequestContext, Browser, Playwright, expect


@pytest.fixture(scope="session")
def estado_autenticado(browser: Browser, base_url: str, tmp_path_factory) -> str:
    caminho = tmp_path_factory.mktemp("auth") / "usuario.json"
    contexto = browser.new_context(base_url=base_url)
    pagina = contexto.new_page()
    pagina.goto("/login")
    pagina.get_by_label("E-mail").fill(os.environ["E2E_USER"])
    pagina.get_by_label("Senha").fill(os.environ["E2E_PASSWORD"])
    pagina.get_by_role("button", name="Entrar").click()
    expect(pagina.get_by_role("heading", name="Painel")).to_be_visible()
    contexto.storage_state(path=caminho)
    contexto.close()
    return str(caminho)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, estado_autenticado: str) -> dict:
    return {**browser_context_args, "storage_state": estado_autenticado,
            "locale": "pt-BR", "timezone_id": "America/Sao_Paulo"}


@pytest.fixture
def api(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    contexto = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers={"Authorization": f"Bearer {os.environ['E2E_API_TOKEN']}"},
    )
    yield contexto
    contexto.dispose()


@pytest.fixture
def pedido_pendente(api: APIRequestContext) -> Generator[dict, None, None]:
    resposta = api.post("/api/pedidos", data={"itens": [{"sku": "CAFE-250G", "quantidade": 2}],
                                             "pagamento": "BOLETO"})
    assert resposta.status == 201, resposta.text()
    pedido = resposta.json()
    yield pedido
    api.delete(f"/api/pedidos/{pedido['id']}")
```

```python
# tests/test_cancelamento_pedido.py
import re

from playwright.sync_api import APIRequestContext, Page, expect


def test_cancela_pedido_pendente(page: Page, api: APIRequestContext, pedido_pendente: dict) -> None:
    pedido_id = pedido_pendente["id"]
    page.goto(f"/pedidos/{pedido_id}")
    with page.expect_response(re.compile(rf"/api/pedidos/{pedido_id}/cancelamento$")) as info:
        page.get_by_role("button", name="Cancelar pedido").click()
        dialogo = page.get_by_role("dialog", name="Cancelar pedido?")
        dialogo.get_by_label("Motivo").select_option("Desisti da compra")
        dialogo.get_by_role("button", name="Confirmar cancelamento").click()
    assert info.value.status == 200

    expect(page.get_by_test_id("status-pedido")).to_have_text("Cancelado")
    assert api.get(f"/api/pedidos/{pedido_id}").json()["status"] == "CANCELADO"
```

Rodar: `pytest --base-url https://hml.exemplo.com.br --browser chromium --tracing retain-on-failure -n 4`
(`-n` vem do `pytest-xdist`; cada worker faz o próprio login de sessão). O
Python não tem `expect.poll`; leia o estado por API depois que a tela
confirmou a conclusão, como acima.

## Cypress: exemplo e armadilhas

```ts
// cypress/support/commands.ts
declare global {
  namespace Cypress { interface Chainable { entrar(): Chainable<void> } }
}

Cypress.Commands.add('entrar', () => {
  cy.env(['E2E_USER', 'E2E_PASSWORD'], { log: false }).then(({ E2E_USER, E2E_PASSWORD }) => {
    cy.session(E2E_USER, () => {
      cy.visit('/login');
      cy.findByLabelText('E-mail').type(E2E_USER);
      cy.findByLabelText('Senha').type(E2E_PASSWORD, { log: false });
      cy.findByRole('button', { name: 'Entrar' }).click();
      cy.findByRole('heading', { name: 'Painel' }).should('be.visible');
    }, {
      validate: () => { cy.request('/api/me').its('status').should('eq', 200); },
      cacheAcrossSpecs: true,
    });
  });
});
export {};
```

```ts
// cypress/e2e/pedidos/cancelamento.cy.ts
describe('Cancelamento de pedido', () => {
  beforeEach(() => cy.entrar());

  it('cancela pedido pendente e registra o status no back-end', () => {
    cy.request('POST', '/api/pedidos', { itens: [{ sku: 'CAFE-250G', quantidade: 2 }], pagamento: 'BOLETO' })
      .its('body.id')
      .then((id: string) => {
        cy.intercept('POST', `/api/pedidos/${id}/cancelamento`).as('cancelar');
        cy.visit(`/pedidos/${id}`);
        cy.findByRole('button', { name: 'Cancelar pedido' }).click();
        cy.findByRole('dialog').within(() => {
          cy.findByLabelText('Motivo').select('Desisti da compra');
          cy.findByRole('button', { name: 'Confirmar cancelamento' }).click();
        });
        cy.wait('@cancelar').its('response.statusCode').should('eq', 200);
        cy.findByTestId('status-pedido').should('have.text', 'Cancelado');
        cy.request(`/api/pedidos/${id}`).its('body.status').should('eq', 'CANCELADO');
      });
  });
});
```

- **Fila de comandos.** `cy.*` enfileira; nada executa na linha em que está.
  Clássico: `let id; cy.request(...).then((r) => { id = r.body.id }); cy.visit(`/pedidos/${id}`)`
  visita `/pedidos/undefined`. Use `.then`, `.its` ou alias.
- **Sem async/await** com comandos Cypress: não são promessas.
- **Retry**: queries e asserções `.should` repetem; ações não; `.then(($el) => expect(...))`
  não repete. Verifique com `.should('have.text', …)`.
- **`cy.wait(5000)` nunca**: registre `cy.intercept(...).as('x')` *antes* da
  ação e `cy.wait('@x')`. No Cypress 16 a interceptação ocorre na rede nativa
  do navegador (Chrome/Edge); `req.httpVersion` deixou de existir.
- **`cy.session`** com `validate` evita sessão expirada passando batido.
- **Segredos**: `Cypress.env()` foi descontinuado na 15.10 e removido na 16;
  use `cy.env([...])` para segredo e `Cypress.expose()` para configuração não
  sensível. `cy.exec()` também saiu na 16: use `cy.task()`.
- Isolamento entre testes é padrão desde a v12 (página, cookies e storage
  limpos); não desligue `testIsolation` para "ganhar tempo".

## Selenium 4

- **Selenium Manager** (embutido) resolve driver e navegador: dispensa
  baixar chromedriver ou usar bibliotecas de gerenciamento de driver.
- **Sem auto-wait**: `find_element` falha na hora se o elemento não existe.
  Use espera explícita para cada condição.
- **Nunca misture espera implícita e explícita**: a documentação avisa que o
  tempo fica imprevisível (implícita de 10 s + explícita de 15 s pode estourar
  só em 20 s). Deixe a implícita em 0.
- `StaleElementReferenceException`: a SPA re-renderizou; localize de novo em
  vez de guardar `WebElement` entre ações.
- WebDriver BiDi (rede, console, eventos sem CDP) avança a cada versão; parte
  da API ainda é beta. Paralelismo via Grid 4 ou runner (`pytest-xdist`, TestNG).

```python
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()  # Selenium Manager resolve driver e navegador
try:
    espera = WebDriverWait(driver, timeout=10)
    driver.get(f"{os.environ['BASE_URL']}/login")
    espera.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(os.environ["E2E_USER"])
    driver.find_element(By.ID, "senha").send_keys(os.environ["E2E_PASSWORD"])
    espera.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='entrar']"))).click()
    espera.until(EC.url_contains("/painel"))
    assert espera.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Painel"))
finally:
    driver.quit()
```

## Emulação mobile e matriz de navegadores

`devices['iPhone 15']` aplica viewport, user agent, densidade e toque sobre o
WebKit do Playwright. Não reproduz Safari de iOS real, teclado virtual
encolhendo a tela, área segura (notch), gestos reais, CPU e memória de
Android de entrada, autofill nem diálogos do sistema. Use emulação para
layout responsivo no CI; valide fluxos críticos em aparelho real ou nuvem
(ver `mobile.md`).

Matriz: escolha pelos dados de acesso dos últimos 90 dias e cubra os motores
— Chromium (Chrome, Edge, Samsung Internet), WebKit (Safari e todo navegador
de iOS) e Gecko (Firefox) se houver público. No Brasil o acesso é
majoritariamente móvel: Chrome Android e Safari iOS vêm primeiro. Separe
"suportado" de "melhor esforço" por escrito. Ritmo comum: Chromium no PR;
Chromium + Firefox + WebKit + mobile emulado no noturno; dispositivo real
antes do release.

## Teste de componente

| Opção | Característica |
| --- | --- |
| Testing Library + Vitest/Jest (jsdom) | rápido; jsdom não tem layout (visibilidade por CSS, scroll e tamanho não são reais) |
| Vitest Browser Mode | navegador real via provedor Playwright ou WebdriverIO; estável desde o Vitest 4 |
| Playwright CT | desde a 1.62: *stories* servidas por uma galeria no seu dev server e fixture `mount` do próprio `@playwright/test`; os pacotes `@playwright/experimental-ct-*` não são mais atualizados |
| Cypress CT | `cy.mount` para React, Vue, Angular, Svelte; o Cypress 16 exige Vite 8+, Angular 21+ e Next.js 15+ |

Prefira componente a E2E para estados difíceis de alcançar pela jornada (erro,
vazio, carregando, 1.000 itens), variações de design system, interação interna
(máscara de CPF, seletor de data) e acessibilidade do componente. Deixe para
E2E integração, navegação, autenticação e contrato real com o back-end.

## Revisão de PR de testes E2E

Ordem do SKILL: falso verde > intermitência > lacuna de risco > lentidão >
manutenção > estilo.

- [ ] Cada teste verifica o efeito de negócio (valor, status, dado
  persistido), não só que "algo apareceu"; esperado calculado, não copiado.
- [ ] Todo `expect` tem `await`; nenhuma asserção instantânea
  (`expect(await …textContent())`) sobre algo que muda.
- [ ] Asserção negativa só depois de um sinal positivo de conclusão.
- [ ] Nenhum `waitForTimeout`, `sleep`, `cy.wait(número)`, `networkidle`
  nem `force: true`.
- [ ] Localizadores por papel, rótulo ou test id; sem `nth`, XPath absoluto
  ou classe gerada; nenhum `.first()` para calar ambiguidade.
- [ ] Dados criados por teste, únicos, limpos; nada depende de ordem ou de
  massa que outro teste altera; roda com `fullyParallel`.
- [ ] Rodou com `--repeat-each` (ou `repetir_teste.py`) antes do merge.
- [ ] Mock coerente com o contrato real; fluxo crítico mantém versão sem mock.
- [ ] Sem segredo no código; `playwright/.auth` no `.gitignore`.
- [ ] Nenhum `test.only` (use `forbidOnly`), `skip`/`fixme` sem issue, nem
  aumento de retries ou timeout sem justificativa.
- [ ] Page object com métodos de intenção e sem asserção escondida.
- [ ] Snapshot visual atualizado com o diff revisado, não com `-u` às cegas.
- [ ] O nome descreve a regra e o nível é o certo: isso não caberia em teste
  de componente, de API ou unitário?
