# Scripts PowerShell e shell (bash e POSIX sh)

Sumário: 1. Ambiente-base · 2. PowerShell: nomes · 3. PowerShell: ShouldProcess e -WhatIf · 4. PowerShell: erros e comandos nativos · 5. PowerShell: 5.1 contra 7 · 6. PowerShell: qualidade (PSScriptAnalyzer e Pester) · 7. Modelo de função · 8. Shell: ShellCheck, Google e POSIX · 9. Exemplos · 10. Limites

Fontes: V-14, V-15, V-57, V-58, V-59, V-60 (PowerShell); V-61, V-62, V-63 (shell). O script em revisão nunca é executado (pode ser destrutivo). PSScriptAnalyzer, Pester e ShellCheck só rodam com autorização, depois de instalados pelo usuário; sem isso, o relatório diz "não executado" e traz o comando. Os trechos de código abaixo são da fábrica e não foram executados.

## 1. Ambiente-base

Windows 11 com Windows PowerShell 5.1 como shell principal (confirme com `$PSVersionTable`); Git Bash fornece `bash` para arquivos `.sh`. Scripts miram o 5.1; recursos do 7 exigem `#requires -Version 7` e aviso ao usuário (V-60). Em comandos de shell do agente neste ambiente, use cmdlets (`Get-ChildItem`, `Get-Content`, `Get-Command`, `ConvertFrom-Json`) em vez de comandos Linux, salvo ao rodar `.sh` (regra própria, baseada em V-14).

## 2. PowerShell: nomes (V-14, V-15)

- Verbo aprovado na forma exata (`Get`, não `Gets`); sem sinônimo (`Remove`, nunca `Delete`); reservados: `ForEach`, `Ping`, `Sort`, `Tee`, `Where`. `New` cria, `Add` acrescenta a algo existente, `Set` modifica (ou cria com dados); `Invoke` é síncrono, `Start` assíncrono; `Test` no lugar de `Ping`; `Get` obtém o objeto, `Read` extrai conteúdo. `Get-Verb` lista todos.
- **`Build` e `Deploy` existem a partir do PowerShell 6; não no 5.1.** A tabela de verbos lista `Build` como sinônimo a evitar de `New` e `Deploy` de `Publish`. No 5.1, use `Invoke-<X>Build`, `New-<Artefato>`, `Publish-`, `Install-`.
- Tabela de escolha: instalar `Install`; desinstalar `Uninstall`; validar ou diagnosticar `Test`; publicar `Publish`; executar e esperar `Invoke`; iniciar sem esperar `Start`; medir `Measure`; comparar `Compare`.
- Substantivos específicos e no singular; PascalCase em funções e parâmetros; `[switch]` em vez de booleano; `ValidateSet` ou enum para opções; `PassThru` em `Add/Set/New`; entrada por pipeline quando fizer sentido; objetos (não texto) na saída; `Write-Verbose`, `Write-Warning`, `Write-Debug` para mensagens (preferir a `Write-Host` é Inferido); ajuda com `.SYNOPSIS` e `.EXAMPLE`; `-LiteralPath` ao lidar com caminhos.
- A página V-15 não trata de `ShouldProcess`: use V-57.

## 3. PowerShell: ShouldProcess e -WhatIf (V-57)

- `[CmdletBinding(SupportsShouldProcess)]` cria `-WhatIf` e `-Confirm`; não crie parâmetro manual nem teste `$WhatIf`.
- `$PSCmdlet.ShouldProcess('alvo', 'operação')` o mais perto possível da mudança e dentro do laço, para executar o máximo de código no modo simulação. Com `-WhatIf` devolve falso e imprime "What if:".
- `ConfirmImpact` (High, Medium, Low, None) é comparado com `$ConfirmPreference` (padrão **High**); o padrão de `ConfirmImpact` é **Medium**; portanto só `High` pergunta sem `-Confirm`. `-Confirm` põe `$ConfirmPreference` em `Low` no escopo.
- `ShouldContinue` ignora `-WhatIf`, `-Confirm` e as preferências e sempre pergunta: evite em script chamado por outros.
- `-Force` próprio: `if ($Force -and -not $PSBoundParameters.ContainsKey('Confirm')) { $ConfirmPreference = 'None' }`, mantendo `-WhatIf` prioritário; nunca ponha `$Force` dentro do `if` do `ShouldProcess`.
- Chamadas internas: `-WhatIf:$WhatIfPreference` explícito; `-Confirm:$false` só depois de tratar o prompt.
- Limite conhecido: `-WhatIf` e `-Confirm` não atravessam um módulo de script que chama outro módulo de script.

## 4. PowerShell: erros e comandos nativos (V-59)

- Três categorias: não terminante (não aciona `catch`, a menos que escalado), terminante de instrução e terminante de script (`throw`). `try/catch` pega as duas terminantes; `catch` filtra por tipo, do mais específico ao mais geral; `$_` é um `ErrorRecord`; `finally` roda sempre, inclusive com Ctrl+C e `exit` no `catch`.
- `-ErrorAction Stop` ou `$ErrorActionPreference = 'Stop'` escalam o erro não terminante e o `catch` o pega (Verificado). Em função avançada (`[CmdletBinding()]`) o erro escalado vira terminante de instrução (o script continua na linha seguinte); em bloco não avançado vira terminante de script. `SilentlyContinue` ou `Ignore` podem suprimir até um `throw`.
- **Comando nativo** (`git`, `msbuild`, `signtool`) com código diferente de zero não gera `ErrorRecord` nem aciona `catch`: teste `$LASTEXITCODE` depois de cada chamada. `$PSNativeCommandUseErrorActionPreference` (experimental no 7.3, estável no 7.4, padrão `$false`) é do 7; no 5.1 não existe (Inferido). Padrões: `$ErrorActionPreference` = `Continue`, `$ConfirmPreference` = `High`, `$WhatIfPreference` = `$false`.

## 5. PowerShell 5.1 contra 7 (V-60)

5.1 roda sobre .NET Framework 4.5; 6 em diante é de código aberto e multiplataforma; Workflow foi removido; `Out-GridView` e cmdlets dependentes de WPF voltaram no 7.0; `$OutputEncoding` passou a UTF-8 sem BOM no lugar de ASCII; `??` e `??=` e `ForEach-Object -Parallel` são do 7. Operador ternário e `&&`/`||` do PowerShell não foram conferidos: não afirme.

## 6. PowerShell: qualidade (V-58)

- PSScriptAnalyzer (MIT): verificador estático (variáveis não inicializadas, tipo `PSCredential`, `Invoke-Expression` e outras); Windows PowerShell 5.1 ou posterior e PowerShell 7.2.11 ou posterior; instalação por `Install-PSResource` ou `Install-Module`. Falhe em erro; exclusão de regra só com justificativa escrita.
- Pester (Apache-2.0): arquivos `*.Tests.ps1`, `Describe`/`Context`/`It`/`Should`, `Invoke-Pester -Output Detailed`, `BeforeAll` para carregar a função por `$PSScriptRoot`. **O Windows traz o Pester 3.4.0**, que não atualiza com `Update-Module`: a versão atual se instala lado a lado com `Install-Module -Name Pester -Force -SkipPublisherCheck`. Confira `Get-Module Pester -ListAvailable` antes de escrever asserções: o Pester 5 usa `Should -Be` e a documentação nova usa `Should-Be`.
- Teste mínimo de destrutivo: roda com `-WhatIf` e prova que nada mudou.

```powershell
# exemplo da fábrica, não executado; ajuste à versão do Pester instalada
Describe 'Remove-BuildOutput' {
    BeforeAll { . "$PSScriptRoot\Remove-BuildOutput.ps1" }
    It 'não remove nada com -WhatIf' {
        $dir = Join-Path $TestDrive 'out'; New-Item -ItemType Directory $dir | Out-Null
        New-Item -ItemType File (Join-Path $dir 'a.txt') | Out-Null
        Remove-BuildOutput -Path $dir -WhatIf
        (Get-ChildItem $dir).Count | Should -Be 1
    }
}
```

## 7. Modelo de função (resumo; versão completa em `assets/templates/script-powershell-modelo.md`)

```powershell
#requires -Version 5.1
function Remove-BuildOutput {
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'High')]
    param(
        [Parameter(Mandatory)][ValidateNotNullOrEmpty()][string]$Path,
        [switch]$Force
    )
    $ErrorActionPreference = 'Stop'
    if ($Force -and -not $PSBoundParameters.ContainsKey('Confirm')) { $ConfirmPreference = 'None' }
    $root = (Resolve-Path -LiteralPath $Path).ProviderPath
    if ($root.TrimEnd('\') -match '^[A-Za-z]:$') { throw "Recusado: '$root' é a raiz de um drive." }
    foreach ($item in Get-ChildItem -LiteralPath $root -Force) {
        if ($PSCmdlet.ShouldProcess($item.FullName, 'Remove')) {
            Remove-Item -LiteralPath $item.FullName -Recurse -Force -WhatIf:$WhatIfPreference
        }
    }
}
```

## 8. Shell: ShellCheck, Google e POSIX

- **ShellCheck (V-61, ferramenta GPL-3.0; wiki sem licença):** SC2086, expansão sem aspas sofre divisão de palavras e globbing: use `"$1"`, `"$@"`; exceções: arrays no bash para divisão intencional, `set -f` ou `IFS=''`. SC2155, `local`, `export` ou `readonly` com substituição de comando na mesma linha mascara o código de saída: declare e atribua em linhas separadas. SC2164, `cd` sem tratamento de falha continua no diretório errado, perigoso antes de `rm`: `cd dir || exit` (em função, `|| return`). Trate esses três como erro. SC2046, SC2034, SC1008 e SC3001 a SC3067 vêm do índice e não foram reconferidos. Declare o dialeto no shebang (`sh` ou `bash`) para o ShellCheck avisar recursos não portáveis; supressão só com comentário de justificativa. No Windows o ambiente é Git Bash (bash, não `sh` puro).
- **Google Shell Style Guide (V-62, B; texto em repositório CC BY 3.0, aqui só destilado, atribuição ao Google):** bash é a única linguagem de shell para executáveis; script com mais de 100 linhas ou fluxo não trivial vai para linguagem mais estruturada; `set` para opções do shell; mensagens de erro para STDERR por função `err()`; aspas em variáveis, `"$@"` no lugar de `$*`; `local` em funções; nomes de função e variável em minúsculas com sublinhado, constantes e variáveis de ambiente em maiúsculas; `(( i++ ))` solto pode encerrar o script com `set -e` quando a expressão vale zero.
- **`set -euo pipefail` é convenção própria, não do Google** (o guia não recomenda `set -e` nem `pipefail`; usa `PIPESTATUS`). Se adotar, registre o aviso: `set -e` tem exceções.
- **POSIX (V-63, B 6):** `set -e` não sai quando falha um comando individual dentro de pipeline de vários comandos (só a do pipeline inteiro conta), nem na lista composta depois de `while`, `until`, `if`, `elif`, nem em pipeline iniciado por `!`, nem em comando de lista AND-OR que não seja o último: rede parcial, não garantia. Para rodar em `sh` puro, não use `[[`, arrays, `local` nem `function` (regra de portabilidade da fábrica; `local` só aparece no POSIX numa tabela de comportamento não especificado). Parte final da página não lida.

## 9. Exemplos de achados

Entrada (PowerShell 5.1): `function Build-Release { param($Path, $Force) Write-Host "Limpando $Path"; Remove-Item "$Path\*" -Recurse -Force; git pull; msbuild app.sln /p:Configuration=Release; Write-Host "Pronto!" }`.

| ID | Sev. (Inferido) | Achado | Correção |
| --- | --- | --- | --- |
| PSH-01 | Média | `Build` não é verbo do 5.1 | `Invoke-ReleaseBuild` ou `New-ReleasePackage` |
| PSH-02 | Alta | Apaga sem `SupportsShouldProcess` | `[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]` e `ShouldProcess` por item |
| PSH-09 | Crítica | `$Path` vazio vira a raiz do drive em `"$Path\*"` | `Mandatory`, `ValidateNotNullOrEmpty`, recusar raiz |
| PSH-07 | Alta | `git pull` e `msbuild` sem `$LASTEXITCODE` | Checar após cada nativo |
| PSH-08 | Baixa | `Write-Host` como saída | `Write-Verbose` e objetos |

Entrada (sh): `#!/bin/sh`, `cd $1`, `rm -rf build/*`, `local out=$(make all)`, `[[ -f out.txt ]] && echo ok`, `echo "erro"`.

| ID | Sev. | Achado | Correção |
| --- | --- | --- | --- |
| SHL-02, SHL-04 | Crítica | `cd $1` sem aspas e sem `|| exit` antes de `rm -rf` (SC2086, SC2164) | `cd "$1" \|\| exit 1` |
| SHL-03 | Média | `local out=$(...)` (SC2155) | `local out; out=$(make all)` |
| SHL-12 | Média | `[[` e `local` com shebang `sh` | Declarar `bash` ou usar construtos POSIX |
| SHL-07 | Baixa | `echo "erro"` em stdout | `echo "erro" >&2` |

## 10. Limites

POSIX lido só de 60.000 a 160.000 de 189.000 caracteres; cobertura do Pester (`-CI`, `-PassThru`, mocks, Discovery contra Run) não lida; `ShouldProcess` de cmdlet compilado não coberto; o nome da ferramenta PowerShell do Claude Code (matcher de hook) não foi verificado: ver `ferramentas-e-mcp.md`.
