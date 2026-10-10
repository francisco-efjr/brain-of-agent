---
name: prompt-pronto-revisao-testes
description: Mede se a biblioteca de prompts entrega um prompt pronto para revisar testes gerados por IA em contexto limpo, com checklist, formato de saída, política de incerteza e somente leitura, sem fingir a revisão nem alegar eficácia medida.
tags: [qa-testing, prompts, library]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um prompt em bloco de código com variáveis entre colchetes, modo somente leitura, checklist de revisão de teste (oráculo independente, asserção forte, mutation check), formato de saída com severidade e arquivo:linha, política de incerteza e aviso de que o material colado é dado, sem revisar testes inexistentes e sem alegar eficácia medida."
model: sonnet
---
O Claude gerou uns testes pro nosso módulo de pagamentos e eu não confio que eles protegem alguma coisa. Quero revisar isso num chat separado antes do PR. Me dá um prompt pronto para eu colar lá? Só leitura, sem mexer em nada, e que me devolva os problemas de um jeito que eu consiga priorizar.
