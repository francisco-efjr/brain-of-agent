# Tabela status → acesso

Decida e escreva **antes** do código. Fonte da tabela Stripe: `V-02` (Verificado). A coluna "Decisão de produto" registra quem decidiu e quando. Estado de billing do tenant muda por webhook ou API, nunca por redirect de checkout.

Política de resolução de status da assinatura: [fatura mais recente (padrão) | todas as faturas] · Versão da API: [..]

## Stripe

| Status | Acesso ao produto | Estado do tenant | Ação / evento | Decisão de produto |
| --- | --- | --- | --- | --- |
| `trialing` | liberado | `trial` | avisar em `customer.subscription.trial_will_end` (padrão 3 dias antes) | |
| `active` | liberado | `active` | após `invoice.paid`, buscar a assinatura e confirmar `active` | |
| `incomplete` | não liberar | `trial`/sem acesso | aguardar até 23 h para pagar | |
| `incomplete_expired` | não liberar | sem acesso | oferecer nova assinatura | |
| `past_due` | **a decidir** (sugestão Inferida: liberar com aviso e prazo) | `active` com aviso | notificar via `invoice.payment_failed`; pedir atualização do pagamento; Smart Retries "não garante" | [quem/quando] |
| `unpaid` | revogar | `deactivated` | oferecer regularização; **nunca apagar dados** | |
| `canceled` | revogar (terminal) | `deactivated` → `offboarding` | oferecer nova assinatura | |
| `paused` | **a decidir** (Suposição: suspender) | `deactivated` | retomar após meio de pagamento padrão | [quem/quando] |

Alertas próprios: `invoice.finalization_failed` (assinatura ativa sem cobrança possível). Formas de pagamento adiadas (ex.: ACH) podem ir a `active` e falhar depois sem sair de `active`.

## Variante: PSP brasileiro (Asaas)

Preencha com o evento **observado no sandbox**; não presuma (V-51; qual evento chega no cancelamento é Não verificável sem teste).

| Cenário | Evento(s) observado(s) | Campo que liga à assinatura | Estado de acesso | Decisão de produto |
| --- | --- | --- | --- | --- |
| assinatura criada (`SUBSCRIPTION_CREATED`) | | `subscription` em `PAYMENT_CREATED` | | |
| cobrança paga (`PAYMENT_*`) | | | | |
| cobrança vencida | | | | |
| assinatura inativada (`SUBSCRIPTION_INACTIVATED`) | | | | |
| assinatura removida (`SUBSCRIPTION_DELETED`) | | | | |
| Pix Automático: pagador cancela a autorização | | estado local da autorização | | |

## Testes

Para cada linha: teste que produz o evento, assertiva sobre `tenant_billing.access` e sobre `tenant_features`, e verificação de que nenhum dado foi apagado.
