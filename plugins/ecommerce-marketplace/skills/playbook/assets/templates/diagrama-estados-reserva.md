# Estados de reserva de estoque e do pedido

Uso: projetar ou revisar reserva com expiração, baixa e ciclo de vida do pedido sem oversell. O TTL de reserva é responsabilidade da aplicação (**Inferido**; o módulo de inventário da Medusa não documenta expiração, V-39, V-48). TTL de lock (segundos) ≠ TTL de reserva (minutos). Plataforma e versão: [X].

## 1. Estados da reserva
```text
held --(pagamento verificado, com lock)--> confirmed --(fulfillment)--> consumed
held --(expires_at vencido, sem pagamento)--> expired
expired --(pagamento tardio e há saldo)--> confirmed
expired --(pagamento tardio sem saldo)--> review   (retenção; humano decide; sem reembolso autônomo)
held/confirmed --(cancelamento antes do envio)--> released
```
Ajuste o diagrama à sua plataforma; remova estados que não existem e acrescente os que existem.

## 2. Tabela de transições
| De | Para | Quem dispara | Condição | Responsável (serviço) | Idempotência | Teste |
| --- | --- | --- | --- | --- | --- | --- |
| held | confirmed | Evento de pagamento verificado | Lock pela chave do carrinho; valor/moeda/hash conferem | [InventoryService] | Chave = carrinho + evento | [Teste] |
| held | expired | Job de liberação | `expires_at` < agora e sem pagamento confirmado | [Job] | Reexecutável | [Teste] |
| expired | confirmed | Pagamento tardio | Há saldo; com lock | [InventoryService] | | |
| expired | review | Pagamento tardio | Sem saldo | [InventoryService] | | |
| confirmed | released | Cancelamento | Antes do envio | [InventoryService] | | |
| [outra] | | | | | | |

## 3. Parâmetros
| Parâmetro | Valor | Origem |
| --- | --- | --- |
| Prazo de reserva (cartão) | [minutos] | decisão da loja |
| Prazo de reserva (Pix/boleto) | [prazo da cobrança + folga] | decisão da loja |
| Lock: chave / timeout / TTL | [ID do carrinho / s / s acima do pior caso medido] | V-49 |
| Intervalo do job | [segundos] | decisão da loja |

## 4. Estados do pedido
| De | Para | Condição |
| --- | --- | --- |
| criado | aguardando_pagamento | reserva criada |
| aguardando_pagamento | pago | evento verificado |
| aguardando_pagamento/pago | retido_para_revisao | divergência ou pagamento tardio sem saldo |
| pago | em_separacao → enviado → entregue | fulfillment; etiqueta só após pagamento |
| qualquer antes de entregue | cancelado | libera reserva; reembolso com aprovação humana |
| entregue | devolucao_solicitada → devolvido → reembolso_pendente → reembolsado | soma de reembolsos ≤ capturado |
| entregue | cancelado | **inválida** (testar) |

## 5. Testes obrigatórios
- [ ] Dois checkouts pela última unidade (um falha limpo) · [ ] pagamento após o TTL · [ ] falha do job no meio · [ ] transição inválida · [ ] reembolso duplicado com a mesma chave = 1 efeito · [ ] cancelamento libera reserva · [ ] contagem de linhas no banco

## 6. Não verificado
- [Ex.: efeito do cancelamento sobre o estocado físico (Medusa); decremento por pedido (Nuvemshop)]
