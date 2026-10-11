Ajudo sim. Li o `flaky.spec.ts` e o problema não é um só: há pelo menos cinco pontos que passam numa máquina rápida e sozinha e falham num runner de CI mais lento, concorrido, com retry. Um aviso antes: não consegui rodar nada (o ambiente `loja-homolog` é fictício aqui e não tenho o Playwright instalado). O que segue é **análise do código**, não resultado medido. Abaixo digo como confirmar qual deles é o seu em uma rodada.

## Suspeitos, do mais ao menos provável para "3 em 10, só no CI"

| # | Trecho | Por que falha só às vezes | O que aparece no trace |
| --- | --- | --- | --- |
| 1 | `waitForTimeout(3000)` depois do login (linhas 10 e 29) e `waitForTimeout(2000)` antes do pagamento (16) | Espera por tempo fixo: se o login demora 3,2 s no CI, o `goto` seguinte cancela a navegação ou chega sem sessão | URL `/login` no passo seguinte; `.add-to-cart` ou `.order-number` não encontrado; "navigation interrupted by another navigation" |
| 2 | Conta `qa@exemplo.com.br` única, `table tr` `nth(1)` e `.status` `first()` (linhas 32 a 34) | Se outro job do CI (outro PR, outro shard) usa a mesma conta ao mesmo tempo, a primeira linha da tabela é o pedido dele, e o carrinho pode ter item de outra execução. Local você roda sozinho. É o que melhor explica "só no CI" | o texto recebido contém outro número de pedido; carrinho com 2 itens |
| 3 | `.status` lido uma vez com `textContent()` (linha 34) | Aprovação de pagamento costuma ser assíncrona (gateway/webhook). `textContent()` não espera nem repete: se ainda está "Pendente", reprova | recebido "Pendente"/"Aguardando", esperado "Aprovado" |
| 4 | Clique em `.add-to-cart` seguido de clique no carrinho por posição, `div.header > div:nth-child(3) > a` (13 e 14) | Navega para o carrinho antes de a requisição de adicionar terminar: carrinho vazio, `text=Finalizar` não aparece. O seletor por posição também quebra com qualquer elemento a mais no cabeçalho | timeout em `text=Finalizar`; requisição de carrinho pendente na aba Network |
| 5 | `numeroPedido` como variável de módulo (linha 3) | O 2º teste depende do 1º. Se o 1º falha e o Playwright reinicia o worker, ou se o CI usa `fullyParallel`/shard, o 2º roda com `numeroPedido` indefinido e conta como segunda falha. Sozinho isso falharia sempre, não 3 em 10; ele **amplifica** os outros: uma falha vira duas | falha no 2º teste sem nenhum erro de tela |

Também são frágeis (não explicam o 3 em 10 sozinhos): `.payment-option >> nth=1` (se a ordem das opções mudar, paga com outra forma e o teste se chama "com cartão"), `.btn-primary` e `.add-to-cart` (classe genérica que pode casar com 2 elementos e dar erro de modo estrito).

## Como confirmar em uma rodada (no runner do CI, que é onde falha)

```bash
# 1) em série, sem retry, guardando o trace da primeira falha
npx playwright test flaky.spec.ts --repeat-each=30 --workers=1 --retries=0 --trace=retain-on-failure
# 2) o mesmo em paralelo
npx playwright test flaky.spec.ts --repeat-each=30 --workers=4 --retries=0 --trace=retain-on-failure
npx playwright show-trace test-results/<pasta-da-falha>/trace.zip
```

Como ler: falhou só no passo 2 (ou só quando há outro job rodando) aponta para conta e dados compartilhados (#2 e #5). Falhou também em série, sempre na mesma linha, aponta para sincronização (#1, #3, #4). Linhas diferentes a cada falha indicam ambiente lento ou instável. Agrupe as falhas pela mensagem do primeiro erro. Se contar "3 em 10" por execução do CI, conte só a primeira falha de cada uma, senão o efeito do #5 infla o número. Duas ressalvas: 30 execuções verdes não provam estabilidade (0 de 30 ainda é compatível com taxa de até uns 10%), e o `trace: 'on-first-retry'`, que muita config usa, grava a reexecução, que pode ter passado. Use `retain-on-failure` para diagnosticar.

## Versão corrigida

Fundi os dois testes em um só com passos, porque é uma jornada sequencial e o segundo dependia do primeiro. Troquei cada espera por tempo por uma espera por condição, localizo a linha do histórico pelo número do pedido (não pela posição), reconfiro o status com recarga e limite de tempo, e tirei a URL e a senha do código. Salvei em `flaky.spec.corrigido.ts`:

```ts
import { test, expect, type Page } from '@playwright/test';

// Variáveis de ambiente (segredos do CI, nunca no código): BASE_URL, E2E_USER, E2E_PASSWORD
const EMAIL = process.env.E2E_USER!;
const SENHA = process.env.E2E_PASSWORD!;

// AJUSTE: rota da API chamada pelo botão "adicionar ao carrinho" (aba Network do trace).
const ADICIONA_AO_CARRINHO = /\/api\/carrinho/;

async function entrar(page: Page) {
  await page.goto('/login');
  await page.locator('#email').fill(EMAIL);
  await page.locator('#senha').fill(SENHA);
  await page.getByRole('button', { name: 'Entrar' }).click();
  // Sinal positivo de login concluído; substitui waitForTimeout(3000).
  // AJUSTE: qualquer elemento que só existe logado.
  await expect(page.getByRole('link', { name: 'Minha conta' })).toBeVisible();
}

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
    // Conta compartilhada: item de outra execução vira falha clara aqui, não pedido
    // com total errado lá na frente. AJUSTE: data-testid.
    await expect(page.getByTestId('item-carrinho')).toHaveCount(1);
  });

  let numeroPedido: string;

  await test.step('finaliza a compra pagando com cartão', async () => {
    await page.getByRole('button', { name: 'Finalizar compra' }).click();
    await page.getByRole('radio', { name: /cartão/i }).check(); // por nome, não por posição
    await page.getByRole('button', { name: 'Confirmar pedido' }).click();

    const numero = page.locator('.order-number');
    await expect(numero).toHaveText(/\d+/); // vazio ou "Processando…" reprova
    numeroPedido = (await numero.innerText()).match(/\d+/)![0]; // AJUSTE: formato do número
  });

  await test.step('o pedido aparece no histórico e é aprovado', async () => {
    await page.goto('/minha-conta/pedidos');
    const linha = page.getByRole('row').filter({ hasText: numeroPedido });

    // Aprovação e listagem são assíncronas: recarrega até aparecer, com limite.
    // AJUSTE o timeout ao tempo máximo aceitável de aprovação em homologação.
    await expect(async () => {
      await page.reload();
      await expect(linha).toHaveCount(1, { timeout: 2_000 });
      await expect(linha.locator('.status')).toHaveText('Aprovado', { timeout: 2_000 });
    }).toPass({ timeout: 30_000, intervals: [1_000, 2_000, 5_000] });
  });
});
```

E no `playwright.config.ts` (trecho em `playwright.config.trecho.ts`): `baseURL: process.env.BASE_URL`, `trace: 'retain-on-failure'`, `actionTimeout: 10_000`, `retries: 1` no CI e `workers` fixo. Retry no máximo 1 ou 2: acima disso ele esconde o problema em vez de mostrá-lo.

**Importante:** não executei esse código, só conferi que o arquivo é sintaticamente válido (checagem de sintaxe com Node, sem o Playwright e sem tipos). Os trechos marcados `AJUSTE` são suposições minhas sobre o DOM e a API da sua loja (nome do botão "Entrar", `data-testid="item-carrinho"`, rota do carrinho, formato do número do pedido). Se os elementos não tiverem nome acessível, peça ao time de front um `data-testid`. Depois de ajustar, rode `--repeat-each=30` no CI (150 se quiser mais confiança) antes de dar por resolvido.

## O que mais encontrei (mesmo sem você perguntar)

- **Falso verde no teste 1.** `expect(numeroPedido).toBeTruthy()` passa com qualquer texto não vazio, inclusive "Erro ao processar". O teste não verifica a forma de pagamento, os itens nem o total. O total esperado deve ser calculado de forma independente (preço do produto × quantidade, não copiado da tela). Não incluí porque não conheço o preço do produto 123. Adicione assim que souber.
- **Senha no código.** `Senha@123` está no arquivo e portanto no histórico do git. Mova para segredo do CI e, se essa senha for usada em qualquer outro lugar, troque.
- **Conta compartilhada é o risco que sobra.** Minha versão detecta carrinho sujo e acha o pedido certo no histórico, mas dois jobs usando o mesmo carrinho ao mesmo tempo ainda podem se atrapalhar. A correção de verdade é uma conta por worker ou por shard (ex.: `e2e+<parallelIndex>@exemplo.com.br`), se a loja permitir criar contas de teste.
- **Dados que ficam.** Cada execução deixa um pedido aprovado em homologação. Se houver endpoint de cancelamento ou limpeza de teste, use no final.
- **Próximo passo de arrumação (opcional).** Login uma vez só via projeto `setup` com `storageState`, e o pedido do teste de histórico criado por API numa fixture, para ele não depender do checkout pela tela.

## O que eu não sei e que mudaria o diagnóstico

1. Qual é a **mensagem e a linha do primeiro erro** nas falhas do CI? É o dado que sozinho mais estreita a causa; se me mandar 2 ou 3 delas, aponto o suspeito exato.
2. O `playwright.config.ts` usa `fullyParallel`, `--shard` ou `retries`? E quantos `workers` no CI?
3. Mais de um job do CI (ou pessoa) usa `qa@exemplo.com.br` ao mesmo tempo?
4. A aprovação do pagamento em homologação é assíncrona? Quanto tempo leva no pior caso razoável? Isso define o `timeout` do `toPass`.
5. O carrinho persiste por conta entre execuções? E o cartão usado é um cartão salvo na conta (o teste original não digita dados de cartão)?
