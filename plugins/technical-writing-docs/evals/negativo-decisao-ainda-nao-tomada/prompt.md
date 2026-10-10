---
name: negativo-decisao-ainda-nao-tomada
description: Caso negativo de fronteira - pedido para escolher entre duas tecnologias (decisão ainda não tomada) não deve acionar a skill escrever-adr, que só registra decisão já tomada, nem gravar ADR.
tags: [technical-writing-docs, negative, adr, boundary]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Compara Kafka e SQS pelos critérios do usuário, dá uma recomendação condicionada aos critérios e às suposições, não escreve nem grava ADR, não trata a escolha como decidida e oferece registrar a decisão em ADR depois que o time decidir."
model: sonnet
---
A gente precisa escolher entre Kafka e SQS para a fila de eventos de pedidos do nosso sistema e eu não sei qual é melhor. Ainda ninguém decidiu nada. Hoje são cerca de 200 eventos por segundo no pico, a equipe tem 4 pessoas, já roda tudo na AWS e nunca operou Kafka. Qual você escolheria e por quê?
