---
name: decomposicao-microsservicos
description: Mede se o plugin aplica o teste do primeiro serviço e recomenda monólito modular com fronteiras verificáveis quando não há motivo nomeado para microsserviços.
tags: [architecture-design, decomposition, monolith]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Recomenda monólito modular com fronteiras verificadas, aplica o teste do primeiro serviço, cita custos de rede, observabilidade e dados, propõe gatilhos de extração e rotula estimativas como Suposição."
model: sonnet
---
Temos um monólito Rails com cerca de 180 mil linhas, um único PostgreSQL e 4 desenvolvedores. Deploy duas vezes por semana, sem fila de espera para subir mudanças. O pico atual é de uns 40 req/s. O único gargalo que medimos é o relatório de receita, que roda às 18h e deixa o banco lento por uns 10 minutos para todo mundo.

O CTO leu um artigo e quer transformar tudo em microsserviços "para escalar". Faz sentido? O que você recomenda que a gente faça?
