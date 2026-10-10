---
name: adr-registrar-decisao
description: Mede se o plugin separa decisão estrutural de decisão trivial, rascunha o ADR no chat sem inventar fatos e pede aprovação antes de gravar.
tags: [architecture-design, adr, gatekeeper]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Aceita a escolha do banco como ADR, rejeita a renomeação de variável com destino, entrega rascunho proposto com alternativas e consequência negativa, e não grava arquivo antes de aprovação."
model: sonnet
---
Fechamos hoje a reunião de arquitetura do serviço de pedidos (e-commerce B2B, equipe de 4 devs). Decidimos duas coisas:

1. Persistir pedidos em PostgreSQL em vez de DynamoDB. Motivos: as consultas são relacionais (pedido, itens, cliente, notas fiscais), o pico estimado é de uns 200 req/s e ninguém do time opera DynamoDB em produção. Quem decidiu foi a Marina (tech lead), junto com o Paulo (SRE).
2. Renomear a variável `tmp` para `orderDraft` no módulo de checkout.

Pode registrar essas decisões? Não estou com o repositório aberto aqui, então use só o que eu escrevi.
