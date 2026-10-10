---
name: prompt-caps-prefill
description: "Mede se o plugin revisa um system prompt com CAPS, regra sem motivo, instrução de ferramenta por medo e prefill, trocando ênfase por motivo, apontando prefill como obsoleto e propondo teste sem afirmar que testou."
tags: [llm-ai-agents, llm-prompt-review]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Troca a ênfase em CAPS por motivo e linguagem calma, dá o motivo e uma alternativa positiva para a regra sobre concorrentes, substitui 'se em dúvida use a ferramenta' por critério de quando buscar, avisa que prefill não é suportado a partir da família 4.6 e sugere saída estruturada, e propõe plano de teste sem afirmar que o prompt foi testado."
model: sonnet
---
Revise este system prompt do meu assistente de suporte (modelo-alvo: Sonnet 5.5) e devolva uma versão melhor. Na API eu também preencho a resposta do assistente com "{" para forçar JSON.

YOU ARE A SUPPORT BOT. CRITICAL: YOU MUST ALWAYS ANSWER IN JSON. NEVER, EVER mention competitors. IMPORTANT!!! If unsure, ALWAYS USE THE search_orders TOOL. Think step by step before every answer.
