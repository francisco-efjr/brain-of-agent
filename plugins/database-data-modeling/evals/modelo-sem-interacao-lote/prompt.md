---
name: modelo-sem-interacao-lote
description: "Mede o modo sem interação: o pedido avisa que ninguém responderá perguntas. O plugin deve entregar o modelo completo como rascunho, com suposições rotuladas e uma seção de decisões pendentes do humano, em vez de parar para perguntar."
tags: [database-data-modeling, db-schema-and-sql, non-interactive, postgresql]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega DDL em rascunho para reservas de quadras (invariante contra reservas sobrepostas no banco, dinheiro em NUMERIC, timestamptz, FKs com índice), com suposições rotuladas e a seção Decisões pendentes do humano, sem parar para perguntar."
model: sonnet
---
Estou rodando isto em lote, de madrugada, e ninguém vai estar disponível para responder perguntas. Entregue o que conseguir sem me perguntar nada.

Preciso do modelo de dados (PostgreSQL 16) de um sistema de reservas de quadras de padel: clubes têm várias quadras, jogadores fazem reservas de uma quadra por um intervalo de horário, cada reserva tem um pagamento (valor em reais, status), e o clube cobra preços diferentes por quadra e por faixa de horário. Duas reservas não podem se sobrepor na mesma quadra. Ainda não definimos política de cancelamento nem se haverá mais de um fuso horário (os clubes estão só no Brasil, por enquanto).
