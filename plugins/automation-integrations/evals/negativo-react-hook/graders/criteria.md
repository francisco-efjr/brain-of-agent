---
type: llm
---
PASS if a resposta identifica uma causa específica do laço no React (o array literal `[1, 2, 3]` cria uma nova referência a cada renderização e entra nas dependências do `useEffect`, e/ou `total` é dependência do efeito que o atualiza), propõe uma correção concreta (memoizar ou mover o array para fora do componente, tirar `total` das dependências, ou derivar `total` direto de `itens.length` sem efeito) e permanece no tema do pedido.

FAIL if a resposta trata o pedido como hook do Claude Code ou desvia para automação, webhooks, MCP, jobs ou criação de skills, OU não oferece correção em código React, OU afirma ter executado o componente.
