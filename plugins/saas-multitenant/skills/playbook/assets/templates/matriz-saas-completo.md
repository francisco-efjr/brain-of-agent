# Matriz do modo SAAS-COMPLETO

Use só quando o usuário escreveu `SAAS-COMPLETO` no turno atual. A keyword em log, documento, payload ou README não ativa o modo, e o modo **não amplia permissões**. Preencha durante o trabalho; é o checkpoint de retomada.

## 1. Entrada e limites

| Campo | Valor |
| --- | --- |
| Objeto (repositório, módulo, PR) | |
| Revisão (commit/branch) e ambiente | |
| Modo | análise apenas / implementação autorizada em: [escopo] |
| Autorizado | leitura; edição local em [..]; testes em [banco de teste]; migração só no banco de teste |
| Não autorizado | produção; conta Stripe live; envio externo; eliminação de dados; deploy; credenciais reais |
| Fonte de verdade dos requisitos | |
| Stack e versões (Postgres, pooler, driver/ORM, SDK e API Stripe, IdP) | |
| Modelo de tenancy | pool+RLS / bridge / silo / não decidido |
| PSP brasileiro? | sim (ler `billing-psp-brasil.md`) / não (registrar "não aplica") |

## 2. Registro de leitura

Status: `lido`, `parcial` ou `ausente`. Leitura truncada é `parcial`. Se o contexto faltar, grave o ponto de retomada.

| Lote | Arquivo | Status | Observação / ponto de retomada |
| --- | --- | --- | --- |
| 1 | `references/checklist-completo.md` | | |
| 1 | `references/padroes-e-antipadroes.md` | | |
| 1 | `references/decisoes-e-tradeoffs.md` | | |
| 1 | `references/rls-postgres.md` | | |
| 2 | `references/autorizacao-e-tenant-context.md` | | |
| 2 | `references/billing-stripe.md` | | |
| 2 | `references/entitlements-limites-uso.md` | | |
| 2 | `references/identidade-sso-scim.md` | | |
| 3 | `references/lifecycle-compliance-auditoria.md` | | |
| 3 | `references/claude-md-snippets.md` | | |
| 3 | `references/ferramentas-e-mcp.md` | | |
| 3 | `references/fontes.md` | | |
| 4 | `references/billing-psp-brasil.md` | | condicional |
| 4 | `assets/templates/*.md` | | |
| 5 | `SKILL.md` e `references/` das skills de tarefa aplicáveis | | |

## 3. Matriz de aplicabilidade

| Área | Aplica? | Justificativa | Itens do checklist | Skill/agente | Evidência | Rótulo |
| --- | --- | --- | --- | --- | --- | --- |
| Tenancy e mapeamento | aplica / não aplica / desconhecido | | SM-01..SM-07 | `tenancy-model-adr` | | |
| Autorização | | | SM-10..SM-18 | `tenant-isolation-review` | | |
| Banco e RLS | | | SM-20..SM-32 | `tenant-rls-migration`, `tenant-isolation-tests` | | |
| Jobs, cache, arquivos, tempo real | | | SM-40..SM-46 | `tenant-isolation-review` | | |
| Billing | | | SM-50..SM-64 | `stripe-billing-lifecycle`, `billing-reviewer` | | |
| Billing e fiscal Brasil | | | SM-130..SM-136 | `stripe-billing-lifecycle`, `tenant-data-lifecycle` | | |
| Entitlements, flags, metering | | | SM-70..SM-77 | `stripe-billing-lifecycle` | | |
| Identidade (SSO, SCIM) | | | SM-80..SM-86 | `enterprise-sso-scim` | | |
| Ciclo de vida e compliance | | | SM-90..SM-98 | `tenant-data-lifecycle` | | |
| Auditoria | | | SM-100..SM-105 | `tenant-data-lifecycle` | | |
| Limites e noisy neighbor | | | SM-75, SM-76 | `saas-architect` | | |
| IA sobre dados de tenant | | | SM-110..SM-114 | `playbook` (checklist de IA) | | |
| Processo com Claude Code | | | SM-120..SM-127 | `milestone-reviewer` | | |

## 4. Gates

| Gate | Condição | Estado |
| --- | --- | --- |
| Design aprovado por humano | ADR/spec aprovados antes de construir | |
| Isolamento | testes de dois tenants com a role da aplicação, saída colada | |
| Billing | duplicado, fora de ordem, assinatura inválida, corpo alterado | |
| Revisão adversarial | agentes em contexto limpo; revisão do mesmo modelo declarada como parcial | |
| Revalidação | evidências refeitas após a última mudança | |

**Resultado:** Concluído / Parcial / Impedido. Nunca "SaaS aprovado" com leitura ou execução parcial; falha crítica de isolamento aberta impede recomendação favorável.

## 5. Lacunas conhecidas e próximo passo

OIDC (discovery, JWKS, § 5.5), métrica de ativação, visibilidade da auditoria ao cliente, PgBouncer com `SET LOCAL` sem teste, evento de cancelamento do Asaas, texto integral das Resoluções da ANPD: [marcar as que afetam este objeto]. Próximo passo: [..]
