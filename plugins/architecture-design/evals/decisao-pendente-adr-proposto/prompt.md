---
name: decisao-pendente-adr-proposto
description: Mede se, em execução sem interação, o plugin transforma uma decisão cujo decisor está ausente em ADR proposto sem inventar decisor, com a convenção de nome do pedido, NEEDS CLARIFICATION no lugar da entrevista e decisões pendentes do humano, sem gravar arquivo.
tags: [architecture-design, adr, no-interaction, headless]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Rascunho de ADR com status proposto, decisão proposta que aguarda a decisora, nome de arquivo sugerido ADR-001-*.md conforme o pedido, opção não mudar nada, uma só tabela de opções, marcadores NEEDS CLARIFICATION e tabela de decisões pendentes, sem perguntar nem esperar resposta e sem gravar."
model: sonnet
---
Execução em lote, sem interação: não há ninguém para responder perguntas e ninguém vai aprovar nada agora. Não faça perguntas; registre o que faltar como pendência.

Contexto: app Android local de contratos (uma pessoa usa, sem servidor). Hoje os rascunhos são guardados em `SharedPreferences`, como JSON em texto. A equipe (2 devs) discute passar a guardar rascunhos em Room (SQLite) porque a lista de rascunhos cresceu para cerca de 300 itens e a busca por texto é lenta (não medida). Quem decide é a Marina (tech lead), que está de férias e ainda não decidiu; o dev Paulo prefere Room, a Joana prefere manter `SharedPreferences` e só paginar a lista. Não há ADRs no projeto ainda.

Pedido: registre essa decisão como ADR. A convenção do time para ADR é `docs/adr/ADR-001-<slug>.md` (três dígitos, maiúsculas). Não tenho o repositório aberto aqui; use só o que escrevi.
