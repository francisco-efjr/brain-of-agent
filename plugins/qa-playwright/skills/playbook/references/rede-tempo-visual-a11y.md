# Rede, tempo, visual, acessibilidade e eventos

Receitas para a camada HTTP, o controle de tempo, a emulação, a regressão visual, os ARIA snapshots, o axe, o component testing e os eventos que nascem de uma ação. Fontes: V-51..V-59. Os trechos de código são de redação própria; confirme APIs na versão fixada (`npx playwright --version`). Skills que usam este arquivo: `api-and-network` e `visual-a11y-responsive`.

## Sumário

- [API com `request` e o padrão híbrido](#api-com-request-e-o-padrão-híbrido)
- [Rede: mock, alteração, HAR, WebSocket, falhas e offline](#rede-mock-alteração-har-websocket-falhas-e-offline)
- [Relógio](#relógio)
- [Emulação](#emulação)
- [Regressão visual](#regressão-visual)
- [ARIA snapshot](#aria-snapshot)
- [Acessibilidade com axe](#acessibilidade-com-axe)
- [Component testing](#component-testing)
- [Eventos que nascem de uma ação](#eventos-que-nascem-de-uma-ação)

## API com `request` e o padrão híbrido

Fonte: V-51. Três usos da fixture `request`: testar a API, **preparar estado** e **validar pós-condição** (`api-testing-js.md:13-15`). Backend de teste, nunca produção. Os exemplos da doc chamam a API real do GitHub e criam repositórios (`:116-120`): não os copie.

- `request` respeita `baseURL` e `extraHTTPHeaders` (`:69`). Token por variável de ambiente (`:41-43`).
- Quando o `baseURL` tem prefixo de caminho (`http://host/api/v1/`), termine-o com `/` e use caminhos sem `/` inicial; com `/` inicial o caminho substitui o prefixo (resolução de URL; nota do plugin `backend-api`). Com `baseURL` só de origem, os dois funcionam.
- **Cookies:** `context.request` e `page.request` usam e atualizam os cookies do contexto; `playwright.request.newContext()` isola (`:300-344`). Escolha explicitamente.
- **Híbrido: dado via API, ação na UI, verificação via API.** Crie o estado por API e só então `page.goto`; ou crie pela UI e consulte a API com o id. Limpe por id capturado (V-33). Um `apiContext` por arquivo (`beforeAll` e `afterAll`).

```ts
test('F-08 criar tarefa persiste @ui', async ({ page, request }, testInfo) => {
  const nome = `Tarefa ${testInfo.testId.slice(0, 6)}`;
  await page.goto('/tarefas');
  await page.getByRole('textbox', { name: 'Nova tarefa' }).fill(nome);
  await page.getByRole('button', { name: 'Adicionar' }).click();
  await expect(page.getByRole('listitem').filter({ hasText: nome })).toHaveCount(1);
  const lista = await (await request.get('/api/tarefas')).json();      // verificação via API
  expect(JSON.stringify(lista)).toContain(nome);
});
```

- GraphQL é `request.post` com corpo `query`: **Inferido**, sem guia na doc.
- O Playwright **não** cobre contrato, schema OpenAPI nem carga (Inferido): use `backend-api:api-test-suite` e `sre-observability`. Exploração de API sem UI: `curl` ou `Invoke-RestMethod` em `127.0.0.1` com dados sintéticos (Inferido; a CLI controla navegador).
- Comparativos de blog Playwright contra REST Assured e Postman foram rejeitados como evidência (V-51).

## Rede: mock, alteração, HAR, WebSocket, falhas e offline

Fonte: V-52, X-12, X-13.

- **Escopo:** `page.route` vale para a página; `context.route` vale também para popups e links abertos (`network.md:443`). Registre a rota **antes** da ação.
- **Glob:** `*` não cruza `/`; `**` cruza.
- **Resposta** (`fulfill`), com corpo e `contentType` realistas:

```ts
await page.route('**/api/tarefas', (route) =>
  route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ erro: 'falha' }) }),
);
```

- **Alteração:** `route.fetch()` e depois `fulfill` com a resposta modificada. **Aborto:** `route.abort()`.
- **Observação:** `page.on('request')`, `page.on('response')` e `page.waitForResponse` (registrado antes da ação).
- **Offline e reconexão:** `context.setOffline(true)` e depois `false`. Na CLI: `network-state-set offline` e `online` (X-13). Offline não afeta WebRTC (`emulation.md:787`). Com Service Worker, o SW pode servir cache.
- **Falhas a cobrir:** timeout, 500, JSON inválido, recurso bloqueado (`abort`), offline e reconexão. Mock prova a lógica da aplicação, não o comportamento real do navegador: mantenha **ao menos um fluxo crítico sem mock**.
- **HAR:** `page.routeFromHAR(path, { update: true })` grava; sem `update` reproduz, com casamento estrito de URL e método (`mock.md:230-233, 417`). CLI: `--save-har` e `--save-har-glob` (`:425`). **Revise e remova tokens antes de commitar.**
- **WebSocket:** `page.routeWebSocket` desde a 1.48; só conexões iniciadas pela página.

```ts
await page.routeWebSocket('wss://exemplo.test/ws', (ws) => {
  ws.onMessage((msg) => ws.send(`eco: ${msg}`));
});
```

- **Limites verificados:** cabeçalhos da pilha de rede (`Cookie`, `Host`, `Accept-Encoding`, `Content-Length`, `Sec-Fetch-*`) não são sobrescrevíveis (`network.md:724-728`); o handler de redirecionamento é chamado uma vez, `fulfill` com 3xx não permite nova interceptação e o WebKit o rejeita (`:730-734`); `route` **não vê** requisições de Service Worker, e MSW interfere (`:806-808`, V-63).
- Mock mantido de contrato velho diverge da API real: confira o contrato (V-52). Mock de APIs do navegador por `addInitScript` antes do load: leitura parcial, fonte B.
- Na CLI, para exploração: `route "**/api/tarefas" --status 500 --body '{"erro":"falha"}'`, `route-list`, `unroute` (X-12).

## Relógio

Fonte: V-53. Substitui `waitForTimeout` para temporização de negócio.

```ts
await page.clock.install({ time: new Date('2026-03-01T08:00:00') });   // PRIMEIRA chamada de clock; senão, comportamento indefinido
await page.goto('/sessao');
await page.clock.fastForward('05:00');                                  // dispara uma vez os timers vencidos
await expect(page.getByRole('alert')).toHaveText(/sessão expirada/i);
```

Três cenários: data fixa (`setFixedTime`), sessão que expira (`install` e `fastForward`), tick controlado (`pauseAt` e `runFor`). O relógio sobrescreve `Date`, timers e `requestAnimationFrame`: pode afetar bibliotecas de animação. `clock` surge na 1.45.

## Emulação

Fonte: V-54. Matriz de cenários para o plano: dispositivo × locale × timezone × tema × permissão, como projetos da config (V-40).

- `devices['Pixel 5']`, `devices['iPhone 12']`; `isMobile` (viewport e toque) deve ser definido **depois** de desestruturar `devices` (`emulation.md:265-279`). `locale` e `timezoneId` só no navegador; permissões; geolocalização só vale para todas as páginas do contexto; `javaScriptEnabled: false`; `colorScheme`.
- 1.64: `screen` passa a vir do descritor do dispositivo; baselines visuais podem mudar.
- Emulação **não substitui aparelho real**; WebKit não é Safari (V-50, V-61).
- Na exploração: `open --device="iPhone 15"`, `resize 1280 800` (gera `page.setViewportSize(...)`) e `set-color-scheme dark` (gera `page.emulateMedia({ colorScheme: 'dark' })`), exercitados em X-26; `--mobile` só consta do `--help`.

```ts
// playwright.config.ts, projetos extras
projects: [
  { name: 'desktop' },
  { name: 'mobile', use: { ...devices['Pixel 5'] } },
  { name: 'escuro', use: { colorScheme: 'dark' } },
],
```

## Regressão visual

Fonte: V-55. Visual serve a **layout** e não substitui o teste da funcionalidade (Inferido).

- Primeira execução gera as capturas até duas consecutivas coincidirem (`test-snapshots-js.md:31-32`). O nome inclui navegador e plataforma (`example-test-1-chromium-darwin.png`): **baseline de Linux não serve para macOS**. Use o mesmo ambiente da geração (container da CI, imagem Docker fixada).
- `await page.mouse.move(-1, -1)` antes da captura. `mask` e `stylePath` para o volátil; `threshold` padrão 0,2; **`animations` tem padrão `disabled`**.
- Primeira geração com `--update-snapshots=missing` (passa a rodada na 1.64). Atualize baseline **só depois de revisar o diff**; `-u` fora da skill visual é proibido por instrução (G-08).
- Cuidado: o `stylePath` de exemplo da doc oculta iframes com `visibility: hidden`, o que esconde conteúdo real.

```ts
await expect(page).toHaveScreenshot('painel.png', {
  mask: [page.getByTestId('relogio')],
  maxDiffPixelRatio: 0.01,
});
```

## ARIA snapshot

Fonte: V-56. "A template is a constraint, not necessarily a complete serialization" (`aria-snapshots.md:144`): valide landmarks, títulos, links e controles sem depender do texto exato.

- `- button` casa qualquer nome (`:232-237`). `/children`: `contain` (padrão), `equal`, `deep-equal` (`:292-298`).
- Modos de atualização: `default` (gera mas **faz o teste falhar**), `missing`, `-u` (`changed`), `all`, `none` (`:370-375`). Na CI use `default` ou `missing`; `-u` só local, com revisão do patch. `--update-source-method`: `patch` (padrão), `3way`, `overwrite`.
- Versões: `toMatchAriaSnapshot` 1.49; `page.ariaSnapshot` 1.59; asserção na página 1.60; JSON 1.63; `Page.getByRef` com modo `ai` 1.64 (não verificado em profundidade).

```ts
await expect(page.getByRole('navigation')).toMatchAriaSnapshot(`
  - navigation:
    - link "Início"
    - link "Tarefas"
`);
```

## Acessibilidade com axe

Fonte: V-57. **`@axe-core/playwright` é dependência nova e não está na pré-autorização:** peça confirmação ou registre decisão pendente (G-11).

- A doc diz: "automated testing cannot detect all types of WCAG violations"; teste também manualmente (teclado e leitor de tela). Não cite cobertura percentual do axe: sem fonte (Não verificado).
- `withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])`: a lista oficial; o Subito usa só `wcag2a` e `wcag2aa`.
- Escaneie cada tela da matriz, **inclusive o estado revelado por interação** (espere o elemento antes de `analyze()`). Anexe o resultado completo com `testInfo.attach`; não faça snapshot do array inteiro de violações (`:172-177`).
- **`exclude()` exclui o elemento, os descendentes e todas as regras** (`:127-128`): prefira `disableRules` por id antes de `exclude`. Exclua elementos de terceiros por seletor.
- Política (fonte B, Subito): lista fixa de páginas críticas, não bloqueia o build, uma issue por violação, bloqueia só regressão nova.

```ts
import AxeBuilder from '@axe-core/playwright';

test('F-12 painel sem violações novas @ui', async ({ page }, testInfo) => {
  await page.goto('/painel');
  await expect(page.getByRole('heading', { name: 'Painel' })).toBeVisible();   // estado pronto antes de analisar
  const resultado = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
  await testInfo.attach('axe', { body: JSON.stringify(resultado, null, 2), contentType: 'application/json' });
  expect(resultado.violations.map((v) => v.id)).toEqual([]);                    // ajuste à política de regressão nova
});
```

## Component testing

Fonte: V-58, conflito 4. **Estável desde a 1.62** (fixture `mount` do `@playwright/test`); a afirmação de que é experimental está desatualizada. Os pacotes `@playwright/experimental-ct-*` ficaram congelados em 1.62.x (npm `latest` = 1.62.1).

- Story = wrapper com props, mocks e providers. Galeria = página do seu dev server com `window.mount({ story, props })` e `window.unmount()`. Projeto `components` com `baseURL` na galeria, `serviceWorkers: 'block'` e `reuseContext: true`; `mount(storyId)` devolve um Locator da raiz.
- Camada entre unidade e E2E: cobre componente isolado, **não** a funcionalidade ponta a ponta. Exige galeria e dev server.
- A doc manda rodar `npx playwright init-skills` e pedir ao agente que monte a galeria: **não execute sem pedido do usuário** (G-13).

## Eventos que nascem de uma ação

Fonte: V-59. **Regra única: registre o handler ou a espera antes da ação que dispara o evento.**

- **Diálogo:** sem listener, o diálogo é descartado sozinho; **com listener, ele deve tratar o diálogo ou a ação trava** (`dialogs.md:12, 42-44, 78`). Teste a confirmação destrutiva nos dois ramos (aceitar e cancelar). Na CLI: `dialog-accept`, `dialog-dismiss` (não exercitados).
- **Download:** inicie `waitForEvent('download')` antes do clique; arquivos temporários somem ao fechar o contexto (`downloads.md:13, 19-22`).
- **Página nova e popup:** capture a promessa antes da ação (`pages.md:162-167`); `context.on('page')` ou `page.on('popup')` (`:317-326`).
- **Upload e file chooser:** `setInputFiles`; para seletor nativo, espera de `filechooser` antes do clique (`class-filechooser.md:59-77`).
- **Iframe:** `frameLocator`; comportamento de iframe cross-origin não lido (Não verificado).

```ts
page.once('dialog', (d) => d.accept());                                  // ANTES do clique
await page.getByRole('button', { name: 'Excluir' }).click();

const downloadPromise = page.waitForEvent('download');                   // ANTES do clique
await page.getByRole('button', { name: 'Exportar' }).click();
const download = await downloadPromise;
expect(download.suggestedFilename()).toMatch(/\.csv$/);
```

Clique que navega: `await page.waitForURL(...)`. `fill` em vez de `pressSequentially`; `check`, `uncheck`, `setChecked`; `selectOption`; `dragTo`. Não use `force: true` nem `dispatchEvent` para destravar teste: registre como achado (V-30).
