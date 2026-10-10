---
name: roteiro-entrevista-jtbd
description: Mede se o plugin monta um roteiro de entrevista de descoberta de 30 minutos centrado em comportamento passado, com regras anti-viés, sem perguntas hipotéticas sobre a ideia e com modelo de anotações.
tags: [product-discovery-specs, run-discovery, jtbd, interview-script]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Roteiro de cerca de 30 minutos em quatro blocos com tempo, perguntas sobre a última vez e o comportamento passado, nenhuma pergunta hipotética sobre usar um produto, regras anti-viés, premissas a confrontar e modelo de anotações com ID."
model: sonnet
---
Vou entrevistar 5 gestores de clínicas pequenas sobre como eles controlam as faltas de pacientes. Monta o roteiro.
