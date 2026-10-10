---
name: negativo-react-botao
description: "Caso negativo que mede sobredisparo: um pedido de componente React com Tailwind e testes não deve acionar nenhuma skill do plugin de sistemas embarcados e IoT."
tags: [systems-embedded-iot, negative]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Entrega o componente React com Tailwind, estado de loading e testes com Testing Library normalmente, sem acionar nenhuma skill do plugin e sem mencionar firmware, gravação em hardware ou o modo EMBARCADOS-COMPLETO."
model: sonnet
---
Cria um componente React com Tailwind para um botão primário com estado de loading e testes com Testing Library.
