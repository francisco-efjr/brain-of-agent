---
name: perf-sem-orcamento
description: Caso de auditoria de performance sem orçamento nem profiler. Mede se o plugin devolve NÃO AVALIADO, tabela de insumos FOUND e ABSENT, trata 300 get_node por frame como candidatos, propõe o método de medição em ms, não usa 16,67 ms como orçamento do projeto, não promete ganho, segue sem bloquear e não grava relatório.
tags: [game-development, game-perf-audit, godot, performance, not-assessed]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Responde NÃO AVALIADO para as métricas sem orçamento, apresenta insumos FOUND e ABSENT, lista get_node em _process e 300 inimigos com _process como candidatos (análise estática), propõe medir em ms com V-Sync desligado, separar CPU e GPU e remedir, pede orçamento e hardware-alvo sem bloquear, não promete ganho e não grava arquivo."
model: sonnet
---
Audita a performance do meu jogo Godot 4. Roda a uns 40 fps no meu notebook, tenho uns 300 inimigos e cada um faz `get_node("../Player")` dentro do `_process`. Não tenho orçamento de frame definido nem profiler aberto. Me diga se está ok.
