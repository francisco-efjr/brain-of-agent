# Notas / incertezas

- pytest não está instalado no ambiente. Validei os testes com um mini-shim (parametrize empilhado + raises com match) rodando num runner próprio, fora da pasta de saída. Não rodei com o pytest real. Pontos de risco mínimos: parametrize empilhado com `vip` em `test_subtotal_negativo_levanta_value_error` e `match="negativo"` (a mensagem do código é "subtotal negativo").
- Os testes seguem a docstring (fonte de verdade = regras do Produto). Assumi que os dois comportamentos (limite de 500 exclusivo e VIP em faixa sem desconto) são bugs, não decisões intencionais. A docstring é explícita nos dois, então a confiança é alta, mas vale confirmar com Produto se existir regra não documentada.
- Deixei os testes falhando (sem xfail) para o bug ficar visível. Alternativa é xfail(strict=True) até o fix.
- Erro meu durante o trabalho: calculei errado um valor esperado (VIP 499,99 = 34,9993 -> 35,00, não 34,99). Corrigido. Todos os valores esperados foram validados contra uma cópia corrigida do código (63/63 passam), o que também confirma a aritmética de todos os casos.
- Ambiguidades da spec que NÃO testei: subtotais com mais de 2 casas decimais entre 499,99 e 500 (ex.: 499,995 — cai nos 5% pelo código, mas a faixa "até 499,99" não define isso); entrada `float` (o type hint é Decimal; `float * Decimal` levanta TypeError, comportamento não especificado); `None`/string; Decimal NaN/Infinity.
- Teto: assumi que o teto se aplica antes do arredondamento (como o código faz); com teto inteiro de 150 o resultado é idêntico nos dois ordens, então não há ambiguidade prática.
- Não modifiquei `desconto.py` (a cópia em outputs é idêntica ao original); a correção está só descrita na resposta.
