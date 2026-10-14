// Template do plugin qa-playwright. Copie para a pasta que tem o package.json do @playwright/test
// (config e package.json juntos: X-17). Ajuste só as variáveis do bloco "AJUSTE".
// Verificado por execução no Windows com Playwright 1.64.0 (X-17, X-18, X-23, X-24, X-25): núcleo, saída por E2E_RUN,
// login pelo projeto `setup` com estado por porta e o gate. O modelo parte da configuração da Microsoft Playwright,
// Apache-2.0 (adaptado). Não verificado: PW_CHANNEL=msedge ou chromium sem Chromium baixado (S-09).
import { defineConfig } from '@playwright/test';

// ---- AJUSTE ---------------------------------------------------------------------------------------
const PORT = Number(process.env.E2E_PORT ?? 4174);       // instância de TESTE. A exploração usa outra porta (ex.: 4173).
const BASE = `http://127.0.0.1:${PORT}`;                  // sempre 127.0.0.1, nunca 0.0.0.0 (G-22)
const CHANNEL = process.env.PW_CHANNEL ?? 'chrome';       // chrome | msedge usam o navegador instalado, sem download (X-04); chromium exige `install chromium`
const COM_LOGIN = process.env.E2E_AUTH === '1';           // liga o projeto `setup` e o estado de login (X-23)
const AUTH = `playwright/.auth/user-${PORT}.json`;        // um estado por porta, gerado contra a instância certa (X-23)
// ---------------------------------------------------------------------------------------------------

// O outputDir é limpo no início de cada execução (docs oficiais, class-testconfig). Por isso cada execução grava na própria
// pasta e uma não apaga o trace da outra (X-18). Execução de evidência: E2E_RUN=<id>. Sem ele, a pasta é 'local'.
const RUN = process.env.E2E_RUN ?? 'local';
const OUT = `test-results/${RUN}`;
const REPORT = `playwright-report/${RUN}`;

export default defineConfig({
  testDir: 'e2e',
  outputDir: OUT,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,                        // rodada local sem retry: a falha aparece como falha (X-17)
  workers: process.env.CI ? 1 : undefined,
  timeout: 30_000,
  expect: { timeout: 5_000 },
  globalTimeout: 30 * 60 * 1000,                          // o relatório sai mesmo se a execução travar (V-42)
  // Não passe --reporter na linha de comando: ele substitui esta lista e o HTML/JSON não saem (X-16).
  reporter: [
    ['list'],
    ['html', { open: 'never', outputFolder: REPORT }],    // open: 'never' impede o servidor do relatório de prender o agente (V-44)
    ['json', { outputFile: `${OUT}/results.json` }],      // lido pelo evidence-report e pelo matrix-auditor (X-18)
  ],
  use: {
    baseURL: BASE,
    ...(CHANNEL === 'chromium' ? {} : { channel: CHANNEL }),
    trace: 'retain-on-failure',                           // com retries 0, 'on-first-retry' não grava nada (V-39, V-45)
    screenshot: 'only-on-failure',
    actionTimeout: 10_000,
    navigationTimeout: 15_000,
  },
  projects: COM_LOGIN
    ? [
        // trace 'off' no setup: o trace grava o valor digitado no fill, inclusive a senha (V-24); sem trace do setup (X-23)
        { name: 'setup', testMatch: /.*\.setup\.ts/, use: { trace: 'off' } },
        { name: 'desktop', dependencies: ['setup'], use: { storageState: AUTH } },
      ]
    : [{ name: 'desktop' }],                              // o testMatch padrão não pega *.setup.ts: sem testIgnore (X-25)
  webServer: {
    command: process.env.E2E_SERVER_CMD ?? 'npm run start',   // precisa ligar em 127.0.0.1:${PORT}
    url: `${BASE}${process.env.E2E_HEALTH_PATH ?? '/'}`,      // health: 2xx, 3xx, 400, 401, 402 ou 403 contam como pronto (V-39)
    env: { PORT: String(PORT) },
    reuseExistingServer: process.env.E2E_REUSE === '1',       // padrão: instância própria, sem o estado da exploração (X-17)
    timeout: 120_000,
    stdout: 'pipe',
  },
});

// Evidência, bash:        E2E_RUN=20261013T1030-evidencia npx playwright test --grep "F-01|F-02"
// Evidência, PowerShell:  $env:E2E_RUN='20261013T1030-evidencia'; npx playwright test --grep "F-01|F-02"; Remove-Item Env:E2E_RUN
// (a variável fica na sessão do PowerShell; sem o Remove-Item, a próxima execução limparia a mesma pasta)
// Nunca use `--%` com npx (X-16). gracefulShutdown é ignorado no Windows: o servidor é encerrado à força (V-39).
