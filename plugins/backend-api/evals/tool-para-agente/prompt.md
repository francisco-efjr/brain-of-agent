---
name: tool-para-agente
description: Mede se o plugin redesenha tools de agente do lado do serviço com consolidação por fluxo, nomes com prefixo, resposta concisa, paginação, erro acionável, schema estrito e avaliação de 10 perguntas, sem inventar métricas nem tratar o limite do Claude Code como regra geral.
tags: [backend-api, agent-tool-design]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Consolida por fluxo, propõe nomes com prefixo e parâmetros sem ambiguidade, modo concise/detailed, paginação e filtros, erro acionável, descrição em quatro frases, strict e additionalProperties false nas tools que mudam estado, anotações readOnlyHint e plano de avaliação de 10 perguntas rotulado como não executado."
model: sonnet
---
Vou expor o backend de pedidos como tools MCP para um agente de atendimento. Hoje são três:

- `list_all_orders()` devolve todas as linhas da tabela (uns 5 MB de JSON).
- `get_order_by_id(id)` devolve o pedido completo.
- `get_customer(id)` devolve o cliente completo.

Em erro todas retornam só `Error 500`. O agente vive errando de tool, chamando a mesma coisa várias vezes ou estourando o contexto. Ele precisa cumprir fluxos como "o cliente X perguntou onde está o último pedido dele" e "cancele o pedido Y se ainda não foi enviado". Como melhoro isso? Não tenho o código aqui; trabalhe com o que escrevi.
