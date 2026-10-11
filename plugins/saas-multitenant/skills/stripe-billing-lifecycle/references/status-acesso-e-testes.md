# Troca de plano, trial, cobrança falha, entitlements, metering e testes

Redação própria, destilada das páginas da Stripe citadas em cada seção (documentação proprietária: sem cópia). Conferido em 2026-10-10; as páginas mudam, então confirme na versão de API do projeto e no changelog antes de implementar. Rótulos: Verificado (lido na fonte), Inferido (nosso), Suposição, Não verificável.

## 1. Troca de plano (V-37)

Fonte: https://docs.stripe.com/billing/subscriptions/change-price. Regras verificadas: enviar o ID do item da assinatura; sem ele, o novo preço é adicionado e a assinatura passa a ter dois preços ativos; a troca de preço volta a quantidade para 1; se o intervalo de faturamento muda, a data de cobrança passa a ser a da mudança; de preço zero (trial) para não zero gera fatura e reinicia o período; `proration_behavior: always_invoice` cobra na hora e combina com atualizações pendentes para só atualizar depois do pagamento; se o pagamento imediato falha, a alteração conclui e a assinatura vai para `past_due`; downgrade gera crédito pro rata.

```ts
const sub = await stripe.subscriptions.retrieve(subscriptionId);
const item = sub.items.data.find((i) => i.price.id === currentPriceId);      // escolha o item pela regra do produto
if (!item) throw new Error('item da assinatura não encontrado');

const updated = await stripe.subscriptions.update(
  subscriptionId,
  {
    items: [{ id: item.id, price: newPriceId, quantity: item.quantity }],   // ID do item e quantidade reenviada
    proration_behavior: 'create_prorations',                                 // decisão registrada no spec
  },
  { idempotencyKey: `tenant-${tenantId}-plan-change-${requestId}` },        // requestId é do pedido do usuário, gravado antes
);
// O acesso do tenant muda quando o webhook chega e o worker reconcilia, não por esta resposta (V-02, V-37).
```

Prévia de proration para mostrar ao cliente: use a API de prévia de fatura da sua versão (o nome do método mudou entre versões do SDK; confira na documentação). Para só atualizar depois que o pagamento passar, use atualizações pendentes (`payment_behavior` com a opção documentada para isso; confira o valor exato na versão). Assinaturas com cronograma seguem as práticas de cronogramas.

Checklist: (1) listar as assinaturas do Customer e ler o ID do item; (2) trocar informando o ID; (3) reenviar a quantidade; (4) decidir proration e mostrar a prévia; (5) tratar `past_due` quando a cobrança imediata falha, ou usar atualizações pendentes; (6) teste: depois da troca, um único preço ativo e a quantidade esperada; (7) acesso por webhook.

Regra de produto para downgrade com uso acima do novo limite (ex.: 10 usuários para plano de 5): bloquear com mensagem que lista o excesso, ou aceitar e desativar excedentes escolhidos pelo administrador, sem apagar dados; decisão no spec (V-38, V-30; brain `Downgrade`).

## 2. Trials (V-38)

Fonte: https://docs.stripe.com/billing/subscriptions/trials. Verificado em 2026-10-10:

| Ponto | Regra |
| --- | --- |
| Pré-requisitos de trial offers | versão de API `2026-09-30.endive` ou posterior e assinatura com modo de faturamento `flexible` |
| Onde não funcionam | Checkout, Payment Links e Elements com Checkout Sessions (usar `trial_end`) |
| Combinações | não combinar `trial_end` com trial offer na mesma assinatura |
| Tipos | gratuito = preço 0 e status `trialing` (só se todos os preços de trial forem 0); pago segue o ciclo de `PaymentIntent` e a assinatura fica `active`, `incomplete` ou `past_due` |
| Duração | não pode mudar depois |
| Portal | só ver, cancelar e reativar (não atualizar, pausar nem retomar) |
| Aviso de fim | `customer.subscription.trial_will_end` segue o Dashboard (padrão 3 dias); a Stripe envia o próprio lembrete 7 dias antes |
| Sem forma de pagamento | `missing_payment_method`: `create_invoice` (padrão), `cancel` ou `pause` |
| MRR | só o item em trial sai do MRR |

Checklist: decidir gratuito ou pago; decidir o que ocorre sem forma de pagamento; escutar `trial_will_end` para o e-mail próprio; confirmar versão de API e modo `flexible`; não combinar com `trial_end`; abuso de trial (mesmo domínio ou cartão repetido) é decisão de produto, sem fonte lida (Suposição).

## 3. Cobrança falha e recuperação (V-38, V-02)

Fonte: https://docs.stripe.com/billing/revenue-recovery/smart-retries. Verificado: configuração padrão recomendada de 8 tentativas em 2 semanas; ordem do meio de pagamento na tentativa: padrão da assinatura, origem padrão da assinatura, padrão do Customer, origem padrão legada do Customer, com atualização do campo onde a falha ocorreu; códigos de recusa definitiva (`incorrect_number`, `lost_card`, `pickup_card`, `stolen_card`, `revocation_of_authorization`, `revocation_of_all_authorizations`, `authentication_required`, `highest_risk_level`, `transaction_not_allowed`) mantêm as tentativas agendadas, mas só executam com novo meio de pagamento; agenda personalizada tem até três tentativas; `attempt_count` em `invoice.payment_failed`; com Automations, `next_payment_attempt` vem em `invoice.updated`; esgotadas as tentativas, a assinatura vira `canceled`, `unpaid`, continua `past_due` ou `paused`, conforme a configuração.

Política recomendada para o spec (Inferido):

| Estado | Acesso | Comunicação | Estado do tenant |
| --- | --- | --- | --- |
| `past_due` dentro do prazo de graça | liberado com aviso visível ao admin | e-mail a cada tentativa falha; link para atualizar o meio de pagamento | `active` |
| `past_due` após o prazo | bloquear escrita ou funcionalidades pagas (decisão) | aviso final | `active` com restrição |
| `unpaid` ou `paused` | revogar acesso | oferta de regularização | `deactivated` (reversível; nunca apagar dados) |
| `canceled` | revogar | oferta de nova assinatura | `offboarding` conforme retenção contratual |

O prazo de graça em dias é decisão de produto (Suposição). Recusa definitiva: peça novo meio de pagamento, não espere as tentativas.

## 4. Customer e portal (V-39)

Fontes: https://docs.stripe.com/billing/customer e https://docs.stripe.com/customer-management. Um Customer por tenant, com e-mail, nome e ID interno em `metadata`; guarde o ID da Stripe no modelo interno; uma só moeda por Customer. Portal: o cliente atualiza pagamento, vê faturas, altera assinatura e cancela na hora ou no fim do ciclo; assinaturas com vários produtos, uso, trial offers ou cobrança por fatura só podem ser canceladas; alteração em `trialing` encerra o trial a menos de `continue_trial`; máximo de 10 produtos para troca de plano; sem iframe; sessões do portal são efêmeras.

## 5. Entitlements e flags (V-05, V-42)

Fonte: https://docs.stripe.com/billing/entitlements (variante de API). Regras: `lookup_key` único por feature, anexável a vários produtos; evento `entitlements.active_entitlement_summary.updated` concede e revoga; resumo com no máximo 10 entitlements (paginar pela URL indicada); listar entitlements ativos no startup, nas checagens de autorização e para reconciliar; persistir internamente. Gate lê só `tenant_features`. Flag: targeting key = `tenant_id` e plano e região como atributos, sem dado pessoal de usuário final (Inferido, V-42); flag controla rollout e exceção, nunca direito pago.

## 6. Metering (V-06)

Fonte: https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage. Eventos de medidor são processados de forma assíncrona; o resumo e a fatura prévia podem não refletir eventos recentes; registro por API, CSV no Dashboard ou S3.

Modelo de ADR de metering (preencher):

| Critério | Billing Meters | Metronome | Decisão |
| --- | --- | --- | --- |
| Já cobra por uso hoje? | apropriado (V-06) | migrar tem custo | |
| Custo e contrato | | | |
| Lock-in | | | |
| Latência de visibilidade ao cliente | assíncrona | não lida (Não verificável) | |
| Granularidade necessária (tenant, usuário, recurso) | | | |

Contagem interna com identificador único por evento (Inferido):

```sql
CREATE TABLE usage_events (
  event_id   uuid PRIMARY KEY,                         -- gerado pelo produtor; retry reenvia o mesmo
  tenant_id  uuid NOT NULL,
  meter      text NOT NULL,
  quantity   bigint NOT NULL CHECK (quantity >= 0),
  occurred_at timestamptz NOT NULL,
  reported_at timestamptz
);
-- Reconciliação diária: total interno por tenant e dia (no fuso do negócio) versus total do provedor.
SELECT tenant_id, (occurred_at AT TIME ZONE 'America/Sao_Paulo')::date AS dia, meter, sum(quantity) AS interno
FROM usage_events WHERE occurred_at >= now() - interval '2 days' GROUP BY 1, 2, 3;
```

Alerta de divergência com limite definido pelo time (Suposição), exibição de uso ao cliente com atraso declarado, job de correção para eventos atrasados (V-06). O campo de identificador único do evento de medidor na API da Stripe deve ser conferido na documentação da sua versão.

## 7. Métricas (V-40)

Fontes: https://docs.stripe.com/billing/subscriptions/analytics e https://a16z.com/16-startup-metrics/ (de 2015). MRR da Stripe = soma do valor mensal normalizado de assinaturas `active` e `past_due`, sem impostos, planos gratuitos e cobrança por uso; `canceled` e `unpaid` viram churn; ARPU = MRR dividido por assinantes ativos; LTV da Stripe = ARPU dividido pelo churn de assinantes (estimativa); conversão de trial = convertidos dividido por encerrados em 30 dias e pode passar de 100%. Definição de "usuário ativo" não é padrão (a16z): defina. NRR não aparece com esse nome nas fontes lidas: use churn líquido de receita (a16z) e retenção de receita por coorte (Stripe). Ativação: Suposição por produto.

## 8. Lista de testes obrigatórios (resumo)

| # | Teste | Esperado |
| --- | --- | --- |
| 1 | mesmo evento duas vezes | um registro em `stripe_events`; um efeito |
| 2 | `invoice.paid` antes de `customer.subscription.created` | estado final correto após reconciliar |
| 3 | assinatura inválida | 400; nada gravado |
| 4 | corpo alterado depois de assinado | 400 |
| 5 | resposta do handler antes do processamento | 200 mesmo com worker parado |
| 6 | Customer sem tenant mapeado | evento mantido, alerta emitido |
| 7 | `past_due` | acesso conforme a política do spec |
| 8 | troca de plano | um único preço ativo; quantidade preservada |
| 9 | retry da chamada de saída com mesma chave | um recurso criado; com corpo alterado, erro |
| 10 | evento perdido | job de reconciliação corrige |
| 11 | tenant A não lê nem altera `tenant_billing_state` do B | isolamento (skill `tenant-isolation-tests`) |
| 12 | `unpaid` ou `paused` | tenant `deactivated`; nenhum dado apagado |

Esqueletos de código para 1 a 4: skill `tenant-isolation-tests`, referência `esqueletos-http.md`.
