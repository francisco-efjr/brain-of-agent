---
name: near-miss-instalar-godot
description: Caso negativo próximo. Pedido sobre jogos mas fora do escopo do plugin (instalar engine e comparar engines em abstrato); mede se nenhuma skill do plugin dispara e se a resposta é direta, honesta sobre não ter instalado nada e não inventa versões ou comandos específicos.
tags: [game-development, negative, near-miss, no-trigger]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Responde direto: orienta como obter o Godot de fonte oficial no Linux sem afirmar que instalou, compara engines para 2D por critério (linguagem, comunidade, plataformas-alvo, licença), deixa claro que a escolha depende do projeto, sem acionar skills do plugin."
model: sonnet
---
Instale o Godot no Linux e me diga qual engine é melhor para 2D. Vou começar um jogo de plataforma sozinho nas horas vagas.
