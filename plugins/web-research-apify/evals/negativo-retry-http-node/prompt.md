---
name: negativo-retry-http-node
description: "Caso negativo de sobredisparo: pergunta de backend sobre retry com backoff exponencial em chamadas fetch no Node 22, tratando 429 e Retry-After, não deve acionar nenhuma skill do plugin de pesquisa com Apify e deve receber resposta técnica direta."
tags: [web-research-apify, negative, backend]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Responde direto com backoff exponencial com jitter, respeito a Retry-After, limite de tentativas, só métodos idempotentes e exemplo curto de fetch no Node 22, sem acionar skill do plugin e sem tratar como pesquisa com Apify."
model: sonnet
---
Como implemento retry com backoff exponencial em chamadas fetch no Node 22, sem biblioteca? Preciso tratar 429 e Retry-After.
