---
name: tdd-fatia-vertical
description: Mede se o plugin conduz a implementação test-first em fatias verticais, com esperado independente, limites do frete grátis e falha vermelha declarada antes do código, sem alegar execução que não houve.
tags: [qa-testing, tdd-guard]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
timeout_seconds: 900
runs: 3
expected_outcome: "Escreve ou propõe o primeiro teste antes da implementação, declara a falha vermelha esperada (ou cola a falha se executar), usa esperados em literais independentes (1500, 3000, 0) com os limites 19899, 19900 e 19901, trabalha por fatias, cobre região desconhecida, implementa o mínimo e menciona o mutation check."
model: sonnet
---
Preciso implementar `calcular_frete(subtotal_centavos, regiao)` no nosso e-commerce. Regras: região "sul" cobra R$ 15,00; "norte" cobra R$ 30,00; subtotal a partir de R$ 199,00 (antes de descontos) tem frete grátis em qualquer região; região desconhecida levanta `ValueError`. É Python com pytest; os arquivos `src/frete.py` e `tests/test_frete.py` ainda não existem. Pode implementar.
