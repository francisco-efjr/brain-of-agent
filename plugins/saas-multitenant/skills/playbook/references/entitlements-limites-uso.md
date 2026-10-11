# Entitlements, feature flags, metering e limites por tenant

Escopo: o que o plano dá ao tenant (entitlements), o que o time liga e desliga (flags), o que o tenant consome (metering) e o que protege os vizinhos (limites e noisy neighbor). Itens `V-nn` em `fontes.md`. Lacuna declarada: gating por plano com flags tem só a fonte de Stripe Entitlements; `compare-metronome` e o conceito de flags do OpenFeature não foram relidos; metering, flags e noisy neighbor não tiveram pesquisa de comunidade (rodada 3).

## Sumário

- [1. Entitlement x flag x configuração](#1-entitlement-x-flag-x-configuração)
- [2. Entitlements locais](#2-entitlements-locais)
- [3. Feature flags com `tenant_id`](#3-feature-flags-com-tenant_id)
- [4. Limites de plano e downgrade](#4-limites-de-plano-e-downgrade)
- [5. Metering de uso](#5-metering-de-uso)
- [6. Noisy neighbor](#6-noisy-neighbor)
- [7. Testes](#7-testes)

## 1. Entitlement x flag x configuração

Conflito C10 (resolvido com **Inferido**): são três coisas diferentes e não se substituem.

| Conceito | Pergunta que responde | Fonte da verdade | Quem muda | Exemplo |
| --- | --- | --- | --- | --- |
| Entitlement | "o tenant **pagou** por isso?" | tabela local `tenant_features`, alimentada por webhook e reconciliação | billing (automático) | `sso`, `audit_export`, `seats_50` |
| Feature flag | "esta funcionalidade está **liberada** para este tenant agora?" | serviço/tabela de flags | produto/engenharia | rollout gradual, beta, exceção operacional |
| Configuração do tenant | "como este tenant **quer** que funcione?" | tabela de configuração | admin do tenant | idioma, fuso, retenção escolhida |

Regra: o gate de uma funcionalidade paga lê **somente** `tenant_features` (snippet 13). Flag nunca concede direito pago; no máximo adiciona uma exceção explícita, com `source = 'manual'`, motivo e prazo, e visível em auditoria.

## 2. Entitlements locais

Fonte: V-05 (Stripe Entitlements, Verificado).

- Cada feature tem `lookup_key` **único** (não reutilizável entre features) e pode ser anexada a vários produtos. Pré-requisito: Subscriptions e Customer.
- O evento `entitlements.active_entitlement_summary.updated` concede e revoga. O resumo traz no máximo **10** entitlements; acima disso, pagine por `entitlements.url`.
- A Stripe recomenda **persistir internamente**, listar active entitlements no startup, nas checagens de autorização e para **reconciliar após falha de webhook**.
- Mudanças de produto afetam assinaturas existentes **só no próximo ciclo**. A página avisa sobre requisitos legais em mudanças de plano.

Implementação:

1. `tenant_features(tenant_id, feature_key, source, updated_at)` com `feature_key = lookup_key` (schema em `billing-stripe.md`, seção 1).
2. Atualização por webhook (dentro da transação do worker, com contexto do tenant) **e** por reconciliação periódica via API (job diário por tenant, uma transação por tenant). Divergência entre API e tabela gera alerta e correção auditada.
3. Gate: função única `hasFeature(tenantId, key)` que lê a tabela; cache de curta duração com `tenant_id` na chave (V-49); invalidação por evento.
4. Em produto sem Stripe Entitlements, o mesmo desenho vale com a tabela de plano → features mantida pelo billing (Inferido).
5. Negação de feature paga responde com erro estável e a oferta de upgrade; nunca 500.

## 3. Feature flags com `tenant_id`

Fonte: V-42 (OpenFeature classe A, Verificado; LaunchDarkly classe B, vendor; Azure em V-33).

- OpenFeature: contexto de avaliação com dados estáticos globais e dinâmicos por chamada, mesclados em três níveis (API, cliente, invocação; precedência remetida à especificação). *Targeting key* é a string única do sujeito e permite rollout percentual determinístico. Cuidado com dado pessoal; hooks `before` podem filtrar.
- LaunchDarkly: contexto com `kind` (user, organization, device), `key` e atributos; só atributos enviados na avaliação servem. A página lida não explica multi-contexto nem o efeito de contextos `organization` no targeting.
- Azure (V-33): feature flags e configuração **por tenant** em vez de infraestrutura customizada por tenant.

Regra do plugin (**Inferido**; "targeting key = tenant" não tem fonte direta): `targetingKey = tenant_id`; plano e região do tenant como atributos; **nenhum dado pessoal do usuário final** no contexto. Não construa um sistema de flags próprio sem aprovação: Claude Code tende a criar flags próprias (V-19, estudo de 2026 com modelos antigos; reavalie com o modelo atual e não cite percentuais).

## 4. Limites de plano e downgrade

| Tipo de limite | Aplicação | Teste (brain, V-23) |
| --- | --- | --- |
| Assentos | contar membros `active` + convites pendentes; checagem na criação do convite **e** na aceitação | plano de 5 assentos: 5º aceito, 6º bloqueado com oferta de upgrade |
| Volume (registros, armazenamento) | contador por tenant atualizado de forma idempotente | limite exato aceito, +1 recusado |
| Taxa (API, exportações) | rate limit por `tenant_id` e por plano | resposta 429 com `Retry-After` |
| Funcionalidade | `tenant_features` | sem entitlement, erro estável com oferta de upgrade |

**Downgrade nunca apaga dados** (V-23, V-38). Política explícita, escolhida no spec e testada: (a) bloquear o downgrade enquanto o uso exceder o novo limite; ou (b) aceitar e colocar o excedente em modo somente leitura/desativado (por exemplo, usuários excedentes `inactive`), com prazo e aviso. Exemplo do brain: sair de 10 usuários para um plano de 5. Mudança de produto vale no próximo ciclo (V-05); a transição acontece por webhook, não pela resposta da API de troca de plano.

Limiares de alerta (por exemplo 80% do limite) e valores de plano são **Suposição** de produto.

## 5. Metering de uso

Fonte: V-06 (Stripe, Verificado), V-39, brain ("Dados, ETL e BI").

1. **Decisão em ADR**: Metronome ou Billing Meters, com custo, lock-in e latência de visibilidade. Billing Meters não é "legacy"; o Stripe recomenda Metronome para a maioria das integrações novas e Billing Meters para quem já cobra assim; o conflito de interesse é do fornecedor (C4).
2. **Evento de uso** com identificador único (Inferido: necessário para retry sem dupla contagem), `tenant_id`, métrica, quantidade, instante UTC. Granularidade (tenant, usuário, recurso) definida no spec.
3. Os eventos são processados de forma assíncrona: a fatura prévia pode não refletir eventos recentes. Mostre o uso ao cliente com **atraso declarado**.
4. **Reconciliação diária** entre a contagem interna e o total do provedor, por partição (dia, tenant), não só pelo total: totais iguais escondem erros que se compensam (brain). Alerta de divergência acima de um limiar (Suposição) e job de correção para eventos atrasados.

```sql
-- Contagem interna por tenant e dia (rode no seu banco; compare com o total do provedor)
SELECT tenant_id,
       date_trunc('day', occurred_at AT TIME ZONE 'America/Sao_Paulo') AS dia,
       metric,
       COUNT(*)            AS eventos,
       COUNT(DISTINCT event_id) AS eventos_unicos,
       SUM(quantity)       AS total
FROM usage_events
WHERE occurred_at >= now() - interval '2 days'
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3;
-- eventos <> eventos_unicos indica duplicata a investigar; o fuso do corte é regra do negócio
```

5. Reprocessamento idempotente: rodar a mesma janela duas vezes dá as mesmas somas (carga por `INSERT` sem `MERGE`/limpeza de partição é a causa clássica, brain).
6. Dado atrasado: evento de 30/09 que chega em 02/10 entra na janela de reprocessamento definida; fora dela vai para tratamento explícito (brain).
7. Ledger append-only como alternativa interna é ideia classe C, não verificada (V-06).

## 6. Noisy neighbor

Fonte: V-09 (Azure, Verificado; classe B), V-49 (rate limit com tenant como dimensão).

Governança: monitorar uso global e por tenant com alertas de pico; quota, throttling e rate limiting; capacidade reservada vendável; balancear tenants entre stamps; mover tarefas pesadas para fora do pico; limitar operações (máximo de registros por resposta, timeout de query); transparência sobre limites. Detecção: falhas aleatórias que funcionam depois; telemetria com identificador do tenant (custo por tenant).

Checklist aplicável (valores são **Suposição**; meça):

- [ ] rate limit por `tenant_id` e por plano, em API **e** em filas, concorrência e conexões;
- [ ] teto de tamanho de página e timeout de query (`statement_timeout` por role/transação);
- [ ] exportações e relatórios pesados em fila, com concorrência por tenant limitada;
- [ ] métricas de latência, erro e consumo **por tenant** (cardinalidade controlada: top-N ou amostragem);
- [ ] alerta quando um tenant consome fração anormal do total;
- [ ] resposta de throttling documentada ao cliente (429 + `Retry-After`);
- [ ] plano enterprise com pool dedicado ou silo (bridge) como saída comercial;
- [ ] teste de carga em ambiente descartável: um tenant satura e os demais mantêm SLO.

## 7. Testes

| # | Teste | Esperado |
| --- | --- | --- |
| 1 | tenant sem entitlement acessa feature paga | negado com erro estável; nada de 500 |
| 2 | evento `active_entitlement_summary.updated` duplicado | tabela idêntica |
| 3 | webhook perdido | reconciliação diária corrige e alerta |
| 4 | flag ligada para tenant sem entitlement | continua negado |
| 5 | tenant A tem feature, tenant B (nome parecido) não | B negado |
| 6 | downgrade com uso acima do novo limite | política escolhida; nenhum dado apagado |
| 7 | evento de uso reenviado | contagem não duplica |
| 8 | divergência artificial entre interno e provedor | alerta dispara |
| 9 | tenant A estoura rate limit | tenant B segue normal |
