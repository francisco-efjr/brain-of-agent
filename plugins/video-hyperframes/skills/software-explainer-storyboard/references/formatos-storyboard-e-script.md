# Formatos de `STORYBOARD.md` e `SCRIPT.md`, direção do vídeo e exemplo mínimo

Base: HyperFrames (HeyGen, Apache-2.0), commit `bf4cf860fbd26a7d51938c5f11987c335d4e848a`: `storyboard-format.md`, `script-format.md`, `story-design.md`, `storyboards.mdx`, `visual-design.md` (V-43, V-44, V-56, V-62), destilado com redação própria. Se a sessão tiver as skills oficiais, confira os nomes de chave no `storyboard-format.md` de lá (chaves desconhecidas são preservadas, mas a forma exata dos valores de `format` e `sfx` não foi verificada aqui).

Sumário: 1 STORYBOARD.md · 2 Direção do vídeo · 3 SCRIPT.md · 4 Exemplo mínimo · 5 Regras de uso.

## 1. `STORYBOARD.md`

**Frontmatter:** `format` (por exemplo `1920x1080`), `duration` (expectativa, não gate), `message` (uma frase), `arc` (a estrutura escolhida), `audience`, `mode` (derivado de `flow` e `storyboard`, V-39), e `music: none` quando não há música. O `mode` é gravado depois que o plano existe e vence na retomada.

**Cada quadro:** `## Frame N — título` seguido de linhas `- chave: valor`.

| Chave | Uso |
| --- | --- |
| `status` | `outline` (plano) -> `built` (layout confirmado, sem movimento) -> `animated` (movimento feito). O pipeline exige todos `animated` antes do índice |
| `scene` | O palco e a ação do quadro; é a chave mais longa. Escreva aqui a **posição de entrada e de saída do fio** (a entrada é igual à saída do quadro anterior) |
| `voiceover` | Guia editável da fala; multilinha colapsa. Vazio no vídeo silencioso |
| `duration`, `transition_in`, `poster`, `src` | Duração do quadro, transição de entrada, imagem de pôster e caminho do HTML (preenchido na construção) |
| `type` | Papel do quadro: `hook`, `pain_point`, `product_intro` (a ideia), `feature_showcase` (unidade do corpo), `benefit_highlight`, `social_proof` (evidência), `branding` (tese ou lição), `cta` |
| `blueprint`, `focal`, `roles` | Forma de tomada; elementos inventados do quadro (palavra herói, nós do diagrama, série do gráfico) |
| `sfx` | Nome(s) da biblioteca embutida (`manifest.json`), disparados no início do quadro; só no regime com SFX. Disparo no meio do quadro exige editar o `audio_meta.json` à mão depois do `fetch-sfx` (`"source":"host"`, volume 0.35; **Verificado, dogfood 2026-10-14, DF-05**: 15 cues resolvidos pela biblioteca local, 31 disparos, 31 `<audio>` montados pelo `assemble-index`) |

Mapeamento de papel para `type` no faceless: gancho = `hook`; a ideia nomeada = `product_intro`; um mecanismo, passo ou camada por quadro = `feature_showcase`; prova, exemplo ou número = `social_proof`; tese ou lição = `branding`.

## 2. Bloco `## Video direction` (uma vez, no corpo do `STORYBOARD.md`)

Escreva a direção **uma vez**, não por quadro. Conteúdo mínimo:

1. Paleta: fundo + uma tinta; ênfase por inversão, escala ou densidade, nunca por terceira cor.
2. Gramática de motion e modelo de reveal: ease suave `power3` como padrão (as durações de cerca de 0,5 s para entradas e 0,35 s para selos e contadores, com `power4.out`, vêm do caso de referência do dono, Inferido: ajuste ao vídeo), sem `back.out`, `elastic` nem `bounce`; em t=0 entra só o âncora; cada peça seguinte entra no cue, espalhada pela segunda metade do quadro.
3. Quadro parado: 100% estático ou jitter sutil de baixa amplitude; **nunca** respiração nem drift lento (doutrina da rota faceless, V-57).
4. Um único respiro no filme.
5. Lista negativa com os dois modos de falha: **slideshow** (tudo entra no começo e congela) e **screensaver** (tudo flutua sem motivo). Acrescente: sem gradiente roxo-azul, sem bokeh, sem chrome de navegador, sem cursor real, sem loops infinitos nem aleatoriedade.

O `## Video direction` **não chega aos workers**: eles leem só o pacote do quadro e o `frame.md`. As regras que importam vão também para a seção `## Regras do vídeo` do `frame.md` (skill `video-design-system`).

## 3. `SCRIPT.md` (opcional; só com narração)

Markdown livre, sem parser estrito. Cabeçalho: `**Voice:**`, `**Voice settings:**`, `**Voice direction:**`. Uma seção por fala: `## Line N — rótulo (Frame N)`, com `**Time:**` (guia) e `**Delivery:**` (direção), e a fala num **bloco recuado em 4 espaços**: **somente o bloco recuado vai ao TTS**. Quadros sem fala ficam fora do arquivo (silêncio é permitido). Regras de escrita: 1 a 2 frases e 6 a 20 palavras por quadro falado; um cue por ideia, para o reveal acompanhar a fala; números e siglas escritos como se fala.

## 4. Exemplo mínimo (sistema fictício de filas de pedidos, 4 quadros, vídeo silencioso)

```markdown
---
format: 1920x1080
duration: 60
message: "O roteador por prioridade faz o pedido urgente furar a fila sem perder os outros"
arc: concept-explainer com processo
audience: desenvolvedores de backend que operam filas
mode: collaborative
music: none
---
## Video direction
Fundo [HEX_FUNDO] e tinta [HEX_TINTA]; um acento [HEX_ACENTO] só no fio. Entradas power3.out (~0,5 s), reveals na segunda metade de cada quadro, em t=0 só o âncora. Quadro parado estático; um respiro no F03. Transição primária: push-slide de 0,4 s. Negativos: slideshow, screensaver, bokeh, gradiente roxo-azul, chrome de navegador, loops infinitos.

## Frame 1 — Gancho
- status: outline
- duration: 8
- type: hook
- scene: palco de 3 colunas vazio; âncora: pedido chega pela esquerda como ponto do acento (fio nasce aqui, entrada x=0, saída x=33%). Texto: "Por que o pedido urgente não espera?"

## Frame 2 — O roteador
- status: outline
- duration: 16
- type: product_intro
- scene: mesmo palco; coluna 1 acende ao ser nomeada ("Roteador"); o fio entra em x=33% (igual à saída do F1) e sai em x=66%. Três níveis de prioridade surgem em ordem (F-001).

## Frame 3 — Os workers
- status: outline
- duration: 18
- type: feature_showcase
- scene: coluna 2 acende; fio entra em x=66%, atravessa os workers e sai em x=100%. Respiro: 2 s sem peça nova no meio.

## Frame 4 — Limites honestos
- status: outline
- duration: 18
- type: branding
- scene: palco recua; frase de lembrança em [tinta]; fio fecha em linha de base. Slot "— figure —" no lugar do ganho de latência, até haver fonte.
```

Exemplo de `SCRIPT.md` para o quadro 2, só se houvesse voz:

```markdown
**Voice:** [ID_p]
**Voice direction:** claro, ritmo calmo

## Line 1 — Roteador (Frame 2)
**Time:** ~12 s

    O roteador lê a prioridade do pedido e decide em qual das três filas ele entra.
```

## 5. Regras de uso

- `duration` do frontmatter é expectativa; a soma dos quadros deve ficar perto dela, e no vídeo com voz a duração real da voz vence (`sync-durations`; não edite durações sincronizadas à mão).
- Corpo de 3 a 6 quadros mais gancho e fecho; acima de 8, aplique o orçamento de leitura e chame o `storyboard-reviewer`.
- Cada quadro nomeia sua técnica (Make-concrete, Reveal-in-order, Contrast, Structure, Evidence, Memory & landing) e a estrutura registrada em `arc` vale para o filme todo: `concept-explainer`, `how-to-process`, `listicle` ou `story-explainer`.
- Depois de gerar os pacotes dos quadros, confira por `Grep` que a posição de entrada e de saída do fio chegou em cada pacote (`.hyperframes\frame-packets\<id>.md`): se o pacote não carrega a chave, mova o texto para a chave `scene` ou para o `frame.md`.
