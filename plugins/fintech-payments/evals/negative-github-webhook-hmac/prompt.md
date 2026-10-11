---
name: negative-github-webhook-hmac
description: "Mede sobredisparo de quase-acerto: pergunta sobre webhook do GitHub com HMAC e dedupe, sem dinheiro, não deve acionar skills de pagamentos; a resposta deve ser técnica e sem regras de ledger, Pix ou PCI."
tags: [fintech-payments, negative, scope]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Responde sobre X-Hub-Signature-256 (HMAC-SHA256 do corpo bruto, comparação em tempo constante) e dedupe pelo ID do delivery, sem acionar skills do plugin de pagamentos e sem trazer ledger, Pix ou PCI."
model: sonnet
---
Tenho um serviço Express que recebe o webhook `push` do GitHub e dispara um deploy. Como valido o header `X-Hub-Signature-256` corretamente e evito processar o mesmo delivery duas vezes?
