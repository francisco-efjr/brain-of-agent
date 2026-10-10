# Catálogo de plugins (gerado)

Gerado por `tools/publish_brain.py` a partir do frontmatter dos plugins publicados. Marketplace: `brain-of-agent` (`claude plugin marketplace add francisco-efjr/brain-of-agent`).

| Plugin | Para quê | Skills | Agentes | Modo completo |
|---|---|---|---|---|
| `product-discovery-specs` | Transforma ideias e pedidos vagos em PRD enxuto, spec testável, critérios de aceite, histórias INVEST, priorização (RICE, ICE, MoSCoW, Kano), roadmap, OKRs e e… | acceptance-criteria, playbook, prioritize-roadmap, prompts, refine-backlog, run-discovery, spec-interview, spec-to-tasks, write-prd, write-spec | decision-recorder, discovery-synthesizer, feasibility-scout, plan-writer, spec-reviewer | PRODUTO-COMPLETO |
| `architecture-design` | Decisões de arquitetura com humano no comando: ADRs, trade-offs, revisão de desenho, system design, decomposição (DDD, monólito modular, strangler), resiliênci… | adr, adr-write, api-design, architecture-plan, decomposition, design-review, playbook, prompts, resilience-and-consistency, system-design | adr-writer, architecture-blueprint, architecture-reviewer, boundary-mapper, skeptic-architect | ARQUITETURA-COMPLETO |
| `web-frontend` | Guia, skills de tarefa, agentes somente leitura e biblioteca de prompts para frontend web com Claude Code (React e Next.js, Vue e Nuxt, Svelte, Angular, TypeSc… | a11y-review, component-review, design-ui, e2e-tests, forms-and-data, frontend-security-review, perf-audit, playbook, prompts, verify-ui | frontend-a11y-reviewer, frontend-code-reviewer, frontend-perf-reviewer, frontend-security-auditor, ui-evaluator | FRONTEND-COMPLETO |
| `backend-api` | Projete, implemente, revise, teste e depure serviços e APIs (REST, GraphQL, gRPC) com contrato OpenAPI, erros RFC 9457, autenticação e autorização, idempotênci… | agent-tool-design, api-contract-design, api-security-review, api-test-suite, backend-claude-md-setup, backend-debugging, idempotency-and-resilience, playbook, prompts, stack-conventions | api-contract-reviewer, api-security-reviewer, api-test-engineer, backend-architect, backend-debugger | BACKEND-COMPLETO |
| `mobile-apps` | Playbook, skills, agentes e prompts para construir, revisar, depurar e publicar apps mobile (iOS/SwiftUI, Android/Compose, React Native/Expo, Flutter): arquite… | mobile-accessibility-review, mobile-architecture-review, mobile-build-troubleshoot, mobile-performance-diagnosis, mobile-platform-features-check, mobile-release-pipeline, mobile-store-release-check, mobile-test-strategy, playbook, prompts, swift-ios-review | mobile-architect, mobile-pr-reviewer, mobile-release-auditor, mobile-security-auditor, mobile-test-engineer | MOBILE-COMPLETO |
| `database-data-modeling` | Modelagem, SQL, índices, planos de execução, transações, migrações sem downtime, multi-tenant e backup para PostgreSQL, MySQL, SQLite, SQL Server, MongoDB, Red… | backup-restore-runbook, db-agent-safety, db-schema-and-sql, nosql-data-modeling, playbook, prompts, query-plan-and-indexing, rls-tenant-review, safe-migrations, transactions-and-isolation | db-migration-planner, db-query-analyst, db-reviewer, db-schema-architect, db-security-auditor | DADOS-COMPLETO |
| `llm-ai-agents` | Playbook, skills de tarefa, subagentes somente leitura e biblioteca de prompts para projetar, revisar e testar aplicações LLM e agentes: engenharia de prompt e… | agent-architecture, agent-security-review, eval-design, instruction-authoring, llm-api-client-review, llm-decision-gates, llm-prompt-review, playbook, prompts, tool-design-review | agent-architect, agent-security-reviewer, eval-designer, prompt-reviewer, rag-pipeline-reviewer | IA-COMPLETO |
| `devops-cloud-infra` | Escreva, revise, planeje e diagnostique infraestrutura (Terraform/OpenTofu/Pulumi, Docker, Kubernetes/Helm, GitOps, GitHub Actions, segredos, canary/blue-green… | cloud-review, deploy-infra, gha-hardening-review, helm-gitops-review, iac-review, infra-troubleshoot, playbook, progressive-delivery, prompts, secrets-review | infra-reviewer, k8s-workload-auditor, pipeline-security-auditor, rollout-planner | DEVOPS-COMPLETO |
| `security-appsec` | Revisão de segurança de diffs e PRs, modelagem de ameaças (STRIDE), autorização por objeto e tenant, segredos, supply chain e triagem de risco de agentes, MCP … | access-control-review, agent-risk-triage, harden-claude-code, playbook, prompts, propose-patch, secrets-supply-chain-review, security-review-diff, threat-model, verify-finding | agent-config-auditor, finding-verifier, patch-reviewer, security-reviewer, threat-modeler | SEGURANCA-COMPLETO |
| `qa-testing` | QA e testes para o Claude Code: estratégia por risco, design de casos, TDD com vermelho confirmado, revisão de testes e E2E, triagem de testes flaky, bug repor… | bug-report, e2e-review, eval-design, flaky-triage, playbook, prompts, tdd-guard, test-design, test-strategy, verification-gate | qa-reporter, test-auditor, test-reviewer, test-writer | QA-COMPLETO |
| `code-quality-refactoring` | Revisão de código com filtro de alto sinal, debugging por causa raiz, refatoração segura com testes de caracterização, migração com juiz de paridade e triagem … | code-health-report, codebase-onboarding, debug-causa-raiz, migration-parity, playbook, prompts, refactor-seguro, review-diff, simplify-safe, tech-debt-triage | code-reviewer, codebase-mapper, debugger, finding-validator, refactor-planner | QUALIDADE-COMPLETO |
| `ux-ui-design` | Direção visual, auditoria de UI, avaliação heurística, acessibilidade WCAG 2.2 AA, design tokens, UX writing e pesquisa com usuários para trabalhar com Claude,… | a11y-checklist, design-brief, design-init, design-tokens, heuristic-eval, playbook, prompts, ui-audit, user-research-plan, ux-writing | a11y-reviewer, design-evaluator, design-system-auditor, ui-designer, ux-researcher | UXUI-COMPLETO |
| `git-workflow-release` | Fluxo de git com Claude Code do commit à release: commits convencionais, PRs pequenos e revisáveis, conflitos, rebase e revert seguros, bisect, semver, changel… | bisect-regressao, commit-convencional, criar-pr, encerrar-branch, playbook, prompts, rebase-seguro, release-cut, resolver-conflitos, triagem-contribuicao | auditor-politica-repo, auditor-release, revisor-diff, revisor-plano | RELEASE-COMPLETO |

**Em construção (ainda não publicados):** `data-engineering`, `data-science-ml`, `sre-observability`, `technical-writing-docs`, `game-development`, `systems-embedded-iot`, `cli-desktop-tooling`, `blockchain-web3`, `automation-integrations`, `saas-multitenant`, `fintech-payments`, `ecommerce-marketplace`. Para essas demandas, use o plugin mais próximo e declare a lacuna.

## product-discovery-specs (`product-discovery-specs` 0.1.0)

Transforma ideias e pedidos vagos em PRD enxuto, spec testável, critérios de aceite, histórias INVEST, priorização (RICE, ICE, MoSCoW, Kano), roadmap, OKRs e experimentos, com entrevista guiada, gates de aprovação humana, revisão adversarial em contexto novo e modo PRODUTO-COMPLETO por pedido explícito.

Instalar: `/plugin install product-discovery-specs@brain-of-agent` · Playbook: `plugins/product-discovery-specs/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/product-discovery-specs:acceptance-criteria` | Escreve e revisa critérios de aceite e histórias antes do código: caça palavras vagas, regras implícitas e requisitos não funcionais, escolhe o formato (regra + exemplo, Given/When/Then, EARS, checklist) e entrega crité… |
| `/product-discovery-specs:playbook` | Guia e router do segmento Produto, descoberta e especificação com IA. |
| `/product-discovery-specs:prioritize-roadmap` | Escolhe o framework de priorização pelo objeto (Opportunity Score, ICE, RICE, MoSCoW, Kano), pontua com origem declarada e versão da escala, mostra sensibilidade e monta roadmap Now-Next-Later, OKRs (objetivo + cerca de… |
| `/product-discovery-specs:prompts` | Biblioteca de prompts curados de Produto, descoberta e especificação. |
| `/product-discovery-specs:refine-backlog` | Refina o backlog: aplica INVEST, divide histórias e épicos em fatias verticais que entregam valor, conduz Example Mapping e three amigos em 25 minutos, verifica se a história está pronta (story-ready) e prepara o planej… |
| `/product-discovery-specs:run-discovery` | Prepara e sintetiza descoberta de produto com usuários em seis modos: interview-script (roteiro JTBD de 30 min, comportamento passado), tree (árvore de oportunidades), risks (quatro grandes riscos), synthesis (notas de … |
| `/product-discovery-specs:spec-interview` | Conduz uma entrevista guiada para transformar um pedido vago de feature em um SPEC.md autocontido e aprovado, antes de qualquer código. |
| `/product-discovery-specs:spec-to-tasks` | Transforma uma spec já aprovada pelo humano (gate G1) em tasks.md (T001 [P] [US1] com caminho exato e checkpoint por história), plano de implementação com IDs e critério de conclusão por fase, lista de features com pass… |
| `/product-discovery-specs:write-prd` | Escreve um PRD enxuto (600 a 1.000 palavras) com problema, objetivos mensuráveis, não-objetivos, requisitos de alto nível, riscos, premissas e faseamento, perguntando antes (até 3 perguntas) quando faltar problema, usuá… |
| `/product-discovery-specs:write-spec` | Formaliza material existente (PRD, notas, ticket, transcrição) em uma spec de feature testável com histórias P1/P2/P3, FR-NNN, SC-NNN sem tecnologia, premissas e [NEEDS CLARIFICATION]; escreve spec de bugfix (atual, esp… |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `product-discovery-specs:decision-recorder` (`plugins/product-discovery-specs/agents/decision-recorder.md`) | Registra decisões de produto duráveis (escopo, corte, trade-off, "não faremos") em um decision record com contexto, opções, justificativa, impacto no usuário e nas métricas e data de revisão. | Read, Grep, Glob, Write |
| `product-discovery-specs:discovery-synthesizer` (`plugins/product-discovery-specs/agents/discovery-synthesizer.md`) | Sintetiza notas ou transcrições de entrevistas com usuários, fornecidas em arquivos, em temas, oportunidades e premissas a testar, sem inventar fala, número ou participante, com tabela de evidências e rótulo do tamanho … | Read, Grep, Glob |
| `product-discovery-specs:feasibility-scout` (`plugins/product-discovery-specs/agents/feasibility-scout.md`) | Mapeia, somente leitura, o código existente que uma spec ou ideia toca (padrões, componentes reutilizáveis, pontos de integração, contratos, testes, dependências) e aponta o risco de viabilidade técnica com evidência ar… | Read, Grep, Glob |
| `product-discovery-specs:plan-writer` (`plugins/product-discovery-specs/agents/plan-writer.md`) | Transforma uma spec aprovada em plano de implementação com IDs rastreáveis (REQ, TASK, TEST, RISK, ASSUMPTION, ALT) e critério de conclusão mensurável por fase, verificável por comando. | Read, Grep, Glob, Write |
| `product-discovery-specs:spec-reviewer` (`plugins/product-discovery-specs/agents/spec-reviewer.md`) | Revisor adversarial, somente leitura e em contexto novo, de spec, PRD, histórias e critérios de aceite antes do código, e do diff contra a spec depois da implementação. | Read, Grep, Glob |

## architecture-design (`architecture-design` 0.2.0)

Decisões de arquitetura com humano no comando: ADRs, trade-offs, revisão de desenho, system design, decomposição (DDD, monólito modular, strangler), resiliência e consistência (retry, circuit breaker, outbox, saga, idempotência), contratos de API, C4/Mermaid e modo ARQUITETURA-COMPLETO.

Instalar: `/plugin install architecture-design@brain-of-agent` · Playbook: `plugins/architecture-design/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/architecture-design:adr` | Decide se uma decisão merece ADR, entrevista o decisor e rascunha o ADR no chat (somente leitura), ou responde 'por que escolhemos X?' lendo docs/adr/. |
| `/architecture-design:adr-write` | Grava no repositório um ADR já aprovado pelo usuário (adr-NNNN-slug.md), substitui um ADR aceito por um novo e atualiza o índice docs/adr/README.md, sempre mostrando o arquivo ou diff antes e pedindo aprovação. |
| `/architecture-design:api-design` | Desenha ou revisa o contrato de uma API HTTP entre times: recursos, semântica de métodos e status, idempotência, operações assíncronas com 202, paginação por cursor, erro padronizado RFC 9457 (application/problem+json),… |
| `/architecture-design:architecture-plan` | Conduz mudança arquitetural em arquivos de trabalho versionados, em quatro modos: pesquisar (research.md com arquivo:linha), planejar (plan.md com requisitos EARS, fases e rollback), anotar (incorpora notas do usuário a… |
| `/architecture-design:decomposition` | Decide entre monólito modular e serviços, mapeia bounded contexts e agregados, desenha fronteiras verificáveis por máquina (hexagonal, regra de dependência com verificador) e planeja extração gradual com strangler fig e… |
| `/architecture-design:design-review` | Revisa em modo somente leitura um plano, design doc, diff ou pasta de arquitetura antes de codar: desafia o escopo, mapeia o estado atual com arquivo:linha, aponta lacunas de correção e de requisitos, lista decisões D-n… |
| `/architecture-design:playbook` | Guia e router do segmento Arquitetura e design de sistemas. |
| `/architecture-design:prompts` | Biblioteca de prompts curados de Arquitetura e design de sistemas. |
| `/architecture-design:resilience-and-consistency` | Escolhe e revisa padrões de resiliência e consistência entre serviços: retry com jitter em uma só camada, circuit breaker, bulkhead, consumidor idempotente, transactional outbox, saga, CQRS e event sourcing, com 'quando… |
| `/architecture-design:system-design` | Conduz o design de um sistema novo ou a evolução de um existente em seis fases (clarificar, estimar, desenhar, trade-offs, modos de falha, iterar), com estimativa de ordem de grandeza feita no texto, diagrama Mermaid de… |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `architecture-design:adr-writer` (`plugins/architecture-design/agents/adr-writer.md`) | Redator de ADR que estrutura e grava um Architecture Decision Record somente depois de uma decisão humana e de aprovação explícita. | Read, Grep, Glob, Write |
| `architecture-design:architecture-blueprint` (`plugins/architecture-design/agents/architecture-blueprint.md`) | Arquiteto sênior somente leitura que entrega um blueprint decisivo para uma feature ou mudança que cruza módulos, ancorado nos padrões reais do código (uma recomendação, 1 a 3 alternativas descartadas, mapa de arquivos,… | Read, Grep, Glob |
| `architecture-design:architecture-reviewer` (`plugins/architecture-design/agents/architecture-reviewer.md`) | Revisor adversarial de arquitetura, somente leitura e em contexto novo, que compara uma diff, um plano (PLAN.md) ou um ADR proposto com os requisitos declarados e reporta apenas lacunas de correção ou de requisito, com … | Read, Grep, Glob |
| `architecture-design:boundary-mapper` (`plugins/architecture-design/agents/boundary-mapper.md`) | Mapeador de fronteiras somente leitura que levanta módulos, camadas e bounded contexts reais de um código, extrai as dependências efetivas por busca de imports, compara com a regra declarada, aponta violações com arquiv… | Read, Grep, Glob |
| `architecture-design:skeptic-architect` (`plugins/architecture-design/agents/skeptic-architect.md`) | Arquiteto cético somente leitura que desafia as premissas de uma proposta, mostra a opção mais simples que atende aos requisitos, diz o que não construir e faz um pré-mortem de 12 meses, sem decidir pelo humano. | Read, Grep, Glob |

## web-frontend (`web-frontend` 0.1.0)

Guia, skills de tarefa, agentes somente leitura e biblioteca de prompts para frontend web com Claude Code (React e Next.js, Vue e Nuxt, Svelte, Angular, TypeScript, Tailwind, WCAG 2.2, Core Web Vitals, formulários, data fetching e testes de UI), sempre com verificação por evidência.

Instalar: `/plugin install web-frontend@brain-of-agent` · Playbook: `plugins/web-frontend/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/web-frontend:a11y-review` | Audita acessibilidade de componentes, telas e fluxos contra WCAG 2.2 AA e relata antes de corrigir: HTML nativo antes de ARIA, nome acessível, rótulo e erro de formulário, teclado e foco, diálogos, contraste, alvo mínim… |
| `/web-frontend:component-review` | Revisa componentes web por correção primeiro e performance por impacto depois (React, Next.js App Router e TSX como eixo; Vue, Nuxt, Svelte e Angular pelas regras do playbook) ou, no modo depurar, isola a causa de bug d… |
| `/web-frontend:design-ui` | Cria ou redesenha UI web em código (landing, dashboard, componente de produto) em fases: brief de 3 linhas, plano com tokens e wireframe ASCII, revisão contra o genérico, build com piso de qualidade e crítica com captur… |
| `/web-frontend:e2e-tests` | Escreve, revisa e estabiliza testes de UI com Playwright (e2e, componente, visual e acessibilidade com axe) e orienta migração guiada por arquivo de regras, por exemplo Cypress para Playwright. |
| `/web-frontend:forms-and-data` | Implementa e revisa formulários acessíveis e fluxos de dados (busca, estado de servidor, cache, SSR/ISR) respeitando framework e versão: validação nativa e no servidor, erro ligado ao campo, Server Actions com useAction… |
| `/web-frontend:frontend-security-review` | Revisa, só em leitura, riscos de segurança do lado do cliente em código de frontend: sinks de DOM (innerHTML, dangerouslySetInnerHTML, v-html, {@html}, bypassSecurityTrust), origem do dado e sanitização, segredo em vari… |
| `/web-frontend:perf-audit` | Diagnostica lentidão de página web (LCP, INP, CLS, bundle e entrega) a partir de evidência medida e liga cada causa a arquivos do projeto, com correções priorizadas e plano para remedir nas mesmas condições. |
| `/web-frontend:playbook` | Guia e router do segmento Frontend web (React, Next.js, Vue, Nuxt, Svelte, Angular, TypeScript, Tailwind, acessibilidade, performance, formulários, data fetching, testes de UI, design-to-code). |
| `/web-frontend:prompts` | Biblioteca de prompts curados do segmento Frontend web (React, Next.js, Vue, Nuxt, Svelte, Angular, TypeScript, Tailwind, acessibilidade, performance, formulários, testes de UI, design-to-code). |
| `/web-frontend:verify-ui` | Prova por evidência que uma mudança de UI funciona: escreve o critério de aceite antes, roda os checks do projeto com autorização, abre a tela em 320 px e desktop (Chrome conectado, Playwright do projeto ou capturas do … |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `web-frontend:frontend-a11y-reviewer` (`plugins/web-frontend/agents/frontend-a11y-reviewer.md`) | Revisor somente leitura de acessibilidade de UI web contra WCAG 2.2 AA (React, Next.js, Vue, Nuxt, Svelte, Angular, HTML e CSS), em contexto limpo. | Read, Grep, Glob |
| `web-frontend:frontend-code-reviewer` (`plugins/web-frontend/agents/frontend-code-reviewer.md`) | Revisor adversarial somente leitura de diffs, componentes e PRs de teste de frontend web (React, Next.js, Vue, Nuxt, Svelte, Angular, TypeScript, Tailwind, Playwright, Vitest), em contexto limpo, que confere requisito a… | Read, Grep, Glob |
| `web-frontend:frontend-perf-reviewer` (`plugins/web-frontend/agents/frontend-perf-reviewer.md`) | Diagnostica lentidão de página web (LCP, INP, CLS, bundle, hidratação, cascata de requisições) a partir de evidência entregue pelo chamador e liga cada causa ao arquivo provável, em modo somente leitura. | Read, Grep, Glob |
| `web-frontend:frontend-security-auditor` (`plugins/web-frontend/agents/frontend-security-auditor.md`) | Auditor de segurança do lado do cliente web, somente leitura. | Read, Grep, Glob |
| `web-frontend:ui-evaluator` (`plugins/web-frontend/agents/ui-evaluator.md`) | Avaliador independente e cético de tela de produto web a partir de capturas em mobile e desktop e do brief ou plano de UI, com nota de 0 a 10 em design, originalidade, craft e funcionalidade, e veredito de aprovação. | Read, Grep, Glob |

## backend-api (`backend-api` 0.1.0)

Projete, implemente, revise, teste e depure serviços e APIs (REST, GraphQL, gRPC) com contrato OpenAPI, erros RFC 9457, autenticação e autorização, idempotência, paginação, rate limiting e tools para agentes, sempre com verificação por evidência.

Instalar: `/plugin install backend-api@brain-of-agent` · Playbook: `plugins/backend-api/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/backend-api:agent-tool-design` | Do lado do serviço/API: desenha, revisa e avalia tools e endpoints consumidos por agentes (function calling, servidor MCP) e integra corretamente a API de um modelo Claude/LLM num backend (tool_use, stop_reason, streami… |
| `/backend-api:api-contract-design` | Desenha, documenta, revisa e evolui o contrato de uma API (REST; GraphQL e gRPC por referência): recursos, status, schemas, erros RFC 9457, paginação por cursor, ETag/cache, operações longas, versionamento, OpenAPI e cl… |
| `/backend-api:api-security-review` | Audita a segurança de uma API ou serviço (diff, PR, módulo ou endpoint) com a grade OWASP API Security Top 10 2023, validação de JWT/OAuth2 e hardening REST; somente leitura, relatório de achados com severidade, confian… |
| `/backend-api:api-test-suite` | Projeta e escreve testes de API (REST, GraphQL, gRPC, eventos, webhooks) que provam regra de negócio, não só status: oráculo independente, authN x authZ com dois usuários, erro RFC 9457, idempotência, paginação, concorr… |
| `/backend-api:backend-claude-md-setup` | Gera ou atualiza o bloco de CLAUDE.md de um projeto backend a partir do repositório real (stack, versões, comandos, camadas) e dos snippets validados do plugin, com teste de remoção, tamanho limitado e confirmação do di… |
| `/backend-api:backend-debugging` | Diagnostica e corrige defeitos de backend com causa raiz antes de correção: erro 500, falha intermitente, timeout, regressão, divergência local x produção, endpoint lento, N+1, esgotamento de pool de conexões. |
| `/backend-api:idempotency-and-resilience` | Torna operações de um serviço seguras sob retry, duplicação e falha parcial: chave de idempotência atômica no banco, timeouts e retries com backoff, rate limiting, webhooks (HMAC, replay, dedupe), filas/jobs at-least-on… |
| `/backend-api:playbook` | Guia e router do segmento Backend e APIs — desenhar, implementar, revisar, testar e depurar serviços e APIs (REST, GraphQL, gRPC) com contrato OpenAPI, erros RFC 9457, autenticação e autorização, validação, idempotência… |
| `/backend-api:prompts` | Biblioteca de prompts curados do segmento Backend e APIs, prontos para colar ou executar. |
| `/backend-api:stack-conventions` | Revisa ou escreve código de serviço seguindo as convenções verificadas da stack do projeto e a versão instalada: FastAPI (camadas, response_model, auth), Go net/http 1.22+, NestJS (guards), Spring Security (resource ser… |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `backend-api:api-contract-reviewer` (`plugins/backend-api/agents/api-contract-reviewer.md`) | Revisor de contrato e compatibilidade de API em contexto novo. | Read, Grep, Glob, Bash |
| `backend-api:api-security-reviewer` (`plugins/backend-api/agents/api-security-reviewer.md`) | Auditor de segurança de API e serviços backend, somente leitura e em contexto novo. | Read, Grep, Glob |
| `backend-api:api-test-engineer` (`plugins/backend-api/agents/api-test-engineer.md`) | Engenheiro de testes de API (REST, GraphQL, gRPC, eventos e webhooks). | Read, Grep, Glob, Bash, Edit, Write |
| `backend-api:backend-architect` (`plugins/backend-api/agents/backend-architect.md`) | Arquiteto de serviço backend que entrega decisões, contratos esboçados e ADR, não código. | Read, Grep, Glob |
| `backend-api:backend-debugger` (`plugins/backend-api/agents/backend-debugger.md`) | Depurador de causa raiz para backend e APIs, com correção mínima e teste de regressão. | Read, Grep, Glob, Bash, Edit, Write |

## mobile-apps (`mobile-apps` 0.1.0)

Playbook, skills, agentes e prompts para construir, revisar, depurar e publicar apps mobile (iOS/SwiftUI, Android/Compose, React Native/Expo, Flutter): arquitetura, offline-first, push, permissões, performance, acessibilidade, testes e checklists de App Store e Google Play, com gates de confirmação antes de qualquer envio.

Instalar: `/plugin install mobile-apps@brain-of-agent` · Playbook: `plugins/mobile-apps/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/mobile-apps:mobile-accessibility-review` | Revisa a acessibilidade de telas mobile (SwiftUI, Compose, React Native, Flutter): rótulos, hints, agrupamento, ordem de foco, alvos de toque, texto escalável, contraste, movimento reduzido e gestos, para VoiceOver e Ta… |
| `/mobile-apps:mobile-architecture-review` | Revisa ou projeta a arquitetura de um app mobile: camadas UI/dados/domínio, dono do estado, fluxo unidirecional, ViewModel e repositório, navegação, injeção de dependência e design offline-first com sincronização e conf… |
| `/mobile-apps:mobile-build-troubleshoot` | Diagnostica falhas de build, sync e dependências em apps mobile (Gradle e AGP, Kotlin, CocoaPods e SPM, Xcode, Metro, Expo prebuild, flutter pub) e planeja atualização de SDK (Expo SDK, React Native, AGP, targetSdk, Flu… |
| `/mobile-apps:mobile-performance-diagnosis` | Diagnostica lentidão, jank, recomposição ou re-render excessivo, cold start e consumo de bateria em apps mobile (Compose, SwiftUI, Flutter, React Native), um eixo por vez e sempre com medição antes e depois. |
| `/mobile-apps:mobile-platform-features-check` | Audita, somente leitura, recursos de plataforma de apps mobile: push (APNs e FCM), permissões em tempo de execução e purpose strings, deep links (Universal Links e App Links) e armazenamento seguro (Keychain, Keystore),… |
| `/mobile-apps:mobile-release-pipeline` | Prepara e, somente após confirmação explícita do usuário, conduz passos de pipeline de release mobile: EAS Build/Submit/Update, fastlane match e pilot, archive e TestFlight pelo Xcode, publicação Play por Gradle. |
| `/mobile-apps:mobile-store-release-check` | Audita, somente leitura, a prontidão de um app mobile para App Store e Google Play: App Review Guidelines, privacy manifest, purpose strings, target API, exclusão de conta, Data safety, permissões sensíveis e conta de d… |
| `/mobile-apps:mobile-test-strategy` | Define a estratégia e o plano de testes de apps mobile por camada e por plataforma: unitário, ViewModel com fake, UI (Compose test, XCTest e XCUIAutomation, widget test, React Native Testing Library), integração e E2E (… |
| `/mobile-apps:playbook` | Guia e router do segmento Aplicativos mobile (iOS/SwiftUI, Android/Compose, React Native/Expo, Flutter). |
| `/mobile-apps:prompts` | Biblioteca de prompts curados do segmento de aplicativos mobile (iOS/SwiftUI, Android/Compose, React Native/Expo, Flutter). |
| `/mobile-apps:swift-ios-review` | Revisa código Swift e SwiftUI: APIs obsoletas, views, dados e estado, navegação, acessibilidade, performance, e triagem de erros de Swift Concurrency (Sendable, isolamento, @MainActor, Swift 6). |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `mobile-apps:mobile-architect` (`plugins/mobile-apps/agents/mobile-architect.md`) | Arquiteto mobile somente leitura que desenha ou revisa a arquitetura de um app (camadas, dono do estado, navegação, offline-first com sincronização e conflitos, escolha nativo vs React Native/Expo vs Flutter) e devolve … | Read, Grep, Glob |
| `mobile-apps:mobile-pr-reviewer` (`plugins/mobile-apps/agents/mobile-pr-reviewer.md`) | Revisor adversarial somente leitura de diffs e PRs de apps mobile (SwiftUI, Compose, React Native/Expo, Flutter) em contexto limpo, que confere requisito a requisito, casos de borda com teste, mudanças fora do escopo e … | Read, Grep, Glob |
| `mobile-apps:mobile-release-auditor` (`plugins/mobile-apps/agents/mobile-release-auditor.md`) | Auditor somente leitura de prontidão para App Store e Google Play que lê Info.plist, PrivacyInfo.xcprivacy, entitlements, AndroidManifest, Gradle e app.json/app.config e devolve um relatório por prioridade (risco prováv… | Read, Grep, Glob |
| `mobile-apps:mobile-security-auditor` (`plugins/mobile-apps/agents/mobile-security-auditor.md`) | Auditor de segurança de apps mobile, somente leitura, organizado pelos oito grupos do OWASP MASVS (armazenamento, criptografia, autenticação, rede, plataforma, código, resiliência, privacidade), procurando segredos e ch… | Read, Grep, Glob |
| `mobile-apps:mobile-test-engineer` (`plugins/mobile-apps/agents/mobile-test-engineer.md`) | Engenheiro de testes mobile que escreve ou ajusta testes (unitário com fake, Compose test, Swift Testing e XCTest, widget test, Jest e React Native Testing Library, fluxos Maestro) no framework que o projeto já usa e ex… | Read, Grep, Glob, Edit, Write, Bash |

## database-data-modeling (`database-data-modeling` 0.1.0)

Modelagem, SQL, índices, planos de execução, transações, migrações sem downtime, multi-tenant e backup para PostgreSQL, MySQL, SQLite, SQL Server, MongoDB, Redis e DynamoDB, com agentes somente leitura e rótulos de evidência.

Instalar: `/plugin install database-data-modeling@brain-of-agent` · Playbook: `plugins/database-data-modeling/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/database-data-modeling:backup-restore-runbook` | Cria e revisa planos e runbooks de backup, restore e PITR (PostgreSQL em profundidade; Redis detalhado; MySQL, SQL Server, MongoDB, DynamoDB, SQLite em modo genérico) com RPO/RTO, teste de restauração em ambiente isolad… |
| `/database-data-modeling:db-agent-safety` | Manual. |
| `/database-data-modeling:db-schema-and-sql` | Projeta e revisa schema relacional e SQL (PostgreSQL, MySQL, SQLite, SQL Server): tabelas, chaves, constraints, tipos, normalização, índices de suporte, consultas parametrizadas e privilégios do papel da aplicação. |
| `/database-data-modeling:nosql-data-modeling` | Modela e revisa dados NoSQL pelo padrão de acesso: MongoDB (embutir vs referenciar, limite de 16 MB, antipadrões), DynamoDB (partition/sort key, GSIs, chaves de alta cardinalidade) e Redis (estrutura, nomes de chave, pe… |
| `/database-data-modeling:playbook` | Guia e router do segmento Bancos de dados e modelagem. |
| `/database-data-modeling:prompts` | Biblioteca de prompts curados do segmento Bancos de dados e modelagem - 28 prompts prontos para revisar migração (PostgreSQL, MySQL), planejar expand/contract e backfill, ensaiar migração, ler EXPLAIN, diagnosticar cons… |
| `/database-data-modeling:query-plan-and-indexing` | Diagnostica consultas lentas, interpreta planos de execução (PostgreSQL EXPLAIN ANALYZE/BUFFERS; SQLite com limite de fonte; MySQL e SQL Server em modo genérico) e desenha índices (multicoluna, cobertura, expressão, par… |
| `/database-data-modeling:rls-tenant-review` | Escolhe e revisa o isolamento multi-tenant em banco relacional (tenant_id compartilhado, schema por tenant, banco por tenant, sharding) e audita Row-Level Security do PostgreSQL: políticas USING/WITH CHECK, BYPASSRLS, F… |
| `/database-data-modeling:safe-migrations` | Planeja e revisa migrações de banco sem downtime: lock por DDL, CREATE INDEX CONCURRENTLY, NOT VALID/VALIDATE, expand/contract, backfill em lotes, rollback e ensaio em cópia; trata migração gerada por ORM (Alembic, Djan… |
| `/database-data-modeling:transactions-and-isolation` | Analisa transações, níveis de isolamento, locks, deadlocks e race conditions (estoque negativo, saldo, reserva, upsert) por SGBD e propõe correção (UPDATE condicional, lock explícito, controle otimista, retry de 40001) … |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `database-data-modeling:db-migration-planner` (`plugins/database-data-modeling/agents/db-migration-planner.md`) | Transforma uma mudança de schema ou de dados em plano por fases (expand, backfill, verificação, migrate, contract, limpeza) com lock declarado por DDL, orçamentos, critério de interrupção, rollback versus restauração e … | Read, Grep, Glob |
| `database-data-modeling:db-query-analyst` (`plugins/database-data-modeling/agents/db-query-analyst.md`) | Interpreta planos de execução e consultas lentas (PostgreSQL EXPLAIN ANALYZE e BUFFERS em profundidade; SQLite EXPLAIN QUERY PLAN; MySQL e SQL Server em modo genérico), detecta N+1 de ORM e propõe índices, reescritas e … | Read, Grep, Glob |
| `database-data-modeling:db-reviewer` (`plugins/database-data-modeling/agents/db-reviewer.md`) | Revisor adversarial somente leitura, em contexto limpo, de mudanças de banco de dados - migrações, DDL, SQL e consultas de ORM, índices, transações, RLS e modelos NoSQL (PostgreSQL, MySQL, SQLite, SQL Server, MongoDB, R… | Read, Grep, Glob |
| `database-data-modeling:db-schema-architect` (`plugins/database-data-modeling/agents/db-schema-architect.md`) | Desenha modelo de dados - relacional por invariantes e consultas críticas; MongoDB, DynamoDB e Redis pelos padrões de acesso - com ADR curto, índices de suporte, estratégia de tenancy e particionamento só quando necessá… | Read, Grep, Glob |
| `database-data-modeling:db-security-auditor` (`plugins/database-data-modeling/agents/db-security-auditor.md`) | Audita segurança de dados em código e configuração, somente leitura - injeção SQL e NoSQL, privilégios do papel da aplicação, segredos de banco, Row-Level Security e isolamento multi-tenant, exposição de dados em logs e… | Read, Grep, Glob |

## llm-ai-agents (`llm-ai-agents` 0.1.0)

Playbook, skills de tarefa, subagentes somente leitura e biblioteca de prompts para projetar, revisar e testar aplicações LLM e agentes: engenharia de prompt e de contexto, tool use e MCP, RAG medido, evals e LLM-as-judge, defesa contra prompt injection, custo e cache, e autoria de CLAUDE.md, skills e plugins.

Instalar: `/plugin install llm-ai-agents@brain-of-agent` · Playbook: `plugins/llm-ai-agents/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/llm-ai-agents:agent-architecture` | Projeta e revisa arquitetura de agentes e workflows com LLM: workflow ou agente, multiagente, delegação a subagentes, gestão de contexto, harness de tarefa longa, escolha entre Agent SDK, CLI, SDK cliente e Managed Agen… |
| `/llm-ai-agents:agent-security-review` | Revisa a segurança de agentes e apps LLM: prompt injection direta e indireta, trifecta letal, Regra de Dois (cartão A/B/C), permissões, exfiltração, agência excessiva, OWASP LLM Top 10. |
| `/llm-ai-agents:eval-design` | Projeta avaliações para aplicações LLM, agentes, RAG, skills e plugins: dataset a partir de falhas reais, graders de código, juiz LLM binário calibrado, pass@k e pass^k, `claude plugin eval`. |
| `/llm-ai-agents:instruction-authoring` | Escreve e revisa CLAUDE.md, AGENTS.md, skills (SKILL.md), subagentes e plugins do Claude Code, e escolhe onde colocar cada instrução (hook, regra, skill, subagente). |
| `/llm-ai-agents:llm-api-client-review` | Revisa código que chama a API Claude ou o Agent SDK: loop de tool use, tool_choice, saídas estruturadas, streaming, citações, prompt caching, contagem de tokens, telemetria OpenTelemetry. |
| `/llm-ai-agents:llm-decision-gates` | Decide entre prompt, RAG e fine-tuning; planeja RAG (chunking, embeddings, reranking, citações) com medição; escolhe modelo e effort; estima custo e latência com preços datados, cache e Batch. |
| `/llm-ai-agents:llm-prompt-review` | Revisa, reescreve e poda prompts, system prompts, templates e prompts de agente para modelos Claude atuais, com checklist de 12 itens e plano de teste. |
| `/llm-ai-agents:playbook` | Guia e router do segmento Aplicações LLM, agentes e engenharia de prompt. |
| `/llm-ai-agents:prompts` | Biblioteca de 39 prompts curados para LLM e agentes, prontos para colar, com variáveis, motivo e fonte. |
| `/llm-ai-agents:tool-design-review` | Revisa e melhora definições de tools para agentes e servidores MCP: descrição, schema, nomes de parâmetro, erros, formato de saída, paginação, orçamento de tokens, segurança e autorização MCP. |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `llm-ai-agents:agent-architect` (`plugins/llm-ai-agents/agents/agent-architect.md`) | Arquiteto de agentes e workflows com LLM, somente leitura, que analisa requisitos e código existente e devolve um brief de arquitetura: chamada única, workflow ou agente; multiagente só se justificado; contexto, delegaç… | Read, Grep, Glob |
| `llm-ai-agents:agent-security-reviewer` (`plugins/llm-ai-agents/agents/agent-security-reviewer.md`) | Auditor de segurança, somente leitura, de agentes e apps LLM: prompt injection direta e indireta, trifecta letal e Regra de Dois (cartão A/B/C), permissões e allowlists, exfiltração, saída do modelo tratada como confiáv… | Read, Grep, Glob |
| `llm-ai-agents:eval-designer` (`plugins/llm-ai-agents/agents/eval-designer.md`) | Projetista de avaliações para prompts, agentes, RAG, skills e plugins, somente leitura: monta suíte de 20 a 50 casos a partir de falhas reais, rubrica, graders de código antes de juiz LLM, plano de calibração do juiz (T… | Read, Grep, Glob |
| `llm-ai-agents:prompt-reviewer` (`plugins/llm-ai-agents/agents/prompt-reviewer.md`) | Revisor somente leitura, em contexto limpo, de prompts de aplicação, system prompts, templates, SKILL.md, subagentes, comandos e CLAUDE.md/AGENTS.md para modelos Claude atuais: motivo das regras, tom, estrutura XML, exe… | Read, Grep, Glob |
| `llm-ai-agents:rag-pipeline-reviewer` (`plugins/llm-ai-agents/agents/rag-pipeline-reviewer.md`) | Revisor somente leitura de código e configuração de RAG e de uso de citações: gate 'a base cabe no contexto?', chunking medido, embeddings e input_type, busca híbrida, reranking, filtro por tenant, citações (documentos … | Read, Grep, Glob |

## devops-cloud-infra (`devops-cloud-infra` 0.1.0)

Escreva, revise, planeje e diagnostique infraestrutura (Terraform/OpenTofu/Pulumi, Docker, Kubernetes/Helm, GitOps, GitHub Actions, segredos, canary/blue-green, serverless e custo) com gate humano antes de qualquer mudança real e evidência executável em cada entrega.

Instalar: `/plugin install devops-cloud-infra@brain-of-agent` · Playbook: `plugins/devops-cloud-infra/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/devops-cloud-infra:cloud-review` | Revisa serviços e arquitetura na nuvem - AWS Lambda, Azure Functions, Cloud Run - e questões de Well-Architected (AWS, GCP, Azure), custo e FinOps (Infracost, Cost Optimization) e plataforma interna (golden path, self-s… |
| `/devops-cloud-infra:deploy-infra` | Conduz plano, revisão e aplicação de uma mudança de infraestrutura já revisada, com gates de aprovação, alvo confirmado e verificação pós-mudança. |
| `/devops-cloud-infra:gha-hardening-review` | Revisa e escreve workflows do GitHub Actions e pipelines de CI/CD com foco em segurança e confiabilidade - pin por SHA, permissions mínimas, script injection, pull_request_target, OIDC, environments com aprovação, cache… |
| `/devops-cloud-infra:helm-gitops-review` | Escreve e revisa Helm charts (Chart.yaml, values, templates) contra as convenções oficiais, roda lint e renderização local, e revisa configuração GitOps - Argo CD (Application, ApplicationSet, sync, prune, self-heal) e … |
| `/devops-cloud-infra:iac-review` | Escreve e revisa infraestrutura como código - Terraform/OpenTofu/Pulumi, Dockerfile, docker-compose e manifests Kubernetes - contra checklists de segurança e boas práticas oficiais; na revisão devolve achados por severi… |
| `/devops-cloud-infra:infra-troubleshoot` | Diagnostica em modo leitura por que um deploy, Pod, release Helm, sync do Argo CD ou Flux, terraform plan/apply ou job de CI/CD falhou e propõe a correção com evidência - CrashLoopBackOff, ImagePullBackOff, Pending, OOM… |
| `/devops-cloud-infra:playbook` | Guia e router do segmento DevOps, cloud e infraestrutura. |
| `/devops-cloud-infra:progressive-delivery` | Planeja e revisa deploy progressivo - blue-green, canary, Argo Rollouts, Flagger, feature flags - com critérios de rollout e rollback definidos antes do deploy, incluindo o que não reverte (schema, state, dados, e-mail … |
| `/devops-cloud-infra:prompts` | Biblioteca de 32 prompts curados de DevOps, cloud e infraestrutura, prontos para colar, com variáveis, motivo e fontes. |
| `/devops-cloud-infra:secrets-review` | Revisa como segredos são criados, guardados, injetados e rotacionados em IaC, Kubernetes, Docker, GitOps e CI, sem expor valores - cita só tipo e arquivo:linha e recomenda rotação quando o segredo esteve em Git, imagem … |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `devops-cloud-infra:infra-reviewer` (`plugins/devops-cloud-infra/agents/infra-reviewer.md`) | Revisor independente e somente leitura de mudanças de infraestrutura como código (Terraform/OpenTofu/Pulumi, Dockerfile, docker-compose, manifests Kubernetes, Helm, workflows do GitHub Actions) em contexto limpo. | Read, Grep, Glob |
| `devops-cloud-infra:k8s-workload-auditor` (`plugins/devops-cloud-infra/agents/k8s-workload-auditor.md`) | Auditor somente leitura de manifests Kubernetes e charts Helm já renderizados quanto a Pod Security Standards, securityContext, RBAC, NetworkPolicy, probes, requests/limits, Secrets e imagens. | Read, Grep, Glob |
| `devops-cloud-infra:pipeline-security-auditor` (`plugins/devops-cloud-infra/agents/pipeline-security-auditor.md`) | Auditor somente leitura de workflows do GitHub Actions e pipelines de CI/CD - injeção de script, pull_request_target, permissions, pin por SHA, segredos, environments, cache, runners, claude-code-action, gates que masca… | Read, Grep, Glob |
| `devops-cloud-infra:rollout-planner` (`plugins/devops-cloud-infra/agents/rollout-planner.md`) | Planejador somente leitura de mudança de infraestrutura e de rollout/rollback. | Read, Grep, Glob |

## security-appsec (`security-appsec` 0.1.0)

Revisão de segurança de diffs e PRs, modelagem de ameaças (STRIDE), autorização por objeto e tenant, segredos, supply chain e triagem de risco de agentes, MCP e plugins, com OWASP Top 10:2025, API Top 10, LLM Top 10 e ASVS, somente leitura por padrão.

Instalar: `/plugin install security-appsec@brain-of-agent` · Playbook: `plugins/security-appsec/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/security-appsec:access-control-review` | Revisa, só em leitura, a autorização de rotas, handlers, consultas, filas, exports e downloads: checagem no servidor, por objeto (IDOR/BOLA), por função (BFLA), por propriedade (mass assignment) e por tenant, com matriz… |
| `/security-appsec:agent-risk-triage` | Tria o risco de um agente, skill, subagente, servidor MCP, plugin ou integração antes de instalar ou conceder acesso: inventário de capacidades, teste da tríade letal (dados privados + conteúdo não confiável + comunicaç… |
| `/security-appsec:harden-claude-code` | Audita em leitura e propõe a configuração de segurança do Claude Code de um projeto: permissions.deny para .env, chaves e segredos, modos de permissão (bypass e auto), hook PreToolUse que bloqueia comando destrutivo com… |
| `/security-appsec:playbook` | Guia e router de segurança de aplicações (appsec) - revisão de código, diff ou PR, modelagem de ameaças (STRIDE), autorização por objeto e tenant (IDOR/BOLA), injeção, XSS, SSRF, autenticação e sessão, segredos, supply … |
| `/security-appsec:prompts` | Biblioteca de prompts curados de segurança de aplicações, prontos para colar ou executar. |
| `/security-appsec:propose-patch` | Rascunha a correção mínima de um achado de segurança já verificado, com teste de regressão que falha antes e passa depois, e a submete a revisão independente (agente patch-reviewer) antes de entregar. |
| `/security-appsec:secrets-supply-chain-review` | Revisa, só em leitura, segredos no código, no histórico e no CI, dependências (typosquatting, scripts de instalação, lockfiles, alerta de CVE x caminho de uso), workflows de CI (permissões, Actions fixadas por SHA, inje… |
| `/security-appsec:security-review-diff` | Revisa, só em leitura, o diff de uma branch, PR ou lista de arquivos e relata apenas as vulnerabilidades que esta mudança introduz (injeção SQL/comando, XSS, SSRF, autenticação, autorização/IDOR, segredos, cripto fraca,… |
| `/security-appsec:threat-model` | Modela as ameaças de uma feature ou sistema em quatro fases: escopo e ativos, DFD textual com fronteiras de confiança, STRIDE por fluxo que cruza fronteira, resposta por ameaça (mitigar, eliminar, transferir, aceitar) c… |
| `/security-appsec:verify-finding` | Tenta refutar, lendo o código, um achado de segurança (do modelo, de scanner SAST/DAST, de pentest ou de colega) e decide Mantido, Rebaixado ou Refutado com prova em arquivo:linha. |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `security-appsec:agent-config-auditor` (`plugins/security-appsec/agents/agent-config-auditor.md`) | Auditor somente leitura de configuração e superfície de risco de agentes de IA. | Read, Glob, Grep |
| `security-appsec:finding-verifier` (`plugins/security-appsec/agents/finding-verifier.md`) | Verificador cético somente leitura que tenta derrubar um achado de segurança antes de ele ir ao relatório. | Read, Glob, Grep |
| `security-appsec:patch-reviewer` (`plugins/security-appsec/agents/patch-reviewer.md`) | Revisor independente somente leitura de patch de segurança. | Read, Glob, Grep |
| `security-appsec:security-reviewer` (`plugins/security-appsec/agents/security-reviewer.md`) | Revisor de segurança de aplicações somente leitura e em contexto novo. | Read, Glob, Grep |
| `security-appsec:threat-modeler` (`plugins/security-appsec/agents/threat-modeler.md`) | Analista de modelagem de ameaças somente leitura. | Read, Glob, Grep |

## qa-testing (`qa-testing` 0.1.0)

QA e testes para o Claude Code: estratégia por risco, design de casos, TDD com vermelho confirmado, revisão de testes e E2E, triagem de testes flaky, bug reports com evidência e evals de skills e LLM, com gate de verificação e o modo QA-COMPLETO.

Instalar: `/plugin install qa-testing@brain-of-agent` · Playbook: `plugins/qa-testing/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/qa-testing:bug-report` | Transforma um sintoma em bug report reproduzível e decidível; reduz o caso ao mínimo, classifica severidade e prioridade, conduz triagem, verificação da correção e escape analysis. |
| `/qa-testing:e2e-review` | Revisa ou escreve testes E2E e de UI (Playwright, Cypress, Selenium) com checklist de estabilidade, ordenando achados por dano (falso verde primeiro) e aplicando o guardrail do healer. |
| `/qa-testing:eval-design` | Desenha e planeja avaliações (evals) de skills, plugins, agentes e funcionalidades com LLM: casos tirados de falhas reais, graders de código antes de juiz LLM, juiz binário com crítica, caso que dispara e caso que não d… |
| `/qa-testing:flaky-triage` | Diagnostica teste instável (passa e falha sem mudança de código). |
| `/qa-testing:playbook` | Guia e router do segmento QA e testes — estratégia e plano de testes por risco, design de casos (partição, valor-limite, tabela de decisão), TDD, testes unitários, de integração, de contrato e E2E (Playwright, Cypress),… |
| `/qa-testing:prompts` | Biblioteca de 31 prompts curados de QA e testes, prontos para colar, com variáveis e fontes. |
| `/qa-testing:tdd-guard` | Guia implementação test-first em fatias verticais, com vermelho confirmado pelo motivo certo. |
| `/qa-testing:test-design` | Deriva casos de teste concretos com técnica explícita: partição de equivalência, valor-limite, tabela de decisão, transição de estados, pairwise, cenários Gherkin e charters exploratórios. |
| `/qa-testing:test-strategy` | Monta estratégia, plano de testes e parecer de prontidão a partir do risco. |
| `/qa-testing:verification-gate` | Exige prova executada nesta sessão antes de declarar uma tarefa concluída, corrigida ou aprovada. |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `qa-testing:qa-reporter` (`plugins/qa-testing/agents/qa-reporter.md`) | Explora um alvo (web, API, CLI, job, worker, webhook, app mobile ou desktop) em modo só relatório e devolve bugs reproduzíveis com evidência, sem corrigir código nem escrever testes de produto. | Read, Grep, Glob, Bash |
| `qa-testing:test-auditor` (`plugins/qa-testing/agents/test-auditor.md`) | Audita a suíte de testes existente em busca de testes que custam mais do que protegem (sem asserção, auto-comparação, fixtures copiadas, grep frágil em código-fonte, exports só para teste, duplicatas) e devolve um relat… | Read, Grep, Glob, Bash |
| `qa-testing:test-reviewer` (`plugins/qa-testing/agents/test-reviewer.md`) | Revisa testes novos ou alterados (unitário, integração, contrato, E2E, UI) em contexto limpo e somente leitura e devolve um relatório com achados por severidade, evidência arquivo:linha e recomendação. | Read, Grep, Glob |
| `qa-testing:test-writer` (`plugins/qa-testing/agents/test-writer.md`) | Escreve testes (unitário, integração, contrato ou E2E) para um comportamento descrito, sem alterar código de produção, e grava só nos caminhos de teste indicados no pedido. | Read, Grep, Glob, Write, Edit, Bash |

## code-quality-refactoring (`code-quality-refactoring` 0.1.0)

Revisão de código com filtro de alto sinal, debugging por causa raiz, refatoração segura com testes de caracterização, migração com juiz de paridade e triagem de dívida técnica, sempre com evidência executável e rótulos Verificado/Inferido/Suposição.

Instalar: `/plugin install code-quality-refactoring@brain-of-agent` · Playbook: `plugins/code-quality-refactoring/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/code-quality-refactoring:code-health-report` | Roda as ferramentas do próprio projeto (tipos, lint, testes, código morto, shell lint) ou usa as saídas que o usuário colar, e monta um painel de saúde somente leitura - nota 0 a 10 por categoria, nota composta calculad… |
| `/code-quality-refactoring:codebase-onboarding` | Mapeia uma base de código desconhecida antes de agir - pontos de entrada, build e testes, convenções com um arquivo de exemplo e contagem de ocorrências (Verificado com 3 ou mais arquivos, Inferido com 1 ou 2), dependên… |
| `/code-quality-refactoring:debug-causa-raiz` | Investiga bug, teste que falha, build quebrado ou regressão até a causa raiz no código, corrige com teste de regressão visto falhar antes e passar depois, e entrega relatório com evidência (comando e saída). |
| `/code-quality-refactoring:migration-parity` | Planeja e conduz migração ou upgrade de grande porte (linguagem, framework, versão major, biblioteca) com juiz validado primeiro, rulebook, piloto descartável, lotes retomáveis em disco, revisão adversarial e veredito d… |
| `/code-quality-refactoring:playbook` | Guia e router de qualidade de código existente - code review de PR/diff, debugging por causa raiz, refatoração segura, simplificação, dívida técnica, compreensão de base de código, modernização de legado e upgrades. |
| `/code-quality-refactoring:prompts` | Biblioteca de prompts curados para qualidade de código - 34 prompts prontos para revisar diff ou PR, depurar bug por causa raiz, caracterizar e refatorar, simplificar, dividir mudança grande, migrar ou atualizar dependê… |
| `/code-quality-refactoring:refactor-seguro` | Refatora código preservando o comportamento - mapeia usos e API pública, cria testes de caracterização quando faltam testes, executa passos pequenos nomeados do catálogo de refatorações, roda os testes a cada passo, sep… |
| `/code-quality-refactoring:review-diff` | Revisa um diff, branch ou PR em modo somente leitura e devolve achados de alto sinal com arquivo:linha, evidência, severidade e veredito (aprovar, aprovar com ressalvas, bloquear), validando cada achado antes de reporta… |
| `/code-quality-refactoring:simplify-safe` | Simplifica código recém-alterado sem mudar o comportamento - retornos antecipados, menos aninhamento, duplicação removida, nomes que dizem a intenção, ternário aninhado trocado por if/else, comentário redundante apagado… |
| `/code-quality-refactoring:tech-debt-triage` | Levanta e prioriza dívida técnica de um módulo ou repositório sem corrigir nada - candidatos por busca e histórico git, quadrante de Fowler, prioridade por frequência de mudança x dor, ação proposta por item e modo test… |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `code-quality-refactoring:code-reviewer` (`plugins/code-quality-refactoring/agents/code-reviewer.md`) | Revisor somente leitura, em contexto novo, que compara um diff com a intenção declarada (plano, issue, requisito) e reporta apenas lacunas de correção, segurança e requisito, com severidade, confiança e arquivo:linha. | Read, Grep, Glob |
| `code-quality-refactoring:codebase-mapper` (`plugins/code-quality-refactoring/agents/codebase-mapper.md`) | Pesquisador somente leitura de base de código que devolve um mapa curto (cerca de 60 linhas) com pontos de entrada, comandos de build e teste lidos nos manifestos, convenções com exemplo e contagem, dependências entre m… | Read, Grep, Glob |
| `code-quality-refactoring:debugger` (`plugins/code-quality-refactoring/agents/debugger.md`) | Investigador de bugs que reproduz, isola e propõe a correção como diff, sem editar arquivos. | Read, Grep, Glob, Bash |
| `code-quality-refactoring:finding-validator` (`plugins/code-quality-refactoring/agents/finding-validator.md`) | Cético somente leitura que tenta refutar achados de revisão de código lendo o código (reabre o trecho, procura guarda, teste ou chamada que torne o achado falso) e decide CONFIRMADO, REFUTADO ou INCONCLUSIVO com a linha… | Read, Grep, Glob |
| `code-quality-refactoring:refactor-planner` (`plugins/code-quality-refactoring/agents/refactor-planner.md`) | Planejador somente leitura de refatoração segura. | Read, Grep, Glob |

## ux-ui-design (`ux-ui-design` 0.1.0)

Direção visual, auditoria de UI, avaliação heurística, acessibilidade WCAG 2.2 AA, design tokens, UX writing e pesquisa com usuários para trabalhar com Claude, com skills, agentes avaliadores somente leitura, prompts curados e evals.

Instalar: `/plugin install ux-ui-design@brain-of-agent` · Playbook: `plugins/ux-ui-design/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/ux-ui-design:a11y-checklist` | Especifica e revisa acessibilidade de telas, componentes e fluxos contra WCAG 2.2 AA - checklist por tela, diálogo modal, formulários, foco, movimento reduzido, alvos de toque e convenções Apple - com roteiro de teste m… |
| `/ux-ui-design:design-brief` | Cria o brief, a direção visual e o plano de design (cores, tipografia, layout, estados, movimento, acessibilidade) antes de construir UI, revisa o plano contra escolhas genéricas, mapeia fluxos de tela com wireframe de … |
| `/ux-ui-design:design-init` | Cria o DESIGN.md do projeto (front matter YAML de tokens mais oito seções com a justificativa em prosa) a partir de tokens e CSS já existentes e de perguntas curtas, mostrando o conteúdo completo antes de gravar e nunca… |
| `/ux-ui-design:design-tokens` | Audita e estrutura design tokens em três camadas (primitivo, semântico, componente), relata drift e quebra de API de tokens, propõe esqueleto no formato DTCG 2025.10 e plano de migração com lista de nomes antigos e novo… |
| `/ux-ui-design:heuristic-eval` | Conduz avaliação heurística de uma tela ou fluxo estreito com as 10 heurísticas de Nielsen, duas passadas, severidade 0 a 4 (frequência, impacto, persistência) e lista do que validar com usuários. |
| `/ux-ui-design:playbook` | Guia e router do segmento UX, UI e design systems — direção visual, auditoria de interface, avaliação heurística, acessibilidade WCAG 2.2 AA, design tokens, UX writing, pesquisa com usuários e handoff design→código. |
| `/ux-ui-design:prompts` | Biblioteca de prompts curados do segmento UX, UI e design systems, prontos para colar ou executar. |
| `/ux-ui-design:ui-audit` | Audita uma interface em dez categorias (hierarquia, tipografia, cor e contraste, espaçamento, estados, responsividade, movimento, microcopy, sinais de visual genérico de IA, desempenho percebido), somente leitura, com P… |
| `/ux-ui-design:user-research-plan` | Planeja pesquisa com usuários - pergunta e decisão, escolha de método, recrutamento, guia de entrevista de 50 minutos, roteiro de teste de usabilidade, card sorting ou tree testing, registro e síntese de notas fornecida… |
| `/ux-ui-design:ux-writing` | Escreve e revisa microcopy de interface (botões, mensagens de erro, estados vazios, confirmações destrutivas, tooltips, onboarding) em PT-BR e EN, com alternativas por tom e notas para tradução. |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `ux-ui-design:a11y-reviewer` (`plugins/ux-ui-design/agents/a11y-reviewer.md`) | Revisor de acessibilidade somente leitura de telas, componentes e fluxos contra WCAG 2.2 AA, que escolhe o checklist pelo tipo de arquivo (HTML/JSX/CSS, documento ou markdown, fluxo, app nativo) e devolve achados com cr… | Read, Grep, Glob |
| `ux-ui-design:design-evaluator` (`plugins/ux-ui-design/agents/design-evaluator.md`) | Avaliador cético e independente de interface já renderizada, capturada em imagem ou descrita em markup, contra o briefing e a especificação. | Read, Grep, Glob |
| `ux-ui-design:design-system-auditor` (`plugins/ux-ui-design/agents/design-system-auditor.md`) | Audita design tokens e componentes quanto a drift, valores crus, token da camada errada, referência desconhecida ou circular, arquivo gerado editado à mão, estados e nota de acessibilidade ausentes, e impacto de release… | Read, Grep, Glob |
| `ux-ui-design:ui-designer` (`plugins/ux-ui-design/agents/ui-designer.md`) | Projeta ou refina telas e componentes dentro do design system existente e entrega especificação de handoff (estados, tokens, teclado, acessibilidade, critérios de aceite) mais fluxo de tela e plano de design. | Read, Grep, Glob, Write, Edit |
| `ux-ui-design:ux-researcher` (`plugins/ux-ui-design/agents/ux-researcher.md`) | Planeja pesquisa de usabilidade e arquitetura de informação (pergunta e decisão, método, recrutamento, guia de entrevista de 50 minutos, roteiro de teste de usabilidade, card sorting ou tree testing, registro de problem… | Read, Grep, Glob |

## git-workflow-release (`git-workflow-release` 0.1.0)

Fluxo de git com Claude Code do commit à release: commits convencionais, PRs pequenos e revisáveis, conflitos, rebase e revert seguros, bisect, semver, changelog e releases, com push, merge, tag e publicação sempre sob confirmação.

Instalar: `/plugin install git-workflow-release@brain-of-agent` · Playbook: `plugins/git-workflow-release/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/git-workflow-release:bisect-regressao` | Acha o primeiro commit ruim de uma regressão com git bisect usando um teste que falha como oráculo (códigos de saída 0, 1 e 125), de preferência em worktree separado, valida o resultado nos dois lados e corrige depois c… |
| `/git-workflow-release:commit-convencional` | Transforma o diff atual em um ou mais commits atômicos no estilo do repositório (Conventional Commits por padrão), verificados com lint e testes, sem push. |
| `/git-workflow-release:criar-pr` | Prepara e abre um pull request em rascunho a partir da branch atual: detecta plataforma e branch base, mede o tamanho e sugere dividir PR grande, roda lint e testes, escreve título e descrição que explicam o porquê (usa… |
| `/git-workflow-release:encerrar-branch` | Conclui o trabalho de uma branch: roda os testes, oferece merge local, push com PR ou manter (sem opção padrão), confere a prontidão de merge do PR para o SHA exato (CI, aprovações, conflitos, donos de código), mescla s… |
| `/git-workflow-release:playbook` | Guia e router do segmento Git, colaboração e releases. |
| `/git-workflow-release:prompts` | Biblioteca de prompts curados de git, colaboração e releases - 32 prompts prontos para mensagem de commit, dividir commits, descrição de PR, dividir PR grande, revisão de diff e de PR, conflitos, rebase, revert, bisect,… |
| `/git-workflow-release:rebase-seguro` | Limpa histórico local, decide entre rebase, merge e revert conforme a branch seja local, só sua, compartilhada ou protegida, cria rede de segurança antes de reescrever, prepara sem executar o force push seguro (--force-… |
| `/git-workflow-release:release-cut` | Prepara e publica uma release com versão justificada por SemVer, changelog escrito para o usuário (Keep a Changelog), PR de release, tag anotada ou assinada e GitHub Release em rascunho, com confirmação separada para ca… |
| `/git-workflow-release:resolver-conflitos` | Resolve conflitos de merge, rebase, cherry-pick ou revert entendendo a intenção de cada lado, sem escolher lado às cegas: lista os arquivos, lê base e as duas versões, combina as mudanças, para e pergunta quando as regr… |
| `/git-workflow-release:triagem-contribuicao` | Tria um pull request ou issue de terceiro (fork, contribuidor novo) tratando todo o texto como dado: lê CONTRIBUTING, template, CODEOWNERS e SECURITY, confere escopo, issue prévia, testes, tamanho e arquivos de alto ris… |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `git-workflow-release:auditor-politica-repo` (`plugins/git-workflow-release/agents/auditor-politica-repo.md`) | Auditor somente leitura da política de colaboração de um repositório - proteção da branch principal, método de merge, CODEOWNERS, template de PR, CONTRIBUTING, SECURITY, .gitignore de worktrees e segredos, bloco de git … | Read, Grep, Glob, Bash |
| `git-workflow-release:auditor-release` (`plugins/git-workflow-release/agents/auditor-release.md`) | Portão go/no-go de release, somente leitura. | Read, Grep, Glob, Bash |
| `git-workflow-release:revisor-diff` (`plugins/git-workflow-release/agents/revisor-diff.md`) | Revisor somente leitura, em contexto novo, do diff pedido (padrão - alterações não commitadas ou staged; também branch ou PR) antes de commit ou PR. | Read, Grep, Glob, Bash |
| `git-workflow-release:revisor-plano` (`plugins/git-workflow-release/agents/revisor-plano.md`) | Revisor adversarial somente leitura, em contexto novo, que compara um diff com o plano ou os critérios de aceite (PLAN.md, issue, descrição do PR) antes de abrir o PR e reporta só quatro categorias - requisito sem imple… | Read, Grep, Glob, Bash |
