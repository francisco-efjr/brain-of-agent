---
name: marketplace-split-carrinho-multi
description: "Caso de disparo de marketplace e split. Marketplace no Brasil com carrinho de vendedores diferentes e comissão de 10%. Mede as quatro perguntas, cobranças e transferências separadas, disponibilidade do Stripe Connect no Brasil como Não verificada, Mercado Pago Split 1:1 como candidato a verificar, KYC, estorno e ausência de ações reais no PSP."
tags: [ecommerce-marketplace, marketplace-split, stripe-connect, mercado-pago, kyc]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aplica as quatro perguntas, indica cobranças e transferências separadas para carrinho multi-vendedor, marca a disponibilidade do Stripe Connect no Brasil como Não verificada, cita o Mercado Pago Split 1:1 como candidato a conferir (vale só para 1:1), trata KYC, repasse e estorno com quem é debitado, entrega ADR com itens Não verificados e não cria conta nem cobrança em PSP."
model: sonnet
---
Estou montando um marketplace de artesanato no Brasil. O comprador pode ter no mesmo carrinho itens de três vendedores diferentes, paga uma vez (Pix ou cartão) e eu fico com 10% de comissão sobre cada item. Os vendedores são em sua maioria MEIs e pessoas físicas. Quem recebe a reclamação de produto e faz o reembolso é a plataforma, mas o dinheiro do estorno deveria sair do vendedor.

Qual tipo de cobrança eu uso e como organizo o repasse? Já pensei em Stripe Connect, mas não sei se serve para o Brasil, e vi que o Mercado Pago tem um tal de split. Quero uma recomendação fundamentada e o que preciso decidir com contador e jurídico antes de começar. Ainda não tenho conta em nenhum PSP.
