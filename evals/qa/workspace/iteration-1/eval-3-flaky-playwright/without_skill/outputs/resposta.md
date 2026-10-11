Li o arquivo. Não consigo rodar contra o homolog daqui, e sem o log de uma falha do CI não dá para cravar uma causa só. Mas há problemas claros no teste, e quase todos explicam "passa local, falha às vezes no CI". Estão em ordem do que eu mais suspeito.

## O que está causando a intermitência

**1. O teste 2 depende do teste 1 por uma variável de módulo (`numeroPedido`).**
Quando um teste falha ou é repetido (retry), o Playwright reinicia o worker, e a variável some. O mesmo acontece com `--shard` e `fullyParallel`. Resultado no CI: qualquer oscilação no teste 1 faz o teste 2 falhar com `Expected substring: undefined`, mesmo que o 1 passe no retry. Localmente tudo roda em ordem, no mesmo worker, e funciona.

**2. Corrida no carrinho.**
O teste clica em `.add-to-cart` e, na linha seguinte, já clica no link do carrinho. Se a requisição de adicionar ainda estiver em voo, a navegação pode abortá-la e o carrinho chega vazio. O `waitForTimeout(2000)` depois de "Finalizar" esconde isso localmente, mas no CI (mais lento) não basta.

**3. Esperas fixas no lugar de esperas por estado.**
`waitForTimeout(3000)` depois do login e `waitForTimeout(2000)` no checkout só funcionam enquanto a máquina for rápida. É o padrão clássico de teste que passa local e falha no CI.

**4. `textContent()` não espera o texto aparecer.**
Ele espera o elemento existir, mas devolve na hora, mesmo vazio. Se `.order-number` aparece antes de ser preenchido, `numeroPedido` fica `""` e o `toBeTruthy()` falha.

**5. O histórico assume que o pedido é a 2ª linha e que o status já é "Aprovado".**
- `table tr >> nth(1)` só serve se a conta `qa@` não tiver outros pedidos entrando ao mesmo tempo. Num CI com várias execuções ou jobs usando a mesma conta, a primeira linha pode ser de outro pedido.
- `.status` `.first()` não está amarrado àquela linha.
- Se o status só vira "Aprovado" depois de um callback do gateway, `textContent()` + `toBe` lê uma vez só e vê "Pendente". Isso também explica uma taxa de falha em torno de 30%.

**6. Seletores frágeis.**
`div.header > div:nth-child(3) > a`, `.payment-option >> nth=1` e `.btn-primary` quebram com qualquer mudança de layout, ou se a ordem das opções de pagamento mudar (feature flag, carregamento assíncrono). Escolher "a 2ª opção" como se fosse "cartão" é um risco à parte.

## Como confirmar qual deles é o seu (5 minutos)

Olhe a mensagem das falhas do CI:

| Erro | Causa provável |
|---|---|
| `Expected substring: undefined` no teste 2 | 1 (acoplamento) |
| Timeout em `Finalizar`, ou carrinho vazio | 2 ou 3 |
| `Expected: "Aprovado"  Received: "Pendente"` | 5 (status assíncrono) |
| `numeroPedido` vazio no teste 1 | 4 |
| Linha com outro número de pedido | 5 (conta compartilhada) |

Para reproduzir localmente com o comportamento do CI:

```
npx playwright test flaky.spec.ts --repeat-each=30 --workers=4
```

No `playwright.config.ts`, deixe `trace: 'on-first-retry'` e suba o `playwright-report` como artefato do CI. Assim a próxima falha já vem com o trace.

## Versão corrigida

Salvei em `flaky.fixed.spec.ts` (mesma pasta desta resposta). Não alterei o seu arquivo original. Resumo do que mudou:

- **Um teste só, com `test.step`**, em vez de dois acoplados. O número do pedido passa a ser uma variável local, e o problema 1 some. (Alternativa, se você quiser o histórico como teste separado: criar o pedido via API em um `beforeAll`/fixture e testar só a tela de histórico.)
- **Sem `waitForTimeout`.** Login espera `waitForURL`. A ida ao carrinho espera o item aparecer. O número do pedido usa `expect(...).toHaveText(/\S+/)`.
- **O histórico acha a linha pelo número do pedido** e espera o status com `expect(...).toPass()` (recarrega a página e tenta de novo, até 30 s).
- **Seletores por papel/nome acessível** (`getByRole`) e `baseURL` em vez da URL repetida.
- `test.setTimeout(90_000)`, porque o fluxo inteiro passa dos 30 s padrão.

```ts
import { test, expect, type Page } from '@playwright/test';

test.use({ baseURL: 'https://loja-homolog.exemplo.com.br' });

async function login(page: Page) {
  await page.goto('/login');
  await page.locator('#email').fill('qa@exemplo.com.br');
  await page.locator('#senha').fill('Senha@123');
  await page.getByRole('button', { name: /entrar/i }).click(); // AJUSTAR
  await page.waitForURL((url) => !url.pathname.endsWith('/login'));
}

test('pedido com cartão é criado e aparece no histórico como Aprovado', async ({ page }) => {
  test.setTimeout(90_000);
  let numeroPedido = '';

  await test.step('login', async () => { await login(page); });

  await test.step('adiciona o produto ao carrinho', async () => {
    await page.goto('/produto/123');
    await page.getByRole('button', { name: /adicionar ao carrinho/i }).click(); // AJUSTAR
    const carrinho = page.getByRole('link', { name: /carrinho/i });             // AJUSTAR
    await expect(carrinho).toContainText('1');                                  // AJUSTAR
    await carrinho.click();
  });

  await test.step('finaliza com cartão', async () => {
    await page.getByRole('button', { name: /finalizar/i }).click();             // AJUSTAR
    await page.getByRole('radio', { name: /cartão/i }).check();                 // AJUSTAR
    await page.locator('#confirmar').click();
    const numero = page.locator('.order-number');
    await expect(numero).toHaveText(/\S+/, { timeout: 20_000 });
    numeroPedido = (await numero.innerText()).trim();
  });

  await test.step('pedido aparece no histórico como Aprovado', async () => {
    const status = page.getByRole('row').filter({ hasText: numeroPedido }).locator('.status');
    await expect(async () => {
      await page.goto('/minha-conta/pedidos');
      await expect(status).toHaveText('Aprovado', { timeout: 2_000 });
    }).toPass({ timeout: 30_000, intervals: [1_000, 2_000, 5_000] });
  });
});
```

## Atenção antes de usar

- **Não consegui executar o teste** (o homolog é fictício aqui e o Playwright não está instalado). Escrevi a versão corrigida sem rodá-la. Os nomes marcados com `AJUSTAR` (botão "Entrar", "Adicionar ao carrinho", link "Carrinho", rádio "Cartão", botão "Finalizar") são **suposições minhas** sobre a tela. Confira no DOM, ou peça `data-testid` ao time de front e use `getByTestId`.
- **O `toPass` no histórico pode esconder um bug real.** Se o produto diz que o pedido deveria aparecer como "Aprovado" na hora, o certo é tirar o `toPass` e abrir um bug. Se o status é assíncrono, mantenha e ajuste o tempo ao SLA do gateway.
- **O teste não preenche dados de cartão.** Estou supondo que o homolog usa um cartão salvo ou um fluxo simulado. Se o fluxo mudar, isso é outra fonte de variação.
- **Dado compartilhado continua sendo risco.** Conta `qa@` única, produto 123 (pode acabar o estoque) e carrinho que sobra de execuções interrompidas. O ideal é uma conta por worker ou execução, ou limpar o carrinho por API no início. Eu não inventei endpoint para isso.
- **Fora do escopo, mas vale mencionar:** a senha está escrita no repositório. Mova para variável de ambiente/secret do CI.
- **`retries` no CI ajudam a destravar o pipeline, mas não resolvem.** Use 1 ou 2 no máximo e acompanhe os testes marcados como "flaky" no relatório, senão a intermitência fica invisível.

Se você me mandar a mensagem de erro de uma ou duas falhas do CI (ou o trace), eu confirmo qual dessas causas é a sua e ajusto a correção.
