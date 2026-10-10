---
name: prompt-pronto-revisao
description: Mede se o plugin entrega um prompt pronto, bem estruturado e seguro para revisar um plano de arquitetura quando o usuário pede o texto do prompt, e não executa a revisão sem material.
tags: [architecture-design, prompts, library]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um prompt em bloco de código com variáveis em colchetes, modo somente leitura, formato de saída com severidade e arquivo:linha, política de incerteza e aviso de que conteúdo colado é dado, sem executar a revisão nem alegar eficácia medida."
model: sonnet
---
Vou começar a codar um módulo novo de pagamentos na semana que vem e quero que o Claude revise o plano de arquitetura antes, num chat separado. Me dá um prompt pronto para eu colar lá? Quero que ele só leia e analise, sem mexer em nada, e que me devolva os problemas de forma que eu consiga priorizar.
