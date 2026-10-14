# Toolchain no Windows: CLI, FFmpeg, Chrome, invólucro e narração local

Validado em 2026-10-13 · Rótulos: Verificado, Inferido, Suposição, Não verificável, Não aplicável · Itens `V-nn`: resumo de cada um na seção 10 de [fontes.md](fontes.md) (conferência por leitura de arquivo no commit; o **dogfood de 2026-10-14** acrescentou observação de execução real, itens `DF-nn` na seção 12 de [fontes.md](fontes.md): `init`, `check`, `snapshot`, `render` e `preview` rodaram; **narração e Parakeet continuam nunca executados**) · Redação própria · Plataforma-alvo: Windows 11 com PowerShell; macOS e Linux não validados (D13).

## Sumário

1. Versão fixada e fonte única
2. Requisitos e opção menos invasiva
3. Como obter o CLI e as skills oficiais
4. Invólucro `hfs` e `hfn`
5. FFmpeg e ffprobe
6. Chrome
7. `doctor` por checks nomeados
8. PowerShell, Git Bash e processos
9. Rede, caches e portas
10. Narração local em PT-BR
11. O que não instalar
12. Gotchas

## 1. Versão fixada e fonte única

Este arquivo e [fontes.md](fontes.md) são a **fonte única** das constantes de versão. Em snippets, prompts e no invólucro elas aparecem como cópias literais que se atualizam juntas: `Grep` por `0.8.154` lista todas.

| Constante | Valor | Origem |
| --- | --- | --- |
| CLI do HyperFrames | `hyperframes@0.8.154` (plugin oficial 0.8.154: `plugin.json:5`, `packages/cli/package.json:3`) | V-20 |
| Commit das skills oficiais | `bf4cf860fbd26a7d51938c5f11987c335d4e848a` em `heygen-com/hyperframes` | relatório de validação; conferido no clone (`git rev-parse HEAD`) |
| Chrome gerenciado | `chrome-headless-shell 152.0.7977.30` (`manager.ts:51`) | V-14 |
| GSAP no compilador | 3.15.0 (`gsapCdn.ts:1`); a documentação cita 3.14.2 | V-19, V-52 |
| Pacotes opcionais | `sherpa-onnx-node@1.13.8`, `onnxruntime-node@1.21.1`, `@google/genai@1.52.0` | V-17 |
| Parakeet TDT 0.6B v3 (int8) | revisão `2bda32ec70b097a55adaa07d9a7173915b43cc78`, 670.478.772 bytes | V-25 |
| Kokoro | modelo cerca de 311 MB e vozes cerca de 27 MB, de `kokoro-onnx` (release `model-files-v1.0`) | V-23 |
| Node | 22 ou superior (`packages/cli/package.json:85-87`) | V-12 |
| Data de conferência | 2026-10-13 | este arquivo |

**Revalidação quando a versão do CLI subir:** (1) leia o `plugin.json` do plugin oficial e confira a versão; (2) refaça a leitura dos itens sensíveis à versão: V-09 (`init`), V-14 e V-15 (Chrome e `doctor`), V-18 e V-19 (qualidades e rede), V-20 (launcher), V-21 (verbos), V-23 e V-25 (vozes e tamanhos), V-41 (pipeline do faceless), V-53 (lint de `clip`); (3) atualize as constantes acima e em `fontes.md` e rode `Grep` por `0.8.154`; (4) registre a nova data. Até lá, números de terceiros (tamanhos, versões, limites de 200 MB) valem como lidos no commit.

## 2. Requisitos e opção menos invasiva

"Referência" é o estado informado pelo dono em 2026-10-13 (não verificado pelos pesquisadores); o `video-env-preflight` mede o estado real.

| Item | Referência | Opção recomendada | Alternativa | Evidência |
| --- | --- | --- | --- | --- |
| Node 22+ | 24.15 | nada | — | V-12 |
| npm e npx | 11.12.1 | nada; o launcher no Windows precisa de `npx-cli.js` ao lado do `node.exe` ou em `npm_execpath` | `npx --yes hyperframes@0.8.154` direto | V-20 |
| Bun | ausente | não instalar (só serve ao build do repositório) | — | V-12 |
| FFmpeg e ffprobe | ausentes | build portátil de 64 bits em `<tools>\ffmpeg\...\bin`, variáveis só na sessão, download confirmado | `.hyperframes\bin\` no projeto (exige cwd = projeto); `winget` (altera o sistema: evitar); `@ffmpeg-installer/*` (binários antigos) | V-13 |
| Chrome | `C:\Program Files\Google\Chrome\Application\chrome.exe` | `HYPERFRAMES_BROWSER_PATH` apontando para esse arquivo, após `Test-Path` | `browser ensure` (download, tamanho Não verificável) | V-14 |
| Python | 3.14 presente | venv dedicado + `HYPERFRAMES_PYTHON`; compatibilidade de `kokoro-onnx` com 3.14: Não verificável | Python 3.10 a 3.12 em venv (instalação extra) ou vídeo silencioso | V-23 |
| espeak-ng | ausente | não instalar de início; testar a voz `p*` antes | instalador externo, com confirmação | V-23 |
| Modelo Kokoro | não baixado | baixado pelo próprio `tts` na 1ª execução, com confirmação | — | V-23 |
| Tempos por palavra | nenhum motor | Parakeet (`models install parakeet`) | legendas desligadas e durações pela voz | V-25 |
| Git e Git Bash | presentes | usar o Bash para snippets bash do upstream | — | V-41 |
| cmake, compilador C | ausentes | não instalar | — | V-25 |
| Credenciais HeyGen, ElevenLabs, Gemini | ausentes | manter ausentes | — | V-06 |
| Docker | ausente | não necessário | — | V-18 |
| Rede no render | necessária | `cdn.jsdelivr.net` (GSAP) **e Google Fonts (todas as fontes, inclusive as "embutidas")**, com cache de fontes fora do projeto em `~\.cache\hyperframes\fonts\` | render offline: rodar uma vez online (Inferido) ou `@font-face` local (Não verificado) | V-19, DF-01 |
| Disco, RAM, GPU | não verificados | `doctor` (checks Disk e Memory) antes de baixar; reserve mais de 1,2 GB para Kokoro, Parakeet e caches | — | Não verificável |
| Pasta do vídeo | a definir | fora de árvores com `.env`; caminhos sempre entre aspas | — | V-05, V-76 |

## 3. Como obter o CLI e as skills oficiais

**Skills oficiais (D5), nesta ordem:** (1) a sessão lista a skill `hyperframes:hyperframes`? Então o plugin oficial existe e o launcher fica em `<raiz-do-plugin>\skills\hyperframes\scripts\plugin-cli.mjs`; (2) senão, o usuário informa o caminho de um clone (`skills\` do clone) no commit fixado; (3) senão, diga que faltam as skills oficiais, mostre as duas opções e pare na decisão dependente. Instalar o plugin ou clonar é download/configuração: confirmação com nome, origem e destino. Clone em pasta fora do projeto.

**Comando de instalação do plugin oficial (lido no README oficial em 2026-10-13 via WebFetch; Verificado como leitura, não executado):**

```text
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
```

A mesma seção do README manda `npx hyperframes skills update` para agentes: recuse (V-09, [seguranca-e-privacidade.md](seguranca-e-privacidade.md)). Copie sempre o comando do README vigente; este vale como lido na data.

**CLI (V-20, Verificado em `plugin-cli.mjs:9-89` e `plugin-installation.md`):**

| Via | Como | Observação |
| --- | --- | --- |
| Launcher do plugin oficial | `node "<raiz-do-plugin>\skills\hyperframes\scripts\plugin-cli.mjs" <verbo>` | exige manifesto com `name: "hyperframes"`; bloqueia o verbo `skills`; exporta `HYPERFRAMES_SKIP_SKILLS=1` e `HYPERFRAMES_NO_UPDATE_CHECK=1`; roda `npx --yes hyperframes@<versão do manifesto>`; no Windows usa `npx-cli.js` via `node`, sem shell. `--script <caminho>` roda um helper Node com o mesmo ambiente |
| `npx` pinado | `npx --yes hyperframes@0.8.154 <verbo>` com as variáveis de sessão na mesma chamada | caminho padrão do invólucro `hfs` |
| Dependência local | `npm install --save-dev hyperframes@0.8.154` no projeto, com confirmação | mitiga os helpers do media-use que chamam `npx hyperframes` sem versão. **Suposição, a testar** |

Regras: rode no diretório do projeto, nunca no do plugin (somente leitura); a 1ª chamada pode baixar aquela versão exata para o cache do npm; falha de download não autoriza `latest`. O pin cobre só o CLI (V-48 #8). Não copie a árvore `skills/hyperframes` para outro plugin: o launcher quebra (nome diferente de `hyperframes`).

## 4. Invólucro `hfs` e `hfn`

O template `hf-sessao.ps1.md` (em `assets/templates/`) traz o `hf.ps1` como bloco de código: o plugin não contém arquivo `.ps1`. O usuário copia para `<pasta-do-video>\scripts\hf.ps1`, **fora de `projeto/`**.

| Função | O que faz |
| --- | --- |
| `hfs <verbo> ...` | roda `npx --yes hyperframes@0.8.154 <verbo>` depois de aplicar a higiene de sessão; bloqueia os verbos proibidos; exige `-Ok` nos verbos de confirmação (`init`, `add`, `browser`, `models`, `tts`, `transcribe`, `remove-background`, `render`, `upgrade` sem `--check`, `clean` sem `--dry-run`, `catalog --on-device`); barra `render` e `preview` sem `HYPERFRAMES_BROWSER_PATH` válido |
| `hfn <script.mjs> ...` | roda um helper Node das skills oficiais (`build-frame`, `frame-packets`, `captions`, `assemble-index`, `transitions`, `audio`) com a mesma higiene; bloqueia os scripts de login da HeyGen; `audio.mjs`, `prefs.mjs` e `recipe.mjs` exigem `-Ok` |
| `Set-HfSession` | variáveis da seção 5 de [seguranca-e-privacidade.md](seguranca-e-privacidade.md); remove nomes de credencial; cria `.env` vazio, `.hf-vazio` e `.media-home` na pasta do vídeo; acha o Chrome do sistema; lê `scripts\hf-env.ps1` (FFmpeg, ffprobe, Python), que não deve ser versionado |
| `-DryRun` | imprime o comando fixado sem executar (cria mesmo assim os arquivos da higiene na pasta do vídeo) |

Uso numa única chamada de ferramenta (cada chamada é um processo novo):

```powershell
. "<pasta-do-video>\scripts\hf.ps1"; Set-Location "<pasta-do-video>\projeto"; hfs lint
```

Teste do invólucro (Verificado pelo crítico em 2026-10-13, Windows PowerShell 5.1, árvore de teste, **só em `-DryRun`**; execução real do CLI **não testada**): parse com 0 erros e 0 bytes fora do ASCII; `hfs usage` bloqueado; `hfs render` sem `-Ok` recusado; `hfs -DryRun lint` de dentro de `projeto/` deixa `projeto/` com 0 entradas; `.env` não vazio interrompe com a mensagem de política; `.hf-log.txt` registra BLOQUEADO e SEM-CONFIRMACAO. Repita o parse e o `-DryRun` depois de copiar.

Limites: o log não captura chamadas feitas fora do invólucro; o invólucro não lê o endereço de escuta do preview (ele remove `HYPERFRAMES_PREVIEW_HOST` da sessão, e o padrão do CLI é `127.0.0.1`), então confira com `Get-NetTCPConnection`; o `-Ok` é fricção, quem autoriza é o usuário no chat; os helpers do media-use continuam chamando `npx hyperframes` sem versão (D4).

**Layout (D10, Inferido de V-09 e V-38):** o `init` recusa pasta com **qualquer** entrada, inclusive dotfiles (`init.ts:842-845`, `readdirSync(destDir).length > 0`). Por isso insumos e arquivos do invólucro ficam na pasta do vídeo, e o `init projeto ...` roda dela; o `BRIEF.md` é a primeira escrita dentro de `projeto/`, logo depois do `init`.

## 5. FFmpeg e ffprobe (V-13, Verificado)

- Variáveis: `HYPERFRAMES_FFMPEG_PATH` e `HYPERFRAMES_FFPROBE_PATH`. Nenhum código de render lê `FFMPEG_PATH`.
- Ordem real (`ffBinaries.ts:192-202,132-156`): (1) a variável, resolvida direto e **sem checar existência** (só o `doctor` exige que exista); (2) no Windows, o diretório de trabalho **antes** do PATH; (3) `.hyperframes\bin\` relativo ao cwd; (4) pacote `@ffmpeg-installer/*` (binários antigos). Consequência: um `ffmpeg.exe` na pasta do projeto vence o PATH; mantenha binários fora do projeto e defina a variável.
- Exigem FFmpeg: render, probe de mídia, transcodificação de TTS em nuvem e a duração no motor de áudio. O `doctor` checa os dois binários.
- Instalação sugerida pelo próprio CLI no Windows: `winget install --id Gyan.FFmpeg -e` ou build de ffmpeg.org com `bin/` no PATH. O plugin evita as duas (alteram o sistema). Opção do plugin: build portátil em pasta do usuário; origem, tamanho e integridade **Não verificáveis aqui**. Fluxo: o usuário escolhe a origem e cola o hash publicado; `Get-FileHash -Algorithm SHA256 "<arquivo>"` compara; extraia em `<tools>\ffmpeg\...\bin`; prove com `& "<caminho>\ffmpeg.exe" -version`; grave as variáveis em `scripts\hf-env.ps1`.
- Caminhos com espaço funcionam: o spawn usa array de argumentos e `windowsHide` (`runFfmpeg.ts:155-159`); nos comandos do agente, sempre entre aspas.

## 6. Chrome (V-14, Verificado)

- `render` e `preview` chamam `ensureBrowser({ preferManagedChrome: true })`: ordem `HYPERFRAMES_BROWSER_PATH` (só se o arquivo **existir**) → cache próprio → **download automático** do `chrome-headless-shell 152.0.7977.30`. O Chrome do sistema é ignorado. O CLI mostra o progresso, mas não pergunta.
- `check`, `layout`, a captura de frames (`snapshot`: Inferido) e `beats` usam `ensureBrowser()` sem essa opção: variável → cache → Chrome do sistema → download. `findSystemBrowser` testa `Program Files\Google\Chrome\Application\chrome.exe`, a versão `(x86)` e `%LOCALAPPDATA%`.
- Com Chrome comum (não headless-shell) a captura cai para screenshot, mais lenta; "any Chrome build works". Efeito na qualidade e no tempo: **Não verificável**.
- Crash conhecido do headless-shell no Windows (0xC0000409 / 3221225595): remediação oficial é `HYPERFRAMES_BROWSER_PATH` para o Chrome instalado.
- Política: antes de `render` ou `preview`, `Test-Path -LiteralPath $env:HYPERFRAMES_BROWSER_PATH` verdadeiro. Arquivo inexistente é ignorado em silêncio e o render baixa Chrome. `browser ensure` e qualquer download: confirmação com origem (CDN do `@puppeteer/browsers`) e tamanho (Não verificável).

## 7. `doctor` por checks nomeados (V-15, Verificado)

`doctor --json` sai sempre com código 0 e traz `ok = todos os checks`. Na máquina de referência `ok` será `false` por Docker, Kokoro, MusicGen, whisper e "atualização disponível". O Chrome do `doctor` aceita o do sistema e diverge do render (seção 6). **Gate correto:** ler `checks[]` e exigir `ok: true` apenas em Node.js, FFmpeg, FFprobe e Chrome.

```powershell
. "<pasta-do-video>\scripts\hf.ps1"; Set-Location "<pasta-do-video>\projeto"
$r = (hfs doctor --json) | ConvertFrom-Json
$r.checks | Format-List *      # inspecione os nomes reais dos campos antes de filtrar
```

Os nomes exatos dos campos de cada item de `checks[]` **não foram verificados**: leia o JSON real. Sem `jq` no Windows, use `ConvertFrom-Json`. O `doctor` executa `ffmpeg -version` e `chrome --version` (locais); a checagem de versão usa o cache do update check. A 1ª chamada do CLI baixa o pacote para o cache do npm: sem evidência de que ele já está lá, conte como download pendente e peça confirmação antes.

## 8. PowerShell, Git Bash e processos (V-41, V-76)

- No Claude Code para Windows há duas ferramentas de shell, `Bash` (Git Bash) e `PowerShell` (Verificado no ambiente do crítico em 2026-10-13). O upstream escreve snippets bash. Tradução:

| Upstream | No Windows |
| --- | --- |
| `cmd ... &` (segundo plano) | `run_in_background` da ferramenta, ou `Start-Process`; espere pelo artefato em disco |
| `for b in ...; do ...; done` | `foreach ($b in ...) { ... }` |
| `test -s arquivo` | `(Test-Path -LiteralPath $a) -and ((Get-Item -LiteralPath $a).Length -gt 0)` |
| `$PROJECT_DIR`, `<SKILL_DIR>`, `<MEDIA_DIR>` | substituições do agente, caminhos absolutos entre aspas |
| `npx hyperframes ...` | `hfs ...` (invólucro) |

- Cada chamada de ferramenta é um processo novo: variáveis na mesma chamada que roda o CLI (Inferido do harness).
- Caminhos com espaço no nome de usuário não quebram o engine (spawn por array), mas quebram comando sem aspas. Caminho UNC gera aviso do `doctor`. Comportamento real de caminhos longos em `check`, `snapshot` e `render`: Não verificável.
- Artefatos de verificação: `ffprobe` com `& $env:HYPERFRAMES_FFPROBE_PATH ...` exige a variável definida na mesma chamada.

## 9. Rede, caches e portas

- A compilação de `render` **e de `check`** busca o GSAP em `cdn.jsdelivr.net` (timeout de 15 s; falha: "The render may fail if this script is required"). É GET público sem dado do usuário (V-19, V-04). Render offline completo: Não verificável; GSAP não é vendorizável (V-75). O `index.html` do `init` aponta para `gsap@3.14.2` (DF-04): use essa mesma URL e versão em todos os quadros.
- **Fontes exigem rede (Verificado, dogfood 2026-10-14, DF-01).** As 18 famílias "embutidas" **não são bundle local** nesta versão do CLI: no `check`, no `snapshot` e no `render` o compilador baixa as faces do Google Fonts (11 de Montserrat e 10 de JetBrains Mono no caso real) e grava cache **fora do projeto**, em `~\.cache\hyperframes\fonts\` (pastas `montserrat\` e `jetbrains-mono\`), além de `~\.cache\hyperframes\history\`. É acesso de rede do render (ao lado do GSAP no jsdelivr) e escrita fora do projeto (cache de ferramenta, sem dado do usuário). Para render 100% offline: rodar uma vez online para popular o cache (**Inferido**) ou embutir `@font-face` local (**Não verificado**). Outra família Google também é buscada em tempo de build (aviso `font_family_without_font_face`); fonte instalada no sistema é capturada em render local.
- Caches: `~\.cache\hyperframes\{chrome,tts,whisper,optional,fonts,history}`, `~\.hyperframes\` (V-08, DF-01; tabela completa em [seguranca-e-privacidade.md](seguranca-e-privacidade.md)).
- Preview: Studio local; abre o navegador sozinho; usa Chrome gerenciado (V-18, V-21). **Endereço (Verificado por leitura em 2026-10-14, `packages/cli/src/server/portUtils.ts:23,441-447`):** escuta em `127.0.0.1` por padrão; `HYPERFRAMES_PREVIEW_HOST` troca o endereço, e o comentário do código avisa que a API do Studio lê, grava e apaga arquivos do projeto e dispara render sem autenticação; por isso a variável fica fora da sessão. **Porta:** começa em 3002 e, se estiver ocupada, o CLI tenta as seguintes (até 100): leia a porta real na saída do `preview`. Confira HTTP 200 em `http://127.0.0.1:<porta>` e a escuta com `Get-NetTCPConnection -State Listen -LocalPort <porta>` (`LocalAddress` `127.0.0.1` ou `::1`; se `0.0.0.0` ou `::`, pare). **Em execução (Verificado, dogfood 2026-10-14, DF-07):** `preview --background --no-open .` subiu em `127.0.0.1:3002` (`netstat`: LISTENING só em `127.0.0.1`) e respondeu HTTP 200; o log fica em `~\.local\state\hyperframes\previews\` (fora do projeto); para parar, `preview "<pasta>" --stop`. Mesmo assim, confira a escuta a cada vez.
- Engine no Windows (V-18): streaming-encode desliga sozinho só com win32, GPU de software forçada, `workers` igual a 1 e sem escolha do usuário; `drawElement` é padrão em win32 com GPU de hardware; modo de pouca memória é automático pela RAM. Efeitos práticos: Não verificáveis.

## 10. Narração local em PT-BR

**Estado: PT-BR ponta a ponta nunca foi executado (L1 a L4). Qualquer promessa de qualidade é indevida.** O caminho padrão recomendado para explicativos é vídeo silencioso com texto na tela (D6).

**Kokoro (V-23, Verificado no código):** Node chama `execFileSync(python, [script, modelo, vozes, texto, voz, velocidade, saída, idioma])` com `kokoro_onnx` e `soundfile`. O Python vem de `HYPERFRAMES_PYTHON` (valida `--version` com "Python 3") e depois de `where python3`/`where python`; override rejeitado cai em silêncio para o PATH. Versão: o código diz 3.10 ou superior (a documentação diz 3.8+, defasada); `kokoro-onnx` com Python 3.14: Não verificável.

**Vozes:** o prefixo da voz define o idioma e `p` é pt-br. As 12 vozes embutidas não incluem nenhuma `p*`; a única voz portuguesa citada no repositório é `pf_dora`, como fixture de teste (`manager.test.ts:20`). `pm_alex` e `pm_santa` não aparecem no repositório (nomes do Kokoro upstream: Suposição). A documentação fala em 54 vozes e o código aceita qualquer ID válido. Confirme tocando `tts --list` e testando a voz depois do download; a sintaxe do `tts` deve ser conferida na ajuda do CLI e em `tts.md` (não validada aqui). `--speed`: 0.7 a 0.8 tutorial, 1.0 padrão, 1.1 a 1.2 intros. Sem timestamps por palavra.

**espeak-ng:** a documentação diz "system-wide" para texto não inglês, com instruções só para `brew` e `apt`; nenhum código checa a presença e não há caminho de instalação para Windows. Não instale de início; teste a voz `p*`; instale só se o erro apontar, com confirmação.

**Instalação (tudo com confirmação):** `python -m venv <pasta>` → `<venv>\Scripts\python.exe -m pip install kokoro-onnx soundfile` (só dentro do venv) → `HYPERFRAMES_PYTHON` no `hf-env.ps1` → modelo baixado pelo `tts` na 1ª execução (cerca de 311 MB mais 27 MB em `~\.cache\hyperframes\tts`) → teste de uma frase com sigla e número, ouvindo o resultado, antes do roteiro inteiro. Se o `pip` falhar no Python 3.14, reporte e ofereça Python 3.10 a 3.12 em venv ou vídeo silencioso.

**Wrapper do faceless não suporta PT-BR sem ajuste (V-24, Verificado):** o `audio.mjs` do faceless fixa `provider: "auto"` e `lang` efetivo `"en"`; aceita `--hyperframes --storyboard --script --out --voice --speed --tts-model --style`, **sem** `--lang` nem `--provider`. Efeitos: (1) sem `--voice` a voz é `am_michael` (inglesa); com `--voice p*` a síntese funciona porque o CLI infere o idioma pelo prefixo; (2) a transcrição de tempos usa `small.en` quando Parakeet não está instalado; (3) qualquer credencial presente muda o provedor.

**Arquitetura do áudio PT-BR (decisão pendente, L2):** (a) wrapper oficial com `--voice` de prefixo `p`, Parakeet instalado e higiene total de credenciais; (b) chamar o motor do media-use direto (`--provider kokoro --lang pt-br --voice ... --only tts`) e converter o meta neutro para o formato do wrapper; (c) gerar o áudio por `tts` e escrever o `audio_meta.json` à mão. Recomendação provisória (**Inferido**): (a), porque mantém o pipeline oficial; fallback (b), que torna a privacidade explícita em vez de higiênica. Decidir depois do teste real.

**Transcrição (V-25, Verificado):** `transcribe --engine auto` usa Parakeet se instalado e se cobre o idioma (cobre `pt`), senão Whisper. Parakeet: `models install parakeet`, Windows x64 suportado (sherpa-onnx), 670.478.772 bytes com SHA-256 fixados mais `sherpa-onnx-node`; licença do modelo CC-BY-4.0 (atribuição obrigatória ao citá-lo). Whisper no Windows procura `HYPERFRAMES_WHISPER_PATH` ou o PATH e senão **faz `git clone` e compila com cmake**: evite. Sem Parakeet, não rode `transcribe` nem `audio.mjs` com TTS local; alternativa: legendas desligadas e durações pela voz. Qualidade PT-BR de Parakeet contra Whisper: Não verificável.

**Música e efeitos (V-29, V-30):** no faceless, sem credencial HeyGen a BGM é **pulada** (`retrieve` explícito sem fallback local); use `music: none`. SFX: 19 `.mp3` da Pixabay no repositório (licença Pixabay: uso comercial e não comercial, sem atribuição; permitida a redistribuição em obras derivadas como vídeos renderizados); não os copie para este plugin. Com credencial HeyGen o `fetch-sfx` busca na HeyGen (revisão do caso real, Inferido): mais um motivo para a sessão higienizada. **Executado (Verificado, dogfood 2026-10-14, DF-05):** sem `SCRIPT.md` e com `music: none`, `audio.mjs` gravou `audio_meta.json` vazio; `audio.mjs fetch-sfx` resolveu 15 cues pela biblioteca local (13 `.mp3` copiados para `projeto\assets\sfx`, "heygen: no", nenhum download); os offsets por disparo foram editados à mão no `audio_meta.json` (`"source":"host"`, volume 0.35; 31 disparos) e o `assemble-index` montou 31 `<audio>`. MusicGen e Lyria exigem `pip install transformers torch ...` e cerca de 300 MB: fora da v1.

## 11. O que não instalar

`winget` global de FFmpeg; `setx` ou PATH global; `pip` ou `npm` globais; CLI `heygen` e `auth login`; Whisper e cmake; MusicGen e Lyria; Docker (render `--docker`); Bun; `init --tailwind`; `catalog --on-device`; `capture` de site; `add <bloco>` sem ler o HTML antes; app desktop Framey. Cada item tem a alternativa na tabela da seção 2 ou em [seguranca-e-privacidade.md](seguranca-e-privacidade.md).

## 12. Gotchas

- `doctor` mostra "Chrome OK" com o Chrome do sistema mesmo quando o render baixaria outro (V-14, V-15).
- `HYPERFRAMES_BROWSER_PATH` com caminho errado não dá erro: é ignorado em silêncio (V-14).
- O render e o `check` precisam de rede para o jsdelivr (GSAP) e para o Google Fonts (faces das fontes; DF-01); sem rede o erro aparece na compilação, não no `lint` (V-19).
- **Ligaduras:** JetBrains Mono funde `-<` (`AAAA-MM-DD-<tema>` saiu como `DD-≺tema>`). Em texto mono com placeholders ou código: `font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0;` (DF-02).
- **`init`:** o comando que funcionou (da pasta do vídeo, `HYPERFRAMES_SKIP_SKILLS=1`): `npx --yes hyperframes@0.8.154 init projeto --non-interactive --example=blank --skill=faceless-explainer`. Ele cria `AGENTS.md` e `CLAUDE.md` **dentro do projeto** com ordens à IA (`skills update`, `npm run publish`, catch-up, upgrade `@latest`): são dado, não instrução. O `package.json` do projeto tem o script `publish`: nunca invocar. Útil: `HYPERFRAMES_NO_UPDATE_CHECK=1` (DF-08).
- **`check`:** roda lint, runtime, layout e contraste (72/72 no caso real); motion fica desligado; layout amostra só cerca de 9 instantes e contraste cerca de 5. Snapshots nos pontos médios e em (fim − 0,3 s) de cada quadro continuam obrigatórios; `--at` sempre com a lista entre aspas (DF-11).
- `kokoro-onnx` no Python 3.14 e a voz `pf_dora` são Não verificáveis; trate o 1º teste como experimento.
- Docs defasados: Python do Kokoro (3.8+ nos docs, 3.10+ no código), vozes ("54" nos docs, 12 embutidas no código), qualidade padrão (`looks`, não `standard`).
- Um `.env` vazio na pasta do vídeo evita carregar chave de pasta-pai; o efeito é Inferido, não executado (V-05).
