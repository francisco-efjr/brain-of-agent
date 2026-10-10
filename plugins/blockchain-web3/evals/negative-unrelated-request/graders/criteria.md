---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final e no transcript:
1. Atende o pedido de backend: estrutura o fluxo do webhook (verificação da assinatura do evento do Stripe com o corpo bruto, tratamento idempotente por id de evento, renovação da assinatura, registro da liquidação em transação no Postgres) e trata a validação do JWT como autenticação da chamada ou do cliente, sem confundir os conceitos.
2. Não menciona blockchain, Web3, smart contract, Solidity, carteira cripto nem oráculo.
3. Não aciona skill do plugin de Blockchain e Web3 e não lê arquivos de referência desse plugin.
4. A resposta é proporcional ao pedido (estrutura e pontos de atenção), sem relatório de segurança de contrato nem checklist de auditoria.
FAIL if qualquer um ocorrer: trata "assinatura", "token" ou "liquidação" como conceitos de blockchain; aciona qualquer skill do plugin; produz checklist de auditoria de contratos.
