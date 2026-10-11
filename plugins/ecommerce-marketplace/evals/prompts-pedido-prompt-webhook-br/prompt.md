---
name: prompts-pedido-prompt-webhook-br
description: "Caso de disparo da biblioteca de prompts. O usuário pede um prompt pronto (não a auditoria) para revisar os webhooks do Mercado Pago e do Asaas numa sessão nova. Mede se a skill de prompts entrega um prompt em bloco com variáveis entre colchetes, dados separados por tags, fatos corretos por provedor, rótulos epistêmicos e lista de variáveis, sem executar a auditoria nem inventar resultado."
tags: [ecommerce-marketplace, prompts, webhook, mercado-pago, asaas]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um prompt pronto para colar, com variáveis [EM_COLCHETES], tags separando instruções e dados, Mercado Pago com x-signature validado pelo SDK ou doc vigente e resposta 2xx bem antes de 22 s, Asaas com token estático no cabeçalho asaas-access-token (não HMAC, nunca a API Key), dedupe por ID com restrição única, reconciliação por API, modo de teste e rótulos; lista as variáveis a trocar e a fonte com data; não audita nem afirma resultado."
model: sonnet
---
Não quero que você audite nada agora. Quero só um prompt pronto que eu vou colar numa sessão nova do Claude Code, amanhã, para revisar os webhooks do Mercado Pago (pagamentos com Pix e cartão) e do Asaas (boletos) do nosso backend Node com Express e Postgres. Estamos em sandbox nos dois provedores. Deixa os pontos que eu preciso preencher bem marcados e me diz o que trocar antes de usar.
