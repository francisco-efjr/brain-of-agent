---
name: negativo-animacao-de-interface
description: "Caso negativo: pedido de animação de interface (modal em React com Tailwind) que não é vídeo. Mede que nenhuma skill do plugin dispara e que a resposta é direta, sem falar de HyperFrames, storyboard nem render."
tags: [video-hyperframes, negative, scope, ui-motion]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Responde direto com código de modal em React com Tailwind (fade e scale suaves, 200 ms, respeitando prefers-reduced-motion), sem invocar nenhuma skill do plugin e sem mencionar HyperFrames, storyboard, GSAP de vídeo ou render."
model: sonnet
---
Preciso de uma animação de entrada para um modal em React com Tailwind: fade e scale suaves, 200 ms, respeitando `prefers-reduced-motion`. Me mostra o código.
