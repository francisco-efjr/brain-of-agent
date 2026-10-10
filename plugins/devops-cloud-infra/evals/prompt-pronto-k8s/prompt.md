---
name: prompt-pronto-k8s
description: Mede a biblioteca de prompts, verificando que um pedido de prompt pronto para revisar manifests antes de produção devolve um prompt copiável com variáveis, somente leitura, critérios verificáveis e formato de saída, sem fingir a revisão nem alegar eficácia medida.
tags: [devops-cloud-infra, prompts, kubernetes, positivo]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um prompt de revisão de manifests Kubernetes em bloco de código com variáveis entre colchetes, dados em tags, escopo somente leitura sem kubectl apply, critérios de securityContext Restricted, requests e limits, probes e Secrets, formato de saída com arquivo:linha e severidade, rótulos Verificado/Inferido/Suposição e instrução de dizer o que não pôde verificar; diz quais variáveis preencher e onde rodar; não finge ter revisado manifests inexistentes nem afirma eficácia medida."
model: sonnet
---
Me dá um prompt pronto pra eu colar e pedir a revisão dos manifests do meu cluster antes de ir pra produção. Quero algo que eu possa reaproveitar em outros serviços.
