# Checklist WCAG 2.2 AA por tela

Cada linha: o que exigir, o critério, como testar à mão e o que a automação cobre. Marque cada item como Verificado (testado, com método), Inferido (lido no código ou visto em captura), Não testado ou Não aplicável. Nível e numeração conferidos na Recommendation de 2024-12-12 (https://www.w3.org/TR/WCAG22/; V-08). Redação própria.

## Sumário

- [Percepção](#percepção)
- [Operação](#operação)
- [Compreensão](#compreensão)
- [Robustez](#robustez)
- [Critérios novos da WCAG 2.2](#critérios-novos-da-wcag-22)
- [Limiares de referência](#limiares-de-referência)
- [Automático versus manual](#automático-versus-manual)

## Percepção

| Exigir | Critério (nível) | Teste manual | Automação |
| --- | --- | --- | --- |
| Imagem informativa com alternativa que diga a função; decorativa com `alt=""` | 1.1.1 (A) | ler o `alt` fora de contexto: dá para entender o que a imagem faz? | acha `alt` ausente; não julga se descreve |
| Estrutura real: títulos, listas, tabelas, regiões; um `h1` por tela, sem saltos | 1.3.1 (A) | navegar por títulos e marcos com leitor de tela | acha parte dos saltos |
| Ordem de leitura coerente com a visual | 1.3.2 (A) | desligar CSS ou navegar com leitor | não cobre |
| Campos de dados pessoais com `autocomplete` correto | 1.3.5 (AA) | conferir o atributo em nome, e-mail, endereço, cartão | cobre parte |
| Informação nunca só por cor | 1.4.1 (A) | simular daltonismo no DevTools (Rendering, Emulate vision deficiencies) | não cobre |
| Contraste de texto 4,5:1 (3:1 se grande) | 1.4.3 (AA) | calcular com valores reais de estado e fundo ([contraste-wcag](${CLAUDE_PLUGIN_ROOT}/skills/design-tokens/references/contraste-wcag.md)) | cobre os pares calculáveis; fundo com imagem vai para `incomplete` |
| Texto ampliável a 200% sem perder conteúdo ou função | 1.4.4 (AA) | zoom do navegador a 200% | não cobre |
| Reflow a 320 px CSS, sem rolagem em duas dimensões (tabela, mapa e diagrama são exceção) | 1.4.10 (AA) | janela de 320 px ou 1280 px a 400% | `scrollWidth` do `html` em teste próprio |
| Contraste de componentes e estados 3:1 (borda de campo, ícone, foco, gráfico) | 1.4.11 (AA) | medir contra a cor adjacente | cobre parte |
| Espaçamento de texto ajustável (linha 1,5×, parágrafo 2×, letras 0,12×, palavras 0,16× o corpo) sem perda | 1.4.12 (AA) | injetar CSS com `!important` e procurar cortes (`overflow: hidden`) | não cobre |
| Conteúdo de hover ou foco: dispensável (Esc), passável (o ponteiro pode ir até ele), persistente | 1.4.13 (AA) | tooltip e menu: Esc fecha? o ponteiro pode entrar nele? | não cobre |
| Vídeo com legenda revisada; áudio com transcrição | 1.2.1, 1.2.2, 1.2.3, 1.2.5 | assistir | não cobre |

## Operação

| Exigir | Critério (nível) | Teste manual | Automação |
| --- | --- | --- | --- |
| Tudo que o mouse faz, o teclado faz (menu em hover, tooltip, carrossel, seletor de data) | 2.1.1 (A) | Tab, Shift+Tab, Enter, Espaço, setas, Esc | não cobre |
| Sem armadilha de teclado (player, editor rico, mapa, iframe de pagamento) | 2.1.2 (A) | sair de cada widget só com teclado | não cobre |
| Pular para o conteúdo no primeiro Tab, levando ao `main` | 2.4.1 (A) | primeiro Tab mostra o link | acha parte |
| Título de aba único e descritivo por tela | 2.4.2 (A) | ler o `title` | cobre presença |
| Ordem de foco segue a visual; sem `tabindex` positivo | 2.4.3 (A) | Tab pela tela inteira | acha `tabindex` positivo |
| Texto de link que faz sentido no contexto | 2.4.4 (A) | lista de links do leitor de tela | acha "clique aqui" só com regra própria |
| Títulos e rótulos descrevem o tópico ou a finalidade | 2.4.6 (AA) | ler | não cobre |
| Foco sempre visível | 2.4.7 (AA) | Tab real (o `focus()` programático pode não ativar `:focus-visible`) | não cobre bem |
| Tempo limite ajustável, com aviso de pelo menos 20 s para estender | 2.2.1 (A) | esperar a sessão expirar | não cobre |
| Algo que se move por mais de 5 s pode ser pausado | 2.2.2 (A) | carrossel, vídeo de fundo | não cobre |
| No máximo 3 flashes por segundo | 2.3.1 (A) | revisar animações | não cobre |
| Alvo com rótulo visível contido no nome acessível | 2.5.3 (A) | comparar texto visível e nome acessível | cobre parte |

## Compreensão

| Exigir | Critério (nível) | Teste manual | Automação |
| --- | --- | --- | --- |
| `lang` correto na página | 3.1.1 (A) | inspecionar `<html lang>` | cobre |
| Foco e contexto não mudam sozinhos ao focar ou preencher | 3.2.1, 3.2.2 (A) | preencher sem enviar | não cobre |
| Todo campo com rótulo ou instrução | 3.3.2 (A) | placeholder não é rótulo | cobre rótulo ausente |
| Erro identificado em texto e ligado ao campo | 3.3.1 (A) | enviar vazio | cobre parte |
| Erro com sugestão de correção quando conhecida | 3.3.3 (AA) | ler as mensagens | não cobre |
| Ações legais, financeiras ou de dados reversíveis, verificadas ou confirmadas | 3.3.4 (AA) | fluxo de pagamento e exclusão | não cobre |

## Robustez

| Exigir | Critério (nível) | Teste manual | Automação |
| --- | --- | --- | --- |
| Nome, papel e estado programáticos em todo controle (botão com ícone tem nome) | 4.1.2 (A) | leitor de tela: "Remover Camiseta azul, botão" | cobre nome vazio e ARIA inválido |
| Mensagens de status anunciadas sem mover o foco (toast, total do carrinho, resultado de busca) | 4.1.3 (AA) | provocar a mudança com leitor ligado | não cobre |

O critério 4.1.1 Parsing foi removido na 2.2; não o use.

## Critérios novos da WCAG 2.2

| Critério | Nível | Exige | Como testar |
| --- | --- | --- | --- |
| 2.4.11 Foco não obscurecido (mínimo) | AA | o elemento focado não fica totalmente escondido por conteúdo do autor | Tab com cabeçalho fixo, banner de cookies e chat abertos; use `scroll-padding` igual à altura da barra fixa |
| 2.5.7 Movimentos de arrastar | AA | alternativa de ponteiro simples para toda ação de arrastar | reordenar lista, slider e kanban sem arrastar |
| 2.5.8 Tamanho do alvo (mínimo) | AA | 24×24 px CSS, ou espaçamento equivalente; exceções: link em texto corrido, controle nativo do navegador, equivalente na página, essencial | medir; `target-size` do axe ajuda |
| 3.2.6 Ajuda consistente | A | canal de ajuda na mesma ordem relativa em todas as telas | comparar as telas do fluxo |
| 3.3.7 Entrada redundante | A | não pedir de novo o que já foi informado no mesmo processo | endereço de entrega repetido na cobrança |
| 3.3.8 Autenticação acessível (mínimo) | AA | entrar sem teste cognitivo (decorar, transcrever, resolver) | colar senha e código; gerenciador de senhas; CAPTCHA de texto sem alternativa reprova |

AAA que costumam ser confundidos com AA: 2.4.12 Foco não obscurecido (aprimorado), 2.4.13 Aparência do foco, 3.3.9 Autenticação acessível (aprimorado), 2.5.5 Tamanho do alvo (aprimorado, 44×44 px).

## Limiares de referência

| O quê | Valor |
| --- | --- |
| Texto normal / grande (a partir de 24 px, ou 18,66 px em negrito) | 4,5:1 / 3:1 |
| Componente de interface e gráfico | 3:1 |
| Alvo mínimo (norma) / meta de toque / AAA | 24 px / 44 px / 44 px CSS |
| Aviso de sessão para estender | pelo menos 20 s |
| Movimento automático sem pausa | até 5 s |
| Flashes | no máximo 3 por segundo |

## Automático versus manual

- axe e semelhantes acertam a parte mecânica: contraste calculável, `alt` e rótulo ausentes, nome de botão e link, `lang`, ARIA inválido, `id` referenciado duplicado, título, tamanho de alvo. A documentação do Storybook cita que a automação encontra "até 57%" dos problemas de WCAG (V-37); o dado depende da amostra e deve ser citado com essa ressalva.
- A máquina não julga se o `alt` descreve a imagem, se a ordem de foco faz sentido, se o widget funciona no teclado, o que o leitor anuncia depois de uma ação, se o erro ajuda. `axe com violação = certamente inacessível; axe zerado ≠ acessível`.
- Rode por rota **e por estado**: carregada (conteúdo real, não o esqueleto), diálogo aberto, formulário em erro, menu móvel, dropdown expandido, toast, tema escuro, 375 px.
- Em legado, não desligue regras: congele as violações atuais (regra e seletor) como linha de base e falhe só com violação nova.
- Tags de regra do axe que juntas equivalem a WCAG 2.2 AA: `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`. Regras `best-practice` não são critério WCAG; separe-as no relatório. Confira a versão do axe instalada.
