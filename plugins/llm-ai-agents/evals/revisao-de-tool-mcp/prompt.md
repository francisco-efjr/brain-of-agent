---
name: revisao-de-tool-mcp
description: "Mede se o plugin revisa duas definições de tool com descrições vazias e uma ferramenta de escrita sem confirmação, reescrevendo a descrição, renomeando parâmetros, exigindo confirmação, sugerindo erros acionáveis e sem inventar campos do protocolo."
tags: [llm-ai-agents, tool-design-review]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Reescreve as descrições dizendo quando usar, quando não usar e qual ferramenta usar no lugar, renomeia os parâmetros para nomes inequívocos, exige confirmação humana em do_action por enviar e-mail, sugere paginação, saída legível e response_format em get_data e erros que dizem como corrigir, e não inventa campos do protocolo."
model: sonnet
---
O meu agente de suporte às vezes escolhe a tool errada e uma vez mandou um e-mail para o cliente que eu nem queria. Aqui estão as duas tools, num servidor MCP que eu mesmo escrevi. `get_data` consulta o CRM e devolve o JSON cru do registro (às vezes 500 linhas, com UUIDs). `do_action` envia um e-mail pelo SMTP da empresa para o endereço passado em `target`. Revisa e me diz o que mudar.

```json
[
  {
    "name": "get_data",
    "description": "Gets data",
    "inputSchema": {
      "type": "object",
      "properties": { "user": { "type": "string" }, "q": { "type": "string" } },
      "required": ["user", "q"]
    }
  },
  {
    "name": "do_action",
    "description": "Does the action",
    "inputSchema": {
      "type": "object",
      "properties": { "target": { "type": "string" } },
      "required": ["target"]
    }
  }
]
```
