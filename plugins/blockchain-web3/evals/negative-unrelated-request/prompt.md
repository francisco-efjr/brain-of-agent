---
name: negative-unrelated-request
description: Caso negativo que mede sobredisparo, verificando que um pedido sobre renovação de assinatura mensal de SaaS com webhook do Stripe, token JWT e liquidação de pagamento no Postgres, sem relação com blockchain, não aciona nenhuma skill do plugin nem traz conteúdo Web3.
tags: [blockchain-web3, negative, trigger]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Responde com a estrutura do fluxo de renovação (validação da assinatura do webhook do Stripe com o corpo bruto, idempotência por id de evento, validação do JWT, transação no Postgres para registrar a liquidação) sem acionar skill do plugin e sem mencionar blockchain, Solidity ou cripto."
model: sonnet
---
No meu SaaS em Node, quero renovar a assinatura mensal do cliente quando o webhook do Stripe chegar, validando o token JWT do header e registrando a liquidação do pagamento no Postgres. Como estruturo isso?
