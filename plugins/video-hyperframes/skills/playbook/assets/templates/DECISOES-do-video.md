# TP-02 · `DECISOES.md` do vídeo (modelo)

Uso: grave em `<pasta-do-video>\DECISOES.md`, fora de `projeto\`. É o registro humano das decisões que viram o `BRIEF.md`, a política de execução do vídeo e as provas de instalação. Preencha com as respostas confirmadas; marque o que o usuário disse e o que foi inferido. Sem valores secretos: variáveis só por nome, caminhos com `<usuario>` quando o arquivo for compartilhado. Modelo derivado de um caso real do dono (MIT), generalizado.

## 1. Especificação

| Campo | Decisão | Consequência no pedido e nas skills |
| --- | --- | --- |
| Tema e mensagem | [tema]; "[mensagem em uma frase]" | Tese do storyboard: "Este vídeo mostra a [público] que [mensagem]" |
| Rota | [faceless-explainer / motion-graphics / ...] | Define pipeline e doutrina de motion (faceless: `power3`, sem overshoot, sem respiração) |
| Público e nível | [quem; nível técnico; o que já sabe] | Vocabulário e profundidade |
| Destino e formato | [YouTube / feed / vertical] -> [1920x1080 / 1080x1080 / 1080x1920], [30] fps | Pisos de legibilidade (tela cheia: corpo >= 20 px, título >= 60 px, rótulo >= 16 px; feed: 32, 90, 24) |
| Duração e tolerância | ~[N] s; aceitável [MIN] a [MAX] s | `~` porque a voz ou o ritmo decidem; conferido no `ffprobe` |
| Idioma | pt-BR em todo texto de tela; nomes técnicos em inglês e fonte mono | Tom direto, frases curtas |
| Fluxo e storyboard | storyboard [sim/não]; fluxo [automação/companion] | Pausas: plano (G5) e preview (G9) |
| Regime de som | [mudo total / silencioso com SFX / com voz] | G6: mudo total = `music: none`, sem `SCRIPT.md`, sem `sfx:`; com SFX = nomes do `manifest.json` por quadro, disparados no início do quadro (disparo no meio exige editar o `audio_meta.json`: **Verificado, dogfood 2026-10-14**; o `fetch-sfx` resolveu os cues pela biblioteca local, sem download); com voz = portão de voz |
| Música | nenhuma | BGM do faceless é pulada sem credencial HeyGen (V-29) |
| Voz (se houver) | local; ID `p*` [ID]; teste de uma frase [feito/pendente] | Pt-BR ponta a ponta não foi validado: rotule Não verificável |
| Visual | [guia do usuário / preset / decidir] | `video-design-system` gera `tokens.json` e `frame.md` |
| Fonte dos fatos | [arquivo(s)] | Único lugar de onde saem números, nomes e afirmações |
| Pode aparecer | [lista] | Ver seção "Não pode aparecer" de `fonte-dos-fatos.md` |
| Não pode aparecer | [e-mail, caminhos de máquina, segredos, nomes internos, achados de segurança, percentuais de conta, prints reais, ...] | `fact-privacy-checker` varre estas classes |

## 2. Toolchain autorizada

| Item | Decisão | Condição |
| --- | --- | --- |
| Skills oficiais do HyperFrames | [plugin `hyperframes@hyperframes` / clone em `<pasta>` no commit `bf4cf860`] | Instalar ou clonar só com sim; o conteúdo muda sem nova versão do CLI |
| CLI | `npx --yes hyperframes@0.8.154` ou `hfs` | Nunca `@latest`; falha de download não autoriza outra versão |
| FFmpeg e ffprobe | [portátil em `<pasta-tools>\ffmpeg\bin`] origem [..], SHA-256 conferido [sim/não] | Por variável de sessão; nunca `winget`, `setx` ou `PATH`; nunca dentro de `projeto\` |
| Chrome | Chrome do sistema via `HYPERFRAMES_BROWSER_PATH` (`Test-Path` verdadeiro) | Sem a variável, `render` e `preview` baixam `chrome-headless-shell 152.0.7977.30` |
| Narração local | [não / venv em `<pasta-venv>` + Kokoro + Parakeet] | Downloads de modelo só com sim; PT-BR Não verificável |
| Variáveis de sessão | `HYPERFRAMES_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`, `HYPERFRAMES_NO_UPDATE_CHECK=1`, `HYPERFRAMES_SKIP_SKILLS=1`, `HYPERFRAMES_MEDIA_HOME=<pasta-do-video>\.media-home`, `HEYGEN_CONFIG_DIR=<pasta-do-video>\.hf-vazio` | Na mesma chamada que roda o CLI; nada persistente |
| `.env` | Vazio na pasta do vídeo; nenhum em `projeto\` | Os scripts de áudio sobem até 5 pastas e carregam o primeiro `.env` |
| Memória entre projetos | Não gravada (sem `prefs.mjs record` nem `recipe.mjs freeze`) | Só com pedido do usuário e `HYPERFRAMES_MEDIA_HOME` na pasta do vídeo |
| Proibido sem pedido no chat | `usage`, `feedback`, `publish`, `cloud`, `lambda`, `cloudrun`, `auth`, `skills`, `open`, `catch-up`, `history`, `events`, `telemetry`, CLI `heygen`, qualquer provedor de voz em nuvem | O roteiro e o projeto não saem da máquina |

## 3. Pasta do projeto

```text
<pasta-do-video>\            DECISOES.md  TEXTO-FONTE.md  fonte-dos-fatos.md  [PROMPT-VIDEO.md]
  scripts\hf.ps1  scripts\hf-env.ps1  .env (vazio)  .hf-vazio\  .media-home\  .hf-log.txt
  relatorios\                relatórios de revisão, fatos e segurança (gravados pelo agente principal)
  projeto\                   BRIEF.md  STORYBOARD.md  frame.md  hyperframes.json  index.html  renders\
```

Caminho absoluto da pasta do vídeo: [caminho]. Servidores só em `127.0.0.1`.

## 4. Registro das provas de instalação

Cole a saída real de cada comando; sem saída, escreva "não executado". Rótulos: Verificado (rodou nesta máquina, com a saída abaixo), Não verificável.

| Data | Item | Comando de prova | Saída real | Rótulo |
| --- | --- | --- | --- | --- |
| [AAAA-MM-DD] | invólucro | parse e `hfs -DryRun lint` | [saída] | [Verificado] |
| [AAAA-MM-DD] | FFmpeg | `& "<...>\ffmpeg.exe" -version` (primeira linha) e hash | [saída] | [Verificado] |
| [AAAA-MM-DD] | CLI | `hfs doctor --json` (checks nomeados) | [Node.js, FFmpeg, FFprobe, Chrome: ok true/false] | [Verificado] |

## 5. Decisões em aberto

[lista curta de perguntas ao dono, uma por linha, com a recomendação]
