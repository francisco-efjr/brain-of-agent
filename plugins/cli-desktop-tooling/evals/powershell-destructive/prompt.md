---
name: powershell-destructive
description: Mede se a revisão de um script PowerShell 5.1 aponta verbo Build inexistente no 5.1, ausência de SupportsShouldProcess, variável de caminho vazia, nativos sem LASTEXITCODE e Write-Host, sem executar o script.
tags: [cli-desktop-tooling, shell-script-review, powershell, scripts]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: Achados com cenário concreto, correção com ShouldProcess e LASTEXITCODE, proposta de teste com -WhatIf e declaração de que o script, o PSScriptAnalyzer e o Pester não foram executados.
model: sonnet
---

Esse script de release roda no Windows PowerShell 5.1 do nosso build server. Revisa pra mim, por favor? Está no release.ps1:

```powershell
function Build-Release {
    param($Path, $Force)
    Write-Host "Limpando $Path"
    Remove-Item "$Path\*" -Recurse -Force
    git pull
    msbuild app.sln /p:Configuration=Release
    Write-Host "Pronto!"
}
```
