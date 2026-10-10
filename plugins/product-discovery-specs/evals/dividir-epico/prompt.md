---
name: dividir-epico
description: Mede se o plugin divide um épico em fatias verticais que entregam valor, aplica INVEST, levanta regras implícitas e perguntas abertas e não divide por camada técnica nem promete prazo.
tags: [product-discovery-specs, refine-backlog, invest, slicing]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega fatias verticais com valor visível e critério resumido, checa INVEST, lista regras implícitas e perguntas abertas com dono, não divide por camada e não trata estimativa como compromisso."
model: sonnet
---
Épico: "Como lojista quero gerenciar pedidos."
Time de 3 devs, sprint de 2 semanas. Divide em histórias.
