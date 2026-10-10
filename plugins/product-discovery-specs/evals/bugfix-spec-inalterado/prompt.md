---
name: bugfix-spec-inalterado
description: Mede se o plugin escreve a spec de um bugfix com comportamento atual, esperado e inalterado, usando os valores concretos do bug, com check que falha antes e passa depois, sem inventar a causa raiz nem afirmar que reproduziu o bug.
tags: [product-discovery-specs, write-spec, bugfix, regression-guard]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Spec de bugfix com atual (subtotal de R$ 162,00), esperado (R$ 180,00) e inalterado (pelo menos três itens), reprodução mínima, check que falha antes e passa depois, perguntas abertas, causa raiz tratada como hipótese e nenhuma afirmação de que o bug foi reproduzido ou corrigido."
model: sonnet
---
Bug na nossa loja virtual: se o cliente clica duas vezes seguidas em "Aplicar" no cupom DEZ10 (10% de desconto), o desconto é aplicado duas vezes. Com um carrinho de R$ 200,00 o subtotal sai R$ 162,00 em vez de R$ 180,00. Acontece no site e, pelo que o suporte falou, no app também. Antes de eu mexer no código, escreve a spec do bugfix. Não tenho o repositório aberto aqui.
