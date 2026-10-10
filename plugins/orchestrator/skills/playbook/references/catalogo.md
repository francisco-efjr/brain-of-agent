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
| `data-engineering` | Engenharia de dados e analytics para o Claude Code: pipelines ETL/ELT, dbt, Airflow e Dagster, Spark e streaming, SQL analítico e custo em warehouses, contrato… | airflow-dag-workflow, data-contracts-quality, dbt-model-workflow, gated-pipeline-migration, pipeline-acceptance, playbook, prompts, spark-streaming-review, sql-review, text-to-sql-safe | analytics-reviewer, data-pipeline-architect, data-pipeline-reviewer, eval-judge, pipeline-debugger | DATAENG-COMPLETO |
| `data-science-ml` | Playbook de ciência de dados e machine learning para Claude Code: EDA sem vazamento, validação e métricas, treino e tuning reprodutíveis, séries temporais, A/B… | ds-eda, ds-inference-review, ds-leakage-audit, ds-llm-eval, ds-mlops-promotion, ds-model-evaluation, ds-time-series-backtest, ds-train-debug, playbook, prompts | ds-eval-auditor, ds-experiment-reviewer, ds-inference-reviewer, ds-leakage-auditor, ds-model-promotion-reviewer | DATASCIENCE-COMPLETO |
| `llm-ai-agents` | Playbook, skills de tarefa, subagentes somente leitura e biblioteca de prompts para projetar, revisar e testar aplicações LLM e agentes: engenharia de prompt e… | agent-architecture, agent-security-review, eval-design, instruction-authoring, llm-api-client-review, llm-decision-gates, llm-prompt-review, playbook, prompts, tool-design-review | agent-architect, agent-security-reviewer, eval-designer, prompt-reviewer, rag-pipeline-reviewer | IA-COMPLETO |
| `devops-cloud-infra` | Escreva, revise, planeje e diagnostique infraestrutura (Terraform/OpenTofu/Pulumi, Docker, Kubernetes/Helm, GitOps, GitHub Actions, segredos, canary/blue-green… | cloud-review, deploy-infra, gha-hardening-review, helm-gitops-review, iac-review, infra-troubleshoot, playbook, progressive-delivery, prompts, secrets-review | infra-reviewer, k8s-workload-auditor, pipeline-security-auditor, rollout-planner | DEVOPS-COMPLETO |
| `sre-observability` | SLI/SLO e error budget, alertas por burn rate, telemetria (OpenTelemetry, Prometheus), triagem de incidentes somente leitura, postmortem blameless, runbooks, c… | alert-review, incident-triage, performance-engineering, playbook, postmortem, prompts, release-health, root-cause-investigation, runbook, slo-design, telemetry-review | incident-support, perf-analyst, postmortem-scribe, reliability-reviewer | SRE-COMPLETO |
| `security-appsec` | Revisão de segurança de diffs e PRs, modelagem de ameaças (STRIDE), autorização por objeto e tenant, segredos, supply chain e triagem de risco de agentes, MCP … | access-control-review, agent-risk-triage, harden-claude-code, playbook, prompts, propose-patch, secrets-supply-chain-review, security-review-diff, threat-model, verify-finding | agent-config-auditor, finding-verifier, patch-reviewer, security-reviewer, threat-modeler | SEGURANCA-COMPLETO |
| `qa-testing` | QA e testes para o Claude Code: estratégia por risco, design de casos, TDD com vermelho confirmado, revisão de testes e E2E, triagem de testes flaky, bug repor… | bug-report, e2e-review, eval-design, flaky-triage, playbook, prompts, tdd-guard, test-design, test-strategy, verification-gate | qa-reporter, test-auditor, test-reviewer, test-writer | QA-COMPLETO |
| `code-quality-refactoring` | Revisão de código com filtro de alto sinal, debugging por causa raiz, refatoração segura com testes de caracterização, migração com juiz de paridade e triagem … | code-health-report, codebase-onboarding, debug-causa-raiz, migration-parity, playbook, prompts, refactor-seguro, review-diff, simplify-safe, tech-debt-triage | code-reviewer, codebase-mapper, debugger, finding-validator, refactor-planner | QUALIDADE-COMPLETO |
| `ux-ui-design` | Direção visual, auditoria de UI, avaliação heurística, acessibilidade WCAG 2.2 AA, design tokens, UX writing e pesquisa com usuários para trabalhar com Claude,… | a11y-checklist, design-brief, design-init, design-tokens, heuristic-eval, playbook, prompts, ui-audit, user-research-plan, ux-writing | a11y-reviewer, design-evaluator, design-system-auditor, ui-designer, ux-researcher | UXUI-COMPLETO |
| `technical-writing-docs` | Documentação técnica com Claude Code: README, tutoriais e guias (Diátaxis), ADRs, runbooks, changelog, docs de API (OpenAPI), docstrings, diagramas Mermaid, do… | auditar-claude-md, diagramar-arquitetura, documentar-codigo, escrever-adr, escrever-changelog-release, escrever-guia-diataxis, escrever-readme, escrever-runbook, playbook, prompts | auditor-de-docs, revisor-de-instrucoes, revisor-de-leitor, technical-writer | DOCS-COMPLETO |
| `game-development` | Playbook, skills, agentes e prompts para desenvolver, revisar, otimizar e testar jogos em Godot/GDScript, Unity/C# e Unreal/C++, com verificação por execução (… | game-netcode-review, game-perf-audit, game-qa-plan, game-verify-by-running, gdd-review, godot-gdscript, playbook, prompts, unity-csharp, unreal-cpp | game-engine-specialist, game-evaluator, gameplay-programmer, gameplay-reviewer, gdd-reviewer | GAMEDEV-COMPLETO |
| `systems-embedded-iot` | Revisão, depuração e testes de firmware (C/C++, Rust no_std, FreeRTOS, Zephyr, ESP32/STM32) com portão humano para gravar em hardware, datasheet primeiro e che… | bus-protocol-review, datasheet-first, firmware-review, firmware-root-cause, firmware-test-host, hw-bench-loop, ota-security-review, playbook, prompts, rtos-concurrency-review | embedded-architect, firmware-debugger, firmware-reviewer, firmware-test-engineer, iot-security-auditor | EMBARCADOS-COMPLETO |
| `cli-desktop-tooling` | Playbook, skills, agentes e prompts para projetar, revisar, empacotar e distribuir CLIs, TUIs e apps desktop (Electron, Tauri, WPF, WinUI, MAUI, Qt), com desig… | cli-design-review, desktop-release-checklist, desktop-security-audit, desktop-stack-decision, dotnet-desktop-review, dx-audit, playbook, prompts, shell-script-review, tui-review | cli-ux-reviewer, desktop-security-auditor, diff-gap-reviewer, release-readiness-auditor, script-reviewer | TOOLING-COMPLETO |
| `blockchain-web3` | Revisão de segurança de smart contracts (Solidity; Anchor com cobertura parcial), testes de invariantes e fuzz com Foundry, checklists de ERC-20/721/1155/4626,… | audit-contracts, contract-security-review, defi-oracle-l2-review, exploit-poc, foundry-testing, playbook, prompts, solana-anchor-review, token-standards-review, wallet-signing-review | defi-protocol-analyst, finding-refuter, invariant-test-engineer, solidity-security-reviewer, web3-agent-safety-auditor | WEB3-COMPLETO |
| `automation-integrations` | Playbook, skills, agentes e prompts para automação de workflows, webhooks idempotentes, integrações entre APIs, servidores MCP, hooks de guardrail, jobs agenda… | assessing-automation-risk, authoring-plugin-skills, building-mcp-servers, designing-workflow-automations, playbook, prompts, responsible-scraping, reviewing-webhook-receivers, scheduling-headless-jobs, writing-hook-guardrails | automation-architect, integration-reviewer, mcp-security-reviewer, plugin-validator, third-party-auditor | AUTOMACAO-COMPLETO |
| `git-workflow-release` | Fluxo de git com Claude Code do commit à release: commits convencionais, PRs pequenos e revisáveis, conflitos, rebase e revert seguros, bisect, semver, changel… | bisect-regressao, commit-convencional, criar-pr, encerrar-branch, playbook, prompts, rebase-seguro, release-cut, resolver-conflitos, triagem-contribuicao | auditor-politica-repo, auditor-release, revisor-diff, revisor-plano | RELEASE-COMPLETO |
| `design-engineering-kit` | Complemento opcional do ux-ui-design para designer-engenheiro: do link do Figma à UI implementada, verificada no navegador (Playwright MCP) e polida, com 17 sk… | animate, animate-expo, animation-vocabulary, apple-design, break-ui, design-taste-frontend, emil-design-eng, find-animation-opportunities, high-end-visual-design, improve-animations, industrial-brutalist-ui, minimalist-ui, mobile-native, pick-ui-library, playbook, prompts, prototype, redesign-existing-projects, review-animations | motion-polish-reviewer, ui-verifier | DESIGNENG-COMPLETO |

**Em construção (ainda não publicados):** `saas-multitenant`, `fintech-payments`, `ecommerce-marketplace`. Para essas demandas, use o plugin mais próximo e declare a lacuna.

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

## data-engineering (`data-engineering` 0.1.0)

Engenharia de dados e analytics para o Claude Code: pipelines ETL/ELT, dbt, Airflow e Dagster, Spark e streaming, SQL analítico e custo em warehouses, contratos e qualidade de dados, linhagem e text-to-SQL seguro, com verificação por saída real, reconciliação de contagens, agentes somente leitura e o modo DATAENG-COMPLETO.

Instalar: `/plugin install data-engineering@brain-of-agent` · Playbook: `plugins/data-engineering/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/data-engineering:airflow-dag-workflow` | Revisa, cria, testa e depura DAGs do Airflow (e orienta assets do Dagster e princípios para Prefect) com checklist de 12 perguntas (idempotência, intervalo da execução, now(), código no topo do arquivo, XCom, sensores, … |
| `/data-engineering:data-contracts-quality` | Define contratos de dados (Open Data Contract Standard 3.2.0), regras de qualidade com ação fail/drop/warn e contagem de violações, política block/warn/log para agentes, convenção de linhagem (OpenLineage) e checklist d… |
| `/data-engineering:dbt-model-workflow` | Cria ou altera modelos dbt (staging, intermediate, marts), YAML, testes e documentação: lê o projeto e os consumidores antes de escrever, segue as convenções vizinhas, testa por tipo de coluna e verifica em target de de… |
| `/data-engineering:gated-pipeline-migration` | Migração ou upgrade de pipeline com fases e gates (dbt, Airflow, Spark, troca de plataforma): preflight de git, lista de mudanças a partir de fonte verificável, detecção sem editar, correções determinísticas, julgamento… |
| `/data-engineering:pipeline-acceptance` | Aceitação de pipeline ou modelo gerado por agente antes de mergear ou promover: reconcilia contagem origem vs destino e campos vs colunas, roda a carga duas vezes para provar idempotência, confere chaves nos dados carre… |
| `/data-engineering:playbook` | Guia e router do segmento Engenharia de dados e analytics. |
| `/data-engineering:prompts` | Biblioteca de prompts curados de engenharia de dados e analytics (dbt, Airflow, Dagster, Spark, streaming, SQL, BigQuery, Delta, contratos e qualidade, evals). |
| `/data-engineering:spark-streaming-review` | Revisa jobs Spark/PySpark, garantias de entrega em streaming (Kafka, Flink, Structured Streaming) e manutenção de tabelas Delta: lê o plano antes de ajustar configuração, AQE, skew, broadcast, UDF, escrita idempotente, … |
| `/data-engineering:sql-review` | Revisa e otimiza SQL analítico sem mudar o resultado: checklist de custo para BigQuery (bytes lidos, partição, sharding, tipos de junção, auto-junção, DML) e checklist de equivalência semântica (NULL, duplicidade, tipo,… |
| `/data-engineering:text-to-sql-safe` | Gera SQL de leitura a partir de perguntas em linguagem natural usando o schema real e a definição governada da métrica, com regras de segurança e custo (só SELECT, sem SELECT *, LIMIT, filtro de partição, sem PII por pa… |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `data-engineering:analytics-reviewer` (`plugins/data-engineering/agents/analytics-reviewer.md`) | Revisor cético e somente leitura de SQL analítico, métricas, modelos de mart e consultas que alimentam relatórios ou dashboards, antes de chegarem a stakeholders. | Read, Grep, Glob |
| `data-engineering:data-pipeline-architect` (`plugins/data-engineering/agents/data-pipeline-architect.md`) | Desenha pipelines de dados novos e mudanças estruturais antes de qualquer implementação, em modo somente leitura - batch ou streaming, workflow fixo ou agente, camadas dbt e grão, modelagem dimensional (fato e dimensões… | Read, Glob, Grep |
| `data-engineering:data-pipeline-reviewer` (`plugins/data-engineering/agents/data-pipeline-reviewer.md`) | Revisor cético e somente leitura de pipelines de dados (modelos e testes dbt, DAGs do Airflow, assets do Dagster, jobs Spark/PySpark, streaming Kafka/Flink, SQL de carga e merge, tabelas Delta, contratos e regras de qua… | Read, Glob, Grep |
| `data-engineering:eval-judge` (`plugins/data-engineering/agents/eval-judge.md`) | Juiz binário de um único modo de falha em saídas de agentes de dados (respostas de skills, prompts, revisões, SQL gerado). | Read |
| `data-engineering:pipeline-debugger` (`plugins/data-engineering/agents/pipeline-debugger.md`) | Investigador somente leitura da causa raiz de falha ou resultado errado em pipelines (DAG do Airflow, asset do Dagster, job Spark, modelo dbt, carga, streaming), a partir de logs, SQL compilado, diffs e versões fornecid… | Read, Glob, Grep |

## data-science-ml (`data-science-ml` 0.1.0)

Playbook de ciência de dados e machine learning para Claude Code: EDA sem vazamento, validação e métricas, treino e tuning reprodutíveis, séries temporais, A/B e inferência causal, avaliação de componentes LLM e promoção de modelos com registro, serving e drift.

Instalar: `/plugin install data-science-ml@brain-of-agent` · Playbook: `plugins/data-science-ml/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/data-science-ml:ds-eda` | Conduz análise exploratória de um dataset antes de modelar, usando só o conjunto de treino - forma e tipos, ausentes e padrão de ausência, alvo e balanceamento, relação com o alvo, cardinalidade, outliers e suspeitas de… |
| `/data-science-ml:ds-inference-review` | Revisa inferência estatística e causal - experimentos A/B (SRM, guardrails, métrica primária, poder e MDE, multiplicidade, CUPED), relatórios com tamanho de efeito e intervalo, escolha de teste (t, Mann-Whitney, qui-qua… |
| `/data-science-ml:ds-leakage-audit` | Audita vazamento de dados (data leakage) e o desenho de validação de um projeto de ML - ordem do split e do pré-processamento, Pipeline, grupos, duplicatas, tempo e disponibilidade de cada feature no momento da decisão. |
| `/data-science-ml:ds-llm-eval` | Projeta a avaliação de um componente LLM dentro de um projeto de dados (classificação, extração, resumo) - critérios de sucesso mensuráveis, conjunto de casos de falhas reais, graders de código antes de juiz, validação … |
| `/data-science-ml:ds-mlops-promotion` | Prepara e revisa a promoção de um modelo para produção - registro de runs e modelos (MLflow), checklist de serving (incluindo o risco de pickle e joblib), plano de monitoramento de drift, prontidão de ML (training-servi… |
| `/data-science-ml:ds-model-evaluation` | Define métrica, baseline e desenho de validação para um problema de ML supervisionado, trata classes desbalanceadas (métrica, pesos, reamostragem dentro do fold, limiar), calibração e feature engineering (encoders por c… |
| `/data-science-ml:ds-time-series-backtest` | Projeta e revisa o backtest de modelos de séries temporais e previsão - origem rolante, horizonte da decisão, covariáveis conhecidas na origem, dados point-in-time, baseline sazonal-naive, MASE, erro por horizonte e cob… |
| `/data-science-ml:ds-train-debug` | Depura e revisa treino de modelos (PyTorch, scikit-learn, LightGBM, XGBoost) - loss que não cai, NaN, treino bom e validação ruim, métrica suspeita, reprodutibilidade (seeds, determinismo, checkpoint) - e planeja tuning… |
| `/data-science-ml:playbook` | Guia e router do segmento Ciência de dados e machine learning: EDA, vazamento de dados e validação, métricas, treino (scikit-learn, PyTorch, gradient boosting), tuning, séries temporais, experimentos A/B, inferência cau… |
| `/data-science-ml:prompts` | Biblioteca de prompts curados do segmento Ciência de dados e machine learning (EDA, vazamento e validação, métricas, treino com scikit-learn, PyTorch e gradient boosting, tuning, séries temporais, A/B, inferência causal… |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `data-science-ml:ds-eval-auditor` (`plugins/data-science-ml/agents/ds-eval-auditor.md`) | Revisor somente leitura do desenho de avaliação de um componente LLM dentro de um projeto de dados (classificação, extração, resumo), em contexto limpo. | Read, Grep, Glob |
| `data-science-ml:ds-experiment-reviewer` (`plugins/data-science-ml/agents/ds-experiment-reviewer.md`) | Revisor independente e somente leitura de experimentos de ML e de avaliação de componentes LLM, em contexto limpo. | Read, Grep, Glob |
| `data-science-ml:ds-inference-reviewer` (`plugins/data-science-ml/agents/ds-inference-reviewer.md`) | Revisor somente leitura de inferência estatística e causal, em contexto limpo. | Read, Grep, Glob |
| `data-science-ml:ds-leakage-auditor` (`plugins/data-science-ml/agents/ds-leakage-auditor.md`) | Auditor somente leitura de vazamento de dados e do desenho de validação de ML, em contexto limpo. | Read, Grep, Glob |
| `data-science-ml:ds-model-promotion-reviewer` (`plugins/data-science-ml/agents/ds-model-promotion-reviewer.md`) | Revisor independente e somente leitura que emite uma decisão (APPROVE, APPROVE WITH WARNINGS ou BLOCK) antes de promover um modelo de ML ou aceitar um pipeline (contratos de dados, vazamento, reprodutibilidade, avaliaçã… | Read, Grep, Glob |

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

## sre-observability (`sre-observability` 0.1.0)

SLI/SLO e error budget, alertas por burn rate, telemetria (OpenTelemetry, Prometheus), triagem de incidentes somente leitura, postmortem blameless, runbooks, canário, testes de carga e performance, com agentes que investigam sem tocar em produção.

Instalar: `/plugin install sre-observability@brain-of-agent` · Playbook: `plugins/sre-observability/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/sre-observability:alert-review` | Revisa regras de alerta, rotas e painéis: separa alerta de sintoma (SLO) de alerta de causa (recurso), converte para burn rate multijanela mostrando a conta, define página x ticket x dashboard, valida PromQL e propõe te… |
| `/sre-observability:incident-triage` | Apoia o Incident Commander durante um incidente de produção em modo somente leitura: sintoma em termos de usuário, severidade sugerida, mudanças recentes, no máximo 3 hipóteses refutáveis com a consulta que as refuta, e… |
| `/sre-observability:performance-engineering` | Planeja e interpreta performance sem executar carga: plano e script de teste de carga (k6, Locust) com thresholds derivados do SLO, leitura de resultados, Core Web Vitals por dado de campo, leitura de flame graph e gate… |
| `/sre-observability:playbook` | Guia e router do segmento SRE, observabilidade e performance - SLI/SLO e error budget, alertas por burn rate, métricas/logs/traces (OpenTelemetry, Prometheus, Grafana), resposta a incidentes, postmortem blameless, runbo… |
| `/sre-observability:postmortem` | Redige ou revisa um postmortem blameless a partir de evidências: confirma o gatilho, monta a linha do tempo com fonte por evento, quantifica o impacto com origem, propõe causas contribuintes de sistema e processo como c… |
| `/sre-observability:prompts` | Biblioteca de 36 prompts curados de SRE, observabilidade e performance, prontos para colar, com variáveis, motivo e fontes. |
| `/sre-observability:release-health` | Conduz, só por comando explícito, a verificação somente leitura de um canário ou do pós-deploy: critérios de rollback definidos antes, poucas métricas (de preferência SLIs), canário comparado com controle concorrente, b… |
| `/sre-observability:root-cause-investigation` | Investiga a causa raiz de um sintoma observado em sistema em execução (regressão de latência ou erro depois de deploy, erro intermitente em produção, p95 que piorou após mudança) antes de propor correção: reproduz, comp… |
| `/sre-observability:runbook` | Escreve ou revisa um runbook por assinatura de falha ligado a um alerta: impacto, diagnóstico somente leitura com comando exato e saída esperada, mitigações como opções que exigem decisão humana e aprovador, escalonamen… |
| `/sre-observability:slo-design` | Conduz a definição do primeiro SLO de um serviço (ou a revisão de um existente) e redige a política de error budget: jornadas críticas, até 5 tipos de SLI em linguagem de usuário, linha de base por janela fixa, metas po… |
| `/sre-observability:telemetry-review` | Revisa instrumentação e telemetria em seis modos: métricas (nomes, unidades, rótulos, cardinalidade, contador x medidor), sinais e pipelines do OpenTelemetry Collector (oficial x Suposição), logging seguro com teste de … |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `sre-observability:incident-support` (`plugins/sre-observability/agents/incident-support.md`) | Apoia o Incident Commander em modo somente leitura durante um incidente de produção em andamento - organiza o sintoma em termos de usuário, mudanças recentes na janela, até 3 hipóteses refutáveis, evidências com procedê… | Read, Grep, Glob |
| `sre-observability:perf-analyst` (`plugins/sre-observability/agents/perf-analyst.md`) | Interpreta resultados de carga, benchmark e perfil que o usuário já executou (resumo do k6, saídas de Locust/JMeter/Gatling, Lighthouse, dados de campo de Web Vitals, flame graph descrito, métricas de APM) e separa medi… | Read, Grep, Glob |
| `sre-observability:postmortem-scribe` (`plugins/sre-observability/agents/postmortem-scribe.md`) | Monta a linha do tempo e o rascunho de postmortem blameless de um incidente já resolvido, apenas a partir das evidências fornecidas (notas, mensagens, alertas, deploys, gráficos descritos, tickets). | Read, Grep, Glob |
| `sre-observability:reliability-reviewer` (`plugins/sre-observability/agents/reliability-reviewer.md`) | Revisor independente, cético e somente leitura de mudanças de confiabilidade em contexto limpo - timeouts, retries, health checks, regras de alerta e burn rate, SLO, instrumentação (rótulos, cardinalidade, logs com dado… | Read, Grep, Glob |

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

## technical-writing-docs (`technical-writing-docs` 0.1.0)

Documentação técnica com Claude Code: README, tutoriais e guias (Diátaxis), ADRs, runbooks, changelog, docs de API (OpenAPI), docstrings, diagramas Mermaid, docs-as-code e arquivos para agentes (CLAUDE.md, AGENTS.md, skills), verificando o que escreve e sem afirmar execução que não houve.

Instalar: `/plugin install technical-writing-docs@brain-of-agent` · Playbook: `plugins/technical-writing-docs/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/technical-writing-docs:auditar-claude-md` | Audita e enxuga arquivos de instrução para agentes (CLAUDE.md, CLAUDE.local.md, AGENTS.md, .claude/rules, arquivos de subpacotes) com rubrica de 100 pontos, relatório antes de qualquer edição, diffs mínimos com motivo, … |
| `/technical-writing-docs:diagramar-arquitetura` | Produz diagramas de arquitetura e fluxo como código (Mermaid, níveis do C4) para documentação, um nível por diagrama, com texto explicativo e teste de renderização no destino antes de prometer que funciona; cai para flo… |
| `/technical-writing-docs:documentar-codigo` | Escreve docstrings e comentários de documentação por linguagem (Python, TypeScript/JavaScript, Rust, Java) com exemplos verificáveis, e documenta APIs a partir de um contrato (OpenAPI, protobuf) ou anotações com fonte ú… |
| `/technical-writing-docs:escrever-adr` | Registra por escrito uma decisão de arquitetura ou engenharia que já foi tomada, em ADR numerada e imutável depois de aceita (formato do projeto ou MADR mínimo), com contexto neutro, opções, decisão em voz ativa e conse… |
| `/technical-writing-docs:escrever-changelog-release` | Escreve entradas de CHANGELOG para humanos (Keep a Changelog) e rascunho de release notes a partir de um intervalo de commits ou PRs, marcando quebras de compatibilidade e recomendando a versão pela convenção de commits. |
| `/technical-writing-docs:escrever-guia-diataxis` | Classifica o pedido nos quatro quadrantes Diátaxis (tutorial, how-to, referência, explicação) e escreve ou reorganiza a documentação a partir do código, dos testes e do contrato, um modo por página, com ligação cruzada,… |
| `/technical-writing-docs:escrever-readme` | Cria, atualiza ou revisa o README de um projeto comparando-o com o estado real do código (manifesto, scripts, LICENSE), com abertura de landing page, exemplo cedo, Quick Start copiável e sem enchimento; marca instalação… |
| `/technical-writing-docs:escrever-runbook` | Escreve runbook ou playbook de alerta para uso em on-call, com pré-requisitos, passos numerados (comando exato, resultado esperado e ramo de falha), marcação de passos destrutivos, verificação, rollback e escalonamento. |
| `/technical-writing-docs:playbook` | Guia e router do segmento Documentação e escrita técnica. |
| `/technical-writing-docs:prompts` | Biblioteca de prompts curados do segmento Documentação e escrita técnica. |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `technical-writing-docs:auditor-de-docs` (`plugins/technical-writing-docs/agents/auditor-de-docs.md`) | Auditor somente leitura que cruza um diff (PR, branch, intervalo de commits ou release) com a documentação do projeto e devolve mapa de cobertura Diátaxis, correções factuais com evidência arquivo:linha, links quebrados… | Read, Grep, Glob, Bash |
| `technical-writing-docs:revisor-de-instrucoes` (`plugins/technical-writing-docs/agents/revisor-de-instrucoes.md`) | Revisor independente, somente leitura e em contexto limpo, de arquivos de instrução para agentes - CLAUDE.md, CLAUDE.local.md, AGENTS.md, .claude/rules/*, SKILL.md e agents/*.md. | Read, Grep, Glob |
| `technical-writing-docs:revisor-de-leitor` (`plugins/technical-writing-docs/agents/revisor-de-leitor.md`) | Leitor novo e limpo, somente leitura, que responde perguntas reais usando apenas o texto de um documento e aponta lacunas - termos sem definição, passos que não conseguiria executar, contradições, pressupostos ocultos e… | Read |
| `technical-writing-docs:technical-writer` (`plugins/technical-writing-docs/agents/technical-writer.md`) | Redator técnico que recebe um briefing (leitor, tipo ou quadrante Diátaxis, fontes de fatos, caminhos de saída) e escreve ou edita arquivos de documentação - README, tutorial, how-to, referência, explicação, ADR de deci… | Read, Grep, Glob, Write, Edit |

## game-development (`game-development` 0.1.0)

Playbook, skills, agentes e prompts para desenvolver, revisar, otimizar e testar jogos em Godot/GDScript, Unity/C# e Unreal/C++, com verificação por execução (headless, sondas, captura), performance por orçamento, autoridade de rede, revisão de GDD, plano de QA e playtest, e modo GAMEDEV-COMPLETO por pedido explícito.

Instalar: `/plugin install game-development@brain-of-agent` · Playbook: `plugins/game-development/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/game-development:game-netcode-review` | Revisa código multiplayer (Unity Netcode for GameObjects e Godot high-level multiplayer) quanto a autoridade, validação de RPC e confiança no cliente, somente leitura, com cenário de abuso por achado. |
| `/game-development:game-perf-audit` | Audita a performance de um jogo (Godot, Unity, Unreal) contra os orçamentos do projeto, sem editar código; lista insumos FOUND/ABSENT, classifica CPU-bound ou GPU-bound, aponta candidatos por impacto x esforço e dá vere… |
| `/game-development:game-qa-plan` | Cria plano de QA de jogo por tipo de teste (Logic, Integration, Visual/Feel, UI, Config/Data), plano de smoke e de playtest, e relatório de playtest que separa defeito de sensação. |
| `/game-development:game-verify-by-running` | Verifica uma funcionalidade ou correção de jogo rodando o projeto (checks headless, sondas, captura, log) e entrega relatório com evidência real, separando o verificado do que exige humano (sensação, áudio, legibilidade… |
| `/game-development:gdd-review` | Revisa GDD ou documento de design de um sistema de jogo em quatro dimensões (completude, consistência, implementabilidade, encaixe com outros sistemas e pilares), com veredito por dimensão e agregado e lista de pergunta… |
| `/game-development:godot-gdscript` | Escreve, revisa e depura GDScript em Godot 4 conforme o guia de estilo oficial, com física em _physics_process e verificação headless. |
| `/game-development:playbook` | Guia e router do segmento Desenvolvimento de jogos (Godot/GDScript, Unity/C#, Unreal/C++) - verificação por execução do jogo, game loop e física, performance e profiling, netcode e autoridade, revisão de GDD, plano de Q… |
| `/game-development:prompts` | Biblioteca de prompts curados do segmento Desenvolvimento de jogos (Godot/GDScript, Unity/C#, Unreal/C++). |
| `/game-development:unity-csharp` | Escreve e revisa C# de runtime em Unity (6000.x; conferir 2022 LTS) com foco em alocação por frame, ciclo de vida, async com Awaitable, ScriptableObjects e testes Edit Mode/Play Mode. |
| `/game-development:unreal-cpp` | Revisa e escreve C++ de Unreal Engine conforme o padrão de código da Epic (UE 5.8) e orienta onde cada dado mora no Gameplay Framework (GameMode, GameState, PlayerState, PlayerController, Pawn, HUD). |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `game-development:game-engine-specialist` (`plugins/game-development/agents/game-engine-specialist.md`) | Especialista somente leitura na engine do projeto (Godot 4, Unity ou Unreal) para dúvidas de API, estrutura de cenas, prefabs e actors, sinais e eventos, e escolha de linguagem (GDScript x C# x GDExtension). | Read, Glob, Grep |
| `game-development:game-evaluator` (`plugins/game-development/agents/game-evaluator.md`) | Avaliador cético e independente do autor para uma funcionalidade de jogo já construída. | Read, Glob, Grep, Bash |
| `game-development:gameplay-programmer` (`plugins/game-development/agents/gameplay-programmer.md`) | Implementa mecânicas de jogo (máquina de estados, input, eventos, dados de gameplay) em GDScript, C# de Unity ou C++ de Unreal a partir de um GDD, critério de aceite ou spec aprovados, e só grava nos caminhos que o pedi… | Read, Glob, Grep, Write, Edit |
| `game-development:gameplay-reviewer` (`plugins/game-development/agents/gameplay-reviewer.md`) | Revisor adversarial somente leitura de diffs e scripts de gameplay (GDScript, C# de Unity, C++ de Unreal) em contexto limpo. | Read, Grep, Glob |
| `game-development:gdd-reviewer` (`plugins/game-development/agents/gdd-reviewer.md`) | Segunda leitura independente e somente leitura de um GDD ou documento de design de sistema, em quatro dimensões (completude, consistência, implementabilidade, encaixe com outros sistemas e pilares), com veredito por dim… | Read, Glob, Grep |

## systems-embedded-iot (`systems-embedded-iot` 0.1.0)

Revisão, depuração e testes de firmware (C/C++, Rust no_std, FreeRTOS, Zephyr, ESP32/STM32) com portão humano para gravar em hardware, datasheet primeiro e checklists de ISR, barramentos, MQTT e OTA seguro.

Instalar: `/plugin install systems-embedded-iot@brain-of-agent` · Playbook: `plugins/systems-embedded-iot/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/systems-embedded-iot:bus-protocol-review` | Revisa drivers de barramento e clientes de rede de dispositivo, somente relato: I2C, SPI, UART, CAN (TWAI), MQTT 3.1.1/5.0 e decisões de pilha BLE. |
| `/systems-embedded-iot:datasheet-first` | Escreve, porta ou revisa driver e código de periférico de firmware ancorando cada registrador, campo de bits, IRQ, pino e função HAL em fonte citada (datasheet, reference manual, errata, SVD ou header); sem fonte, para … |
| `/systems-embedded-iot:firmware-review` | Revisa código C/C++ de firmware sem editá-lo: retorno de erro, recursos, tipos e atomicidade, estilo defensivo, robustez de campo e política de memória. |
| `/systems-embedded-iot:firmware-root-cause` | Depura travamentos, resets, HardFault, panic, watchdog, corrupção de memória e comportamento intermitente de firmware com causa raiz antes da correção: registra motivo de reset e registradores de falha, formula no máxim… |
| `/systems-embedded-iot:firmware-test-host` | Planeja, escreve e roda testes de firmware no host e, com gate, no alvo: ztest (unit_testing, native_sim), Unity/CMock/Ceedling, ESP-IDF (Unity no alvo, mocks no host Linux, pytest-embedded), PlatformIO native, Rust (ca… |
| `/systems-embedded-iot:hw-bench-loop` | Conduz o ciclo compilar, gravar com confirmação, observar, comparar e corrigir numa bancada real de firmware, com cartão de gravação, confirmação explícita no chat, parada em ambiguidade e registro de evidência por está… |
| `/systems-embedded-iot:ota-security-review` | Revisa, somente leitura, atualização OTA, bootloader (MCUboot, ESP-IDF), secure boot, custódia de chaves, interfaces de depuração e baseline de segurança de dispositivo IoT (perguntas derivadas de NIST IR 8259A/Rev. |
| `/systems-embedded-iot:playbook` | Guia e router do segmento Sistemas, embarcados e IoT - revisar, depurar, testar e projetar firmware (C/C++, Rust no_std, FreeRTOS, Zephyr, ESP32/STM32/Arduino), barramentos (I2C, SPI, UART, CAN, MQTT, BLE), OTA e segura… |
| `/systems-embedded-iot:prompts` | Biblioteca de 30 prompts curados de firmware, embarcados e IoT, prontos para colar, com variáveis, motivo e fonte. |
| `/systems-embedded-iot:rtos-concurrency-review` | Revisa ISR, tarefas, prioridades, pilhas e dado compartilhado em firmware bare metal, FreeRTOS, Zephyr e Rust (RTIC, Embassy, critical-section), somente relato: tabela de dados compartilhados, tabela API por contexto, y… |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `systems-embedded-iot:embedded-architect` (`plugins/systems-embedded-iot/agents/embedded-architect.md`) | Arquiteto de decisões de firmware que produz ADR e orçamentos iniciais sem escrever arquivos. | Read, Grep, Glob |
| `systems-embedded-iot:firmware-debugger` (`plugins/systems-embedded-iot/agents/firmware-debugger.md`) | Investigador de causa raiz de firmware que propõe correção mínima sem aplicar. | Read, Grep, Glob, Bash |
| `systems-embedded-iot:firmware-reviewer` (`plugins/systems-embedded-iot/agents/firmware-reviewer.md`) | Revisor adversarial somente leitura de diffs e arquivos de firmware (C/C++/Rust no_std, FreeRTOS, Zephyr, ESP-IDF, STM32 HAL), em contexto limpo. | Read, Grep, Glob |
| `systems-embedded-iot:firmware-test-engineer` (`plugins/systems-embedded-iot/agents/firmware-test-engineer.md`) | Escritor de testes de firmware no host - Unity/CMock/Ceedling, ztest (unit_testing, native_sim), ESP-IDF Unity e pytest-embedded, PlatformIO native, cargo test com fakes de embedded-hal - mais planos de HIL com portão d… | Read, Grep, Glob, Write, Edit, Bash |
| `systems-embedded-iot:iot-security-auditor` (`plugins/systems-embedded-iot/agents/iot-security-auditor.md`) | Auditor somente leitura de segurança de dispositivo IoT e embarcado - OTA, bootloader, secure boot, custódia de chaves, interfaces de depuração, segredos no repositório, TLS do cliente e baseline NIST IR 8259A e ETSI EN… | Read, Grep, Glob |

## cli-desktop-tooling (`cli-desktop-tooling` 0.1.0)

Playbook, skills, agentes e prompts para projetar, revisar, empacotar e distribuir CLIs, TUIs e apps desktop (Electron, Tauri, WPF, WinUI, MAUI, Qt), com design de CLI para humanos e agentes, segurança desktop, assinatura de código, instaladores, auto-update, scripts PowerShell e bash e auditoria de developer experience.

Instalar: `/plugin install cli-desktop-tooling@brain-of-agent` · Playbook: `plugins/cli-desktop-tooling/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/cli-desktop-tooling:cli-design-review` | Revisa, somente leitura, o design de uma CLI (qualquer linguagem) para humanos e para agentes: subcomandos, flags, --help, exit codes, stdout versus stderr, --json, --no-input, erros acionáveis, segredos, ações destruti… |
| `/cli-desktop-tooling:desktop-release-checklist` | Audita, somente leitura, a prontidão de release de um app desktop (não tags, changelog ou semver, que são de git-workflow-release): assinatura de código no Windows e no macOS, SmartScreen, notarização, instaladores (MSI… |
| `/cli-desktop-tooling:desktop-security-audit` | Audita, somente leitura, a segurança de um app desktop Electron ou Tauri v2: mapa da fronteira de confiança, isolamento de contexto, sandbox, IPC, navegação, novas janelas, permissões, CSP, fuses, capabilities, AppManif… |
| `/cli-desktop-tooling:desktop-stack-decision` | Ajuda a escolher a stack de um app desktop (Electron, Tauri, WinUI 3, WPF, .NET MAUI ou Qt) a partir dos requisitos, separando restrições duras de distribuição (MSIX, Store, macOS, mobile, licença) de preferências, apli… |
| `/cli-desktop-tooling:dotnet-desktop-review` | Revisa, somente leitura, um app desktop .NET (WPF, WinUI 3 ou MAUI): comandos e data binding, MVVM Toolkit (CommunityToolkit.Mvvm), acessibilidade (nome acessível, teclado, alto contraste, escala, AutomationPeer, Narrat… |
| `/cli-desktop-tooling:dx-audit` | Audita a developer experience (DX) de uma CLI, biblioteca ou ferramenta: tempo até o primeiro resultado útil (TTHW), atritos de instalação, qualidade de ajuda e erros, documentação, caminho de upgrade e desinstalação, c… |
| `/cli-desktop-tooling:playbook` | Guia e router do segmento CLI, desktop e ferramentas de desenvolvedor: design de CLIs (argumentos, exit codes, saída para humanos e máquinas, uso por agentes), TUIs, apps desktop (Electron, Tauri, WPF, WinUI, MAUI, Qt),… |
| `/cli-desktop-tooling:prompts` | Biblioteca de prompts curados do segmento CLI, desktop e ferramentas de desenvolvedor (30 prompts prontos, com variáveis, motivo e fonte). |
| `/cli-desktop-tooling:shell-script-review` | Revisa, somente leitura, scripts PowerShell (.ps1, .psm1) e shell (.sh): verbos aprovados, SupportsShouldProcess e -WhatIf, tratamento de erro, $LASTEXITCODE em comandos nativos, PowerShell 5.1 versus 7, PSScriptAnalyze… |
| `/cli-desktop-tooling:tui-review` | Revisa, somente leitura, uma TUI (interface de terminal) em Textual (Python), Ratatui (Rust) ou Bubble Tea (Go): separação entre estado e renderização, bindings de teclado visíveis, ordem de foco, tratamento de resize, … |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `cli-desktop-tooling:cli-ux-reviewer` (`plugins/cli-desktop-tooling/agents/cli-ux-reviewer.md`) | Revisor somente leitura de CLIs e TUIs, em contexto limpo, para humanos e agentes. | Read, Grep, Glob |
| `cli-desktop-tooling:desktop-security-auditor` (`plugins/cli-desktop-tooling/agents/desktop-security-auditor.md`) | Auditor somente leitura da fronteira de confiança de apps Electron e Tauri v2: contextIsolation, nodeIntegration, sandbox, preload, IPC, navegação, permissões, CSP, fuses, capabilities, isolation pattern. | Read, Grep, Glob |
| `cli-desktop-tooling:diff-gap-reviewer` (`plugins/cli-desktop-tooling/agents/diff-gap-reviewer.md`) | Revisor adversarial genérico, em contexto novo e somente leitura, para qualquer mudança de CLI, TUI, app desktop, script ou instalador. | Read, Grep, Glob |
| `cli-desktop-tooling:release-readiness-auditor` (`plugins/cli-desktop-tooling/agents/release-readiness-auditor.md`) | Auditor somente leitura da prontidão de release de apps desktop: assinatura de código (Windows e macOS), SmartScreen, notarização, instaladores (MSIX, Inno Setup, WiX, NSIS, MSI), winget, auto-update (Electron, Tauri, S… | Read, Grep, Glob |
| `cli-desktop-tooling:script-reviewer` (`plugins/cli-desktop-tooling/agents/script-reviewer.md`) | Revisor somente leitura de scripts PowerShell (.ps1, .psm1) e shell (.sh/bash/sh): verbos aprovados, ShouldProcess e -WhatIf, tratamento de erro, $LASTEXITCODE, PSScriptAnalyzer, Pester, ShellCheck, aspas, cd sem ||, lo… | Read, Grep, Glob |

## blockchain-web3 (`blockchain-web3` 0.1.0)

Revisão de segurança de smart contracts (Solidity; Anchor com cobertura parcial), testes de invariantes e fuzz com Foundry, checklists de ERC-20/721/1155/4626, oráculos, L2, upgradeability e assinaturas, com portões de validação por PoC e regras para manter chaves e deploy fora do agente.

Instalar: `/plugin install blockchain-web3@brain-of-agent` · Playbook: `plugins/blockchain-web3/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/blockchain-web3:audit-contracts` | Conduz auditoria assistida de smart contracts em 5 fases com portões (definição, reconhecimento, varredura, validação, relatório), marcador de conclusão em cada arquivo de audit/, aprovação de custo antes de paralelismo… |
| `/blockchain-web3:contract-security-review` | Revisa diff ou arquivos de smart contract (Solidity) e relata só vulnerabilidades exploráveis, com caminho de ataque, refutação e confiança >= 0,8, somente leitura. |
| `/blockchain-web3:defi-oracle-l2-review` | Revisa como contratos consomem preço e oráculo (Chainlink: idade por updatedAt, decimals, feed por rede), premissas de L2 (feed de uptime do sequenciador, carência, alias de endereço, taxa de dados L1) e hooks do Uniswa… |
| `/blockchain-web3:exploit-poc` | Transforma um candidato a achado de segurança em PoC executável somente em fork local ou teste diferencial Foundry, roda forge test, cola comando e saída e classifica: PoC-passed, PoC-failed, apenas-rastro-de-código ou … |
| `/blockchain-web3:foundry-testing` | Cria e revisa testes Foundry para smart contracts em quatro modos: unit (unitário e fork local), invariants (handler, ghost, bound(), contadores), fuzz e gas (forge snapshot antes/depois). |
| `/blockchain-web3:playbook` | Guia e router do segmento Blockchain e Web3: desenvolvimento e auditoria assistida de smart contracts (Solidity; Anchor parcial), testes unitários, de fork, invariantes e fuzz com Foundry, padrões ERC (20, 721, 1155, 46… |
| `/blockchain-web3:prompts` | Biblioteca de 29 prompts curados de Blockchain e Web3 prontos para colar, com variáveis e fontes. |
| `/blockchain-web3:solana-anchor-review` | Revisa constraints de conta e riscos básicos de programas Solana escritos em Anchor (Signer, UncheckedAccount com /// CHECK:, PDAs com seeds e bump, has_one, init_if_needed, realloc, close, discriminador), somente leitu… |
| `/blockchain-web3:token-standards-review` | Confere conformidade e integração segura de tokens ERC-20, ERC-721, ERC-1155 e cofres ERC-4626 (arredondamento, preview, ataque de inflação de shares, hooks de recebimento, token com taxa ou rebase), somente leitura. |
| `/blockchain-web3:wallet-signing-review` | Revisa a segurança de assinaturas off-chain (EIP-712, permit, meta-transação, claim assinado) e da integração de carteira (EIP-1193): domínio, nonce, validade, replay, frontrunning, erros do provider e 'o que o usuário … |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `blockchain-web3:defi-protocol-analyst` (`plugins/blockchain-web3/agents/defi-protocol-analyst.md`) | Analista somente leitura de oráculos de preço, premissas de L2, vaults ERC-4626 e hooks do Uniswap v4 em protocolos DeFi. | Read, Grep, Glob |
| `blockchain-web3:finding-refuter` (`plugins/blockchain-web3/agents/finding-refuter.md`) | Revisor adversarial em contexto novo que tenta derrubar um achado de segurança de smart contract antes de ele entrar no relatório ou virar PoC. | Read, Grep, Glob |
| `blockchain-web3:invariant-test-engineer` (`plugins/blockchain-web3/agents/invariant-test-engineer.md`) | Engenheiro de testes Foundry que escreve handlers, ghosts, invariantes, testes de fuzz, de fork e de regressão para smart contracts e mede gás com forge snapshot. | Read, Grep, Glob, Write, Edit, Bash |
| `blockchain-web3:solidity-security-reviewer` (`plugins/blockchain-web3/agents/solidity-security-reviewer.md`) | Revisa diffs e arquivos de smart contracts (Solidity; Anchor com cobertura parcial) em busca de vulnerabilidades exploráveis, somente leitura, e devolve um relatório com achados por severidade, evidência arquivo:linha e… | Read, Grep, Glob |
| `blockchain-web3:web3-agent-safety-auditor` (`plugins/blockchain-web3/agents/web3-agent-safety-auditor.md`) | Audita a configuração do Claude Code de um repositório Web3 (permissões, hooks, CLAUDE.md, MCP, scripts, skills de terceiros) quanto a vazamento de chave e a movimentação de fundos pelo agente. | Read, Grep, Glob |

## automation-integrations (`automation-integrations` 0.1.0)

Playbook, skills, agentes e prompts para automação de workflows, webhooks idempotentes, integrações entre APIs, servidores MCP, hooks de guardrail, jobs agendados com claude -p, scraping responsável e autoria de skills e plugins do Claude Code, com segurança contra injeção em conteúdo externo.

Instalar: `/plugin install automation-integrations@brain-of-agent` · Playbook: `plugins/automation-integrations/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/automation-integrations:assessing-automation-risk` | Avalia, só em leitura, o risco de uma automação, de uma configuração de MCP ou da adoção de skill, plugin, hook ou instalador de terceiro: trifecta letal (dado privado, conteúdo hostil, saída externa), escopos e aprovaç… |
| `/automation-integrations:authoring-plugin-skills` | Cria, revisa, calibra e avalia skills e plugins do Claude Code: frontmatter real, descrição que dispara, estrutura com progressive disclosure, suíte claude plugin eval, checklist de manifesto e codificação de um fluxo a… |
| `/automation-integrations:building-mcp-servers` | Projeta, implementa e avalia um servidor MCP (stdio local ou HTTP remoto) que expõe uma API ou sistema como tools para o Claude: mapa API-para-tools por intenção, schemas, anotações de risco, logs em stderr, checagem de… |
| `/automation-integrations:designing-workflow-automations` | Desenha workflows de automação (n8n, Zapier, Make, scripts, cron) e sincronizações entre APIs com contrato de falha: workflow ou agente, chave de idempotência, retry com backoff, 429 e Retry-After, paginação, OAuth refr… |
| `/automation-integrations:playbook` | Guia e router do segmento Automação, integrações e MCP. |
| `/automation-integrations:prompts` | Biblioteca de prompts curados do segmento Automação, integrações e MCP, prontos para colar: entrevista de requisitos, workflow ou agente, plano e avaliação de servidor MCP, revisão de segurança de MCP, auditoria e imple… |
| `/automation-integrations:responsible-scraping` | Planeja e executa extração de dados da web em modo somente leitura, respeitando robots.txt (RFC 9309), taxa e termos, e devolve um JSON estável com nota de conformidade. |
| `/automation-integrations:reviewing-webhook-receivers` | Revisa ou implementa um receptor de webhook confiável: corpo bruto, assinatura em tempo constante, tolerância de timestamp, deduplicação por ID de evento, 2xx rápido com fila, ordem não garantida, fila de mortas e repro… |
| `/automation-integrations:scheduling-headless-jobs` | Desenha jobs agendados e automações de CI com claude -p e a claude-code-action de forma segura e verificável: --bare, lista mínima de ferramentas, modo sem prompts, teto de custo, saída JSON, gate de plugin_errors e mcp… |
| `/automation-integrations:writing-hook-guardrails` | Projeta, escreve e testa um hook de guardrail do Claude Code (por exemplo bloquear git push --force, rm -rf fora do projeto ou leitura de segredos) e entrega script, casos de teste e o trecho de configuração sem ativá-l… |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `automation-integrations:automation-architect` (`plugins/automation-integrations/agents/automation-architect.md`) | Projetista de automações e integrações: escolhe a forma mais simples e confiável (workflow, agente com limite, tool MCP, hook, job claude -p, skill) e desenha o contrato de falha, os riscos e o plano de verificação, sem… | Read, Grep, Glob |
| `automation-integrations:integration-reviewer` (`plugins/automation-integrations/agents/integration-reviewer.md`) | Revisor independente, adversarial e somente leitura de integrações: receptores de webhook, consumidores de fila, jobs agendados, clientes de API de saída e fluxos de erro de workflows (n8n e similares). | Read, Grep, Glob |
| `automation-integrations:mcp-security-reviewer` (`plugins/automation-integrations/agents/mcp-security-reviewer.md`) | Revisor somente leitura de segurança de servidores MCP (código) e de configuração de MCP (.mcp.json, settings, servidores de plugin, uso em claude -p e CI). | Read, Grep, Glob |
| `automation-integrations:plugin-validator` (`plugins/automation-integrations/agents/plugin-validator.md`) | Valida estrutura, manifesto, frontmatter e qualidade de prompt de um plugin do Claude Code (skills, agentes, evals), rodando só os validadores oficiais e a verificação estrutural, sem instalar nem executar código do plu… | Read, Grep, Glob, Bash |
| `automation-integrations:third-party-auditor` (`plugins/automation-integrations/agents/third-party-auditor.md`) | Auditor somente leitura de skills, plugins, servidores MCP, hooks, scripts e instaladores de terceiros antes da adoção. | Read, Grep, Glob |

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

## design-engineering-kit (`design-engineering-kit` 0.1.0)

Complemento opcional do ux-ui-design para designer-engenheiro: do link do Figma à UI implementada, verificada no navegador (Playwright MCP) e polida, com 17 skills de motion, polimento e direção visual (Emil Kowalski e taste-skill, MIT, vendorizadas sem alteração), precedência explícita de estilo (design system do projeto, design system da casa, direções taste), agentes somente leitura, prompts e evals.

Instalar: `/plugin install design-engineering-kit@brain-of-agent` · Playbook: `plugins/design-engineering-kit/skills/playbook/SKILL.md`

| Skill | Quando usar |
|---|---|
| `/design-engineering-kit:animate` | Build an animation from scratch, making the decisions in the order that determines whether it feels right — should it animate at all, what purpose, which tool, which properties, which curve and duration, how it interrup… |
| `/design-engineering-kit:animate-expo` | Build animations in React Native and Expo, making the decisions in the order that determines whether they feel right — should it animate, which thread it runs on, which properties, spring or timing, how the gesture hand… |
| `/design-engineering-kit:animation-vocabulary` | Reverse-lookup glossary that turns a vague description of a web animation or motion effect into its exact term ("the bouncy thing when a popover opens" → Pop in; "the iOS rubber-band scroll" → Rubber-banding). |
| `/design-engineering-kit:apple-design` | Apple's approach to interface design and fluid, physical motion, translated for the web. |
| `/design-engineering-kit:break-ui` | Try to break a piece of UI by feeding it worst-case data — long names, unbreakable emails, one-letter names, missing fields, huge counts, zero items, long labels, non-Latin text, emoji, extreme numbers — then render it … |
| `/design-engineering-kit:design-taste-frontend` | Anti-slop frontend skill for landing pages, portfolios, and redesigns. |
| `/design-engineering-kit:emil-design-eng` | This skill encodes Emil Kowalski's philosophy on UI polish, component design, animation decisions, and the invisible details that make software feel great. |
| `/design-engineering-kit:find-animation-opportunities` | Search a codebase or UI for places that don't animate but should, and reject everything that shouldn't. |
| `/design-engineering-kit:high-end-visual-design` | Teaches the AI to design like a high-end agency. |
| `/design-engineering-kit:improve-animations` | Survey a codebase's animation and motion code as a senior motion advisor, then produce a prioritized audit and self-contained implementation plans for other agents (or cheaper models) to execute. |
| `/design-engineering-kit:industrial-brutalist-ui` | Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics. |
| `/design-engineering-kit:minimalist-ui` | Clean editorial-style interfaces. |
| `/design-engineering-kit:mobile-native` | Make a web app feel native on a phone — the small CSS and meta-tag fixes that separate "a website in a browser" from something that feels installed. |
| `/design-engineering-kit:pick-ui-library` | Pick the right library for a given frontend task from a curated, opinionated list — numbers, OTP inputs, charts, command menus, virtualization, drag and drop, toasts, state, styling, and more. |
| `/design-engineering-kit:playbook` | Guia e router do designer-engenheiro. |
| `/design-engineering-kit:prompts` | Biblioteca de 16 prompts prontos para designer-engenheiro, com objetivo, quando usar, prompt em bloco e critério de pronto - implementar tela a partir de link do Figma, mapear variáveis para tokens, comparar com o frame… |
| `/design-engineering-kit:prototype` | Build multiple genuinely different versions of a UI piece you describe, rendered behind a visual picker so you can flip through them live and promote the one that feels right. |
| `/design-engineering-kit:redesign-existing-projects` | Upgrades existing websites and apps to premium quality. |
| `/design-engineering-kit:review-animations` | Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy. |

| Agente | Quando delegar | Ferramentas |
|---|---|---|
| `design-engineering-kit:motion-polish-reviewer` (`plugins/design-engineering-kit/agents/motion-polish-reviewer.md`) | Revisa motion e polimento de UI por leitura, aplicando os 10 padrões da skill review-animations, o checklist do emil-design-eng e o catálogo do break-ui, sempre depois dos tokens de motion do design system do projeto. | Read, Grep, Glob |
| `design-engineering-kit:ui-verifier` (`plugins/design-engineering-kit/agents/ui-verifier.md`) | Verifica no navegador, com o Playwright MCP, uma UI já implementada contra o Figma, o brief ou o design system, e devolve relatório com achados (ID, severidade, evidência, recomendação). | (herda) |
