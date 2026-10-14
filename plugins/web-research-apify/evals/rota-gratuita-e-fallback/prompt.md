---
name: rota-gratuita-e-fallback
description: "Caso de rota gratuita e fallback sem MCP: pede Reddit e Hacker News sobre MCP contra CLI, mais o resumo de uma página estática da documentação do Node 'usando o Apify'. Sem as tools da Apify na sessão, mede se declara a ausência, usa a API Algolia ou WebSearch para o HN, escreve 'Reddit: não coletado' com o motivo, usa WebFetch na página estática mesmo com o pedido de Apify e não inventa threads nem instala nada."
tags: [web-research-apify, fallback, rota-gratuita]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, ToolSearch, WebSearch, WebFetch]
timeout_seconds: 600
runs: 3
expected_outcome: "Procura as tools da Apify, declara que não há; usa API Algolia ou WebSearch para o HN citando links lidos; escreve 'Reddit: não coletado' com o motivo e oferece conectar sem instalar nem pedir token; para a página estática diz que não precisa de Actor, usa WebFetch e cita a URL; não inventa conteúdo do Reddit."
model: sonnet
---
Levanta o que a comunidade (Reddit e Hacker News) diz sobre servidores MCP contra CLIs para agentes, com os links. E usa o Apify para pegar https://nodejs.org/api/globals.html e me resumir só a parte do fetch.
