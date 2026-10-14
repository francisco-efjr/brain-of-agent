# Render e entrega: qualidades, rede, formatos, `ffprobe` e "Onde ver agora"

Base: HyperFrames (HeyGen, Apache-2.0), commit `bf4cf860fbd26a7d51938c5f11987c335d4e848a`: `render/plan.ts`, `render.ts`, `preview-render.md`, `htmlCompiler.ts`, `docs/prompting/rendering-and-output.mdx` (V-18, V-19, V-22, V-70), destilado com redação própria. Código vence documentação. **Nenhum render real foi executado na construção deste plugin** (lacuna L6); o dogfood de 2026-10-14 (vídeo silencioso de 12 quadros) executou `check`, `snapshot`, `preview` e `render` (DF-01, DF-07, DF-11), mas sem registrar métricas de render que valham aqui: velocidade, RAM, tamanho do MP4 e desempenho com Chrome comum são Não verificáveis; o primeiro render desta máquina começa por um teste curto.

Sumário: 1 Qualidade · 2 Saída e formatos · 3 Rede · 4 Só local · 5 Preview · 6 Render de teste · 7 `ffprobe` · 8 Falhas · 9 Entrega.

## 1. Qualidade (`--quality`)

| Valor | Equivale a | Quando usar |
| --- | --- | --- |
| `draft` | draft | Render de teste e conferência de montagem |
| `standard` | standard | Rascunho aceitável |
| `high` | high | **Entrega.** O pipeline faceless oficial usa `--quality high` |
| `looks` | standard com CRF 16 | **Padrão do código** quando a flag é omitida |
| `delivery` | high | Alias de entrega |

Os docs que dizem "`standard` é o padrão" estão defasados (V-18). Passe sempre a qualidade por extenso: não dependa do padrão. `--workers 1` só quando precisar comparar quadros com exatidão. `--docker` e `--batch` não são necessários. Não repita `lint`, `check` nem `snapshot` depois do render.

## 2. Saída e formatos

- **`--output renders\<nome>.mp4` sempre.** O help diz `renders/<name>.mp4` e um doc diz `renders/<projeto>_<data>_<hora>.<ext>`: ambiguidade não resolvida no upstream (C13).
- Formatos: `mp4`, `webm`, `mov` (ProRes 4444 com alpha), `gif`, sequência PNG, `hls`. **WebM com alpha** só decodifica em navegador: para editor, use MOV ProRes 4444 ou sequência PNG.
- Resolução e taxa seguem o `aspect` do `BRIEF.md` (1920x1080, 1080x1080 ou 1080x1920) a 30 fps. **Não peça 4K nem 60 fps por hábito**: 4K é flag de render (supersampling) e não muda conteúdo preso à grade de pixels; 60 fps dobra quadros e é desperdício para redes sociais. HDR é por fonte e só MP4 (não reconferido).
- Windows: o codificador em streaming desliga sozinho só em win32 com GPU de software forçada, `workers` numérico igual a 1 e sem escolha explícita do usuário; o modo low-memory entra pela RAM total. Efeito prático: Não verificável.

## 3. Rede

A compilação do `render` **e do `check`** faz GET público em `cdn.jsdelivr.net` (GSAP 3.15.0 por padrão; timeout de 15 s; valida `integrity`), e embute o texto. Falha de download: "The render may fail if this script is required (e.g. GSAP)". Fontes (**corrigido pela execução real, Verificado, dogfood 2026-10-14, DF-01**): as 18 famílias "embutidas" **não são bundle local** nesta versão do CLI. No `check`, no `snapshot` e no `render` o compilador baixa as faces do Google Fonts (11 de Montserrat e 10 de JetBrains Mono no caso real) e grava cache fora do projeto, em `%USERPROFILE%\.cache\hyperframes\fonts\` (pastas `montserrat\` e `jetbrains-mono\`), além de `%USERPROFILE%\.cache\hyperframes\history\`: é acesso de rede do render (ao lado do GSAP) e escrita fora do projeto (cache de ferramenta, sem dado do usuário). Família fora das 18 vem do Google Fonts do mesmo jeito (aviso `font_family_without_font_face`) ou da instalação local. Para render 100% offline: rodar uma vez online para popular o cache (Inferido) ou embutir `@font-face` local (Não verificado). Informe o usuário antes do render; não é possível "vendorizar" o GSAP (licença não OSI).

## 4. Onde renderizar: só local

Local é o padrão e a iteração. `cloud render` zipa o projeto (até 200 MB) e envia à HeyGen; `lambda` e `cloudrun` usam contas AWS e GCP e geram custo; `publish` envia o projeto inteiro. Todos são proibidos por padrão neste plugin: o roteiro e o projeto não saem da máquina. Se o usuário pedir, descreva o efeito (o que sai, para onde, custo desconhecido) e peça confirmação específica.

## 5. Preview

`hfs preview --background --no-open .` (de dentro de `projeto\`; `--no-open` evita abrir o navegador); a porta começa em **3002** e, se estiver ocupada, o CLI tenta as seguintes (até 100), então leia a porta real na saída do comando; sem `--no-open` o Studio local pode abrir o navegador sozinho. Verifique HTTP 200 e o endereço de escuta (troque `3002` pela porta lida):

```powershell
$porta = 3002
(Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:$porta").StatusCode
Get-NetTCPConnection -State Listen -LocalPort $porta | Select-Object LocalAddress, LocalPort, OwningProcess
```

`LocalAddress` deve ser `127.0.0.1` ou `::1`; se for `0.0.0.0` ou `::`, pare e avise. Por leitura do código (`packages/cli/src/server/portUtils.ts:441-447`, 2026-10-14), o servidor escuta em `127.0.0.1` por padrão e só muda com `HYPERFRAMES_PREVIEW_HOST`, que o invólucro remove; a conferência continua a cada vez. **Em execução (Verificado, dogfood 2026-10-14, DF-07):** subiu em `127.0.0.1:3002`, `netstat` mostrou LISTENING só em `127.0.0.1` e o HTTP deu 200; o log fica em `%USERPROFILE%\.local\state\hyperframes\previews\` (fora do projeto); para parar, `hfs preview "<pasta>" --stop`. O PID da coluna `OwningProcess` vai para o "Onde ver agora". Sem `HYPERFRAMES_BROWSER_PATH` válido, o `preview` também baixa o `chrome-headless-shell`: o invólucro recusa.

## 6. Render de teste (primeira vez nesta máquina)

Prova V-13 (FFmpeg), V-14 (Chrome) e V-19 (rede) com evidência antes do render caro. Preferência: um projeto de teste com composição de cerca de 5 s (por exemplo, um `init` do exemplo `blank` em pasta separada, se ele renderizar: Suposição). Sem projeto de teste: `--quality draft` do próprio vídeo, avisando que leva o tempo de um render inteiro. Registre tempo e resultado no `COMO-RENDERIZAR.md`. Se a máquina já tem um render de teste registrado, pule.

## 7. `ffprobe`

```powershell
. "<pasta-do-video>\scripts\hf.ps1" ; Set-Location "<pasta-do-video>\projeto" ; Set-HfSession
& $env:HYPERFRAMES_FFPROBE_PATH -v error -show_entries "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate" -of json "renders\<nome>.mp4"
```

Sintaxe conferida na construção com um clipe de 2 s e um FFmpeg portátil: devolve JSON; num clipe sem trilha de áudio, a lista `streams` não traz fluxo `audio` (com `-select_streams a` a saída é vazia e o código é 0). Confira:

| Campo | Critério |
| --- | --- |
| `format.duration` | Dentro da tolerância gravada no `DECISOES.md` (no caso de referência, 85 a 95 s para ~90 s). Sem tolerância gravada, reporte a diferença e deixe o usuário decidir |
| `width` x `height` | Igual ao `aspect` do `BRIEF.md` |
| `r_frame_rate` | Fração (`30/1`) igual ao pedido |
| Fluxo `audio` | Mudo total: nenhum. Silencioso com SFX ou com voz: um. Incoerência com o regime de som é achado |
| `size` | Registre; arquivo vazio ou minúsculo é falha |

Confirme também que o caminho absoluto existe (`Test-Path`) antes de anunciá-lo.

## 8. Falhas

Mostre o `stderr` e pare. Crash `0xC0000409` (3221225595) do `headless-shell` no Windows: confira `HYPERFRAMES_BROWSER_PATH` (remediação oficial). Sinal de download de Chrome: pare e pergunte. GSAP não baixado: verifique a rede para `cdn.jsdelivr.net`. Depois de 3 tentativas, pare e reporte o que falta.

## 9. Entrega

1. `COMO-RENDERIZAR.md` (template TP-05), só com o que foi executado.
2. Bloco **Onde ver agora** (primeiro item da mensagem final):

```text
Onde ver agora
- MP4: <caminho absoluto> | <duração> s | <largura>x<altura> | <fps> | áudio: <nenhum | 1 fluxo, codec>
- Contact sheet: <caminho absoluto>
- Preview: http://127.0.0.1:<porta> (HTTP 200, escuta local conferida, PID <n>; parar com Stop-Process -Id <n>) | preview encerrado
- Como refazer: <pasta-do-video>\projeto\COMO-RENDERIZAR.md
```

3. `recipe.mjs freeze` (memória do "look" entre projetos) só se o usuário pedir, com `HYPERFRAMES_MEDIA_HOME` na pasta do vídeo: a gravação vai para `<home>\.media\recipes` (D14).
4. Se o preview não sobreviver ao fim da sessão, diga.
