---
name: workflow-vs-multiagente
description: "Mede se o plugin recomenda workflow ou chamada única como baseline antes de multiagente, cita o custo extra, propõe medir com os tickets rotulados e define parada e teto, em vez de aprovar o orquestrador por padrão."
tags: [llm-ai-agents, agent-architecture]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Recomenda encadeamento ou roteamento (workflow) com chamada única como baseline, explica que multiagente adiciona custo e superfície de falha sem necessidade quando os passos são sempre os mesmos, propõe medir com os 2.000 tickets rotulados, define condição de parada, teto e eval, e registra a alternativa descartada."
model: sonnet
---
Tenho um sistema de suporte que classifica cada ticket em 6 categorias (cobrança, entrega, defeito, troca, conta, outros) e depois responde com um prompt diferente por categoria. Os passos são sempre os mesmos: classificar, buscar dados do pedido, responder. Já temos 2.000 tickets antigos rotulados com a categoria correta e a resposta aprovada pelo time. Meu colega quer montar um orquestrador com 6 agentes, um por categoria, cada um com ferramentas próprias (CRM, rastreio, estoque). Faz sentido? Como você desenharia e como a gente decide sem achismo?
