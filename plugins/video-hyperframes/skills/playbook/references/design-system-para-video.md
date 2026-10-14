# Design system para vídeo: `frame.md`, tokens, tipografia e pisos de legibilidade

Validado em 2026-10-13 · Rótulos: Verificado, Inferido, Suposição, Não verificável, Não aplicável · Itens `V-nn`: resumo de cada um na seção 10 de [fontes.md](fontes.md) (leitura de arquivo no commit validado; o dogfood de 2026-10-14 renderizou um vídeo silencioso e corrigiu a tipografia: itens `DF-nn`, seção 12 de [fontes.md](fontes.md)) · Redação própria · Exemplos usam `[HEX_*]`, `<pasta>` e `<usuario>`: o plugin **não embute** o design system de ninguém (V-71) · Versões: [toolchain-windows.md](toolchain-windows.md).

## Sumário

1. Arquivos e precedência
2. A pergunta de design em 3 estados
3. Presets e o remix do `build-frame.mjs`
4. `tokens.json`
5. Marca estrita, escala livre
6. Tipografia: embutidas, lista "banida" e guardrails
7. Pisos de legibilidade por destino
8. Fundo, gradiente, unidades e área útil
9. Seção `## Regras do vídeo`
10. Checagem: `frame.md` final = tokens
11. Método: converter o design system de um usuário
12. Gotchas

## 1. Arquivos e precedência (V-66, Verificado)

- `frame.md` é frontmatter YAML **normativo** (cores, tipo, espaçamento, componentes; cite valores exatos) mais prosa de contexto. Precedência: `frame.md` → `design.md` → `DESIGN.md`; vale o primeiro que existir. O nome de trabalho é sempre minúsculo: o preset entrega `FRAME.md` como modelo que vira `frame.md`.
- O `DESIGN.md` da raiz do repositório do HyperFrames é o design do site de docs, não um `frame.md` de vídeo (por citação do pesquisador; não relido).
- Um `DESIGN.md` do usuário, de produto, é **entrada**, não saída: traduza-o para `tokens.json` e `frame.md`. Criar ou auditar design system de produto é do plugin `ux-ui-design` (`/ux-ui-design:playbook`).
- Quando o `frame.md` muda, reexecute os passos que geram composições.

## 2. A pergunta de design em 3 estados (V-40, Verificado)

| Estado | Ação |
| --- | --- |
| (1) **Já tem guia** (`frame.md`, `design.md`, `DESIGN.md`) | nota no `BRIEF.md` § Assets; o guia vira verdade |
| (2) **Não tem, mas importa** | escolha 2 a 3 presets e abra cada `frame-presets/<nome>/frame-showcase.html` no navegador para o usuário escolher **por olho**; o resultado vira `style_preset` por workflow |
| (3) **Não se importa** | o workflow decide e diz por quê |
| (4) Nada serve | "design picker" como pergunta adiada |

A oferta de capacidades é de no máximo 1 a 2 linhas rastreadas ao conceito, nunca o catálogo inteiro. No faceless, cores e fontes da marca só entram se o usuário as der: vão para `capture\extracted\tokens.json` e o `build-frame.mjs` remixa o preset; sem elas, o preset mantém a paleta dele. (A afirmação do núcleo de que o remix "só vale com captura de site" não foi reconferida.)

## 3. Presets e o remix do `build-frame.mjs` (V-66, V-41)

13 presets em `skills/hyperframes-creative/frame-presets/`: `biennale-yellow`, `blockframe`, `blue-professional`, `bold-poster`, `broadside`, `capsule`, `cartesian`, `code-editorial`, `cobalt-grid`, `coral`, `creative-mode`, `daisy-days`, `editorial-forest`. Cada um traz `FRAME.md`, `caption-skin.html` e `frame-showcase.html` (só um dos 13 foi lido por inteiro; os demais: Não verificado).

Comando (pelo invólucro): `hfn "<SKILL_DIR>\scripts\build-frame.mjs" --preset "<nome>" --hyperframes .` (gera `frame.md` e `.hyperframes\caption-skin.html`).

O que o remix faz e não faz (Inferido por análise estática do caso real; **polaridade escura não testada por execução**): remapeia fundo, tinta e acentos e troca as famílias; parte de presets claros e pode **inverter a polaridade**; painel, texto secundário, cores semânticas e terminal não vêm do remix. Portanto: leia a linha de resumo que o script imprime, abra o `frame.md` e force à mão, nas chaves de `colors:`, os valores do guia; confirme as famílias. Presets podem impor `text-transform` (`upper`, `lower`), barras de topo e rodapé e numeração de slide: para nomes de arquivo, comandos e siglas, desligue o `text-transform` e remova as barras.

Evite copiar bokeh ou gradiente roxo-azul de preset; "forçar tema sobre preset" por texto livre é antipadrão: use o caminho suportado (`tokens.json` e remix).

## 4. `tokens.json` (V-41 passo 1, Verificado)

Esquema: `{ "title": "", "description": "", "colors": [], "fonts": [] }`, em `capture\extracted\tokens.json`. `colors` em hex na ordem que o remix espera (fundo, tinta, acentos; confira o resumo impresso). `fonts` com família e pesos. O caso real omitiu um campo `colorStats`, o que sugere que ele é opcional (Inferido). Não rode `capture` para obter tokens: preencha à mão a partir do guia do usuário.

## 5. Marca estrita, escala livre (V-66, Verificado)

**Estrito:** hex, famílias, pesos, fundo (claro continua claro). **Livre:** tamanhos e bordas, adaptados ao vídeo. Tabela web → vídeo:

| Elemento | Web | Vídeo |
| --- | --- | --- |
| Títulos | 32 a 48 px | 64 a 120 px |
| Corpo | 14 a 16 px | 28 a 42 px |
| Rótulos | 12 px | 18 a 24 px |
| Opacidade decorativa | 3 a 8% | 12 a 25% |
| Bordas | 1 px | 2 a 4 px |
| Padding | 16 a 32 px | 60 a 140 px |

Texto abaixo de 24 px exige justificativa (piso do destino, seção 7). Faixas típicas, não regras: calibre com `snapshot`.

## 6. Tipografia (V-67, V-19, DF-01, DF-02, Verificado)

- O compilador reconhece **18 famílias** sem aviso `font_family_without_font_face`, só nos pesos listados (League Gothic e Archivo Black: só 400). **Correção do dogfood (Verificado, 2026-10-14, DF-01):** nesta versão do CLI elas **não são bundle local**; no `check`, no `snapshot` e no `render` o compilador baixa as faces do Google Fonts (11 de Montserrat e 10 de JetBrains Mono no caso real) e grava cache fora do projeto, em `~\.cache\hyperframes\fonts\`. Logo "embutida" aqui só quer dizer "sem aviso", não "offline"; o render precisa de rede (ao lado do GSAP no jsdelivr). Para render 100% offline: rodar uma vez online para popular o cache (Inferido) ou embutir `@font-face` local (Não verificado). As 18: Inter, Roboto, Open Sans, Lato, Nunito, Montserrat, Poppins, Outfit, Oswald, League Gothic, Archivo Black, Playfair Display, EB Garamond, Space Mono, IBM Plex Mono, JetBrains Mono, Source Code Pro, Noto Sans JP.
- Apelidos resolvem para embutidas: Helvetica e Arial → Inter; Futura e Arial Black → Montserrat; Bebas Neue → League Gothic; Garamond → EB Garamond; Courier New → JetBrains Mono.
- Fora das 18: Google Fonts em tempo de build também (aviso `font_family_without_font_face`, "fail-closed" em render distribuído) ou fonte instalada localmente (capturada em render local). Fonte proprietária do sistema (por exemplo SF Pro) **não vai no render**: troque por família embutida.
- **Lista "banida"** do upstream (default de LLM a evitar, não proibição técnica): Inter, Roboto, Open Sans, Noto Sans, Arimo, Lato, Source Sans, PT Sans, Nunito, Poppins, Outfit, Sora, Playfair Display, Cormorant Garamond, Bodoni Moda, EB Garamond, Cinzel, Prata, Syne. Presets a usam (blockframe e code-editorial usam Inter; code-editorial usa EB Garamond): conflito resolvido como "evitar quando há escolha, não bloquear". Famílias **embutidas e não banidas**: Montserrat, Oswald, League Gothic, Archivo Black, Space Mono, IBM Plex Mono, JetBrains Mono, Source Code Pro, Noto Sans JP (C6).
- **Ligaduras (Verificado, DF-02):** JetBrains Mono funde `-<` numa ligadura (`AAAA-MM-DD-<tema>` apareceu como `DD-≺tema>`). Em todo texto mono com placeholders ou código, `font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0;` em `#root` e nos descendentes.
- Guardrails: não pareie duas sans (serif com sans, ou sans com mono); uma família expressiva por cena; contraste de peso extremo (o texto diz 300 e 900, mas as embutidas trazem 400, 700 e 900: use 400 e 900 onde existir; Inferido); texto de 3 s na tela deve ser legível em 2 s.
- **PT-BR (Inferido):** Montserrat mais JetBrains Mono atendem "embutida e não banida". Cobertura dos acentos nas embutidas: **Não verificável** sem `snapshot`; renderize um quadro de teste com acentos antes do storyboard final (L10).

## 7. Pisos de legibilidade por destino (V-67, "primeira passada; calibre com render real")

| Destino | Corpo | Títulos | Rótulos |
| --- | --- | --- | --- |
| Tela cheia (YouTube, embed, site) | 20 px ou mais | 60 px ou mais | 16 px ou mais |
| Feed (X, LinkedIn, Instagram) | 32 px ou mais | 90 px ou mais | 24 px ou mais |

Vídeo que vai a mais de um destino segue o piso mais restritivo (decisão do dono, registrada no `BRIEF.md`). Estimativas visuais de tamanho por imagem são relativas à altura do canvas e rotuladas como estimativa.

## 8. Fundo, gradiente, unidades e área útil (V-66, V-45, V-41)

- **Fundo claro:** bordas de 2 px ou mais e acento saturado. **Sem gradiente linear de tela cheia em fundo escuro**: faixas sob H.264; degradê leve e curto é decisão consciente, a conferir no `snapshot`.
- Unidades `cqw` com `container-type: size`, nunca `vw` (regra do preset `code-editorial`, `FRAME.md:135-137`).
- **Área útil:** todo conteúdo acima de cerca de 83% da altura; a faixa inferior de 17% é reservada às legendas **mesmo desativadas** (`frame-worker-core.md:50`, V-45). Em 1080p, fica abaixo de y ≈ 896 px.
- Um acento por quadro; cores semânticas só onde há significado e em áreas pequenas; no máximo duas cores base (fundo e tinta), com ênfase por inversão, escala ou densidade.
- Fundo de tela cheia em camada `class="clip"`, não no `#root` (V-41, V-53).

## 9. Seção `## Regras do vídeo` (achado do caso real, REVISAO-PROMPT C09/C10)

Os workers de quadro leem **só o pacote do quadro e o `frame.md`**, nunca o `STORYBOARD.md`; logo o `## Video direction` não chega a eles (V-41, V-45). Grave no **fim do `frame.md`**:

```markdown
## Regras do vídeo
- Destino: [tela cheia | feed]. Pisos: corpo [20 | 32] px, títulos [60 | 90] px ou mais, rótulos [16 | 24] px.
- Acento único: [HEX_ACENTO], no máximo um destaque por quadro. Semânticas só onde há significado: [HEX_VALIDADO], [HEX_ATENCAO], [HEX_BLOQUEADO].
- Tom do texto: PT-BR direto, frases curtas, sem emoji nem exclamação. Nomes de arquivo, comandos e siglas como escritos (sem text-transform), em fonte mono, com `font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0;` em `#root` e descendentes (a mono funde `-<`).
- Código dos quadros: ids e classes prefixados pelo `frame_id` só em seletores de atributo (`[id="..."]`, `[class~="..."]`) ou `CSS.escape`/`getElementById`, nunca `#01-...`; todo elemento com `data-start` tem `id`; posição por classes. GSAP: [URL única do `index.html` do `init`, por exemplo `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js`].
- Movimento: entradas power3.out (cerca de 0,5 s); selos, chips e contadores power4.out (cerca de 0,35 s); sem back.out, elastic ou bounce; nada entra todo de uma vez.
- Área útil: todo conteúdo acima de ~83% da altura (faixa inferior reservada às legendas, mesmo desativadas).
- Negativos: [lista do BRIEF: sem bokeh, sem gradiente roxo-azul, sem chrome de navegador, sem cursor real].
- Fio persistente: [descrição]; posição de entrada e saída em cada quadro, no bloco do quadro.
```

As curvas e tempos são exemplos do caso real (Inferido; `power3` como padrão é Verificado em V-57): ajuste ao projeto.

**Precedência quando o `_role.md` oficial do worker discorda (Verificado, dogfood 2026-10-14, DF-09):** o `_role.md` pede "herói visível até 0,5 s" e um `@font-face` por fonte, o que conflita com storyboards de revelação progressiva e com fontes do conjunto "embutido". No caso real prevaleceu o `frame.md` (`## Regras do vídeo`) e o `check` passou com 0 erros. Registre a decisão no `frame.md` e no `DECISOES.md`, e repita no despacho de cada worker que o `frame.md` vence o `_role.md` nesses dois pontos. As linhas de `Scene` dos quadros só **nomeiam** o movimento; curvas e milissegundos ficam aqui e no `## Video direction`.

## 10. Checagem: `frame.md` final = tokens

Depois do remix, e a cada mudança, preencha:

| Token | Valor do usuário | Valor no `frame.md` | Igual? |
| --- | --- | --- | --- |
| fundo | `[HEX_FUNDO]` | ... | sim ou não |
| tinta | `[HEX_TINTA]` | ... | |
| acento | `[HEX_ACENTO]` | ... | |
| semânticas | `[HEX_*]` | ... | |
| família de título e peso | `[FAMILIA]` `[PESO]` | ... | |
| família técnica e peso | `[FAMILIA_MONO]` `[PESO]` | ... | |

Qualquer "não": sobrescreva à mão e confira de novo. Liste as fontes com origem (embutida, instalada, Google). O `check` valida contraste WCAG AA como **erro** (V-47): 4,5:1 para texto normal e 3:1 para texto grande (conhecimento estável). Texto pequeno sobre acento claro é o risco clássico: calcule a razão do par antes de fixá-lo. Preenchimento de acento com texto branco por cima também deve passar.

## 11. Método: converter o design system de um usuário (sem embutir nenhum)

O caso real (V-71) mostrou o método; os valores do dono **não** entram aqui. Para qualquer sistema de produto:

| Elemento do sistema | Decisão para vídeo | Motivo |
| --- | --- | --- |
| Tinta e fundo escuro | tinta sólida `[HEX_TINTA]` no fundo `[HEX_FUNDO]`; degradê vertical leve só se necessário | marca estrita; evitar faixas |
| Fundo claro de produto | manter claro; bordas de 2 px ou mais e acento saturado | polaridade é da marca |
| Acento | **um** `[HEX_ACENTO]` por quadro | uma ideia, um destaque |
| Verde, âmbar, vermelho semânticos | só como confirmação, atenção e bloqueio, em áreas pequenas | cor com significado |
| Fonte proprietária do sistema | trocar por embutida (Montserrat; JetBrains Mono ou IBM Plex Mono) | fonte do sistema não vai no render |
| Molas e bounce da UI | `power3.out` sem bounce | doutrina do faceless (V-57) |
| Componentes React e UI do app | não usar; redesenhar em SVG/CSS | contrato de composição |
| Mascote, ícone, logo | só com autorização do dono por item | privacidade e marca |
| Tamanhos e bordas web | escala da seção 5 | legibilidade em vídeo |

Contraste do acento em texto pequeno: o `check` mediu 72 de 72 pares no caso real, mas amostra só cerca de 5 instantes por quadro (Verificado, DF-11); confirme no `snapshot`. Acentuação PT-BR nas fontes: Não verificável até o `snapshot` (L10).

## 12. Gotchas

- O preset impõe polaridade e fonte: leia o resumo do `build-frame.mjs` e confira o `frame.md`.
- `Scene` com curva ou milissegundos contraria `motion-language.md`: valores vão no `frame.md` e no `## Video direction`.
- Regras globais fora do `frame.md` não chegam ao worker.
- SF Pro e outras fontes proprietárias renderizam como fallback: o vídeo "funciona" e fica errado.
- Quadros com mais de uma fonte expressiva ou dois acentos pedem corte, não decoração.
