import { test, expect, type Page } from '@playwright/test';

// Requer @playwright/test >= 1.29 (getByRole, expect(...).toPass).
// Os pontos marcados com "AJUSTAR" usam nomes acessíveis que eu SUPUS.
// Troque pelo que a tela realmente expõe (ideal: pedir data-testid ao time de front).

test.use({ baseURL: 'https://loja-homolog.exemplo.com.br' });

async function login(page: Page) {
  await page.goto('/login');
  await page.locator('#email').fill('qa@exemplo.com.br');
  await page.locator('#senha').fill('Senha@123');
  await page.getByRole('button', { name: /entrar/i }).click(); // AJUSTAR (era '.btn-primary')
  // Espera o login terminar de verdade, em vez de dormir 3s.
  await page.waitForURL((url) => !url.pathname.endsWith('/login'));
}

// O histórico depende do pedido criado no checkout, então os dois passos viram UM teste.
// Antes, o 2º teste lia uma variável de módulo preenchida pelo 1º: qualquer retry,
// falha anterior, --shard ou fullyParallel reiniciava o worker e a variável vinha undefined.
test('pedido com cartão é criado e aparece no histórico como Aprovado', async ({ page }) => {
  test.setTimeout(90_000); // login + gateway de pagamento + espera de status
  let numeroPedido = '';

  await test.step('login', async () => {
    await login(page);
  });

  await test.step('adiciona o produto ao carrinho', async () => {
    await page.goto('/produto/123');
    await page.getByRole('button', { name: /adicionar ao carrinho/i }).click(); // AJUSTAR (era '.add-to-cart')

    // Só sai da página depois que o item entrou no carrinho. Antes o teste clicava no
    // link do carrinho logo após o clique, e a navegação podia abortar a requisição.
    const carrinho = page.getByRole('link', { name: /carrinho/i }); // AJUSTAR (era 'div.header > div:nth-child(3) > a')
    await expect(carrinho).toContainText('1'); // AJUSTAR: use o sinal que a tela dá (badge, toast...)
    await carrinho.click();
  });

  await test.step('finaliza com cartão', async () => {
    await page.getByRole('button', { name: /finalizar/i }).click(); // AJUSTAR (era 'text=Finalizar')
    // Escolhe a opção pelo nome, não pela posição (era '.payment-option >> nth=1').
    await page.getByRole('radio', { name: /cartão/i }).check(); // AJUSTAR
    await page.locator('#confirmar').click();

    const numero = page.locator('.order-number');
    // Espera o número ser preenchido. textContent() devolve na hora, mesmo vazio.
    await expect(numero).toHaveText(/\S+/, { timeout: 20_000 }); // se souber o formato, use-o (ex.: /^\d{6,}$/)
    numeroPedido = (await numero.innerText()).trim();
  });

  await test.step('pedido aparece no histórico como Aprovado', async () => {
    // A linha é localizada pelo número do pedido. Antes era "a 2ª linha da tabela",
    // que quebra se a conta QA for compartilhada com outras execuções do CI.
    const status = page.getByRole('row').filter({ hasText: numeroPedido }).locator('.status');

    // Se o status muda de forma assíncrona (callback do gateway), recarrega e tenta de novo
    // até um limite explícito. Se o status DEVERIA estar Aprovado de imediato, retire este
    // toPass: ele esconderia um problema real da aplicação.
    await expect(async () => {
      await page.goto('/minha-conta/pedidos');
      await expect(status).toHaveText('Aprovado', { timeout: 2_000 });
    }).toPass({ timeout: 30_000, intervals: [1_000, 2_000, 5_000] });
  });
});
