# Acessibilidade

Como decidir o alvo de conformidade, automatizar a parte mecânica, executar o
roteiro manual (teclado, leitor de tela, zoom) e reportar achados em web e
mobile. Leia quando a tarefa envolver WCAG, leitor de tela, contraste,
auditoria de tela ou obrigação legal de acessibilidade.

## Sumário

- [Normas e qual alvo adotar](#normas-e-qual-alvo-adotar)
- [POUR e as falhas mais frequentes](#pour-e-as-falhas-mais-frequentes)
- [Critérios novos da WCAG 2.2](#critérios-novos-da-wcag-22)
- [Limiares de referência](#limiares-de-referência)
- [O que automatizar e o que não](#o-que-automatizar-e-o-que-não)
- [axe-core por ferramenta](#axe-core-por-ferramenta)
- [Medições além do axe](#medições-além-do-axe)
- [Roteiro manual](#roteiro-manual)
- [ARIA: padrões e erros comuns](#aria-padrões-e-erros-comuns)
- [Mobile](#mobile)
- [Público idoso](#público-idoso)
- [Como reportar um achado](#como-reportar-um-achado)
- [Armadilhas da automação](#armadilhas-da-automação)

## Normas e qual alvo adotar

**Estado das informações normativas:** a tabela é uma orientação de escopo.
Datas, versões e contagens herdadas ainda precisam de confirmação primária
por jurisdição antes de fundamentar uma auditoria. Não as trate como validadas
pelo CI ou por esta skill.

| Referência | Escopo | Base técnica | Obrigatória para |
| --- | --- | --- | --- |
| **WCAG 2.2** (W3C, 2023) | conteúdo web; aplicada por analogia a apps | níveis A, AA, AAA | não é lei; é a base técnica de quase todas as leis |
| **ABNT NBR 17060:2022** | aplicativos de dispositivos móveis (nativos, web e híbridos) | 54 requisitos derivados da WCAG | norma técnica; referência para cumprir a LBI |
| **LBI — Lei 13.146/2015, art. 63** | sites de empresas com sede ou representação comercial no país e de órgãos de governo | "diretrizes adotadas internacionalmente" (na prática, WCAG) | lei federal |
| **eMAG 3.1** (2014) | sites e portais do governo | WCAG adaptada | administração pública federal |
| **European Accessibility Act** (Diretiva UE 2019/882) | produtos e serviços ao consumidor: e-commerce, bancos, e-books, transporte, telecomunicações | EN 301 549 | em vigor desde 28/06/2025 para quem vende a consumidores na UE, inclusive empresa de fora; microempresas de serviços são isentas |
| **EN 301 549** | norma europeia de TIC | v3.2.1 → WCAG 2.1 AA; v4.1.1 (set/2026) → WCAG 2.2 AA | referência do EAA; a v4.1.1 só presume conformidade depois de citada no Jornal Oficial da UE — até lá vale a v3.2.1 |
| **Section 508** (EUA) | órgãos federais americanos e seus fornecedores | WCAG 2.0 AA | contratos com o governo federal dos EUA |
| **WCAG 3** | — | — | ninguém: ainda é rascunho (Working Draft) do W3C, **não é norma** |

**Referência técnica inicial para web: WCAG 2.2 nível AA**, salvo contrato
ou requisito aplicável diferente. Isso não declara atendimento automático à
LBI, NBR 17060, EN 301 549 ou Section 508. Identifique jurisdição, produto,
contrato, versão vigente e requisitos adicionais antes de avaliar conformidade.
Section 508, por exemplo, inclui disposições de software, desempenho funcional,
documentação e outros componentes além de critérios web.

Fonte primária para escopo: [U.S. Access Board — Revised 508 Standards](https://www.access-board.gov/ict/).
A tabela acima é orientação inicial, não parecer jurídico. Datas, contagens e
versões normativas devem ser confirmadas na fonte oficial antes de uso; sem
confirmação, registre **não verificado**. Critérios AAA podem ser necessários
por contrato ou necessidades do público; não presuma sua dispensa universal.

- A 2.2 **removeu o 4.1.1 (Parsing)**, e o W3C anotou na 2.0 e na 2.1 que ele
  conta como sempre atendido em HTML. Não reporte "HTML inválido"; reporte o
  efeito (`id` duplicado que quebra `aria-labelledby` falha em 1.3.1 ou 4.1.2).
- NBR 17060 é norma técnica, não lei, mas pesa em app comercial: o CDC (art.
  39, VIII) trata como prática abusiva vender produto ou serviço em desacordo
  com norma da ABNT quando não há norma oficial específica.
- Overlay ("acessibilidade com uma linha de código") não dá conformidade; nos
  EUA a FTC puniu em 2025 um fornecedor desses por propaganda enganosa.

## POUR e as falhas mais frequentes

Os quatro princípios viram perguntas de teste: **Perceptível** (todo conteúdo
chega por algum sentido? contraste, alternativa de imagem, legenda, cor),
**Operável** (dá para usar sem mouse, sem pressa, sem gesto preciso?),
**Compreensível** (a pessoa entende e se recupera de erro?) e **Robusto** (a
tecnologia assistiva lê nome, papel e estado de cada componente?).

A WebAIM Million 2026 (home pages do primeiro milhão de sites) achou falha
detectável em 95,9% das páginas, média de 56,1 erros por página, e **96% dos
erros em seis tipos** — todos detectáveis por máquina e baratos de corrigir.
Comece toda auditoria por eles:

| Falha | % das páginas | Critério |
| --- | --- | --- |
| Contraste de texto baixo | 83,9% | 1.4.3 |
| Imagem sem texto alternativo | 53,1% | 1.1.1 |
| Campo de formulário sem rótulo | 51,0% | 1.3.1, 3.3.2, 4.1.2 |
| Link vazio (ícone sem nome) | 46,3% | 2.4.4, 4.1.2 |
| Botão vazio | 30,6% | 4.1.2 |
| Idioma da página ausente (`<html lang>`) | 13,5% | 3.1.1 |

No mesmo estudo, páginas com ARIA tiveram **mais** erros (59,1) que sem (42).

## Critérios novos da WCAG 2.2

| Critério | Nível | Exige | Como testar |
| --- | --- | --- | --- |
| 2.4.11 Foco não obscurecido (mínimo) | AA | elemento focado não fica **totalmente** escondido por conteúdo do autor | Tab com cabeçalho fixo, banner de cookies e chat abertos |
| 2.4.12 Foco não obscurecido (aprimorado) | AAA | nenhuma parte do foco escondida | idem, exigindo foco inteiro visível |
| 2.4.13 Aparência do foco | AAA | indicador com área ≥ perímetro de 2 px CSS e contraste 3:1 entre focado e não focado | medir o contorno |
| 2.5.7 Movimentos de arrastar | AA | alternativa de ponteiro simples para toda ação de arrastar | reordenar lista, slider, kanban sem arrastar |
| 2.5.8 Tamanho do alvo (mínimo) | AA | 24×24 px CSS ou espaçamento equivalente; exceções: link em texto, controle nativo, equivalente na página, essencial | regra `target-size` do axe + medição |
| 3.2.6 Ajuda consistente | A | canal de ajuda repetido na mesma ordem relativa em todas as telas | comparar telas do fluxo |
| 3.3.7 Entrada redundante | A | não pedir de novo o que já foi informado no mesmo processo | endereço de entrega → cobrança |
| 3.3.8 Autenticação acessível (mínimo) | AA | entrar sem teste cognitivo (decorar, transcrever, resolver) | colar senha e código; gerenciador de senhas; CAPTCHA de texto sem alternativa reprova |
| 3.3.9 Autenticação acessível (aprimorado) | AAA | idem, sem exceção para reconhecer objeto ou conteúdo pessoal | — |

## Limiares de referência

| O quê | Critério | Nível | Valor |
| --- | --- | --- | --- |
| Contraste de texto | 1.4.3 | AA | 4,5:1; texto grande (≥ 24 px, ou ≥ 18,66 px negrito) 3:1 |
| Contraste de componente (borda de campo, ícone, foco) | 1.4.11 | AA | 3:1 |
| Redimensionar texto | 1.4.4 | AA | 200% sem perder conteúdo ou função |
| Reflow | 1.4.10 | AA | 320 px CSS de largura sem rolagem horizontal (= 1280 px a 400%) |
| Espaçamento de texto | 1.4.12 | AA | linha 1,5×; parágrafo 2×; letras 0,12×; palavras 0,16× a fonte |
| Alvo de toque | 2.5.8 / 2.5.5 | AA / AAA | 24×24 / 44×44 px CSS |
| Tempo limite | 2.2.1 | A | desligar, ajustar ou estender; aviso com ≥ 20 s para estender |
| Movimento automático | 2.2.2 | A | pausar, parar ou ocultar o que se move por mais de 5 s |
| Piscar | 2.3.1 | A | no máximo 3 flashes por segundo |

## O que automatizar e o que não

O axe-core, motor aberto por trás da maioria das ferramentas, acerta a parte
mecânica: contraste calculável, alt e rótulo ausentes, nome de botão e link,
`lang`, ARIA inválido, `id` referenciado duplicado, título, `target-size`. Em
estudo da Deque (mais de 2.000 auditorias), a varredura automática cobriu 57%
dos problemas **em volume**, porque os erros frequentes são mecânicos; em
número de critérios WCAG, a cobertura é bem menor. A máquina não decide se o
alt descreve a imagem, se a ordem de foco faz sentido, se o widget customizado
funciona no teclado, o que o leitor anuncia após uma ação, se o erro ajuda,
se a legenda está certa. **axe com violação = certamente inacessível; axe
zerado ≠ acessível.**

- Leia também `incomplete` (o que o axe não conseguiu decidir, como contraste
  sobre imagem de fundo): é a fila de revisão manual.
- Rode em **rotas e estados**: carregada, diálogo aberto, formulário em erro,
  menu de celular, dropdown expandido, toast visível, tema escuro, 375 px. A
  maioria das violações de rótulo só aparece com o formulário aberto ou em erro.
- Em legado, não desligue regras: congele as violações atuais (regra +
  seletor) como linha de base e falhe só com violação nova.

## axe-core por ferramenta

As tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa` e `wcag22aa` juntas
correspondem a WCAG 2.2 AA. Regras `best-practice` ajudam, mas não são
critério WCAG: separe-as no relatório.

### Playwright com TypeScript (`@axe-core/playwright`)

```ts
// tests/acessibilidade.spec.ts — requer use.baseURL no playwright.config.ts
import { test, expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];

async function varrer(page: Page, escopo?: string) {
  let builder = new AxeBuilder({ page }).withTags(TAGS);
  if (escopo) builder = builder.include(escopo); // ex.: '[role="dialog"]' com o diálogo aberto
  return (await builder.analyze()).violations;
}

function resumo(violacoes: Awaited<ReturnType<typeof varrer>>): string {
  return violacoes
    .map((v) => `[${v.impact}] ${v.id}: ${v.help}\n  ${v.nodes.map((n) => n.target.join(' ')).join('\n  ')}`)
    .join('\n');
}

for (const rota of ['/', '/login', '/cadastro', '/produtos']) {
  test(`sem violações WCAG 2.2 AA em ${rota}`, async ({ page }) => {
    await page.goto(rota);
    await expect(page.getByRole('main')).toBeVisible(); // conteúdo real, não o esqueleto
    const violacoes = await varrer(page);
    expect(violacoes, resumo(violacoes)).toEqual([]);
  });
}

test('cadastro em estado de erro continua acessível', async ({ page }) => {
  await page.goto('/cadastro');
  await page.getByRole('button', { name: 'Criar conta' }).click();
  await expect(page.getByText('Informe seu e-mail')).toBeVisible();
  const violacoes = await varrer(page);
  expect(violacoes, resumo(violacoes)).toEqual([]);
});
```

`exclude()` e `disableRules()` existem, mas cada uso esconde barreira real:
registre o motivo e o risco ao lado.

### Python (`scripts/auditoria_axe.py`)

O script varre rotas recém-carregadas no Chromium (1440×900, locale pt-BR)
com as mesmas cinco tags, imprime impacto, regra, até 5 seletores e o link da
regra, e sai com código 1 se houver violação. Requer `pip install playwright
&& playwright install chromium`. Na primeira execução baixa o axe-core 4.10.2
do cdnjs e o guarda como `axe.min.js` ao lado do script (depois roda sem
rede); injeta o axe por avaliação direta, o que passa por CSP restritiva.

```bash
python scripts/auditoria_axe.py https://homolog.exemplo.com / /login /cadastro
python scripts/auditoria_axe.py http://localhost:3000 /produtos --largura 375 --altura 812
python scripts/auditoria_axe.py http://localhost:3000 $(cat rotas.txt)   # uma rota por linha
```

Opções: `--largura`, `--altura` e `--esperar` (ms após a carga, padrão 800).
Reporta só `violations` (não `incomplete`) e não interage com a página. Para
estados, reaproveite as funções dele num teste:

```python
# tests/test_acessibilidade_estados.py — requer pytest-playwright
import os
import sys

from playwright.sync_api import Page, expect

sys.path.insert(0, os.environ["QA_SCRIPTS"])  # caminho de skills/qa/scripts
from auditoria_axe import analisar, obter_axe  # noqa: E402

BASE = os.environ.get("BASE_URL", "http://localhost:3000")
AXE = obter_axe()


def test_cadastro_em_erro_sem_violacoes(page: Page) -> None:
    page.goto(f"{BASE}/cadastro")
    page.get_by_role("button", name="Criar conta").click()
    expect(page.get_by_text("Informe seu e-mail")).to_be_visible()
    violacoes = analisar(page, AXE)
    assert not violacoes, [(v["id"], [n["target"] for n in v["nodes"]]) for v in violacoes]
```

### Cypress, jest-axe, Lighthouse e pa11y

```js
// cypress/support/e2e.js: import 'cypress-axe';   (axe-core é dependência par)
const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];

it('cadastro em erro sem violações', () => {
  cy.visit('/cadastro');
  cy.injectAxe(); // depois do visit; repita após recarga completa da página
  cy.contains('button', 'Criar conta').click();
  cy.contains('Informe seu e-mail').should('be.visible');
  cy.checkA11y(null, { runOnly: { type: 'tag', values: TAGS } });
});
```

- **cypress-axe:** sem callback, só diz quantas violações houve; para listar
  regra e seletor na CI, passe como terceiro argumento de `checkA11y` uma
  função que chame uma `cy.task` de log registrada em `setupNodeEvents`.
- **jest-axe:** componente isolado, barato para a matriz de estados (vazio,
  erro, carregando, desabilitado): `expect.extend(toHaveNoViolations)` e
  `expect(await axe(container)).toHaveNoViolations()` após o `render`. No
  JSDOM não há layout: contraste fica desligado; alvo e reflow não existem.
- **Lighthouse:** a nota é média ponderada de um subconjunto de regras do axe.
  Nota 100 não é conformidade; use como tendência. No Lighthouse CI:
  `"categories:accessibility": ["error", {"minScore": 0.95}]`.
- **pa11y / pa11y-ci:** lista de URLs no pipeline, com `actions` ("click
  element #abrir", "wait for element .modal to be visible") para chegar a
  estados. Use `--runner axe` para ter as regras do resto da suíte (o runner
  padrão, HTML_CodeSniffer, dá resultados diferentes) e confira na sua versão
  quais regras WCAG 2.2 o `--standard` ativa.

## Medições além do axe

- Tamanho real do texto em pixels (computado, não a classe CSS).
- Alvo de toque medido para 44 px, contando o `<label>` associado como área.
- Mudança visível de estilo ao receber foco (código abaixo).
- Reflow: viewport de 320 px e `scrollWidth - clientWidth <= 0` no `<html>`.
- Espaçamento do 1.4.12 injetado com `page.addStyleTag` (as quatro medidas da
  tabela, com `!important`), procurando elemento com `overflow: hidden` cujo
  `scrollHeight` passou do `clientHeight`.
- Título de aba único por tela e um `h1` por tela.

```ts
test('botão Entrar muda de estilo ao receber foco pelo teclado', async ({ page }) => {
  await page.goto('/login');
  const botao = page.getByRole('button', { name: 'Entrar' });
  const estilo = () => botao.evaluate((el) => { const s = getComputedStyle(el);
    return [s.outlineStyle, s.outlineWidth, s.boxShadow, s.backgroundColor, s.borderColor].join('|'); });
  const antes = await estilo();
  await page.getByLabel('Senha').focus();
  await page.keyboard.press('Tab'); // Tab real: focus() programático pode não ativar :focus-visible
  await expect(botao).toBeFocused();
  expect(await estilo()).not.toBe(antes);
});
```

## Roteiro manual

Faça por **tarefa completa** (cadastrar, comprar, recuperar senha), não por
tela isolada: os defeitos graves aparecem na transição entre telas. Só pessoa
avalia também linguagem (termo que o usuário não conhece, instrução ambígua)
e, quando der, observe 3 a 5 pessoas do público real em silêncio.

### Teclado

Tab e Shift+Tab, Enter (link, botão), Espaço (botão, caixa de seleção), setas
(rádio, abas, menu, slider), Esc (fecha diálogo e menu). No macOS, ative a
navegação por teclado do sistema e, no Safari, "Pressionar Tab para destacar
cada item" — senão o Tab pula links e você reporta falso defeito.

1. O primeiro Tab mostra "Pular para o conteúdo", que leva ao `main` (2.4.1).
2. Ordem de foco segue a ordem visual (2.4.3); `tabindex` positivo é defeito.
3. Foco sempre visível (2.4.7), não coberto por cabeçalho fixo, banner de
   cookies ou chat (2.4.11).
4. Tudo que funciona com mouse funciona com teclado (2.1.1): menu no hover,
   tooltip, carrossel, arrastar, seletor de data.
5. Sem armadilha (2.1.2): sai de player, editor rico, mapa, iframe de pagamento.
6. Diálogo: foco entra, Tab circula dentro, Esc fecha, foco volta ao gatilho.
7. Conteúdo de hover ou foco sai com Esc e não some ao passar o ponteiro
   sobre ele (1.4.13).

### Leitor de tela

Combinações de referência: NVDA + Firefox ou Chrome e JAWS + Chrome
(Windows), VoiceOver + Safari (macOS, iOS), TalkBack + Chrome (Android).
Priorize a do seu público. Gestos de celular estão em [Mobile](#mobile).

| Ação | NVDA (tecla NVDA = Insert) | JAWS | VoiceOver macOS (VO = Ctrl+Option) |
| --- | --- | --- | --- |
| Ligar | Ctrl+Alt+N | — | Cmd+F5 |
| Próximo item / ativar | ↓ / Enter | ↓ / Enter | VO+→ / VO+Espaço |
| Próximo título / por nível | H / 1–6 | H / 1–6 | VO+Cmd+H |
| Próximo campo de formulário | F | F | VO+Cmd+J |
| Listas de elementos | NVDA+F7 | Insert+F6 (títulos), Insert+F7 (links), Insert+F5 (campos) | VO+U (rotor) |
| Modo navegação ↔ formulário | NVDA+Espaço | Enter no campo entra no modo formulário | — |
| Ler a partir daqui / calar | NVDA+↓ / Ctrl | Insert+↓ / Ctrl | VO+A / Ctrl |

Anote em três colunas — passo, o que foi anunciado, o que deveria ser — e
verifique: nome, papel e estado de cada controle ("Aceito os termos, caixa de
seleção, não marcada"); conteúdo encontrável por títulos e marcos (`main`,
`nav`); erro de formulário anunciado com o modo de corrigir; mudança dinâmica
anunciada (item adicionado, total, toast); foco em lugar sensato após cada
ação — fechar diálogo, enviar formulário, trocar de rota em SPA (foco no `h1`
ou novo título anunciado; a falha clássica é o foco ficar na página que sumiu).

### Zoom, reflow, movimento, cor e mídia

- Zoom de 200%: nada cortado ou sobreposto. Janela de 1280 px a 400%: só
  rolagem vertical (tabela, mapa e diagrama são exceção) e menu acessível.
- Fonte grande do sistema somada ao zoom; retrato e paisagem (1.3.4).
- Movimento reduzido ligado no sistema (ou `page.emulateMedia({ reducedMotion:
  'reduce' })`): parallax e animação de transição param.
- Nada só por cor (1.4.1): simule daltonismo no Chrome DevTools (Rendering →
  Emulate vision deficiencies); teste o tema escuro, que tem contraste próprio.
- Vídeo: legenda sincronizada e revisada (1.2.2, A) — automática sem revisão
  erra nome próprio e número; audiodescrição ou alternativa (1.2.3, A; 1.2.5,
  AA); ao vivo, legenda (1.2.4, AA). Podcast: transcrição (1.2.1). Som
  automático por mais de 3 s precisa de controle (1.4.2).

## ARIA: padrões e erros comuns

**Nenhum ARIA é melhor que ARIA ruim** (aviso do guia de práticas ARIA do
W3C). ARIA muda o que é anunciado, não o comportamento: `<div role="button">`
não recebe foco nem responde a Enter e Espaço sozinho. Use o elemento nativo
(`button`, `a`, `input`, `select`, `dialog`); ARIA só onde o HTML não tem o
padrão. Erros de toda auditoria:

- `aria-label` em `div` ou `span` sem papel: vários leitores ignoram.
- `aria-hidden="true"` em elemento focável ou em ancestral dele: o foco cai
  em algo que o leitor diz não existir.
- Nome acessível diferente do texto visível (2.5.3): quem usa controle por
  voz diz "clicar Enviar" e nada acontece porque o nome é "submit-form".
- `role="presentation"` em tabela de dados; `aria-live` em região que muda a
  cada segundo.

**Diálogo modal.** Prefira `<dialog>` com `showModal()`: deixa o fundo inerte
e fecha com Esc. Verifique: nome do diálogo (`aria-labelledby` no título);
foco entra no primeiro elemento útil; nem o Tab nem o cursor virtual do leitor
escapam para o fundo; ao fechar, o foco volta ao gatilho (navegadores atuais
fazem isso com `<dialog>`; em modal feito à mão, é do código).

**Live regions para toast e erro.** A região precisa existir no DOM, vazia,
**antes** da mensagem; inseri-la junto com o texto faz muitos leitores calarem.
Toast com ação ("Desfazer") que some em 3 s falha em tempo (2.2.1).

```html
<div id="aviso" role="status"></div>      <!-- educado: "Produto adicionado ao carrinho" -->
<div id="erro-global" role="alert"></div> <!-- interrompe: só para erro que bloqueia -->
```

**Formulário.**

```html
<label for="email">E-mail</label>
<input id="email" name="email" type="email" autocomplete="email" required
       aria-invalid="true" aria-describedby="email-dica email-erro">
<p id="email-dica">Usaremos para enviar a nota fiscal.</p>
<p id="email-erro">Informe um e-mail no formato nome@exemplo.com.</p>
```

- Rótulo visível e ligado; placeholder não é rótulo (some ao digitar).
- Obrigatório com `required` e indicação visível que não seja só cor nem
  asterisco sem legenda; `aria-invalid` só depois de validar.
- Erro que diz como corrigir (3.3.3), ligado por `aria-describedby`. Ao enviar
  com erro, foco no primeiro campo inválido ou num resumo com links.
- Rádios relacionados em `fieldset` com `legend`; `autocomplete` correto em
  dados pessoais (1.3.5).

**Combobox e abas.** `role="combobox"` não recebe nome do próprio conteúdo:
sem `aria-label` ou `aria-labelledby`, o leitor anuncia "caixa de combinação"
e nada mais. Abas usadas como filtro deixam `aria-controls` apontando para
painel inexistente; sem painel, é grupo de botões com `aria-pressed`.

## Mobile

- **Alvo:** 44×44 pt (iOS) e 48×48 dp (Android) são as referências das
  plataformas; os 24 px CSS da WCAG são piso, não meta.
- **Nome acessível:** Android `contentDescription` (Compose:
  `Modifier.semantics { contentDescription = "…" }`); iOS `accessibilityLabel`
  (SwiftUI `.accessibilityLabel("…")`); React Native `accessibilityLabel` com
  `accessibilityRole`; Flutter `Semantics(label: …)`. Imagem decorativa sai da
  árvore (Android `importantForAccessibility="no"`, iOS
  `isAccessibilityElement = false`). Não ponha o papel no rótulo ("botão
  Salvar" vira "botão Salvar, botão").
- **ID de teste vazando para o leitor:** no Android, o localizador
  "accessibility id" do Appium usa o `content-desc`, que o TalkBack anuncia —
  `btn_submit_01` ali é lido em voz alta. Use `resource-id` ou `testTag` para
  automação. No iOS, `accessibilityIdentifier` é para automação e não é lido.
- **Fonte:** Dynamic Type (iOS) e escala de fonte (Android, até 200% desde o
  Android 14). Use `sp` e estilos de texto do sistema; na escala máxima, o
  texto não trunca e a tela rola.
- **Gestos comuns a TalkBack e VoiceOver iOS:** deslizar para a direita ou
  esquerda (próximo/anterior), toque duplo (ativar), arrastar o dedo
  (explorar). VoiceOver: rotor (girar dois dedos) e deslizar para cima/baixo
  para ir por títulos ou links; "Z" com dois dedos volta; toque com dois dedos
  pausa a fala. TalkBack: dois dedos rolam; os gestos de navegar por título
  mudam com a versão (veja o tutorial do aparelho).
- Gesto de vários dedos e sacudir o aparelho precisam de alternativa simples
  (2.5.1, 2.5.4).
- **Automação:** Espresso `AccessibilityChecks.enable()`
  (`androidx.test.espresso.accessibility`), app Accessibility Scanner,
  XCUITest `XCUIApplication().performAccessibilityAudit()` (Xcode 15+) e
  Accessibility Inspector. Mais em `references/mobile.md`.

## Público idoso

A pesquisa do W3C (WAI-AGE) mostra sobreposição grande entre necessidades de
pessoas idosas e de pessoas com deficiência, em quatro eixos: visão
(contraste, foco de perto), destreza (precisão do gesto), audição e cognição
(memória de trabalho, concentração). Para público de 40 a 90 anos, puxe
parâmetros acima da norma:

| Parâmetro | Norma (AA) | Recomendado |
| --- | --- | --- |
| Alvo de toque | 24 px | **44 px** (2.5.5, AAA) |
| Corpo de texto | sem mínimo | **16–18 px**, piso absoluto de 14 px |
| Contraste de texto | 4,5:1 | 4,5:1 sem exceção; 7:1 onde couber |
| Ampliação | 200% pelo navegador | 200% **mais** controle de fonte na interface |
| Ação destrutiva | — | confirmação que diz em palavras o que vai acontecer |
| Ícone sozinho | nome acessível | nome acessível **e** legenda visível |

Barato e eficaz: `autocomplete` correto nos campos de acesso (quem não decora
senha depende do gerenciador), erro em linguagem simples ligado ao campo,
nada só por cor, `prefers-reduced-motion` respeitado, aviso antes de a sessão
expirar.

## Como reportar um achado

Além do formato de bug do `SKILL.md`, inclua: critério WCAG (número, nome,
nível), quem é afetado, tecnologia assistiva e navegador usados, o que foi
**anunciado** versus o esperado, e sugestão de correção. Severidade pelo
efeito na tarefa (impede sem contorno → alta), não só pelo `impact` do axe.

> **Carrinho: botão de remover item é anunciado só como "botão"**
>
> - **Critério:** 4.1.2 Nome, função, valor (A).
> - **Afeta:** quem usa leitor de tela e quem usa controle por voz.
> - **Ambiente:** homologação, build 2.14.0; Windows 11, Firefox + NVDA;
>   reproduz em iOS, Safari + VoiceOver.
> - **Passos:** 1. Adicionar "Camiseta azul M" e "Boné preto" ao carrinho.
>   2. Abrir `/carrinho`. 3. Com NVDA ligado, Tab até o primeiro item.
> - **Esperado:** "Remover Camiseta azul M do carrinho, botão".
> - **Obtido:** "botão" — não dá para saber o que faz nem de qual item.
> - **Evidência:** axe `button-name` (critical) em
>   `.cart-item:nth-child(1) .icon-btn`; gravação com áudio do leitor.
> - **Severidade:** alta (impede revisar o carrinho com autonomia, sem
>   contorno). **Prioridade:** alta (fluxo de compra).
> - **Correção:** `<button type="button" aria-label="Remover Camiseta azul M
>   do carrinho">` com o ícone em `<svg aria-hidden="true">`; após remover,
>   foco no próximo item e aviso em `role="status"` ("Camiseta azul M
>   removida. Total: R$ 89,90").

## Armadilhas da automação

- **Varredura no esqueleto de carregamento** dá zero violações e falso verde;
  espere o conteúdo real.
- **Só desktop e tema claro:** menu de celular e tema escuro têm violações
  próprias; rode também a 375 px e no escuro.
- **Excluir widget de terceiro "porque não é nosso":** a barreira continua
  para o usuário; registre como risco e cobre do fornecedor.
- **Campo espelho invisível:** bibliotecas como Radix mantêm um `input` de
  1 px para envio do formulário; não é alvo de toque, não entra na conta.
- **Medição durante animação:** espere a transição terminar.
- **`sr-only` com foco:** "pular para o conteúdo" mede 1×1 até receber foco;
  trate como exceção explícita.
- **Foco por `focus()` programático** pode não ativar `:focus-visible`; use Tab.
- **Gate só com `critical`:** contraste costuma vir como `serious`, e a falha
  mais comum da web passa.
- **Nota do Lighthouse como meta:** nota 100 com teclado quebrado é comum.
