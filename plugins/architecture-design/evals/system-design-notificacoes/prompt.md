---
name: system-design-notificacoes
description: Mede se o plugin conduz um system design em fases, com perguntas, estimativa de ordem de grandeza no texto com premissas rotuladas, diagrama pequeno, modos de falha e o que não construir.
tags: [architecture-design, system-design, estimation]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Bash]
timeout_seconds: 600
runs: 3
expected_outcome: "Faz perguntas de esclarecimento, estima QPS e armazenamento no texto com premissas Suposição, entrega diagrama Mermaid de até 15 nós, tabela de trade-offs, modos de falha e o que não construir, sem executar scripts."
model: sonnet
---
Projete um serviço de notificações (e-mail e push) para a nossa plataforma: 2 milhões de usuários cadastrados, picos de 50 mil envios por minuto em campanhas, retentativas quando o provedor falha e preferências de canal por usuário. Time de 5 pessoas, nuvem pública, orçamento moderado. Preciso de um design doc curto que eu possa levar para a revisão técnica na quinta.
