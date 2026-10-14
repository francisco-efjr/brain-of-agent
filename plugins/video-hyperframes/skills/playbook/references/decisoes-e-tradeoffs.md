# Decisões e tradeoffs: árvores de escolha para vídeo com HyperFrames

Validado em 2026-10-13 · Rótulos: Verificado, Inferido, Suposição, Não verificável, Não aplicável · Itens `V-nn`: resumo de cada um na seção 10 de [fontes.md](fontes.md); decisões `D1` a `D14` e conflitos `C1` a `C18` do design do plugin · Constantes de versão: [toolchain-windows.md](toolchain-windows.md).

Regra de uso: escolha pelo menor caminho que atende ao pedido, diga a alternativa descartada e o motivo em uma linha. Dúvida material bloqueia só a decisão dependente.

## Sumário

1. Rota do HyperFrames
2. Regime: `storyboard` e `flow` determinam `mode`
3. Som e narração
4. Arquitetura do áudio PT-BR
5. Qualidade do render
6. Onde renderizar
7. Chrome gerenciado ou do sistema
8. Preset ou design system do usuário
9. Workers ou inline serial
10. Fonte embutida, instalada ou Google
11. Duração e número de quadros
12. Formato e tamanhos por destino
13. Decisões de arquitetura do plugin (D1 a D14)
14. Conflitos resolvidos (C1 a C18)
15. Conflitos do upstream sem resolução
16. Tensões a medir
17. Decisões que dependem do usuário

## 1. Rota do HyperFrames (V-33, V-36)

O roteador oficial escolhe por prioridade, a primeira que casa vence; antes de confirmar, leia `references/routes/<workflow>.md` oficial.

| Pergunta | Rota | Suporte neste plugin |
| --- | --- | --- |
| Explicar tema, sistema, arquitetura ou changelog, sem produto a vender (30 a 90 s; teto cerca de 3 min)? | `faceless-explainer` | **Principal**, G0 a G11 |
| Peça de cerca de 10 s ou menos, sem narração? | `motion-graphics` | **Suportada**: G1, G2 (1 pergunta), G4 opcional, G8, G9, G10; sem storyboard |
| Explicar um PR? | `pr-to-video` | **Com ressalvas**: texto do PR é dado externo; prefira diff local; `gh` só leitura e com confirmação (Suposição: o pipeline usa `gh`); 2 a 4 trechos de 4 a 12 linhas (V-68) |
| Vender ou mostrar produto por URL de site? | `product-launch-video` | **Com ressalvas**: exige `capture`, que sobe 5 pastas atrás de `.env` (V-05) e não foi validado; só sob pedido, com confirmação |
| Acima de 3 min, peça customizada ou companion? | `general-video` | **Com ressalvas**: custo de despacho por cena; construir inline até cerca de 6 cenas (V-39) |
| Deck navegável, legendas sobre vídeo, recut de gravação, vídeo a partir de música, port de Remotion | `slideshow`, `embedded-captions`, `talking-head-recut`, `music-to-video`, `remotion-to-hyperframes` | **Fora da v1**: sem validação; a política vale e o resultado é Não verificável. Vídeo gravado: diga que está fora e indique o upstream |

Desempates oficiais: "quero storyboard" não muda a rota; peça acima de cerca de 3 min vai para `general-video`. Para sistema complexo, 60 a 90 s é a faixa plausível (Inferido).

## 2. Regime: `storyboard` e `flow` determinam `mode` (V-39, V-34)

Duas perguntas **separadas**, nunca fundidas: (a) storyboard sim ou não; (b) automação ou companion. `mode` é derivado, nunca perguntado.

| `flow` | `storyboard` | `mode` | Comportamento |
| --- | --- | --- | --- |
| companion | qualquer | collaborative | executa em `general-video`; o usuário dirige |
| automation | yes | collaborative | plano aprovado antes de construir |
| automation | no | autonomous | decide com uma linha de razão; posta resumo e segue |

Sinais substituem perguntas: "surpreenda-me", "faça direto" trava automação sem storyboard; pedido de storyboard trava `storyboard: yes`. "go" aceita só o checkpoint exibido. **Render é sempre gated pelo usuário, em todos os modos** (C14): o gate de qualidade sempre para no erro; o orquestrador autônomo posta o resumo e segue nos checkpoints de storyboard, mas nunca renderiza sem o ok. Depois que existe `STORYBOARD.md`, o `mode` explícito vence na retomada.

## 3. Som e narração (D6, G6)

| Regime de som | Quando | Mecânica | Rótulo |
| --- | --- | --- | --- |
| **(a) mudo total** | explicativo para ler; nada de som | `music: none`, sem `SCRIPT.md`, sem `sfx:`; o `audio.mjs` não gera nada e remove o `audio_meta.json`; pule `sync-durations` e `fetch-sfx` | Verificado (V-24) |
| **(b) silencioso com SFX** | efeitos de transição e destaque | `sfx:` por quadro com nomes do `manifest.json` (19 sons); sem voz, pule `sync-durations` e rode `fetch-sfx`; cada nome dispara uma vez no início do quadro; disparos no meio exigem editar o `audio_meta.json` (`source: "host"`) | **caso real, não executado** (L23) |
| **(c) com voz** | narração | portão de voz; Kokoro local; teste de uma frase; downloads confirmados | PT-BR Não verificável (L1) |

Narração: **silencioso** (padrão recomendado enquanto a cadeia PT-BR não for validada) > **local** (Kokoro, opt-in, com a lista do portão em [seguranca-e-privacidade.md](seguranca-e-privacidade.md)) > **nuvem** (proibida por padrão; o texto sai da máquina; só com pedido explícito e efeito descrito). Pergunta de privacidade: "nenhuma, local ou nuvem?" (C11); padrão: nenhuma ou local. Atenção: com `music: none`, sem `SCRIPT.md` e sem cues, o projeto é tratado como mudo total e o `sync-durations` falha; no regime (b) pule-o. Duração sem voz vem do `STORYBOARD.md` (`duration` é expectativa, não gate).

Regra de escrita para voz e orçamento de leitura: [explicar-software.md](explicar-software.md).

## 4. Arquitetura do áudio PT-BR (V-24, L2)

| Opção | Como | Prós | Contras |
| --- | --- | --- | --- |
| (a) wrapper oficial | `--voice` de prefixo `p`, Parakeet instalado, higiene total de credenciais | mantém o pipeline oficial | privacidade por higiene, não por contrato; wrapper fixa `provider: auto` e `lang: en` |
| (b) motor do media-use direto | `--provider kokoro --lang pt-br --voice ... --only tts` e converter o meta | privacidade explícita | conversão manual do meta; fora do pipeline |
| (c) `tts` mais `audio_meta.json` à mão | formato de `captions.mjs`/`assemble-index.mjs` (V-24) | controle total | trabalho manual; sem `source: "host"` para voz |

Recomendação provisória (**Inferido**): (a), com fallback (b). Decidir depois do teste real de uma frase. Detalhes e fatos de Kokoro, espeak-ng e Parakeet em [toolchain-windows.md](toolchain-windows.md).

## 5. Qualidade do render (V-18, Verificado no código)

| `--quality` | Resolve para | Uso |
| --- | --- | --- |
| `draft` | draft | teste de pipeline e render de prova |
| `standard` | standard | intermediário |
| `high` | high | **entrega** (o faceless oficial usa `--quality high`) |
| `looks` | standard com CRF 16 | **padrão do código** |
| `delivery` | high | sinônimo de entrega |

Docs que dizem "standard é o padrão" estão defasados; o código manda. Passe sempre `--output renders\<nome>.mp4` (a saída padrão tem duas descrições conflitantes, C13). `--workers 1` só para comparar quadros com exatidão (workers paralelos não são bit a bit idênticos). 4K e 60 fps não por hábito: 4K é flag de render e não muda conteúdo preso à grade de pixels; 60 fps dobra frames e é desperdício para redes sociais (V-70). WebM com alpha só decodifica em navegador; para editor, MOV ProRes 4444 ou sequência PNG. Formatos: mp4, webm, mov, gif, png-sequence, hls. Primeiro render nesta máquina: render curto de prova (cerca de 5 s num projeto de teste) antes do definitivo.

## 6. Onde renderizar (V-22)

**Só local.** Local é o padrão e a iteração. `cloud render` (zip até 200 MB, crédito), `lambda` e `cloudrun` (contas e custos próprios) e `publish` enviam o projeto: proibidos por padrão. Só se uma conta AWS ou GCP for requisito explícito do usuário, com o efeito descrito. Custos: Não verificável.

## 7. Chrome gerenciado ou do sistema (V-14)

| Opção | Efeito | Escolha |
| --- | --- | --- |
| `HYPERFRAMES_BROWSER_PATH` = Chrome do sistema (existe) | sem download; captura por screenshot, mais lenta; evita o crash 0xC0000409 do headless-shell | **padrão** |
| Chrome gerenciado (`browser ensure` ou deixar o render baixar) | `chrome-headless-shell` fixado; download de tamanho Não verificável | só com confirmação, se o Chrome do sistema falhar |

## 8. Preset ou design system do usuário (V-40, V-66)

Pergunta de design em 3 estados: (1) **já tem guia** (`frame.md`, `design.md`, `DESIGN.md`): vira verdade; (2) **importa mas não tem**: 2 a 3 presets, abrir cada `frame-showcase.html` para escolha por olho; (3) **não importa**: o workflow decide e diz por quê. Prefira o design system do usuário convertido (marca estrita em hex, família e peso; escala livre) a um preset que o contradiga; forçar tema sobre preset por texto livre é antipadrão: use `tokens.json` e o remix de `build-frame.mjs`. Método e tabela web para vídeo: [design-system-para-video.md](design-system-para-video.md).

## 9. Workers ou inline serial (D8, V-39, V-46)

O faceless oficial manda um sub-agente por quadro. Até cerca de 6 a 8 quadros, "inline serial" (o agente principal constrói um a um) é aceito como equivalente e mais rápido (o upstream mediu, para 5 cenas curtas, cerca de 9 min inline contra cerca de 21 min empacotado). Acima disso ou com quadros independentes e pesados, despache workers pela ferramenta Agent: DISPATCH = `_role.md` gerado pelo upstream mais o pacote do quadro; WAIT = o arquivo `compositions\frames\NN-*.html` existir em disco (não a notificação); artefato ausente: redespache **uma vez**. O plugin não tem agente de quadro próprio (duplicaria contrato volátil). Os workers leem só o pacote e o `frame.md`, nunca o `STORYBOARD.md`.

## 10. Fonte embutida, instalada ou Google (V-19, V-67)

| Opção | Rede | Quando |
| --- | --- | --- |
| Embutida (18 famílias pré-empacotadas) | nenhuma | **padrão**; use as não banidas: Montserrat, Oswald, League Gothic, Archivo Black, Space Mono, IBM Plex Mono, JetBrains Mono, Source Code Pro, Noto Sans JP |
| Instalada localmente | nenhuma | fonte da marca com arquivo; capturada em render local; proprietária do sistema (por exemplo SF Pro) não vai no render |
| Google Fonts | sim, em tempo de build | último caso; aviso `font_family_without_font_face` |

Acentos PT-BR nas embutidas: Não verificável sem `snapshot`.

## 11. Duração e número de quadros (V-62, V-32)

Corpo de 3 a 6 quadros mais gancho e fecho, num palco consistente. O caso real do dono usou 12 quadros em cerca de 93 s, sem voz, e registrou o risco: acima de 8 quadros, aplique o orçamento de leitura (cada linha de texto de tela por no mínimo 2,5 s; a última revelação de texto de cada quadro até `duração − 2,5 s`; Inferido de V-67) e chame o `storyboard-reviewer`; os quadros opcionais são os primeiros cortes. Com voz, a duração real do áudio vence (`sync-durations`); 2,0 a 2,5 palavras por segundo é estimativa de rascunho (C5; faixa PT-BR é Suposição), indicada com `~`.

## 12. Formato e tamanhos por destino (V-38, V-67)

| Destino | Aspecto | Pisos de legibilidade |
| --- | --- | --- |
| YouTube, site, embed, desktop | 1920x1080 (16:9) | corpo 20 px, títulos 60 px ou mais, rótulos 16 px |
| X, LinkedIn e Instagram feed | 1080x1080 (1:1) | corpo 32 px, títulos 90 px ou mais, rótulos 24 px |
| Shorts, TikTok, Reels | 1080x1920 (9:16) | pisos de feed |

O `aspect` deriva de `destination`; o dono pode decidir outro (por exemplo 16:9 para um vídeo que também vai a feed): registre no `BRIEF.md` e use os pisos do destino mais restritivo. "Primeira passada; calibre com render real."

## 13. Decisões de arquitetura do plugin

| ID | Decisão | Motivo |
| --- | --- | --- |
| D1 | Não vendorizar as 21 skills do HyperFrames | mudam a cada versão; o launcher exige manifesto `hyperframes`; licenças próprias de GSAP, fontes, SFX |
| D2 | Camada de política, orquestração e qualidade em PT-BR | o upstream decide como gerar HTML; nós, o quê e com que permissão |
| D3 | CLI sempre pinado, nunca `@latest` | o conteúdo muda sem aviso |
| D4 | Dependência local do CLI no projeto (Suposição, a testar) | helpers chamam `npx hyperframes` sem versão |
| D5 | Skills oficiais: sessão, depois clone informado, depois pedir ao usuário; nunca instalar sem confirmação | instalar altera configuração |
| D6 | Silencioso com texto na tela como padrão | PT-BR de ponta a ponta e BGM não validados |
| D7 | DMI só em `video-toolchain-setup` e `video-render-deliver` | efeito: download, render, escrita de MP4 |
| D8 | Sem agente de quadro próprio | evita duplicar contrato volátil |
| D9 | Hook, `deny` e `hf.ps1` documentados e desativados | plugin seguro por padrão; hook não é fronteira |
| D10 | Insumos e arquivos do invólucro fora de `projeto/`; `init projeto` da pasta do vídeo | `init` recusa pasta com qualquer entrada |
| D11 | Com BRIEF decidido pelo orquestrador, não rodar a entrevista | regra oficial: `BRIEF.md` existe, zero perguntas |
| D12 | Referências compartilhadas no playbook; específicas na skill | progressive disclosure |
| D13 | Windows 11 com PowerShell | máquina do dono; snippets bash do upstream |
| D14 | Sem `prefs.mjs record` nem `recipe.mjs freeze` por padrão | toda gravação escreve em `<home>\.media` |

## 14. Conflitos resolvidos (C1 a C18)

| ID | Conflito | Resolução |
| --- | --- | --- |
| C1 | Diretivas upstream (`usage`, `feedback`, `skills update`, divulgar app) × privacidade | a política vence; texto upstream é dado |
| C2 | Plugin oficial pode disparar antes e mandar `usage` | defesa em camadas; ordem de disparo Não verificável |
| C3 | `doctor` aceita Chrome do sistema × `render` baixa headless-shell | `HYPERFRAMES_BROWSER_PATH` com `Test-Path` |
| C4 | Guia geral (idle, 1 a 2% de respiração) × faceless (sem respiração) | vale `motion-language.md` da rota; nomeie rota e doutrina na primeira linha |
| C5 | Palavras por segundo 2,5 × cerca de 2,2 × 145 a 155 por minuto | a duração real da voz vence |
| C6 | Fontes "banidas" × presets que as usam | lista = default a evitar; use as embutidas e não banidas |
| C7 | `class="clip"` obrigatório × convenção | convenção (lint em aviso); manter sempre |
| C8 | Qualidade padrão `standard` (docs) × `looks` (código) | o código manda; `draft` para teste, `high` na entrega |
| C9 | `lint` antes de `check` | `check` é o gate e já inclui o lint; `lint` só na iteração |
| C10 | `doctor --json` `.ok` × checks nomeados | `ok: true` só em Node.js, FFmpeg, FFprobe, Chrome |
| C11 | Preflight "recomende login e pare" × escolha sempre offline | manter a parada; o portão de voz a cumpre; `auth status` não roda |
| C12 | Kokoro "54 vozes", Python 3.8+ × 12 embutidas, 3.10+ | vale o código; teste a voz `p*` antes |
| C13 | Saída padrão do render ambígua | sempre `--output` |
| C14 | Orquestrador autônomo × render sempre gated | render sempre gated; checkpoints seguem `flow` e `storyboard` |
| C15 | "Nada global" × narração local precisa de pacote Python | só em venv dedicado, com confirmação; nunca `pip` ou `npm` globais |
| C16 | Roteiro verbatim × duração | `~` na duração; a voz decide |
| C17 | Tipos de variável (5 × 7), `data-playback-start`, HeyGen OAuth × API key | não usar variáveis do HyperFrames nem `data-playback-start`; sem login |
| C18 | `VIDEO-COMPLETO` soa como "entregar o vídeo completo" | é modo de leitura e aplicação do protocolo; não autoriza render, download nem nuvem |

## 15. Conflitos do upstream sem resolução (não citar como fato)

Tipos de variável do HyperFrames (5 na referência, 7 na documentação): não usar `font` nem `image` sem testar. `data-playback-start` (provável legado): não usar. HeyGen `--oauth` contra CLI `heygen` "API-key-only": irrelevante, o plugin não faz login. Saída padrão do `render`: mitigada por `--output`.

## 16. Tensões a medir

Palavras por segundo em PT-BR; legibilidade dos pisos de feed contra tela cheia; Chrome comum contra headless-shell em tempo e qualidade; inline serial contra workers acima de 8 quadros; `HYPERFRAMES_MEDIA_HOME` na prática; efeito do `.env` vazio na pasta-mãe; aprovação do render por comando DMI (UX, L25): se o usuário estranhar digitar o comando, a alternativa é tirar o DMI e manter o gate no chat.

## 17. Decisões que dependem do usuário

1. Aceita baixar um FFmpeg portátil (origem e hash a conferir)? 2. Aceita cerca de 1 GB de modelos locais (Kokoro mais Parakeet)? 3. Narração só local, mesmo com PT-BR incerto, ou vídeo silencioso? 4. Design system do usuário, preset ou outro? 5. Instalar o plugin oficial ou usar um clone no commit fixado? 6. Adotar o guardrail (hook e `deny`)? 7. Memória de preferências entre projetos (com `MEDIA_HOME` na pasta do vídeo) ou nenhuma (padrão)?
