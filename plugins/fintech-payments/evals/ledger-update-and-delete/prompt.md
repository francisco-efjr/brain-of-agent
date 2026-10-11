---
name: ledger-update-and-delete
description: "Mede se, em execução em lote sem ninguém para responder, o plugin redesenha saldo e estorno como ledger append-only com estorno ligado ao original e proteção contra saldo negativo, entregando rascunho com Suposições e Decisões pendentes do humano, sem gravar arquivos."
tags: [fintech-payments, money-ledger-design, no-interaction]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Propõe lançamentos append-only, estorno por lançamento ligado ao original com limite do saldo estornável, saldo derivado, proteção contra saldo negativo no banco, testes de concorrência e de rateio, rótulos Inferido e Verificado onde cabem, e entrega rascunho com Decisões pendentes do humano sem fazer perguntas nem gravar arquivos."
model: sonnet
---
Execução em lote, sem interação: não há ninguém para responder perguntas agora e ninguém vai aprovar nada neste momento. Não faça perguntas; registre o que faltar como pendência e entregue o trabalho até o fim em status rascunho. Não grave arquivos; entregue o texto na resposta.

Preciso de estorno parcial e de impedir saldo negativo quando dois débitos chegam juntos. Hoje fazemos `UPDATE accounts SET balance = balance - :v` depois de ler o saldo no código, e estorno é `DELETE FROM payments WHERE id = :id`. Banco: Postgres, ORM qualquer. As carteiras são em BRL e o backend atende o app Android e o painel web. Como redesenhar? Não sei se vamos aceitar outras moedas nem qual é a política de arredondamento do rateio; quem decide isso é a Marina (financeiro), que está de férias.
