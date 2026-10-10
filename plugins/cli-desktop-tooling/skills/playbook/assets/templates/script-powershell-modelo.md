# Modelo de script PowerShell (5.1)

Função de referência para scripts que apagam, movem, publicam ou instalam. **Não executada**: antes de usar, rode `Invoke-ScriptAnalyzer` (PSScriptAnalyzer) e o teste Pester abaixo, com `-WhatIf` primeiro, e só depois em dados reais. Instalar PSScriptAnalyzer e Pester é decisão do usuário (V-58). Fontes: V-14, V-15, V-57, V-59, V-60.

Pontos do modelo:
- Verbo aprovado no 5.1 (`Remove`); `Build` e `Deploy` só existem a partir do PowerShell 6 (confira `Get-Verb`).
- `SupportsShouldProcess` com `ConfirmImpact='High'`: só `High` pede confirmação sem `-Confirm` (padrão de `$ConfirmPreference` é High).
- `ShouldProcess` dentro do laço, perto da mudança; chamadas internas com `-WhatIf:$WhatIfPreference`; `-Force` próprio fora do `if` do `ShouldProcess`.
- `$ErrorActionPreference = 'Stop'`, `try/catch/finally`, `$LASTEXITCODE` após comando nativo.
- Parâmetro de caminho obrigatório, `-LiteralPath`, recusa da raiz de drive (variável vazia em `"$Path\*"` vira a raiz).

```powershell
#requires -Version 5.1
<#
.SYNOPSIS
Remove o conteúdo de uma pasta de saída de build.
.DESCRIPTION
Pede confirmação (ConfirmImpact High). Use -WhatIf para simular e -Force para pular a confirmação.
.EXAMPLE
Remove-BuildOutput -Path .\out -WhatIf
#>
function Remove-BuildOutput {
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'High')]
    param(
        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [ValidateNotNullOrEmpty()]
        [string]$Path,

        [switch]$Force
    )
    begin {
        $ErrorActionPreference = 'Stop'
        if ($Force -and -not $PSBoundParameters.ContainsKey('Confirm')) { $ConfirmPreference = 'None' }
    }
    process {
        try {
            $root = (Resolve-Path -LiteralPath $Path).ProviderPath
            if ($root.TrimEnd('\') -match '^[A-Za-z]:$') { throw "Recusado: '$root' é a raiz de um drive." }
            foreach ($item in Get-ChildItem -LiteralPath $root -Force) {
                if ($PSCmdlet.ShouldProcess($item.FullName, 'Remove')) {
                    Remove-Item -LiteralPath $item.FullName -Recurse -Force -WhatIf:$WhatIfPreference
                }
            }
        }
        catch {
            Write-Error -ErrorRecord $_
        }
        finally {
            Write-Verbose 'Remove-BuildOutput concluído.'
        }
    }
}

# Comando nativo: o catch não dispara por exit code; confira $LASTEXITCODE.
function Invoke-NativeChecked {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$FilePath, [string[]]$ArgumentList)
    & $FilePath @ArgumentList
    if ($LASTEXITCODE -ne 0) { throw "$FilePath terminou com código $LASTEXITCODE." }
}
```

Teste Pester (confira `Get-Module Pester -ListAvailable`: o Windows traz o 3.4.0; o Pester 5 usa `Should -Be`, a documentação nova usa `Should-Be`):

```powershell
Describe 'Remove-BuildOutput' {
    BeforeAll { . "$PSScriptRoot\Remove-BuildOutput.ps1" }
    It 'não remove nada com -WhatIf' {
        $dir = Join-Path $TestDrive 'out'
        New-Item -ItemType Directory $dir | Out-Null
        New-Item -ItemType File (Join-Path $dir 'a.txt') | Out-Null
        Remove-BuildOutput -Path $dir -WhatIf
        (Get-ChildItem $dir).Count | Should -Be 1
    }
    It 'recusa caminho vazio' {
        { Remove-BuildOutput -Path '' -WhatIf } | Should -Throw
    }
}
```

Limites: `-WhatIf` e `-Confirm` não atravessam módulo de script que chama outro módulo de script (V-57). Nenhum teste aponta para uma raiz de drive real: a recusa da raiz fica verificada por leitura da função, não por execução. Marque o resultado como "não executado" até haver saída colada.
