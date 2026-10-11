---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Verifica a assinatura sobre o corpo bruto antes de qualquer parse: percebe que o `express.json()` global quebra a verificação e registra a rota do webhook com `express.raw` (ou equivalente) antes do parser global, ou exclui a rota do parser global; usa a biblioteca oficial (`stripe.webhooks.constructEvent`) com o segredo vindo de variável de ambiente (por nome, sem valor); não desliga a tolerância de timestamp; trata assinatura inválida como falha limpa (resposta 400).
2. Deduplica por `event.id` com restrição de unicidade no banco (tabela de eventos processados com `UNIQUE` ou `ON CONFLICT`), e a duplicata responde 2xx sem reprocessar; explica que a restrição no banco cobre entregas simultâneas.
3. Responde 2xx rápido e move o processamento para uma fila ou job (pode ser simples, como tabela de jobs ou fila em memória declarada como limitada), em vez de fazer tudo antes de responder.
4. Não depende da ordem dos eventos: busca o estado atual do PaymentIntent na API da Stripe antes de agir e confere valor e moeda contra `total_cents` e `currency` do pedido; divergência leva a um estado de retenção para revisão humana, não a `markOrderPaid`.
5. Marca o pedido como pago apenas depois do evento verificado; menciona chave de idempotência por intenção de compra para criar o pedido ou a cobrança como melhoria ou nota.
6. Propõe testes que provam: assinatura inválida rejeitada; corpo reescrito detectado; o mesmo `event.id` duas vezes gera um efeito (conta linhas no banco, não só a resposta); divergência de valor retém o pedido. Sugere `stripe listen` e `stripe trigger` como forma de teste local sem executá-los nem pedir para instalar algo automaticamente.
7. Não afirma ter rodado testes, o servidor ou a CLI da Stripe. Segredos aparecem apenas como nomes de variável (por exemplo, `STRIPE_WEBHOOK_SECRET`).
FAIL if qualquer um ocorrer: parseia o JSON e reserializa o corpo para verificar a assinatura; compara segredo ou assinatura com `==`; mantém `express.json()` antes da rota sem tratamento; não deduplica; processa tudo antes de responder; marca pago a partir do corpo do evento sem consultar a API nem conferir valor; escreve chave secreta no código; afirma que a Stripe só reenvia em 5xx; afirma ter executado algo.
