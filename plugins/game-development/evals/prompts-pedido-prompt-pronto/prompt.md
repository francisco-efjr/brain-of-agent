---
name: prompts-pedido-prompt-pronto
description: Caso da biblioteca de prompts. Pedido de um prompt pronto (não da execução da tarefa). Mede se a skill prompts dispara, entrega o prompt de diagnóstico de movimento com as variáveis ainda visíveis, preenche só o que a conversa trouxe, não inventa versão nem diagnóstico e oferece executar se a pessoa colar o código.
tags: [game-development, prompts, library, godot]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um prompt em bloco de código para diagnosticar movimento lento no Godot 4, com o sintoma preenchido e as variáveis de script e versão ainda entre colchetes, diz onde rodar (somente leitura) e por que funciona, lista o que falta preencher, oferece executar o diagnóstico se o script for colado e não afirma que o script tem ou não o problema."
model: sonnet
---
Me dá um prompt pronto para eu revisar o movimento do meu personagem no Godot, ele anda devagar demais. Vou colar num subagente depois.
