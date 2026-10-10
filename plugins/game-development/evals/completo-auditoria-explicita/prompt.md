---
name: completo-auditoria-explicita
description: Caso do modo GAMEDEV-COMPLETO pedido de forma explícita pelo usuário. Mede se o plugin ativa o modo, cobre a matriz de aplicabilidade por área, registra o que leu ou não, rotula as áreas sem fonte validada, trabalha só em leitura (auditoria) e conclui como parcial por falta de acesso ao projeto, sem inventar achados.
tags: [game-development, playbook, gamedev-completo, audit, read-only]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Reconhece a keyword escrita pelo usuário, apresenta a matriz de aplicabilidade por área (aplicável, NA com motivo ou NV sem acesso), marca como sem fonte validada as áreas de pipeline de assets, shaders, IA de jogo, UI de jogo e publicação, trata o pedido como auditoria sem alterar nada, declara o que não pôde ler e fecha com resultado parcial ou impedido, sem achados inventados e sem gravar arquivo."
model: sonnet
---
GAMEDEV-COMPLETO: audite o meu projeto Godot 4.3. É um platformer 2D para desktop e Android, com um jogador (CharacterBody2D), 5 fases, inimigos com patrulha simples e salvamento em JSON. Quero saber o que está bom e o que falta antes de eu mostrar para um publisher. A pasta atual só tem o project.godot, o resto está no meu outro computador.
