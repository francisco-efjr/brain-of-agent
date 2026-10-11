---
name: spec-downgrade-assentos
description: Mede se o plugin escreve uma spec testável de convites com limite por plano e downgrade, com requisitos de isolamento, autorização, billing idempotente, limites e downgrade sem apagar dados, aceite com dois tenants, fora de escopo, gate de bloqueio e Suposições, sem começar a implementar e com no máximo duas perguntas materiais.
tags: [saas-multitenant, saas-feature-spec, spec, plans]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega spec com REQ numerados de isolamento, autorização por papel, eventos de billing idempotentes e fora de ordem, limites por plano e downgrade sem apagar dados, critérios de aceite Given/When/Then com teste negativo entre dois tenants, fora de escopo, gate, Suposições e marcadores de esclarecimento, sem código e com no máximo duas perguntas."
model: sonnet
---
Preciso da spec de uma feature para o nosso SaaS B2B (cada empresa cliente é um tenant): convites de usuários com limite por plano e downgrade de plano. Os planos são Free com 3 assentos, Pro com 10 e Business com 50. Quem paga é a empresa, no cartão, pela Stripe; o plano muda por upgrade ou downgrade pelo portal de cobrança. Hoje qualquer admin do tenant convida por e-mail sem limite, e o convite expira em 7 dias.

Escreve a spec. Não implemente nada e entregue o texto na resposta, sem gravar arquivos. Não sei ainda o que deve acontecer se uma empresa com 10 usuários fizer downgrade de Pro para Free; se faltar algo que muda a spec, pergunte, mas só o essencial.
