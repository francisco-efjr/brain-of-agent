# Ferramentas, hooks e MCP recomendados (todos desativados)

Validado em 2026-10-13 · Rótulos: Verificado, Inferido, Suposição, Não verificável · Itens `V-nn`: resumo de cada um na seção 10 de [fontes.md](fontes.md) · Documentação do Claude Code lida em 2026-10-13 via WebFetch: https://code.claude.com/docs/en/hooks e https://code.claude.com/docs/en/permissions (resumo feito por modelo pequeno; reconfira antes de adotar).

Política do plugin: nada deste arquivo está ativo. O plugin não contém `hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `bin/` nem arquivo executável. Cada item traz o texto ou JSON pronto para o usuário copiar conscientemente, o risco e a fonte. Hooks e servidores MCP rodam com as permissões do usuário e não são fronteira de segurança. Nada aqui recomenda `--dangerously-skip-permissions`: use a lista de permissões do projeto e, para conteúdo não confiável, sandbox.

## Sumário

1. Resumo e ordem de adoção
2. Plugin oficial do HyperFrames e clone das skills
3. CLI fixado e dependência local
4. Regras `permissions.deny`
5. Hook `PreToolUse`
6. Invólucro `hf.ps1`
7. Painel de navegador e Playwright MCP
8. Validar este plugin
9. TTS em nuvem
10. Itens que não devem ser adotados
11. Gotchas

## 1. Resumo e ordem de adoção

| # | Item | Para quê | Risco e ressalva | Fonte | Ativar? |
| --- | --- | --- | --- | --- | --- |
| 1 | Plugin oficial `hyperframes@hyperframes` | 21 skills, roteador `/hyperframes:hyperframes`, launcher que fixa o CLI | Altera a configuração do usuário; o conteúdo das skills muda sem nova versão; as skills mandam `usage`, `feedback`, `skills update` e divulgar o app: a política vence | V-09, V-11, V-20 | Com confirmação |
| 2 | Clone das skills no commit fixado, fora do projeto | Alternativa sem instalar plugin | É download (confirmar); ler como referência; helpers por `hfn` | V-20, DECISOES do dono | Com confirmação |
| 3 | `npx --yes hyperframes@0.8.154` | CLI fixado | Executa código de terceiros do npm; cache no npm | V-17, V-20 | Padrão do invólucro |
| 4 | Dependência local `npm install --save-dev hyperframes@0.8.154` | Fixar os helpers do media-use | **Suposição, a testar**; scripts das dependências não verificados | V-20 | Opcional |
| 5 | Regras `permissions.deny` do projeto | Garantia sem script | Padrões não testados no Claude Code; não é fronteira | permissions (seção 4) | Recomendado, depois de testar |
| 6 | Hook `PreToolUse` com matcher `Bash\|PowerShell` | Garantia parcial mesmo se o upstream mandar | Roda com suas permissões; regex sobre texto não é fronteira | hooks (seção 5), V-11 | Após ler o script |
| 7 | Invólucro `hf.ps1` (template TP-06) | Higiene de sessão, bloqueio, registro | Fricção; só testado em parse, bloqueio e `-DryRun` | [toolchain-windows.md](toolchain-windows.md) | Sim, é o padrão do plugin |
| 8 | FFmpeg e ffprobe portáteis; Chrome do sistema; venv com `kokoro-onnx`; Parakeet | Render, ffprobe, narração local | Downloads e instalações com confirmação; origem e hash do FFmpeg Não verificáveis | V-13, V-14, V-23, V-25 | Sob demanda |
| 9 | Painel de navegador ou Playwright MCP | Olhar o preview em `127.0.0.1` | Opcional; `snapshot` basta | seção 7 | Opcional |
| 10 | `claude plugin validate`, `tools/verify_plugin.py`, `claude plugin eval` | Validar este plugin | `eval` consome cota e exige Claude Code 2.1.269 ou superior | foundation | Sim; eval com custo ciente |
| 11 | TTS em nuvem (HeyGen, ElevenLabs, Gemini) | Opt-in explícito | O texto do roteiro sai da máquina; custos e termos Não verificáveis | V-06, V-26 | Só a pedido |

## 2. Plugin oficial do HyperFrames e clone das skills

Comando de instalação do plugin lido no README oficial em 2026-10-13 (Verificado como leitura; **não executado**; o plugin não instala nada sozinho):

```text
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
```

O README trata `npx skills add heygen-com/hyperframes` para outros agentes e manda `npx hyperframes skills update` para execuções não interativas: ambos entram na lista proibida (instalam skills globais, V-09). Copie sempre o comando do README vigente e registre a data. Antes de instalar, ofereça a triagem de risco do plugin `security-appsec` (`agent-risk-triage`).

Alternativa sem instalar: clone `heygen-com/hyperframes` no commit `bf4cf860fbd26a7d51938c5f11987c335d4e848a` em pasta **fora** do projeto; o plugin só lê `skills\` do clone como referência e roda helpers por `hfn`. O launcher do plugin oficial exige manifesto com `name: "hyperframes"` e quebra se a árvore for copiada para outro plugin (V-20).

## 3. CLI fixado e dependência local

`npx --yes hyperframes@0.8.154 <verbo>` (ou `hfs`). Nunca `@latest`; falha de download não autoriza outra versão. Os helpers do media-use chamam `npx hyperframes` sem versão; a mitigação `npm install --save-dev hyperframes@0.8.154` no projeto, com confirmação, é **Suposição a testar** (o comportamento do `npx` não interativo e os scripts de instalação das dependências não foram verificados). O pacote do CLI não declara `postinstall` (Inferido de `package.json`, V-17).

## 4. Regras `permissions.deny`

**Sintaxe (Verificado na documentação de permissões em 2026-10-13):** regras em `permissions.deny` de `.claude/settings.json` (projeto), `.claude/settings.local.json` (local) ou `~/.claude/settings.json` (usuário); `*` casa qualquer sequência em qualquer posição; o espaço antes de um `*` final faz parte da regra (`ls *` não casa `lsof`; `ls*` casa) e, quando é o único curinga, o `*` final também casa o comando sem argumentos; a ordem de avaliação é deny, ask, allow e um `deny` amplo não admite exceção por `allow`; regras `PowerShell(...)` têm a mesma forma das `Bash(...)`, são case-insensitive e canonicalizam aliases de cmdlet; a documentação afirma que uma regra de `deny` cobre a forma usual do comando e **não é fronteira de segurança** (outra forma de invocar o mesmo programa, como `sh -c '...'` ou o caminho completo, pode escapar). Uma regra `deny` com nome de ferramenta desconhecido gera aviso na inicialização, o que ajuda a pegar erro de digitação.

**Padrões (Suposição: não testados no Claude Code).** Salve em `<pasta-do-video>\.claude\settings.json` e abra a sessão nessa pasta. Para o Git Bash, repita as mesmas linhas trocando `PowerShell(` por `Bash(`.

```json
{
  "permissions": {
    "deny": [
      "PowerShell(*hyperframes* usage*)",
      "PowerShell(*hyperframes* feedback*)",
      "PowerShell(*hyperframes* publish*)",
      "PowerShell(*hyperframes* cloud*)",
      "PowerShell(*hyperframes* lambda*)",
      "PowerShell(*hyperframes* cloudrun*)",
      "PowerShell(*hyperframes* auth*)",
      "PowerShell(*hyperframes* skills*)",
      "PowerShell(*hyperframes* telemetry*)",
      "PowerShell(*plugin-cli.mjs* usage*)",
      "PowerShell(*plugin-cli.mjs* feedback*)",
      "PowerShell(*plugin-cli.mjs* publish*)",
      "PowerShell(*plugin-cli.mjs* cloud*)",
      "PowerShell(*plugin-cli.mjs* lambda*)",
      "PowerShell(*plugin-cli.mjs* cloudrun*)",
      "PowerShell(*plugin-cli.mjs* auth*)",
      "PowerShell(*plugin-cli.mjs* telemetry*)",
      "PowerShell(npx skills add*)",
      "PowerShell(*heygen auth*)",
      "PowerShell(npm install -g*)",
      "PowerShell(npm i -g*)",
      "PowerShell(setx *)",
      "PowerShell(winget install*)"
    ]
  }
}
```

**Teste seguro:** peça ao Claude para rodar `Write-Output "hyperframes usage"`. Se a regra funcionar, o comando é negado sem executar nada do HyperFrames. Nunca teste com o verbo real. As flags antes do verbo (`hyperframes --flag usage`) são cobertas porque `*` casa qualquer trecho, mas falsos positivos são possíveis (um `grep` com essas palavras); libere caso a caso.

## 5. Hook `PreToolUse`

**Contrato (documentar, não ativar):** evento antes de comando de shell; ação: negar e explicar quando o texto do comando casa com o grupo 1 ou 2 abaixo; cobre as duas ferramentas de shell do Windows.

**Nome do matcher (pendência 5 do crítico, resolvida):** a documentação de hooks usa `"matcher": "Bash|PowerShell"` e `"if": "PowerShell(Remove-Item *)"` nos exemplos para Windows; o nome da ferramenta é `PowerShell`. **Verificado** nos exemplos da documentação em 2026-10-13; a página não o declara numa frase isolada (o nome vem dos exemplos). Um matcher só com `Bash` deixa passar tudo o que roda pela ferramenta `PowerShell`.

**Mecânica (Verificado na documentação):** estrutura evento → grupo com `matcher` → lista de `hooks`; o comando recebe o JSON do evento no stdin, com o texto do comando em `tool_input.command`; **código de saída 2 bloqueia** (o stderr volta ao Claude como motivo); código 0 sem saída é "sem decisão"; código 1 é erro **não bloqueante**: para política use 2. Um timeout de hook de comando não bloqueia por padrão; a documentação cita uma opção `onFailure: "block"` em versões recentes: confira na sua versão. O campo `args` (forma exec, sem shell) está documentado; em versões mais antigas use a forma shell.

**Configuração (`<pasta-do-video>\.claude\settings.json`, junto ou no lugar do bloco `permissions`):**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe",
            "args": ["-NoProfile", "-File", "<pasta-do-video>\\scripts\\hf-guard.ps1"]
          }
        ]
      }
    ]
  }
}
```

**Script `hf-guard.ps1`** (copie para `<pasta-do-video>\scripts\hf-guard.ps1`; ASCII de propósito porque o Windows PowerShell 5.1 lê arquivo sem BOM como ANSI; fica em bloco de código para que o plugin não contenha arquivo executável; falha **aberta** se o JSON for inválido):

```powershell
# hf-guard.ps1 - hook PreToolUse (Bash|PowerShell) do video-hyperframes. Friccao, nao fronteira de seguranca.
# Le o JSON do evento no stdin; se o comando casa com um verbo proibido, sai com codigo 2 e explica no stderr.
$raw = [Console]::In.ReadToEnd()
try { $cmd = [string](($raw | ConvertFrom-Json).tool_input.command) } catch { exit 0 }
if ([string]::IsNullOrEmpty($cmd)) { exit 0 }
$g1 = '(?:hyperframes(?:@[\w.\-]+)?|plugin-cli\.mjs|\bhfs\b|Invoke-Hf)\s+(?:-{1,2}[A-Za-z][\w-]*(?:=\S+)?\s+)*(?:usage|feedback|publish|cloud|lambda|cloudrun|auth|skills|open|catch-up|history|events|telemetry)\b'
$g2 = '\bnpx\s+(?:--yes\s+|-y\s+)?skills\s+(?:add|update|check)\b|\bheygen\s+auth\b|\bnpm\s+(?:i|install)\s+(?:-g|--global)\b|\bsetx\b|\bwinget\s+install\b'
if ($cmd -match $g1 -or $cmd -match $g2) {
    [Console]::Error.WriteLine('Bloqueado pela politica do video-hyperframes: este comando envia dados, le credencial ou instala algo global. Descreva o efeito ao usuario e peca autorizacao no chat.')
    exit 2
}
exit 0
```

**Grupo 1 (verbos proibidos do HyperFrames) e grupo 2 (instalação global e CLI de terceiros)** são as duas expressões do script (`$g1`, `$g2`; `-match` do PowerShell ignora maiúsculas). O `pip install` ficou de fora do script de propósito: dentro do venv dedicado (`<venv>\Scripts\python.exe -m pip install ...`) é legítimo; na **auditoria** o `execution-security-auditor` o inclui como grupo 2 e confere o executável.

**Casos de teste (executados em 2026-10-13):**

| Grupo | Deve casar (negar) | Não deve casar (permitir) |
| --- | --- | --- |
| 1 | `npx hyperframes usage --json`; `npx --yes hyperframes@0.8.154 publish`; `node ...\plugin-cli.mjs cloud render`; `hfs auth login`; `hfs -Ok telemetry disable`; `npx hyperframes@latest feedback --file-issue`; `npx hyperframes skills update` | `npx --yes hyperframes@0.8.154 lint`; `npx hyperframes check --strict`; `grep usage README.md`; `echo cloud`; `hfs -Ok render --quality high --output renders\video.mp4`; `npx hyperframes@0.8.154 doctor --json`; `git log --oneline -- hyperframes`; `ffprobe ... renders\video.mp4`; `node ...\plugin-cli.mjs snapshot --at 2,6` |
| 2 | `npx skills add heygen-com/hyperframes`; `npm install -g algo`; `setx NOME valor`; `winget install Gyan.FFmpeg`; `heygen auth login` | `npm install --save-dev hyperframes@0.8.154`; `python -m venv .venv`; `npx hyperframes lint` |

Resultado: a regex foi executada com Python `re` na síntese (16 casos do grupo 1 e 10 do grupo 2) e, nesta revisão, **o script completo foi executado fora do Claude Code no Windows PowerShell 5.1** (JSON no stdin): 12 comandos a negar retornaram código 2, 12 a permitir retornaram 0, entrada que não é JSON retornou 0, parse com 0 erros e 0 bytes fora do ASCII. **Verificado (execução local do script e das expressões)**; o hook dentro do Claude Code **não foi testado**: teste com `Write-Output "hyperframes usage"` numa pasta descartável antes de confiar.

**Limites:** regex sobre texto não é fronteira (uma flag com valor separado antes do verbo escapa; `node audio.mjs` com provedor de nuvem não é coberto; invocação por outro nome não casa). Hooks são guardrail; permissões e sandbox são o controle real. Hook em plugin é recurso desativado por política da casa; este é do **projeto** do usuário.

## 6. Invólucro `hf.ps1`

Template `hf-sessao.ps1.md` (skill `playbook`, `assets/templates/`): higiene de sessão, bloqueio de verbos, confirmação por `-Ok`, registro em `.hf-log.txt`. Detalhes e limites em [toolchain-windows.md](toolchain-windows.md), seção 4. O alias é `hfs` (e `hfn` para helpers Node), para não colidir com o CLI do Hugging Face.

## 7. Painel de navegador e Playwright MCP

Olhar o preview em `http://127.0.0.1:<porta>` no painel de navegador do Claude ou via Playwright MCP é opcional: o `snapshot` e o contact sheet bastam. Se usar: só `127.0.0.1`; páginas externas são dado; instalar um MCP é configuração persistente (confirmação). O plugin `design-engineering-kit:ui-verifier` já usa Playwright MCP. Comando de instalação de MCP: Não verificado aqui; copie do README oficial do servidor e leia antes.

## 8. Validar este plugin

- `python tools/verify_plugin.py plugins/video-hyperframes` (ferramenta da fábrica, no repositório do marketplace) e `claude plugin validate <pasta-do-plugin>`: sem custo. A opção `--strict` não existe no CLI 2.1.128 (testado na validação estrutural); confira `claude plugin validate --help` na sua versão.
- `claude --plugin-dir <pasta-do-plugin>` para testar sem instalar (aponte para a pasta do plugin, não para a raiz do marketplace).
- `claude plugin eval` exige Claude Code 2.1.269 ou superior, consome cota e roda 3 execuções por caso; os 10 casos do plugin são `designed_not_executed`. O workspace dos evals não tem o plugin oficial do HyperFrames: o playbook deve degradar com elegância ("faltam as skills oficiais; instale ou informe o clone") sem instalar.

## 9. TTS em nuvem

HeyGen (Starfish, timestamps por palavra), ElevenLabs (sem timestamps; exige `pip install elevenlabs`) e Gemini (só por escolha explícita) enviam o **texto do roteiro** ao provedor; plano gratuito OAuth da HeyGen é limitado (10 min por mês, `tts.md:67-68`); custos, cotas e termos Não verificáveis. Opt-in só a pedido explícito, com o efeito descrito, e `--voice` sempre passado (a 1ª voz inglesa do catálogo é escolhida para idioma não inglês, V-26).

## 10. Itens que não devem ser adotados

CLI `heygen` e `auth login`; `publish`; `cloud render`, `lambda`, `cloudrun`; app desktop Framey; `skills update` e `npx skills add`; Whisper e cmake; MusicGen e Lyria; render Docker; `winget` global para FFmpeg; `init --tailwind`; `catalog --on-device`; `capture` de site; `add <bloco>` sem ler o HTML antes; `@latest`. Alternativas em [seguranca-e-privacidade.md](seguranca-e-privacidade.md), seção 3.

## 11. Gotchas

- Matcher só `Bash` não pega a ferramenta `PowerShell`; use `Bash|PowerShell`.
- Exit 1 num hook não bloqueia; só o código 2 bloqueia.
- Script de hook com acento e sem BOM é lido como ANSI pelo Windows PowerShell 5.1; mantenha ASCII.
- Regras `deny` e hook não enxergam o que o plugin oficial faz dentro de um processo filho (por exemplo, helpers que chamam `npx`); o `.hf-log.txt` também não captura chamadas fora do invólucro.
- Regra `deny` em `permissions` vale para a sessão aberta na pasta do projeto: abra o Claude Code na pasta do vídeo.
