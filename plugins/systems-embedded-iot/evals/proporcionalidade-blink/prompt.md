---
name: proporcionalidade-blink
description: "Mede proporcionalidade: uma pergunta pontual e básica de Arduino deve receber resposta direta e curta, sem relatório longo, matriz de áreas nem modo EMBARCADOS-COMPLETO."
tags: [systems-embedded-iot, proporcionalidade]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Responde diretamente com o sketch mínimo (pinMode, digitalWrite, delay, usando LED_BUILTIN) e uma ou duas linhas de explicação, sem relatório longo, sem matriz de aplicabilidade, sem ativar o modo EMBARCADOS-COMPLETO e sem perguntas desnecessárias."
model: sonnet
---
Como pisco um LED no Arduino Uno? Só quero o básico.
