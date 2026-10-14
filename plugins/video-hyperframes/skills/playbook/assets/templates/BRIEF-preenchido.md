# TP-01 · `BRIEF.md` preenchido (exemplo genérico)

Uso: copie o bloco para `<pasta-do-video>\projeto\BRIEF.md` como **primeira escrita dentro de `projeto\`**, depois do `init` (o `init` recusa pasta com qualquer arquivo, D10). Com o `BRIEF.md` presente, as skills não refazem perguntas de brief: ele é o token de não repetição e a verdade da retomada (V-33, V-38). Quem preenche é a skill `video-brief-interview`, a partir das respostas confirmadas pelo usuário; se o orquestrador já entregou as decisões, grave os campos sem rodar a entrevista (D11).

## Exemplo (sistema fictício de filas de pedidos, vídeo silencioso, YouTube)

```markdown
---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Um roteador por prioridade faz o pedido urgente furar a fila sem perder nenhum outro"
destination: youtube
aspect: 1920x1080
language: pt-BR
audience: "desenvolvedores de backend que operam filas e querem entender o roteamento"
length: 90s
angle: concept
narration: no
---
## Intent
Explicar por dentro como o roteador por prioridade, os workers e a fila de mortas trabalham juntos, em camadas, no mesmo palco. Prova com os números do arquivo de fatos; fecha com os limites honestos.

## Assets
- fonte-dos-fatos.md — ledger de afirmações; todo número do vídeo vem daqui
- TEXTO-FONTE.md — texto aprovado, copiado verbatim para capture/extracted/visible-text.txt

## Customizations
- design: guia do usuário em tokens.json -> frame.md (ver video-design-system)

## Notes
- som: mudo total (music: none, sem SCRIPT.md, sem sfx)
- privacidade: nada de nuvem, nada de login; o roteiro não sai da máquina
- tolerância de duração: 85 a 95 s
```

## Campos e valores normalizados

| Campo | Valores | Observação |
| --- | --- | --- |
| `workflow` | `faceless-explainer`, `motion-graphics`, `pr-to-video`, `product-launch-video`, `general-video` | Rota oficial; a v1 do plugin só dá suporte completo a `faceless-explainer` |
| `flow` | `automation` ou `companion` | Pergunta separada da de storyboard, nunca fundida (V-34) |
| `storyboard` | `yes` ou `no` | "Quero storyboard" trava `yes`; "surpreenda-me" trava `automation` + `no` |
| `message` | uma frase entre aspas | Ecoada para o usuário, não perguntada (V-35) |
| `destination` | Exemplos: `youtube`, `embed`, `x`, `linkedin`, `instagram-feed`, `shorts`, `tiktok` | O upstream só mostra `youtube` em exemplo (V-38): mantenha um vocabulário curto e consistente. Decide `aspect` e os pisos de legibilidade |
| `aspect` | `1920x1080`, `1080x1080`, `1080x1920` | Derivado: YouTube, site ou desktop = 1920x1080; feed social = 1080x1080; Shorts, TikTok e Reels = 1080x1920 |
| `language` | `pt-BR` | O idioma do usuário; declare, não pergunte |
| `audience` | frase curta | Inferida; pergunte só se mudar a história |
| `length` | `30s` a `90s` (teto de cerca de 3 min no faceless) | Com roteiro verbatim use `~` e deixe a voz decidir |
| `angle` | `concept`, `how-to`, `listicle`, `narrative` | Recomende o que o formato do texto sugere |
| `narration` | `yes`, `minimal`, `no` | Campo do contrato (`brief-contract.md:74`), ausente da tabela de `brief-format.md`; inclua |

O modo (`mode`) **não** entra aqui e nunca é perguntado: deriva de `flow` e `storyboard` (companion = collaborative; automation + yes = collaborative; automation + no = autonomous) e é gravado no frontmatter do `STORYBOARD.md`, onde vence na retomada (V-39).

Regras: a fala do usuário vai no corpo, os valores normalizados no frontmatter; mudança de ideia no meio da execução é nova confirmação; `## Assets` tem um arquivo por linha no formato `caminho — o que é, onde entra`. O plugin **não** grava memória entre projetos (`prefs.mjs record`, D14).

Fonte: HyperFrames (HeyGen, Apache-2.0), commit `bf4cf860`: `brief-format.md`, `brief-contract.md` (V-38, V-39); exemplo de redação própria.
