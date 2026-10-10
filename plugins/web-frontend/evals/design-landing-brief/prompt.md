---
name: design-landing-brief
description: Mede se o plugin conduz a criação de uma landing em Next.js com Tailwind v4 pelo processo brief, plano de tokens e revisão contra o genérico antes do código, com tokens em @theme, piso de qualidade verificável, conteúdo plausível sem fatos inventados e declaração do que não foi verificado.
tags: [web-frontend, design-ui, tailwind, tokens, landing]
max_turns: 16
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 900
runs: 3
expected_outcome: "Apresenta brief de três linhas e plano com quatro a seis cores nomeadas, papéis tipográficos e wireframe em ASCII antes de qualquer código, registra revisão com mudei X porque Y, implementa com tokens em @theme, cobre 320 px, foco visível e reduced-motion, usa texto plausível marcado como exemplo e diz o que não verificou."
model: sonnet
---
Preciso da landing page da Cooperativa Café da Serra. Somos uma cooperativa de pequenos produtores que vende café especial torrado para cafeterias e torrefadores. O objetivo da página é fazer o dono de uma cafeteria pedir uma amostra. O projeto é novo, Next.js com App Router e Tailwind v4, e ainda não temos identidade visual definida nem fotos. Me mostre o plano antes do código e depois construa a página. Idioma: português do Brasil.
