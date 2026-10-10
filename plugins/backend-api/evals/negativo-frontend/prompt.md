---
name: negativo-frontend
description: Caso negativo que mede sobredisparo, verificando que uma pergunta de React sobre useMemo e useCallback não aciona nenhuma skill do plugin de backend e recebe resposta técnica direta.
tags: [backend-api, negative, frontend]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Explica corretamente a diferença entre useMemo e useCallback com um exemplo curto, sem acionar skill do plugin backend-api."
model: sonnet
---
Explica a diferença entre useMemo e useCallback no React com um exemplo curto? Estou montando um componente de lista com filtro e fico na dúvida de quando usar cada um.
