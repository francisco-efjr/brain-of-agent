---
name: juiz-llm-concordancia-enganosa
description: Caso de disparo e de fidelidade estatística. Mede se o plugin explica o viés de taxa-base de uma concordância de 94 por cento quando 95 por cento dos resumos são bons, pede TPR, TNR e kappa, divisão de rótulos, especialista e prompt congelado, aponta juiz igual ao gerador e recomenda código antes de juiz.
tags: [data-science-ml, ds-llm-eval, llm-judge, evals, statistics]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Explica que um juiz que sempre aprova concordaria cerca de 95 por cento quando 95 por cento dos resumos são bons, tornando 94 por cento concordância sem valor, pede TPR e TNR, kappa, mais rótulos, especialista nomeado, divisão treino-dev-teste e prompt congelado, aponta que juiz igual ao gerador não é independente, recomenda asserções em código antes do juiz e não aprova o uso como gate de CI."
model: sonnet
---
Nosso time usa um LLM para resumir tickets de suporte e queremos medir a qualidade dos resumos automaticamente, usando o mesmo modelo que gera os resumos como juiz ("este resumo é bom? sim ou não"). Para validar o juiz, uma analista rotulou à mão 50 resumos e comparamos: o juiz concordou com ela em 47 dos 50, ou seja, 94% de concordância. Pela análise dela, 95% dos resumos da amostra são bons.

Com 94% de concordância queremos colocar o juiz como gate no CI: se a taxa de "sim" cair abaixo de 90% em 200 resumos de teste a cada deploy, bloqueia o merge. O prompt do juiz ainda está sendo ajustado, mas já deve estar perto do final. Isso está bem montado? Posso seguir?
