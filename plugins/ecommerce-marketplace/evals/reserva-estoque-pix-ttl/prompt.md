---
name: reserva-estoque-pix-ttl
description: "Caso de disparo de estoque e reserva. Última unidade, cliente gera Pix e demora, loja em Medusa v2 que só baixa estoque quando o pagamento chega. Mede escritor único, reserva com expiração da aplicação rotulada como Inferido, job de liberação com lock por carrinho, pagamento tardio, TTL de lock diferente de TTL de reserva e testes de concorrência."
tags: [ecommerce-marketplace, estoque-reserva-pedido, medusa, pix, oversell]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Propõe escritor único de estoque, reserva na conclusão do carrinho com expires_at próprio da loja (Inferido), job de liberação com lock pela chave do carrinho, pagamento após a liberação reabrindo a reserva ou retendo para revisão humana, distingue TTL de lock e de reserva, diz que a Medusa não documenta TTL de reserva e lista testes de concorrência; não afirma TTL nativo nem reembolsa sozinho."
model: sonnet
---
Tenho uma loja em Medusa v2 e um produto com uma única unidade em estoque. O fluxo hoje: o cliente fecha o carrinho, a gente gera um Pix com validade de 30 minutos e, quando o webhook de pagamento chega, um subscriber chama o `adjustInventory` do módulo de estoque e cria o pedido. O problema é que dois clientes conseguem gerar Pix para a mesma última unidade e o segundo que paga fica sem produto (já aconteceu duas vezes, tive que reembolsar na mão).

Como evito vender a mesma unidade duas vezes sem deixar a unidade presa para sempre quando o cliente desiste do Pix? Quero um desenho e a lista de testes antes de mexer em código. O código de estoque está espalhado: tem o subscriber do webhook, uma rota de admin que ajusta quantidade e um script de importação de planilha que também grava estoque.
