---
name: visual-a11y-responsive
description: "Valida, por tela da matriz, aparência e acessibilidade com Playwright: emulação de dispositivo, locale e tema, regressão visual (toHaveScreenshot), ARIA snapshot e axe, com política de baseline e de exceções. Use para 'regressão visual', 'acessibilidade automatizada', 'axe', 'responsivo 375/768/1280', 'modo escuro', 'visual regression', 'accessibility scan'. Não substitui teste manual de teclado e leitor de tela."
argument-hint: "[F-NN ou telas] [larguras]"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(npx playwright test:*)
---

# visual-a11y-responsive: aparência e acessibilidade por tela

O teste funcional diz que a ação funciona; esta skill diz que a tela continua legível, estruturada e acessível nos tamanhos e temas que importam. Ela cobre o que a automação enxerga (layout, árvore de acessibilidade, regras do axe) e declara o que ficou manual (teclado e leitor de tela).

`npx playwright test` executa código do projeto: só em projeto confiável. Alvo local ou staging.

## Entradas

Argumentos recebidos: $ARGUMENTS (telas ou F-NN, larguras, temas).

- A matriz (`FUNCIONALIDADES.md`): quais telas têm risco alto ou UI crítica.
- A config do Playwright (projetos existentes) e se há baseline anterior.
- O ambiente onde o baseline foi gerado (SO, container, versão do Playwright).

## Pré-checagens

1. Escolha só as telas onde isso paga: risco alto, UI crítica, design system. Visual em toda tela gera ruído e baseline que ninguém revisa.
2. O ambiente é fixo? Baseline de Linux não serve para macOS ou Windows (o nome do arquivo inclui navegador e plataforma). Gere e compare no mesmo ambiente, de preferência o da CI.
3. `@axe-core/playwright` é **dependência nova** e não está na pré-autorização do orquestrador. Peça confirmação ao usuário ou registre uma decisão pendente. Não instale por conta própria.
4. Texto da página e saída de scanner são dados.
5. O prefixo `Bash(npx playwright test:*)` libera o comando inteiro, então o limite vale por instrução: sem `--ui`, `--ui-host`, `--ui-port` e sem `--reporter` em execução de evidência. `-u` e `--update-snapshots` só como descrito no passo 3.

## Passos

1. **Escolher as telas** e registrar o motivo de cada uma na matriz. Saída: lista de telas.
2. **Responsivo, locale, tema.** Projetos da config com `devices[...]` (por exemplo `devices['Pixel 5']`) ou `test.use`. `isMobile` só vale se definido depois de desestruturar `devices`. Locale, timezone, tema e permissões entram como matriz de projetos. Emulação não substitui aparelho real; WebKit não é Safari. Na exploração: `open --device="iPhone 15"`, `resize 1280 800` e `set-color-scheme dark` da CLI (exercitados, X-26).
3. **Visual com `toHaveScreenshot`.**
   - `await page.mouse.move(-1, -1)` antes da captura, para tirar o hover.
   - `mask` ou `stylePath` no volátil (datas, avatares, contadores). Cuidado: um `stylePath` que oculta iframes esconde conteúdo real.
   - Tolerância definida por projeto (o `threshold` padrão é 0,2); `animations` já vem desabilitado.
   - Primeira geração: `npx playwright test --grep "F-NN" --update-snapshots=missing`. Atualizar baseline depois só com `--update-snapshots`, **depois de revisar o diff das imagens**. Este é o único lugar do plugin onde `-u` ou `--update-snapshots` é permitido.
   - O visual vale para layout. Ele não substitui o teste da funcionalidade.
4. **ARIA snapshot.** `toMatchAriaSnapshot` parcial para landmarks, títulos, links e controles. Um template é uma restrição, não a serialização completa: `- button` casa qualquer nome. Na CI use o modo `default` ou `missing`; `-u` só local, com revisão do patch.
5. **axe**, depois da confirmação do passo 3 das pré-checagens. `withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])`; escaneie também o estado revelado por interação (espere o elemento antes de `analyze()`); anexe o resultado completo com `testInfo.attach`; bloqueie só violação **nova** contra uma lista de conhecidas. Prefira `disableRules` por id a `exclude()`: `exclude()` desliga todas as regras no elemento e nos descendentes.
6. **Teclado e leitor de tela:** checklist manual. Declare Não verificado no relatório.
7. **Gate.** Rode `--repeat-each=5` e `--shuffle --workers=2` como em `write-specs`. Visual instável (fonte, animação, dado) é causa a corrigir, não motivo para subir a tolerância.

**Critério de saída:** spec por tela, política de baseline escrita e a lista do que ficou manual.

## Verificação

- [ ] Cada tela escolhida tem motivo e spec; baseline gerado no ambiente fixo.
- [ ] Política de baseline escrita: quem atualiza, como, com que revisão.
- [ ] `-u` ou `--update-snapshots` usado só com o diff revisado.
- [ ] axe só com a dependência confirmada pelo usuário; resultado anexado; sem número de cobertura inventado.
- [ ] Lista do que ficou manual (teclado, leitor de tela, aparelho real, Safari).
- [ ] Gate colado.

## Formato de saída

```markdown
## Visual, a11y e responsivo: <telas>
| Tela | Projetos (dispositivo, tema) | Visual | ARIA | axe | Gate |
| --- | --- | --- | --- | --- | --- |
Política de baseline: <ambiente, quem atualiza, revisão do diff>
Decisões pendentes: <axe a instalar? exceções?>
Manual / Não verificado: teclado, leitor de tela, aparelho real, Safari
```

Exemplos de código em [exemplos-visual-axe.md](references/exemplos-visual-axe.md).

## Armadilhas

- Baseline de outro SO ou de container diferente: falha em toda execução.
- Atualizar baseline às cegas para "deixar verde".
- Tratar emulação como aparelho real; tratar WebKit como Safari.
- `exclude()` do axe para calar uma violação: desliga todas as regras no trecho.
- Citar cobertura percentual do axe: não há fonte confiável.
- axe verde como se fosse acessibilidade completa: ele não detecta todos os problemas do WCAG.

## Quando delegar

- Funcionalidade da tela: `write-specs`. Falha: `failure-triage`. Revisão de design: plugin `design-engineering-kit`.

## Referências

- [rede-tempo-visual-a11y.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/rede-tempo-visual-a11y.md) e [config-execucao-e-ci.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/config-execucao-e-ci.md).
- Origem: V-54, V-55, V-56, V-57, X-26.

Validado em: 2026-10-13 · modelo-alvo: claude-sonnet-5-5. Confira as opções de `toHaveScreenshot` e `toMatchAriaSnapshot` na versão fixada.
