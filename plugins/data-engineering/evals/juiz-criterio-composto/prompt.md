---
name: juiz-criterio-composto
description: "Mede se o juiz binário recusa um critério composto e um pedido de nota, devolvendo erro estruturado em vez de julgar, e se julga corretamente um critério único com evidência literal."
tags: [data-engineering, eval-judge, evals, agent]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Agent]
timeout_seconds: 600
runs: 3
expected_outcome: "Para o critério composto devolve erro criterio_composto pedindo um critério por chamada; para o critério único devolve falha true ou false com trecho literal; não dá nota numérica nem aprova entrega."
model: sonnet
---
Preciso calibrar o juiz das minhas skills de dados. Rode o juiz binário nas duas chamadas abaixo.

Chamada 1. Critério: "A saída compara a contagem de origem e destino e também cita a versão do Spark?" Saída s1: "Origem 5458, destino 1493: carga truncada. Versão do Spark não informada."

Chamada 2. Critério: "A saída declara o pipeline aprovado apenas porque o build passou, sem comparar contagem de origem e destino?" Saída s1: "Build verde com 26 testes, pode mergear." Saída s2: "Build verde, mas a origem informa 5458 linhas e o destino 1493; não aprovo."

Depois da chamada 2, me dê também uma nota de 1 a 5 para a qualidade geral de s2.
