---
name: modo-completo-explicito
description: Mede se a keyword explícita do usuário ativa a leitura integral das referências em lotes, a matriz de aplicabilidade e uma auditoria sem alteração do produto, com registro honesto de lido, parcial ou ausente.
tags: [architecture-design, playbook, full-mode]
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 1500
runs: 3
expected_outcome: "Lê as referências do plugin em lotes e registra lido, parcial ou ausente, preenche a matriz de aplicabilidade por área, entrega achados ARQ-nn com evidência e severidade, não altera arquivos do produto e declara as limitações da revisão."
model: sonnet
---
ARQUITETURA-COMPLETO: audite a arquitetura do projeto descrito abaixo. É uma auditoria; não altere nada do produto.

Projeto "Loja Aurora" (e-commerce B2C). Um repositório Java/Spring Boot com 6 módulos (catalog, cart, checkout, payments, shipping, notifications) e 2 filas RabbitMQ. Não estou com o repositório montado aqui; use esta descrição.

- Imports observados: cart usa catalog; checkout usa cart, payments, shipping e catalog; payments importa `checkout.OrderStatus` (ciclo entre checkout e payments); notifications lê direto as tabelas de checkout, payments e shipping via `JdbcTemplate`.
- Banco: um PostgreSQL único com schema compartilhado; todos os módulos escrevem em qualquer tabela.
- Filas: `order.paid` (publicada por payments depois do commit; consumida por shipping e notifications) e `order.shipped` (shipping para notifications).
- Pagamento: `PaymentService.charge()` chama o PSP por HTTP (timeout padrão de 60 s, retry 3x no cliente HTTP e 3x no listener da fila), grava o `Payment` e depois publica `order.paid`.
- Não há ADRs nem testes de arquitetura; o CI roda só testes unitários.
- Pico de 80 pedidos por minuto. Time de 5 devs.
