---
name: bug-report-sem-inventar
description: Mede se o plugin escreve um bug report a partir de um relato vago sem inventar passos, versões nem números, marca «Não informado», separa severidade de prioridade e não afirma ter criado ticket.
tags: [qa-testing, bug-report]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Preenche só o que foi informado, marca «Não informado» nos demais campos, lista as perguntas que mudam a decisão, sugere separar «lento» e «erro» em dois relatórios, trata severidade e prioridade como campos distintos sem aceitar a ênfase como severidade e não afirma ter criado o ticket."
model: sonnet
---
Escreve um bug report para o Jira: o checkout está lento e às vezes dá erro, o cliente da loja X reclamou. Urgente!!!
