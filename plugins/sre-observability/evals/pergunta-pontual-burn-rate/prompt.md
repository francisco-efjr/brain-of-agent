---
name: pergunta-pontual-burn-rate
description: "Mede a proporcionalidade: uma pergunta pontual sobre burn rate com SLO de 99,9 por cento em 30 dias deve receber resposta curta e direta com a conta, sem montar relatório, handoff, matriz nem ativar o modo completo."
tags: [sre-observability, playbook, proporcionalidade]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Responde em poucas linhas: burn rate de 14,4 consome 2 por cento do orçamento em 1 hora (0,02 x 720 h / 1 h), limiar de erro de 1,44 por cento, janela curta de 5 min; avisa que vale para 99,9 por cento em 30 dias; não monta relatório longo, handoff, matriz de aplicabilidade nem lê referências em lote; não executa comandos."
model: sonnet
---
Meu SLO é 99,9% de disponibilidade em 30 dias. Qual taxa de erro em 1 hora faz sentido para disparar uma página rápida? Só preciso do número e de como chegar nele.
