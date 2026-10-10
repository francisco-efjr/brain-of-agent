---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega uma query PostgreSQL correta que agrega o total por região e vendedor no período de 2026-09-01 (inclusive) a 2026-10-01 (exclusivo, ou intervalo equivalente) e aplica uma função de janela de ranking (`RANK()`, `DENSE_RANK()` ou `ROW_NUMBER()`) com `PARTITION BY regiao` e `ORDER BY` do total em ordem decrescente.
2. Explica de forma curta a escolha entre `RANK`, `DENSE_RANK` e `ROW_NUMBER` quando há empate.
3. Responde direto, sem transformar o pedido em revisão de arquitetura mobile, checklist de loja ou qualquer fluxo do segmento de aplicativos mobile.
FAIL if qualquer um ocorrer: aciona qualquer skill ou agente do plugin mobile-apps; usa sintaxe que não existe no PostgreSQL; afirma ter executado a query contra um banco; propõe mudar de banco ou de arquitetura.
