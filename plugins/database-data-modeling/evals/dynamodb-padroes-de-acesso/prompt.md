---
name: dynamodb-padroes-de-acesso
description: "Mede se o plugin, diante de um pedido vago de modelar DynamoDB, levanta os padrões de acesso antes de propor chaves, em vez de entregar tabelas sem as perguntas do sistema."
tags: [database-data-modeling, nosql-data-modeling, dynamodb, access-patterns]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Antes de propor chaves, pergunta ou lista os padrões de acesso (consultas por cliente, por status, janela de tempo, volume, consistência) e só então apresenta um modelo condicional com PK, SK e GSIs rotulado como suposição, avisando que capacidade não foi verificada."
model: sonnet
---
Preciso modelar os pedidos de um e-commerce no DynamoDB. Crie as tabelas pra mim.
