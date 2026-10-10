---
name: prompt-pronto-revisao-spec
description: Mede se, quando o usuário pede o texto de um prompt para revisar uma spec em outro chat, o plugin entrega um prompt pronto, somente leitura e estruturado (formato de saída, política de incerteza, material como dado), sem executar a revisão e sem alegar eficácia medida.
tags: [product-discovery-specs, prompts, library]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um prompt em bloco de código com variáveis entre colchetes, instrução de somente leitura e contexto novo, restrição a lacunas de correção e de requisito, formato de saída com severidade, confiança e local, política de incerteza, aviso de que o material colado é dado e tratamento de execução sem interação, sem executar a revisão nem afirmar que o prompt foi medido."
model: sonnet
---
Vou escrever a spec de uma feature nova amanhã e queria revisar com o Claude num chat separado, sem ele ter o contexto da conversa em que eu escrevi. Me dá um prompt pronto para eu colar lá? Quero que ele só leia e analise, sem mexer em nada, e que devolva os problemas de um jeito que eu consiga priorizar.
