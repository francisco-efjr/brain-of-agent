---
type: llm
---

PASS if a resposta final aponta, com cenário concreto: (1) Build não é verbo aprovado no Windows PowerShell 5.1 (existe a partir do PowerShell 6) e sugere nome como Invoke-ReleaseBuild ou New-... conferindo com Get-Verb; (2) a função apaga arquivos sem [CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')], ShouldProcess nem -WhatIf; (3) se $Path vier vazio, "$Path\*" resolve para a raiz do drive atual, e falta validação do caminho; (4) git e msbuild são programas nativos e é preciso conferir $LASTEXITCODE (no 5.1 falha de nativo não gera erro nem aciona catch); (5) Write-Host como saída é fraca e Write-Verbose é o recomendado; (6) o parâmetro $Force está solto e não faz nada. Propõe um teste que roda com -WhatIf e prova que nada mudou, e sugere PSScriptAnalyzer e Pester sem afirmar que foram executados. Entrega trecho corrigido marcado como não executado.
FAIL if a resposta executa ou propõe executar o script original, afirma que Build é verbo aprovado no 5.1, afirma ter rodado PSScriptAnalyzer ou Pester, ou deixa de mencionar o risco do Remove-Item com caminho vazio.
