# Billing com Stripe: assinatura, webhooks, planos, trials e métricas

Escopo: assinatura recorrente de SaaS B2B com Stripe Billing e a sincronização com o tenant. Ledger, Pix, boleto, cartão, PCI e conciliação bancária ficam em `/fintech-payments:playbook`. PSP brasileiro (Asaas) está em `billing-psp-brasil.md`. A documentação da Stripe muda: tudo aqui foi lido em 2026-10-10 (V-02..V-06, V-37..V-40); **confirme a versão de API do projeto e o changelog antes de copiar um nome de campo, evento ou número**.

Segurança desta referência: nunca peça nem escreva `sk_`, `rk_` ou `whsec_` reais; exemplos usam variáveis de ambiente. O plugin não chama a API da Stripe; testes em modo teste são executados pelo usuário ou pelo CI do usuário. Mutação em conta live só com autorização concreta e fora das skills.

## Sumário

- [1. Modelo de dados](#1-modelo-de-dados)
- [2. Status da assinatura para acesso](#2-status-da-assinatura-para-acesso)
- [3. Handler de webhook em 8 passos](#3-handler-de-webhook-em-8-passos)
- [4. Idempotência: dois níveis](#4-idempotência-dois-níveis)
- [5. Upgrade e downgrade](#5-upgrade-e-downgrade)
- [6. Trials e recuperação de cobrança](#6-trials-e-recuperação-de-cobrança)
- [7. Customer por tenant, portal e moeda](#7-customer-por-tenant-portal-e-moeda)
- [8. Metering: Billing Meters ou Metronome](#8-metering-billing-meters-ou-metronome)
- [9. Testes obrigatórios](#9-testes-obrigatórios)
- [10. Dicionário de métricas SaaS](#10-dicionário-de-métricas-saas)
- [11. Fuso e virada de período](#11-fuso-e-virada-de-período)

## 1. Modelo de dados

Redação própria; adapte tipos e nomes. Tabelas de billing são gravadas **apenas** pelo módulo de billing (snippet 5, V-21).

```sql
-- Mapa cliente Stripe -> tenant. Sem RLS: o worker de webhook ainda não tem contexto.
-- Acesso restrito à role do módulo de billing (GRANT mínimo); nenhuma outra camada lê esta tabela.
CREATE TABLE stripe_customer_map (
  stripe_customer_id text PRIMARY KEY,
  tenant_id          uuid NOT NULL UNIQUE
);

CREATE TABLE tenant_billing (          -- com RLS por tenant, como qualquer tabela de tenant
  tenant_id              uuid PRIMARY KEY,
  stripe_subscription_id text UNIQUE,
  status                 text NOT NULL,         -- espelho de subscription.status
  access                 text NOT NULL,         -- 'full' | 'grace' | 'blocked' (política da seção 2)
  current_period_end     timestamptz,
  last_event_id          text,
  updated_at             timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE stripe_events (            -- deduplicação de eventos RECEBIDOS (V-03)
  event_id     text PRIMARY KEY,         -- evt_...
  type         text NOT NULL,
  received_at  timestamptz NOT NULL DEFAULT now(),
  processed_at timestamptz,
  tenant_id    uuid,
  error        text
);

CREATE TABLE tenant_features (          -- entitlements locais (V-05); ver entitlements-limites-uso.md
  tenant_id   uuid NOT NULL,
  feature_key text NOT NULL,             -- = lookup_key da feature na Stripe
  source      text NOT NULL,             -- 'stripe' | 'manual' | 'reconcile'
  updated_at  timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, feature_key)
);
```

`metadata.tenant_id` no Customer e o mapa acima permitem resolver o tenant pelo `customer` do evento (V-39). Se o evento chegar sem tenant mapeado: **registrar e alertar**, nunca descartar em silêncio.

## 2. Status da assinatura para acesso

Fonte: V-02 (Verificado em `subscriptions/overview` e `subscriptions/webhooks`). A coluna "decisão de produto" é escrita **no spec** antes do código (`assets/templates/tabela-status-acesso.md`).

| Status | Acesso ao produto | Ação / observação |
| --- | --- | --- |
| `trialing` | liberado | avisar em `customer.subscription.trial_will_end` (padrão: 3 dias antes) |
| `active` | liberado | após `invoice.paid`, buscar a assinatura e confirmar `active` antes de estender validade |
| `incomplete` | não liberar | até 23 h para pagar; depois vira `incomplete_expired` e exige nova assinatura |
| `incomplete_expired` | não liberar | oferecer nova assinatura |
| `past_due` | **decisão de produto** | padrão sugerido (**Inferido**, C7): liberar com aviso e prazo; Smart Retries "não garante" recuperação; notificar via `invoice.payment_failed` |
| `unpaid` | revogar (tenant `deactivated`) | oferecer regularização; nunca apagar dados (V-38, V-30) |
| `canceled` | revogar (terminal) | oferecer nova assinatura |
| `paused` | **Suposição**: suspender | retomar após meio de pagamento padrão |

Regras que evitam bugs reais:

- Estado de billing do tenant muda por webhook ou API, **nunca** por redirect de checkout (`success_url`): o redirect pode ser forjado, repetido ou nunca ocorrer.
- A resolução de status é configurável: "fatura mais recente" (padrão) ou "todas as faturas". Com "todas", `invoice.paid` **não** torna a assinatura `active` necessariamente; confirme o status buscando a assinatura (V-02, V-03).
- Formas de pagamento adiadas (por exemplo ACH) podem ir direto a `active` e falhar depois sem sair de `active`; ao provisionar, confirme `active` ou entitlements ativos, não só o evento de pagamento.
- `invoice.finalization_failed` deixa a assinatura ativa sem cobrança possível: alerta próprio.
- Eventos de risco, se o SaaS guarda esses dados: `charge.dispute.created`, `charge.refunded`, `radar.early_fraud_warning.created`, `customer.updated`. Assine só os eventos usados.

## 3. Handler de webhook em 8 passos

Fonte: V-03 (Verificado em `/webhooks` e `/billing/subscriptions/webhooks`).

1. **Corpo bruto**: leia o corpo sem parser JSON antes da verificação (`express.json()` antes do handler quebra a assinatura).
2. **Assinatura**: verifique `Stripe-Signature` com o segredo `whsec_` (variável de ambiente); falha responde 400. Tolerância padrão de 5 minutos, nunca 0. Segredo pode ser rotacionado com até 24 h de sobreposição.
3. **Deduplicação**: `INSERT` do `event.id` em `stripe_events` com PK; se já existe, responda 200 sem agir. Quando houver dois Events para o mesmo fato, use também `data.object.id` + `type`.
4. **Enfileire e responda 2xx** antes da lógica pesada. Redirecionamento 3xx conta como falha.
5. **Worker busca o objeto atual** na API (não confia no payload nem na ordem: a ordem de entrega não é garantida e `created` não serve para ordenar), resolve o tenant, abre transação com `set_config('app.tenant_id', $1, true)` e grava o resultado.
6. **Erros**: transitório responde 5xx (retry); evento sem tenant mapeado: registrar e alertar. Retentativas por até 3 dias com backoff exponencial (no sandbox, 3 em poucas horas). Reenvio manual por 15 dias (Dashboard) ou 30 (CLI).
7. **Testes** (seção 9).
8. **Política de status** da seção 2 antes de tratar `invoice.paid` como "ativo".

Complementos da doc: a página recomenda eventos *thin* para novas integrações (e snapshot se ferramenta de terceiros exigir payload completo), lista de IPs permitidos como segunda camada, exempte a rota de CSRF e use HTTPS com TLS 1.2/1.3.

Esqueleto (TypeScript/Express), **não executado**; `constructEvent` serve a eventos *snapshot*; para eventos *thin* use o método que o seu SDK documenta (confira a versão, PAD-13):

```ts
app.post("/webhooks/stripe", express.raw({ type: "application/json" }), async (req, res) => {
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, req.header("stripe-signature")!, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch {
    return res.sendStatus(400);                       // assinatura inválida ou corpo alterado
  }
  const inserted = await db.query(
    "INSERT INTO stripe_events (event_id, type) VALUES ($1, $2) ON CONFLICT DO NOTHING RETURNING event_id",
    [event.id, event.type]);
  if (inserted.rowCount === 1) await queue.enqueue({ eventId: event.id });   // worker faz o resto
  return res.sendStatus(200);                         // duplicado também responde 200
});
```

Worker (pseudocódigo): `obj = stripe.<recurso>.retrieve(id)` → `tenant = lookup(customer)` → `BEGIN; set_config(...); UPSERT tenant_billing/tenant_features; UPDATE stripe_events SET processed_at; COMMIT`. Falha após 5 tentativas vai para DLQ com motivo; reprocessamento existe e é testado (brain: backoff com jitter, mensagem venenosa).

## 4. Idempotência: dois níveis

Não confunda (V-03 x V-04).

| Nível | Problema | Mecanismo |
| --- | --- | --- |
| Entrada | o mesmo evento chega mais de uma vez | `event.id` UNIQUE (seção 3) |
| Saída | o retry de uma chamada à API pode cobrar duas vezes | cabeçalho `Idempotency-Key` da Stripe |

Fatos de V-04 (Verificado): na API v1 a Stripe salva status e corpo da primeira requisição com a chave, **inclusive 500**; chave de até 255 caracteres, UUID v4 ou aleatória, sem dados pessoais; chaves podem ser descartadas após 24 horas; parâmetros diferentes com a mesma chave geram erro; falha de validação ou conflito concorrente não salva resultado e pode ser repetida; na API v2 as repetições completam trabalho parcial; POST aceita a chave, GET e DELETE não precisam.

Prática: derive a chave da **operação de negócio** (`tenant-{id}-troca-plano-{pedido}`), grave-a antes da chamada e reutilize em todo retry. Teste repetindo com o mesmo corpo (mesmo resultado) e com corpo alterado (erro esperado). **Conte linhas no banco**, não só a resposta (brain, "Cobrança dupla").

Brain (cobrança): duplo clique, timeout seguido de retry e dois workers concorrentes devem produzir **uma** cobrança; a segunda chamada devolve o resultado da primeira. O PSP pode concluir a cobrança antes do timeout e o banco não compartilha transação com o PSP: o estado é reconstruído por webhook e API, não pela resposta da chamada.

## 5. Upgrade e downgrade

Fonte: V-37 (Verificado).

1. Liste as assinaturas do Customer e leia o **ID do item** da assinatura.
2. Troque o preço **informando o ID do item**. Sem ele, o novo preço é **adicionado** e a assinatura fica com dois preços ativos.
3. **Reenvie a quantidade**: a troca de preço volta a quantidade para 1.
4. Decida e mostre a prorrata: `proration_behavior: always_invoice` cobra na hora e combina com atualizações pendentes para só atualizar depois do pagamento; se o pagamento imediato falha, a alteração conclui e a assinatura vai para `past_due`.
5. Downgrade gera crédito pro rata. Mudança de intervalo de faturamento muda a data de cobrança para a da mudança; preço zero (trial) para não zero gera fatura e reinicia o período. Assinaturas com cronograma seguem as práticas de cronogramas.
6. O acesso do tenant muda por **webhook** (seção 2), nunca pela resposta da chamada. Downgrade **não apaga dados**: política explícita (bloquear ou desativar o excedente), por exemplo 10 usuários indo para um plano de 5 (brain).
7. Teste automático: após a troca, a assinatura tem **um único preço ativo** e a quantidade esperada.

## 6. Trials e recuperação de cobrança

Fonte: V-38 (Verificado em `trials` e `smart-retries`). Conferir o changelog antes de fixar a versão.

**Trial offers**: exigem versão de API `2026-09-30.endive` ou posterior **e** assinatura com modo de faturamento `flexible`; não funcionam com Checkout, Payment Links nem Elements com Checkout Sessions (use `trial_end` nesses casos); não combine `trial_end` com trial offer na mesma assinatura; teste gratuito = preço 0 e status `trialing` só se todos os preços de trial forem 0; teste pago segue o ciclo de `PaymentIntent` e a assinatura fica `active`, `incomplete` ou `past_due`; a duração não pode mudar depois; no portal só se pode ver, cancelar e reativar. `customer.subscription.trial_will_end` segue o Dashboard (padrão 3 dias) e a Stripe envia o próprio lembrete 7 dias antes; `missing_payment_method` = `create_invoice` (padrão), `cancel` ou `pause`.

**Smart Retries**: configuração padrão recomendada de 8 tentativas em 2 semanas; ordem do meio de pagamento por tentativa: padrão da assinatura, origem padrão da assinatura, padrão do Customer, origem padrão legada do Customer. Recusas definitivas (`incorrect_number`, `lost_card`, `pickup_card`, `stolen_card`, `revocation_of_authorization`, `revocation_of_all_authorizations`, `authentication_required`, `highest_risk_level`, `transaction_not_allowed`) mantêm as tentativas agendadas, mas só executam com **novo meio de pagamento**. Agenda personalizada tem até três tentativas; `attempt_count` vem em `invoice.payment_failed`. Esgotadas as tentativas, a assinatura vira `canceled`, `unpaid`, continua `past_due` ou `paused`, conforme a configuração.

Checklist: decidir trial gratuito ou pago; decidir o que ocorre sem forma de pagamento; escutar `trial_will_end` para o e-mail próprio; confirmar versão de API e `flexible`; política de acesso por status **antes** do código; `unpaid`/`paused` → tenant `deactivated` (nunca apagar); recusa definitiva pede novo meio de pagamento na UI.

## 7. Customer por tenant, portal e moeda

Fonte: V-39 (Verificado em `billing/customer` e `customer-management`).

- Padrão (**Inferido**; a página diz "usuário ou empresa"): **um tenant = um Customer**, com `metadata.tenant_id` e o ID Stripe guardado no modelo interno. Exceção em ADR: várias moedas por tenant exigem dois Customers, porque o Customer tem moeda única, imutável depois de definida.
- Portal: o cliente atualiza pagamento, vê faturas, altera e cancela assinatura (na hora ou no fim do ciclo). Limitações: assinaturas com vários produtos, cobrança por uso, trial offers ou cobrança por fatura só podem ser canceladas; alteração em `trialing` encerra o trial a menos de `continue_trial`; máximo de 10 produtos para troca de plano; sem iframe; sessões efêmeras. Configure o portal sabendo disso antes de prometer autoatendimento total.
- Subconta de PSP para o tenant cobrar o cliente final é outro fluxo de dinheiro e **não** entra no Customer do SaaS (`billing-psp-brasil.md`, V-53, Inferido).

## 8. Metering: Billing Meters ou Metronome

Fonte: V-06 e V-39 (Verificado). Detalhes operacionais em `entitlements-limites-uso.md`.

- Eventos de medidor são processados de forma assíncrona; resumo e fatura prévia podem não refletir eventos recentes. Registro por API, CSV no Dashboard ou S3.
- A página diz que o **Metronome** é recomendado para a maioria das integrações novas e que Billing Meters só é apropriado para quem **já** cobra assim. **Correção registrada**: "Billing Meters é legacy" é falso; "documentação legada" é o processo anterior (`usage-based-legacy`). A página `compare-metronome` não foi relida.
- A recomendação vem do próprio fornecedor: avalie o conflito de interesse e registre a decisão em ADR (custo, lock-in, latência de visibilidade).

## 9. Testes obrigatórios

| # | Teste | Esperado |
| --- | --- | --- |
| 1 | mesmo evento enviado duas vezes | um efeito; segunda resposta 200 sem ação; uma linha em `stripe_events` |
| 2 | `invoice.paid` antes de `customer.subscription.created` | estado final correto após o worker buscar o objeto atual |
| 3 | assinatura inválida | 400, nada gravado |
| 4 | corpo alterado após assinar | 400 |
| 5 | evento sem tenant mapeado | registrado e alertado, sem exceção silenciosa |
| 6 | retry de chamada de saída com a mesma `Idempotency-Key` | mesmo resultado; contagem de cobranças = 1 |
| 7 | mesma chave, corpo diferente | erro explícito, nunca reaproveitamento silencioso |
| 8 | troca de preço | um único preço ativo, quantidade preservada |
| 9 | `past_due`, `unpaid`, `canceled` | acesso conforme a tabela da seção 2; dados preservados |
| 10 | falha da cobrança imediata em upgrade | `past_due` tratado conforme a política |
| 11 | dois workers concorrentes no mesmo evento | um efeito (UNIQUE) |
| 12 | worker cai após gravar e antes do ACK | reprocessamento sem duplicar (brain `recovery-fila`) |
| 13 | webhook de tenant A não altera tenant B | isolamento (RLS + contexto na transação do worker) |

## 10. Dicionário de métricas SaaS

Fontes: Stripe Billing Analytics (A, Verificado) e a16z "16 startup metrics" (B, 2015) (V-40). Regra: **a definição do produto é a da Stripe ou vem marcada como diferente**, para conciliar com o Dashboard. Template: `assets/templates/dicionario-metricas-saas.md`.

| Métrica | Definição (fonte) | Cuidado |
| --- | --- | --- |
| MRR | soma do valor mensal normalizado das assinaturas `active` e `past_due`, sem impostos, planos gratuitos e cobrança por uso (Stripe) | `canceled` e `unpaid` viram churn; descontos e momento de "ativo" são configuráveis (mudança em 24 a 48 h) |
| Crescimento de MRR | novo + reativação + expansão − contração − churn ± câmbio (Stripe) | |
| Assinante ativo | MRR positivo em `active` ou `past_due`, contado uma vez (Stripe) | |
| Churn de assinantes | churn dos 30 dias ÷ (ativos de 30 dias atrás + novos) (Stripe) | |
| Receita perdida | MRR perdido + contração (Stripe) | |
| ARPU | MRR ÷ ativos (Stripe) | |
| LTV | Stripe: ARPU ÷ churn de assinantes (estimativa). a16z: margem de contribuição × vida média (1 ÷ churn mensal) | declare qual fórmula |
| Conversão de trial | convertidos ÷ encerrados em 30 dias (Stripe) | pode passar de 100% |
| Retenção de receita por coorte | Stripe | pode passar de 100% |
| Churn bruto de receita | MRR perdido ÷ MRR inicial (a16z) | |
| Churn líquido de receita | (perdido − upsell) ÷ MRR inicial (a16z) | o equivalente documentado de "NRR"; o termo NRR não aparece nas fontes lidas |
| ARR | sem taxas únicas e sem "bookings × 12" (a16z) | |
| CAC, CMGR | a16z | |
| Ativação | **Suposição**: nenhuma fonte lida define; defina por produto, com evento e janela | "usuário ativo" não tem definição padrão (a16z manda definir) |

## 11. Fuso e virada de período

Brain ("Dados, ETL e BI" e "Pagamentos"): contadores e limites diários zeram no fuso definido pela regra (em geral `America/Sao_Paulo`), não em UTC; corte do dia de métricas no fuso do negócio; teste com transação às 23:59:59 e 00:00:00. Para tenants brasileiros, a virada de período de cobrança e relatórios mostra a data no fuso do cliente. Dinheiro em centavos inteiros ou decimal exato, nunca `float`.
