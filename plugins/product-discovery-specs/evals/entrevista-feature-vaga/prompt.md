---
name: entrevista-feature-vaga
description: Mede se o plugin entrevista antes de especificar uma feature vaga (login com Google), com no máximo 3 perguntas por rodada, sem repetir a stack informada, sem escrever código e sem tratar "já pode começar" como aprovação.
tags: [product-discovery-specs, spec-interview, interview, needs-write-grant]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Não escreve código nem arquivos; faz no máximo 3 perguntas abertas ou um play back com até 3 perguntas; não repergunta a stack; levanta ao menos uma regra implícita (conta existente com o mesmo e-mail ou perda de acesso ao Google) e o fora de escopo; admite não ver o repositório e oferece um SPEC.md com [NEEDS CLARIFICATION] para aprovação."
model: sonnet
---
Quero adicionar login com Google no meu app de agenda de consultas (Next.js + Postgres; hoje só e-mail e senha). Os pacientes se cadastram sozinhos pelo site. Já pode começar?
