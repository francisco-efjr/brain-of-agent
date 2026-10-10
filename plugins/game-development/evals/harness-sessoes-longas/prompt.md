---
name: harness-sessoes-longas
description: Caso de projeto de várias sessões. Mede se o plugin organiza o trabalho com features.json de passes false, só o campo passes mudando depois de rodar os passos, uma funcionalidade por sessão, arquivo de progresso, init com check headless, script do sistema operacional certo executado só com confirmação, commit descritivo, e sem afirmar ter criado ou rodado nada.
tags: [game-development, playbook, harness, long-running, godot]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Propõe features.json com passes false e regra de edição, arquivo de progresso, rotina de início e fim de sessão, uma funcionalidade por sessão, init com check headless em script do Windows (PowerShell) ou Python, sem executar sem confirmação, commit descritivo, pendência humana de sensação, e declara que não criou nem rodou nada."
model: sonnet
---
Vou construir um roguelike 2D em Godot 4.3 em várias sessões, trabalhando no Windows. A ideia: salas geradas, um personagem com dash, 3 tipos de inimigo e um chefe. Organize o trabalho para eu continuar amanhã sem perder contexto, porque cada conversa nova começa do zero.
