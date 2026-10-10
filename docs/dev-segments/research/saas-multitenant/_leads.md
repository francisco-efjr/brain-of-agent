# saas-multitenant — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Segmento com lacuna declarada em quase todos os atlas (CT, CP). Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| supabase/agent-skills (EC-21) | https://github.com/supabase/agent-skills | B (6) | Regras de Postgres em 8 categorias incluindo RLS, conexões e locks: base para isolamento por tenant. MIT (HTML); conteúdo não lido. |
| FastAPI production architecture (CT-07) | https://github.com/PatrickJS/awesome-cursorrules | B | "Every query scoped by user_id (multi-tenancy)"; "single writer" por domínio; idempotência. CC0, literais Verificados. Escopo por `user_id` precisa ser generalizado para `tenant_id`. |
| VoltAgent subagents (EC-09) | https://github.com/VoltAgent/awesome-claude-code-subagents | B | Segurança e compliance; tag saas-multitenant; abrir categorias. |
| claude-code-security-review (AO-24) | https://github.com/anthropics/claude-code-security-review | A | Revisão de PR com foco em authz; exclusões podem não servir. MIT. |
| security-and-owasp (CT-16) | https://github.com/github/awesome-copilot | B | A01 controle de acesso; BOLA/IDOR no molde de checklist. MIT. |
| Amplifying (CP-24) | https://amplifying.ai/research/claude-code-picks | B | Proibir auth, flags e cache próprios quando há biblioteca padrão; declarar stack. |
| Willison, lethal trifecta (PC-21) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | A | Dados de vários tenants + conteúdo não confiável + saída externa em features de IA. |
| Brex Prompt Engineering Guide (PC-29) | https://github.com/brexhq/prompt-engineering | B | Nunca usar dados reais de cliente para fine-tuning; conteúdo oculto pode ser visto pelo usuário. MIT. |
| gstack `/office-hours`, `/spec` (BR-20) | https://github.com/garrytan/gstack | B | Premissas antes da solução; REQ-NN. |
| Sanity (CP-22) | https://www.sanity.io/blog/first-attempt-will-be-95-garbage | B | Produção nunca conectada ao agente (relevante a dados de tenants). |
| Hooks guardrail (CP-19) | https://aitmpl.com/blog/secure-git-workflow/ | B | Negar leitura de `.env`/migrations. |

## 2. Repositórios e arquivos a abrir
- `supabase/agent-skills` (RLS, schema, locks).
- `PatrickJS/awesome-cursorrules/rules/fastapi-production-architecture-…mdc`.
- `github/awesome-copilot/instructions/security-and-owasp.instructions.md`.
- `brains/qa/references/dominios.md` e `brains/fullstack/evals/cases.json` (snapshot do brain).
- Stripe Billing, entitlements, SSO/SAML/SCIM, LGPD/GDPR e multi-tenancy em PostgreSQL (RLS oficial) não estão no atlas: lente authoritative.

## 3. Materiais oficiais Anthropic pertinentes
AO-24 (security-review aplica a saas-multitenant), AO-23, AO-10 (hooks), AO-09 (db-reader). Nenhum material Anthropic específico de SaaS foi aprovado.

## 4. Padrões da comunidade
- Nenhum relato de praticante aprovado (lacuna declarada em CP).
- Consultas sempre escopadas ao tenant; dono único de escrita por domínio (CT-07).
- Declarar stack e bibliotecas aceitas (CP-24).

## 5. O que o brain-of-agent já oferece
- `brains/qa/references/dominios.md` (sementes SaaS: multi-tenant, billing; B, MIT; manter "não verificado" e datar normas), `brains/fullstack/evals/cases.json` (16 casos de eval).
- BR-09: regras BR como sementes; BR-20: `/spec`, `/office-hours`; BR-08: BVA, tabelas de decisão, estados.
- BR-03: modo `SAAS-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte aprovada para modelos de multi-tenancy (RLS vs schema vs banco), metering, SSO/SCIM, auditoria, noisy neighbors, métricas SaaS.
- supabase/agent-skills não foi lido.
- Qualquer teste de isolamento de tenants deve usar dados sintéticos; nunca dados reais.
