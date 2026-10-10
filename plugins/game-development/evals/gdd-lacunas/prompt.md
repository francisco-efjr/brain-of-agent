---
name: gdd-lacunas
description: Caso de revisão de GDD somente leitura. Mede se o plugin trata seção vazia como lacuna e nunca aprova, aponta a contradição entre dash e stamina, a dependência sem documento e a falta de critérios de aceite, não inventa números de balanceamento, devolve perguntas abertas e não grava arquivo.
tags: [game-development, gdd-review, design, read-only]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Avalia as quatro dimensões com veredito NEEDS REVISION ou MAJOR REVISION NEEDED, trata a economia vazia como lacuna, aponta a contradição dash x stamina, a dependência do Sistema de Forja sem documento e a falta de critérios de aceite, lista perguntas abertas, não inventa valores e não grava arquivo."
model: sonnet
---
Revisa esse GDD e me diz se está implementável. Vou entregar para o time de programação na segunda.

Pilares: ritmo e leitura clara.
Combate: dano = ataque - defesa, crítico 10%.
Dash: consome stamina.
Stamina: não afeta movimento.
Economia: (vazio)
Crafting: depende do Sistema de Forja (a definir).
