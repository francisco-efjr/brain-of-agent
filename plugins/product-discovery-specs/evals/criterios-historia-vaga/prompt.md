---
name: criterios-historia-vaga
description: Mede se o plugin aponta palavras vagas numa história, converte em perguntas e critérios mensuráveis rotulados como Suposição, cobre caminho negativo e escreve cenários declarativos na ordem feliz, falhas e não funcionais.
tags: [product-discovery-specs, acceptance-criteria, vague-words]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta rápido, vários formatos, etc. e seguro como vagos, faz perguntas, propõe critérios mensuráveis com limites marcados como Suposição ou pergunta aberta, inclui ao menos um caminho negativo, escreve cenários declarativos em ordem feliz, falhas, não funcionais e pergunta ou declara o canal (web, app, API)."
model: sonnet
---
História: "Como gerente quero exportar relatórios para analisar dados."
Critérios que o time anotou: o export deve ser rápido, suportar vários formatos etc. e ser seguro.

Escreve os critérios de aceite dessa história.
