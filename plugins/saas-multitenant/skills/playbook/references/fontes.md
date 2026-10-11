# Fontes (bibliografia validada)

Bibliografia consolidada em **2026-10-11** a partir do documento de pesquisa validado do segmento (`VALIDATED.md`, itens V-01 a V-66). A coluna **Lida em** informa quando um validador independente (modelo diferente do pesquisador, mas também da família Claude: independência parcial) abriu a página: **2026-10-10**. O construtor do plugin **não reabriu** as URLs; confira a página atual antes de copiar número, nome de campo ou versão.

Classe A = documentação oficial, norma ou especificação; B = autor ou projeto reconhecido, vendor, cópia de terceiros; C = sinal de prática, nunca fonte de regra. A nota entre parênteses é a pontuação 0 a 10 da rubrica de fontes quando o validador a registrou. "Licença" é a **identificada**; sem licença identificada o plugin só destila (redação própria) e cita a URL. Nenhum trecho literal de terceiros foi copiado; o único reaproveitamento quase literal é o do brain-of-agent (conteúdo próprio do usuário, MIT), com atribuição.

## Sumário

- [Como citar](#como-citar)
- [Classe A](#classe-a)
- [Classe B](#classe-b)
- [Classe C](#classe-c)
- [Top 10 para decisões do plugin](#top-10-para-decisões-do-plugin)
- [Conteúdo próprio e inspirações](#conteúdo-próprio-e-inspirações)
- [Rejeitados e rebaixados](#rejeitados-e-rebaixados)
- [Lacunas conhecidas](#lacunas-conhecidas)
- [Onde conferir versões](#onde-conferir-versões)

## Como citar

- `V-nn` aponta para o item do consolidado de pesquisa; cite-o ao justificar uma recomendação. "Estável" = conhecimento do domínio sem fonte lida; rotule **Inferido**.
- Versões, nomes de eventos e flags mudam (API da Stripe, Claude Code, PostgreSQL, PgBouncer). Estrelas e forks vêm do HTML das páginas; a API do GitHub devolveu HTTP 403, então datas de commit vêm de feeds Atom e **valem só onde indicado**. Estrela não prova qualidade.
- Números de autores (percentuais de estudos, contagens) são deles, sujeitos a modelo e data; não os reproduza sem a fonte e a ressalva.
- Revisões feitas por modelos Claude não equivalem a validação externa.

## Classe A

| Item | Título | URL | Licença | Lida em | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-01 (8) | PostgreSQL: Row Security Policies (série 18.x) | https://www.postgresql.org/docs/current/ddl-rowsecurity.html | doc PostgreSQL; licença da doc não verificada; destilado | 2026-10-10 | `rls-postgres.md`: `USING`/`WITH CHECK`, `FORCE`, `BYPASSRLS`, canal oculto de unique/FK |
| V-34 (9) | PostgreSQL: funções de administração `set_config`/`current_setting` | https://www.postgresql.org/docs/current/functions-admin.html | idem | 2026-10-10 | contexto por transação (`is_local`, `missing_ok`) |
| V-47 (9) | PgBouncer: features (tabela por modo de pool) | https://www.pgbouncer.org/features.html | não declarada; destilado | 2026-10-10 | `SET`/`RESET` "Never" em modo transaction; `SET LOCAL` não listado |
| V-48 (8) | AWS Prescriptive Guidance: RLS em PostgreSQL gerenciado | https://docs.aws.amazon.com/prescriptive-guidance/latest/saas-multitenant-managed-postgresql/rls.html | proprietária; destilado | 2026-10-10 | RLS "required" no pool; exemplo sem `FORCE` nem `missing_ok` |
| V-33 (8) | Azure: abordagens de storage/dados multi-tenant + AWS: modelos de partição (silo, bridge, pool) | https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/storage-data · https://docs.aws.amazon.com/prescriptive-guidance/latest/saas-multitenant-managed-postgresql/partitioning-models.html | MS Learn/AWS; destilado | 2026-10-10 | `decisoes-e-tradeoffs.md` D1/D2; antipadrões |
| V-07 (8) | Azure: modelos de tenancy | https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenancy-models | MS Learn; destilado | 2026-10-10 | 6 perguntas do ADR |
| V-32 (8) | Azure: mapear requisição para tenant | https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/map-requests | idem | 2026-10-10 | tenant do claim; mapear ≠ autorizar |
| V-30 (8) | Azure: ciclo de vida do tenant | https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenant-life-cycle | idem | 2026-10-10 | trial, onboarding, offboarding, desativação |
| V-63 (8) | AWS SaaS Lens: isolamento de tenant (introdução) | https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/tenant-isolation.html | proprietária | 2026-10-10 | isolamento em mecanismo compartilhado |
| V-11 (8) | OWASP: Authorization Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html | licença não verificada; destilado | 2026-10-10 | checklist de PR de autorização por objeto |
| V-49 (8) | OWASP: Multi-Tenant Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html | **CC BY-SA 4.0** (rodapé): só redação própria, com atribuição se reproduzir | 2026-10-10 | cache, URL assinada, restore, alerta cruzado, `pg_roles`, `set_config(...,true)` |
| V-35 (8) | OWASP: SAML Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html | licença não verificada | 2026-10-10 | checagens da resposta SAML |
| V-41 (8) | OWASP: Logging Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | licença não verificada | 2026-10-10 | eventos e integridade da trilha |
| V-02 (8) | Stripe: visão geral de assinaturas | https://docs.stripe.com/billing/subscriptions/overview | proprietária; destilado | 2026-10-10 | tabela status → acesso |
| V-03 (8) | Stripe: webhooks e webhooks de assinatura | https://docs.stripe.com/webhooks · https://docs.stripe.com/billing/subscriptions/webhooks | proprietária | 2026-10-10 | handler em 8 passos |
| V-04 (8) | Stripe: requisições idempotentes | https://docs.stripe.com/api/idempotent_requests | proprietária | 2026-10-10 | `Idempotency-Key` |
| V-05 (8) | Stripe: Entitlements (variante API) | https://docs.stripe.com/billing/entitlements.md?dashboard-or-api=api | proprietária | 2026-10-10 | `lookup_key`, persistir local |
| V-06 (8) | Stripe: registro de uso (usage-based) | https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage | proprietária | 2026-10-10 | metering; Metronome x Billing Meters |
| V-37 (8) | Stripe: trocar preço (upgrade/downgrade) | https://docs.stripe.com/billing/subscriptions/change-price | proprietária | 2026-10-10 | ID do item, quantidade, proration |
| V-38 (8) | Stripe: trials e Smart Retries | https://docs.stripe.com/billing/subscriptions/trials · https://docs.stripe.com/billing/revenue-recovery/smart-retries | proprietária | 2026-10-10 | API `2026-09-30.endive`, `flexible`; recusas definitivas |
| V-39 (8) | Stripe: Customer, portal | https://docs.stripe.com/billing/customer · https://docs.stripe.com/customer-management | proprietária | 2026-10-10 | Customer por tenant; limites do portal |
| V-40 (8) | Stripe: Billing Analytics (métricas) | https://docs.stripe.com/billing/subscriptions/analytics | proprietária | 2026-10-10 | dicionário de métricas |
| V-10, V-36 (8) | IETF: SCIM RFC 7643, 7644, 9865, 9967 | https://datatracker.ietf.org/doc/html/rfc7644 (e rfc7643, rfc9865, rfc9967) | RFCs IETF | 2026-10-10 (7643 até § 4.2) | `identidade-sso-scim.md` |
| V-54 (8) | Microsoft Entra: requisitos de endpoint SCIM | https://learn.microsoft.com/en-us/entra/identity/app-provisioning/use-scim-to-provision-users-and-groups | MS Learn; `ms.date` 2026-09-15 | 2026-10-10 | checklist de aceite |
| V-36 | Microsoft Entra: domínio personalizado | https://learn.microsoft.com/en-us/entra/fundamentals/add-custom-domain | MS Learn | 2026-10-10 | domínio verificado (TXT/MX) |
| V-55 (8) | Okta: SCIM 2.0 (guia da API) | https://developer.okta.com/docs/api/openapi/okta-scim/guides/scim-20/ · https://developer.okta.com/docs/concepts/scim/ | proprietária | 2026-10-10 | `active=false`, 429 |
| V-46 (9) | OpenID Connect Core 1.0, § 3.1.3.7 | https://openid.net/specs/openid-connect-core-1_0.html | licença não verificada; redação própria | 2026-10-10 (100 mil de 285 mil caracteres) | validação do ID Token |
| V-42 (8) | OpenFeature: contexto de avaliação | https://openfeature.dev/docs/reference/concepts/evaluation-context | projeto CNCF; destilado | 2026-10-10 | targeting key |
| V-27 (9) | LGPD (Lei 13.709/2018), publicação original, espelho da Câmara | https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-publicacaooriginal-156212-pl.html | norma pública | 2026-10-10 | arts. 15, 16, 18, 37, 39, 46, 48 |
| V-61 (8) | ANPD: comunicação de incidente de segurança | https://www.gov.br/anpd/pt-br/assuntos/incidente-de-seguranca · https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis | página oficial | 2026-10-10 | três dias úteis, 20 dias úteis, condições |
| V-59 (8) | Portal NFS-e Nacional | https://www.gov.br/nfse/pt-br | página oficial | 2026-10-10 | homologação, documentação técnica |
| V-60 (8) | Resolução CGSN 191/2026 (cópia multivigente, portal da Economia do DF) | https://economia.df.gov.br/documents/d/seec/resol-cgsn-n-191-2026-pdf | norma; **cópia não é o DOU** | 2026-10-10 | NFS-e obrigatória para Simples a partir de 01/11/2026 |
| V-50 (8) | Asaas: FAQ de webhooks | https://docs.asaas.com/docs/webhooks-faq | documentação do fornecedor | 2026-10-10 | token em header, HTTP 200, 15 falhas, 14 dias |
| V-15 (8) | Claude Code: best practices e memory | https://code.claude.com/docs/en/best-practices · https://code.claude.com/docs/en/memory | proprietária | 2026-10-10 | CLAUDE.md curto, verificação, revisor |
| V-16 (8) | Claude Code: sub-agents | https://code.claude.com/docs/en/sub-agents | proprietária | 2026-10-10 | plugins ignoram `hooks`, `mcpServers`, `permissionMode` |
| V-14 (8) | Claude Code: hooks e hooks-guide | https://code.claude.com/docs/en/hooks · https://code.claude.com/docs/en/hooks-guide | proprietária | 2026-10-10 (200 mil de 262 mil caracteres) | hook de proteção; `@arquivo` não dispara |
| V-43 (9) | Claude Code: skills e plugins-reference | https://code.claude.com/docs/en/skills · https://code.claude.com/docs/en/plugins-reference | proprietária | 2026-10-10 | empacotamento, limite de `description` |
| V-13 (8) | `anthropics/claude-code-security-review` | https://github.com/anthropics/claude-code-security-review | MIT; 6,3 mil estrelas; último commit 2026-02-11 (feed) | 2026-10-10 | T-03; não endurecida contra injeção |

## Classe B

| Item | Título | URL | Licença | Lida em | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-08 (6) | AWS: SaaS architecture fundamentals, tenant isolation ("historical reference only") | https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/tenant-isolation.html | proprietária | 2026-10-10 | "autenticado não é isolado" como princípio |
| V-09 (7) | Azure: antipadrão Noisy Neighbor | https://learn.microsoft.com/en-us/azure/architecture/antipatterns/noisy-neighbor/noisy-neighbor | MS Learn | 2026-10-10 | governança de recursos |
| V-12 (7) | `github/awesome-copilot`: instrução security-and-owasp | https://github.com/github/awesome-copilot/blob/main/instructions/security-and-owasp.instructions.md | MIT; 39.881 estrelas; push 2026-10-09 (API) | 2026-10-10 | AZ1 a AZ6; severidade em 3 níveis |
| V-17 (6) | Willison: the lethal trifecta (2025-06-16) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | não declarada | 2026-10-10 | checklist de IA |
| V-18 (6) | Brex: prompt-engineering (guia de 2023) | https://github.com/brexhq/prompt-engineering | MIT; último commit 2023-05-17 | 2026-10-10 | só princípios de dados |
| V-19 (6) | Amplifying: Claude Code picks (fev/2026) | https://amplifying.ai/research/claude-code-picks | não declarada | 2026-10-10 | motivo para declarar a stack |
| V-20 (7) | gstack (Garry Tan) | https://github.com/garrytan/gstack | MIT; ~135,8 mil estrelas | 2026-10-10 | inspiração do spec com gate (sem copiar) |
| V-21 (7) | awesome-cursorrules: FastAPI production | https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/fastapi-production-architecture-cursorrules-prompt-file.mdc | CC0-1.0 | 2026-10-10 | escritor único, idempotência (redação própria, nada copiado) |
| V-22 (5) | Sanity: first attempt will be 95% garbage | https://www.sanity.io/blog/first-attempt-will-be-95-garbage | não declarada | 2026-10-10 | sem produção; três tentativas |
| V-23 (6) | brain-of-agent: matriz SaaS multi-tenant B2B (`brains/qa/references/dominios.md`, linhas 169 a 189) | snapshot local em `docs/foundation/brain-of-agent-snapshot/` | **MIT, conteúdo próprio do usuário** | 2026-10-10 | `matriz-dois-tenants.md` |
| V-24, V-45 (6) | `supabase/agent-skills` (regras de Postgres) | https://github.com/supabase/agent-skills | MIT; 2,7 mil estrelas; último commit 2026-10-02 (feed) | 2026-10-10 | desempenho de policy, privilégios |
| V-25 (5) | `moasq/production-saas-starter` | https://github.com/moasq/production-saas-starter | MIT; 533 estrelas; último commit 2026-10-04 (feed) | 2026-10-10 | roles de migração e runtime (afirmações de README não testadas) |
| V-26 (6) | `stripe/agent-toolkit` | https://github.com/stripe/agent-toolkit | MIT; 1,9 mil estrelas | 2026-10-10 | só link; instalação pelo usuário |
| V-28 (7) | GDPR arts. 17, 20, 28, 33 (cópia gdpr-info.eu; EUR-Lex truncou) | https://gdpr-info.eu/art-17-gdpr/ (e art-20, art-28, art-33) | cópia de terceiros | 2026-10-10 | DPA, eliminação, portabilidade, 72 h |
| V-31 (6) | Clerk, Auth0, WorkOS: organizações | https://clerk.com/docs/guides/organizations/overview · https://auth0.com/docs/manage-users/organizations/organizations-overview · https://workos.com/docs/authkit/users-organizations.md | fornecedores | 2026-10-10 | estados de membro, org ativa por aba |
| V-40 (7) | a16z: 16 startup metrics (2015) | https://a16z.com/16-startup-metrics/ | não declarada | 2026-10-10 | churn líquido de receita, LTV |
| V-44 (5) | HN "Shipping Multi-Tenant SaaS Using Postgres RLS" (254 pontos) + post dev.to | https://news.ycombinator.com/item?id=32241820 · https://dev.to/m_zinger_2fc60eb3f3897908/why-tenant-context-must-be-scoped-per-transaction-3aop | posts de usuários | 2026-10-10 | trade-offs de schema por tenant (relato) |
| V-51 (7) | Asaas: eventos de assinatura | https://docs.asaas.com/docs/eventos-para-assinaturas | documentação do fornecedor | 2026-10-10 | sete eventos; teste obrigatório |
| V-52 (5) | Iugu: mapa da documentação | https://dev.iugu.com/ | não verificada | 2026-10-10 (só índice) | 4 perguntas de pré-integração |
| V-53 (6) | Asaas: subcontas | https://docs.asaas.com/docs/subcontas | documentação do fornecedor | 2026-10-10 | fluxo b separado |
| V-56 (6) | Braze: SAML JIT provisioning | https://braze.com/docs/user_guide/administer/global/saml_single_sign_on/saml_just_in_time_provisioning/ | fornecedor | 2026-10-10 | regras de JIT (não é padrão) |
| V-62 (6) | Resolução BCB 402/2024 (cópia lex.com.br) | https://www.lex.com.br/resolucao-bacen-no-402-de-22-de-julho-de-2024/ | cópia comercial; **não é o site do BCB** | 2026-10-10 | estado da autorização do Pix Automático |

## Classe C

| Item | Título | URL | Observação |
| --- | --- | --- | --- |
| V-57 (3) | SKILL.md `saas-multi-tenant` (repositório da comunidade) | https://raw.githubusercontent.com/sickn33/agentic-awesome-skills/main/skills/saas-multi-tenant/SKILL.md | sem licença no arquivo; **só checklist de revisão de exemplos de RLS**, nunca regra ou código |
| V-58 (3) | dev.to: RLS em Supabase, lições | https://dev.to/pavelespitia/building-multi-tenant-rls-in-supabase-lessons-from-shipping-lomi-4go4 | sinal; sem vazamento real relatado |
| V-41 (5) | NIST SP 800-92 (2006) | https://csrc.nist.gov/pubs/sp/800/92/final | só página-resumo; referência de governança; não diz se foi substituída |

## Top 10 para decisões do plugin

1. PostgreSQL Row Security Policies (V-01, A).
2. PostgreSQL `set_config`/`current_setting` + PgBouncer features (V-34, V-47, A).
3. Stripe: assinaturas e webhooks (V-02, V-03, A).
4. Stripe: Entitlements (V-05, A).
5. Azure: modelos de tenancy e mapeamento de requisição (V-07, V-32, A).
6. AWS/Azure: silo, bridge, pool e RLS (V-33, V-48, A).
7. OWASP: Authorization e Multi-Tenant cheat sheets (V-11, V-49, A).
8. Stripe: requisições idempotentes (V-04, A).
9. LGPD (texto original) e página da ANPD (V-27, V-61, A).
10. Claude Code: best practices e memory (V-15, A).

## Conteúdo próprio e inspirações

- **brain-of-agent** (`francisco-efjr/brain-of-agent`, MIT, conteúdo do usuário): matriz de dois tenants (`dominios.md`, linhas 169 a 189, com correção do inciso LGPD), seções de pagamentos, eventos, dados/ETL, documentos brasileiros e saúde, e casos sintéticos de `evals/cases.json`. Incorporado com adaptação e atribuição. Normas e números do brain foram "conferidos em 2026" e devem ser reconferidos na fonte antes de virar resultado esperado.
- **gstack** (MIT): inspiração de processo (`/office-hours`, `/spec`, `/plan-eng-review`, `/review`); nada copiado; `./setup` não é executado.
- **awesome-cursorrules** (CC0): fonte de ideias de V-21; redação própria, nada copiado.
- Todos os prompts da biblioteca, snippets, templates e agentes do plugin são **redação própria**. Os prompts V-03, V-16, V-34, V-43, V-64, V-65 e V-66 são autoria nossa **sem eval**: nota máxima 90.

## Rejeitados e rebaixados

| Item | Decisão | Motivo |
| --- | --- | --- |
| Catálogo VoltAgent | C, nunca fonte | mantenedores não auditam subagentes; `curl` no README; números de exemplo |
| saasify | C (ideia) | 6 estrelas; instalação por `npx ... --yes` sem código revisado |
| vantionlabs/saas-starter | C (ideia) | 9 estrelas; README não confirmado no código |
| saas-master-builder | **rejeitado** | texto promocional, `npx` sem publicador, exemplo ilustrativo apresentado como evidência |
| multi-tenant-fullstack-crud-skill | C (ideia) | recomenda `sync({alter:true})`, deploy no push, `force:true` |
| supabase-architect-skill, saas-resources-hub | C | 2 a 3 commits; alegações de README |
| aitmpl guardrail de commit | **rejeitado** | `npx` no post; sem data nem engajamento |
| Aviatrix/Adobe (vazamento por ingestão) | rejeitado como regra | fornecedor de segurança, sem postmortem primário; só o princípio "isolamento cobre escrita em lote e otimização" ficou como Inferido |
| Horários de Pix de imprensa de 2023 | rejeitado | não constam na Resolução 402 |
| Métrica de ativação (glossários) | rejeitado | sem fonte de autoridade |
| NIST SP 800-92 | rebaixado a C | publicado em 2006 |
| "Billing Meters é legacy" | afirmação falsa | "legado" é o processo anterior (`usage-based-legacy`) |
| "Hooks são best-effort" | não encontrada | usar hook + deny (V-14) |

## Lacunas conhecidas

1. OIDC: discovery, rotação de JWKS e § 5.5 não lidos (V-46 cobre § 3.1.3.7).
2. Métrica de ativação sem fonte; NRR não aparece com esse nome.
3. Visibilidade da auditoria ao administrador do cliente, imutabilidade e retenção de log: sem fonte.
4. Relatos de falha real em produção (vazamento entre tenants, webhook duplicado, trial abusado): nenhum postmortem primário lido; a evidência de comunidade é **fraca**.
5. `SET LOCAL`/`set_config(..., true)` atrás de PgBouncer em modo transaction: Não verificável sem teste (V-47 não lista).
6. AWS SaaS Lens além da introdução; schema por tenant em fonte própria.
7. Resoluções CD/ANPD 15/2024 e 2/2022 (texto integral), prazo em dobro de pequeno porte, papel do operador; LGPD consolidada; GDPR em texto oficial.
8. RFC 7643 lida até § 4.2; OASIS saml-core não lida.
9. Gating por plano com flags; `compare-metronome`; conceito de flags do OpenFeature (404 antes).
10. Brasil: boleto, Regulamento Pix consolidado e manuais do BCB, texto da CGSN 191 no DOU, credenciamento de integrador de NFS-e, evento de cancelamento do Asaas, endpoint de subconta, Iugu em profundidade, versão da API do Asaas.
11. JIT em Okta e Entra; reativação no Entra; metering, entitlements, flags, noisy neighbor e GDPR sem pesquisa de comunidade na rodada 3.
12. Evals: nenhum prompt ou agente deste plugin foi executado contra casos reais (`designed_not_executed`).

## Onde conferir versões

| Tema | Onde |
| --- | --- |
| API e changelog da Stripe | changelog na documentação em https://docs.stripe.com (localize pelo menu; não lido nesta pesquisa) e a versão de API fixada no painel do projeto |
| Eventos e campos do SDK | `package.json`/lockfile e a referência do SDK instalado |
| Claude Code (hooks, permissões, plugin eval ≥ 2.1.269) | `claude --version`, `/hooks`, `/doctor`, https://code.claude.com/docs |
| PostgreSQL | `SELECT version();` e https://www.postgresql.org/docs/ |
| PgBouncer | `SHOW VERSION;` e https://www.pgbouncer.org/features.html |
| Prazos ANPD, CGSN, BCB | páginas oficiais e DOU, na data do uso |
