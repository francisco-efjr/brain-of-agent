---
name: juiz-com-15-exemplos
description: "Mede se o plugin desenha um juiz LLM binário com crítica curta, diz que 15 exemplos são poucos, separa treino, desenvolvimento e teste, usa TPR e TNR e juiz de outro modelo, em vez de entregar escala 1 a 10 sem calibração."
tags: [llm-ai-agents, eval-design, prompts]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega prompt de juiz com critério único binário e crítica curta antes do veredito, trata a resposta avaliada como dado, usa modelo diferente do gerador, diz que 15 exemplos são insuficientes (começar com cerca de 30 até não surgirem modos de falha novos), propõe divisão treino, desenvolvimento e teste e relata TPR e TNR, sem afirmar que o juiz funciona."
model: sonnet
---
Quero um LLM juiz (nota de 1 a 10) para avaliar as respostas do meu chatbot de atendimento de um banco digital. O que mais me preocupa é o bot afirmar uma taxa ou um prazo que não está na base de conhecimento. Tenho 15 respostas que eu mesmo rotulei como boas ou ruins. Mostra o prompt do juiz e me diz como validar que ele presta antes de eu usar como métrica no CI.
