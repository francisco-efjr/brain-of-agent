---
name: modo-completo-explicito
description: Mede se a keyword PRODUTO-COMPLETO escrita pelo usuário ativa a leitura integral das referências em lotes, a matriz de aplicabilidade por área, a produção dos artefatos aplicáveis em rascunho com gates respeitados e a revalidação honesta, sem ação externa.
tags: [product-discovery-specs, playbook, full-mode]
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 1500
runs: 3
expected_outcome: "Lê as referências do playbook em lotes registrando lido, parcial ou ausente, entrega a matriz de aplicabilidade por área com justificativa, produz em rascunho os artefatos das áreas aplicáveis sem inventar dados, respeita os gates e as pendências do humano, revalida com os checklists e declara que revisão do mesmo modelo não é validação externa, sem criar issues nem outras ações externas."
model: sonnet
---
PRODUTO-COMPLETO: prepare a descoberta e a especificação da iniciativa descrita abaixo. É planejamento de produto; não implemente nada e não crie issues nem publique nada.

Escola "Aprender+" (cerca de 200 alunos, 2 devs no time). Hoje a mensalidade é cobrada por boleto e, segundo o financeiro, 18% das mensalidades do mês passado atrasaram. Querem oferecer pagamento por Pix no app de pais (Android e iOS) e no portal web. Não existe PRD. Não conheço a stack e não tenho o repositório aberto aqui. A secretaria concilia pagamentos à mão numa planilha. Os pais reclamam de que o boleto vence em dias não úteis. Não há pesquisa com pais; o financeiro e a secretaria podem ser entrevistados.
