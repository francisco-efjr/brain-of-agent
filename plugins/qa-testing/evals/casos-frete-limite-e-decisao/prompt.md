---
name: casos-frete-limite-e-decisao
description: Mede se o plugin deriva casos de teste com técnica explícita (tabela de decisão e valor-limite de três valores), dados concretos e esperado calculado, e trata as ambiguidades como pergunta em vez de inventar.
tags: [qa-testing, test-design]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Usa tabela de decisão (completa ou colapsada) e valor-limite com 198,99, 199,00 e 199,01; entrega casos com ID, dados concretos, esperado em reais, prioridade e técnica em tabela colável; declara ou pergunta as ambiguidades do limite e da ordem dos descontos; isola uma condição inválida por caso."
model: sonnet
---
Preciso de casos de teste para esta regra do checkout: frete grátis para subtotal a partir de R$ 199,00 ou para cliente VIP; cupom dá 10% de desconto; cliente VIP dá 5%; cupom e desconto VIP não acumulam (vale o cupom). Me entregue os casos prontos para colar na planilha do time.
