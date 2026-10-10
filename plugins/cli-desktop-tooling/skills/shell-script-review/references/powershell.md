# PowerShell: checklist PSH, antes/depois e comandos de qualidade

Verificado em 2026-10-10 contra V-14, V-15, V-57, V-58, V-59, V-60. Ambiente-base: Windows PowerShell 5.1. Itens marcados Inferido são conhecimento estável do ecossistema ou dedução da fábrica. Os trechos são ilustrativos e **não foram executados**.

Sumário: [Checklist](#checklist-psh) · [Verbos](#escolha-de-verbo-v-14-v-60) · [Antes/depois](#antesdepois) · [Pester](#teste-pester-com--whatif) · [5.1 versus 7](#compatibilidade-51-versus-7-v-60) · [Comandos para o usuário](#comandos-de-qualidade-para-o-usuário-executar)

## Checklist PSH

IDs PSH-01 a PSH-16 e severidades padrão: os do `checklist-completo.md` do playbook (`${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/checklist-completo.md`). PSH-17 e PSH-18 são extensões desta skill (Inferido quanto à numeração e à severidade).

| ID | Sev. | Verificar | Detectar | Fonte |
| --- | --- | --- | --- | --- |
| PSH-01 | Média | Verbo aprovado; `Build-` e `Deploy-` só a partir do PowerShell 6 | `function \w+-\w+` comparado com `Get-Verb`; `Build-`, `Deploy-` em script do 5.1 | V-14, V-60 |
| PSH-02 | Baixa | Substantivo singular em PascalCase | nomes plurais ou fora de PascalCase | V-15 |
| PSH-03 | Baixa | `[switch]` em vez de booleano; `ValidateSet` para listas de opções | `[bool]$`, `[string]$Modo` sem validação | V-15 |
| PSH-04 | Alta | Função que apaga, move, publica ou instala usa `[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]` | `Remove-Item`, `Move-Item`, `Set-*`, `Publish-*`, instalação sem `SupportsShouldProcess` | V-57 |
| PSH-05 | Média | `ShouldProcess` perto da mudança e dentro do laço | `ShouldProcess` fora do `foreach` | V-57 |
| PSH-06 | Média | `-Force` próprio: `if ($Force -and -not $PSBoundParameters.ContainsKey('Confirm')) { $ConfirmPreference = 'None' }`, com `$Force` nunca dentro do `if` do `ShouldProcess`; chamadas internas com `-WhatIf:$WhatIfPreference` e, depois do prompt tratado, `-Confirm:$false` | `$Force` perto de `ShouldProcess`; cmdlet destrutivo interno sem `-WhatIf:$WhatIfPreference` | V-57 |
| PSH-07 | Alta | `$LASTEXITCODE` conferido depois de cada comando nativo | `git`, `msbuild`, `signtool`, `dotnet`, `npm` sem teste na linha seguinte | V-59 |
| PSH-08 | Média | `$ErrorActionPreference = 'Stop'` no topo e `try/catch/finally` | ausência; `catch {}` vazio; `-ErrorAction SilentlyContinue` ou `Ignore` em operação crítica | V-59 |
| PSH-09 | Baixa | Mensagens por `Write-Verbose/Warning/Debug`; saída como objetos | `Write-Host` fora de script interativo declarado (Inferido); `Write-Output` com texto formatado | V-15 |
| PSH-10 | Média | `-LiteralPath` quando o caminho pode ter curingas | `-Path` com entrada externa | V-15 |
| PSH-11 | Baixa | Ajuda com `.SYNOPSIS` e `.EXAMPLE` | bloco `<# .SYNOPSIS #>` ausente | V-15 |
| PSH-12 | Crítica | Variável vazia em `"$Path\*"` com remoção recursiva; parâmetro de caminho validado | `Remove-Item "$` com variável de parâmetro sem `ValidateNotNullOrEmpty`; sem recusa da raiz | V-57 (Inferido) |
| PSH-13 | Média | `??`, `??=`, `ForEach-Object -Parallel`, `Build-`, `Deploy-` só com `#requires -Version 7` | uso sem `#requires` | V-60 |
| PSH-14 | Baixa | PSScriptAnalyzer no fluxo (falha em erro; exclusão justificada) | ausência de etapa/configuração | V-58 |
| PSH-15 | Média | Teste Pester com `-WhatIf` prova que nada mudou; versão do Pester conferida | ausência de teste | V-57, V-58 |
| PSH-16 | Média | Sem `ShouldContinue` em script chamado por outros scripts (ele ignora `-WhatIf`, `-Confirm` e as preferências) | `ShouldContinue` | V-57 |
| PSH-17 | Alta | Segredo como `[string]$Password`/`$Token` no parâmetro; `Invoke-Expression` (extensão) | `[string]$Password`, `Invoke-Expression`, `ConvertTo-SecureString -AsPlainText` | V-58 (regras do analisador citadas: `PSCredential`, `Invoke-Expression`), Inferido |
| PSH-18 | Baixa | Ciente de que `-WhatIf` e `-Confirm` não atravessam módulo de script que chama outro módulo de script (extensão) | módulos encadeados | V-57 |

## Escolha de verbo (V-14, V-60)

| Intenção | Verbo | Observação |
| --- | --- | --- |
| Instalar / desinstalar | `Install` / `Uninstall` | |
| Validar, diagnosticar | `Test` | No lugar de `Ping` (reservado) |
| Publicar | `Publish` | `Deploy` só existe a partir do 6 |
| Implantar em destino remoto | `Deploy` (7) | No 5.1, `Publish-` ou `Invoke-<X>Deploy` |
| Compilar | `Invoke-<X>Build` ou `New-<Artefato>` | `Build` só a partir do 6 |
| Executar e esperar / iniciar sem esperar | `Invoke` / `Start` | `Invoke` é síncrono, `Start` é assíncrono |
| Medir / comparar | `Measure` / `Compare` | |
| Remover | `Remove` | nunca `Delete` |
| Criar / acrescentar / modificar | `New` / `Add` / `Set` | `Add` acrescenta a algo existente |
| Obter objeto / ler conteúdo | `Get` / `Read` | |

Verbos reservados: `ForEach`, `Ping`, `Sort`, `Tee`, `Where`. Use a forma exata (`Get`, não `Gets`). Confirme sempre com `Get-Verb` na versão instalada.

## Antes/depois

Antes (achados PSH-01, 04, 07, 08, 12):

```powershell
function Limpar-Build($Saida) {
    Remove-Item "$Saida\*" -Recurse -Force
    git clean -fdx
    Write-Host "pronto"
}
```

Depois (modelo; não executado):

```powershell
#requires -Version 5.1
function Clear-BuildOutput {
    <#
    .SYNOPSIS
    Remove os arquivos de saída de build de uma pasta.
    .EXAMPLE
    Clear-BuildOutput -Path .\dist -WhatIf
    #>
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'High')]
    param(
        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$Path,

        [switch]$Force
    )

    $ErrorActionPreference = 'Stop'
    if ($Force -and -not $PSBoundParameters.ContainsKey('Confirm')) { $ConfirmPreference = 'None' }

    try {
        $pasta = (Resolve-Path -LiteralPath $Path).ProviderPath
        if ($pasta -eq [System.IO.Path]::GetPathRoot($pasta)) {
            throw "Recusado: '$pasta' é a raiz de um drive."
        }
        foreach ($item in Get-ChildItem -LiteralPath $pasta -Force) {
            if ($PSCmdlet.ShouldProcess($item.FullName, 'Remover')) {
                Remove-Item -LiteralPath $item.FullName -Recurse -Force -Confirm:$false -WhatIf:$WhatIfPreference
            }
        }
        Write-Verbose "Limpeza de '$pasta' concluída."
    }
    catch {
        throw "Falha ao limpar '$Path': $($_.Exception.Message)"
    }
}
```

Para o comando nativo, depois de cada chamada:

```powershell
& git clean -fdx -- $pasta
if ($LASTEXITCODE -ne 0) { throw "git clean falhou com código $LASTEXITCODE" }
```

Por que assim: `SupportsShouldProcess` cria `-WhatIf` e `-Confirm` sozinhos (não declare parâmetros manuais); `ShouldProcess` dentro do laço deixa o `-WhatIf` listar cada item; `-Confirm:$false` no `Remove-Item` evita um segundo prompt depois que o seu já foi tratado, e `-WhatIf:$WhatIfPreference` mantém a simulação; a checagem da raiz protege contra caminho vazio ou curto demais (V-57, V-59, V-15).

## Teste Pester com -WhatIf

Ilustrativo para Pester 5 (a documentação nova usa `Should-Be`; confira `Get-Module Pester -ListAvailable` e a versão antes de escrever asserções):

```powershell
BeforeAll { . "$PSScriptRoot\Clear-BuildOutput.ps1" }

Describe 'Clear-BuildOutput' {
    It 'não remove nada com -WhatIf' {
        $dir = Join-Path $TestDrive 'dist'
        New-Item -ItemType Directory -Path $dir | Out-Null
        New-Item -ItemType File -Path (Join-Path $dir 'a.txt') | Out-Null

        Clear-BuildOutput -Path $dir -WhatIf

        Test-Path -LiteralPath (Join-Path $dir 'a.txt') | Should -BeTrue
    }
    It 'recusa um caminho vazio' {
        { Clear-BuildOutput -Path '' } | Should -Throw
    }
}
```

`Invoke-Pester -Output Detailed` roda os testes (V-58). Pester 5 exige que o código a testar seja carregado no `BeforeAll` (diferença Discovery versus Run: lacuna 10, não lida).

## Compatibilidade 5.1 versus 7 (V-60)

| Tema | 5.1 | 7.x |
| --- | --- | --- |
| Base | .NET Framework 4.5 | .NET moderno, código aberto, multiplataforma |
| `??`, `??=`, `ForEach-Object -Parallel` | não existem | existem |
| Verbos `Build`, `Deploy` | não existem | existem (desde o 6) |
| `$OutputEncoding` | ASCII | UTF-8 sem BOM |
| `Out-GridView` / dependentes de WPF | existem | voltaram no 7.0 |
| `$PSNativeCommandUseErrorActionPreference` | não existe (Inferido) | experimental no 7.3, estável no 7.4, padrão `$false` |
| Workflow | existe | removido |

Não conferido (V-60): operador ternário e `&&`/`||` do 7. Codificação de arquivos: no 5.1, `>` e `Out-File` gravam UTF-16 LE e `-Encoding utf8` grava com BOM (conhecimento estável, Inferido); defina a codificação explicitamente quando outro programa lê o arquivo.

## Comandos de qualidade para o usuário executar

Nenhum deles foi rodado pela skill; peça autorização ou entregue ao usuário.

```powershell
$PSVersionTable.PSVersion                                   # versão em uso
Get-Verb | Where-Object Verb -eq 'Build'                    # vazio no 5.1
Get-Module Pester -ListAvailable | Select-Object Name, Version
# Instalar altera o ambiente (decisão do usuário):
#   Install-Module PSScriptAnalyzer -Scope CurrentUser
#   Install-Module Pester -Force -SkipPublisherCheck        # Pester atual lado a lado (V-58)
Invoke-ScriptAnalyzer -Path .\scripts -Recurse -Severity Error, Warning
Invoke-Pester -Output Detailed
```

Regras do PSScriptAnalyzer citadas na fonte: variáveis não inicializadas, uso do tipo `PSCredential`, `Invoke-Expression`, entre outras. Suporta Windows PowerShell 5.1 ou posterior e PowerShell 7.2.11 ou posterior (V-58).
