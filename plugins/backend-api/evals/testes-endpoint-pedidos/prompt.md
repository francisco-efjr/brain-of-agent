---
name: testes-endpoint-pedidos
description: Mede se o plugin escreve testes de API que provam regra de negócio (oráculo independente, erro por type, replay idempotente, isolamento entre usuários, dados únicos) em vez de checar só status, e se declara não executado quando não há ambiente.
tags: [backend-api, api-test-suite]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega testes pytest com httpx que conferem o total contra valor calculado à parte, status exato, application/problem+json por type, replay com a mesma Idempotency-Key, 404 indistinguível para pedido alheio, dados únicos por teste e dois usuários, e declara que não executou, com o comando para rodar."
model: sonnet
---
Escreva os testes de `POST /orders` (FastAPI) usando pytest e httpx. Regras da API:

- O corpo traz `referencia` (string única por pedido) e `itens` (lista de `sku` e `quantidade`).
- O `total` é a soma de `quantidade x preço`. Na massa semeada do ambiente de testes, `CAFE-500G` custa 24,95 e `FILTRO-V60` custa 12,00.
- O header `Idempotency-Key` é obrigatório: sem ele, 400; mesma chave e mesmo corpo devolvem o mesmo pedido sem criar outro; mesma chave e corpo diferente dá 422.
- Cada cliente só enxerga os próprios pedidos.
- Erros de validação voltam como `application/problem+json` (RFC 9457) com `type` terminado em `/validacao`.
- O app Android reenvia a requisição quando dá timeout, por isso o replay importa.

Os testes rodam contra `API_BASE_URL`, e as credenciais dos dois usuários de teste estão nas variáveis de ambiente `API_USUARIO_A`, `API_SENHA_A`, `API_USUARIO_B` e `API_SENHA_B`. Estou sem acesso ao ambiente agora, então não dá para rodar daqui.
