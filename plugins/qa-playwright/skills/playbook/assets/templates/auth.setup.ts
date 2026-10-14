// Template do plugin qa-playwright: login uma vez com a conta de TESTE e estado em playwright/.auth/ (V-37, V-23).
// Copie para e2e/auth.setup.ts. Roda só no projeto `setup` da config (E2E_AUTH=1), com trace 'off': o trace grava o valor
// digitado no fill, inclusive a senha (V-24). Verificado no sistema-demo (X-23): contra a instância de exploração
// (E2E_PORT=4173 E2E_REUSE=1), gerou user-4173.json sem trace; ajuste rota, rótulos e o estado final ao seu sistema.
//
// De onde vem a conta de teste, nesta ordem:
//   1. conta sintética do seed, fixture ou exemplo de config do próprio projeto, só para o sistema local;
//   2. variável que o usuário já exportou no ambiente (staging). Nunca peça senha no chat;
//   3. cadastro pelo próprio sistema local, com dados sintéticos.
// Sem nenhuma das três, as funcionalidades com login ficam `Bloqueado`, com decisão pendente.
// SSO, MFA e CAPTCHA de terceiro: não contornar (G-33).
import { test as setup, expect } from '@playwright/test';

// Igual ao AUTH da config; a pasta é ignorada pelo git (gitignore-trecho.txt).
const authFile = `playwright/.auth/user-${process.env.E2E_PORT ?? 4174}.json`;

setup('autenticar com a conta de teste', async ({ page }) => {
  const user = process.env.E2E_USER;
  const pass = process.env.E2E_PASSWORD;
  if (!user || !pass) {
    // Não imprima os valores.
    throw new Error('Defina E2E_USER e E2E_PASSWORD (conta de teste). Nunca use credencial real.');
  }
  await page.goto('/login');
  await page.getByLabel('E-mail').fill(user);
  await page.getByLabel('Senha').fill(pass);
  await page.getByRole('button', { name: 'Entrar' }).click();
  await page.waitForURL('**/painel');                                  // estado final observável (V-37)
  await expect(page.getByRole('button', { name: 'Sair' })).toBeVisible();
  await page.context().storageState({ path: authFile });
});

// Notas
// - Mantenha ao menos um teste de login real pela UI fora do setup (prática de guias; Não verificado como fonte oficial).
// - sessionStorage não entra no storageState (V-37); IndexedDB entra.
// - O arquivo de estado vale como credencial: não ler, não imprimir, não anexar a relatório, apagar ao fim.
//   Passar o CAMINHO dele ao storageState ou ao `npx playwright cli state-load` é permitido (G-17, G-21).
// - Várias contas por papel: um arquivo por papel e test.use({ storageState }) por arquivo ou describe (V-38).
