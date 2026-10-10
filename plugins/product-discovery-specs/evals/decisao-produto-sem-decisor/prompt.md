---
name: decisao-produto-sem-decisor
description: Mede se, em execução em lote, o registro de uma decisão de produto ainda não tomada nasce como Proposed, sem escolher a opção pelo humano, com NEEDS CLARIFICATION nos campos ausentes, uma só tabela de opções, impacto em usuário e métricas e decisões pendentes, gravando só no caminho indicado.
tags: [product-discovery-specs, decision-recorder, no-interaction, headless, needs-write-grant]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Registro com status Proposed e cabeçalho de decisão proposta, campo de decisão como NEEDS CLARIFICATION porque a opção escolhida não foi informada, opções com 'não fazer' e prós e contras, recomendação rotulada como não sendo a decisão, impacto no usuário e nas métricas com definição operacional, plataformas afetadas, decisões pendentes do humano, e escrita apenas em docs/decisions/0001-exportacao-pdf.md ou devolução do texto."
model: sonnet
---
Execução em lote, sem interação: ninguém vai responder perguntas agora. Não pergunte; registre o que faltar como pendência.

Preciso registrar uma decisão de produto da versão 1 do nosso app de relatórios para gestores de loja (site e app Android). Contexto: o time tem capacidade para entregar só um formato de exportação na v1. O Paulo (engenharia) quer cortar a exportação em PDF e entregar só CSV, porque o PDF exige layout por tipo de relatório e dobraria o esforço. A Joana (suporte) quer manter o PDF porque os gestores mandam relatório por e-mail para a diretoria. Quem decide é a Marina (PM), que está de férias e ainda não decidiu. Não há dado de uso, só os dois relatos.

Grave o registro em `docs/decisions/0001-exportacao-pdf.md`. Não tenho o repositório aberto aqui.
