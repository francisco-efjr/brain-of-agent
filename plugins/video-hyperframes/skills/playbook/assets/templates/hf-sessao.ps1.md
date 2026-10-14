# TP-06 · Invólucro de sessão `hf.ps1` (texto para copiar)

Para que serve: rodar o CLI do HyperFrames sempre com a mesma higiene de sessão (versão fixa, telemetria desligada, credenciais de nuvem fora da sessão, Chrome por caminho explícito) e deixar um registro dos comandos. Não é fronteira de segurança, é fricção e registro: quem chama `npx hyperframes` direto escapa dele, e a autorização de verdade é o seu "sim" no chat.

Como instalar: a skill `/video-hyperframes:video-toolchain-setup` copia o bloco da seção 3 para `<pasta-do-video>\scripts\hf.ps1` (e, se preciso, a seção 4 para `scripts\hf-env.ps1`), com o seu "sim". Não existe `.ps1` dentro do plugin de propósito: o texto fica neste `.md` para você ler antes de executar. Grave o arquivo em ASCII (a ferramenta Write do Claude Code ou `Set-Content -Encoding ASCII`): o Windows PowerShell 5.1 lê arquivo sem BOM como ANSI, e o bloco foi escrito sem acentos por isso.

## Sumário

1. Layout (decisão D10)
2. O que o invólucro faz
3. O invólucro (copiar sem editar)
4. `scripts\hf-env.ps1` de exemplo
5. Como usar
6. Como testar sem executar o HyperFrames (com o resultado do teste)
7. Limitações

## 1. Layout (decisão D10)

```text
<pasta-do-video>\
  scripts\hf.ps1  scripts\hf-env.ps1     <- este invólucro e seus caminhos locais (não versionar hf-env.ps1)
  .env (vazio)  .hf-vazio\  .media-home\  .hf-log.txt   <- criados pelo invólucro; não versionar
  projeto\                                <- `init projeto` roda da pasta-mãe; antes do init não existe ou está vazia
```

Por que fora de `projeto\`: o `init` recusa pasta com qualquer entrada, inclusive dotfiles (`init.ts:842-845`, leitura no commit `bf4cf860`). O `.env` vazio fica na pasta do vídeo porque os scripts de áudio sobem até 5 pastas e carregam o primeiro `.env` que encontram (V-05); um arquivo vazio encerra a subida sem carregar nada (efeito Inferido de `heygen.mjs:72-95`, não executado).

## 2. O que o invólucro faz

| Função | Efeito |
| --- | --- |
| `hfs <verbo> ...` (`Invoke-Hf`) | Roda `node <npx-cli.js> --yes hyperframes@0.8.154 <verbo> ...` sem shell. Bloqueia verbos proibidos, exige `-Ok` nos de confirmação, recusa `render` e `preview` se `HYPERFRAMES_BROWSER_PATH` não aponta para arquivo que existe (o CLI ignoraria e baixaria outro Chrome, V-14) |
| `hfn <script.mjs> ...` (`Invoke-HfNode`) | Roda um helper Node das skills oficiais (`build-frame`, `frame-packets`, `captions`, `assemble-index`, `transitions`, `audio`) com a mesma higiene |
| `Set-HfSession` | Define `HYPERFRAMES_NO_TELEMETRY`, `DO_NOT_TRACK`, `HYPERFRAMES_NO_UPDATE_CHECK`, `HYPERFRAMES_SKIP_SKILLS`, `HYPERFRAMES_MEDIA_HOME` e `HEYGEN_CONFIG_DIR` (pasta vazia); remove da sessão as variáveis de credencial de nuvem e `HYPERFRAMES_PREVIEW_HOST` (o preview fica no padrão `127.0.0.1`); cria `.env` vazio, `.hf-vazio\`, `.media-home\`; para com erro se achar `.env` não vazio na pasta do vídeo ou no diretório atual; acha o Chrome do sistema; lê `scripts\hf-env.ps1` |
| `Write-HfLog` | Acrescenta `data status hfs verbo argumentos` a `.hf-log.txt` (nunca variáveis de ambiente). Estados: `BLOQUEADO`, `SEM-CONFIRMACAO`, `EXEC` |

| Grupo | Verbos | Motivo e alternativa |
| --- | --- | --- |
| Bloqueados (`$HfDeny`) | `usage`, `feedback`, `publish`, `cloud`, `lambda`, `cloudrun`, `auth`, `skills`, `open`, `catch-up`, `history`, `events`, `telemetry`, `heygen` | `usage` lê a credencial OAuth do Claude Code; `feedback` é canal público; `publish`, `cloud`, `lambda` e `cloudrun` enviam o projeto; `auth` e `heygen` mexem em credencial; `skills` instala skills globais; `open`, `catch-up`, `history`, `events` chamam app externo ou recurso em teste; `telemetry` muda configuração persistente. Alternativa: variáveis de sessão e render local. Só o usuário, no chat, depois de ouvir o efeito |
| Com `-Ok` (`$HfConfirm`) | `init`, `add`, `browser`, `models`, `tts`, `transcribe`, `remove-background`, `render`, `upgrade` (menos `--check`), `clean` (menos `--dry-run`), `catalog --on-device` | Download, instalação, escrita persistente ou custo. Repita com `-Ok` depois do "sim" |
| Livres | `lint`, `check`, `snapshot`, `timeline`, `compositions`, `compare`, `doctor`, `catalog --query`, `upgrade --check`, `clean --dry-run`, `preview` (Chrome válido) | Leitura ou efeito local |
| `hfn` bloqueado | `heygen-tts.mjs`, `heygen-voice.mjs`, `heygen.mjs` | Provedor de nuvem; o roteiro sairia da máquina |
| `hfn` com `-Ok` | `audio.mjs`, `prefs.mjs`, `recipe.mjs` | Voz, download de modelo ou gravação em `.media` (sem `record` nem `freeze` por padrão, D14) |

## 3. O invólucro (copiar sem editar)

```powershell
# hf.ps1 - involucro de sessao segura para o CLI do HyperFrames (esqueleto do plugin video-hyperframes)
# Copie para <pasta-do-video>\scripts\hf.ps1, FORA de projeto\ (o init recusa pasta com qualquer entrada, init.ts:842-845).
# Uso (uma chamada de ferramenta):  . "<pasta-do-video>\scripts\hf.ps1" ; hfs -Ok init projeto --non-interactive --example=blank --skill=faceless-explainer
#   depois:  . "<pasta-do-video>\scripts\hf.ps1" ; Set-Location "<pasta-do-video>\projeto" ; hfs lint ; hfs -Ok render --quality high --output renders\video.mp4
# Nao e fronteira de seguranca: e friccao e registro. A politica vive em seguranca-e-privacidade.md.
# ASCII de proposito: o Windows PowerShell 5.1 le arquivo sem BOM como ANSI.
$script:HfVersion = '0.8.154'
$script:HfDir     = $PSScriptRoot                    # <pasta-do-video>\scripts (hf-env.ps1 fica aqui)
$script:HfRoot    = Split-Path -Parent $PSScriptRoot  # <pasta-do-video>: .env vazio, .hf-vazio, .media-home e .hf-log.txt
$script:HfDeny    = @('usage','feedback','publish','cloud','lambda','cloudrun','auth','skills','open','catch-up','history','events','telemetry','heygen')
$script:HfConfirm = @('init','add','browser','models','tts','transcribe','remove-background','render','upgrade','clean')
$script:HfCredVars = @('HEYGEN_API_KEY','HEYGEN_ACCESS_TOKEN','HYPERFRAMES_API_KEY','ELEVENLABS_API_KEY','GEMINI_API_KEY','GOOGLE_API_KEY','HEYGEN_API_BASE')

function Write-HfLog([string]$Status, [string[]]$A) {
    # registro de comandos (verbo e argumentos, nunca variaveis de ambiente) para a auditoria pos-execucao
    $linha = '{0} {1} hfs {2}' -f (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss'), $Status, ($A -join ' ')
    Add-Content -LiteralPath (Join-Path $script:HfRoot '.hf-log.txt') -Value $linha
}

function Set-HfSession {
    $env:HYPERFRAMES_NO_TELEMETRY = '1'; $env:DO_NOT_TRACK = '1'
    $env:HYPERFRAMES_NO_UPDATE_CHECK = '1'; $env:HYPERFRAMES_SKIP_SKILLS = '1'
    foreach ($n in $script:HfCredVars) { Remove-Item -LiteralPath "Env:$n" -ErrorAction SilentlyContinue }
    # preview so em 127.0.0.1 (padrao do CLI); HYPERFRAMES_PREVIEW_HOST exporia a API do Studio na rede
    Remove-Item -LiteralPath 'Env:HYPERFRAMES_PREVIEW_HOST' -ErrorAction SilentlyContinue
    foreach ($d in @('.hf-vazio', '.media-home')) {
        $p = Join-Path $script:HfRoot $d
        if (-not (Test-Path -LiteralPath $p)) { New-Item -ItemType Directory -Path $p | Out-Null }
    }
    $env:HEYGEN_CONFIG_DIR = Join-Path $script:HfRoot '.hf-vazio'
    # prefs.mjs record grava sempre em <home>\.media (ledger de promocao); assim fica na pasta do video
    $env:HYPERFRAMES_MEDIA_HOME = Join-Path $script:HfRoot '.media-home'
    # .env vazio na pasta do video: os scripts de audio sobem ate 5 pastas e param no primeiro .env
    $raizEnv = Join-Path $script:HfRoot '.env'
    if (-not (Test-Path -LiteralPath $raizEnv)) { New-Item -ItemType File -Path $raizEnv | Out-Null }
    foreach ($f in (@($raizEnv, (Join-Path (Get-Location).Path '.env')) | Select-Object -Unique)) {
        if ((Test-Path -LiteralPath $f) -and ((Get-Item -LiteralPath $f).Length -gt 0)) { throw ".env nao vazio em '$f': nao abra; pergunte ao usuario." }
    }
    $chrome = @(
        (Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe'),
        (Join-Path ${env:ProgramFiles(x86)} 'Google\Chrome\Application\chrome.exe'),
        (Join-Path $env:LOCALAPPDATA 'Google\Chrome\Application\chrome.exe')
    ) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if ($chrome) { $env:HYPERFRAMES_BROWSER_PATH = $chrome } else { Remove-Item -LiteralPath 'Env:HYPERFRAMES_BROWSER_PATH' -ErrorAction SilentlyContinue }
    # scripts\hf-env.ps1 (opcional, do usuario) define HYPERFRAMES_FFMPEG_PATH, HYPERFRAMES_FFPROBE_PATH e HYPERFRAMES_PYTHON
    $cfg = Join-Path $script:HfDir 'hf-env.ps1'
    if (Test-Path -LiteralPath $cfg) { . $cfg }
}

function Invoke-Hf {
    param([switch]$Ok, [switch]$DryRun, [Parameter(ValueFromRemainingArguments = $true)][string[]]$HfArgs)
    if (-not $HfArgs -or $HfArgs.Count -eq 0) { throw 'Informe o subcomando do hyperframes.' }
    $verbo = $HfArgs[0].ToLowerInvariant()
    if ($script:HfDeny -contains $verbo) { Write-HfLog 'BLOQUEADO' $HfArgs; Write-Error "Bloqueado pela politica (verbo '$verbo'): so com pedido explicito do usuario no chat."; return }
    $precisa = ($script:HfConfirm -contains $verbo) -and -not ($verbo -eq 'upgrade' -and $HfArgs -contains '--check') -and -not ($verbo -eq 'clean' -and $HfArgs -contains '--dry-run')
    if (($verbo -eq 'catalog') -and ($HfArgs -contains '--on-device')) { $precisa = $true }
    if ($precisa -and -not $Ok) { Write-HfLog 'SEM-CONFIRMACAO' $HfArgs; Write-Error "O verbo '$verbo' exige confirmacao do usuario no chat; repita com -Ok depois do sim."; return }
    Set-HfSession
    $temChrome = $env:HYPERFRAMES_BROWSER_PATH -and (Test-Path -LiteralPath $env:HYPERFRAMES_BROWSER_PATH)
    if (($verbo -eq 'render' -or $verbo -eq 'preview') -and -not $temChrome) { Write-Error 'HYPERFRAMES_BROWSER_PATH ausente ou inexistente: render/preview baixariam o chrome-headless-shell. Pare e pergunte.'; return }
    $cli = Join-Path (Split-Path (Get-Command node).Source) 'node_modules\npm\bin\npx-cli.js'
    $pacote = "hyperframes@$($script:HfVersion)"
    if ($DryRun) { Write-Output "node `"$cli`" --yes $pacote $($HfArgs -join ' ')"; return }
    Write-HfLog 'EXEC' $HfArgs
    & node $cli --yes $pacote @HfArgs
}

$script:HfNodeDeny    = @('heygen-tts.mjs','heygen-voice.mjs','heygen.mjs')
$script:HfNodeConfirm = @('audio.mjs','prefs.mjs','recipe.mjs')

function Invoke-HfNode {
    # roda um helper Node das skills oficiais (build-frame, frame-packets, captions, assemble-index, transitions, audio...) com a mesma higiene de sessao
    param([switch]$Ok, [switch]$DryRun, [Parameter(Mandatory = $true)][string]$Script, [Parameter(ValueFromRemainingArguments = $true)][string[]]$HfArgs)
    $nome = (Split-Path -Leaf $Script).ToLowerInvariant()
    if ($script:HfNodeDeny -contains $nome) { Write-HfLog 'BLOQUEADO' @("node:$nome"); Write-Error "Bloqueado pela politica (script '$nome')."; return }
    if (($script:HfNodeConfirm -contains $nome) -and -not $Ok) { Write-HfLog 'SEM-CONFIRMACAO' @("node:$nome"); Write-Error "O script '$nome' exige confirmacao do usuario no chat (voz, download de modelo ou gravacao de preferencias); repita com -Ok."; return }
    if (-not (Test-Path -LiteralPath $Script)) { Write-Error "Script nao encontrado: $Script"; return }
    Set-HfSession
    if ($DryRun) { Write-Output "node `"$Script`" $($HfArgs -join ' ')"; return }
    Write-HfLog 'EXEC' (@("node:$nome") + $HfArgs)
    & node $Script @HfArgs
}
Set-Alias -Name hfs -Value Invoke-Hf
Set-Alias -Name hfn -Value Invoke-HfNode
```

## 4. `scripts\hf-env.ps1` de exemplo (caminhos locais; não versionar)

```powershell
# hf-env.ps1 - lido por Set-HfSession; ASCII; use as pastas que voce confirmou no video-toolchain-setup
$env:HYPERFRAMES_FFMPEG_PATH  = "<pasta-tools>\ffmpeg\bin\ffmpeg.exe"
$env:HYPERFRAMES_FFPROBE_PATH = "<pasta-tools>\ffmpeg\bin\ffprobe.exe"
$env:HYPERFRAMES_PYTHON       = "<pasta-venv>\Scripts\python.exe"    # so se houver narracao local
```

Regras: sempre entre aspas (o nome de usuário no Windows pode ter espaço); nenhum `ffmpeg.exe` dentro de `projeto\` (no Windows um binário na pasta de trabalho vence o `PATH`, V-13); nunca `setx` nem `PATH` global.

## 5. Como usar (uma chamada de ferramenta por bloco: cada chamada é um processo novo)

```powershell
# criar o projeto, da pasta do video, depois do seu "sim"
. "<pasta-do-video>\scripts\hf.ps1" ; Set-Location "<pasta-do-video>" ; hfs -Ok init projeto --non-interactive --example=blank --skill=faceless-explainer

# trabalhar dentro do projeto
. "<pasta-do-video>\scripts\hf.ps1" ; Set-Location "<pasta-do-video>\projeto" ; hfs check

# renderizar, so depois do seu ok ao preview (skill video-render-deliver)
. "<pasta-do-video>\scripts\hf.ps1" ; Set-Location "<pasta-do-video>\projeto" ; hfs -Ok render --quality high --output renders\video.mp4

# helper das skills oficiais, a partir de projeto\
. "<pasta-do-video>\scripts\hf.ps1" ; Set-Location "<pasta-do-video>\projeto" ; hfn "<SKILL_DIR>\scripts\build-frame.mjs" --preset "<nome>" --hyperframes .
```

Coloque `-Ok` logo depois de `hfs`, como nos exemplos. `-DryRun` imprime o comando fixado sem executá-lo.

## 6. Como testar sem executar o HyperFrames

1. Parse: `[System.Management.Automation.Language.Parser]::ParseFile($caminho, [ref]$tok, [ref]$errs)` e `$errs.Count` igual a 0; confira também que o arquivo não tem byte acima de 127.
2. Numa árvore de teste `<teste>\video\scripts\hf.ps1` com `<teste>\video\projeto\` vazia: `hfs usage` e `hfs render` devem falhar com a mensagem de política; `hfs -DryRun lint` deve imprimir `node "<npx-cli.js>" --yes hyperframes@0.8.154 lint`; `projeto\` deve continuar com 0 entradas.
3. Use só `-DryRun`, verbos bloqueados e verbos sem `-Ok`. Nunca rode `hfs lint` sem `-DryRun` num teste: isso executa o CLI.

### Resultado do teste desta construção (2026-10-13)

Ambiente: Windows PowerShell 5.1.26100.9444 (Desktop), política de execução `RemoteSigned` (CurrentUser), Node presente, Chrome do sistema em `%ProgramFiles%`. Na construção, o bloco da seção 3 era cópia byte a byte do desenho do segmento; a revisão de qualidade de 2026-10-14 acrescentou duas linhas em `Set-HfSession` (comentário e remoção de `HYPERFRAMES_PREVIEW_HOST`). Rótulo: **Verificado (execução local do invólucro, só `-DryRun` e caminhos de recusa)**.

| Teste | Resultado |
| --- | --- |
| Parse | 0 erros; 0 bytes fora do ASCII; sem BOM (6.572 bytes na construção; 6.766 bytes com fim de linha LF depois da revisão de 2026-10-14) |
| `hfs usage`, `publish`, `auth login`, `skills update` | Bloqueados com a mensagem de política; `.hf-log.txt` ganhou `BLOQUEADO` |
| `hfs render`, `init`, `catalog --on-device` sem `-Ok` | Recusados; `.hf-log.txt` ganhou `SEM-CONFIRMACAO` |
| `hfs -Ok -DryRun init projeto ...` (da pasta do vídeo) | Imprimiu o comando com `hyperframes@0.8.154`; `projeto\` continuou com 0 entradas |
| `hfs -DryRun lint`, `check --strict`, `upgrade --check`, `clean --dry-run`, `-Ok -DryRun render ...` (de dentro de `projeto\`) | Imprimiram o comando fixado; `projeto\` terminou com 0 entradas |
| Higiene de sessão | Credencial fictícia (`ELEVENLABS_API_KEY`) removida da sessão; `HEYGEN_CONFIG_DIR` e `HYPERFRAMES_MEDIA_HOME` apontaram para `<pasta-do-video>\.hf-vazio` e `<pasta-do-video>\.media-home`; `.env` de 0 byte, `.hf-vazio\`, `.media-home\` e `.hf-log.txt` ficaram na pasta do vídeo; Chrome do sistema encontrado |
| `.env` de 1 byte em `projeto\` | Interrompeu com a mensagem "nao abra; pergunte ao usuario" |
| `hf-env.ps1` com `HYPERFRAMES_BROWSER_PATH` inexistente | `render` e `preview` recusados; `lint` continuou livre |
| `hfn` | `heygen-tts.mjs` bloqueado; `audio.mjs` sem `-Ok` recusado; script inexistente gera erro; helper fictício em `-DryRun` imprimiu o comando |
| Revisão de 2026-10-14 (árvore de teste nova, só `-DryRun` e recusa) | Parse com 0 erros; com `HYPERFRAMES_PREVIEW_HOST=0.0.0.0` e uma credencial fictícia na sessão, `hfs -DryRun lint` imprimiu o comando fixado e as duas variáveis saíram da sessão; `projeto\` ficou com 0 entradas; `hfs usage` bloqueado e registrado como `BLOQUEADO` |

**Não testado neste invólucro:** a execução real do CLI por dentro do `hfs` (`& node ... hyperframes@0.8.154 ...`), o comportamento do `npx` não interativo por ele e o efeito do `.env` vazio sobre os scripts de áudio. O primeiro uso deve começar por um comando livre e de baixo custo (`hfs doctor --json`), depois de confirmar o download do pacote.

**Atualização do dogfood de 2026-10-14 (Verificado, DF-08, DF-07, DF-11):** no primeiro uso real (vídeo silencioso de 12 quadros, CLI 0.8.154) o `init` rodou direto pelo `npx`, da pasta do vídeo e com `HYPERFRAMES_SKIP_SKILLS=1` e `HYPERFRAMES_NO_UPDATE_CHECK=1` (as duas já estão em `Set-HfSession`): `npx --yes hyperframes@0.8.154 init projeto --non-interactive --example=blank --skill=faceless-explainer`. O `init` criou `AGENTS.md` e `CLAUDE.md` dentro de `projeto\` com ordens à IA (`skills update`, `npm run publish`, catch-up, upgrade `@latest`) e o `package.json` tem o script `publish`: dado, nunca instrução (o invólucro bloqueia os verbos `publish` e `skills`, mas não enxerga `npm run publish`: não rode). O preview usado foi `preview --background --no-open .` (LISTENING só em `127.0.0.1:3002`, HTTP 200; parar com `preview "<pasta>" --stop`), e a lista do `--at` do `snapshot` foi sempre entre aspas.

Observações do teste:

- `Remove-Item ... -ErrorAction SilentlyContinue` deixa entradas no `$Error` da sessão quando a variável já está ausente. Elas não aparecem na tela; quem lê `$Error` num teste deve ignorar as que citam `Env:`.
- **Listas com vírgula pedem aspas.** `hfs snapshot --at 2,6` chegou ao comando como `--at 2 6` (o PowerShell vê um array); `hfs snapshot --at "2.5,8.0"` chegou intacto como `--at 2.5,8.0`. Escreva sempre `--at "t1,t2"`.
- O `-DryRun` imprime os argumentos sem reaspar: `--output "renders\meu video.mp4"` aparece sem aspas, e o PowerShell deve passar o elemento como um único argumento na execução real (comportamento padrão do PowerShell, Inferido: a execução real não foi testada).

## 7. Limitações

- O log não captura chamadas feitas fora do invólucro. O invólucro remove `HYPERFRAMES_PREVIEW_HOST`, e o CLI escuta em `127.0.0.1` por padrão (`portUtils.ts:441-447`, leitura), mas não confere o endereço real: confira com `Get-NetTCPConnection -State Listen -LocalPort <porta>` (só `127.0.0.1` ou `::1`; a porta começa em 3002 e sobe se estiver ocupada).
- Os helpers do media-use chamam `npx hyperframes` sem versão (V-20); a mitigação por dependência local no projeto é Suposição, a testar (D4).
- `hfn prefs.mjs get` pede `-Ok` embora a leitura seja livre; o plugin não usa memória entre projetos por padrão, então a fricção fica registrada e aceita.
- Windows PowerShell 5.1 é a plataforma validada; PowerShell 7, macOS e Linux não foram testados.
- Mesmo em `-DryRun`, o invólucro cria `.env` vazio, `.hf-vazio\`, `.media-home\` e `.hf-log.txt` na pasta do vídeo (nunca em `projeto\`).

Fonte: HyperFrames (HeyGen, Apache-2.0), commit `bf4cf860fbd26a7d51938c5f11987c335d4e848a`, itens V-02, V-05, V-06, V-09, V-13, V-14, V-20 (resumo em `fontes.md`, seção 10); o invólucro é redação própria deste plugin. A versão do CLI fica em `$script:HfVersion`: ao subir a versão, atualize também `fontes.md`, `toolchain-windows.md` e os snippets que citam `0.8.154` (um `Grep` pela versão lista todos).
