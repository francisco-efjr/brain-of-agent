# Dez categorias de auditoria de UI

Cada item recebe PASS, PARTIAL ou FAIL com evidência. Etiquetas: `[script]` quando uma regra, contagem ou `Grep` comprova; `[julgamento]` quando é opinião fundamentada (rótulo Inferido). Limiares marcados "polegar" são regras de polegar do workflow de origem, úteis como alerta e não como norma; normas WCAG e INP estão marcadas "norma" (Verificado nas fontes V-08 e V-36).

Origem: as dez categorias adaptam o `design-review` do gstack (MIT, Garry Tan; redação própria). O formato de crítica de hierarquia vem de V-28 (MIT). Wireframes e capturas de referência: 375, 768 e 1440 px.

## Sumário

1. [Hierarquia e composição](#1-hierarquia-e-composição)
2. [Tipografia](#2-tipografia)
3. [Cor e contraste](#3-cor-e-contraste)
4. [Espaçamento e layout](#4-espaçamento-e-layout)
5. [Estados de interação](#5-estados-de-interação)
6. [Responsividade](#6-responsividade)
7. [Movimento](#7-movimento)
8. [Conteúdo e microcopy](#8-conteúdo-e-microcopy)
9. [Sinais de visual genérico de IA](#9-sinais-de-visual-genérico-de-ia)
10. [Desempenho percebido](#10-desempenho-percebido)
11. [Como ler o impacto](#como-ler-o-impacto)

## 1. Hierarquia e composição

| Item | Etiqueta | PASS quando |
| --- | --- | --- |
| Ponto focal e ação primária | julgamento | existe uma zona primária por tela e no máximo uma ação primária por vista |
| Fluxo do olhar | julgamento | a leitura segue a ordem da tarefa; o ponto de entrada é óbvio |
| Ruído visual | julgamento | elementos não competem por atenção; peso compatível com a importância |
| Teste do olho semicerrado | julgamento | desfocada, a hierarquia ainda aparece |
| Propósito em 3 segundos | julgamento | o conteúdo acima da dobra diz o que a página oferece |
| Sobreposição | script/julgamento | nada se sobrepõe de forma inesperada (z-index) |
| Densidade | julgamento | adequada ao tipo de conteúdo e à superfície |
| Espaço em branco | julgamento | intencional, não sobra de layout |

Falhas típicas: primários concorrentes, hierarquia achatada (tudo com o mesmo peso), ênfase falsa (destaque em item secundário), chamada principal enterrada.

## 2. Tipografia

| Item | Etiqueta | PASS quando |
| --- | --- | --- |
| Famílias | script | até 3 famílias (polegar) |
| Corpo | script | pelo menos 16 px; rótulos e legendas pelo menos 12 px (polegar) |
| Escala | script/julgamento | passos com razão consistente (por exemplo 1,25 ou 1,333; polegar) |
| Altura de linha | script | cerca de 1,5 no corpo e 1,15 a 1,25 em títulos (polegar) |
| Medida | script | 45 a 75 caracteres por linha, abaixo de 80 (polegar; o plano de design adota < 80) |
| Títulos | script | sem salto de nível (h1 para h3 sem h2); um h1 por tela |
| Contraste de peso | julgamento | pelo menos dois pesos distintos constroem a hierarquia |
| Fonte padrão do sistema como primária | julgamento | numa superfície Persuade/Experience há escolha tipográfica deliberada; num app (Operate) fonte neutra passa se o DESIGN.md disser |
| Detalhes | script | `font-variant-numeric: tabular-nums` em colunas de números; reticências com o caractere `…` em estados de carregamento; aspas tipográficas (polegar, polimento) |

## 3. Cor e contraste

| Item | Etiqueta | PASS quando |
| --- | --- | --- |
| Texto | script | 4,5:1 normal, 3:1 grande (norma 1.4.3), calculado nos valores reais |
| Componentes | script | 3:1 para borda de campo, ícone sem texto, indicador de foco (norma 1.4.11) |
| Cor nunca única | julgamento | estado e erro têm também texto, ícone ou padrão (norma 1.4.1) |
| Paleta coerente | script/julgamento | até cerca de 12 cores não neutras distintas (polegar); neutros todos quentes ou todos frios |
| Cores semânticas | julgamento | sucesso, erro e aviso consistentes em todo o produto |
| Daltonismo | julgamento | nada depende só de vermelho contra verde |
| Modo escuro, se existir | julgamento/script | superfícies por elevação, não só inversão; texto não é branco puro por padrão (polegar); contraste recalculado no escuro; `color-scheme: dark` declarado |

## 4. Espaçamento e layout

| Item | Etiqueta | PASS quando |
| --- | --- | --- |
| Escala de espaçamento | script | valores vêm de uma escala (base 4 ou 8 px), não de números arbitrários |
| Ritmo | julgamento | itens relacionados mais próximos, seções distintas mais afastadas |
| Alinhamento e grade | julgamento | nada flutua fora da grade; consistente entre breakpoints |
| Hierarquia de raios | julgamento | raios variam por papel; raio interno = raio externo menos o intervalo |
| Largura máxima de leitura | script | texto corrido não ocupa a largura toda |
| Rolagem horizontal | script | nenhuma em 320 e 375 px |
| Notch | script | `env(safe-area-inset-*)` quando houver barras fixas em celulares com recorte |
| Estado na URL | julgamento | filtros, abas e paginação refletidos na URL quando fizer sentido |

## 5. Estados de interação

| Item | Etiqueta | PASS quando |
| --- | --- | --- |
| Foco visível | script | `:focus-visible` com contorno visível; `outline: none` só com substituto equivalente |
| Hover, ativo, desabilitado | script/julgamento | todos os elementos interativos têm os quatro estados distinguíveis |
| Carregando | julgamento | esqueleto com o formato do conteúdo real; sem salto de layout |
| Vazio | julgamento | mensagem útil, motivo e ação principal, não apenas "Nenhum item" |
| Erro | julgamento | específico e com próximo passo (ver [ux-writing](${CLAUDE_PLUGIN_ROOT}/skills/ux-writing/SKILL.md)) |
| Sucesso | julgamento | confirmação perceptível; some sozinha só se não esconder informação necessária |
| Alvo | script | no mínimo 24×24 px CSS (norma 2.5.8); meta de toque 44 px |
| Escolha sem esforço | julgamento | em cada ponto de decisão fica óbvio o que acontece ao clicar; quando exige pensar, impacto alto |

## 6. Responsividade

| Item | Etiqueta | PASS quando |
| --- | --- | --- |
| Layout mobile faz sentido | julgamento | não é a coluna do desktop empilhada sem decisão |
| Reflow | script | 320 px sem rolagem em duas dimensões (norma 1.4.10) |
| Viewport | script | sem `user-scalable=no` nem `maximum-scale=1` |
| Texto | script | corpo legível sem zoom (pelo menos 16 px) |
| Navegação | julgamento | recolhe de forma previsível |
| Formulários no celular | script | `type`, `inputmode` e `autocomplete` corretos; fonte do campo de pelo menos 16 px evita zoom automático no iOS (regra citada em V-27) |
| Imagens | script | `srcset`/`sizes` ou contenção CSS; largura e altura definidas |

## 7. Movimento

| Item | Etiqueta | PASS quando |
| --- | --- | --- |
| Movimento reduzido | script | animação não essencial sob `prefers-reduced-motion: no-preference` ou removida em `reduce` |
| Propriedades | script | sem `transition: all`; anima `transform` e `opacity`, não largura, altura, `top`, `left` |
| Propósito | julgamento | cada animação comunica mudança de estado, atenção ou relação espacial |
| Faixa de duração | julgamento | cerca de 50 a 700 ms (polegar; sem diretriz oficial lida) |
| Easing | julgamento | saída para entrar, entrada para sair, ambos para mover (polegar) |
| Um momento orquestrado | julgamento | não repete a mesma entrada em todas as seções; conteúdo nunca fica escondido atrás do tempo da animação |
| Conteúdo móvel | script | mais de 5 s tem pausa (WCAG 2.2.2); no máximo 3 flashes por segundo (2.3.1) |

## 8. Conteúdo e microcopy

| Item | Etiqueta | PASS quando |
| --- | --- | --- |
| Botões | julgamento | verbo + objeto específico, não "Enviar" nem "Continuar" isolados |
| Erros | julgamento | o que aconteceu, por quê, o que fazer agora |
| Placeholder e lorem ipsum | script | nenhum visível em produção |
| Truncamento | script | tratado com reticências, `line-clamp` ou quebra; informação essencial não é cortada |
| Voz ativa | julgamento | "Instale a CLI", não "A CLI será instalada" |
| Ação destrutiva | julgamento | confirmação que nomeia o que será perdido, ou desfazer |
| Conversa fiada | julgamento | parágrafos de boas-vindas e autoelogio que não ajudam a tarefa; se dá para ouvir "blá blá blá", cortar |
| Instruções longas | julgamento | instrução de mais de uma frase sinaliza uma interação que falhou; registrar a instrução e a interação que ela compensa |

## 9. Sinais de visual genérico de IA

Pergunta-guia: um designer de estúdio respeitado entregaria isto? Só é defeito se o briefing não pediu. Cada sinal vale como alerta; um item que o briefing ou a marca mandam é PASS com nota.

| Sinal | Etiqueta |
| --- | --- |
| Fundo ou esquema em gradiente roxo/violeta/índigo | script (Grep) |
| Grade de três colunas com ícone em círculo colorido, título em negrito e duas linhas, repetida três vezes | julgamento |
| Ícones em círculos coloridos como decoração de seção | julgamento |
| Tudo centralizado (títulos, descrições, cartões) | script (contagem de `text-align: center`) |
| Mesmo raio grande em todos os elementos | script |
| Bolhas decorativas, círculos flutuantes, divisores ondulados em SVG | julgamento |
| Emoji como elemento de design (foguete no título, emoji como marcador) | script |
| Borda lateral colorida em cartões | script (Grep) |
| Texto de herói genérico ("Bem-vindo a…", "Libere o poder de…", "Sua solução completa para…") | julgamento |
| Ritmo de seções de template (herói, três recursos, depoimentos, preços, chamada, todas com a mesma altura) | julgamento |
| Fonte do sistema como principal de exibição | script |
| Botão primário em gradiente; hero com foto de banco genérica ou caixa cinza no lugar | julgamento |
| Cartões com sombra como contêiner de tudo; vidro fosco como superfície padrão | julgamento |
| Depoimentos com avatares, estrelas e falas que ninguém disse; três números grandes sem fonte | julgamento |
| "Saiba mais" e "Começar" como únicas chamadas | julgamento |
| Rabiscos e mascotes SVG gerados no lugar de direção de arte | julgamento |
| Todo caminho secundário dentro de modal | julgamento |
| Gráficos de linha pequenos, anéis de progresso e avatares falsos preenchendo espaço onde faltou conteúdo | julgamento |
| Só o caminho feliz desenhado | julgamento (vira achado da categoria 5) |
| Escolha de claro ou escuro por clichê ("escuro porque é ferramenta de dev") em vez de cena de uso | julgamento |

Sinais de polimento (anote, não pontue): espaçamento monótono, easing com salto, ponto pulsante, cursor piscante, rótulos de seção numerados, excesso de travessões, espaçamento de letras muito negativo, sombra larga com borda fina, fundo de grade ou listras repetidas, transformação de imagem no hover, fonte monoespaçada como fantasia, superfícies do navegador sem tema (`::selection`, cursor de texto, barras de rolagem).

Reuse a lista com cautela: ela é de 2026, envelhece e a correção vira o novo default (relatos de deriva para creme + terracota existem).

## 10. Desempenho percebido

| Item | Etiqueta | PASS quando |
| --- | --- | --- |
| Resposta a clique e tecla | script (campo) | INP bom: até 200 ms no percentil 75; entre 200 e 500 ms precisa melhorar; acima, ruim (norma web.dev, V-36); medir antes e depois, em campo quando possível |
| Estabilidade de layout | script | sem saltos visíveis no carregamento (CLS "bom" até 0,1; Inferido, conferir web.dev) |
| Carregamento do maior elemento | script | LCP "bom" até 2,5 s no p75 (Inferido, conferir web.dev); metas mais duras do workflow de origem são polegar |
| Esqueleto | julgamento | mesmo formato do conteúdo real |
| Imagens | script | `loading="lazy"` abaixo da dobra, dimensões definidas, formatos modernos |
| Fontes | script | `font-display: swap`; fontes críticas pré-carregadas para evitar troca visível |

Medidas de campo exigem instrumentação; sem elas, escreva "não medido".

## Como ler o impacto

- **Alto**: impede ou atrapalha a tarefa principal, ou falha o teste de tronco, ou barra um usuário com deficiência.
- **Médio**: degrada a experiência sem impedir a tarefa; inconsistências de sistema.
- **Polimento**: acabamento; anote, não bloqueie a entrega.
- Um FAIL na tarefa principal é impacto alto mesmo com bom acabamento.
