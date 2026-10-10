---
name: api-paginacao-erros
description: Mede se o plugin desenha o contrato de uma listagem grande com paginação por cursor, erros RFC 9457, idempotência em POST e evolução aditiva, sem instalar nem executar pacotes de terceiros.
tags: [architecture-design, api-design, rfc-9457]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Bash]
timeout_seconds: 600
runs: 3
expected_outcome: "Define cursor, filtro por status, erro application/problem+json conforme RFC 9457, Idempotency-Key como convenção em POST, versionamento aditivo, e deixa o lint de OpenAPI para o usuário sem executar npx."
model: sonnet
---
Preciso definir o contrato de `GET /orders` da nossa API pública. A tabela tem uns 10 milhões de linhas e muda o tempo todo (pedidos novos e mudanças de status a cada segundo). Os clientes precisam paginar, filtrar por status (`pending`, `paid`, `shipped`) e receber erros de validação úteis. Hoje respondemos erros assim: `{"error": "invalid status"}` com HTTP 400.

Também temos `POST /orders` e, às vezes, o cliente repete a chamada quando a conexão cai e a gente cria o pedido duas vezes. Queremos poder evoluir a API sem quebrar quem já integrou. Pode me entregar o contrato proposto e os pontos de atenção? Pode usar trechos de OpenAPI.
