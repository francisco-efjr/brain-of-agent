# E2E de checkout com Playwright e provedor isolado

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. Fontes: Playwright network, mock, test-fixtures e browser-contexts (V-40, Classe A, páginas lidas) e regras de E2E do awesome-copilot (MIT, V-23, só o padrão). Confira a versão do `@playwright/test` instalada em `package.json` e a doc dessa versão antes de aplicar; as APIs usadas abaixo (`context.route`, `route.fulfill`, `route.abort`, `test.extend`, `serviceWorkers`) constam das páginas lidas.

## Regras (V-40, V-23)

1. Um arquivo `.spec.ts` por fluxo: carrinho, cupom, endereço/frete, pagamento recusado, pagamento aprovado, reenvio (duplo clique/retry).
2. Cada teste roda em contexto de navegador novo (cookies e storage próprios): não dependa da ordem; cada teste cria e limpa o próprio estado por fixture.
3. Provedor de pagamento mockado com `context.route` + `route.fulfill` (cobre também popups e links abertos, ao contrário de `page.route`). Sem tocar na rede real.
4. Um único teste contra o **sandbox** do provedor, com chaves de teste vindas de variável de ambiente; sem chave, o teste é pulado. Nunca produção.
5. `serviceWorkers: 'block'` na configuração: um Service Worker (por exemplo, o do MSW) pode interceptar antes e esconder a requisição de `route`.
6. HAR só para respostas estáveis, revisado em PR; HAR grava cabeçalhos, então nunca com tokens ou dados reais. Sem entrada correspondente (URL, método, payload de POST), a requisição é abortada.
7. Totais conferidos contra cálculo independente em centavos inteiros, nunca contra o valor que a própria tela mostra.
8. Asserções web-first (`await expect(locator)...`), localizadores por papel/rótulo/texto, sem esperas fixas. Teste com asserção trivial não vale como verificação.

## Configuração

```ts
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  use: {
    baseURL: process.env.LOJA_URL ?? 'http://localhost:3000',   // nunca um host de produção
    serviceWorkers: 'block',
    trace: 'on-first-retry',
  },
});
```

## Fixture: carrinho sintético com limpeza

A API `/api/teste/...` abaixo é um exemplo: crie uma rota equivalente, habilitada só em ambiente de teste, ou use o seed do projeto.

```ts
// tests/fixtures.ts
import { test as base, expect } from '@playwright/test';

type Loja = { carrinhoId: string; totalEsperadoCentavos: number };

export const test = base.extend<{ loja: Loja }>({
  loja: async ({ request }, use) => {
    // 2 x R$ 49,90 + frete fixo de R$ 15,00 definido no seed de teste
    const r = await request.post('/api/teste/carrinhos', {
      data: { itens: [{ sku: 'SKU-TESTE-1', qtd: 2 }], cep: '01310100' },
    });
    expect(r.ok()).toBeTruthy();
    const { id } = await r.json();
    await use({ carrinhoId: id, totalEsperadoCentavos: 2 * 4990 + 1500 });
    await request.delete(`/api/teste/carrinhos/${id}`);          // limpeza depois do `use`
  },
});
export { expect };
```

## Specs: recusa, timeout e aprovação sem rede real

```ts
// tests/pagamento.spec.ts
import { test, expect } from './fixtures';

const PSP = 'https://api.psp-exemplo.test/**';     // host do PSP no seu projeto (use o domínio da API de teste dele)

test.describe('pagamento com PSP isolado', () => {
  test('recusa mantém o carrinho e não cria pedido', async ({ page, context, request, loja }) => {
    await context.route(PSP, (route) =>
      route.fulfill({ status: 402, contentType: 'application/json', body: JSON.stringify({ erro: 'cartao_recusado' }) }));

    await page.goto(`/checkout?carrinho=${loja.carrinhoId}`);
    await expect(page.getByTestId('total')).toContainText(/R\$\s*114,80/);   // \s casa o U+00A0 do Intl pt-BR
    await page.getByLabel('Número do cartão').fill('4242 4242 4242 4242');   // cartão de teste público do provedor
    await page.getByRole('button', { name: 'Pagar' }).click();

    await expect(page.getByRole('alert')).toContainText(/recusad/i);
    const pedidos = await request.get(`/api/teste/pedidos?carrinho=${loja.carrinhoId}`);
    expect(await pedidos.json()).toHaveLength(0);                             // efeito no estado, não só na tela
  });

  test('timeout do PSP deixa o pedido pendente e permite nova tentativa', async ({ page, context, loja }) => {
    await context.route(PSP, (route) => route.abort('timedout'));
    await page.goto(`/checkout?carrinho=${loja.carrinhoId}`);
    await page.getByRole('button', { name: 'Pagar' }).click();
    await expect(page.getByRole('alert')).toContainText(/tente novamente/i);
    await expect(page.getByRole('button', { name: 'Pagar' })).toBeEnabled();
  });

  test('duplo clique em Pagar gera uma única cobrança', async ({ page, context, loja }) => {
    let cobrancas = 0;
    await context.route(PSP, async (route) => {
      if (route.request().method() === 'POST') cobrancas++;
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'requires_confirmation' }) });
    });
    await page.goto(`/checkout?carrinho=${loja.carrinhoId}`);
    const pagar = page.getByRole('button', { name: 'Pagar' });
    await pagar.dblclick();
    await expect.poll(() => cobrancas).toBe(1);
  });
});
```

O `expect.poll` do duplo clique só prova que houve ao menos uma chamada ao PSP no momento da leitura; para provar o máximo, confira também no servidor de teste que existe uma só cobrança/pedido para a chave de idempotência (contagem de linhas, como no teste de recusa).

O total `R$ 114,80` vem do oráculo independente da fixture (2 x 4990 + 1500 = 11480 centavos). Se o valor mudar, a divergência está no sistema, não na asserção.

## Um teste real no sandbox

```ts
// tests/sandbox-psp.spec.ts
import { test, expect } from './fixtures';

test('fluxo real contra o sandbox do PSP', async ({ page, loja }) => {
  test.skip(!process.env.PSP_SANDBOX_KEY, 'sem chave de sandbox no ambiente');   // a chave é lida pelo servidor de teste, não pelo teste
  await page.goto(`/checkout?carrinho=${loja.carrinhoId}`);
  // ... preencher com o cartão de teste do provedor e confirmar a aprovação por webhook de sandbox
  await expect(page.getByRole('heading', { name: /pedido confirmado/i })).toBeVisible();
});
```

Conferir: nome da variável, chaves e cartões de teste ficam na doc do seu PSP; o plugin não recebe segredo. Webhook de sandbox chega por encaminhador oficial do provedor (por exemplo `stripe listen`, documentado em `webhook-pagamento`, não executado por esta skill).

## Comando de execução e evidência

```bash
npx playwright test --project=chromium tests/pagamento.spec.ts
```

Cole a saída literal no relatório. Se não rodou, escreva "não executei". CI verde com asserções fracas não prova fluxo funcionando.

## Limites declarados

- Reuso de `storageState` para autenticação e relatórios de trace não foram lidos em V-40: consulte a doc da sua versão.
- Se o formulário de cartão é um iframe do provedor, `context.route` intercepta as requisições dele, mas o preenchimento exige `frameLocator`; o comportamento depende do provedor (Não verificado aqui).
- A API de teste `/api/teste/...` é ilustrativa e precisa existir no seu projeto, desligada em produção.
