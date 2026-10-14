---
name: brief-existente-sem-perguntas
description: "Existe um BRIEF.md completo e o usuário diz para continuar de onde parou. Mede se o plugin não refaz a entrevista, reconhece automation com storyboard sim como modo colaborativo com plano aprovado antes de construir, e lista os próximos passos na ordem certa."
tags: [video-hyperframes, playbook, brief, gates]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Não faz pergunta de brief (ângulo, duração, destino, regime já estão no BRIEF); reconhece automation mais storyboard yes como modo colaborativo, com o plano aprovado pelo usuário antes de construir; lista os próximos passos em ordem (preflight, fonte e fatos, design, storyboard para aprovação, quadros, revisão, preview, render só com ok); não afirma ter criado arquivos."
model: sonnet
---
O BRIEF.md do meu vídeo está abaixo. Continue de onde parou; já respondi tudo. Diga qual é o próximo passo e o que vem depois dele.

```markdown
---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Um pedido que falha três vezes não se perde: vai para a fila de mortas e pode ser reprocessado"
destination: youtube
aspect: 1920x1080
language: pt-BR
audience: desenvolvedores e operadores de plataforma
length: 90s
angle: concept
narration: no
---
## Intent
Explicar por dentro como o sistema de filas de pedidos trata falhas, sem narração, com texto na tela.
## Assets
- fonte-dos-fatos.md — fatos aprovados do sistema
## Notes
- Sem números de desempenho. Sem música.
```
