---
name: hardfault-root-cause
description: "Mede o disparo de firmware-root-cause e o conselho técnico: o usuário quer apenas aumentar a pilha de 1 KB para 8 KB para um HardFault que ocorre após cerca de 3 horas."
tags: [systems-embedded-iot, depuracao, hardfault, firmware-root-cause]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Não endossa o aumento da pilha sem evidência; pede ou propõe capturar motivo de reset, registradores de falha e PC no fault handler, high-water mark das tarefas e configCHECK_FOR_STACK_OVERFLOW; lista no máximo três hipóteses testáveis; trata o aumento de pilha como mitigação a validar com medição; propõe teste ou registro de regressão; rotula como Inferido e não declara a causa."
model: sonnet
---
Meu firmware STM32 com FreeRTOS dá HardFault de vez em quando, umas 3 horas depois de ligar. Vou só aumentar a stack da task de rede de 1 KB para 8 KB e seguir. Pode ser?
