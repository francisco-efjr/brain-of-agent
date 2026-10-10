---
name: offline-notas-sync
description: Mede se o plugin desenha o offline-first de um app Android de notas com Room como fonte de verdade, fila persistente e idempotente, conflito como decisão explícita e perguntas de projeto respondidas ou assumidas, sem encerrar apenas com perguntas em execução sem interação.
tags: [mobile-apps, mobile-architecture-review, offline-first, android]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um desenho com Room como fonte canônica, escrita local primeiro, fila persistente e idempotente com backoff, WorkManager para trabalho adiável, timestamp ou versão, conflito como opção explícita com cuidado sobre o relógio e plano de teste de transição de rede, com suposições rotuladas."
model: sonnet
---
Quero um app Android de notas (Kotlin, Jetpack Compose, Room) que funcione offline e sincronize com a minha API REST quando voltar a rede. Eu edito as notas no celular e no tablet, às vezes as duas ao mesmo tempo. Desenhe a arquitetura da sincronização para eu implementar depois. Não tenho como responder perguntas agora: se faltar informação, assuma o que for mais seguro e me diga o que assumiu.
