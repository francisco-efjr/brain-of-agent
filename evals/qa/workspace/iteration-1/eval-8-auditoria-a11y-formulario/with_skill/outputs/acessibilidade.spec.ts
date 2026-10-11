// Regressão de acessibilidade do cadastro. NÃO EXECUTADO: o ambiente desta auditoria
// não tinha Playwright, axe-core nem rede. Rode no projeto e ajuste ao que aparecer.
//
// Requisitos: @playwright/test >= 1.45 (page.clock), @axe-core/playwright, e a página
// servida pelo baseURL do playwright.config.ts. Por padrão testa a versão corrigida;
// para ver os defeitos do original: PAGINA=/cadastro.html npx playwright test acessibilidade
import { test, expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const PAGINA = process.env.PAGINA ?? '/cadastro-corrigido.html';
const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];

async function varrer(page: Page) {
  return (await new AxeBuilder({ page }).withTags(TAGS).analyze()).violations;
}

function resumo(violacoes: Awaited<ReturnType<typeof varrer>>): string {
  return violacoes
    .map((v) => `[${v.impact}] ${v.id}: ${v.help}\n  ${v.nodes.map((n) => n.target.join(' ')).join('\n  ')}`)
    .join('\n');
}

async function preencherValido(page: Page) {
  await page.getByLabel('Nome completo').fill('Maria da Silva');
  await page.getByLabel('CPF').fill('529.982.247-25'); // CPF sintético válido
  await page.getByLabel('Data de nascimento').fill('25/12/1950');
  await page.getByLabel('E-mail').fill('maria@exemplo.com');
  await page.getByLabel('Crie uma senha').fill('senha-de-teste-8');
}

const termos = (page: Page) => page.getByRole('checkbox', { name: /Li e aceito/ });
const enviar = (page: Page) => page.getByRole('button', { name: 'Enviar cadastro' });

test.beforeEach(async ({ page }) => {
  await page.goto(PAGINA);
  await expect(page.getByRole('main')).toBeVisible();
});

test('sem violações WCAG 2.2 AA na tela inicial', async ({ page }) => {
  const violacoes = await varrer(page);
  expect(violacoes, resumo(violacoes)).toEqual([]);
});

test('sem violações WCAG 2.2 AA com o formulário em erro', async ({ page }) => {
  await enviar(page).click();
  await expect(page.getByRole('alert')).toBeFocused(); // foco vai ao resumo de erros
  const violacoes = await varrer(page);
  expect(violacoes, resumo(violacoes)).toEqual([]);
});

test('erro de CPF fica ligado ao campo e é lido junto com ele', async ({ page }) => {
  await preencherValido(page);
  await page.getByLabel('CPF').fill('123.456.789-00'); // dígitos verificadores errados
  await termos(page).check();
  await enviar(page).click();
  const cpf = page.getByLabel('CPF');
  await expect(cpf).toHaveAttribute('aria-invalid', 'true');
  await expect(cpf).toHaveAccessibleDescription(/CPF inválido/);
});

test('dá para concluir o cadastro só com teclado', async ({ page }) => {
  await preencherValido(page);
  await termos(page).focus();
  await page.keyboard.press('Space');
  await page.keyboard.press('Tab'); // link "termos de uso"
  await page.keyboard.press('Tab'); // botão
  await expect(enviar(page)).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('status')).toHaveText('Cadastro realizado com sucesso.');
});

test('confirmação de sucesso não some sozinha (2.2.1)', async ({ page }) => {
  await page.clock.install();
  await page.goto(PAGINA);
  await preencherValido(page);
  await termos(page).check();
  await enviar(page).click();
  await expect(page.getByRole('status')).toHaveText('Cadastro realizado com sucesso.');
  await page.clock.fastForward(10_000);
  await expect(page.getByRole('status')).toHaveText('Cadastro realizado com sucesso.');
});

test('campo recebe contorno de foco visível com Tab real (2.4.7)', async ({ page }) => {
  await page.keyboard.press('Tab'); // Tab real: focus() programático pode não ativar :focus-visible
  const campo = page.getByLabel('Nome completo');
  await expect(campo).toBeFocused();
  const contorno = await campo.evaluate((el) => {
    const s = getComputedStyle(el);
    return { estilo: s.outlineStyle, largura: parseFloat(s.outlineWidth) };
  });
  expect(contorno.estilo).not.toBe('none');
  expect(contorno.largura).toBeGreaterThanOrEqual(2);
});

test('sem rolagem horizontal em 320 px (1.4.10)', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 640 });
  const sobra = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(sobra).toBeLessThanOrEqual(0);
});
