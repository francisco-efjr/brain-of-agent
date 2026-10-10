---
name: rag-ou-fine-tuning
description: "Mede se o plugin aplica o gate de contexto e de fine-tuning antes de indexar ou treinar: manual pequeno cabe no contexto, exige suíte própria, não promete fine-tuning direto de Claude e rotula suposições."
tags: [llm-ai-agents, llm-decision-gates]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aplica o gate: uma base de 120 páginas cabe no contexto (abaixo de cerca de 500 páginas ou 200 mil tokens, a confirmar contando tokens), recomenda prompt completo com cache e sem RAG, exige suíte de avaliação própria antes de qualquer investimento, não promete fine-tuning direto de Claude na API e rotula Inferido ou Suposição."
model: sonnet
---
Na empresa temos um manual interno de 120 páginas (PDF) e um FAQ de 40 perguntas e respostas, que muda umas duas vezes por ano. Queremos um assistente que responda dúvidas dos atendentes com base nisso. Meu chefe quer fazer fine-tuning do Claude com esses documentos; um colega quer montar RAG com banco vetorial, chunking e reranker. Qual dos dois a gente faz? Já adianto que ainda não temos nenhuma forma de medir qualidade das respostas.
