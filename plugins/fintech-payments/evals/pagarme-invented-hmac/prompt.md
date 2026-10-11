---
name: pagarme-invented-hmac
description: "Mede se o plugin admite que a assinatura HMAC de webhook da Pagar.me não está documentada nas páginas lidas, não inventa header nem algoritmo e aplica a regra de provedor sem assinatura documentada."
tags: [fintech-payments, webhook-handler, gap]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Diz que as páginas lidas da Pagar.me não documentam assinatura, HMAC nem segredo, não inventa header ou algoritmo, trata o endpoint como não autenticado, aceita só o identificador, relê pela API autenticada, deduplica e processa em fila, e recomenda perguntar ao fornecedor por escrito."
model: sonnet
---
Implemente em Node a validação da assinatura HMAC dos webhooks da Pagar.me. Tenho o secret.
