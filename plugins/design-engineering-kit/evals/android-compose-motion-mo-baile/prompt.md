---
name: android-compose-motion-mo-baile
description: "Caso de adaptação por plataforma: o usuário descreve os tokens de movimento do design system Mo baile (molas, crossfade, reduzir movimento) e quer levar a animação do sheet de ajustes para Jetpack Compose, perguntando se pode copiar o linear() do CSS. Mede se o assistente traduz os princípios e tokens para spring e tween em vez de copiar CSS, trata reduzir movimento como ponto único no tema, rotula valores de Material 3 como não verificáveis e diz que Playwright não verifica Android."
tags: [design-engineering-kit, android, compose, motion, mo-baile, platform]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 420
runs: 3
expected_outcome: "Recusa copiar o linear() do CSS, traduz as molas para spring com dampingRatio igual a 1 menos o bounce e a rigidez dos tokens, o crossfade para tween de 180 ms, propõe reduzir movimento como ponto único no tema lendo a escala de animação do sistema, sugere ModalBottomSheet antes de custom, rotula Material 3 e comportamento do Compose como inferido ou não verificável, não herda estética macOS e indica emulador ou dispositivo para verificar."
model: sonnet
---
No app web da casa usamos o design system Mo baile. Os tokens de movimento dele (`tokens/motion.css`): mola `smooth` com duração perceptual de 0,5 s e bounce 0 (stiffness 157,91 e damping 25,13), mola `snappy` com 0,35 s e bounce 0,15 (stiffness 322,27 e damping 30,52), crossfade de 180 ms para trocar de seção, e "Reduzir movimento" que troca as molas por `linear` e encurta as durações, tudo por sobrescrita de token.

Agora vamos fazer a versão Android do app, em Jetpack Compose. Como levo a animação do sheet de ajustes e o "Reduzir movimento" para lá? Dá para só copiar o `linear()` do CSS para o Kotlin? Não tenho o projeto aberto; o app Android ainda não existe.
