---
name: pergunta-pontual-sem-referencias
description: Caso de proporcionalidade. Pergunta conceitual curta sobre SRM em teste A/B. Mede se a resposta é direta e curta, com a conta do qui-quadrado explicada, sem relatório longo, sem modelo de artefato e sem carregar as referências do playbook.
tags: [data-science-ml, proportionality, ds-inference-review, srm]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Explica em poucas linhas que SRM é a diferença entre as contagens observadas por braço e a razão planejada, que se testa com qui-quadrado de aderência, que p muito pequeno (convenção p < 0,001) indica problema de atribuição ou de logging e bloqueia a leitura dos efeitos, sem ler referências nem montar relatório."
model: sonnet
---
O que é SRM num teste A/B e como eu sei se o meu tem? Responde em poucas linhas, é só para eu entender o conceito.
