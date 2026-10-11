---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Explica a causa provável da cobrança dupla e do acesso errado: nenhum controle de duplicado (o mesmo evento reentregue estende `paidUntil` de novo), ordem de entrega não garantida, e concessão de acesso por eventos isolados e pela página de sucesso.
2. Aponta que `express.json()` global antes da rota impede a verificação da assinatura (que exige o corpo bruto) e que não há verificação de `Stripe-Signature` com o segredo `whsec_` guardado em variável de ambiente ou cofre.
3. Propõe o fluxo seguro: corpo bruto; assinatura verificada com falha respondendo 400; `event.id` gravado em tabela com restrição UNIQUE antes de agir (duplicado responde 200 sem efeito); resposta 2xx antes da lógica pesada com fila; worker que busca o objeto atual (assinatura) na API em vez de confiar no payload ou na ordem; evento sem tenant mapeado registrado e alertado.
4. Define o acesso por tabela de status da assinatura (por exemplo `trialing` e `active` liberam; `unpaid`, `canceled`, `incomplete_expired` revogam) e não por redirect de checkout nem por `invoice.paid` isolado; diz que a página `/sucesso` não deve conceder acesso, só informar; trata `past_due` e `paused` como decisão de produto a registrar (com sugestão, rotulada como tal) e não como regra técnica.
5. Lista os testes: evento duplicado, evento fora de ordem (`invoice.paid` antes de `customer.subscription.created`), assinatura inválida e corpo alterado, e diz que contará linhas no banco, não só a resposta.
6. Não pede, não cola e não escreve chave real (`sk_`, `whsec_`); usa placeholder ou variável de ambiente; declara que não executou nada e que confirmará nomes de métodos do SDK na versão instalada.
FAIL if qualquer um ocorrer: confia na ordem ou no payload; mantém `express.json()` antes da verificação; aceita o webhook sem assinatura; mantém a concessão de acesso pelo `success_url`; trata `invoice.paid` como prova suficiente de `active`; pede ou escreve chave real; afirma que testou o webhook.
