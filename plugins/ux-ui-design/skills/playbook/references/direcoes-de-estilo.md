# Direções de estilo: catálogo para escolher antes de desenhar

Conteúdo validado em 2026-10-11. Pesquisa técnica (agente com leitura de código, registros shadcn, CSS compilado e payloads) em três fontes: **cult-ui** (github.com/nolly-studio/cult-ui, MIT), **Skiper UI** (skiper-ui.com, componentes free com atribuição obrigatória e Pro pago) e **OriginKit** (originkit.dev, licença proprietária). Este arquivo filtra o que serve para decisão de design e transforma em **direções nomeadas**: o agente de design pergunta qual seguir em vez de cair no visual default do modelo. A forma do componente (arquivos, API, doc) é sempre a de [padrao-componente-cult-ui](padrao-componente-cult-ui.md), qualquer que seja a direção.

## Sumário

1. Quando perguntar e quando não
2. Roteiro de perguntas do agente de design
3. Catálogo de direções (D1 a D10)
4. Eixos independentes: aparência, movimento, densidade
5. Presets de movimento
6. Técnicas assinatura (com regra de acessibilidade)
7. Como uma direção vira código
8. Licenças e o que nunca copiar
9. Filtro aplicado: o que entrou e o que ficou de fora

## 1. Quando perguntar e quando não

| Situação | Ação |
| --- | --- |
| Projeto tem design system, `DESIGN.md` ou tokens | **Não pergunte direção.** O sistema vence (princípio 2 do playbook). Direção só entra se o usuário pedir "nova direção" ou "redesign". |
| Usuário pediu o design system da casa (Mo baile) | Use o Mo baile ([design-system-da-casa](design-system-da-casa.md)); não ofereça o catálogo. |
| Produto novo, sem sistema, ou pedido de "nova cara", "redesign", "landing" | **Pergunte** com o roteiro da seção 2. A primeira opção é sempre o design system da casa (Mo baile, adaptado à plataforma); as outras são as direções recomendadas para a superfície. |
| Modo sem interação (lote, subagente) | Não pergunte. Sem sistema no projeto, use o da casa adaptado à plataforma (regra do `ORCHESTRATOR.md`); com pedido de nova direção, escolha pela tabela de recomendação por superfície. Rotule **Suposição** e liste a escolha em "Decisões pendentes do humano" com as duas alternativas mais próximas. |

## 2. Roteiro de perguntas do agente de design

Uma pergunta por vez, só as que mudam o resultado. Use `AskUserQuestion` quando disponível; senão, lista numerada.

1. **Superfície** (se não estiver claro no pedido): Operate (app, painel), Persuade (landing, marketing), Read (docs), Experience (portfólio, campanha).
2. **Direção:** ofereça o design system da casa (quando não houver sistema no projeto) e as **3 recomendadas** para a superfície (tabela abaixo), cada opção com uma linha de "parece com" e uma de "custa". Sempre ofereça "Outra direção do catálogo" e "Misturar duas (base + acento)".
3. **Aparência:** claro, escuro ou os dois (padrão: os dois para Operate; o que a direção sugere para Persuade).
4. **Intensidade de movimento:** sutil, expressivo ou cinemático (seção 4). Cinemático só em Persuade e Experience.

Recomendação por superfície (as primeiras são as mais seguras):

| Superfície | Recomendadas | Possíveis com justificativa |
| --- | --- | --- |
| Operate (app, painel, ferramenta) | D3 Ledger limpo · D1 Halo fosco · D7 Estúdio escuro · D5 Vidro Apple | D2 Tátil (apps de consumo) |
| Persuade (landing, marketing) | D4 Detalhe obsessivo · D6 Editorial · D2 Tátil · D1 Halo fosco | D8 Cinemático (só no hero), D9 Generativo, D10 Lúdico |
| Read (docs, base de conhecimento) | D3 Ledger limpo · D4 Detalhe obsessivo | D7 Estúdio escuro |
| Experience (portfólio, campanha, evento) | D6 Editorial · D8 Cinemático · D9 Generativo · D10 Lúdico | qualquer uma |

Misturas que funcionam: D3 + acento D1 (painel sóbrio com botão primário Halo); D4 + acento D6 (landing contida com um título editorial); D7 + hero D8 (site escuro com um único fundo WebGL). Evite misturar duas direções expressivas (D8 + D10).

## 3. Catálogo de direções

Valores são **ponto de partida** observado nas fontes, não marca do usuário: vão para tokens primitivos e passam pelo contraste calculado antes de virar semânticos. Fonte da observação entre colchetes.

### D1 · Halo fosco
- **Parece com:** cápsulas translúcidas com borda luminosa animada; Vercel encontra iOS. [cult-ui, kit Halo, 2025–2026]
- **Superfície:** pílulas `rounded-full`; preenchimento `backdrop-blur-xl backdrop-saturate-150` sobre `color-mix(in oklch, var(--card) 82%, transparent)`; realce interno `0 1px 0 rgb(255 255 255 / .1) inset`.
- **Assinatura:** aro em gradiente desfocado que desliza na borda inferior (`#ff0080 → #7928ca → #00d4ff → #0070f3`, laço de 4 a 6 s); rótulo com fade escalonado de 18 ms por caractere; pressionar `active:scale-[0.96]`.
- **Movimento:** preset *snappy-layout* (seção 5). **Tipo:** Geist ou fonte do sistema, peso 450 a 500.
- **Componentes de referência:** Halo Button, Input, Select, Switch, Segmented, Tabs, Badge, Progress, Toast, Dropzone. **Custa:** blur em listas longas pesa em GPU fraca; aro animado precisa parar com movimento reduzido.

### D2 · Tátil (texturizado, skeuo-soft)
- **Parece com:** objetos físicos com bisel, papel creme e botões que afundam. [cult-ui Texture/Neumorph; seções claras do OriginKit]
- **Superfície:** bordas aninhadas concêntricas (4 a 5 camadas, `rounded-[24→20px]`, alternando `white/50` e `black/10`); micro-gradiente vertical em todo preenchimento (`from-neutral-800 to-black`, invertido no pressionado); fundo creme `#f4f0e8`; sombras empilhadas com realce interno.
- **Assinatura:** botão pílula com borda de 3 px e gradiente vertical; texto com leve relevo (`text-shadow`).
- **Movimento:** *snappy* com mola de pressão (stiffness 400, damping 10 só no clique). **Tipo:** sans humanista; serif display opcional.
- **Componentes de referência:** Texture Button/Card, Neumorph Button/Eyebrow, Organic Button/Card, Cutout Card, Folded Card. **Custa:** contraste de bordas sutis precisa de 3:1 nos componentes; não serve para tabelas densas.

### D3 · Ledger limpo
- **Parece com:** documentação e painel sóbrios, acromáticos, cartões sem borda flutuando em sombra suave. [cult-ui DESIGN.md "Clean Modern Ledger", site de docs]
- **Superfície:** neutros OKLCH (tinta `#171717`, tela `#FAFAFA`); cartões sem borda com `shadow-soft` (`0 0 0 1px rgb(0 0 0/.06), 0 1px 2px -1px rgb(0 0 0/.06), 0 2px 4px rgb(0 0 0/.04)`); folhas com `corner-shape: squircle` e `rounded-[1.5rem]`; `--radius: 0.625rem`.
- **Assinatura:** títulos Geist peso 450 com `tracking-[-0.06em]`; eyebrow mono de 10 px em caixa alta; uma fonte pixel de acento por seção, no máximo.
- **Movimento:** *sutil*; só transições nomeadas, nunca `transition-all`. **Componentes:** Code Block, Steps, Tabs, Timer, Data views, Browser Window.
- **Custa:** pouco; o risco é ficar genérico. Exija um acento (tipo, ilustração ou dado) que venha do produto.

### D4 · Detalhe obsessivo (craft minimal)
- **Parece com:** sites de Rauno Freiberg, Emil Kowalski, Vercel: interface quieta onde o movimento carrega a personalidade. [Skiper UI, coleções Rauno, Vercel, Minimal interactions]
- **Superfície:** papel quente `#f5f4f3` com quase-pretos `#080808` e `#121212`; bordas `#e0e0e0`; cor saturada só como acento raro; profundidade por desfoque, não por sombra.
- **Assinatura:** texto que rola por caractere (escalonamento de 35 ms, a partir do centro); sublinhado que cresce da origem; número animado (NumberFlow); desfoque progressivo (`backdrop-filter` + `mask-image`); troca de tema com View Transitions (revelação circular, 0,7 s, expo-out); legenda pequena em caixa alta com 40% de opacidade (checar contraste: costuma falhar).
- **Movimento:** *crisp* e *snappy*. **Tipo:** Geist, Plus Jakarta Sans ou Inter Display com tracking negativo (`-0.03em`).
- **Custa:** cada microinteração precisa de versão por teclado e de movimento reduzido; a Skiper não faz isso.

### D5 · Vidro Apple (web)
- **Parece com:** navegação de apple.com e do iOS: barras e menus de vidro, conteúdo sólido. [Skiper Apple Navbar e Feature Block; Mo baile]
- **Regra:** vidro só na camada de navegação, nunca em conteúdo, nunca vidro sobre vidro (mesma regra do Mo baile). Fallback sólido com reduzir transparência.
- **Assinatura:** squircle (filtro SVG ou `corner-shape`), borda Apple Intelligence (gradiente brilhante só em estado de IA), raios concêntricos.
- **Movimento:** *smooth* e *snappy* (as molas da Apple). **Tipo:** pilha do sistema (`-apple-system`).
- **Quando:** app web que convive com app Apple nativo. Em app macOS nativo, use o Mo baile.

### D6 · Editorial display
- **Parece com:** revista e campanha de moda: tipografia gigante condensada, imagem grande, rolagem que conta história. [Skiper Nike, Siena, Oliver parallax, Scroll Effects]
- **Assinatura:** display condensado (`text-[20vw]`, famílias tipo Bebas, Thunder, PP Mori) com tracking apertado; parallax em colunas; revelação de imagem por máscara e `clip-path`; pilha de cartões fixa na rolagem; caminho SVG que desenha com a rolagem.
- **Movimento:** *expressivo*, ligado à rolagem (`useScroll` + `useTransform`). **Custa:** nunca sequestre a rolagem nativa (Lenis global está fora); a versão sem animação precisa contar a mesma história.

### D7 · Estúdio escuro
- **Parece com:** Linear e Vercel no escuro: cinzas neutros em camadas, um único acento quente. [site do OriginKit]
- **Escala de superfícies:** fundo `#0F0F10`, cartão `#1B1C1D`, corpo `#222425`, elevado `#2D2D2F`, popover `#343434`, campo `#414143`, traço `#3E3F40`; texto `#F7F7F7`, secundário `#B7B7B8`, terciário `#7A7C7F`; acento laranja `#FA7319`; destrutivo `#E5484D`.
- **Assinatura:** linhas finas de 1 px em vez de sombras; raio de 10 a 13 px nos cartões; botão primário branco com texto preto; brilho que percorre o texto e skeleton com shimmer.
- **Movimento:** um token só: `--motion-duration: 220ms`, `--motion-ease: cubic-bezier(0.16, 1, 0.3, 1)`. **Tipo:** Inter ou Geist, tracking `-0.015em`.
- **Custa:** precisa de um tema claro desenhado à parte (a fonte não tem). Contraste calculado sobre `#0F0F10`: `#F7F7F7` e `#B7B7B8` 9,56:1, `#7A7C7F` 4,58:1 (passa por pouco; não use sobre `#2D2D2F` ou mais claro sem recalcular), acento `#FA7319` 6,87:1.

### D8 · Cinemático (showpiece WebGL)
- **Parece com:** sites premiados: shader no hero, objeto 3D que reage ao cursor. [OriginKit Background e Interactive; cult-ui Hero Dithering, Liquid Metal, Heatmap com Paper Shaders]
- **Regra de uso:** **um** momento por página, no hero ou numa seção de destaque; nunca em app (Operate).
- **Obrigatório:** pausar fora da tela (`IntersectionObserver`) e com a aba oculta; canvas sensível a `devicePixelRatio`; poster estático para movimento reduzido, dispositivo fraco e sem WebGL; título real em HTML (`srTitle`) por cima do efeito.
- **Custa:** peso (three.js, shaders), bateria, LCP. O OriginKit não pausa os loops; aqui é obrigatório.

### D9 · Generativo e textura digital
- **Parece com:** pixel, dither, halftone, ASCII e grão: estética de tela e impressão. [cult-ui Dither Image, Pixel Heading, Texture Overlay, Distorted Glass; OriginKit ASCII e Dither]
- **Assinatura:** fonte pixel (Geist Pixel) em títulos curtos; dither Bayer em imagem; ruído SVG (`feTurbulence`) como textura de fundo; grade de feixes.
- **Custa:** texto em fonte pixel só em display (nunca em corpo); textura sobre texto reduz contraste, então meça com a textura ligada.

### D10 · Lúdico e orgânico
- **Parece com:** interface com elasticidade: formas que se fundem (goo), botões que viram painel, ilhas que mudam de forma. [Skiper Gooey e Squircle; cult-ui Dynamic Island, Family Button, Organic Button]
- **Assinatura:** filtro goo (`feGaussianBlur` + `feColorMatrix`); `layoutId` compartilhado para morfar entre estados; molas com bounce de 0,2 a 0,35.
- **Movimento:** *bouncy*, só em manipulação direta e em transição de estado. **Custa:** gatilhos precisam ser `<button>` com `aria-expanded` (o cult-ui usa `div` no Family Button; aqui não).

## 4. Eixos independentes

Combine com qualquer direção.

| Eixo | Opções | Regra |
| --- | --- | --- |
| Aparência | claro · escuro · os dois · alto contraste | Aparência é sobrescrita de token, nunca componente separado (o OriginKit separa claro e escuro em seções diferentes; aqui não). |
| Intensidade de movimento | **sutil** (hover, foco, entrada de 150 a 220 ms) · **expressivo** (layout, escalonamento, ligado à rolagem) · **cinemático** (WebGL, preloader, cursor) | Tudo tem fallback de movimento reduzido. Cinemático só em Persuade e Experience. |
| Densidade | compacta (gaps de 14 a 18 px, controles de 28 a 32 px) · regular · ampla (editorial) | Alvo mínimo de 24 px CSS sempre; 44 px no toque. |

## 5. Presets de movimento

Declare como tokens (`tokens/motion.css`) e constantes compartilhadas (regra C-11). Todos vão a duração 0 ou crossfade com movimento reduzido.

| Preset | Valor | Uso | Fonte |
| --- | --- | --- | --- |
| `crisp` | tween 0,3 s, `easeInOut` | fades e trocas simples | Skiper (mais frequente) |
| `ui-micro` | 220 ms, `cubic-bezier(0.16, 1, 0.3, 1)` | hover, press, microinteração | OriginKit |
| `snappy-layout` | spring `bounce 0.12, damping 34, stiffness 420` | pílulas, segmentados, indicadores com `layoutId` | cult-ui Halo |
| `snappy` | spring `stiffness 400, damping 30` | ilhas, expansões | cult-ui, Skiper |
| `soft-tabs` | spring `bounce 0.2, duration 0.4` | abas com direção | cult-ui |
| `bouncy` | spring `bounce 0.35` | manipulação direta, lúdico (D10) | Skiper |
| `caret` | spring `stiffness 500, damping 30, mass 0.5` | cursor de texto, seguidores | Skiper |
| `ease-out-quint` | `cubic-bezier(0.23, 1, 0.32, 1)` | saídas e entradas em CSS | cult-ui (13 usos) |
| `ease-out-expo` | `cubic-bezier(0.19, 1, 0.22, 1)` | revelações, troca de tema | Skiper |
| `stagger-char` | 18 ms (rótulo) a 35 ms (título), opcional a partir do centro: `delay = s * abs(i - (n-1)/2)` | texto | cult-ui, Skiper |

## 6. Técnicas assinatura

| Técnica | Direções | Regra de acessibilidade e desempenho |
| --- | --- | --- |
| Desfoque progressivo (`backdrop-filter` + `mask-image`) | D4, D5 | Fallback sólido com reduzir transparência |
| Vidro fosco com `color-mix` | D1, D5 | Texto sobre vidro medido no pior fundo possível |
| Aro em gradiente animado | D1 | Para com movimento reduzido; não é o único sinal de foco |
| Bordas aninhadas concêntricas | D2 | Interno = externo − padding; contraste 3:1 da borda externa |
| Texto que rola por caractere | D4, D6 | `aria-label` com o texto inteiro; caracteres `aria-hidden` |
| Número animado | D4, D3 | `tabular-nums`; o valor final é anunciado uma vez |
| View Transitions na troca de tema | D4 | Detecte suporte; sem suporte ou com movimento reduzido, troca direta |
| Revelação por `clip-path` e máscara | D6 | Conteúdo existe no DOM antes da animação |
| Filtro goo e squircle em SVG | D10, D5 | Decorativo, `aria-hidden` |
| Shader e WebGL | D8, D9 | Pausa fora da tela, poster, `srTitle` |
| Revelar no hover | D4, D6 | Mesmo conteúdo com `:focus-visible` e toque; hover só com `(hover:hover) and (pointer:fine)` |

## 7. Como uma direção vira código

- **Tokens primeiro:** a direção escolhida gera primitivos (cores, raio, sombra, movimento) e semânticos (`--card`, `--border`, `--ring`, `--accent`) no padrão de [design-tokens](design-tokens.md). Componente nunca recebe hex.
- **Direção por atributo:** `[data-direction="halo"]` sobrescreve tokens, como as aparências do Mo baile. Trocar de direção não exige mudar componente.
- **Looks nomeados por componente** (ideia do OriginKit): quando um componente tem variações de estilo (não de função), declare `look` como variante cva fechada (`look: "halo" | "texture" | "ledger"`), documentada na tabela de API.
- **Esquema de controles** (ideia do OriginKit `tweakSchema`, opcional): para componentes de efeito, um objeto tipado de parâmetros (número com min, max e passo; enum; cor; transição) que alimenta a tabela de API, o playground e a validação. Ajuste por IA mexe só nesses valores, não reescreve código.
- **Etiqueta de direção e aparência em cada item** (ideia da Skiper `theme`): o catálogo do sistema filtra por direção (Claro, Escuro, Colorido, Mínimo, Gradiente, Futurista, Enterprise, como os filtros do OriginKit).
- **Doc:** a página do componente segue [doc-componente](../assets/templates/doc-componente.md) e diz em Features a qual direção ele pertence.

## 8. Licenças e o que nunca copiar

| Fonte | Licença | Pode | Não pode |
| --- | --- | --- | --- |
| cult-ui | MIT | Instalar pelo registro (`@cult-ui/<nome>`), adaptar código com atribuição no `THIRD_PARTY_NOTICES` | Remover o aviso de copyright |
| Skiper UI | Free com **atribuição obrigatória**; Pro pago ($129 único) | Usar componente free com crédito à Skiper UI; usar ideias e valores de movimento | Copiar código Pro sem licença; muitos componentes são recriações de sites de terceiros (Nike, Apple, Vercel): não reproduza marca ou layout identificável |
| OriginKit | Proprietária (só a CLI é MIT) | Usar em projeto do usuário dentro do plano; usar como inspiração de taxonomia e processo | **Colocar código do OriginKit em design system, UI kit, template ou biblioteca** (proibido pela licença); espelhar o catálogo via MCP |

Instalar, copiar ou criar conta em qualquer uma é decisão do usuário (fronteira de ações). Este plugin só cita nomes e valores observados.

Falhas observadas nas fontes que não entram aqui: cores cruas dentro de componentes (Skiper, OriginKit, cult-ui geração 1); rolagem sequestrada (Lenis global); interação só no hover; loops de rAF sem pausa; manifesto de dependências incompleto; CSS necessário fora do registro.

## 9. Filtro aplicado: o que entrou e o que ficou de fora

- **Entrou:** convenções de componente e de doc do cult-ui (arquivo próprio); estéticas recorrentes nas três fontes viraram D1 a D10; valores de movimento repetidos em mais de uma fonte; ideias de processo (looks nomeados, esquema de controles, filtros por direção, demo e doc pareados).
- **Ficou de fora:** catálogo integral de efeitos (593 no OriginKit, 107 na Skiper): é inventário, não decisão; os nomes de componente aparecem só como referência por direção. Preços e limites de plano (mudam). Jogos, preloaders e componentes de marca de terceiros (Web3 Uniswap, Nike).
- **Não verificado:** renderização em navegador de cada direção; contraste dos valores das fontes (exceto os cálculos citados em D7 e o `#4f4f4e` sobre `#f5f4f3` da D4, 7,47:1); desempenho real dos efeitos WebGL. Reconfira as fontes a cada 6 meses.
