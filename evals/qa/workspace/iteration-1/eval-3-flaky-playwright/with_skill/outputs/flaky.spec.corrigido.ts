import { test, expect, type Page } from '@playwright/test';

// Não executado: não tenho acesso ao seu ambiente de homologação nem ao DOM real.
// Tudo marcado com "AJUSTE" é suposição minha sobre a loja; confirme no trace.
//
// Variáveis de ambiente (segredos do CI, nunca no código):
//   BASE_URL, E2E_USER, E2E_PASSWORD
// Rodar: BASE_URL=https://loja-homolog.exemplo.com.br npx playwright test flaky.spec.corrigido.ts

const EMAIL = process.env.E2E_USER!;
const SENHA = process.env.E2E_PASSWORD!;

// AJUSTE: rota da API chamada pelo botão "adicionar ao carrinho" (veja a aba Network do trace).
const ADICIONA_AO_CARRINHO = /\/api\/carrinho/;

async function entrar(page: Page) {
  await page.goto('/login');
  await page.locator('#email').fill(EMAIL);
  await page.locator('#senha').fill(SENHA);
  await page.getByRole('button', { name: 'Entrar' }).click();
  // Sinal POSITIVO de login concluído; substitui waitForTimeout(3000).
  // AJUSTE: qualquer elemento que só existe logado.
  await expect(page.getByRole('link', { name: 'Minha conta' })).toBeVisible();
}

// Os dois testes originais viraram um só: o segundo dependia do número do pedido
// criado pelo primeiro (variável de módulo), o que quebra com retry, worker novo,
// fullyParallel, shard ou --grep. Uma jornada sequencial é um único cenário.
test('cria pedido com cartão e o pedido aparece no histórico como Aprovado', async ({ page }) => {
  test.slow(); // jornada longa + aprovação assíncrona: 90 s em vez de 30 s, só neste teste

  await entrar(page);

  await test.step('adiciona o produto 123 ao carrinho', async () => {
    await page.goto('/produto/123');
    // Registre a espera ANTES do clique que dispara a requisição.
    const adicionou = page.waitForResponse(
      (r) => ADICIONA_AO_CARRINHO.test(r.url()) && r.request().method() === 'POST',
    );
    await page.getByRole('button', { name: 'Adicionar ao carrinho' }).click();
    expect((await adicionou).ok()).toBe(true);
  });

  await test.step('abre o carrinho e confere que só há o item esperado', async () => {
    await page.getByRole('link', { name: /carrinho/i }).click();
    await expect(page).toHaveURL(/\/carrinho/);
    // Conta compartilhada: item deixado por outra execução vira falha clara aqui,
    // em vez de pedido com total errado lá na frente. AJUSTE: data-testid.
    await expect(page.getByTestId('item-carrinho')).toHaveCount(1);
  });

  let numeroPedido: string;

  await test.step('finaliza a compra pagando com cartão', async () => {
    await page.getByRole('button', { name: 'Finalizar compra' }).click();
    await page.getByRole('radio', { name: /cartão/i }).check(); // por nome, não por posição (nth=1)
    await page.getByRole('button', { name: 'Confirmar pedido' }).click();

    const numero = page.locator('.order-number');
    await expect(numero).toHaveText(/\d+/); // espera o número chegar (vazio ou "Processando…" reprova)
    numeroPedido = (await numero.innerText()).match(/\d+/)![0]; // AJUSTE: formato do número
  });

  await test.step('o pedido aparece no histórico e é aprovado', async () => {
    await page.goto('/minha-conta/pedidos');
    // Linha identificada pelo número do pedido, não por "primeira linha da tabela".
    const linha = page.getByRole('row').filter({ hasText: numeroPedido });

    // Aprovação (gateway/webhook) e listagem são assíncronas: recarrega até aparecer,
    // com limite. AJUSTE o timeout para o tempo máximo aceitável de aprovação em homologação.
    await expect(async () => {
      await page.reload();
      await expect(linha).toHaveCount(1, { timeout: 2_000 });
      await expect(linha.locator('.status')).toHaveText('Aprovado', { timeout: 2_000 });
    }).toPass({ timeout: 30_000, intervals: [1_000, 2_000, 5_000] });
  });
});
