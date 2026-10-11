# Billing com PSP brasileiro (Asaas) e Pix Automático

Referência **condicional** (Inferido): leia só se o produto cobra assinatura por PSP local. Sem PSP brasileiro, registre "não aplica" na matriz do `SAAS-COMPLETO`. Escopo: o que muda no handler de webhook, no mapeamento evento → estado de acesso do tenant e no estado da autorização do Pix Automático. Ledger, Pix/boleto/cartão em geral, PCI, antifraude e conciliação bancária ficam em `/fintech-payments:playbook`. Marketplace multi-vendedor fica em `/ecommerce-marketplace:playbook`. Não é orientação jurídica nem contábil.

Estado da evidência (rodada 3, 2026-10-10): Asaas lido em documentação oficial (V-50, V-51, V-53); Iugu só o índice (V-52); Pix Automático em **cópia comercial** da Resolução BCB 402/2024, não no site do BCB (V-62). Versão da API do Asaas: **não verificada**. Confirme na documentação vigente do provedor antes de integrar.

## Sumário

- [1. Diferença central em relação à Stripe](#1-diferença-central-em-relação-à-stripe)
- [2. Webhook do Asaas: checklist](#2-webhook-do-asaas-checklist)
- [3. Eventos de assinatura e de cobrança](#3-eventos-de-assinatura-e-de-cobrança)
- [4. Subcontas: outro fluxo de dinheiro](#4-subcontas-outro-fluxo-de-dinheiro)
- [5. Iugu: perguntas de pré-integração](#5-iugu-perguntas-de-pré-integração)
- [6. Pix Automático: estado da autorização](#6-pix-automático-estado-da-autorização)
- [7. Esqueleto de handler com token em header](#7-esqueleto-de-handler-com-token-em-header)
- [8. Testes de sandbox por cenário](#8-testes-de-sandbox-por-cenário)
- [9. Lacunas](#9-lacunas)

## 1. Diferença central em relação à Stripe

| Aspecto | Stripe (V-03) | Asaas (V-50) |
| --- | --- | --- |
| Autenticação do webhook | assinatura do corpo (`Stripe-Signature`) | `authToken` estático no header `asaas-access-token`; a FAQ não menciona assinatura do corpo (HMAC) |
| Resposta de sucesso | qualquer 2xx | **somente HTTP 200**; outros 2xx contam como falha |
| Prazo | responder antes da lógica pesada | até **10 segundos** |
| Redirecionamento | 3xx conta como falha | 301, 302, 307 e 308 não são seguidos |
| Fila após falhas | retentativas por até 3 dias | após **15 falhas consecutivas** a fila é interrompida; eventos novos são guardados sem envio até a reativação |
| Retenção de pendentes | reenvio manual por 15 dias (Dashboard) ou 30 (CLI) | eventos pendentes por até **14 dias**, depois removidos de forma permanente |
| Identificador do evento | `event.id` | `id` do evento, que se repete quando o evento chega mais de uma vez: use como chave de idempotência |
| Ordem | não garantida | modo sequencial preserva a ordem; o não sequencial não garante |

Sem assinatura do corpo, o token estático **não impede replay** por quem o conheça ou capture (Inferido). A mitigação é em camadas: comparação do header com o segredo do cofre, `id` com UNIQUE (replay vira no-op), allowlist de IP e HTTPS.

## 2. Webhook do Asaas: checklist

Fonte: V-50 (Verificado na FAQ); itens de implementação são redação própria.

1. Rota HTTPS direta, sem redirecionamento.
2. Compare `asaas-access-token` com o segredo guardado no cofre; comparação em tempo constante (**Inferido**, boa prática). A **API key nunca serve de `authToken`** (a documentação desaconselha); gere um token próprio e rotacione.
3. Grave o `id` do evento em tabela com UNIQUE **antes** de agir; repetido responde 200 sem efeito.
4. Responda **200** em menos de 10 s e processe fora da requisição (fila + worker).
5. Alerta de **fila interrompida** antes dos 14 dias (métrica: tempo desde o último evento recebido, ou consulta periódica ao estado da fila no painel/API do provedor, a confirmar na documentação vigente).
6. Allowlist de IPs oficiais como camada extra; o sandbox pode ter IPs extras, então **valide os dois ambientes**.
7. Não assuma ordem: o worker busca a cobrança/assinatura atual na API do provedor (se a API expuser o objeto, a confirmar) e só então grava o estado.
8. Sem segredo no código nem em log; `authToken` nunca em URL.

## 3. Eventos de assinatura e de cobrança

Fonte: V-51 (Verificado na página de eventos de assinatura; classe B).

- Sete eventos de assinatura: `SUBSCRIPTION_CREATED`, `_UPDATED`, `_INACTIVATED`, `_DELETED`, `_SPLIT_DISABLED`, `_SPLIT_DIVERGENCE_BLOCK` e `_SPLIT_DIVERGENCE_BLOCK_FINISHED`. `INACTIVATED` vale para assinatura inativada; `DELETED` para removida.
- As cobranças geradas chegam como `PAYMENT_*`; `PAYMENT_CREATED` traz o campo `subscription`, que liga a cobrança à assinatura.
- A página não usa o termo "cancelamento" nem cita `PAYMENT_DELETED`. **Qual evento chega num cancelamento é Não verificável sem sandbox** (conflito C15 aberto).

Regra proposta: o acesso do tenant deriva de `SUBSCRIPTION_INACTIVATED`, `SUBSCRIPTION_DELETED` e dos `PAYMENT_*` associados pelo campo `subscription`. Antes de adotar, teste no sandbox: criar, pagar, atrasar, inativar e remover, e **registre qual evento chega em cada caso** em `assets/templates/tabela-status-acesso.md` (variante PSP). Equivalente Stripe: `billing-stripe.md`, seção 2.

Tabela de acesso a preencher com o observado (não copie como fato):

| Cenário no sandbox | Evento(s) observado(s) | Estado de acesso do tenant | Decisão de produto |
| --- | --- | --- | --- |
| assinatura criada | _a registrar_ | _a registrar_ | |
| cobrança paga | _a registrar_ | full | |
| cobrança vencida | _a registrar_ | grace ou blocked | prazo de tolerância |
| assinatura inativada | _a registrar_ | blocked | |
| assinatura removida | _a registrar_ | blocked (dados preservados) | |

## 4. Subcontas: outro fluxo de dinheiro

Fonte: V-53 (Verificado em `docs.asaas.com/docs/subcontas`; classe B).

- Criação de subconta por API: permitida para conta-pai pessoa jurídica (CNPJ). O modelo BaaS exige acordo e habilitação prévios; criar conta pela API sem essa configuração não a torna BaaS. No modelo não-BaaS, o titular usa o Asaas, com ativação e onboarding próprios. Clientes novos que criam subcontas por API ficam sujeitos a período de avaliação regulatório (limites em outra FAQ, **não lida**).
- Regra (**Inferido**): separe dois fluxos. (a) O SaaS cobra o tenant: Customer da Stripe ou cliente do PSP do SaaS. (b) O tenant cobra o cliente final dele: subconta é candidata a este fluxo. **Não misture no mesmo Customer.** Endpoint, campos e herança de webhooks da subconta: Não verificáveis.

## 5. Iugu: perguntas de pré-integração

Fonte: V-52 (classe B, só índice de `dev.iugu.com`; sem regra). Faça estas quatro perguntas lendo a documentação **antes** de integrar:

1. Os gatilhos (webhooks) são assinados e como se verifica? (O changelog cita "Assinatura RSA: múltiplos tokens e novo parâmetro X-Signature-Token-Id" de 28/07/2026; se vale para os gatilhos é Não verificável.)
2. A criação de fatura aceita chave de idempotência? (Existe página "Chave de Idempotência".)
3. Quem reenvia gatilho perdido e em que intervalo?
4. Uma assinatura suspensa dispara evento?

## 6. Pix Automático: estado da autorização

Fonte: V-62 (classe B; cópia lex.com.br da Resolução BCB 402/2024; **não é o site do BCB**).

- O art. 11-Q define o Pix Automático como serviço em que o prestador do pagador inicia o Pix na conta do pagador, a partir de instruções periódicas do prestador do recebedor, com autorização prévia específica concedida uma vez, sem autenticação a cada transação. O pagador pode cancelar a autorização a qualquer momento, ou alterá-la quando permitido; o prestador do pagador também cancela se o recebedor pedir (art. 11-Q, § 1º, IV e V). O art. 3º revoga a Resolução BCB 360/2023; início em 16/06/2025 (art. 2º, I).
- A jornada de cancelamento e de alteração é remetida a manuais do BCB que **não foram lidos**. Horários de corte vindos de imprensa de 2023 (22h, 23h59) não constam no texto da 402: **não use**.

Modelo de dados (**Inferido**): guarde o **estado da autorização** (`ativa`, `cancelada_pelo_pagador`, `cancelada_pelo_recebedor`), valor máximo, periodicidade e datas; reconcilie com o banco/PSP antes de marcar a cobrança como paga; trate cancelamento da autorização como evento que leva o tenant ao fluxo de cobrança falha (`past_due`/`deactivated` conforme política), nunca a apagar dados.

## 7. Esqueleto de handler com token em header

TypeScript/Express, **não executado**; adapte à sua stack (PAD-13).

```ts
import { timingSafeEqual } from "node:crypto";

function tokenOk(received: string | undefined): boolean {
  const expected = Buffer.from(process.env.ASAAS_WEBHOOK_TOKEN ?? "");   // vem do cofre
  const got = Buffer.from(received ?? "");
  return expected.length > 0 && got.length === expected.length && timingSafeEqual(got, expected);
}

app.post("/webhooks/asaas", express.json(), async (req, res) => {
  if (!tokenOk(req.header("asaas-access-token"))) return res.sendStatus(401);
  const ins = await db.query(
    "INSERT INTO psp_events (provider, event_id, type) VALUES ('asaas', $1, $2) ON CONFLICT DO NOTHING RETURNING event_id",
    [req.body.id, req.body.event]);
  if (ins.rowCount === 1) await queue.enqueue({ provider: "asaas", eventId: req.body.id });
  return res.sendStatus(200);          // somente 200; processamento fora da requisição
});
```

Os nomes dos campos `id` e `event` do corpo devem ser conferidos na documentação vigente (a FAQ lida confirma o `id` do evento como chave de idempotência; o restante do formato é **Não verificado** aqui).

## 8. Testes de sandbox por cenário

Marcados como `a executar` até alguém rodar no sandbox do provedor com credenciais de teste do usuário.

| # | Teste | Esperado |
| --- | --- | --- |
| 1 | mesmo evento duas vezes | um efeito; UNIQUE no `id` |
| 2 | token errado ou ausente | 401, nada gravado |
| 3 | handler responde 202/204 | provedor conta como falha; teste de contrato com a regra "somente 200" |
| 4 | processamento lento (> 10 s) dentro da requisição | falha; processamento movido para worker |
| 5 | 15 falhas consecutivas simuladas | alerta de fila interrompida dispara |
| 6 | IP fora da allowlist em produção e sandbox | bloqueado/aceito conforme a lista de cada ambiente |
| 7 | criar, pagar, atrasar, inativar e remover assinatura | registrar o evento observado em cada caso (tabela da seção 3) |
| 8 | Pix Automático: pagador cancela a autorização | estado local `cancelada_pelo_pagador`; cobrança futura não é marcada como paga |

Revisão com o prompt PR-33 da biblioteca (V-66) e o agente `billing-reviewer`.

## 9. Lacunas

Qual evento chega no cancelamento (C15); endpoint e campos de subconta; Iugu além do índice; versão da API do Asaas; manuais do BCB do Pix Automático; boleto e Regulamento Pix consolidado; texto integral dos atos no DOU. NFS-e e datas fiscais: `lifecycle-compliance-auditoria.md`.
