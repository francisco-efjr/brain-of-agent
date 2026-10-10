---
name: modo-sem-interacao-rascunho
description: Mede se, em execução em lote sem ninguém para responder, o plugin entrega o contrato completo como rascunho com suposições rotuladas e uma seção de decisões pendentes do humano, cobrindo cliente mobile, sem fazer perguntas bloqueantes nem gravar arquivos.
tags: [backend-api, api-contract-design, no-interaction, mobile]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega o contrato de exportação assíncrona como rascunho completo (202 com monitor, estados, lista com cursor, erros RFC 9457, idempotência, autorização por dono), rotula Suposições, inclui Decisões pendentes do humano com opções e impacto, trata o app Android em campo e não grava arquivos nem espera resposta."
model: sonnet
---
Execução em lote, sem interação: não há ninguém para responder perguntas agora e ninguém vai aprovar nada neste momento. Não faça perguntas; registre o que faltar como pendência e entregue o trabalho até o fim em status rascunho. Não grave arquivos; entregue o texto na resposta.

Contexto: API de uma plataforma de notas fiscais. Usuários pedem a exportação de notas de um período em CSV pelo app Android (versões antigas ficam meses em campo) e pelo painel web. A geração pode levar de segundos a alguns minutos. Hoje não existe endpoint de exportação, só `GET /invoices` (sem paginação). Quem vai decidir a estratégia de versionamento da API e a retenção dos arquivos é a Helena (tech lead), que está em viagem. Não sei se há parceiros que também vão usar isso.

Pedido: desenhe o contrato do recurso de exportação (criação, acompanhamento, download e listagem das exportações do usuário). Não tenho o repositório aberto aqui; use só o que escrevi.
