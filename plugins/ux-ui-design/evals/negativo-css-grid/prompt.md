---
name: negativo-css-grid
description: Caso negativo que mede sobredisparo, verificando que uma pergunta conceitual sobre CSS grid e flexbox não aciona nenhuma skill do plugin de UX e design e recebe resposta técnica direta com exemplo curto.
tags: [ux-ui-design, negative, css]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Explica corretamente a diferença entre CSS grid (bidimensional) e flexbox (unidimensional) com exemplo curto, sem acionar skill do plugin ux-ui-design e sem transformar a pergunta em auditoria ou plano de design."
model: sonnet
---
Pode me explicar a diferença entre CSS grid e flexbox, com um exemplo curto? Estou montando um layout de galeria de fotos e fico em dúvida sobre qual dos dois usar.
