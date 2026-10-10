---
name: negativo-usar-cli-terceiros
description: Caso negativo difícil. Pergunta sobre usar a AWS CLI, que contém a palavra CLI mas não é projetar nem revisar uma CLI. Nenhuma skill do plugin deve disparar.
tags: [cli-desktop-tooling, negativo]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: Resposta com o comando da AWS CLI e saída em JSON, sem acionar skills do plugin pela palavra CLI.
model: sonnet
---

Como listo os buckets S3 de uma região específica com o AWS CLI e salvo a saída em JSON num arquivo?
