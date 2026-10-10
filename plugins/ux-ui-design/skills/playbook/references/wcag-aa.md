# WCAG 2.2 AA para design: checklist, padrões e roteiro de teste

Como especificar e revisar acessibilidade no nível de design e de fluxo, e como orientar testes automáticos e manuais. Base: W3C WCAG 2.2 (V-08), ARIA APG (V-10), regras de acessibilidade para código de UI (V-09), Storybook/axe (V-37), movimento reduzido (V-38), INP (V-36) e o guia de acessibilidade do brain-of-agent (MIT, do autor do plugin, adaptado). Itens citados do brain e não reverificados nesta rodada levam "Não verificado".

## Sumário

- [Alvo e normas](#alvo-e-normas)
- [Fatos que corrigem erros comuns](#fatos-que-corrigem-erros-comuns)
- [Critérios novos da WCAG 2.2](#critérios-novos-da-wcag-22)
- [Limiares de referência](#limiares-de-referência)
- [Checklist AA por tela](#checklist-aa-por-tela)
- [Contraste: como calcular](#contraste-como-calcular)
- [Diálogo modal (APG)](#diálogo-modal-apg)
- [Formulários](#formulários)
- [Movimento e performance percebida](#movimento-e-performance-percebida)
- [Automação como piso](#automação-como-piso)
- [Roteiro manual](#roteiro-manual)
- [ARIA: erros de toda auditoria](#aria-erros-de-toda-auditoria)
- [Mobile e público idoso](#mobile-e-público-idoso)
- [Como reportar um achado](#como-reportar-um-achado)
- [Armadilhas da automação](#armadilhas-da-automação)

## Alvo e normas

Alvo técnico inicial para web: **WCAG 2.2 nível AA**, salvo contrato ou requisito aplicável diferente. Isso **não** declara conformidade à LBI, NBR 17060, EN 301 549 ou Section 508. Identifique jurisdição, produto, contrato e versão vigente antes de afirmar conformidade; sem parecer jurídico. Critérios AAA podem ser exigidos por contrato ou pelo público: não presuma dispensa.

| Referência | Escopo (orientação do brain; **Não verificado** juridicamente nesta rodada) |
| --- | --- |
| WCAG 2.2 (W3C) | Conteúdo web; base técnica de quase todas as leis. Não é lei. |
| ABNT NBR 17060:2022 | Aplicativos móveis; derivada da WCAG. Norma técnica, não lei. |
| LBI (Lei 13.146/2015, art. 63) | Sites de empresas com representação no Brasil e de governo; "diretrizes adotadas internacionalmente". |
| eMAG | Portais do governo federal. |
| European Accessibility Act e EN 301 549 | Produtos e serviços ao consumidor na UE; confirmar a versão da EN 301 549 citada oficialmente. |
| Section 508 (EUA) | Governo federal dos EUA e fornecedores; inclui software e documentação além de critérios web (fonte: U.S. Access Board, B-03). |
| WCAG 3 | Rascunho, não é norma. |

Overlay ("acessibilidade com uma linha de código") não dá conformidade (afirmação do brain; Não verificado).

## Fatos que corrigem erros comuns

- A Recommendation vigente da WCAG 2.2 é de **2024-12-12**; a publicação original foi de 2023-10-05. São **86** critérios (78 herdados + 9 novos - 4.1.1). Versões antigas do brain citam "2023" e "87": usar 2024-12-12 e 86 (Verificado, V-08).
- **4.1.1 Parsing foi removido.** Não reporte "HTML inválido"; reporte o efeito (id duplicado que quebra `aria-labelledby` falha 1.3.1 ou 4.1.2).
- 2.4.12 (foco não obscurecido, aprimorado) e 2.4.13 (aparência do foco) são AAA, não AA.
- O exemplo "#999 sobre branco ≈ 2,5:1" de um guia de terceiros está impreciso: calculado pela fórmula WCAG, #999999 sobre #FFFFFF é **2,85:1** (reprova 1.4.3 do mesmo jeito). #767676 sobre branco é 4,54:1 (passa).
- O Lighthouse não prova conformidade: nota 100 com teclado quebrado é comum.

## Critérios novos da WCAG 2.2

| Critério | Nível | Exige | Como testar |
| --- | --- | --- | --- |
| 2.4.11 Foco não obscurecido (mínimo) | AA | Elemento focado não fica totalmente escondido por conteúdo do autor | Tab com cabeçalho fixo, banner de cookies e chat abertos |
| 2.5.7 Movimentos de arrastar | AA | Alternativa de ponteiro simples a toda ação de arrastar | Reordenar lista, slider e kanban sem arrastar |
| 2.5.8 Tamanho do alvo (mínimo) | AA | 24×24 px CSS, ou espaçamento equivalente (círculo de 24 px sem sobrepor outro alvo); exceções: link em texto, controle nativo do agente de usuário, equivalente na página, essencial | Medir alvo computado; regra `target-size` do axe |
| 3.2.6 Ajuda consistente | A | Canal de ajuda repetido na mesma ordem relativa nas telas do fluxo | Comparar telas |
| 3.3.7 Entrada redundante | A | Não pedir de novo o que já foi informado no mesmo processo | Endereço de entrega → cobrança |
| 3.3.8 Autenticação acessível (mínimo) | AA | Entrar sem teste cognitivo obrigatório (decorar, transcrever, resolver) | Colar senha e código; gerenciador de senhas; CAPTCHA de texto sem alternativa reprova |

## Limiares de referência

| O quê | Critério | Nível | Valor |
| --- | --- | --- | --- |
| Contraste de texto | 1.4.3 | AA | 4,5:1; texto grande (≥ 24 px, ou ≥ 18,66 px em negrito) 3:1 |
| Contraste de componente e gráfico (borda de campo, ícone, foco) | 1.4.11 | AA | 3:1 |
| Redimensionar texto | 1.4.4 | AA | 200% sem perder conteúdo ou função |
| Reflow | 1.4.10 | AA | 320 px CSS de largura sem rolagem horizontal (equivale a 1280 px a 400%) |
| Espaçamento de texto | 1.4.12 | AA | linha 1,5×; parágrafo 2×; letras 0,12×; palavras 0,16× o tamanho da fonte |
| Conteúdo em hover ou foco | 1.4.13 | AA | dispensável (Esc), passável (o ponteiro entra nele) e persistente |
| Alvo de toque | 2.5.8 / 2.5.5 | AA / AAA | 24×24 / 44×44 px CSS |
| Tempo limite | 2.2.1 | A | desligar, ajustar ou estender; aviso com pelo menos 20 s para estender |
| Movimento automático | 2.2.2 | A | pausar, parar ou ocultar o que se move por mais de 5 s |
| Piscar | 2.3.1 | A | no máximo 3 flashes por segundo |

## Checklist AA por tela

Use `assets/templates/checklist-a11y-por-tela.md` para registrar status (Verificado, Inferido, Não testado). Itens essenciais, cada um com como testar:

1. Idioma da página (`<html lang>`) e título único por tela: inspeção + axe `html-has-lang`.
2. Estrutura: um `h1`, títulos sem saltos, landmarks (`main`, `nav`), link "pular para o conteúdo": inspeção + Tab.
3. Todo controle tem nome, papel e estado (4.1.2): árvore de acessibilidade do navegador ou leitor de tela.
4. Rótulo visível contido no nome acessível (2.5.3): comparar texto visível e nome computado.
5. Contraste 4,5:1 (texto) e 3:1 (componentes) nos estados padrão, hover, foco, desabilitado e erro, em claro e escuro: calcular (ver abaixo).
6. Nada só por cor (1.4.1): simular daltonismo no DevTools (Rendering → Emulate vision deficiencies).
7. Reflow em 320 px e zoom de 200% sem perda; espaçamento de texto aplicado sem cortar conteúdo.
8. Foco visível (2.4.7), não obscurecido (2.4.11), ordem de foco igual à visual (2.4.3), sem armadilha (2.1.2), sem `tabindex` positivo.
9. Alvos ≥ 24×24 px CSS (meta 44 em toque): medir o alvo computado, contando o `<label>` associado como área.
10. Conteúdo de hover e foco dispensável e persistente (1.4.13); tudo que funciona com mouse funciona com teclado (2.1.1).
11. Formulários: rótulo, instruções, erro ligado ao campo, `autocomplete`, entrada redundante, autenticação sem teste cognitivo (ver abaixo).
12. Movimento: `prefers-reduced-motion` respeitado; nada piscando mais de 3 vezes por segundo.
13. Imagens informativas com alternativa; decorativas com `alt=""`; ícone sozinho com nome acessível e, para público idoso, legenda visível.
14. Mídia: legenda sincronizada e revisada (1.2.2, A); audiodescrição ou alternativa (1.2.3 A, 1.2.5 AA); som automático por mais de 3 s com controle (1.4.2).

Se o alvo for um fluxo, escolha a tarefa crítica (cadastro, compra, recuperar senha) e aplique o checklist em cada transição entre telas: os defeitos graves aparecem nas transições.

## Contraste: como calcular

Fórmula da WCAG: luminância relativa `L = 0,2126·R + 0,7152·G + 0,0722·B`, com cada canal sRGB `c = valor/255` linearizado: `c/12,92` se `c ≤ 0,04045`, senão `((c+0,055)/1,055)^2,4` (a WCAG 2.2 usa 0,04045; textos antigos citam 0,03928, sem diferença prática). Razão = `(L_claro + 0,05) / (L_escuro + 0,05)`. Exemplos calculados em 2026-10-10 (Verificado, cálculo): #FFFFFF sobre #1A1C1E = 17,09:1 (o exemplo de saída do linter do `design.md` diz 15,42:1: não use o linter como oráculo); #0F766E sobre #FFFFFF = 5,47:1; #667085 sobre #FFFFFF = 4,97:1; #98A2B3 sobre #FFFFFF = 2,58:1 (reprova); #D0D5DD sobre #FFFFFF = 1,47:1 (serve para divisor decorativo, não para borda de campo, que pede 3:1).

Regras: meça no estado e no fundo reais, nunca pela imagem; texto sobre imagem ou gradiente entra na fila de revisão manual (o axe a classifica como `incomplete`); registre o par, o valor e o estado.

## Diálogo modal (APG)

Preferir `<dialog>` com `showModal()` (deixa o fundo inerte e fecha com Esc). Checklist de 9 itens (V-10, V-09):

1. `role="dialog"` com todo o conteúdo necessário como descendente; `aria-modal="true"` só quando a interação externa está de fato bloqueada e obscurecida.
2. Nome por `aria-labelledby` (título visível) ou `aria-label`.
3. Foco inicial no primeiro elemento focável; em conteúdo longo ou estruturado, num elemento estático com `tabindex="-1"` (por exemplo o título).
4. Em ação irreversível, considere focar a ação menos destrutiva.
5. Tab e Shift+Tab circulam dentro do diálogo; nem o Tab nem o cursor virtual do leitor escapam para o fundo.
6. Esc fecha.
7. Botão visível de fechar ou cancelar.
8. Ao fechar, o foco volta ao elemento que abriu (modal feito à mão: responsabilidade do código).
9. Sem `tabindex` positivo.

## Formulários

```html
<label for="email">E-mail</label>
<input id="email" name="email" type="email" autocomplete="email" required
       aria-invalid="true" aria-describedby="email-dica email-erro">
<p id="email-dica">Usaremos para enviar a nota fiscal.</p>
<p id="email-erro">Informe um e-mail no formato nome@exemplo.com.</p>
```

- Rótulo visível e associado; placeholder não é rótulo (some ao digitar).
- Obrigatório com `required` e indicação visível que não seja só cor nem asterisco sem legenda; `aria-invalid` só depois de validar.
- Erro diz como corrigir (3.3.3), ligado ao campo por `aria-describedby`. Ao enviar com erro, foco no primeiro campo inválido ou num resumo com links.
- Rádios relacionados em `fieldset` com `legend`; `autocomplete` correto em dados pessoais (1.3.5); não bloquear colar nem autofill.
- Live regions para toast e erro: a região precisa existir no DOM, vazia, **antes** da mensagem; inseri-la junto com o texto faz muitos leitores calarem. `role="status"` para avisos educados, `role="alert"` só para erro que bloqueia. Toast com ação que some em 3 s falha em tempo (2.2.1).

## Movimento e performance percebida

- Aplique a animação dentro de `@media (prefers-reduced-motion: no-preference)` (quem não entende a consulta também não recebe); movimento não essencial é removido sob `reduce`; o essencial pode ficar. "Reduzir" não é "zero movimento" (trecho de busca, Não lido). Em JavaScript, ouça `matchMedia('(prefers-reduced-motion: reduce)')` e o evento `change`, parando animações em andamento (V-38).
- Anime apenas `transform` e `opacity`; nunca `transition: all`; propriedades listadas (V-27).
- Fluxos de clique e tecla: **INP ≤ 200 ms** no percentil 75 (bom); 200 a 500 ms precisa melhorar; acima de 500 ms é ruim; medir primeiro em campo, separando móvel e desktop (V-36). Rolagem, hover e zoom não entram no INP.

## Automação como piso

**axe com violação = certamente inacessível; axe zerado ≠ acessível.** O axe-core, motor aberto por trás da maioria das ferramentas, pega a parte mecânica: contraste calculável, alt e rótulo ausentes, nome de botão e link, `lang`, ARIA inválido, `id` referenciado duplicado, `target-size`. A documentação do Storybook cita que o axe pega "até 57% dos problemas de WCAG" (V-37); o brain atribui os 57% a um estudo da Deque medido em volume de problemas, não em critérios (Não verificado). A máquina não decide se o alt descreve a imagem, se a ordem de foco faz sentido, se o widget customizado funciona no teclado, o que o leitor anuncia depois de uma ação.

- Tags do axe equivalentes a WCAG 2.2 AA: `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`. Regras `best-practice` não são critério WCAG: separe-as no relatório.
- Leia `incomplete` (o que o axe não conseguiu decidir): é a fila de revisão manual.
- Varra rotas e estados: carregada, diálogo aberto, formulário em erro, menu de celular, dropdown expandido, toast visível, tema escuro, 375 px.
- Em legado, congele as violações atuais (regra + seletor) como linha de base e falhe só em violação nova; `exclude()` e `disableRules()` escondem barreira real: registre motivo e risco.
- Storybook: `npx storybook add @storybook/addon-a11y`; `parameters.a11y.test`: `'off'`, `'todo'` (aviso na UI, sem falhar o CI) ou `'error'` (falha o teste); adoção gradual: `error` global, marcar os componentes falhos como `todo`, corrigir um a um (V-37). Instalar altera `package.json`: só com autorização.
- Código de automação (Playwright, Cypress, jest-axe, pa11y, Lighthouse CI) pertence a `/qa-testing:playbook` e `/web-frontend:playbook`; o script `auditoria_axe.py` do brain baixa o axe-core do cdnjs na primeira execução e exige `pip install playwright`: leia antes de rodar (ver `ferramentas-e-mcp.md`).

## Roteiro manual

Faça por tarefa completa, não por tela isolada. Só pessoas avaliam linguagem (termo desconhecido, instrução ambígua); quando der, observe 3 a 5 pessoas do público real em silêncio.

**Teclado** (Tab, Shift+Tab, Enter, Espaço, setas, Esc). No macOS ative a navegação por teclado do sistema e, no Safari, "Pressionar Tab para destacar cada item"; senão o Tab pula links e você reporta falso defeito.

1. O primeiro Tab mostra "Pular para o conteúdo" (2.4.1).
2. A ordem de foco segue a ordem visual (2.4.3).
3. O foco é sempre visível (2.4.7) e não coberto por cabeçalho fixo, banner de cookies ou chat (2.4.11).
4. Tudo que funciona com mouse funciona com teclado (2.1.1): menu no hover, tooltip, carrossel, arrastar, seletor de data.
5. Sem armadilha (2.1.2): saia de player, editor rico, mapa, iframe de pagamento.
6. Diálogo: foco entra, Tab circula, Esc fecha, foco volta ao gatilho.
7. Conteúdo de hover ou foco sai com Esc e não some ao passar o ponteiro sobre ele (1.4.13).

**Leitor de tela.** Combinações de referência: NVDA com Firefox ou Chrome e JAWS com Chrome (Windows), VoiceOver com Safari (macOS, iOS), TalkBack com Chrome (Android). Priorize a do público. Anote em três colunas: passo, o que foi anunciado, o que deveria ser. Verifique nome, papel e estado de cada controle; títulos e marcos para navegar; erro anunciado com o modo de corrigir; mudança dinâmica anunciada (item adicionado, total, toast); foco em lugar sensato depois de cada ação (fechar diálogo, enviar formulário, trocar de rota em SPA: foco no `h1` ou novo título anunciado; a falha clássica é o foco ficar na página que sumiu).

| Ação | NVDA (tecla NVDA = Insert) | VoiceOver macOS (VO = Ctrl+Option) |
| --- | --- | --- |
| Ligar | Ctrl+Alt+N | Cmd+F5 |
| Próximo título / por nível | H / 1 a 6 | VO+Cmd+H |
| Próximo campo de formulário | F | VO+Cmd+J |
| Lista de elementos (rotor) | NVDA+F7 | VO+U |
| Modo navegação ↔ formulário | NVDA+Espaço | n/a |

Atalhos do JAWS e gestos de celular: conferir no tutorial da versão instalada (Não verificado nesta rodada; os gestos de TalkBack mudam com a versão).

**Zoom, movimento, cor e mídia.** Zoom de 200%: nada cortado ou sobreposto. Janela de 1280 px a 400%: só rolagem vertical (tabela, mapa e diagrama são exceção). Fonte grande do sistema somada ao zoom; retrato e paisagem (1.3.4). Movimento reduzido ligado no sistema: parallax e transições param. Tema escuro tem contraste próprio: teste.

## ARIA: erros de toda auditoria

**Nenhum ARIA é melhor que ARIA ruim.** ARIA muda o que é anunciado, não o comportamento: `<div role="button">` não recebe foco nem responde a Enter e Espaço. Use o elemento nativo (`button`, `a`, `input`, `select`, `dialog`) e ARIA só onde o HTML não tem o padrão. Para widgets personalizados, localize o padrão no APG (https://www.w3.org/WAI/ARIA/apg/patterns/) e implemente semântica e interação, não só o papel.

- `aria-label` em `div` ou `span` sem papel: vários leitores ignoram.
- `aria-hidden="true"` em elemento focável ou em ancestral dele: o foco cai em algo que o leitor diz não existir.
- Nome acessível diferente do texto visível (2.5.3): quem usa voz diz "clicar Enviar" e nada acontece porque o nome é `submit-form`.
- `role="presentation"` em tabela de dados; `aria-live` em região que muda a cada segundo.
- `role="combobox"` sem `aria-label` ou `aria-labelledby`: o leitor anuncia só "caixa de combinação". Abas usadas como filtro, com `aria-controls` apontando para painel inexistente, são na verdade um grupo de botões com `aria-pressed`.

## Mobile e público idoso

- Alvo: 44×44 pt (iOS padrão; ver `apple-e-plataformas.md`) e 48×48 dp (Android) são as referências das plataformas; 48 dp é **Não verificável** aqui (Material 3 é lacuna). Os 24 px CSS da WCAG são piso.
- Nome acessível por plataforma: Android `contentDescription`; iOS `accessibilityLabel`; React Native `accessibilityLabel` com `accessibilityRole`; Flutter `Semantics(label: …)`. Não ponha o papel no rótulo ("botão Salvar" vira "botão Salvar, botão"). Implementação nativa: `/mobile-apps:playbook`.
- Texto: Dynamic Type no iOS e escala de fonte no Android; na escala máxima o texto não trunca e a tela rola.
- Gestos de vários dedos e sacudir o aparelho precisam de alternativa simples (2.5.1, 2.5.4).
- Público de 40 a 90 anos (a pesquisa WAI-AGE do W3C mostra sobreposição com necessidades de pessoas com deficiência; fonte lida pelo brain, Não verificado): alvo 44 px, corpo 16 a 18 px (piso 14), contraste 4,5:1 sem exceção (7:1 onde couber), ampliação de 200% mais controle de fonte na interface, confirmação destrutiva que diz em palavras o que vai acontecer, ícone com nome acessível e legenda, `autocomplete` nos campos de acesso, aviso antes de a sessão expirar.

## Como reportar um achado

Use `assets/templates/achado-a11y.md`. Campos: critério WCAG (número, nome, nível), quem é afetado, tecnologia assistiva e navegador, passos, esperado, obtido (o que foi **anunciado**), evidência, severidade pelo efeito na tarefa (impede sem contorno → alta), correção. Escala de severidade do plugin: crítico (antes do merge), importante (na sprint), sugestão (V-09), que mapeia para alta, média e baixa.

Exemplo resumido: **Carrinho: botão de remover item é anunciado só como "botão"** · 4.1.2 Nome, função, valor (A) · afeta leitor de tela e controle por voz · esperado "Remover Camiseta azul M do carrinho, botão" · obtido "botão" · evidência: axe `button-name` em `.cart-item:nth-child(1) .icon-btn` · severidade alta (impede revisar o carrinho com autonomia) · correção: `<button type="button" aria-label="Remover Camiseta azul M do carrinho">` com o ícone em `<svg aria-hidden="true">`; depois de remover, foco no próximo item e aviso em `role="status"`.

## Armadilhas da automação

- Varredura no esqueleto de carregamento dá zero violações e falso verde: espere o conteúdo real.
- Só desktop e tema claro: menu de celular e tema escuro têm violações próprias; rode a 375 px e no escuro.
- Excluir widget de terceiro "porque não é nosso": a barreira continua para o usuário; registre como risco e cobre o fornecedor.
- Medição durante animação: espere a transição terminar.
- "Pular para o conteúdo" escondido com `sr-only` mede 1×1 até receber foco: trate como exceção explícita.
- Foco por `focus()` programático pode não ativar `:focus-visible`: use Tab real.
- Gate só com `critical` deixa passar contraste, que costuma vir como `serious`.
- Nota do Lighthouse como meta: nota 100 com teclado quebrado é comum; use como tendência (`"categories:accessibility": ["error", {"minScore": 0.95}]` no Lighthouse CI, exemplo do brain).
- JSDOM não tem layout: contraste, alvo e reflow não existem em teste de componente isolado.
