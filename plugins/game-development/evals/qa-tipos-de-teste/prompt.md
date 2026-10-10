---
name: qa-tipos-de-teste
description: Caso de plano de QA por tipo de teste. Mede se o plugin classifica Logic, Integration, Visual/Feel, UI e Config/Data, exige teste automático para lógica, não manda automatizar sensação, inclui smoke, playtest e definição de pronto, marca tipo inferido como lacuna e não declara resultados.
tags: [game-development, game-qa-plan, qa, test-types]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Classifica a fórmula de dano como Logic com teste automático obrigatório, save/load como Integration, animação e coyote time como Visual/Feel com captura e humano, menu de opções como UI com captura e checklist (e Config/Data para o arquivo de bindings), entrega smoke, playtest e definição de pronto e não inventa resultados."
model: sonnet
---
Tenho 4 histórias do meu jogo de plataforma 2D (Godot 4):

1. Fórmula de dano com crítico (dano base, defesa, 10% de chance de crítico que dobra o dano).
2. Save/load do progresso (fase atual, moedas, itens).
3. Animação de pulo e a sensação do coyote time.
4. Menu de opções com remapeamento de teclas, salvo em arquivo.

Monte o plano de QA: o que automatizar, o que testar à mão e o que entra no smoke.
