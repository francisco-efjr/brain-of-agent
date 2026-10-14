---
name: negativo-pergunta-conceitual
description: "Caso negativo de proporcionalidade: uma pergunta conceitual curta ('o que é TDD?') não deve acionar skill de processo nem comando do ciclo de engenharia. Mede se a resposta é direta, curta e correta, sem plano, spec, entrevista nem auditoria."
tags: [engineering-lifecycle, negative, proportionality]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Explica TDD em poucas linhas (teste que falha primeiro, implementação mínima para passar, refatoração com a suíte verde), sem acionar skill de processo, sem pedir contexto e sem relatório extenso."
---
O que é TDD? Explica em poucas linhas.
