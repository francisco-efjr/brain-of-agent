---
name: experimento-peeking
description: Mede se o plugin identifica o erro de espiar o teste A/B e parar ao ver significância, calcula a amostra pela regra de bolso com os números dados e rejeita um plano de 10 mil visitantes por braço como insuficiente.
tags: [product-discovery-specs, run-discovery, ab-testing, peeking]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta que olhar todo dia e encerrar quando o p-valor cai abaixo de 0,05 infla o falso positivo; calcula cerca de 24,6 mil por braço pela regra n = 16 sigma ao quadrado sobre delta ao quadrado, rotulada como regra de bolso; diz que 10 mil é insuficiente; propõe amostra e parada fixas antes ou análise sequencial com checkpoints."
model: sonnet
---
Vou rodar um A/B de checkout com 10 mil visitantes por braço. Pretendo olhar o resultado toda manhã e encerrar assim que o p-valor cair abaixo de 0,05. A taxa de conversão atual é 4% e quero detectar um aumento de 0,5 ponto percentual. Está bom?
