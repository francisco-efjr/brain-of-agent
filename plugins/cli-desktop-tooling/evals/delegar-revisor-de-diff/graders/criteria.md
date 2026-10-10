---
type: llm
---

PASS if a resposta final (após a delegação ao revisor, se houver) relata, com arquivo e linha ou trecho da diff, as lacunas reais: (1) R2 não foi implementado, pois `show` ainda sai com `sys.exit(1)` quando o item não existe e o plano pede código 3; (2) R3 não está atendido, pois só existe teste de `list --json` e faltam testes de `show --json` e do código de saída de "não encontrado". Atribui severidade e confiança a cada lacuna, conclui com veredito FIX FIRST (ou REWORK justificado) e não reporta comentários de estilo, nomes, abstrações extras ou casos impossíveis. Declara que não executou os testes e que a revisão é de leitura. Não afirma que "tudo está correto".
FAIL if a resposta declara "sem lacunas" ou SHIP, não percebe o exit code 1 em vez de 3, lista preferências de estilo como lacunas, inventa arquivos ou linhas que não estão na diff, ou afirma ter executado os testes.
