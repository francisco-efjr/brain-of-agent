# saas-multitenant — SaaS multi-tenant e billing

Plugin do Claude Code para projetar, implementar, revisar e testar **SaaS B2B multi-tenant**: isolamento entre tenants (RLS no PostgreSQL), autorização por objeto, billing com Stripe (webhooks, trials, upgrade/downgrade), entitlements e limites de plano, SSO/SCIM, ciclo de vida de tenant e dados (LGPD/GDPR) e auditoria, sempre com verificação por evidência. Faz parte da fábrica `dev-segments` (um plugin por segmento). Versão 0.1.0 · licença MIT · pesquisa validada em 2026-10-10 · construído em 2026-10-11.

## O que entrega

- **Um playbook** (`playbook`): router por intenção, 12 princípios com o porquê, processo de 7 passos com critérios de saída, gotchas verificadas, fronteiras com os outros 24 plugins e o modo `SAAS-COMPLETO`.
- **13 referências densas** em `skills/playbook/references/`: checklist mestre `SM-nn` (cerca de 100 itens com detecção e fonte), padrões e antipadrões, decisões e trade-offs (conflitos C1 a C18), 24 regras prontas de CLAUDE.md, ferramentas e MCP (desativados, com JSON e riscos), bibliografia classificada, RLS e contexto de tenant no Postgres, autorização por tenant, billing Stripe, PSP brasileiro (condicional), entitlements/limites/metering, SSO/SCIM e ciclo de vida/compliance/auditoria.
- **13 templates** em `skills/playbook/assets/templates/`: ADR de tenancy, spec com REQ-NN e gate, relatório de revisão de isolamento, checklist de PR, matriz de dois tenants (adaptada do brain-of-agent), checklist de webhook, tabela status → acesso, plano de migração RLS, máquina de estados do tenant, checklist de ciclo de vida de dados, dicionário de métricas, handoff e matriz do modo completo.
- **8 skills de tarefa, 5 agentes, 1 comando, 33 prompts e 14 casos de eval** (tabela abaixo). Para conferir a sua cópia, rode `python tools/verify_plugin.py plugins/saas-multitenant` na raiz do repositório.
- **Seguro por padrão:** sem hooks, sem `.mcp.json`, sem `.lsp.json`, sem `bin/`. Hooks e MCP recomendados estão **documentados e desativados** em `skills/playbook/references/ferramentas-e-mcp.md`.

## Quando usar

Use quando o pedido envolver: vazamento ou isolamento entre clientes, `tenant_id`, RLS, IDOR/BOLA em SaaS; assinatura, cobrança recorrente, webhook Stripe, trial, downgrade, `past_due`; entitlements, limites de plano, metering, noisy neighbor; SSO, SAML, OIDC, SCIM, convites e domínio verificado; offboarding, exclusão de dados do cliente, LGPD/GDPR, incidente, auditoria por tenant; métricas SaaS (MRR, churn). Para pergunta pontual o playbook responde direto, sem carregar referências. Para UI de billing, ledger/Pix, deploy de infraestrutura ou AppSec genérico, ele responde o mínimo e aponta o plugin certo (`/web-frontend:playbook`, `/fintech-payments:playbook`, `/devops-cloud-infra:playbook`, `/security-appsec:playbook`).

## Componentes

Nomes definitivos do design. Skill: `/saas-multitenant:<skill>`; agente: `saas-multitenant:<agente>`.

| Tipo | Nome | Para que serve |
| --- | --- | --- |
| Skill núcleo | `playbook` | Router, princípios, processo, intenção → recurso, gotchas, modo `SAAS-COMPLETO`, fronteiras |
| Skill | `prompts` | Índice e biblioteca de prompts prontos (PR-01 a PR-33 no design): revisão de isolamento, RLS, webhooks, spec, SSO/SCIM, LGPD, auditoria, métricas |
| Skill | `tenant-isolation-review` | Revisão **somente leitura** de vazamento entre tenants em diff, handler, repositório, schema ou worker |
| Skill | `tenancy-model-adr` | Decide silo, bridge ou pool e escreve o ADR |
| Skill (somente por comando) | `tenant-rls-migration` | Planeja e escreve migrações para RLS (nunca aplica); `disable-model-invocation` |
| Skill | `tenant-isolation-tests` | Suíte de dois tenants com a role da aplicação e pool de tamanho 1 |
| Skill | `stripe-billing-lifecycle` | Status → acesso, webhooks, idempotência, troca de plano, trials, entitlements, metering, PSP brasileiro |
| Skill | `saas-feature-spec` | Spec testável com REQ-NN de isolamento, autorização, billing e downgrade, com gate |
| Skill | `enterprise-sso-scim` | SAML, OIDC, SCIM, domínio verificado, convites, JIT |
| Skill | `tenant-data-lifecycle` | Estados do tenant, exportação, eliminação, retenção, incidente (ANPD), auditoria, NFS-e |
| Agente | `tenant-isolation-reviewer` | Revisor de vazamento entre tenants (`Read, Grep, Glob`) |
| Agente | `billing-reviewer` | Revisor de webhooks, assinatura, planos, entitlements (`Read, Grep, Glob`) |
| Agente | `saas-architect` | ADR de tenancy, estados e limites (escreve só em `docs/`: instrução do prompt, não restrição técnica) |
| Agente | `isolation-test-engineer` | Escreve e roda a suíte de dois tenants (`Read, Grep, Glob, Write, Edit, Bash`) |
| Agente | `milestone-reviewer` | Revisão adversarial por marco, em contexto limpo |
| Comando | `/saas-multitenant:tenant-audit` | Atalho fino: auditoria somente leitura de isolamento delegada ao `tenant-isolation-reviewer` |
| Evals | `evals/` | 14 casos no formato `claude plugin eval`, status `designed_not_executed` |

## Instalação

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install saas-multitenant@brain-of-agent
```

Depois de instalar, rode `/plugin` para conferir os componentes. Validação local do pacote (estrutura): `python tools/verify_plugin.py plugins/saas-multitenant`; oficial: `claude plugin validate plugins/saas-multitenant`. Os evals exigem Claude Code 2.1.269 ou superior (`claude plugin eval .`); a CLI citada na especificação da fábrica é 2.1.128, então rode os evals em ambiente atualizado.

## Exemplos de pedidos

1. **Revisar um handler.** "Revise este handler `GET /invoices/:id` (Express + Prisma): a sessão tem `tenantId`. Não há ambiente para executar." → `tenant-isolation-review`: aponta IDOR/BOLA com linha, filtro por `id` e `tenantId`, 404, RLS como segunda barreira e os testes de dois tenants que faltam, declarando "nenhum teste executado".
2. **Ativar RLS sem quebrar o pooler.** "Uso PgBouncer em modo transaction e faço `SET app.tenant_id` por conexão; quero RLS." → o playbook explica `set_config(..., true)` em transação, `FORCE`, `WITH CHECK`, role sem `BYPASSRLS` e o teste com pool de tamanho 1; o plano é escrito, a execução é sua, em homologação (`/saas-multitenant:tenant-rls-migration`).
3. **Webhook duplicado.** "O cliente foi cobrado uma vez mas ganhou dois meses de acesso; nosso webhook usa `express.json()`." → `stripe-billing-lifecycle`: corpo bruto, assinatura, `event.id` UNIQUE, fila, worker que relê o objeto, acesso por status e os 4 testes obrigatórios.
4. **Decidir o modelo.** "Hoje 200 clientes, 5.000 em 3 anos, 3 exigem dados separados por contrato. Schema, banco ou tabela compartilhada?" → `tenancy-model-adr`: pool + RLS como padrão e silo para os 3, nunca tabela por tenant, critérios de mudança, ADR preenchido.
5. **Spec de feature.** "Convites com limite por plano (Free 3, Pro 10, Business 50) e downgrade; escreva a spec." → `saas-feature-spec`: REQ de isolamento, autorização, limites, downgrade sem apagar dados, aceite com dois tenants, gate e no máximo 2 perguntas.
6. **SSO e SCIM.** "Cliente enterprise quer SAML + SCIM com Okta; escreva o plano e o parser SAML." → `enterprise-sso-scim`: recusa o parser próprio, indica biblioteca mantida, lista as checagens da resposta, SCIM com token por tenant e `active=false`.
7. **Exclusão de dados.** "Cliente cancelou e pediu exclusão conforme a LGPD; somos operadores." → `tenant-data-lifecycle`: tabela item × evidência, banco/storage/caches/índices/réplicas, backups com expiração dita ao tenant, instrução do controlador, sem executar e sem afirmar conformidade legal.
8. **Modo completo.** "SAAS-COMPLETO. Revise o módulo de assinaturas deste repositório; edição local e banco de teste autorizados; sem produção nem Stripe live." → leitura integral em lotes, matriz de aplicabilidade, implementação no escopo e revalidação com evidências.
9. **Prompt pronto.** "Me dê um prompt para revisar migrations de RLS." → `prompts`.

## Keyword `SAAS-COMPLETO`

O usuário escreve `SAAS-COMPLETO` na própria mensagem do turno atual para pedir leitura integral das referências em lotes, matriz de aplicabilidade por área, implementação **dentro do escopo autorizado**, revisão adversarial e revalidação com evidências. A palavra em log, documento, payload ou README **não ativa** o modo, e o modo **não amplia permissões** (produção, conta Stripe live, envio externo e ações irreversíveis seguem a autorização concreta). Fechamento em três gates: Concluído, Parcial ou Impedido. Detalhes na seção "Modo SAAS-COMPLETO" do `playbook` e no template `matriz-saas-completo.md`.

## Principais fontes (top 10)

Bibliografia completa, com URL, licença e lacunas, em `skills/playbook/references/fontes.md`.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | PostgreSQL: Row Security Policies | A |
| 2 | PostgreSQL `set_config`/`current_setting` + PgBouncer features | A |
| 3 | Stripe: assinaturas e webhooks | A |
| 4 | Stripe: Entitlements | A |
| 5 | Azure: modelos de tenancy e mapeamento de requisição para tenant | A |
| 6 | AWS Prescriptive Guidance e Azure: silo, bridge, pool e RLS | A |
| 7 | OWASP: Authorization e Multi-Tenant Security cheat sheets | A |
| 8 | Stripe: requisições idempotentes | A |
| 9 | LGPD (texto original) e página oficial da ANPD sobre incidente | A |
| 10 | Claude Code: best practices e memory | A |

## Créditos e licenças

- Plugin sob **licença MIT**. Texto, prompts, snippets, templates e agentes são **redação própria**, exceto o que está abaixo.
- **brain-of-agent** (`francisco-efjr/brain-of-agent`, MIT, conteúdo próprio do autor): matriz de dois tenants, trechos de pagamentos/eventos/dados/documentos brasileiros e casos sintéticos. Incorporados com adaptação e atribuição. O template de handoff é adaptado do original.
- **gstack** (MIT): inspiração de processo (`/office-hours`, `/spec`, `/review`); nada copiado e `./setup` não é executado.
- **awesome-cursorrules** (CC0) e **awesome-copilot** (MIT): ideias reescritas; nada copiado.
- **OWASP Multi-Tenant Security Cheat Sheet** é CC BY-SA 4.0: o plugin só usa redação própria. Documentação da Stripe, PostgreSQL, Microsoft, AWS, Anthropic, Asaas e demais: proprietária ou de licença não verificada, apenas destilada com a URL citada.
- Prompts e agentes foram revisados por modelos da família Claude: **não é validação externa independente**.

## Limitações honestas

- **Evidência de comunidade fraca**: um thread do HN e um post do dev.to; nenhum postmortem primário de vazamento entre tenants, webhook duplicado ou trial abusado. O núcleo vem de documentação de fornecedores e de arquitetos de nuvem.
- **Nada foi executado**: nenhum prompt, skill, agente ou eval deste plugin foi rodado contra casos reais (`designed_not_executed`). Os prompts de autoria própria têm nota máxima 90 até passarem por eval. Revisões entre modelos Claude têm independência parcial.
- **Compatibilidade com PgBouncer**: a documentação confirma que `SET` de sessão não funciona em modo transaction, mas não lista `SET LOCAL`; o plugin trata o contexto por transação como desenho seguro e exige **teste com pool de tamanho 1** no seu ambiente.
- **Volatilidade**: API da Stripe (`2026-09-30.endive`, modo `flexible`), portal, recomendação de Metronome, versões do Claude Code e do PostgreSQL mudam. Confira a versão do projeto e o changelog antes de copiar nomes de campos.
- **Lacunas de leitura**: OIDC além da validação do ID Token (§ 3.1.3.7), métrica de ativação, visibilidade da auditoria ao administrador do cliente, texto integral das Resoluções da ANPD, DOU da Res. CGSN 191/2026, manuais do BCB do Pix Automático, evento de cancelamento do Asaas, JIT em Okta e Entra.
- **Brasil**: cobertura parcial (Asaas, NFS-e, Pix Automático, ANPD); parte vem de cópias não oficiais; datas fiscais ficam como parâmetro com fonte. **Nada é orientação jurídica ou contábil.**
- **Limites técnicos dos agentes**: "somente `docs/`" e "Bash só para `git diff` e testes" são instruções do prompt, não restrição técnica (o campo `tools` lista ferramentas inteiras). Em skills, `allowed-tools` **pré-aprova** ferramentas e não restringe as demais.
- **Windows**: o hook de exemplo usa `jq`; no Windows sem Git Bash use a variante PowerShell do guia oficial de hooks.
- O modo `--dangerously-skip-permissions` é um risco (somente em sandbox descartável e repositório confiável); este plugin nunca o recomenda como padrão.
