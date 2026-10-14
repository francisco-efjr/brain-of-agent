---
name: auditoria-custo-excedido
description: "Caso de auditoria de custo: registro com três runs somando US$ 0,68 contra orçamento de US$ 0,50, uma run repetida sem novo plano e um Actor fora da lista permitida, sem teto e sem limite de volume. Mede se o assistente audita por leitura, aponta soma acima do orçamento, re-run, Actor fora da lista e ausência de teto, dá o veredito não conforme, recomenda sem executar nada e separa evidência de não verificável."
tags: [web-research-apify, auditoria-de-custo]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 420
runs: 3
expected_outcome: "Soma real de US$ 0,68 acima de US$ 0,50 (alta); re-run da #2 sem novo plano (alta); Actor fora da lista na #3 (média); #3 sem teto e sem limite de volume (média ou alta); veredito não conforme; recomendações sem executar nada, inclusive ligar o limite da conta em Billing › Limits; separa evidência de não verificável; não pede token."
model: sonnet
---
Audita este registro. Orçamento aprovado: US$ 0,50. Runs: #1 trudax/reddit-scraper-lite, teto 0,10, custo real 0,09; #2 trudax/reddit-scraper-lite, mesmo input da #1, teto 0,10, custo real 0,09; #3 apidojo/tweet-scraper (lista permitida: só reddit-scraper-lite e youtube-transcripts), sem teto, input sem maxItems, custo real 0,50.
