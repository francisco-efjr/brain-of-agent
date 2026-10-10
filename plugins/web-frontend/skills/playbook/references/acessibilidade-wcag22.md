# Acessibilidade web: WCAG 2.2, HTML nativo antes de ARIA e roteiro de teste

Como definir o alvo, implementar com HTML nativo, automatizar a parte mecânica, testar por teclado e leitor de tela e reportar achados. Leia ao construir ou revisar componentes interativos, formulários, diálogos ou ao auditar uma tela. Conferido em 2026-10-10 (V-16, V-24, V-45, V-56, V-58) e adaptado do material próprio `brains/qa/references/acessibilidade.md` do brain-of-agent (MIT). O que o brain trazia sem confirmação primária está rotulado Inferido ou Não verificado.

## Sumário

- [Alvo e normas](#alvo-e-normas)
- [POUR e ordem de triagem](#pour-e-ordem-de-triagem)
- [Critérios novos da WCAG 2.2](#critérios-novos-da-wcag-22)
- [Limiares de referência](#limiares-de-referência)
- [HTML nativo antes de ARIA](#html-nativo-antes-de-aria)
- [Formulários acessíveis](#formulários-acessíveis)
- [Diálogo modal, live regions e erros comuns de ARIA](#diálogo-modal-live-regions-e-erros-comuns-de-aria)
- [Automação com axe](#automação-com-axe)
- [Roteiro manual](#roteiro-manual)
- [Formato de achado](#formato-de-achado)
- [Armadilhas da automação](#armadilhas-da-automação)
- [Público idoso](#público-idoso)

## Alvo e normas

Alvo técnico inicial para web: **WCAG 2.2 nível AA**, salvo contrato ou requisito aplicável diferente (V-16, Verificado: Recomendação do W3C de 5 out 2023; o snapshot atual em w3.org/TR/WCAG22 é de 12 dez 2024). Isso não declara conformidade legal. Identifique jurisdição, produto, contrato e versão vigente antes de falar em conformidade.

| Referência | Escopo | Rótulo |
| --- | --- | --- |
| WCAG 2.2 (W3C) | conteúdo web; base técnica de quase todas as leis | Verificado |
| ABNT NBR 17060 | aplicativos móveis (nativos, web e híbridos), derivada da WCAG | Inferido (contagem de requisitos e datas Não verificadas) |
| LBI (Lei 13.146/2015, art. 63) | sites de empresas com sede ou representação no país e de órgãos públicos | Inferido |
| eMAG | portais do governo federal | Inferido |
| European Accessibility Act e EN 301 549 | produtos e serviços ao consumidor na UE | Inferido; versão da EN e vigência: Não verificado |
| Section 508 (EUA) | órgãos federais e fornecedores; inclui disposições além de critérios web | Inferido; fonte primária a consultar: https://www.access-board.gov/ict/ |
| WCAG 3 | rascunho do W3C, não é norma | Inferido |

Esta tabela é orientação de escopo, não parecer jurídico. Datas e versões normativas precisam de confirmação na fonte oficial; sem ela, registre Não verificado. Critérios AAA podem ser exigidos por contrato ou pelo público; não presuma dispensa. Overlay ("acessibilidade com uma linha de código") não dá conformidade (Inferido).

A WCAG 2.2 removeu o critério 4.1.1 Parsing (V-16). Não reporte "HTML inválido"; reporte o efeito: `id` duplicado que quebra `aria-labelledby` falha em 1.3.1 ou 4.1.2.

## POUR e ordem de triagem

Os quatro princípios viram perguntas de teste: **Perceptível** (todo conteúdo chega por algum sentido? contraste, alternativa de imagem, legenda), **Operável** (dá para usar sem mouse, sem pressa, sem gesto preciso?), **Compreensível** (a pessoa entende e se recupera de erro?), **Robusto** (a tecnologia assistiva lê nome, papel e estado de cada componente?).

Ordem de triagem para começar uma auditoria, pelas falhas mais frequentes e detectáveis por máquina (lista do brain, derivada da WebAIM Million 2026; os percentuais do brain ficaram fora por não rechecados, Inferido):

1. Contraste de texto baixo (1.4.3).
2. Imagem sem texto alternativo (1.1.1).
3. Campo de formulário sem rótulo (1.3.1, 3.3.2, 4.1.2).
4. Link vazio, como ícone sem nome (2.4.4, 4.1.2).
5. Botão vazio (4.1.2).
6. Idioma da página ausente, `<html lang>` (3.1.1).

## Critérios novos da WCAG 2.2

(V-16, Verificado: nove critérios novos; A: 3.2.6 e 3.3.7; AA: 2.4.11, 2.5.7, 2.5.8, 3.3.8; AAA: 2.4.12, 2.4.13, 3.3.9.)

| Critério | Nível | Exige | Como testar |
| --- | --- | --- | --- |
| 2.4.11 Foco não obscurecido (mínimo) | AA | elemento focado não fica totalmente escondido por conteúdo do autor | Tab com cabeçalho fixo, banner de cookies e chat abertos |
| 2.4.12 Foco não obscurecido (aprimorado) | AAA | nenhuma parte do foco escondida | idem, exigindo o foco inteiro visível |
| 2.4.13 Aparência do foco | AAA | indicador com área mínima e contraste 3:1 entre focado e não focado | medir o contorno |
| 2.5.7 Movimentos de arrastar | AA | alternativa de ponteiro simples para toda ação de arrastar | reordenar lista, slider, kanban sem arrastar |
| 2.5.8 Tamanho do alvo (mínimo) | AA | alvo de pelo menos 24 por 24 px CSS ou espaçamento equivalente; exceções: espaçamento, equivalente, inline, controle do agente de usuário, essencial | regra `target-size` do axe e medição |
| 3.2.6 Ajuda consistente | A | canal de ajuda na mesma ordem relativa em todas as telas | comparar telas do fluxo |
| 3.3.7 Entrada redundante | A | não pedir de novo o que já foi informado no mesmo processo | endereço de entrega para cobrança |
| 3.3.8 Autenticação acessível (mínimo) | AA | entrar sem teste cognitivo (decorar, transcrever, resolver) | colar senha e código; gerenciador de senhas; CAPTCHA de texto sem alternativa reprova |
| 3.3.9 Autenticação acessível (aprimorado) | AAA | idem, sem exceção para reconhecer objeto ou conteúdo pessoal | n/a |

## Limiares de referência

| O quê | Critério | Nível | Valor |
| --- | --- | --- | --- |
| Contraste de texto | 1.4.3 | AA | 4,5:1; texto grande 3:1 |
| Contraste de componente (borda de campo, ícone, foco) | 1.4.11 | AA | 3:1 |
| Redimensionar texto | 1.4.4 | AA | 200% sem perder conteúdo ou função |
| Reflow | 1.4.10 | AA | 320 px CSS de largura sem rolagem horizontal |
| Espaçamento de texto | 1.4.12 | AA | linha 1,5x, parágrafo 2x, letras 0,12x, palavras 0,16x o tamanho da fonte |
| Alvo | 2.5.8 / 2.5.5 | AA / AAA | 24x24 / 44x44 px CSS |
| Tempo limite | 2.2.1 | A | desligar, ajustar ou estender |
| Movimento automático | 2.2.2 | A | pausar, parar ou ocultar o que se move por mais de 5 s |
| Piscar | 2.3.1 | A | no máximo 3 flashes por segundo |

Os valores desta tabela vêm do brain (Inferido, valores conhecidos da WCAG); conferir no texto normativo em w3.org/TR/WCAG22 antes de citar em laudo.

## HTML nativo antes de ARIA

Fonte: ARIA in HTML, Recomendação W3C de 11 ago 2026 (V-58, Verificado), e as quatro regras de uso de ARIA ainda legíveis em "Using ARIA", hoje Discontinued Draft (V-58): 1) prefira HTML nativo; 2) não mude a semântica nativa sem necessidade; 3) todo controle ARIA interativo funciona com teclado; 4) nunca `role="presentation"` nem `aria-hidden="true"` em elemento focável.

Checklist de componente novo (V-58, V-24):

1. Existe elemento nativo (`button`, `a`, `input`, `select`, `dialog`, `details`)? Use-o.
2. Se não existe, qual padrão do APG (https://www.w3.org/WAI/ARIA/apg/patterns/) e quais teclas ele define? Implemente teclado e foco conforme o padrão.
3. Sem papel redundante (`role="button"` em `<button>`); `aria-checked` não vai em elemento que suporta `checked`.
4. Teclado completo: Enter, Espaço, Esc e setas conforme o padrão.
5. Nada de `aria-hidden` ou `role="presentation"` em focável.
6. Link desabilitado: `disabled` não é válido em `<a>`; use `aria-disabled` sabendo que o link continua operável (V-58).
7. Teste só com teclado.

ARIA muda o que é anunciado, não o comportamento: `<div role="button">` não recebe foco nem responde a Enter e Espaço sozinho (brain, conhecimento estável). O estudo do brain de que páginas com ARIA tiveram mais erros é Inferido; use apenas como motivo para preferir HTML nativo.

## Formulários acessíveis

(V-45; Verificado nas fontes: itens 1 a 5 e 8.)

1. Todo campo tem `<label for>` visível; instrução ligada por `aria-describedby`; placeholder não substitui rótulo (3.3.2).
2. Validação nativa primeiro (`required`, `type`, `pattern`, `min`, `max`); estilo de erro com `:user-invalid`, que só marca após interação (`:invalid` marca antes do primeiro toque).
3. Mensagem de erro em texto, dizendo o que está errado e como corrigir: "Informe um e-mail no formato nome@dominio.com" cumpre 3.3.1 e 3.3.3; "E-mail inválido" cumpre só 3.3.1.
4. Erro associado ao campo (`aria-describedby`) e anunciado; com vários erros, resumo único (quantidade e lista) em vez de vários `aria-live`, porque `aria-live="assertive"` tende a anunciar só o primeiro.
5. Cor nunca é o único sinal; ícone ou prefixo de texto ("Erro:").
6. Envio sensível (pagamento, exclusão, dados regulados): ofereça reversão, verificação com chance de corrigir ou tela de confirmação (3.3.4, nível AA).
7. Estado de envio visível (botão com pendência) e foco gerenciado após o envio (Inferido).
8. Validação no servidor sempre; a do cliente é só experiência.
9. Teste: só teclado, leitor de tela, zoom de 200%, e axe como complemento.

Não verificável pelas fontes lidas, confirme em APG ou W3C antes de virar regra: `aria-invalid`, mover o foco ao primeiro campo com erro, `autocomplete` correto (1.3.5), `fieldset` com `legend` para grupos de rádio. O brain recomenda essas práticas (conhecimento comum), mas elas são Inferidas aqui.

Exemplo do brain (adaptado) com rótulo, instrução e erro ligados:

```html
<label for="email">E-mail</label>
<input id="email" name="email" type="email" autocomplete="email" required
       aria-invalid="true" aria-describedby="email-dica email-erro">
<p id="email-dica">Usaremos para enviar a nota fiscal.</p>
<p id="email-erro">Informe um e-mail no formato nome@exemplo.com.</p>
```

## Diálogo modal, live regions e erros comuns de ARIA

**Diálogo modal (brain, conhecimento estável).** Prefira `<dialog>` com `showModal()`: deixa o fundo inerte e fecha com Esc. Verifique: nome do diálogo (`aria-labelledby` no título); foco entra no primeiro elemento útil; Tab não escapa para o fundo; ao fechar, o foco volta ao gatilho (navegadores atuais fazem isso com `<dialog>`; em modal feito à mão é do código).

**Live regions.** A região precisa existir no DOM, vazia, antes da mensagem; inseri-la junto com o texto faz muitos leitores calarem. `role="status"` é educado ("Produto adicionado"); `role="alert"` interrompe e fica para erro que bloqueia. Toast com ação que some em 3 s falha em tempo (2.2.1).

**Erros comuns em auditoria:**

- `aria-label` em `div` ou `span` sem papel: vários leitores ignoram.
- `aria-hidden="true"` em elemento focável ou em ancestral dele.
- Nome acessível diferente do texto visível (2.5.3): quem usa voz diz "clicar Enviar" e nada acontece porque o nome é `submit-form`.
- `role="presentation"` em tabela de dados; `aria-live` em região que muda a cada segundo.
- `role="combobox"` sem `aria-label` ou `aria-labelledby`: o leitor anuncia "caixa de combinação" e nada mais.
- Abas usadas como filtro, com `aria-controls` para painel inexistente: sem painel é grupo de botões com `aria-pressed`.

## Automação com axe

axe-core (Deque; MPL-2.0: use o pacote, não copie código) acerta a parte mecânica: contraste calculável, alt e rótulo ausentes, nome de botão e link, `lang`, ARIA inválido, `id` referenciado duplicado, título, `target-size`. Ele não decide se o alt descreve a imagem, se a ordem de foco faz sentido, se o widget funciona no teclado, o que o leitor anuncia, se o erro ajuda. **Axe com violação é certamente inacessível; axe zerado não é acessível.** O número de cobertura "57%" atribuído à Deque no brain não foi confirmado: não o cite.

- Leia também `incomplete` (o que o axe não decidiu, como contraste sobre imagem): é a fila de revisão manual.
- Rode em rotas e estados: carregada, diálogo aberto, formulário em erro, menu móvel, dropdown expandido, toast, tema escuro, 375 px. A maioria das violações de rótulo só aparece com o formulário aberto ou em erro.
- Em legado, não desligue regras: congele as violações atuais (regra e seletor) como linha de base e falhe só com violação nova.
- Tags: `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa` e `wcag22aa` juntas correspondem a WCAG 2.2 AA; o `doc/API.md` do axe-core 4.14.0 lista `wcag22aa` e a página do Playwright não (V-56). Confirme que a versão instalada do axe lista a tag. Regras `best-practice` ajudam, mas não são critério WCAG: separe no relatório.
- `exclude()` remove o elemento e todos os descendentes; `disableRules()` e `exclude()` pedem justificativa escrita e prazo.

Exemplo Playwright com TypeScript (do brain, adaptado; pacote `@axe-core/playwright`, confirmar nome e versão em npm):

```ts
import { test, expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];

async function varrer(page: Page, escopo?: string) {
  let builder = new AxeBuilder({ page }).withTags(TAGS);
  if (escopo) builder = builder.include(escopo); // ex.: '[role="dialog"]' com o diálogo aberto
  return (await builder.analyze()).violations;
}

test('cadastro em estado de erro continua acessível', async ({ page }) => {
  await page.goto('/cadastro');
  await page.getByRole('button', { name: 'Criar conta' }).click();
  await expect(page.getByText('Informe seu e-mail')).toBeVisible(); // conteúdo real, não o esqueleto
  const violacoes = await varrer(page);
  expect(violacoes, JSON.stringify(violacoes.map((v) => v.id))).toEqual([]);
});
```

Lighthouse: a nota de acessibilidade usa um subconjunto de regras do axe; nota 100 não é conformidade e não substitui axe nem teste manual (V-57).

## Roteiro manual

Faça por tarefa completa (cadastrar, comprar, recuperar senha), não por tela: os defeitos graves aparecem na transição entre telas.

### Teclado

Tab e Shift+Tab, Enter (link, botão), Espaço (botão, caixa de seleção), setas (rádio, abas, menu, slider), Esc (fecha diálogo e menu). No macOS, ative a navegação por teclado do sistema e, no Safari, "Pressionar Tab para destacar cada item"; sem isso o Tab pula links e você reporta falso defeito (brain).

1. O primeiro Tab mostra "Pular para o conteúdo", que leva ao `main` (2.4.1).
2. A ordem de foco segue a ordem visual (2.4.3); `tabindex` positivo é defeito.
3. Foco sempre visível (2.4.7) e não coberto por cabeçalho fixo, banner ou chat (2.4.11).
4. Tudo que funciona com mouse funciona com teclado (2.1.1): menu no hover, tooltip, carrossel, arrastar, seletor de data.
5. Sem armadilha de foco (2.1.2): sai de player, editor rico, mapa, iframe de pagamento.
6. Diálogo: foco entra, Tab circula dentro, Esc fecha, foco volta ao gatilho.
7. Conteúdo de hover ou foco sai com Esc e não some ao passar o ponteiro sobre ele (1.4.13).

### Leitor de tela

Combinações de referência: NVDA com Firefox ou Chrome e JAWS com Chrome (Windows), VoiceOver com Safari (macOS e iOS), TalkBack com Chrome (Android). Priorize a do seu público. Comandos úteis: NVDA liga com Ctrl+Alt+N, H navega por títulos, F por campos de formulário, NVDA+F7 lista elementos; VoiceOver no macOS liga com Cmd+F5, rotor com VO+U (VO = Ctrl+Option). Confira os atalhos na versão que você usa (Inferido).

Anote em três colunas (passo, o que foi anunciado, o que deveria ser) e verifique: nome, papel e estado de cada controle; conteúdo encontrável por títulos e marcos (`main`, `nav`); erro anunciado com o modo de corrigir; mudança dinâmica anunciada (item adicionado, toast); foco em lugar sensato após fechar diálogo, enviar formulário e trocar de rota em SPA (foco no `h1` ou novo título anunciado; a falha clássica é o foco ficar na página que sumiu). Comportamento de leitor que você não observou é Inferido, nunca fato.

### Zoom, reflow, movimento, cor e mídia

- Zoom de 200%: nada cortado ou sobreposto. Janela de 1280 px a 400%: só rolagem vertical (tabela, mapa e diagrama são exceção).
- Movimento reduzido ligado no sistema ou `page.emulateMedia({ reducedMotion: 'reduce' })`: parallax e animação de transição param (V-23).
- Nada só por cor (1.4.1): simule daltonismo no DevTools (Rendering, Emulate vision deficiencies); teste o tema escuro, que tem contraste próprio.
- Vídeo: legenda sincronizada e revisada (1.2.2); legenda automática sem revisão erra nome próprio e número (brain). Som automático por mais de 3 s precisa de controle (1.4.2).

## Formato de achado

Além do formato do relatório de revisão, inclua: critério WCAG (número, nome, nível), quem é afetado, tecnologia assistiva e navegador usados, o anunciado versus o esperado e a correção. Severidade pelo efeito na tarefa (impede sem contorno é alta), não só pelo `impact` do axe. Modelo completo: `../assets/templates/relatorio-a11y.md`.

Exemplo curto:

> **Carrinho: botão de remover item é anunciado só como "botão"** (4.1.2 Nome, função, valor, nível A). Afeta quem usa leitor de tela ou controle por voz. Ambiente: Windows 11, Firefox com NVDA. Esperado: "Remover Camiseta azul M do carrinho, botão". Obtido: "botão". Evidência: axe `button-name` em `.cart-item:nth-child(1) .icon-btn`. Severidade: alta (impede revisar o carrinho com autonomia). Correção: `<button type="button" aria-label="Remover Camiseta azul M do carrinho">` com o ícone em `<svg aria-hidden="true">`; após remover, foco no próximo item e aviso em `role="status"`.

Para agentes, o molde é `arquivo:linha - severidade - critério WCAG - esperado versus observado - correção` (V-17, V-61), com severidade Crítico (tarefa impossível), Alto (confunde, prende foco ou esconde erro), Médio (atrito com contorno) e Baixo (polimento), mais lista "não testado".

## Armadilhas da automação

- Varredura no esqueleto de carregamento dá zero violações e falso verde; espere o conteúdo real.
- Só desktop e tema claro: menu móvel e tema escuro têm violações próprias; rode a 375 px e no escuro.
- Excluir widget de terceiro "porque não é nosso": a barreira continua para o usuário; registre como risco.
- Medição durante animação: espere a transição terminar.
- `sr-only` com foco (link "pular para o conteúdo") mede 1x1 até receber foco; trate como exceção explícita.
- Foco por `focus()` programático pode não ativar `:focus-visible`; use Tab real.
- Gate só com `critical`: contraste costuma vir como `serious`, e a falha mais comum passa.
- Nota do Lighthouse como meta: nota 100 com teclado quebrado é comum.

## Público idoso

O W3C (WAI-AGE) aponta sobreposição entre necessidades de pessoas idosas e de pessoas com deficiência (visão, destreza, audição, cognição; Inferido, fonte não relida). Para público de 40 a 90 anos, puxe parâmetros acima da norma (valores do brain, Suposição de projeto): alvo de 44 px, corpo de 16 a 18 px, contraste 4,5:1 sem exceção, controle de fonte além do zoom, confirmação de ação destrutiva em palavras, ícone sozinho com nome acessível e legenda visível, `autocomplete` correto em login, aviso antes de a sessão expirar.
