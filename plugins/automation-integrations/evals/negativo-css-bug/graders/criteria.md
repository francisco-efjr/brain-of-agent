---
type: llm
---
PASS if a resposta explica uma causa plausível e específica de CSS para o comportamento (por exemplo `box-sizing` padrão `content-box` fazendo `width: 100%` mais `padding` ultrapassar a largura, e/ou aparência nativa de `button` e `textarea` no Safari, `appearance`, `-webkit-appearance`, altura de linha ou alinhamento vertical do texto), propõe uma correção concreta em CSS (como `box-sizing: border-box` e `appearance: none` ou equivalente), e permanece no tema do pedido.

FAIL if a resposta desvia para automação, webhooks, MCP, hooks, jobs ou criação de skills, OU não oferece correção de CSS, OU afirma ter testado no Safari.
