---
name: contrato-quebra-compat
description: Mede se o plugin classifica cada mudança de contrato como compatível ou breaking (incluindo enum novo em resposta), considera clientes mobile que não atualizam na hora, propõe alternativa compatível e plano de deprecação sem inventar saída de ferramenta.
tags: [backend-api, api-contract-design, mobile]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Classifica as quatro mudanças como breaking, explica o enum novo em resposta, considera apps em campo e parceiros, propõe alternativas compatíveis com coexistência e Deprecation/Sunset, sugere validador de spec rotulado como não executado e não aprova a publicação como está."
model: sonnet
---
Vou publicar esta mudança na API v1 amanhã de manhã. Posso publicar?

1. `POST /orders` passa a exigir o campo `taxId` no corpo.
2. O campo `status` de `GET /orders/{id}` ganha o valor novo `REFUNDED` (hoje: `PENDING`, `PAID`, `CANCELLED`).
3. `GET /orders?page=2` deixa de existir e vira `GET /orders?cursor=<token>`.
4. Removo `items[].sku` das respostas, porque agora existe `items[].productId`.

Consumidores: o app Android (versões 3.x em campo, não dá para forçar atualização), o app iOS, a SPA web e dois parceiros que integram direto pela API v1. Não tenho a spec aqui; considere só o que escrevi.
