# TP-05 · `COMO-RENDERIZAR.md` (modelo de entrega)

Uso: a skill `video-render-deliver` grava este arquivo em `<pasta-do-video>\projeto\COMO-RENDERIZAR.md` depois do render, para que qualquer pessoa refaça o MP4 sem a conversa. Escreva só o que foi executado, com a saída real; o resto fica marcado como "não executado". Sem valores de variáveis, sem chaves, sem caminhos pessoais quando o arquivo for compartilhado (`<usuario>`).

## 1. Resultado

- MP4: `[caminho absoluto]\renders\[nome].mp4`
- Medido com `ffprobe` em [AAAA-MM-DD]: duração [s] · largura x altura [..] · taxa de quadros [..] · áudio [nenhum / 1 fluxo: codec]
- Duração pedida: ~[N] s (tolerância [MIN] a [MAX] s) -> [dentro / fora]
- Qualidade: `[draft / standard / high / looks / delivery]` · tempo do render: [..]
- Contact sheet: `[caminho]\contact-sheet.jpg` · relatório de revisão: [caminho]

## 2. Pré-requisitos (sem valores secretos)

- Windows 11 com Windows PowerShell 5.1; Node 22 ou superior; invólucro `hf.ps1` em `<pasta-do-video>\scripts\`
- Skills oficiais do HyperFrames: [plugin / clone] no commit [hash]; CLI `hyperframes@0.8.154`
- Chrome do sistema; FFmpeg e ffprobe portáteis (origem [..], SHA-256 conferido [sim/não])
- Rede para `cdn.jsdelivr.net` (o GSAP é buscado na compilação do `check` e do `render`) e, se houver fonte fora do pacote, para o Google Fonts
- Variáveis de sessão (só nomes): `HYPERFRAMES_NO_TELEMETRY`, `DO_NOT_TRACK`, `HYPERFRAMES_NO_UPDATE_CHECK`, `HYPERFRAMES_SKIP_SKILLS`, `HYPERFRAMES_MEDIA_HOME`, `HYPERFRAMES_BROWSER_PATH`, `HYPERFRAMES_FFMPEG_PATH`, `HYPERFRAMES_FFPROBE_PATH`

## 3. Comandos (cada bloco é uma chamada de ferramenta: o processo é novo)

```powershell
# verificar (gate): check inclui o lint
. "<pasta-do-video>\scripts\hf.ps1" ; Set-Location "<pasta-do-video>\projeto" ; hfs check

# contact sheet nos pontos medios das cenas
. "<pasta-do-video>\scripts\hf.ps1" ; Set-Location "<pasta-do-video>\projeto" ; hfs snapshot --at "[t1,t2,...]"

# preview local (aprovacao); conferir escuta em 127.0.0.1
. "<pasta-do-video>\scripts\hf.ps1" ; Set-Location "<pasta-do-video>\projeto" ; hfs preview --background

# render, so depois do ok ao preview; --output sempre explicito
. "<pasta-do-video>\scripts\hf.ps1" ; Set-Location "<pasta-do-video>\projeto" ; hfs -Ok render --quality [q] --output renders\[nome].mp4

# medir o MP4
. "<pasta-do-video>\scripts\hf.ps1" ; Set-Location "<pasta-do-video>\projeto" ; Set-HfSession ; & $env:HYPERFRAMES_FFPROBE_PATH -v error -show_entries "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate" -of json "renders\[nome].mp4"
```

## 4. Como ler o `ffprobe`

`format.duration` em segundos (compare com a tolerância); `streams[].width` e `height` devem igualar o `aspect` do `BRIEF.md`; `r_frame_rate` vem como fração (`30/1`); sem fluxo `audio` quando o regime é mudo total, um fluxo quando há SFX ou voz. Nada disso é "pronto" sem a saída colada na seção 5.

## 5. O que foi executado de fato

| Passo | Executado? | Saída ou evidência | Rótulo |
| --- | --- | --- | --- |
| `check` | [sim/não] | [erros, avisos, `browserSkipped`] | [Verificado / Não executado] |
| `snapshot` e contact sheet | | [id] | |
| Preview | | [HTTP 200 em 127.0.0.1:porta; escuta local conferida] | |
| Render de teste curto | | [duração e tempo] | |
| Render final | | [comando e tempo] | |
| `ffprobe` | | [JSON colado ou resumo com os campos acima] | |

O que não foi executado e por quê: [lista]. Limitações conhecidas: PT-BR de ponta a ponta e o desempenho do render com Chrome comum não foram medidos antes do primeiro uso; [outras].

## 6. Como refazer e como desfazer

- Refazer: repita a seção 3 na ordem; para mudar algo, altere **uma** variável por render ("mude só X para Y; mantenha o resto").
- Desfazer: apague `renders\[nome].mp4`; o preview em segundo plano para com `Stop-Process -Id [PID]`; as pastas `.hyperframes\`, `.media-home\` e `.hf-vazio\` podem ser apagadas à mão. Nada foi gravado em `PATH`, registro do Windows ou skills globais. O CLI mantém caches fora do projeto (`~\.hyperframes`, `~\.cache\hyperframes`) que só você decide limpar (`hfs clean --dry-run` mostra o que sairia).

## 7. Aviso de rede e privacidade

O render consulta `cdn.jsdelivr.net` (GET público, sem dado do usuário). Nada do roteiro, do projeto ou de credenciais foi enviado; o projeto não foi publicado nem renderizado na nuvem.
