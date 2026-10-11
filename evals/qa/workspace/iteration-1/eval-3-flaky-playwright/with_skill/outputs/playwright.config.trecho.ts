// Trecho (não é o arquivo inteiro): o que mexer no seu playwright.config.ts para diagnosticar e estabilizar.
// Não executado; confira os nomes das opções na versão do Playwright que você usa.
import { defineConfig } from '@playwright/test';

const CI = !!process.env.CI;

export default defineConfig({
  retries: CI ? 1 : 0,           // retry mostra o flaky no relatório; mais que 2 esconde defeito
  workers: CI ? 2 : undefined,   // fixe no CI; container pode reportar núcleos errados
  use: {
    baseURL: process.env.BASE_URL, // some a URL fixa dos testes
    actionTimeout: 10_000,         // padrão é sem limite: clique travado consome os 30 s do teste
    trace: 'retain-on-failure',    // guarda a PRIMEIRA falha (on-first-retry grava a reexecução, que pode ter passado)
    screenshot: 'only-on-failure',
  },
});
