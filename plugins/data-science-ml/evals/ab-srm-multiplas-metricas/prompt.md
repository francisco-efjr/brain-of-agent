---
name: ab-srm-multiplas-metricas
description: Caso de disparo e de fidelidade estatística. Mede se o plugin lê SRM primeiro num A/B planejado 50/50 com 50.800 contra 49.200 usuários, aponta multiplicidade de 12 métricas por 4 segmentos, trata o segmento mobile como exploratório, pede métrica primária e intervalo e não recomenda lançar com p igual a 0,03.
tags: [data-science-ml, ds-inference-review, ab-test, srm, multiplicity]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Calcula ou reconhece o SRM (qui-quadrado próximo de 25,6 com 1 grau de liberdade, p muito menor que 0,001) e bloqueia a leitura do resto até explicar a causa, aponta a multiplicidade de 12 métricas por 4 segmentos e o segmento mobile não pré-registrado como exploratório, pede métrica primária, efeito com intervalo e regra de parada, e não recomenda lançar."
model: sonnet
---
Rodamos um teste A/B do novo fluxo de checkout durante duas semanas. O plano era 50/50 entre controle (A) e variante (B), randomizando por usuário, com 100.000 usuários elegíveis. O que a ferramenta mostrou:

```text
Usuários no experimento: A = 50.800   B = 49.200   (total 100.000)
Métricas acompanhadas: 12 (conversão, receita por usuário, ticket médio, itens por pedido, tempo no checkout, abandono de carrinho, uso de cupom, reclamações, reembolsos, NPS, retorno em 7 dias, retorno em 14 dias)
Segmentos analisados: 4 (desktop, mobile, novos usuários, recorrentes)
Resultado destacado pela ferramenta: receita por usuário em mobile, B contra A: +4,1%, p = 0,03
Conversão geral: B +0,6%, p = 0,21
```

A variante B ganhou na receita em mobile, que é o nosso maior canal. Posso mandar lançar para todo mundo? Preciso de uma resposta de revisão, não de uma nova análise: não tenho os dados brutos à mão.
