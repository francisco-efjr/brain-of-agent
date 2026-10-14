# Registro de conhecimento por tag (gerado)

Gerado por `tools/publish_brain.py` a partir de `docs/foundation/knowledge/*.json` da fábrica (tags curadas) e dos `keywords` de cada plugin publicado (uma tag automática por plugin). Esquema e regras: `docs/dev-segments/foundation/knowledge-registry-spec.md`. Não edite à mão.

**Como o orquestrador usa (ORCHESTRATOR.md §3, passo 3):** case a demanda com os gatilhos (sinônimos, PT-BR ou EN; pode casar mais de uma tag). O especialista vem da rota **líder**; o subagente carrega também as skills das rotas de **fundamentos**; **apoio** entra se o contexto pedir; o validador independente vem da coluna própria. Tag **em construção**: declare a lacuna e use a rota publicada mais próxima. Nenhuma tag casando: use `CATALOGO.md` e a tabela de combinações do §4, e registre a lacuna.

Tags: 29 curadas, 27 automáticas; 53 publicadas, 3 em construção.

## Tags curadas (conhecimento transversal e adquirido)

| Tag | Conhecimento | Gatilhos (amostra) | Líder | Fundamentos e apoio | Validador | Status |
|---|---|---|---|---|---|---|
| `adr-decisoes` | ADRs e documentação de decisões | escreve um adr para essa decisão; documenta por que escolhemos x; registra a decisão de arquitetura; me dá um modelo de adr; como numero os adrs desse repo; substituir um adr antigo… | `architecture-design` · agentes `architecture-design:adr-writer` · skills `adr`, `adr-write` | `engineering-lifecycle` · skills `documentation-and-adrs`<br>`technical-writing-docs` · agentes `technical-writing-docs:technical-writer` · skills `escrever-adr`, `escrever-readme`<br>`product-discovery-specs` · agentes `product-discovery-specs:decision-recorder` | `technical-writing-docs:auditor-de-docs` | publicado |
| `barra-de-qualidade` | Barra de qualidade (CONSTRAINTS.md), catraca e guarda de afrouxamento | defina nossos padrões de qualidade; crie um constraints.md; set up constraints; quality gates para o agente; o agente está pulando teste pra passar; o agente silenciou o lint… | `engineering-lifecycle` · agentes `engineering-lifecycle:quality-bar-guardian` · skills `constraint-driven-development` | `qa-testing` · skills `tdd-guard`, `verification-gate`<br>`code-quality-refactoring` · skills `tech-debt-triage`<br>`devops-cloud-infra` · skills `gha-hardening-review`<br>`sre-observability` · skills `slo-design` | `qa-testing:test-auditor` | publicado |
| `ci-cd-portoes` | CI/CD e portões de qualidade | monta o pipeline de ci para esse repo; meu ci está lento; o ci falhou, o que faço; quais gates devo ter; configura o github actions; shift left nos testes… | `devops-cloud-infra` · agentes `devops-cloud-infra:pipeline-security-auditor` · skills `gha-hardening-review`, `secrets-review`, `deploy-infra` | `engineering-lifecycle` · skills `ci-cd-and-automation`<br>`qa-testing` · skills `verification-gate`<br>`git-workflow-release` · skills `criar-pr` | `devops-cloud-infra:infra-reviewer` | publicado |
| `contexto-agente` | Contexto, regras do projeto e handoff entre sessões | o agente está ignorando as convenções do projeto; como montar o claude.md; o agente está inventando apis; a sessão está ficando confusa; o contexto está grande, o que cortar; quando devo abrir uma sessão nova… | `engineering-lifecycle` · skills `context-engineering` | `llm-ai-agents` · skills `instruction-authoring`<br>`technical-writing-docs` · skills `auditar-claude-md`<br>`backend-api` · skills `backend-claude-md-setup`<br>`product-discovery-specs` · skills `spec-to-tasks` | `technical-writing-docs:revisor-de-instrucoes` | publicado |
| `contrato-api` | Contrato de API, idempotência e retries seguros | desenhe os endpoints dessa feature; como versionar essa api sem quebrar clientes; defina o contrato entre esses módulos; put ou patch; paginação e erros padronizados; adicione um campo sem quebrar quem consome… | `backend-api` · agentes `backend-api:backend-architect` · skills `api-contract-design`, `idempotency-and-resilience` | `engineering-lifecycle` · skills `api-and-interface-design`<br>`architecture-design` · skills `api-design`, `resilience-and-consistency`<br>`fintech-payments` · skills `payment-idempotency`<br>`automation-integrations` · skills `reviewing-webhook-receivers` | `backend-api:api-contract-reviewer` | publicado |
| `definicao-de-pronto` | Definição de pronto e checklists de verificação | quando posso considerar isso pronto; isso está pronto de verdade; checklist antes do merge; o que falta para fechar essa tarefa; crie um critério de pronto para o projeto; gate final antes de subir… | `qa-testing` · skills `verification-gate` | `engineering-lifecycle` · skills `incremental-implementation`<br>`ux-ui-design` · skills `a11y-checklist`<br>`security-appsec` · skills `secrets-supply-chain-review`<br>`web-frontend` · skills `perf-audit` | `qa-testing:test-reviewer` | publicado |
| `deprecacao-migracao` | Deprecação, migração e mudança de schema sem downtime | como removo essa api antiga; quero descontinuar essa funcionalidade; plano de deprecação; como migro os usuários para o novo serviço; devo manter esse sistema legado; código que ninguém mantém mas todo mundo usa… | `code-quality-refactoring` · skills `migration-parity`, `refactor-seguro` | `engineering-lifecycle` · skills `deprecation-and-migration`<br>`database-data-modeling` · agentes `database-data-modeling:db-migration-planner` · skills `safe-migrations`<br>`architecture-design` · skills `decomposition` | `database-data-modeling:db-reviewer` | publicado |
| `depuracao-causa-raiz` | Depurar até a causa raiz | depura esse erro; por que isso está falhando; os testes quebraram depois da mudança; o build falhou, o que é isso; funcionava ontem e parou; acha o commit que introduziu o bug… | `code-quality-refactoring` · agentes `code-quality-refactoring:debugger` · skills `debug-causa-raiz` | `engineering-lifecycle` · skills `debugging-and-error-recovery`<br>`sre-observability` · skills `root-cause-investigation`<br>`backend-api` · skills `backend-debugging`<br>`git-workflow-release` · skills `bisect-regressao` | `code-quality-refactoring:finding-validator` | publicado |
| `docs-oficiais` | Código fundamentado na documentação oficial da versão em uso | confirme na documentação oficial antes de implementar; isso ainda é a forma recomendada nessa versão; essa api está deprecada; use a sintaxe da versão do meu package.json; cite as fontes dessa implementação; não quero código de memória… | `engineering-lifecycle` · skills `source-driven-development` | `backend-api` · skills `stack-conventions`<br>`security-appsec` · skills `agent-risk-triage` | `code-quality-refactoring:finding-validator` | publicado |
| `entrevista-intencao` | Entrevista de intenção e ambiguidade explícita | me entreviste antes de começar; interview me; grill me; stress-test my thinking; não sei bem o que quero; o que eu realmente quero com isso… | `engineering-lifecycle` · skills `interview-me` | `product-discovery-specs` · skills `spec-interview`, `write-prd` | `product-discovery-specs:spec-reviewer` | publicado |
| `fatias-incrementais` | Implementação em fatias verticais pequenas | implemente isso em etapas pequenas; faça só a próxima tarefa do plano; não quero um pr gigante; vamos por partes testando cada uma; feature atrás de flag; mantenha o build verde entre os passos… | `engineering-lifecycle` · skills `incremental-implementation` | `qa-testing` · skills `tdd-guard`<br>`git-workflow-release` · skills `commit-convencional`, `criar-pr`<br>`code-quality-refactoring` · skills `refactor-seguro` | `git-workflow-release:revisor-plano` | publicado |
| `git-versionamento-release` | Git, commits atômicos, branches curtas e versionamento | como organizo meus commits; faça commits atômicos; faça um pr pequeno; quanto deve ter um commit; como volto ao último estado que funcionava; qual versão devo subir… | `git-workflow-release` · agentes `git-workflow-release:revisor-diff` · skills `commit-convencional`, `criar-pr`, `rebase-seguro`, `release-cut`, `encerrar-branch` | `engineering-lifecycle` · skills `git-workflow-and-versioning`<br>`technical-writing-docs` · skills `escrever-changelog-release` | `git-workflow-release:auditor-release` | publicado |
| `lancamento-rollback` | Lançamento em produção: checklist, rollout em estágios e rollback | vamos subir isso para produção, o que falta; checklist antes do deploy; estamos prontos para o go-live; como fazemos o rollout gradual; canary de 5% dos usuários; quero lançar atrás de uma flag… | `devops-cloud-infra` · agentes `devops-cloud-infra:rollout-planner` · skills `progressive-delivery` | `engineering-lifecycle` · skills `shipping-and-launch`<br>`sre-observability` · skills `release-health`, `slo-design`<br>`database-data-modeling` · skills `backup-restore-runbook`, `safe-migrations`<br>`technical-writing-docs` · skills `escrever-runbook` | `git-workflow-release:auditor-release` | publicado |
| `observabilidade-instrumentar` | Observabilidade: instrumentar, métricas RED e alertas por sintoma | instrumenta esse serviço; adiciona logs e métricas nessa feature; não consigo saber o que aconteceu em produção; como estruturar meus logs; adiciona tracing com opentelemetry; quais métricas devo expor… | `sre-observability` · skills `telemetry-review`, `alert-review`, `slo-design`, `runbook` | `engineering-lifecycle` · skills `observability-and-instrumentation`<br>`technical-writing-docs` · skills `escrever-runbook` | `sre-observability:reliability-reviewer` | publicado |
| `orquestracao-multiagente` | Orquestração de subagentes: padrões e anti-padrões | orquestrar subagentes; rodar especialistas em paralelo; fan-out com merge; quando usar subagente ou agent team; agente chamando agente; router de agentes… | `orchestrator` · agentes `orchestrator:demand-router` · skills `playbook` | `engineering-lifecycle` · agentes `engineering-lifecycle:code-reviewer`, `engineering-lifecycle:security-auditor`, `engineering-lifecycle:test-engineer` · skills `shipping-and-launch`<br>`llm-ai-agents` · skills `agent-architecture` | `llm-ai-agents:agent-security-reviewer` | publicado |
| `performance-web` | Medir e otimizar performance (Core Web Vitals, N+1, índice, cache) | isso está lento; otimiza a performance disso; melhora o lcp da página; core web vitals ruins; tem n+1 nessa consulta; o endpoint demora demais… | `web-frontend` · agentes `web-frontend:frontend-perf-reviewer` · skills `perf-audit` | `engineering-lifecycle` · agentes `engineering-lifecycle:web-performance-auditor` · skills `performance-optimization`<br>`sre-observability` · skills `performance-engineering`<br>`database-data-modeling` · skills `query-plan-and-indexing` | `sre-observability:perf-analyst` | publicado |
| `pesquisa-web-apify` | Pesquisa e coleta de dados na web em escala (Apify MCP) | pesquisa na web em escala; pesquisar fontes em massa; raspar dados; web scraping; coletar dados de sites; crawler… | `web-research-apify` · agentes `web-research-apify:apify-researcher` · skills `playbook`, `escolher-actor`, `dataset-para-itens` (em construção) | `automation-integrations` · agentes `automation-integrations:third-party-auditor` · skills `responsible-scraping`, `assessing-automation-risk`<br>`security-appsec` · agentes `security-appsec:agent-config-auditor` · skills `agent-risk-triage`<br>`llm-ai-agents` · agentes `llm-ai-agents:agent-security-reviewer` · skills `tool-design-review` | `web-research-apify:apify-source-verifier`, `web-research-apify:apify-cost-auditor`, `automation-integrations:third-party-auditor` | em construção |
| `quebrar-em-tarefas` | Quebrar a spec em tarefas verticais e verificáveis | quebre em tarefas; faça o plano de implementação; divida isso em tarefas; break this into tasks; plan the implementation; tarefas verticais… | `product-discovery-specs` · agentes `product-discovery-specs:plan-writer` · skills `spec-to-tasks`, `refine-backlog` | `engineering-lifecycle` · skills `planning-and-task-breakdown`<br>`architecture-design` · skills `decomposition`<br>`qa-testing` · skills `test-design` | `product-discovery-specs:spec-reviewer` | publicado |
| `refinar-ideia` | Refinar uma ideia: divergir, convergir e cortar | refine essa ideia; refine this idea; ideate on; me ajuda a refinar essa ideia; gera variações disso; quais outras abordagens existem… | `engineering-lifecycle` · skills `idea-refine` | `product-discovery-specs` · agentes `product-discovery-specs:decision-recorder`, `product-discovery-specs:feasibility-scout` · skills `run-discovery`, `prioritize-roadmap` | `architecture-design:skeptic-architect` | publicado |
| `revisao-de-codigo` | Revisão de código antes do merge | revisa esse pr; faz o code review desse diff; posso mergear isso; revisa minhas mudanças antes do merge; dá uma olhada nesse diff; revisão em cinco eixos… | `code-quality-refactoring` · agentes `code-quality-refactoring:code-reviewer` · skills `review-diff` | `engineering-lifecycle` · agentes `engineering-lifecycle:code-reviewer` · skills `code-review-and-quality`<br>`security-appsec` · skills `security-review-diff`<br>`git-workflow-release` · agentes `git-workflow-release:revisor-diff` · skills `criar-pr` | `code-quality-refactoring:finding-validator` | publicado |
| `revisao-por-duvida` | Revisão por dúvida em contexto novo e triagem de achados | revise isso antes de eu confiar; faça uma revisão adversarial; encontre o que pode dar errado nesse plano; questione minhas suposições; dê uma segunda opinião com contexto limpo; prove que esse código está errado… | `engineering-lifecycle` · agentes `engineering-lifecycle:fresh-context-doubter` · skills `doubt-driven-development` | `architecture-design` · agentes `architecture-design:skeptic-architect` · skills `design-review`<br>`security-appsec` · agentes `security-appsec:finding-verifier` | `code-quality-refactoring:finding-validator` | publicado |
| `roteador-de-fases` | Roteador de fases do ciclo de engenharia | qual skill usar; por onde começo essa tarefa; em que fase do ciclo estou; qual é o próximo passo do ciclo; me guie pelas fases; qual comando usar agora… | `orchestrator` · agentes `orchestrator:demand-router` · skills `playbook` | `engineering-lifecycle` · skills `using-agent-skills`<br>`automation-integrations` · skills `authoring-plugin-skills` | `llm-ai-agents:prompt-reviewer` | publicado |
| `seguranca-hardening` | Segurança: modelagem de ameaças, endurecimento e fronteiras de aprovação | isso é seguro; revisa a segurança disso; audita as vulnerabilidades; endurece esse endpoint; tem injeção aqui; faça uma modelagem de ameaças… | `security-appsec` · agentes `security-appsec:security-reviewer`, `security-appsec:threat-modeler` · skills `security-review-diff`, `threat-model`, `secrets-supply-chain-review`, `harden-claude-code`, `agent-risk-triage` | `engineering-lifecycle` · agentes `engineering-lifecycle:security-auditor` · skills `security-and-hardening`<br>`backend-api` · skills `api-security-review`<br>`llm-ai-agents` · agentes `llm-ai-agents:agent-security-reviewer` · skills `agent-security-review` | `security-appsec:finding-verifier` | publicado |
| `simplificar-codigo` | Simplificar código sem mudar o comportamento | simplifica esse código; deixa isso mais legível; esse código está complicado demais; refatora sem mudar o comportamento; tira o aninhamento e o código morto; posso apagar esse código… | `code-quality-refactoring` · skills `simplify-safe`, `refactor-seguro`, `tech-debt-triage` | `engineering-lifecycle` · skills `code-simplification`<br>`qa-testing` · skills `test-design` | `qa-testing:test-auditor` | publicado |
| `spec-antes-do-codigo` | Spec antes do código, com aprovação | escreva a spec antes; write a spec first; faça um prd; spec antes do código; não codar antes de ter spec; documente os requisitos antes de implementar… | `product-discovery-specs` · skills `write-spec`, `write-prd`, `spec-interview`, `acceptance-criteria` | `engineering-lifecycle` · skills `spec-driven-development`<br>`architecture-design` · skills `decomposition`<br>`qa-testing` · skills `test-strategy` | `product-discovery-specs:spec-reviewer` | publicado |
| `tdd` | TDD, pirâmide e padrões de teste | faça isso com tdd; escreva o teste antes do código; crie um teste que reproduza esse bug antes de corrigir; red green refactor; prove-it; teste de regressão para esse bug… | `qa-testing` · agentes `qa-testing:test-writer`, `qa-testing:test-reviewer` · skills `tdd-guard`, `test-design`, `test-strategy`, `flaky-triage` | `engineering-lifecycle` · agentes `engineering-lifecycle:test-engineer` · skills `test-driven-development`<br>`web-frontend` · skills `e2e-tests`<br>`backend-api` · skills `api-test-suite` | `qa-testing:test-auditor` | publicado |
| `testes-funcionais-playwright` | Validação funcional, funcionalidade por funcionalidade, com Playwright | testar funcionalidade por funcionalidade; validar cada funcionalidade; abrir o app e validar; validação funcional; matriz de funcionalidades; inventário de funcionalidades… | `qa-playwright` · agentes `qa-playwright:feature-explorer`, `qa-playwright:spec-writer`, `qa-playwright:spec-reviewer`, `qa-playwright:failure-triager`, `qa-playwright:matrix-auditor` · skills `playbook`, `feature-inventory`, `explore-feature`, `write-specs` (em construção) | `qa-testing` · agentes `qa-testing:test-auditor`, `qa-testing:test-writer` · skills `e2e-review`, `test-strategy`, `verification-gate`<br>`web-frontend` · agentes `web-frontend:ui-evaluator` · skills `e2e-tests`, `verify-ui`<br>`engineering-lifecycle` · agentes `engineering-lifecycle:test-engineer` · skills `browser-testing-with-devtools`, `test-driven-development`<br>`design-engineering-kit` · agentes `design-engineering-kit:ui-verifier` · skills `playbook` | `qa-playwright:matrix-auditor`, `qa-testing:test-auditor` | em construção |
| `ui-producao` | UI de produção: acessível, responsiva e verificada no navegador | monte esse componente; crie essa tela responsiva; isso parece feito por ia, melhore; faça o formulário acessível; estados de carregando, vazio e erro; tem erro no console da página… | `web-frontend` · agentes `web-frontend:frontend-a11y-reviewer`, `web-frontend:frontend-code-reviewer` · skills `design-ui`, `component-review`, `a11y-review`, `verify-ui` | `engineering-lifecycle` · skills `frontend-ui-engineering`, `browser-testing-with-devtools`<br>`ux-ui-design` · skills `a11y-checklist`, `design-tokens`<br>`design-engineering-kit` · skills `design-taste-frontend`, `minimalist-ui` | `web-frontend:ui-evaluator` | publicado |
| `video-edicao` | Edição e produção de vídeo com código (HyperFrames) | edição de vídeo; editar vídeo; editar um vídeo; montar um vídeo; criar um vídeo; produzir um vídeo… | `video-hyperframes` · skills `playbook` (em construção) | `design-engineering-kit` · agentes `design-engineering-kit:motion-polish-reviewer` · skills `animate`, `animation-vocabulary`, `review-animations`<br>`ux-ui-design` · agentes `ux-ui-design:design-evaluator` · skills `design-brief`, `ux-writing` | `design-engineering-kit:motion-polish-reviewer` | em construção |

## Tags por plugin (automáticas: gatilhos = keywords do plugin)

| Tag | Conhecimento | Gatilhos (amostra) | Líder | Fundamentos e apoio | Validador | Status |
|---|---|---|---|---|---|---|
| `architecture-design` | Decisões de arquitetura com humano no comando: ADRs, trade-offs, revisão de desenho, system design, decomposi… | architecture; adr; system-design; c4; ddd; hexagonal… | `architecture-design` · agentes `architecture-design:adr-writer`, `architecture-design:architecture-blueprint`, `architecture-design:architecture-reviewer`, `architecture-design:boundary-mapper`, `architecture-design:skeptic-architect` · skills `playbook` | — | — | publicado |
| `automation-integrations` | Playbook, skills, agentes e prompts para automação de workflows, webhooks idempotentes, integrações entre API… | automation; integrations; mcp; mcp-server; webhooks; idempotency… | `automation-integrations` · agentes `automation-integrations:automation-architect`, `automation-integrations:integration-reviewer`, `automation-integrations:mcp-security-reviewer`, `automation-integrations:plugin-validator`, `automation-integrations:third-party-auditor` · skills `playbook` | — | — | publicado |
| `backend-api` | Projete, implemente, revise, teste e depure serviços e APIs (REST, GraphQL, gRPC) com contrato OpenAPI, erros… | backend; api; rest; openapi; graphql; grpc… | `backend-api` · agentes `backend-api:api-contract-reviewer`, `backend-api:api-security-reviewer`, `backend-api:api-test-engineer`, `backend-api:backend-architect`, `backend-api:backend-debugger` · skills `playbook` | — | — | publicado |
| `blockchain-web3` | Revisão de segurança de smart contracts (Solidity; Anchor com cobertura parcial), testes de invariantes e fuz… | web3; blockchain; solidity; smart-contracts; foundry; openzeppelin… | `blockchain-web3` · agentes `blockchain-web3:defi-protocol-analyst`, `blockchain-web3:finding-refuter`, `blockchain-web3:invariant-test-engineer`, `blockchain-web3:solidity-security-reviewer`, `blockchain-web3:web3-agent-safety-auditor` · skills `playbook` | — | — | publicado |
| `cli-desktop-tooling` | Playbook, skills, agentes e prompts para projetar, revisar, empacotar e distribuir CLIs, TUIs e apps desktop … | cli; command-line; tui; electron; tauri; wpf… | `cli-desktop-tooling` · agentes `cli-desktop-tooling:cli-ux-reviewer`, `cli-desktop-tooling:desktop-security-auditor`, `cli-desktop-tooling:diff-gap-reviewer`, `cli-desktop-tooling:release-readiness-auditor`, `cli-desktop-tooling:script-reviewer` · skills `playbook` | — | — | publicado |
| `code-quality-refactoring` | Revisão de código com filtro de alto sinal, debugging por causa raiz, refatoração segura com testes de caract… | code-review; refactoring; debugging; root-cause; technical-debt; legacy-modernization… | `code-quality-refactoring` · agentes `code-quality-refactoring:code-reviewer`, `code-quality-refactoring:codebase-mapper`, `code-quality-refactoring:debugger`, `code-quality-refactoring:finding-validator`, `code-quality-refactoring:refactor-planner` · skills `playbook` | — | — | publicado |
| `data-engineering` | Engenharia de dados e analytics para o Claude Code: pipelines ETL/ELT, dbt, Airflow e Dagster, Spark e stream… | data-engineering; etl; elt; dbt; airflow; dagster… | `data-engineering` · agentes `data-engineering:analytics-reviewer`, `data-engineering:data-pipeline-architect`, `data-engineering:data-pipeline-reviewer`, `data-engineering:eval-judge`, `data-engineering:pipeline-debugger` · skills `playbook` | — | — | publicado |
| `data-science-ml` | Playbook de ciência de dados e machine learning para Claude Code: EDA sem vazamento, validação e métricas, tr… | data-science; machine-learning; scikit-learn; pytorch; gradient-boosting; data-leakage… | `data-science-ml` · agentes `data-science-ml:ds-eval-auditor`, `data-science-ml:ds-experiment-reviewer`, `data-science-ml:ds-inference-reviewer`, `data-science-ml:ds-leakage-auditor`, `data-science-ml:ds-model-promotion-reviewer` · skills `playbook` | — | — | publicado |
| `database-data-modeling` | Modelagem, SQL, índices, planos de execução, transações, migrações sem downtime, multi-tenant e backup para P… | database; sql; postgresql; mysql; sqlite; mongodb… | `database-data-modeling` · agentes `database-data-modeling:db-migration-planner`, `database-data-modeling:db-query-analyst`, `database-data-modeling:db-reviewer`, `database-data-modeling:db-schema-architect`, `database-data-modeling:db-security-auditor` · skills `playbook` | — | — | publicado |
| `design-engineering-kit` | Complemento opcional do ux-ui-design para designer-engenheiro: do link do Figma à UI implementada, verificada… | design-engineering; figma; figma-mcp; playwright; playwright-mcp; design-to-code… | `design-engineering-kit` · agentes `design-engineering-kit:motion-polish-reviewer`, `design-engineering-kit:ui-verifier` · skills `playbook` | — | — | publicado |
| `devops-cloud-infra` | Escreva, revise, planeje e diagnostique infraestrutura (Terraform/OpenTofu/Pulumi, Docker, Kubernetes/Helm, G… | devops; cloud; infrastructure-as-code; terraform; kubernetes; docker… | `devops-cloud-infra` · agentes `devops-cloud-infra:infra-reviewer`, `devops-cloud-infra:k8s-workload-auditor`, `devops-cloud-infra:pipeline-security-auditor`, `devops-cloud-infra:rollout-planner` · skills `playbook` | — | — | publicado |
| `ecommerce-marketplace` | Guia, skills e revisores para construir e operar lojas virtuais e marketplaces com o Claude Code: checkout se… | ecommerce; marketplace; checkout; payments; webhooks; idempotency… | `ecommerce-marketplace` · agentes `ecommerce-marketplace:arquiteto-loja`, `ecommerce-marketplace:auditor-catalogo-seo`, `ecommerce-marketplace:auditor-pagamentos-integracoes`, `ecommerce-marketplace:revisor-a11y-checkout`, `ecommerce-marketplace:revisor-checkout` · skills `playbook` | — | — | publicado |
| `engineering-lifecycle` | Ciclo de vida de engenharia com disciplina de agente, do agent-skills de Addy Osmani (MIT): DEFINE → PLAN → B… | lifecycle-completo; engineering-lifecycle; ciclo de vida de engenharia; spec-driven-development; spec antes do código; planning-and-task-breakdown… | `engineering-lifecycle` · agentes `engineering-lifecycle:code-reviewer`, `engineering-lifecycle:fresh-context-doubter`, `engineering-lifecycle:quality-bar-guardian`, `engineering-lifecycle:security-auditor`, `engineering-lifecycle:test-engineer`, `engineering-lifecycle:web-performance-auditor` · skills `playbook` | — | — | publicado |
| `fintech-payments` | Construa, revise e teste sistemas de pagamentos (Pix, boleto, cartão) com idempotência, webhooks verificados,… | fintech; payments; pagamentos; pix; boleto; idempotency… | `fintech-payments` · agentes `fintech-payments:payment-debugger`, `fintech-payments:payment-reviewer`, `fintech-payments:payment-test-engineer`, `fintech-payments:payments-architect`, `fintech-payments:reconciliation-analyst` · skills `playbook` | — | — | publicado |
| `game-development` | Playbook, skills, agentes e prompts para desenvolver, revisar, otimizar e testar jogos em Godot/GDScript, Uni… | game-development; gamedev; godot; gdscript; unity; unreal… | `game-development` · agentes `game-development:game-engine-specialist`, `game-development:game-evaluator`, `game-development:gameplay-programmer`, `game-development:gameplay-reviewer`, `game-development:gdd-reviewer` · skills `playbook` | — | — | publicado |
| `git-workflow-release` | Fluxo de git com Claude Code do commit à release: commits convencionais, PRs pequenos e revisáveis, conflitos… | git; conventional-commits; pull-request; code-review; merge-conflicts; rebase… | `git-workflow-release` · agentes `git-workflow-release:auditor-politica-repo`, `git-workflow-release:auditor-release`, `git-workflow-release:revisor-diff`, `git-workflow-release:revisor-plano` · skills `playbook` | — | — | publicado |
| `llm-ai-agents` | Playbook, skills de tarefa, subagentes somente leitura e biblioteca de prompts para projetar, revisar e testa… | llm; ai-agents; prompt-engineering; context-engineering; tool-use; mcp… | `llm-ai-agents` · agentes `llm-ai-agents:agent-architect`, `llm-ai-agents:agent-security-reviewer`, `llm-ai-agents:eval-designer`, `llm-ai-agents:prompt-reviewer`, `llm-ai-agents:rag-pipeline-reviewer` · skills `playbook` | — | — | publicado |
| `mobile-apps` | Playbook, skills, agentes e prompts para construir, revisar, depurar e publicar apps mobile (iOS/SwiftUI, And… | mobile; ios; android; swiftui; jetpack-compose; react-native… | `mobile-apps` · agentes `mobile-apps:mobile-architect`, `mobile-apps:mobile-pr-reviewer`, `mobile-apps:mobile-release-auditor`, `mobile-apps:mobile-security-auditor`, `mobile-apps:mobile-test-engineer` · skills `playbook` | — | — | publicado |
| `product-discovery-specs` | Transforma ideias e pedidos vagos em PRD enxuto, spec testável, critérios de aceite, histórias INVEST, priori… | produto-completo; product-discovery; prd; spec-driven-development; user-stories; acceptance-criteria… | `product-discovery-specs` · agentes `product-discovery-specs:decision-recorder`, `product-discovery-specs:discovery-synthesizer`, `product-discovery-specs:feasibility-scout`, `product-discovery-specs:plan-writer`, `product-discovery-specs:spec-reviewer` · skills `playbook` | — | — | publicado |
| `qa-testing` | QA e testes para o Claude Code: estratégia por risco, design de casos, TDD com vermelho confirmado, revisão d… | qa; testing; test-strategy; test-design; tdd; e2e… | `qa-testing` · agentes `qa-testing:qa-reporter`, `qa-testing:test-auditor`, `qa-testing:test-reviewer`, `qa-testing:test-writer` · skills `playbook` | — | — | publicado |
| `saas-multitenant` | Projete, implemente, revise e teste SaaS B2B multi-tenant com Claude Code: isolamento por tenant (RLS no Post… | saas; multi-tenant; tenant-isolation; row-level-security; postgres; stripe-billing… | `saas-multitenant` · agentes `saas-multitenant:billing-reviewer`, `saas-multitenant:isolation-test-engineer`, `saas-multitenant:milestone-reviewer`, `saas-multitenant:saas-architect`, `saas-multitenant:tenant-isolation-reviewer` · skills `playbook` | — | — | publicado |
| `security-appsec` | Revisão de segurança de diffs e PRs, modelagem de ameaças (STRIDE), autorização por objeto e tenant, segredos… | security; appsec; owasp; threat-modeling; stride; security-review… | `security-appsec` · agentes `security-appsec:agent-config-auditor`, `security-appsec:finding-verifier`, `security-appsec:patch-reviewer`, `security-appsec:security-reviewer`, `security-appsec:threat-modeler` · skills `playbook` | — | — | publicado |
| `sre-observability` | SLI/SLO e error budget, alertas por burn rate, telemetria (OpenTelemetry, Prometheus), triagem de incidentes … | sre; observability; slo; error-budget; burn-rate; alerting… | `sre-observability` · agentes `sre-observability:incident-support`, `sre-observability:perf-analyst`, `sre-observability:postmortem-scribe`, `sre-observability:reliability-reviewer` · skills `playbook` | — | — | publicado |
| `systems-embedded-iot` | Revisão, depuração e testes de firmware (C/C++, Rust no_std, FreeRTOS, Zephyr, ESP32/STM32) com portão humano… | embedded; firmware; iot; rtos; freertos; zephyr… | `systems-embedded-iot` · agentes `systems-embedded-iot:embedded-architect`, `systems-embedded-iot:firmware-debugger`, `systems-embedded-iot:firmware-reviewer`, `systems-embedded-iot:firmware-test-engineer`, `systems-embedded-iot:iot-security-auditor` · skills `playbook` | — | — | publicado |
| `technical-writing-docs` | Documentação técnica com Claude Code: README, tutoriais e guias (Diátaxis), ADRs, runbooks, changelog, docs d… | documentation; technical-writing; readme; diataxis; adr; runbook… | `technical-writing-docs` · agentes `technical-writing-docs:auditor-de-docs`, `technical-writing-docs:revisor-de-instrucoes`, `technical-writing-docs:revisor-de-leitor`, `technical-writing-docs:technical-writer` · skills `playbook` | — | — | publicado |
| `ux-ui-design` | Direção visual, auditoria de UI, avaliação heurística, acessibilidade WCAG 2.2 AA, design tokens, UX writing … | ux; ui; design-system; design-tokens; accessibility; wcag… | `ux-ui-design` · agentes `ux-ui-design:a11y-reviewer`, `ux-ui-design:design-evaluator`, `ux-ui-design:design-system-auditor`, `ux-ui-design:ui-designer`, `ux-ui-design:ux-researcher` · skills `playbook` | — | — | publicado |
| `web-frontend` | Guia, skills de tarefa, agentes somente leitura e biblioteca de prompts para frontend web com Claude Code (Re… | frontend; react; nextjs; vue; nuxt; svelte… | `web-frontend` · agentes `web-frontend:frontend-a11y-reviewer`, `web-frontend:frontend-code-reviewer`, `web-frontend:frontend-perf-reviewer`, `web-frontend:frontend-security-auditor`, `web-frontend:ui-evaluator` · skills `playbook` | — | — | publicado |

## Detalhes das tags curadas

### `adr-decisoes` — ADRs e documentação de decisões (publicado)

Registra decisões de arquitetura em ADR (contexto, decisão, alternativas com motivo, consequências, status e data) respeitando antes a convenção do repositório; não apaga ADR antigo, substitui; mantém README e regras de agente atualizados.

- **Gatilhos:** escreve um adr para essa decisão; documenta por que escolhemos x; registra a decisão de arquitetura; me dá um modelo de adr; como numero os adrs desse repo; substituir um adr antigo; readme para esse projeto; documenta essa api pública; write an adr for this; adr template; record why we chose this library; supersede an old adr; documentation-and-adrs

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `architecture-design` | lider | `adr`, `adr-write` | `adr-writer` | publicado |
| `engineering-lifecycle` | fundamentos | `documentation-and-adrs` | — | publicado |
| `technical-writing-docs` | apoio | `escrever-adr`, `escrever-readme` | `technical-writer` | publicado |
| `product-discovery-specs` | apoio | — | `decision-recorder` | publicado |
- **Validadores:** `technical-writing-docs:auditor-de-docs`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-29. A convenção do repositório-alvo vence; sem ela, a do brain (docs/adr, MADR) (C-12). adr-write é manual-only e só grava ADR aprovado.

### `barra-de-qualidade` — Barra de qualidade (CONSTRAINTS.md), catraca e guarda de afrouxamento (publicado)

Registra a barra do projeto num contrato versionado (piso, números com comando, métricas em catraca, exceções com dono e prazo) e vigia o diff contra o afrouxamento: supressão nova, teste pulado, limiar baixado.

- **Gatilhos:** defina nossos padrões de qualidade; crie um constraints.md; set up constraints; quality gates para o agente; o agente está pulando teste pra passar; o agente silenciou o lint; bloqueie eslint-disable no diff; o limiar de cobertura foi reduzido; trave a cobertura atual; catraca de qualidade; ratchet the coverage; check whether the diff weakened our quality bar; constraint-driven development; /constraints

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `engineering-lifecycle` | lider | `constraint-driven-development` | `quality-bar-guardian` | publicado |
| `qa-testing` | fundamentos | `tdd-guard`, `verification-gate` | — | publicado |
| `code-quality-refactoring` | apoio | `tech-debt-triage` | — | publicado |
| `devops-cloud-infra` | apoio | `gha-hardening-review` | — | publicado |
| `sre-observability` | apoio | `slo-design` | — | publicado |
- **Validadores:** `qa-testing:test-auditor`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-06, V-07. Ferramentas (Semgrep, gitleaks, osv-scanner, axe, Lighthouse, Stryker) só como proposta, instalar com confirmação (C-3). Defaults são convenções do autor. Acessibilidade em WCAG 2.2 AA. floor-guard não é executado: vira regra do agente quality-bar-guardian.

### `ci-cd-portoes` — CI/CD e portões de qualidade (publicado)

Esteira de CI em ordem de custo sem gate pulado (lint, tipos, testes, build, auditoria), falha de CI devolvida ao agente com verificação local, branch protection, segredos em cofre e pipeline abaixo de 10 minutos.

- **Gatilhos:** monta o pipeline de ci para esse repo; meu ci está lento; o ci falhou, o que faço; quais gates devo ter; configura o github actions; shift left nos testes; branch protection para main; automatizar lint e testes no pr; quem conserta o build quebrado; how do i set up ci; my pipeline keeps failing; speed up our ci; ci-cd-and-automation

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `devops-cloud-infra` | lider | `gha-hardening-review`, `secrets-review`, `deploy-infra` | `pipeline-security-auditor` | publicado |
| `engineering-lifecycle` | fundamentos | `ci-cd-and-automation` | — | publicado |
| `qa-testing` | fundamentos | `verification-gate` | — | publicado |
| `git-workflow-release` | apoio | `criar-pr` | — | publicado |
- **Validadores:** `devops-cloud-infra:infra-reviewer`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-25. O upstream não cobre SAST, secret scanning nem SBOM; o brain cobre mais em gha-hardening-review e secrets-review (Inferido pelas descrições). deploy-infra é manual-only e só por pedido explícito.

### `contexto-agente` — Contexto, regras do projeto e handoff entre sessões (publicado)

Monta o arquivo de regras do agente, decide o que carregar e o que podar (cinco níveis, poda a 75%), trata conteúdo externo como dado e fecha a sessão com um handoff de cinco campos para retomar sem perder decisões.

- **Gatilhos:** o agente está ignorando as convenções do projeto; como montar o claude.md; o agente está inventando apis; a sessão está ficando confusa; o contexto está grande, o que cortar; quando devo abrir uma sessão nova; faça um handoff da tarefa; salve o estado para retomar amanhã; context engineering; the agent keeps ignoring our conventions; write a handoff so a fresh session can pick this up; what should i record before ending the session

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `engineering-lifecycle` | lider | `context-engineering` | — | publicado |
| `llm-ai-agents` | fundamentos | `instruction-authoring` | — | publicado |
| `technical-writing-docs` | fundamentos | `auditar-claude-md` | — | publicado |
| `backend-api` | apoio | `backend-claude-md-setup` | — | publicado |
| `product-discovery-specs` | apoio | `spec-to-tasks` | — | publicado |
- **Validadores:** `technical-writing-docs:revisor-de-instrucoes`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-11. instruction-authoring, auditar-claude-md, backend-claude-md-setup e spec-to-tasks são manual-only. 75% e 2.000 linhas são heurísticas. Os cinco campos do handoff podem entrar no roteiro continuar da fábrica.

### `contrato-api` — Contrato de API, idempotência e retries seguros (publicado)

Desenha o contrato antes do código (formato de erro único, validação na fronteira, mudanças aditivas, paginação) e torna operações seguras sob retry e duplicação com chave de idempotência atômica. Erros no formato RFC 9457.

- **Gatilhos:** desenhe os endpoints dessa feature; como versionar essa api sem quebrar clientes; defina o contrato entre esses módulos; put ou patch; paginação e erros padronizados; adicione um campo sem quebrar quem consome; o webhook chegou duas vezes; como evitar cobrança duplicada; preciso de idempotency-key; o timeout não diz se passou, e agora; make this endpoint safe to retry; design the rest endpoints for this; keep the api backward compatible; api-and-interface-design

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `backend-api` | lider | `api-contract-design`, `idempotency-and-resilience` | `backend-architect` | publicado |
| `engineering-lifecycle` | fundamentos | `api-and-interface-design` | — | publicado |
| `architecture-design` | fundamentos | `api-design`, `resilience-and-consistency` | — | publicado |
| `fintech-payments` | apoio | `payment-idempotency` | — | publicado |
| `automation-integrations` | apoio | `reviewing-webhook-receivers` | — | publicado |
- **Validadores:** `backend-api:api-contract-reviewer`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-15, V-16. RFC 9457 do backend-api prevalece sobre o envelope de erro do upstream (C-2). Idempotência existe em cinco plugins: backend-api é a referência canônica.

### `definicao-de-pronto` — Definição de pronto e checklists de verificação (publicado)

Aplica a Definition of Done fixa (correção, qualidade, integração, documentação, prontidão) e os checklists de segurança, performance e acessibilidade, com evidência por item; pronto exige verificação em execução.

- **Gatilhos:** quando posso considerar isso pronto; isso está pronto de verdade; checklist antes do merge; o que falta para fechar essa tarefa; crie um critério de pronto para o projeto; gate final antes de subir; checklist de segurança, performance e acessibilidade; o que conferir antes de lançar; lista de verificação wcag; ready to merge; what's our definition of done; pre-merge checklist; definition-of-done

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `qa-testing` | lider | `verification-gate` | — | publicado |
| `engineering-lifecycle` | fundamentos | `incremental-implementation` | — | publicado |
| `ux-ui-design` | fundamentos | `a11y-checklist` | — | publicado |
| `security-appsec` | apoio | `secrets-supply-chain-review` | — | publicado |
| `web-frontend` | apoio | `perf-audit` | — | publicado |
- **Validadores:** `qa-testing:test-reviewer`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-17. definition-of-done.md e os *-checklist.md ficam em references/ do plugin (citados por incremental-implementation e shipping-and-launch). Acessibilidade em WCAG 2.2 AA. A matriz de gerenciadores do security-checklist é snapshot datado.

### `deprecacao-migracao` — Deprecação, migração e mudança de schema sem downtime (publicado)

Decide se um sistema deve ser mantido ou descontinuado (cinco perguntas, substituto antes do aviso, regra do churn) e conduz a migração sem quebrar consumidores, inclusive schema em expand/contract com down testado.

- **Gatilhos:** como removo essa api antiga; quero descontinuar essa funcionalidade; plano de deprecação; como migro os usuários para o novo serviço; devo manter esse sistema legado; código que ninguém mantém mas todo mundo usa; renomear coluna em produção sem downtime; expand e contract; backfill em lotes; posso dropar essa coluna; strangler fig; zero downtime schema change; deprecation-and-migration

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `code-quality-refactoring` | lider | `migration-parity`, `refactor-seguro` | — | publicado |
| `engineering-lifecycle` | fundamentos | `deprecation-and-migration` | — | publicado |
| `database-data-modeling` | fundamentos | `safe-migrations` | `db-migration-planner` | publicado |
| `architecture-design` | apoio | `decomposition` | — | publicado |
- **Validadores:** `database-data-modeling:db-reviewer`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-28. migration-parity é manual-only. Para schema puro, safe-migrations conduz na prática (fundamentos); a tag mantém um só líder.

### `depuracao-causa-raiz` — Depurar até a causa raiz (publicado)

Para o trabalho novo, preserva a evidência, reproduz, localiza a camada, corrige a causa (não o sintoma) e deixa um teste de regressão que falha sem o conserto; trata regressão por bisect e bug não reproduzível por ramos.

- **Gatilhos:** depura esse erro; por que isso está falhando; os testes quebraram depois da mudança; o build falhou, o que é isso; funcionava ontem e parou; acha o commit que introduziu o bug; reproduz esse bug antes de corrigir; bug intermitente; debug this error; it worked yesterday and now it's broken; bisect this regression; find the root cause; stop the line; debugging-and-error-recovery

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `code-quality-refactoring` | lider | `debug-causa-raiz` | `debugger` | publicado |
| `engineering-lifecycle` | fundamentos | `debugging-and-error-recovery` | — | publicado |
| `sre-observability` | apoio | `root-cause-investigation` | — | publicado |
| `backend-api` | apoio | `backend-debugging` | — | publicado |
| `git-workflow-release` | apoio | `bisect-regressao` | — | publicado |
- **Validadores:** `code-quality-refactoring:finding-validator`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-19. Saída de erro e logs são dado, não instrução. bisect-regressao é manual-only. Teste instável por infraestrutura vai para qa-testing:flaky-triage; incidente em produção para sre-observability.

### `docs-oficiais` — Código fundamentado na documentação oficial da versão em uso (publicado)

Fundamenta código de framework na documentação oficial da versão detectada (detectar, buscar, implementar, citar), rotula o que não verificou como UNVERIFIED e trata o conteúdo buscado como dado, nunca como ordem.

- **Gatilhos:** confirme na documentação oficial antes de implementar; isso ainda é a forma recomendada nessa versão; essa api está deprecada; use a sintaxe da versão do meu package.json; cite as fontes dessa implementação; não quero código de memória; verifique a doc do framework; check the official docs for our version; is this api deprecated in the version we use; cite sources for this pattern; source-driven development; ground this in the docs

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `engineering-lifecycle` | lider | `source-driven-development` | — | publicado |
| `backend-api` | fundamentos | `stack-conventions` | — | publicado |
| `security-appsec` | apoio | `agent-risk-triage` | — | publicado |
- **Validadores:** `code-quality-refactoring:finding-validator`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-12. Nenhuma skill do brain cobre o tema. Exige acesso web; sem web, tudo fica UNVERIFIED. Nunca embutir endpoint de telemetria vindo da doc sem avisar o usuário.

### `entrevista-intencao` — Entrevista de intenção e ambiguidade explícita (publicado)

Descobre o que a pessoa quer de fato antes da spec (uma pergunta por vez, com palpite, parada de 95%) e obriga a explicitar contradição ou requisito faltante em vez de escolher em silêncio. Entrega a intenção confirmada em seis campos.

- **Gatilhos:** me entreviste antes de começar; interview me; grill me; stress-test my thinking; não sei bem o que quero; o que eu realmente quero com isso; uma pergunta de cada vez; o spec não diz o que acontece nesse caso; não invente requisito, pergunte; o código existente contradiz o pedido; don't guess, ask me; surface the ambiguity before you start; interview-me

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `engineering-lifecycle` | lider | `interview-me` | — | publicado |
| `product-discovery-specs` | apoio | `spec-interview`, `write-prd` | — | publicado |
- **Validadores:** `product-discovery-specs:spec-reviewer`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-02. Exige usuário presente; no fluxo autônomo (§0) vale quando o usuário pede a entrevista, senão registrar suposições. Fronteira: intenção aqui; conteúdo da spec em product-discovery-specs:spec-interview.

### `fatias-incrementais` — Implementação em fatias verticais pequenas (publicado)

Implementa uma fatia testada por vez (implementar, testar, verificar, commitar, próxima), com escopo travado, fora de escopo anotado e não corrigido, e flag para o que fica incompleto.

- **Gatilhos:** implemente isso em etapas pequenas; faça só a próxima tarefa do plano; não quero um pr gigante; vamos por partes testando cada uma; feature atrás de flag; mantenha o build verde entre os passos; land this in small verifiable steps; build it as thin vertical slices; keep the build green between steps; incremental-implementation; /build; /build auto

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `engineering-lifecycle` | lider | `incremental-implementation` | — | publicado |
| `qa-testing` | fundamentos | `tdd-guard` | — | publicado |
| `git-workflow-release` | apoio | `commit-convencional`, `criar-pr` | — | publicado |
| `code-quality-refactoring` | apoio | `refactor-seguro` | — | publicado |
- **Validadores:** `git-workflow-release:revisor-plano`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-08, V-31. /build auto exige SPEC.md, árvore limpa e aprovação única; commit por tarefa só em branch local, sem push. commit-convencional e criar-pr são manual-only.

### `git-versionamento-release` — Git, commits atômicos, branches curtas e versionamento (publicado)

Commits atômicos como save points (uma coisa por commit, mensagem com o porquê), PRs de cerca de 100 linhas, branches curtas trunk-based, versão pelo impacto ao consumidor (SemVer), tag anotada e changelog curado.

- **Gatilhos:** como organizo meus commits; faça commits atômicos; faça um pr pequeno; quanto deve ter um commit; como volto ao último estado que funcionava; qual versão devo subir; escreve o changelog dessa release; gitflow ou trunk-based; minha branch está há duas semanas; main sempre deployável; git worktree para agentes em paralelo; what semver bump is this; how big should a pr be; git-workflow-and-versioning

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `git-workflow-release` | lider | `commit-convencional`, `criar-pr`, `rebase-seguro`, `release-cut`, `encerrar-branch` | `revisor-diff` | publicado |
| `engineering-lifecycle` | fundamentos | `git-workflow-and-versioning` | — | publicado |
| `technical-writing-docs` | apoio | `escrever-changelog-release` | — | publicado |
- **Validadores:** `git-workflow-release:auditor-release`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-24. git reset --hard HEAD só após git status e com o trabalho salvo ou confirmado (C-5); push e tag exigem confirmação. As skills do líder são manual-only. O vínculo com DORA no upstream é crença sem link.

### `lancamento-rollback` — Lançamento em produção: checklist, rollout em estágios e rollback (publicado)

Prepara um lançamento reversível: checklist pré-lançamento em oito grupos, flag como kill switch, rollout em estágios com limiares para avançar, segurar ou reverter, e plano de rollback escrito antes do deploy.

- **Gatilhos:** vamos subir isso para produção, o que falta; checklist antes do deploy; estamos prontos para o go-live; como fazemos o rollout gradual; canary de 5% dos usuários; quero lançar atrás de uma flag; quando remover a feature flag; qual o plano de rollback dessa release; como reverto se der errado; quando devo reverter; pre-launch checklist; are we ready to ship; shipping-and-launch; /ship

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `devops-cloud-infra` | lider | `progressive-delivery` | `rollout-planner` | publicado |
| `engineering-lifecycle` | fundamentos | `shipping-and-launch` | — | publicado |
| `sre-observability` | fundamentos | `release-health`, `slo-design` | — | publicado |
| `database-data-modeling` | apoio | `backup-restore-runbook`, `safe-migrations` | — | publicado |
| `technical-writing-docs` | apoio | `escrever-runbook` | — | publicado |
- **Validadores:** `git-workflow-release:auditor-release`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-26, V-27, V-32. Um só roteiro de canário por projeto (C-7). Limiares e tempos são exemplos do autor. O plano é documento: push, deploy e publicação exigem confirmação (§5). release-health é manual-only.

### `observabilidade-instrumentar` — Observabilidade: instrumentar, métricas RED e alertas por sintoma (publicado)

Instrumenta código novo para que o incidente seja consulta: perguntas do on-call antes dos sinais, logs estruturados com correlation ID, métricas RED e USE com labels limitados, tracing OpenTelemetry e alertas por sintoma com runbook.

- **Gatilhos:** instrumenta esse serviço; adiciona logs e métricas nessa feature; não consigo saber o que aconteceu em produção; como estruturar meus logs; adiciona tracing com opentelemetry; quais métricas devo expor; o pager toca o tempo todo; alertas por sintoma; métricas red; set up logging for this service; we can't debug prod, what should we log; symptom-based alerting; observability-and-instrumentation

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `sre-observability` | lider | `telemetry-review`, `alert-review`, `slo-design`, `runbook` | — | publicado |
| `engineering-lifecycle` | fundamentos | `observability-and-instrumentation` | — | publicado |
| `technical-writing-docs` | apoio | `escrever-runbook` | — | publicado |
- **Validadores:** `sre-observability:reliability-reviewer`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-30. Exemplos do upstream em Node e Prometheus; limiares são exemplos. Nunca logar segredo ou PII.

### `orquestracao-multiagente` — Orquestração de subagentes: padrões e anti-padrões (publicado)

Critério para orquestrar subagentes: invocação direta, comando de persona única, fan-out paralelo com merge na sessão principal, pipeline conduzido pelo usuário e isolamento de pesquisa; profundidade 1, personas não invocam personas, quatro anti-padrões.

- **Gatilhos:** orquestrar subagentes; rodar especialistas em paralelo; fan-out com merge; quando usar subagente ou agent team; agente chamando agente; router de agentes; dividir a análise entre especialistas; quem orquestra os subagentes; agent teams para debugar hipóteses; multi-agent orchestration pattern; run specialist agents in parallel; persona calls persona; orchestration-patterns

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `orchestrator` | lider | `playbook` | `demand-router` | publicado |
| `engineering-lifecycle` | fundamentos | `shipping-and-launch` | `code-reviewer`, `security-auditor`, `test-engineer` | publicado |
| `llm-ai-agents` | apoio | `agent-architecture` | — | publicado |
- **Validadores:** `llm-ai-agents:agent-security-reviewer`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-32, V-33, V-34. Reconciliação com o ORCHESTRATOR em §8 (decisão do dono). Agent Teams é experimental e não adotado. O registro de tags é dado lido pela sessão principal, não um roteador que executa.

### `performance-web` — Medir e otimizar performance (Core Web Vitals, N+1, índice, cache) (publicado)

Mede antes de otimizar (sintético e RUM p75), muda uma coisa por vez, mantém só o que supera a variância, registra as tentativas revertidas e deixa guarda de regressão. Cobre Core Web Vitals, N+1, índice, pool e cache.

- **Gatilhos:** isso está lento; otimiza a performance disso; melhora o lcp da página; core web vitals ruins; tem n+1 nessa consulta; o endpoint demora demais; o bundle está pesado; defina orçamentos de performance; auditoria de web vitals; profile this; the page is slow; set performance budgets; performance-optimization; /webperf

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `web-frontend` | lider | `perf-audit` | `frontend-perf-reviewer` | publicado |
| `engineering-lifecycle` | fundamentos | `performance-optimization` | `web-performance-auditor` | publicado |
| `sre-observability` | apoio | `performance-engineering` | — | publicado |
| `database-data-modeling` | apoio | `query-plan-and-indexing` | — | publicado |
- **Validadores:** `sre-observability:perf-analyst`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-23. Nunca fabricar métrica: valor com fonte rotulada (Field, Lab, Trace) ou not measured. O modo Deep do upstream usa npx: só com versão fixada e confirmação, ou JSON fornecido pelo usuário (C-4). CRUX_API_KEY nunca no plugin.

### `pesquisa-web-apify` — Pesquisa e coleta de dados na web em escala (Apify MCP) (em construção)

Pesquisar fontes em massa, raspar e extrair dados de sites e redes sociais com Actors do Apify via MCP, com teto de gasto aprovado pelo usuário, uso responsável e conteúdo coletado tratado como dado. Alimenta o método de pesquisa da fábrica.

- **Gatilhos:** pesquisa na web em escala; pesquisar fontes em massa; raspar dados; web scraping; coletar dados de sites; crawler; apify; actor do apify; pesquisar no reddit; transcrição de youtube; serp; scrape reddit; scrape this site; collect data from the web; apify-completo

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `web-research-apify` | lider | `playbook`, `escolher-actor`, `dataset-para-itens` | `apify-researcher` | em construção |
| `automation-integrations` | fundamentos | `responsible-scraping`, `assessing-automation-risk` | `third-party-auditor` | publicado |
| `security-appsec` | apoio | `agent-risk-triage` | `agent-config-auditor` | publicado |
| `llm-ai-agents` | apoio | `tool-design-review` | `agent-security-reviewer` | publicado |
- **Validadores:** `web-research-apify:apify-source-verifier`, `web-research-apify:apify-cost-auditor`, `automation-integrations:third-party-auditor`
- **Fontes:** `docs/dev-segments/research/web-research-apify/VALIDATED.md`, `docs/dev-segments/research/web-research-apify/SYNTHESIS.md`
- **Notas:** Rota gratuita primeiro: scraping com código próprio ou de página estática fica com automation-integrations:responsible-scraping, sem Apify; Apify só quando a rota gratuita falha (bloqueio, JavaScript, sem API). Sem .mcp.json ativo: a conexão (mcp.apify.com, OAuth) é feita pelo usuário com confirmação. pesquisa-com-orcamento só roda por comando (gasta dinheiro). Despachado como general-purpose, o agente não herda tools: repetir orçamento, ferramentas e regras no prompt (P-21).

### `quebrar-em-tarefas` — Quebrar a spec em tarefas verticais e verificáveis (publicado)

Converte a spec aprovada em plano e tarefas pequenas, cada uma com critério de aceite, verificação, dependências e tamanho; checkpoints a cada 2 ou 3 tarefas e paralelismo explícito.

- **Gatilhos:** quebre em tarefas; faça o plano de implementação; divida isso em tarefas; break this into tasks; plan the implementation; tarefas verticais; quais tarefas podem rodar em paralelo; monte o tasks/plan.md; isso é uma tarefa ou duas; tarefas pequenas o bastante para uma sessão; coloque checkpoints entre as fases; task list with acceptance criteria; planning-and-task-breakdown; /plan

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `product-discovery-specs` | lider | `spec-to-tasks`, `refine-backlog` | `plan-writer` | publicado |
| `engineering-lifecycle` | fundamentos | `planning-and-task-breakdown` | — | publicado |
| `architecture-design` | apoio | `decomposition` | — | publicado |
| `qa-testing` | apoio | `test-design` | — | publicado |
- **Validadores:** `product-discovery-specs:spec-reviewer`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-05. spec-to-tasks é manual-only e exige spec aprovada (gate G1). Convenção T001/REQ/TASK do brain prevalece (C-10); não sobrescrever plano com tarefas abertas.

### `refinar-ideia` — Refinar uma ideia: divergir, convergir e cortar (publicado)

Transforma ideia vaga em direção escolhida: reformula como How Might We, diverge com lentes, converge em 2 a 3 direções, expõe premissas e entrega um one-pager com MVP e lista Not Doing.

- **Gatilhos:** refine essa ideia; refine this idea; ideate on; me ajuda a refinar essa ideia; gera variações disso; quais outras abordagens existem; o que eu deixaria de fora; monte a lista do que não faremos; transforme isso num one-pager; how might we; brainstorm the options; expand options before i choose; idea-refine

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `engineering-lifecycle` | lider | `idea-refine` | — | publicado |
| `product-discovery-specs` | apoio | `run-discovery`, `prioritize-roadmap` | `decision-recorder`, `feasibility-scout` | publicado |
- **Validadores:** `architecture-design:skeptic-architect`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-03. O brain cobre descoberta com usuários e priorização, não divergência por lentes nem Not Doing obrigatória. O one-pager só vai para docs/ideas/ com confirmação.

### `revisao-de-codigo` — Revisão de código antes do merge (publicado)

Revisa a mudança em cinco eixos (correção, legibilidade, arquitetura, segurança, performance) com rótulos de severidade, arquivo:linha, mutação manual e limite de tamanho da mudança.

- **Gatilhos:** revisa esse pr; faz o code review desse diff; posso mergear isso; revisa minhas mudanças antes do merge; dá uma olhada nesse diff; revisão em cinco eixos; code review com severidade crítico e nit; mudança grande demais, como dividir o pr; review this before i merge; code review this pr; review my diff; five-axis review; code-review-and-quality; /review

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `code-quality-refactoring` | lider | `review-diff` | `code-reviewer` | publicado |
| `engineering-lifecycle` | fundamentos | `code-review-and-quality` | `code-reviewer` | publicado |
| `security-appsec` | apoio | `security-review-diff` | — | publicado |
| `git-workflow-release` | apoio | `criar-pr` | `revisor-diff` | publicado |
- **Validadores:** `code-quality-refactoring:finding-validator`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-20. Rótulos divergem entre skill e persona: adotar um conjunto com arquivo:linha (C-8). A mutação manual altera arquivo: fazer em cópia ou worktree (C-15).

### `revisao-por-duvida` — Revisão por dúvida em contexto novo e triagem de achados (publicado)

Submete decisões não triviais a um revisor adversarial em contexto novo (só artefato e contrato, nunca a conclusão), classifica os achados em quatro classes e para em três rodadas. Quem orquestra é a sessão principal.

- **Gatilhos:** revise isso antes de eu confiar; faça uma revisão adversarial; encontre o que pode dar errado nesse plano; questione minhas suposições; dê uma segunda opinião com contexto limpo; prove que esse código está errado; o revisor disse isso, procede; separe o que é real do que é ruído nos achados; é falso positivo; play devil's advocate on this design; what could go wrong with this migration; fresh-context review; doubt-driven development; triage these review findings

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `engineering-lifecycle` | lider | `doubt-driven-development` | `fresh-context-doubter` | publicado |
| `architecture-design` | apoio | `design-review` | `skeptic-architect` | publicado |
| `security-appsec` | apoio | — | `finding-verifier` | publicado |
- **Validadores:** `code-quality-refactoring:finding-validator`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-13. Só a sessão principal dispara o DOUBT (profundidade 1); a skill não entra no skills: de persona. CLI externa (codex, gemini) só com confirmação e em modo leitura (C-16). Há seis revisores céticos no brain; o ganho é o protocolo comum.

### `roteador-de-fases` — Roteador de fases do ciclo de engenharia (publicado)

Decide em que fase do ciclo (definir, planejar, construir, verificar, revisar, entregar) o trabalho está e qual skill ou comando do engineering-lifecycle se aplica. É fundamentos do orquestrador, não um segundo roteador ativo.

- **Gatilhos:** qual skill usar; por onde começo essa tarefa; em que fase do ciclo estou; qual é o próximo passo do ciclo; me guie pelas fases; qual comando usar agora; ciclo de vida da entrega; spec, plan, build, review, ship; which skill applies; where do i start with this feature; walk me through the lifecycle; what's the next step in the lifecycle; using-agent-skills; lifecycle-completo

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `orchestrator` | lider | `playbook` | `demand-router` | publicado |
| `engineering-lifecycle` | fundamentos | `using-agent-skills` | — | publicado |
| `automation-integrations` | apoio | `authoring-plugin-skills` | — | publicado |
- **Validadores:** `llm-ai-agents:prompt-reviewer`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-01, V-31, V-35, V-36. Um só roteador ativo: o registro de tags lido pela sessão principal. using-agent-skills entra como fundamentos (o upstream desaconselha dois roteadores). Sequência pensada para código; não cobre dados, ML ou embarcados.

### `seguranca-hardening` — Segurança: modelagem de ameaças, endurecimento e fronteiras de aprovação (publicado)

Modela ameaças antes dos controles, aplica a regra de três camadas (sempre, pedir antes, nunca), protege caminhos destrutivos derivados de dados e trata saída de LLM e dependências como entrada não confiável.

- **Gatilhos:** isso é seguro; revisa a segurança disso; audita as vulnerabilidades; endurece esse endpoint; tem injeção aqui; faça uma modelagem de ameaças; posso mexer na autenticação; o que exige aprovação antes de mudar a segurança; checa o caminho antes de deletar; nunca commitar segredo; security review this; harden this endpoint; threat model this feature; owasp check; security-and-hardening

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `security-appsec` | lider | `security-review-diff`, `threat-model`, `secrets-supply-chain-review`, `harden-claude-code`, `agent-risk-triage` | `security-reviewer`, `threat-modeler` | publicado |
| `engineering-lifecycle` | fundamentos | `security-and-hardening` | `security-auditor` | publicado |
| `backend-api` | apoio | `api-security-review` | — | publicado |
| `llm-ai-agents` | apoio | `agent-security-review` | `agent-security-reviewer` | publicado |
- **Validadores:** `security-appsec:finding-verifier`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-22. PoC descritivo, sem payload operacional e sem execução (C-6). A matriz de scripts de dependência é snapshot datado. OAuth e JWT não são cobertos pelo upstream.

### `simplificar-codigo` — Simplificar código sem mudar o comportamento (publicado)

Simplifica entendendo antes de tocar (Chesterton's Fence), uma mudança por vez com testes intactos, refatoração em commit separado e automação acima de 500 linhas afetadas.

- **Gatilhos:** simplifica esse código; deixa isso mais legível; esse código está complicado demais; refatora sem mudar o comportamento; tira o aninhamento e o código morto; posso apagar esse código; clean up this code; make this more readable; simplify this without changing behavior; chesterton's fence; code-simplification; /code-simplify

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `code-quality-refactoring` | lider | `simplify-safe`, `refactor-seguro`, `tech-debt-triage` | — | publicado |
| `engineering-lifecycle` | fundamentos | `code-simplification` | — | publicado |
| `qa-testing` | apoio | `test-design` | — | publicado |
- **Validadores:** `qa-testing:test-auditor`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-21. Não adotar o hook simplify-ignore (altera arquivos na leitura). Não simplificar código de performance crítica sem medição.

### `spec-antes-do-codigo` — Spec antes do código, com aprovação (publicado)

Escreve e aprova a spec (seis áreas, Boundaries Always, Ask first e Never, critérios testáveis) antes do plano e do código; propõe mapa de capacidades quando o pedido agrupa módulos independentes.

- **Gatilhos:** escreva a spec antes; write a spec first; faça um prd; spec antes do código; não codar antes de ter spec; documente os requisitos antes de implementar; quero um spec.md; divida em módulos antes da spec; spec com always, ask first e never; template de spec; write the requirements before coding; spec-driven development; /spec

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `product-discovery-specs` | lider | `write-spec`, `write-prd`, `spec-interview`, `acceptance-criteria` | — | publicado |
| `engineering-lifecycle` | fundamentos | `spec-driven-development` | — | publicado |
| `architecture-design` | apoio | `decomposition` | — | publicado |
| `qa-testing` | apoio | `test-strategy` | — | publicado |
- **Validadores:** `product-discovery-specs:spec-reviewer`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-04. IDs FR-/SC- do brain prevalecem sobre Success Criteria em prosa (C-11); SPEC-<id>.md só com mapa de capacidades aprovado. Parar o turno após a spec.

### `tdd` — TDD, pirâmide e padrões de teste (publicado)

Escreve o teste antes do código e, em bug, o teste de reprodução que falha antes do conserto (Prove-It); escolhe o nível do teste pelo recurso que consome e aplica AAA, DAMP e dublê só na fronteira.

- **Gatilhos:** faça isso com tdd; escreva o teste antes do código; crie um teste que reproduza esse bug antes de corrigir; red green refactor; prove-it; teste de regressão para esse bug; qual a proporção entre testes unitários e de integração; pirâmide de testes; devo mockar isso; meus testes quebram quando refatoro; write a failing test first; test pyramid; test-driven-development; /test

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `qa-testing` | lider | `tdd-guard`, `test-design`, `test-strategy`, `flaky-triage` | `test-writer`, `test-reviewer` | publicado |
| `engineering-lifecycle` | fundamentos | `test-driven-development` | `test-engineer` | publicado |
| `web-frontend` | apoio | `e2e-tests` | — | publicado |
| `backend-api` | apoio | `api-test-suite` | — | publicado |
- **Validadores:** `qa-testing:test-auditor`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-09, V-10. Desempate com testes-funcionais-playwright: aqui é desenho e estilo de teste; lá, validação funcional com evidência. A persona test-engineer, sem shell, não confirma a falha.

### `testes-funcionais-playwright` — Validação funcional, funcionalidade por funcionalidade, com Playwright (em construção)

Inventariar as funcionalidades do sistema, montar a matriz, explorar o app rodando e codificar specs Playwright por funcionalidade (E2E, API, visual, acessibilidade, responsivo, rede e falhas) com evidência: trace, screenshot e relatório HTML. Em UI nativa mobile, registra N/A com motivo e usa o equivalente, mantendo a mesma matriz.

- **Gatilhos:** testar funcionalidade por funcionalidade; validar cada funcionalidade; abrir o app e validar; validação funcional; matriz de funcionalidades; inventário de funcionalidades; testes de ponta a ponta; testes e2e; end-to-end; testar no navegador; automação de testes web; playwright; playwright mcp; playwright cli; healer; trace viewer; e2e tests; browser tests; functional validation; test every feature; feature by feature validation; playwright-completo

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `qa-playwright` | lider | `playbook`, `feature-inventory`, `explore-feature`, `write-specs` | `feature-explorer`, `spec-writer`, `spec-reviewer`, `failure-triager`, `matrix-auditor` | em construção |
| `qa-testing` | fundamentos | `e2e-review`, `test-strategy`, `verification-gate` | `test-auditor`, `test-writer` | publicado |
| `web-frontend` | fundamentos | `e2e-tests`, `verify-ui` | `ui-evaluator` | publicado |
| `engineering-lifecycle` | fundamentos | `browser-testing-with-devtools`, `test-driven-development` | `test-engineer` | publicado |
| `design-engineering-kit` | apoio | `playbook` | `ui-verifier` | publicado |
- **Validadores:** `qa-playwright:matrix-auditor`, `qa-testing:test-auditor`
- **Fontes:** `docs/dev-segments/research/qa-playwright/VALIDATED.md`, `docs/dev-segments/research/qa-playwright/SYNTHESIS.md`
- **Notas:** Passo obrigatório do ORCHESTRATOR §3.2 em toda rodada de teste com superfície web ou HTTP. Exploração com `npx playwright cli` da versão fixada do projeto (sem @latest, sem .mcp.json). Preparo pré-autorizado pelo dono: @playwright/test exato como devDependency na branch local, harness e2e-playwright/, Chromium no cache só sem Chrome/Edge. Exigem confirmação: --with-deps/admin, plugin ou MCP no Claude Code, init-agents, outras dependências, produção. UI nativa Android/iOS: N/A com equivalente (Compose/Espresso/UI Automator, exploração por adb).

### `ui-producao` — UI de produção: acessível, responsiva e verificada no navegador (publicado)

Constrói telas e componentes de produção (estados completos, teclado, responsivo, sem estética genérica de IA) e verifica no navegador com DevTools: console limpo, rede, DOM, screenshots antes e depois. Alvo de acessibilidade WCAG 2.2 AA.

- **Gatilhos:** monte esse componente; crie essa tela responsiva; isso parece feito por ia, melhore; faça o formulário acessível; estados de carregando, vazio e erro; tem erro no console da página; inspecione as requisições de rede dessa ação; tire screenshot antes e depois da mudança; chrome devtools; devtools mcp; this ui looks generic; check console errors and network calls in the browser; frontend-ui-engineering; browser-testing-with-devtools

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `web-frontend` | lider | `design-ui`, `component-review`, `a11y-review`, `verify-ui` | `frontend-a11y-reviewer`, `frontend-code-reviewer` | publicado |
| `engineering-lifecycle` | fundamentos | `frontend-ui-engineering`, `browser-testing-with-devtools` | — | publicado |
| `ux-ui-design` | fundamentos | `a11y-checklist`, `design-tokens` | — | publicado |
| `design-engineering-kit` | apoio | `design-taste-frontend`, `minimalist-ui` | — | publicado |
- **Validadores:** `web-frontend:ui-evaluator`
- **Fontes:** `docs/dev-segments/research/engineering-lifecycle/VALIDATED.md`
- **Notas:** V-14, V-18. Desempate com testes-funcionais-playwright: aqui, construção e inspeção interativa; lá, suítes por funcionalidade. MCP chrome-devtools não vem ativo: versão fixada e confirmação (C-4); perfil isolado; --autoConnect só com autorização. WCAG 2.2 AA (C-1).

### `video-edicao` — Edição e produção de vídeo com código (HyperFrames) (em construção)

Criar, editar e renderizar vídeos por código: roteiro, cenas, animação, legendas, narração e render local, seguindo o playbook do HyperFrames. Entrega o vídeo renderizado ou o projeto pronto para renderizar, com o toolchain conferido.

- **Gatilhos:** edição de vídeo; editar vídeo; editar um vídeo; montar um vídeo; criar um vídeo; produzir um vídeo; renderizar vídeo; vídeo explicativo; vídeo demo do produto; motion graphics; animação em vídeo; legendas e cortes; video editing; edit a video; render a video; explainer video; hyperframes

| Plugin | Papel | Skills | Agentes | Status |
|---|---|---|---|---|
| `video-hyperframes` | lider | `playbook` | — | em construção |
| `design-engineering-kit` | apoio | `animate`, `animation-vocabulary`, `review-animations` | `motion-polish-reviewer` | publicado |
| `ux-ui-design` | apoio | `design-brief`, `ux-writing` | `design-evaluator` | publicado |
- **Validadores:** `design-engineering-kit:motion-polish-reviewer`
- **Fontes:** `docs/dev-segments/research/video-hyperframes/VALIDATED.md`
- **Notas:** Plugin em construção por outra sessão (item 30 do plano da fábrica). Render local exige Node 22+ e FFmpeg; instalação só com confirmação do usuário. O status desta tag muda sozinho quando o plugin for publicado.
