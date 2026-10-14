# Checklist E2E detalhado: Playwright, Cypress e Selenium

Apoio da skill `e2e-review`. Traz as buscas para localizar problemas, a configuração recomendada, receitas de stub e login, notas de Cypress e Selenium, o guardrail do healer e uma revisão completa de exemplo.

Rótulos: Verificado = lido em V-19 (Playwright best practices), V-20 (test agents), V-21 (retries), V-22 (Testing Library), V-24 (Cypress), V-11 (webapp-testing). Itens marcados Inferido são conhecimento estável do domínio e não constam nas páginas lidas: confirme na documentação da versão instalada (`npx playwright --version`, `npx cypress --version`).

## Sumário

- [Buscas rápidas](#buscas-rápidas)
- [Configuração recomendada do Playwright](#configuração-recomendada-do-playwright)
- [Login e estado reaproveitado](#login-e-estado-reaproveitado)
- [Stub de rede](#stub-de-rede)
- [Cypress](#cypress)
- [Selenium](#selenium)
- [Seletores: prioridade](#seletores-prioridade)
- [Healer e agentes do Playwright](#healer-e-agentes-do-playwright)
- [Reconhecimento em 5 passos](#reconhecimento-em-5-passos)
- [Revisão completa de exemplo](#revisão-completa-de-exemplo)

## Buscas rápidas

Use a ferramenta Grep da sessão (ou `rg`) para listar candidatos; o resultado é pista, não veredito: leia o teste antes de apontar.

| Alvo | Padrão (regex) | Item |
| --- | --- | --- |
| Espera fixa | `waitForTimeout\|cy\.wait\(\s*\d\|Thread\.sleep\|time\.sleep\|setTimeout` | E-03 |
| Asserção que não espera | `expect\(await .*\.(isVisible\|isHidden\|isChecked\|textContent\|innerText)\(` | E-02 |
| Asserção fraca | `not\.toBeNull\|toBeTruthy\(\)\|toBeDefined\(\)\|status.*200` | E-01 |
| Seletor frágil | `xpath=\|//div\|nth-child\|\.nth\(\|\.btn-\|css-[a-z0-9]{5}` | E-08 |
| Segredos | `password\|senha\|secret\|token\|apikey\|Bearer ` | E-10 |
| Teste silenciado | `\.only\(\|\bfit\(\|\bfdescribe\(\|\.skip\(\|test\.fixme` | E-11 |
| Estado global | `^let \|^var ` em arquivos de spec | E-04 |
| Limpeza tardia | `afterAll\|after\(` | E-07 |
| URL fixa | `https?://localhost\|https?://[a-z0-9.-]+\.(com\|net\|io)` | E-10 |
| Rota registrada | `page\.route\|cy\.intercept` (confira a ordem em relação ao `click`/`goto`) | E-05 |

Nas células da tabela a alternância aparece como `\|` por causa do Markdown; ao buscar com a ferramenta Grep (ripgrep) ou `rg`, use `|` sem a barra invertida.

## Configuração recomendada do Playwright

V-19: trace por padrão no primeiro retry em CI; isolamento; projeto de setup para login. Os demais campos são Inferido (API estável do Playwright Test).

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,               // falha o CI se sobrou test.only
  retries: process.env.CI ? 1 : 0,            // 1 retentativa como sinal, nunca como correção
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    trace: 'on-first-retry',
    locale: 'pt-BR',
    timezoneId: 'America/Sao_Paulo',
  },
  projects: [
    { name: 'setup', testMatch: /auth\.setup\.ts/ },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], storageState: 'e2e/.auth/user.json' },
      dependencies: ['setup'],
    },
  ],
});
```

Notas: `e2e/.auth/` entra no `.gitignore` (o arquivo de estado contém cookies). Retries por grupo: `test.describe.configure({ retries: 2 })` (V-21). Resultados são classificados em passed, flaky (falhou e passou no retry) e failed; trate flaky como falha a investigar (skill `flaky-triage`). Depois de falha o worker é descartado e um novo é iniciado (V-21).

## Login e estado reaproveitado

Projeto de setup (V-19 recomenda reaproveitar login):

```ts
// e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

setup('autentica', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('E-mail').fill(process.env.E2E_USER!);
  await page.getByLabel('Senha').fill(process.env.E2E_PASSWORD!);
  await page.getByRole('button', { name: 'Entrar' }).click();
  await expect(page.getByRole('heading', { name: 'Painel' })).toBeVisible();
  await page.context().storageState({ path: 'e2e/.auth/user.json' });
});
```

Credenciais vêm do ambiente (`E2E_USER`, `E2E_PASSWORD`), de conta de teste. Quando o app tem API de login, prefira chamar a API (`request.post`) em vez de percorrer a UI; um teste dedicado cobre a tela de login. Cypress equivalente: `cy.session()` com login programático (V-24).

## Stub de rede

V-19: não teste terceiros; stube com `page.route`. Regras práticas:

1. Registre a rota **antes** da ação que dispara a requisição (clique, `goto`). Rota registrada depois nunca intercepta.
2. Responda com status, `contentType` e corpo realistas (campos e tipos do contrato real). Corpo `{}` esconde bugs de leitura da resposta.
3. Se o handler usa `await route.fulfill(...)`, tudo certo; se retorna a promessa (`r => r.fulfill(...)`), também. Não aponte falta de `await` nesse caso.
4. Falhas também: `route.fulfill({ status: 500 })` e `route.abort()` para provar o tratamento de erro.

```ts
await page.route('**/api/pagamento', route =>
  route.fulfill({
    status: 201,
    contentType: 'application/json',
    body: JSON.stringify({ id: 'pg_123', status: 'aprovado', valor: 25000 }),
  }));
await page.getByRole('button', { name: 'Pagar' }).click();
await expect(page.getByRole('status')).toHaveText('Pagamento aprovado');
```

Contrato com o terceiro verifica-se fora do E2E (Pact ou sandbox do parceiro).

## Cypress

Base: V-24 (doc oficial, atualizada em 20/09/2026). Verificado:

- Atributos dedicados (`data-cy`) em vez de tag, classe ou id (decisão deste plugin: papel/rótulo antes; ver seção de seletores).
- Evite `cy.wait(<número>)`; espere por alias de rede: `cy.intercept('POST', '/api/pedidos').as('criar'); ... cy.wait('@criar')`.
- Teste só o que você controla; login programático e `cy.session()`.
- Limpe dados em `beforeEach`, não em `after` (pode nunca rodar).
- Cada teste deve passar sozinho (valide com `it.only`).
- Page Objects aparecem como anti-padrão; várias asserções num teste E2E são aceitáveis.
- Não atribua o retorno de comandos a variáveis (comandos são enfileirados; use `.then()` ou aliases).
- Segredos fora do código (a página cita `cy.env()`; variáveis `CYPRESS_*` são a alternativa clássica, Inferido); defina `baseUrl`.

A página lida não cobre retries. Configuração usual (Inferido): `retries: { runMode: 1, openMode: 0 }` em `cypress.config.*`; confira na doc da versão.

## Selenium

Sem fonte A/B lida nesta pesquisa (Inferido): esperas explícitas (`WebDriverWait` com `expected_conditions`) em lugar de `time.sleep` e de espera implícita misturada; localizadores por `By.ID`/`By.CSS_SELECTOR` estáveis ou por atributos de acessibilidade; um driver por teste, encerrado em `finally`/fixture; execução headless no CI; evite XPath absoluto. Para regressão visual e dispositivos, trate como suíte à parte.

## Seletores: prioridade

Conforme V-22 (Testing Library) e V-19: `getByRole` (com `name`), depois rótulo (`getByLabel`), placeholder, texto, valor exibido, `alt`/título, e `getByTestId` por último. Playwright oferece os mesmos conceitos (`getByRole`, `getByLabel`, `getByText`, `getByTestId`). Teste de seletor por papel também valida acessibilidade básica: se o botão não tem nome acessível, o locator por papel falha, e isso é informação.

## Healer e agentes do Playwright

Base: V-20 (Verificado). O planner escreve plano em Markdown em `specs/`; o generator produz testes em `tests/`; o healer reexecuta, ajusta e entrega o teste passando **ou um teste pulado se julgar a funcionalidade quebrada**. O setup é `npx playwright init-agents --loop=claude` (também `vscode`, `codex`, `opencode`) e deve ser regenerado após atualizar o Playwright. Isso executa pacote npm e gera arquivos no repositório: só a pedido do usuário, com versão fixada e diff revisado (T-02 em `ferramentas-e-mcp.md`).

Guardrail (K4, Inferido a partir de V-20 e V-06): corrija o teste só quando a funcionalidade está correta; se parece quebrada, registre como falha de produto e não ajuste a asserção; todo teste "curado" ou pulado passa por revisão de diff antes de entrar. Editar ou remover testes para fazer passar é inaceitável no harness da Anthropic (V-06).

## Reconhecimento em 5 passos

Para escrever E2E em app local/staging que você não conhece (V-11): (1) navegar; (2) esperar um elemento esperado da página (não `networkidle`, desencorajado pela documentação do Playwright); (3) capturar screenshot e lista de elementos interativos; (4) escolher seletores; (5) agir e conferir o resultado. Exemplo de script (Node, ambiente de teste, saída na pasta do projeto):

```js
// recon.mjs: rode com BASE_URL do ambiente de teste
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(process.env.BASE_URL);
await page.getByRole('main').waitFor();      // um elemento esperado da página, não `networkidle`
await page.screenshot({ path: 'recon.png', fullPage: true });
const itens = await page
  .locator('a, button, input, select, textarea, [role]')
  .evaluateAll(els => els.slice(0, 80).map(e => ({
    tag: e.tagName.toLowerCase(),
    papel: e.getAttribute('role'),
    nome: e.getAttribute('aria-label') ?? e.textContent?.trim().slice(0, 40),
  })));
console.log(JSON.stringify(itens, null, 2));
await browser.close();
```

Espere sempre um elemento ou condição de negócio, inclusive no reconhecimento: a documentação do Playwright marca `networkidle` como DISCOURAGED (`api/params.md`, Verificado no qa-playwright V-32). Para explorar um app rodando funcionalidade por funcionalidade, prefira `npx playwright cli` da versão fixada (plugin `qa-playwright`), que devolve a árvore de acessibilidade e o código com locator estável. A skill `webapp-testing` da Anthropic (Apache-2.0) traz um helper `with_server.py`; este plugin documenta o comando, não o embute, porque o helper executa comandos de shell arbitrários passados em `--server` (leia o código antes de rodar).

## Revisão completa de exemplo

Teste submetido (domínio fictício: reserva de sala):

```ts
test('reserva sala', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('#email', 'gerente@empresa.com');
  await page.fill('#senha', 'Gerente#2026');
  await page.click('.btn.btn-lg.btn-primary');
  await page.waitForTimeout(4000);
  await page.click('xpath=//div[2]/nav/ul/li[3]/a');
  await page.click('text=Sala 3');
  const confirmacao = await page.textContent('.msg');
  expect(confirmacao).toBeTruthy();
  await page.route('**/api/reservas', r => r.fulfill({ status: 200, body: '{}' }));
});
test.afterAll(async () => { await apagarReservas(); });
```

Revisão (ordem por dano; não executei o teste, revisão por leitura):

| arquivo:linha | achado | consequência | severidade | correção |
| --- | --- | --- | --- | --- |
| reserva.spec.ts:10 | `expect(confirmacao).toBeTruthy()` | passa com qualquer texto, inclusive "Erro ao reservar"; falso verde | Crítica | `await expect(page.getByRole('status')).toHaveText('Sala 3 reservada às 10:00')` |
| reserva.spec.ts:3-4 | e-mail e senha no código | credencial vazada em repositório | Crítica | variáveis de ambiente de conta de teste; trocar a senha exposta |
| reserva.spec.ts:11 | `page.route` depois da ação | o stub nunca intercepta; o teste bate na API real ou passa sem exercitar o contrato; corpo `{}` e sem `contentType` | Alta | registrar a rota antes do clique em "Reservar", com corpo e `contentType` realistas |
| reserva.spec.ts:6 | `waitForTimeout(4000)` | flaky em CI lento, desperdiça 4 s em máquina rápida | Alta | `await expect(page.getByRole('heading', { name: 'Painel' })).toBeVisible()` |
| reserva.spec.ts:13 | limpeza só em `afterAll` | se o teste cair antes, restam reservas e o próximo run falha por conflito | Alta | `beforeEach` apaga reservas da sala |
| reserva.spec.ts:5,7 | `.btn.btn-lg.btn-primary` e XPath absoluto | quebra a cada mudança de layout ou tema | Média | `getByRole('button', { name: 'Entrar' })`, `getByRole('link', { name: 'Salas' })` |
| reserva.spec.ts:2-5 | login pela UI e URL fixa no mesmo teste da reserva | falha de login mascara a regra de reserva; lentidão; ambiente fixo no código | Baixa | projeto de setup autentica; `baseURL` na configuração; o teste só reserva |

Veredito: Precisa de ajuste. Não verificado: execução do teste e comportamento real da API. Revisão feita pelo mesmo modelo que pode ter escrito o teste; não é validação independente.
