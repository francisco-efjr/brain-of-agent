---
name: negative-near-miss-qa
description: "Caso negativo de vizinho próximo que mede sobredisparo: um pedido de estratégia de testes (pirâmide e e2e) é de outro segmento e não deve acionar nenhuma skill deste plugin."
tags: [code-quality-refactoring, negative, near-miss, qa]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Responde diretamente com uma estratégia de testes para o checkout (distribuição entre unitário, integração e e2e) ou indica que o tema é de estratégia de testes, sem acionar nenhuma skill do plugin."
model: sonnet
---
Preciso montar a estratégia de testes do checkout do nosso e-commerce. O que fica em teste unitário, o que vai pra integração e o que vale a pena cobrir com e2e no Playwright? E mais ou menos quantos testes de cada tipo? Somos 4 devs, o checkout tem carrinho, cupom de desconto, frete, pagamento com cartão e Pix, e confirmação de pedido.
