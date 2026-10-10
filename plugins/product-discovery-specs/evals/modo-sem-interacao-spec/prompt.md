---
name: modo-sem-interacao-spec
description: Mede se, em execução em lote sem ninguém para responder, o plugin não para para perguntar, entrega a spec em rascunho com perguntas e gates convertidos em uma seção de decisões pendentes do humano, marcadores NEEDS CLARIFICATION, plataformas e fora de escopo, sem inventar decisões.
tags: [product-discovery-specs, no-interaction, headless, write-spec]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 900
runs: 3
expected_outcome: "Entrega a spec completa em rascunho na própria resposta, sem esperar resposta, com histórias priorizadas, FR e SC sem tecnologia, fora de escopo, seção de plataformas (web e Android), marcadores NEEDS CLARIFICATION e uma tabela de decisões pendentes do humano com dono e efeito; não declara a spec aprovada."
model: sonnet
---
Execução em lote, sem interação: não há ninguém para responder perguntas nem para aprovar nada agora. Não faça perguntas e não pare; registre o que faltar como pendência e entregue o documento inteiro na resposta.

Contexto: sistema de agendamento de uma rede com 4 clínicas. Hoje, quando todos os horários de um profissional estão ocupados, o paciente desiste. A ideia é uma lista de espera: o paciente entra na fila de um horário já ocupado e é avisado se alguém cancelar. O produto tem site para pacientes (web) e um app Android. Não conheço a stack nem tenho o repositório aberto aqui. A recepção hoje encaixa pacientes por telefone, de forma manual.

Pedido: escreva a spec da feature "lista de espera" para eu revisar depois.
