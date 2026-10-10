---
name: negativo-componente-react
description: "Caso negativo. Pedido de frontend sem relação com dados: nenhuma skill do plugin data-engineering deve disparar."
tags: [data-engineering, negative]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um componente React em TypeScript de tabela com ordenação e paginação sem acionar nenhuma skill do plugin data-engineering e sem ler suas referências."
model: sonnet
---
Escreva um componente React em TypeScript de tabela com ordenação por coluna e paginação no cliente. Props: `rows` (array de objetos com `id`, `nome` e `valor`) e `pageSize` (padrão 10).
