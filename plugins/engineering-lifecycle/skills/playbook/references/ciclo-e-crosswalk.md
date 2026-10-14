# Ciclo e crosswalk com o brain

Uma linha por skill (25), depois as 4 personas, os 9 comandos, os 2 agentes próprios e os conflitos que o bloco de precedência resolve. Base: pesquisa validada em 2026-10-13 (`docs/research/engineering-lifecycle/VALIDATED.md`, itens V-01 a V-37). Fonte do upstream: addyosmani/agent-skills (MIT), commit `aeac41d4d005999432bb7312f7ff06383a91d59d`.

**Limite de confiança.** A coluna "O brain já tinha" vem do `frontmatter` e da descrição dos itens do brain, conferidos por listagem de arquivos; o corpo deles não foi relido nesta construção. Para o conteúdo interno, trate como **Inferido**. A coluna "O upstream acrescenta" vem da leitura das skills vendorizadas (Verificado nos pontos com linha citada no VALIDATED). Os papéis (líder, fundamentos, apoio) vêm de `docs/foundation/knowledge/*.json`.

## 1. As 25 skills

As skills ficam em `../../<nome>/SKILL.md` (por exemplo [using-agent-skills](../../using-agent-skills/SKILL.md)). Plugins do brain no formato `plugin:skill`.

| Fase | Skill | Comando | Tag (papel deste plugin) | Plugin do brain (líder e apoios) | O upstream acrescenta | O brain já tinha |
| --- | --- | --- | --- | --- | --- | --- |
| Todas | using-agent-skills | | `roteador-de-fases` (fundamentos) | `orchestrator:playbook` + agente `demand-router` (líder) | Sequência de 16 passos, seis comportamentos, dez failure modes | Roteamento por tags (ORCHESTRATOR §3) e `demand-router`; `product-discovery-specs:playbook` como entrada de definir |
| DEFINE | interview-me | | `entrevista-intencao` (líder) | `product-discovery-specs:spec-interview`, `write-prd` (apoio) | Hipótese com confiança, uma pergunta por vez com palpite, parada de 95%, restate em seis campos | `spec-interview` (entrevista até SPEC.md aprovado), `write-prd` (até 3 perguntas) |
| DEFINE | idea-refine | | `refinar-ideia` (líder) | `product-discovery-specs:run-discovery`, `prioritize-roadmap`; agentes `decision-recorder`, `feasibility-scout` (apoio) | Divergência por lentes, lista Not Doing obrigatória, one-pager | Descoberta com usuários (JTBD, árvore de oportunidades), priorização, registro de "não faremos" |
| DEFINE | spec-driven-development | `spec` | `spec-antes-do-codigo` (fundamentos) | `product-discovery-specs:write-spec`, `write-prd`, `spec-interview`, `acceptance-criteria` (líder) | Gate "não avance", Phase 0 (mapa de capacidades), spec em seis áreas, Boundaries Always/Ask first/Never | `write-spec` (P1/P2/P3, FR-NNN, SC-NNN, `[NEEDS CLARIFICATION]`); `qa-testing:test-strategy`; `architecture-design:decomposition` |
| DEFINE | constraint-driven-development | `constraints` | `barra-de-qualidade` (líder) | `qa-testing:tdd-guard`, `verification-gate`; `code-quality-refactoring:tech-debt-triage`; `devops-cloud-infra:gha-hardening-review`; `sre-observability:slo-design` | `CONSTRAINTS.md` versionado com catraca, guarda de diff (floor-guard), checagem posicionada por custo | Peças soltas por dimensão; nenhum contrato único versionado |
| PLAN | planning-and-task-breakdown | `plan` | `quebrar-em-tarefas` (fundamentos) | `product-discovery-specs:spec-to-tasks`, `refine-backlog`; agente `plan-writer` (líder) | Fatias verticais, tamanhos XS a XL por arquivos, checkpoints a cada 2 a 3 tarefas, não sobrescrever plano aberto | `spec-to-tasks` (T001 [P] [US1], gate G1, briefing de sessão nova; manual-only), `refine-backlog` (INVEST) |
| BUILD | incremental-implementation | `build` | `fatias-incrementais` (líder), `definicao-de-pronto` (fundamentos) | `qa-testing:tdd-guard`; `git-workflow-release:commit-convencional`, `criar-pr`; `code-quality-refactoring:refactor-seguro` | Menor fatia ponta a ponta, ~100 linhas, anotar o fora de escopo, commit por fatia | `tdd-guard` (test-first em fatias verticais); `refine-backlog` fatia backlog, não implementação |
| BUILD | context-engineering | | `contexto-agente` (líder) | `llm-ai-agents:instruction-authoring`, `technical-writing-docs:auditar-claude-md` (fundamentos); `backend-api:backend-claude-md-setup` | Hierarquia de cinco níveis, confiança por origem, handoff de cinco campos, gestão de confusão | `instruction-authoring` e `auditar-claude-md` (manual-only); `spec-to-tasks` (briefing); `git-workflow-release:encerrar-branch` |
| BUILD | source-driven-development | | `docs-oficiais` (líder) | `backend-api:stack-conventions` (fundamentos); `security-appsec:agent-risk-triage` (apoio) | DETECT, FETCH, IMPLEMENT, CITE; `UNVERIFIED`; segurança na recuperação de doc | Nenhuma skill cobre o tema; `stack-conventions` (convenções da versão instalada); `agent-risk-triage` (conteúdo externo é dado) |
| BUILD | doubt-driven-development | | `revisao-por-duvida` (líder) | `architecture-design:skeptic-architect`; `security-appsec:finding-verifier`; também `code-quality-refactoring:finding-validator`, `product-discovery-specs:spec-reviewer`, `git-workflow-release:revisor-plano` | Protocolo comum: ARTIFACT + CONTRACT sem a CLAIM, prompt adversarial, RECONCILE em quatro classes, parada em três ciclos | Seis variantes do mesmo gesto, todas somente leitura, cada uma com seu domínio |
| BUILD | frontend-ui-engineering | | `ui-producao` (fundamentos) | `web-frontend:design-ui`, `component-review`, `a11y-review`, `verify-ui` (líder); `ux-ui-design:a11y-checklist`, `design-tokens` | Estados carregando, vazio, erro, sucesso; mobile-first em 320, 768, 1024, 1440 px | `a11y-review` e `a11y-checklist` com WCAG 2.2 AA; `verify-ui` abre a tela em 320 px e desktop |
| BUILD | api-and-interface-design | | `contrato-api` (fundamentos) | `backend-api:api-contract-design`, `idempotency-and-resilience` (líder); `architecture-design:api-design` | Contrato antes do código, One-Version Rule, Hyrum's Law, idempotência (422, 409, 202) | `api-contract-design` (OpenAPI 3.1, RFC 9457, cursor); `idempotency-and-resilience` (chave atômica, HMAC, DLQ, outbox) |
| VERIFY | test-driven-development | `test` | `tdd` (fundamentos) | `qa-testing:tdd-guard`, `test-design`, `test-strategy`, `flaky-triage`; agentes `test-writer`, `test-reviewer` (líder) | Prove-It como ritual, descobrir o comando de teste do repo, real > fake > stub > mock, pirâmide e tamanhos | `tdd-guard` (test-first, vermelho pelo motivo certo, mutation check) |
| VERIFY | browser-testing-with-devtools | `test` (UI) | `ui-producao`, `testes-funcionais-playwright` (fundamentos) | `web-frontend:verify-ui`; `qa-playwright:playbook`; `design-engineering-kit:ui-verifier`; `qa-testing:e2e-review` | Verificação em runtime pelo MCP `chrome-devtools`; DOM, console e rede como dados não confiáveis | `verify-ui`; `ui-verifier` (Playwright MCP) |
| VERIFY | debugging-and-error-recovery | | `depuracao-causa-raiz` (fundamentos) | `code-quality-refactoring:debug-causa-raiz` + agente `debugger` (líder); `git-workflow-release:bisect-regressao`; `backend-api:backend-debugging`; `sre-observability:root-cause-investigation` | Stop-the-line em seis passos, ramos de não reproduzível, saída de erro como dado | `debug-causa-raiz` (regressão vista falhar e depois passar); `bisect-regressao` (manual-only) |
| REVIEW | code-review-and-quality | `review` | `revisao-de-codigo` (fundamentos) | `code-quality-refactoring:review-diff` + agentes `code-reviewer`, `finding-validator` (líder); `security-appsec:security-review-diff`; `git-workflow-release:criar-pr` | Cinco eixos, mutação manual, tamanhos 100/300/1000, rótulos de severidade | `review-diff` (somente leitura, `arquivo:linha`, valida cada achado) |
| REVIEW | code-simplification | `code-simplify` | `simplificar-codigo` (fundamentos) | `code-quality-refactoring:simplify-safe`, `refactor-seguro`, `tech-debt-triage` (líder) | Cerca de Chesterton, Rule of 500, lista de padrões concretos | `simplify-safe` (mesma saída de teste antes e depois) |
| REVIEW | security-and-hardening | persona `security-auditor` | `seguranca-hardening` (fundamentos) | `security-appsec:security-review-diff`, `threat-model`, `secrets-supply-chain-review`, `harden-claude-code`, `agent-risk-triage` (líder); `backend-api:api-security-review`; `llm-ai-agents:agent-security-review` | Três camadas, caminho destrutivo derivado de dados, scripts de instalação bloqueados até revisão | Cobertura ampla e sobreposta; este plugin fica só em fundamentos |
| REVIEW | performance-optimization | `webperf` | `performance-web` (fundamentos) | `web-frontend:perf-audit` + agente `frontend-perf-reviewer` (líder); `sre-observability:performance-engineering`; `database-data-modeling:query-plan-and-indexing` | Keep/Revert estrito (neutro = reverter), ledger de tentativas, Quick e Deep honestos | `perf-audit` (evidência medida; LCP, INP, CLS; remedir nas mesmas condições) |
| SHIP | git-workflow-and-versioning | | `git-versionamento-release` (fundamentos) | `git-workflow-release:commit-convencional`, `criar-pr`, `rebase-seguro`, `release-cut`, `encerrar-branch` (líder) | Save point, trunk-based, resumo final com bloco "não toquei" | Skills manual-only; agentes `revisor-diff`, `auditor-release` |
| SHIP | ci-cd-and-automation | | `ci-cd-portoes` (fundamentos) | `devops-cloud-infra:gha-hardening-review`, `secrets-review`, `deploy-infra` (líder) | Esteira em ordem de custo, Build Cop, nenhum gate pulado | `gha-hardening-review` (pin por SHA, permissions mínimas, OIDC); cobre mais que o upstream (Inferido pela descrição) |
| SHIP | deprecation-and-migration | | `deprecacao-migracao` (fundamentos) | `code-quality-refactoring:migration-parity`, `refactor-seguro` (líder); `database-data-modeling:safe-migrations` | Churn Rule, código zumbi, cinco perguntas antes de deprecar | `safe-migrations` (expand/contract, backfill em lotes, ensaio em cópia); `decomposition` (strangler) |
| SHIP | documentation-and-adrs | | `adr-decisoes` (fundamentos) | `architecture-design:adr`, `adr-write` (líder); `technical-writing-docs:escrever-adr`, `escrever-readme` | Convenção do repositório primeiro; ciclo Proposed, Accepted, Superseded | `adr` (MADR em `docs/adr`, imutável após aceito) |
| SHIP | observability-and-instrumentation | | `observabilidade-instrumentar` (fundamentos) | `sre-observability:telemetry-review`, `alert-review`, `slo-design`, `runbook` (líder) | Perguntas do on-call viram sinal, campo de ponto de entrada, alerta por sintoma | `telemetry-review` (cardinalidade, OTel Collector); `alert-review` (burn rate multijanela) |
| SHIP | shipping-and-launch | `ship` | `lancamento-rollback`, `orquestracao-multiagente` (fundamentos) | `devops-cloud-infra:progressive-delivery` + agente `rollout-planner` (líder); `sre-observability:release-health`, `slo-design`; `database-data-modeling:backup-restore-runbook` | Checklist em oito grupos, rollback antes do GO, limiares de rollout em estágios | `progressive-delivery` (blue-green, canário, critérios de rollout e rollback antes do deploy) |

## 2. As 4 personas

As personas ficam como estão (em inglês). **Nenhuma declara `tools` nem `model`**: só `name` e `description`. No brain, revisores são somente leitura por instrução no prompt (SKILL.md, "Como usar com o orquestrador"). Todas terminam com a seção Composition: "não invoque outra persona; recomende no relatório".

| Persona | Papel | Acionada por | Equivalente no brain |
| --- | --- | --- | --- |
| [code-reviewer](../../../agents/code-reviewer.md) | Revisão em cinco eixos; veredito APPROVE ou REQUEST CHANGES | `/ship` (fan-out); direto | `code-quality-refactoring:code-reviewer`, `review-diff` |
| [security-auditor](../../../agents/security-auditor.md) | Vulnerabilidades, STRIDE por fronteira, severidade com ação | `/ship`; direto | `security-appsec:security-reviewer`, `security-review-diff` |
| [test-engineer](../../../agents/test-engineer.md) | Estratégia de teste e análise de lacunas de cobertura | `/ship`; direto; `/test` usa a skill, não a persona | `qa-testing:test-writer`, `test-reviewer`, `test-auditor` |
| [web-performance-auditor](../../../agents/web-performance-auditor.md) | Core Web Vitals, modos Quick e Deep, scorecard com fonte rotulada | `/webperf` (fora do `/ship`) | `web-frontend:frontend-perf-reviewer`, `perf-audit` |

## 3. Os 9 comandos

Fórmula do upstream: **comando = skill + regra de parada + formato de saída**. Prefixo `/engineering-lifecycle:`.

| Comando | Skill que invoca | Parada | Equivalente no brain (aproximado) |
| --- | --- | --- | --- |
| `spec` | spec-driven-development | Confirmação da spec antes do plano | `spec-interview`, `write-spec` |
| `plan` | planning-and-task-breakdown | Não sobrescreve plano com tarefas abertas | `spec-to-tasks` |
| `build` | incremental-implementation + test-driven-development | Uma tarefa; `build auto` com spec, árvore limpa e "sim" único | `qa-testing:tdd-guard` |
| `test` | test-driven-development | Suíte completa verde; Prove-It em bug | `qa-testing:test-design` |
| `review` | code-review-and-quality | Veredito com `arquivo:linha` | `code-quality-refactoring:review-diff` |
| `code-simplify` | code-simplification | Reverte a mudança que quebra teste | `simplify-safe` |
| `constraints` | constraint-driven-development | Máx. quatro perguntas; `check`, `guard`, `ratchet` | `qa-testing:verification-gate` |
| `webperf` | persona web-performance-auditor | Relatório único, sem merge | `web-frontend:perf-audit` |
| `ship` | shipping-and-launch + 3 personas | GO ou NO-GO; rollback antes de qualquer GO | `git-workflow-release:release-cut`, `rollout-planner` |

O `/ship` do upstream não tem validador independente por achado nem deduplicação com IDs de origem; o brain tem (ORCHESTRATOR §3.1 e §3 passo 6). No brain, use o `/ship` como base e acrescente essas duas etapas.

## 4. Agentes próprios deste plugin

| Agente | Papel | Ferramentas |
| --- | --- | --- |
| [`engineering-lifecycle:fresh-context-doubter`](../../../agents/fresh-context-doubter.md) | Revisor adversarial de artefato sem dono (decisão, plano, afirmação). Recebe ARTIFACT e CONTRACT, nunca a CLAIM | `Read, Grep, Glob` |
| [`engineering-lifecycle:quality-bar-guardian`](../../../agents/quality-bar-guardian.md) | Aplica as regras do floor-guard ao diff que a sessão principal passa; `LIMPO`, `VIOLAÇÃO` ou `NÃO RODOU` por regra | `Read, Grep, Glob` |

Não substituem `finding-validator`, `skeptic-architect`, `finding-verifier` nem `test-auditor`; para spec, segurança, arquitetura e diff de código, a sessão principal prefere o cético do domínio.

## 5. Conflitos e precedência

A regra do brain prevalece. O bloco de dez linhas do SKILL.md resume; esta tabela guarda a origem.

| # | Tema | Upstream | Brain | Vale |
| --- | --- | --- | --- | --- |
| C-1 | WCAG | 2.1 AA | 2.2 AA | 2.2 AA; o alvo de toque de 44 px do upstream é mais estrito que o mínimo da 2.2 e pode ficar |
| C-2 | Erro de API | Envelope próprio `{error:{code,message,details}}` | RFC 9457, `application/problem+json` | RFC 9457, um formato só |
| C-3 | Instalar ferramentas | `/constraints` instala oito ferramentas e edita `package.json` | Sem instalar sem confirmação | Proposta com comandos; instala só com confirmação |
| C-4 | MCP e `npx` | `chrome-devtools-mcp@latest` com `-y`; `npx lighthouse` | Sem `.mcp.json` ativo; MCP documentado | Versão fixada e confirmação; perfil isolado; ou JSON fornecido |
| C-5 | `git reset --hard HEAD` | Recuperação sem ressalva | Ação destrutiva pede confirmação | Só após `git status` e com trabalho salvo ou confirmado |
| C-6 | Prova de conceito | "How to exploit it" | Auditoria não altera nem executa | Descritiva, sem payload |
| C-7 | Roteiro de canário | 1/10/100 em ci-cd; 5/25/50/100 em shipping | Critérios definidos antes do deploy | Um roteiro por projeto, registrado no plano (Suposição: 5/25/50/100) |
| C-8 | Severidade | Skill e persona divergem | Achado sem `arquivo:linha` é descartado | Critical, Required, Optional, Nit, FYI, com `arquivo:linha` |
| C-9 | Quem roteia | `using-agent-skills` | Orquestrador e tags | Um roteador só: a sessão principal |
| C-10 | Plano e tarefas | `tasks/plan.md`, `tasks/todo.md`, "Task N" | `tasks.md` com T001 [P] [US1], IDs REQ/TASK | Convenção do repo alvo ou do brain; manter "não sobrescrever plano aberto" |
| C-11 | Spec | `SPEC.md`, Success Criteria em prosa | `SPEC.md` com FR-NNN, SC-NNN | IDs do brain; mapa de capacidades só com módulos independentes |
| C-12 | ADR | `docs/decisions/ADR-001` | `docs/adr/adr-NNNN-slug.md`, MADR | Convenção do repo alvo; senão a do brain |
| C-13 | Gates × autonomia | Param e esperam "yes" | ORCHESTRATOR §0: conduz sem pedir, três paradas | Gate vale quando o usuário invoca; no autônomo vira suposição ou decisão pendente |
| C-14 | Vendorizar intacto | Skills originais | Plano da fábrica | Adaptação só na camada própria, com precedência declarada |
| C-15 | Mutação manual | Inverte condição no arquivo | Auditoria não altera o produto | Em cópia ou worktree, restaurando |
| C-16 | Segunda opinião por CLI | `codex exec`, `gemini` com o artefato | Envio a terceiro exige confirmação | Só com confirmação, em modo leitura |
| C-17 | Persona sem `tools` | Confia em texto | Agentes do brain declaram `tools` | `tools` e "somente leitura" no prompt do subagente |

## 6. O que o upstream não cobre

Gitflow em profundidade, monorepo, publicação de pacote, SAST, varredura de segredos e SBOM no pipeline, comunicação de deprecação a consumidores externos, rollback de dados com perda, LGPD em logs, provedor de feature flags, OAuth e JWT, concorrência e banco em depuração, performance de backend, evals de persona e de comando, testes fora de JS e TS, e stacks que não sejam web. Para esses temas, o líder do segmento no brain é a fonte.
