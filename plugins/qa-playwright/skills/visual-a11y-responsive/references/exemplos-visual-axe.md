# Exemplos: responsivo, visual, ARIA e axe

Trechos de redação própria para o sistema-demo de tarefas. Textos de título, nomes de controles e larguras são de exemplo. As opções valem para o Playwright 1.64 (V-54 a V-57); confirme na versão fixada.

## 1. Projetos de dispositivo, tema e locale (config)

```ts
// playwright.config.ts (trecho de projects)
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'celular', use: { ...devices['Pixel 5'] } },
    { name: 'desktop-escuro', use: { ...devices['Desktop Chrome'], colorScheme: 'dark' } },
    { name: 'desktop-en', use: { ...devices['Desktop Chrome'], locale: 'en-US', timezoneId: 'America/New_York' } },
  ],
});
```

Rodar um projeto: `npx playwright test --grep "F-07" --project=celular`. Emulação não é aparelho real, e o WebKit não é o Safari.

## 2. Regressão visual com `toHaveScreenshot`

```ts
import { test, expect } from './fixtures';

test('F-06 tela de tarefas mantém o layout @ui', async ({ page, app }) => {
  await app.abrir('/tarefas');
  await expect(page.getByRole('textbox', { name: 'Nova tarefa' })).toBeVisible();   // estado pronto, sem espera por tempo
  await page.mouse.move(-1, -1);                                                    // tira o hover da captura
  await expect(page).toHaveScreenshot('tarefas-vazia.png', {
    mask: [page.getByText(/pendente\(s\)/)],    // o contador é volátil: mascare ou trate no teste funcional
    maxDiffPixelRatio: 0.01,                    // tolerância por projeto, definida e revisada
  });
});
```

Primeira geração e atualização:

```bash
npx playwright test --grep "F-06" --update-snapshots=missing
```

O comando acima só cria o que falta. Para atualizar um baseline existente depois de revisar o diff das imagens, use `--update-snapshots` com o escopo mais estreito possível (um F-NN, um projeto). Nunca como reflexo para "deixar verde".

Política de baseline (modelo para a rodada):

| Item | Regra |
| --- | --- |
| Ambiente | o mesmo da geração (SO e container da CI); baseline por plataforma no nome do arquivo |
| Quem atualiza | uma pessoa, em commit próprio, com o diff das imagens revisado |
| Volátil | `mask` ou `stylePath`; tolerância por projeto |
| Falha | diff visto no relatório HTML antes de qualquer atualização |

## 3. ARIA snapshot parcial

```ts
test('F-06 estrutura da tela de tarefas @ui', async ({ page, app }) => {
  await app.abrir('/tarefas');
  await expect(page.getByRole('main')).toMatchAriaSnapshot(`
    - textbox "Nova tarefa"
    - button "Adicionar"
  `);
});
```

O template é uma restrição, não a serialização completa: o que não está nele pode existir. `- button` sem nome casa qualquer botão. Atualização: na CI use o modo `default` (gera o patch e falha) ou `missing`; `-u` só local, com revisão do patch.

## 4. axe com gate por violação nova

Pré-requisito: `@axe-core/playwright` instalado **com a confirmação do usuário** (dependência fora da pré-autorização).

```ts
import AxeBuilder from '@axe-core/playwright';
import { test, expect } from './fixtures';

const conhecidas = new Set<string>([/* ids de regras já registradas como dívida, com issue */]);

test('F-06 acessibilidade da tela de tarefas @ui', async ({ page, app }, testInfo) => {
  await app.abrir('/tarefas');
  await expect(page.getByRole('button', { name: 'Adicionar' })).toBeVisible();   // espere o estado antes de analisar

  const resultado = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();

  await testInfo.attach('axe-resultado', {
    body: JSON.stringify(resultado, null, 2),
    contentType: 'application/json',
  });

  const novas = resultado.violations.filter((v) => !conhecidas.has(v.id));
  expect(novas, `violações novas: ${novas.map((v) => v.id).join(', ')}`).toEqual([]);
});
```

Regras de uso:

- Escaneie também o estado revelado por interação (menu aberto, diálogo): abra, espere o elemento, depois `analyze()`.
- Exceção em ordem de granularidade: `disableRules(['<id>'])` antes de `exclude('<seletor>')`. `exclude()` tira o elemento e os descendentes de **todas** as regras.
- O resultado completo vai em anexo, não em snapshot do array inteiro.
- Elemento de terceiro (widget externo) pode ser excluído por seletor, com comentário e issue.

## 5. O que fica manual

Navegação por teclado complexa, ordem de foco, leitor de tela e clareza do conteúdo não são detectados de forma confiável pela automação (a própria documentação manda testar manualmente). Liste-os no relatório como Não verificado.
