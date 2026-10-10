---
name: rice-calculo
description: Mede se o plugin calcula RICE com aritmética correta, registra a versão da escala, mostra a sensibilidade entre itens próximos e trata o ranking como apoio à decisão, sem acrescentar dados.
tags: [product-discovery-specs, prioritize-roadmap, rice]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Scores A=1600, B=1500, C=1000, D=300 e ordem A, B, C, D; cita a escala usada; destaca que A e B estão próximos e o que inverteria a ordem; deixa a decisão com o humano e não inventa dados."
model: sonnet
---
Prioriza com RICE (trimestre). Os números abaixo vêm do time de produto:

- A: alcance 2000, impacto 2, confiança 80%, esforço 2 pessoas-mês
- B: alcance 500, impacto 3, confiança 100%, esforço 1 pessoa-mês
- C: alcance 8000, impacto 1, confiança 50%, esforço 4 pessoas-mês
- D: alcance 300, impacto 0,5, confiança 100%, esforço 0,5 pessoa-mês
