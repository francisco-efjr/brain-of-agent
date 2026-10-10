---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Explica corretamente que `useMemo` memoriza o resultado de um cálculo e `useCallback` memoriza a própria função (equivalente a `useMemo(() => fn, deps)`), ambos controlados por lista de dependências.
2. Inclui um exemplo curto e coerente com o contexto de lista com filtro (por exemplo `useMemo` para a lista filtrada e `useCallback` para um handler passado a filho memoizado).
3. Responde direto, sem transformar a pergunta em revisão de API, contrato, segurança ou plano de backend.
FAIL if qualquer um ocorrer: aciona qualquer skill ou agente do plugin backend-api; afirma que useCallback sempre melhora a performance; inclui conteúdo de API REST, OpenAPI, autenticação ou idempotência sem relação com a pergunta.
