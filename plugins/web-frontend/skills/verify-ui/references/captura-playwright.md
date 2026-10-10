# Captura de evidência com Playwright (script de apoio para verify-ui)

Redação própria, a partir de V-08 (reconhecimento), V-36 (procedimento) e V-20 (esperas). O plugin não instala Playwright e não baixa navegadores: use só se o projeto já o tem (`@playwright/test` no `package.json`). O script é gerado por você numa pasta de artefatos (projeto ou scratchpad da sessão), executado com autorização do usuário e não é versionado. Código gerado por agente é código que roda na máquina do usuário: mostre o conteúdo antes de executar.

## Script 1: capturas em duas larguras, overflow e console

```js
// captura-ui.mjs — uso: node captura-ui.mjs <url> <pastaDeArtefatos>
import { chromium } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';

const [url, pasta] = process.argv.slice(2);
if (!url || !pasta) {
  console.error('uso: node captura-ui.mjs <url> <pastaDeArtefatos>');
  process.exit(2);
}
mkdirSync(pasta, { recursive: true });

const larguras = [['mobile-320', 320, 800], ['desktop-1280', 1280, 800]];
const mensagens = [];
const browser = await chromium.launch();
try {
  for (const [nome, width, height] of larguras) {
    const context = await browser.newContext({ viewport: { width, height } });
    const page = await context.newPage();
    page.on('console', (m) => {
      if (m.type() === 'error' || m.type() === 'warning') mensagens.push(`[${nome}] ${m.type()}: ${m.text()}`);
    });
    page.on('pageerror', (e) => mensagens.push(`[${nome}] pageerror: ${e.message}`));

    await page.goto(url);
    await page.getByRole('main').waitFor(); // sinal de conteúdo real; nunca networkidle nem sleep
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    console.log(`${nome}: overflow horizontal = ${overflow}px`);
    await page.screenshot({ path: join(pasta, `${nome}.png`), fullPage: true });
    await context.close();
  }
} finally {
  await browser.close();
}
console.log(mensagens.length ? mensagens.join('\n') : 'console: sem erros nem avisos');
```

Saída esperada: duas linhas `overflow horizontal`, dois PNGs, resumo do console. Se a página não tem `<main>`, o script falha na espera: isso é um achado de semântica (landmark ausente), não um problema do script; use outro sinal (um heading esperado) e registre.

## Script 2: percurso só com teclado (registro de foco)

Acrescente depois do `goto`, no mesmo contexto. Pressiona Tab N vezes e registra onde o foco caiu, para provar ordem, ausência de armadilha e foco que some.

```js
async function descreverFoco(page) {
  return page.evaluate(() => {
    const e = document.activeElement;
    if (!e || e === document.body) return 'body (nenhum elemento focado)';
    const nome = (e.getAttribute('aria-label') || e.textContent || e.getAttribute('name') || '').trim().slice(0, 40);
    const papel = e.getAttribute('role') ? `[role=${e.getAttribute('role')}]` : '';
    return `${e.tagName.toLowerCase()}${papel} "${nome}"`;
  });
}

for (let i = 1; i <= 15; i++) {
  await page.keyboard.press('Tab'); // Tab real: focus() programático pode não ativar :focus-visible
  console.log(`Tab ${i}: ${await descreverFoco(page)}`);
}
```

Leitura da saída: a sequência deve seguir a ordem visual (WCAG 2.4.3); `body` no meio da sequência indica foco perdido; repetição do mesmo elemento indica armadilha (2.1.2). Esse log é Verificado para ordem e foco; o que um leitor de tela anunciaria continua Inferido.

## Script 3: estado de erro

```js
await page.getByRole('button', { name: 'Enviar' }).click();
await page.getByRole('alert').waitFor(); // ou getByText('Informe seu e-mail')
await page.screenshot({ path: join(pasta, 'erro-320.png'), fullPage: true });
```

Ajuste nomes e papéis ao projeto. Se `getByRole('alert')` não existe, o erro pode não estar sendo anunciado: registre o achado em vez de trocar por seletor de classe.

## Cuidados

- `waitForTimeout`, `networkidle` e `force: true` não entram. Espera fixa só como estímulo em gravação de interação (V-63).
- Persistência: depois do envio, `await page.reload()` e confirme que o dado aparece; captura pós-clique não prova gravação.
- Limite de tentativas: duas correções ou três hipóteses (V-62).
- Dados: apenas ambiente local ou fictício; se o login for necessário, o usuário fornece a sessão (por exemplo um `storageState` próprio) e você não digita credenciais.
- Versões: confira a versão instalada do Playwright (`npx playwright --version`); as chamadas acima são estáveis, mas a API de opções pode ganhar campos.
- Windows: use `path.join` e evite caminhos fixos como `/tmp`.
