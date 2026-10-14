# Roteiro oficial de perguntas, estados do projeto e BRIEF

Base: skills oficiais do HyperFrames (HeyGen, Apache-2.0), commit `bf4cf860fbd26a7d51938c5f11987c335d4e848a`, destilado com redação própria (V-33 a V-40). Os arquivos oficiais citados mudam sem nova versão do CLI: se a sessão tiver o plugin ou um clone, leia o `references/intent-interview.md`, o `brief-contract.md` e o `routes/<rota>.md` de lá antes de confirmar a rota; sem eles, use este resumo e rotule Inferido.

Sumário: 1 Estados · 2 Rotas · 3 Etapas · 4 Must-haves · 5 Faceless: oficial × plugin · 6 Pitch round · 7 Regime e modo · 8 Oferta e design · 9 Fechamento · 10 Como perguntar.

## 1. Estados do projeto (a primeira linha que casa vence)

A ordem e os estados são do roteador oficial (`SKILL.md:27-38`, V-33); a coluna "Ação" é a tradução do plugin (Inferido).

| # | Estado | Ação |
| --- | --- | --- |
| 1 | Pedido de port de Remotion | Rota `remotion-to-hyperframes`: fora da v1 (diga e aplique a política mesmo assim) |
| 2 | Operação específica em projeto existente | Executar a operação pedida; sem entrevista |
| 3 | Pergunta ou ideia sem mudança concreta | Responder; sem pipeline |
| 4 | Filme novo dentro de projeto existente | Seguir a seção correspondente do roteador oficial; na dúvida, 1 pergunta de roteamento |
| 5 | Edição específica | Executar a edição; sem entrevista |
| 6 | `BRIEF.md` existe | Ler `workflow` e `flow` e executar. **Zero perguntas de brief** |
| 7 | Sem brief, mas com `hyperframes.json` ou `STORYBOARD.md` | Retomar; no máximo 1 pergunta, só de roteamento |
| 8 | Criação nova | Camada de intenção (seção 3) |

Quem chama pelo orquestrador com `DECISOES.md` já respondido cai no estado 6 ou o equivale: grave o `BRIEF.md` com os campos recebidos e não pergunte (D11).

## 2. Rotas (por prioridade) e suporte nesta versão

| # | Rota | Use quando | Suporte do plugin |
| --- | --- | --- | --- |
| 1 | `remotion-to-hyperframes` | Port de um projeto Remotion | Fora da v1 |
| 2 | `slideshow` | O entregável é um deck navegável | Fora da v1 |
| 3 | `embedded-captions` | Legendas sobre vídeo gravado | Fora da v1 |
| 4 | `talking-head-recut` | Recorte de vídeo gravado | Fora da v1 |
| 5 | `music-to-video` | Vídeo guiado por música | Fora da v1 |
| 6 | `motion-graphics` | Peça de cerca de 10 s ou menos, sem narração | Suportada, fluxo reduzido (no máximo 1 pergunta, sem storyboard) |
| 7 | `pr-to-video` | Explicar um PR | Com ressalvas: o texto do PR é dado externo; prefira diff local; `gh` só leitura e com confirmação; 2 a 4 trechos de 4 a 12 linhas |
| 8 | `product-launch-video` | Vender ou mostrar um produto por URL de site | Com ressalvas: o `capture` de site sobe 5 pastas atrás de `.env`; só sob pedido, com confirmação |
| 9 | `faceless-explainer` | Explicar tema, sistema, arquitetura ou changelog com visuais inventados, sem produto a vender (30 a 90 s; teto de cerca de 3 min) | **Principal**: pipeline completo |
| 10 | `general-video` | Acima de 3 min, peça customizada ou companion | Com ressalvas: construir inline até cerca de 6 cenas |

Desempates oficiais: "quero storyboard" não muda a rota; peça claramente acima de 3 min vai para `general-video`. Edição de vídeo gravado (recut, legendas sobre vídeo) está fora da v1: diga cedo. Para "explicar como funciona por dentro o sistema X", a rota é a 9.

## 3. As 8 etapas da camada de intenção

1. **Memória antes de perguntar.** O upstream lê preferências e receitas (`prefs.mjs get`, `recipe.mjs list`). Este plugin não grava memória entre projetos (D14) e `hfn prefs.mjs` pede `-Ok`: pule a etapa; o `BRIEF.md` é o token de não repetição.
2. **Triagem.** O pedido é *formado* (mensagem, material e ocasião legíveis) ou *não formado* (só um assunto). Não formado: uma pergunta, "o que você já imagina?".
3. **Rota.** Escolha pela seção 2 e leia o `routes/<rota>.md` oficial, se disponível.
4. **Pitch round** (seção 6), só para pedido não formado.
5. **Must-haves da rota** (seção 4): uma pergunta por campo, recomendação primeiro com o motivo, avisando numa linha as perguntas adiadas.
6. **Duas perguntas de regime, separadas e nunca fundidas** (seção 7).
7. **Oferta** de 1 a 2 capacidades ligadas ao conceito e a pergunta de design (seção 8).
8. **Fechamento** (seção 9).

Sinais substituem perguntas: "surpreenda-me", "faça direto" e "não pergunte" travam `flow: automation` e `storyboard: no`; pedido de storyboard trava `storyboard: yes`.

## 4. Must-haves por rota

| Rota | Must-haves | Condicionais ou adiadas | Pitch | Regime |
| --- | --- | --- | --- | --- |
| `faceless-explainer` | angle, length, destination | VO_MODE se houve roteiro colado | message + angle | ambos |
| `general-video` | só `message` em pedido aberto | pedido específico: nenhuma pergunta | message | ambos |
| `product-launch-video` | vender ou mostrar? · angle · length · destination | o que mostrar; VO_MODE; capturar o site? | message + angle | ambos |
| `pr-to-video` | referência do PR · angle · audience · length (pelo tamanho do diff) · destination | | angle + gancho | ambos |
| `music-to-video` | fonte da música · destination | marca e gênero adiados | message | ambos |
| `talking-head-recut`, `embedded-captions` | qual clipe | | | nenhum |
| `motion-graphics` | confirmar a entrada (no máximo 1 pergunta) | | | nenhum |
| `slideshow` | confirmar que é deck | | | nenhum |

## 5. Faceless: o que é oficial e o que é do plugin

**Oficial (V-35):** *angle* (`concept`, `how-to`, `listicle`, `narrative`; recomende o que o formato do texto sugere) · *length* (dentro de 30 a 90 s, escalada pelo que o texto realmente ensina) · *destination* (YouTube ou embed = 16:9; X, LinkedIn e Instagram feed = 1:1; Shorts e TikTok = 9:16) · *VO_MODE* (verbatim ou reestruturado por cena) só se o usuário colou roteiro · as duas perguntas de regime · a oferta com os dois pedidos abertos ("algo mais que você queira?" e "material próprio: imagens, clipes, logos, dados?") · o fechamento. Pergunte só o que o pedido não respondeu: **inferência não é resposta**.

**Derivados, não perguntados:** `message` (ecoada em uma frase), `language` (idioma do usuário, declarado), `audience` (infira; pergunte só se mudar a história), `aspect` (de `destination`), voz (pedido, depois o lembrado, depois o padrão do upstream). "Você tem o texto do sistema?" não é pergunta oficial: o texto é insumo do passo 1 do pipeline.

**Adições deste plugin (rotule como nossas):**

| Adição | Por quê | Padrão recomendado |
| --- | --- | --- |
| Fonte dos fatos e do que pode aparecer | Nenhum número inventado (V-61) | Arquivo(s) do dono; lista "não pode aparecer" |
| Privacidade do roteiro: nenhuma narração, local ou nuvem | O roteiro sai da máquina se houver credencial de nuvem (V-06) | Nenhuma ou local |
| Regime de som: mudo total, silencioso com SFX ou com voz | O pipeline trata cada um de forma diferente (V-24) | Silencioso (mudo total ou com SFX) |
| Idioma, tom e ID de voz `p*` explícito, se houver voz | Sem `--voice` o padrão é inglês (V-24) | pt-BR direto; voz só após teste de uma frase |
| Design: já tem guia, importa, não importa | Marca estrita (V-40, V-66) | Guia do usuário vence |
| Pasta do vídeo e resultado do preflight | Layout D10 e toolchain | Pasta nova e curta, sem `.env` acima |

O roteiro de 14 perguntas que circulou na pesquisa bruta não é oficial; não o use.

## 6. Pitch round (raro neste plugin)

Só para pedido não formado. Pergunte primeiro o que o usuário já imagina (a ideia dele entra como um pitch). Depois apresente cinco caminhos antes de qualquer recomendação, três linhas cada (conceito; mundo visual; gancho): mundo do assunto, emoção, audiência (atender ou quebrar a expectativa), anti-padrão invertido, formato incomum (carta, contagem, receita, mapa). Uma rodada só; misturar é resposta válida. As probabilidades que o upstream pede para estimar são heurística de diversidade, não métrica. Vídeo de sistema com tese clara quase nunca precisa disto.

## 7. Regime, modo e gates

Duas perguntas, cada uma sozinha: (a) *storyboard* sim ou não; (b) *flow*: `automation` (o agente dirige) ou `companion` (o usuário dirige). As quatro combinações são válidas. O `mode` é **derivado, nunca perguntado**: companion = collaborative; automation + yes = collaborative; automation + no = autonomous. Depois de existir `STORYBOARD.md`, o `mode` fica no frontmatter dele e vence na retomada. "go" vale só para o checkpoint exibido.

Gates do upstream: preferência (colaborativo pergunta; autônomo decide com uma linha de razão) · checkpoint · qualidade (para no erro) · roteamento · credencial (neste plugin, sempre offline). **O render é sempre gated pelo usuário**, nos dois modos.

## 8. Oferta e design (3 estados)

Ofereça no máximo 1 a 2 capacidades rastreadas ao conceito, nunca o catálogo (sugestão que serviria a qualquer vídeo é descartada). Design: (1) **já tem guia** (`frame.md`, `design.md`, `DESIGN.md`): anote em `## Assets` e vira verdade; (2) **importa mas não tem**: escolha 2 a 3 presets e peça ao usuário que abra o `frame-showcase.html` de cada um, para decidir por olho; (3) **não importa**: decida e diga por quê. Detalhes: skill `video-design-system`.

## 9. Fechamento

Faça a checagem de integração entre as respostas (formato x destino x duração x som). Resuma separando "você disse" de "inferido". **Revisão não é confirmação**: espere o ok explícito. Só então grave `DECISOES.md` e `BRIEF.md`; mudança de ideia depois disso é nova confirmação.

## 10. Como perguntar

Uma pergunta por mensagem, com a recomendação primeiro e o motivo; ofereça o "pode ser" como resposta curta.

- "Duração: recomendo ~75 s, porque o texto ensina quatro camadas e cada uma pede uns 12 s. Serve, ou prefere mais curto?"
- "Destino: se vai para o YouTube, o formato é 1920x1080 e os textos podem ser menores; para feed, 1080x1080 e o corpo sobe para 32 px. Qual é o destino principal?"
- "Som: recomendo vídeo silencioso com texto na tela, porque a cadeia de voz em português ainda não foi validada nesta máquina. Prefere assim, ou quer testar voz local?"
