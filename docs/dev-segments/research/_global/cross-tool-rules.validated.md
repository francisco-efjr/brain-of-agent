# Regras e prompts de outras ferramentas de IA para código — atlas validado (condensado)

Validador independente (claude-sonnet-5-5; o pesquisador foi outro modelo) · Data: 2026-10-09 · Origem: `cross-tool-rules.md` (30 itens R-cross-01..30) · Rubricas: prompt-quality-rubric, source-quality-rubric.

## Resultado da validação

- Re-verificado com ferramentas (~35% dos itens, priorizando classe A, números e citações literais): API do GitHub para 9 repositórios (estrelas, licença, push); 17 arquivos `raw.githubusercontent.com` com 40+ trechos literais (todos presentes, coerentes com a licença CC0/MIT); arXiv 2602.11988; Vercel; AAIF; Augment; Codex; Cursor; Windsurf/Devin; Gemini CLI; Thoughtworks; Claude Code memory; agents.md; docs.github.com; Sanglard; HN Algolia; LICENSE do PostHog.
- Verificado: estrelas, licenças e datas de push conferem (variação de poucas estrelas). Nenhuma injeção dirigida a IAs foi encontrada no atlas nem nas páginas lidas (agents.md, Sanglard e arquivos de regra contêm diretivas para agentes de código como conteúdo-exemplo, não dirigidas ao leitor). Nenhum texto sem licença permissiva foi copiado literalmente (literais só de CC0/MIT; PostHog `.cursorrules` é MIT fora de `ee/`, confirmado no LICENSE).
- Correções aplicadas (marcadas **[corr]**): estrelas de spec-kit/ruler agora verificadas; data do Sanglard; limiar do Augment; `excludeAgent` não reconfirmado; "quatro tipos" do Cursor.
- Lacunas que continuam: `cursor.directory` não lido; goose/Augment CLI/Factory/Devin só por snippet; exemplo first-party de AGENTS.md da OpenAI ausente; Reddit não alcançado; nenhum estudo por segmento. Itens com tom CAPS ("OVERRIDE", "MUST") exigem calibrar o tom ao portar (D10).

Convenção: "Lit." = trechos literais permitidos (licença + atribuição); "Dest." = destilar com redação própria.

---

## Itens aprovados

### R-cross-01 — AGENTS.md (agents.md + agentsmd/agents.md)
https://agents.md/ · https://github.com/agentsmd/agents.md · Classe A (9) · MIT · 24.846★, push 2026-09-10 (Verificado). Site afirma "over 60k" projetos e 88 AGENTS.md no repo da OpenAI (afirmação do site, Verificado na página). HN 837/382.
- Markdown puro, sem campos obrigatórios ("README para agentes"); o mais próximo do arquivo editado prevalece; prompt do usuário sobrepõe.
- Esqueleto reutilizável: comandos exatos · convenções divergentes · limites (pastas geradas) · verificação de "pronto" · PR/commit. Regra de ouro: só o que o agente não descobre lendo o repo.
- Thoughtworks Radar: Trial, nov/2025 (Verificado; fora da edição atual).
[seg:technical-writing-docs] [seg:automation-integrations] [seg:code-quality-refactoring] [seg:cli-desktop-tooling] [seg:git-workflow-release]

### R-cross-02 — Evidência empírica sobre arquivos de contexto
arXiv 2602.11988 (ETH; v1 2026-02-12, v3 2026-09-29, Verificado) · aaif.io/blog/measuring-agents-md-what-five-runs-show-that-one-doesn-t (Griffiths, 2026-07-22) · vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals (Jude Gao, 2026-01-27) · augmentcode.com/blog/how-to-write-good-agents-dot-md-files (Zhenylenko, 2026-04-22) · addyosmani.com/blog/agents-md · Classe A (ETH) / B (demais) · Dest.
- ETH: contexto não melhora sucesso em geral, custo +20% em média; instruções são seguidas; visão geral do repo não ajuda; vale para práticas não padrão.
- AAIF: 12 linhas, 5 runs, mediana: tempo -27%, créditos -24%, diff -26% (tarefa ambígua); 1 run inverte o resultado (+44%): nunca concluir com uma execução. Verificado.
- Vercel: baseline 53% = skill 53% → skill com instrução 79% → índice AGENTS.md 100%; índice 40 KB→8 KB mantém 100%. Conhecimento sempre necessário vai passivo; skills para procedimentos. (Benchmark do próprio fornecedor.)
- Augment: arquivos de 100–150 linhas + referências on-demand lideram; refs lidas em >90% das sessões com motivo, docs órfãos <10%; muitos "don'ts" sem "dos" causam sobre-exploração. **[corr]** o limiar exato varia no texto (15+/30+/30–50); não citar "30+" como número fixo.
- Checklist "o que merece uma linha": comando que o agente erraria; limite físico; convenção contraintuitiva; comando de verificação; regra de escopo; índice de caminhos. Remover: árvore de diretórios, dependências, "boas práticas", legado, o que já está no README.
- Ressalva: tarefas one-shot Python/JS; benchmarks de fornecedores; "porquê" em meia linha.
[seg:llm-ai-agents] [seg:technical-writing-docs] [seg:code-quality-refactoring] [seg:automation-integrations] [seg:cli-desktop-tooling]

### R-cross-03 — OpenAI Codex: descoberta e precedência de AGENTS.md
https://learn.chatgpt.com/docs/agent-configuration/agents-md · Classe A (8) · Dest. · Verificado na página.
- `AGENTS.override.md` → `AGENTS.md` → `project_doc_fallback_filenames`; um arquivo por diretório; concatena raiz→cwd (o mais próximo vem depois); `project_doc_max_bytes` 32 KiB por cadeia, excedente descartado.
- Seção `## Code Review Rules` perto do código: uma linha = comportamento a sinalizar + exceção segura; formatação/lint ficam no CI.
- `AGENTS.override.md` não é lido pelo Claude Code.
[seg:code-quality-refactoring] [seg:security-appsec] [seg:automation-integrations]

### R-cross-04 — Claude Code como destino do porte (CLAUDE.md, AGENTS.md, rules, imports)
https://code.claude.com/docs/en/memory · Classe A (9) · Dest. · Verificado 2026-10-09: AGENTS.md lido direto desde v2.1.277 e só sem CLAUDE.md; alvo <200 linhas; auto memory 200 linhas/25 KB; imports até 4 saltos; CLAUDE.md é contexto, não enforcement (usar hook PreToolUse).
- Tabela de porte: `alwaysApply`/copilot-instructions/`global_rules`/Kiro always/Aider CONVENTIONS → `CLAUDE.md` ou `.claude/rules/<tema>.md` sem `paths`; `globs`/`applyTo`/`paths`/`fileMatch`/`fileRegex` → `.claude/rules` com `paths:` (único campo lido); só `description`/`model_decision`/`auto` → skill; `manual`/prompt files → skill invocável; `.agent.md`/modos Roo/droids → subagent em `.claude/agents/`; Memory Bank → auto memory nativo.
- Ponte universal: `CLAUDE.md` com `@AGENTS.md` na 1ª linha + seção `## Claude Code`; symlink é frágil no Windows.
- Migração: `/init` lê regras de Cursor/Copilot (com `CLAUDE_CODE_NEW_INIT=1`, também AGENTS/Windsurf/Cline), `/import`, `/doctor prompt-audit`. Versões 2.1.283/285/213 não reconferidas (**Inferido**): conferir a instalada.
[seg:automation-integrations] [seg:technical-writing-docs] [seg:llm-ai-agents] [seg:code-quality-refactoring]

### R-cross-05 — Cursor: `.cursor/rules/*.mdc`
https://cursor.com/docs/context/rules · Classe A (8) · Dest. · Verificado: campos `description`/`globs`/`alwaysApply`, "Keep rules under 500 lines", `.md` sem frontmatter é ignorado, quatro modos de aplicação (Always/Intelligently/Specific Files/Manually). **[corr]** a página lista "quatro tipos de regra" distintos (Project/User/Team/AGENTS.md); não confundir com os modos.
- Triagem ao portar: ver R-cross-04; cortar persona "You are an expert…", manter diretivas verificáveis; regra nova só quando o agente repete o erro.
- A maioria dos `.mdc` comunitários usa `globs: **/*` + `alwaysApply: false` (efeito de regra global): decidir conscientemente. Skills/`/migrate-to-skills`: só snippet (Não verificado).
[seg:web-frontend] [seg:code-quality-refactoring] [seg:automation-integrations]

### R-cross-06 — PatrickJS/awesome-cursorrules (catálogo)
https://github.com/PatrickJS/awesome-cursorrules · Classe B (7) · CC0-1.0 · 40.894★, push 2026-05-30 (Verificado; >4 meses). Lit. permitido com atribuição.
- Layout atual `rules/<nome>.mdc`; qualidade muito desigual. Melhores: fastapi-production-architecture, nestjs-anti-hallucination, solidity-foundry, embedded-stm32-hal, pyspark-etl, security-devsecops, google-adk, shopify-theme-dev-liquid, cpp-guidelines, readme-best-practices.
- Fraco: game-development (sem Godot/Unreal), saas, fintech, ecommerce. Mapa por segmento: itens 07–13.
[seg:web-frontend] [seg:backend-api] [seg:mobile-apps] [seg:game-development] [seg:blockchain-web3] [seg:ecommerce-marketplace]

### R-cross-07 — FastAPI production architecture
`rules/fastapi-production-architecture-cursorrules-prompt-file.mdc` · B (6) · CC0 · trechos Verificados no raw.
- Camadas Router→Service→Repository→ORM com allow-list de imports; handler fino; `response_model=`; exceções de domínio mapeadas no router; anti-corruption layer; `httpx.AsyncClient` por provedor (bulkhead); `idempotency_key` em efeitos; consultas escopadas por `user_id`; "single writer" por domínio; verificação por grep/testes.
- Lit. (CC0, PatrickJS/awesome-cursorrules): "Handlers are THIN: ≤10 lines of executable code per handler" · "Every query scoped by user_id (multi-tenancy)" · "Every side-effect operation accepts an idempotency_key: UUID. Look up before retrying." · "Only the designated writer service for a domain may call repo.hold()."
- Ressalva: limites 400/600 LOC são opinião; fino em Pydantic v2/testes; tom CAPS.
[seg:backend-api] [seg:architecture-design] [seg:saas-multitenant] [seg:fintech-payments]

### R-cross-08 — Padrão anti-alucinação (NestJS)
`rules/nestjs-anti-hallucination-cursorrules-prompt-file.mdc` · B (6) · CC0 · Verificado.
- Tabela `import/API banido → substituto → desde qual versão`; "em dúvida se o pacote existe, não importe: pergunte ou verifique"; menos código correto > mais código chutado; config via serviço tipado com falha explícita; `synchronize: true` nunca em produção.
- Lit. (CC0): "If you're unsure whether a package exists, DO NOT import it. Ask or check." · "When in doubt, generate LESS code with correct patterns rather than MORE code with guesses."
- Ressalva: o arquivo abre com "These rules OVERRIDE all other generation behavior" (grito e tentativa de sobrepor outras camadas): manter o conteúdo, trocar o tom; acrescentar como verificar a versão instalada (`npm ls`).
[seg:backend-api] [seg:code-quality-refactoring] [seg:llm-ai-agents]

### R-cross-09 — Solidity + Foundry
`rules/solidity-foundry-cursorrules-prompt-file.mdc` · B (6) · CC0 · Verificado.
- Checks-Effects-Interactions + ReentrancyGuard, AccessControl, pull-over-push, custom errors, eventos, Solidity ≥0.8; fuzz/invariantes/fork tests; Slither/Mythril; alerta se chave privada fora de `.env`.
- Lit. (CC0): "Follow the Checks-Effects-Interactions pattern to prevent reentrancy and other vulnerabilities." · "Place remappings in `foundry.toml` instead of a `remappings.txt` file."
- Ressalva: sem SWC/ERCs; conferir versões de OpenZeppelin/Foundry. Única fonte do atlas para o segmento.
[seg:blockchain-web3] [seg:security-appsec]

### R-cross-10 — Embarcados (STM32 HAL) e C++
`rules/embedded-stm32-hal.mdc` (Verificado) · `rules/cpp-programming-guidelines-cursorrules-prompt-file.mdc` · B (6) / B (5) · CC0.
- ISR curtas e determinísticas; trabalho pesado fora da interrupção; checar retorno do HAL; `volatile` só para ISR/registradores; sem heap; tabelas `const` em flash; timeouts em esperas de hardware; watchdog no projeto; DMA/CPU sem sincronização é proibido; lógica pura testada no host. C++: RAII, Rule of Zero/Five, `std::optional/expected`.
- Lit. (CC0): "Keep ISRs short and deterministic." · "Avoid heap allocation in firmware unless the project explicitly allows it." · "Do not share buffers between DMA and CPU without synchronization."
- Ressalva: sem MISRA, sanitizers, clang-tidy, CI: o plugin deve acrescentar.
[seg:systems-embedded-iot]

### R-cross-11 — Dados/ML/LLM (PySpark, pandas, LLM workflow, Google ADK)
`rules/pyspark-etl-best-practices-…mdc`, `pandas-scikit-learn-guide-…`, `python-llm-ml-workflow-…`, `google-adk.mdc` (Verificado) · B (6) pyspark/ADK; C (4) pandas/LLM · CC0.
- PySpark: merges idempotentes e independentes de ordem, validar unicidade de PK após escrita, `.byName()`, sem UDF/`collect()` em produção. ADK: um agente por objetivo, validar argumentos de tool antes de efeitos, estado pequeno, testes de roteamento e chamadas inseguras, acesso controlado em código e não em prompt.
- Lit. (CC0): "Merges must be idempotent" · "Validate primary key uniqueness after writes" · "Validate tool arguments before performing side effects." · "Do not rely on prompt text for access control."
- Ressalva: pandas e LLM workflow são genéricos (sem leakage/CV; sem eval/custo): só como sinal.
[seg:data-engineering] [seg:data-science-ml] [seg:llm-ai-agents]

### R-cross-12 — Mobile (SwiftUI, Compose, Flutter) e "Flexibility Notice"
`rules/swiftui-guidelines-…mdc` (B 6, Verificado), `android-jetpack-compose-…`, `flutter-app-expert-…` (C 4) · CC0.
- Swift 6 concurrency, `@MainActor`, `.task(id:)`, `body` ≤ 50 linhas, IDs estáveis, mocks por protocolo, warnings como erros. Padrão "Flexibility Notice": adaptar à arquitetura existente em vez de impor estrutura.
- Lit. (CC0): "Always use stable `id`" · "Treat warnings as errors." · "Adapt to existing project architecture while maintaining clean code principles"
- Ressalva: acessibilidade e publicação em lojas ausentes; Android/Flutter em formato gerado, sem verificação.
[seg:mobile-apps] [seg:qa-testing]

### R-cross-13 — Transversais do awesome-cursorrules (DevSecOps, commits, README, Playwright, Gherkin)
`security-devsecops-ssdls-appsec.mdc` (Verificado), `git-conventional-commit-messages.mdc`, `readme-best-practices-…`, `playwright-e2e-testing-…`, `gherkin-style-testing-…` · B (6) · CC0.
- DevSecOps: sem segredos hardcoded, sem log de dados sensíveis, queries parametrizadas, nova dependência só com aprovação, auth por framework, secret scanning/SAST/SCA no CI, ciclo de feedback das regras. README = landing page, exemplo funcional nas 5 primeiras linhas, checar que imagens existem. Playwright: `page.route`, auto-wait, 3–5 testes por arquivo. Gherkin em linguagem de negócio.
- Lit. (CC0): "Never hardcode secrets, credentials, or API keys." · "Use parameterized queries or ORM for all database access." · "Write READMEs like landing pages, not API docs." · "Leverage Playwright's auto-waiting instead of explicit waits"
- Ressalva: commits copiam a spec Conventional Commits (CC-BY 3.0, atribuição não reconferida): citar conventionalcommits.org. Anti-exemplos: ver rejeitados.
[seg:security-appsec] [seg:git-workflow-release] [seg:technical-writing-docs] [seg:qa-testing] [seg:product-discovery-specs]

### R-cross-14 — github/awesome-copilot (catálogo)
https://github.com/github/awesome-copilot · Classe A (8) · MIT · 39.873★, push 2026-10-09 (Verificado). Raiz atual (API): `agents`, `instructions`, `skills`, `plugins` (104 dirs), `hooks`, `workflows`, `cookbook`; sem `chatmodes/` nem `prompts/` (Verificado).
- Cobre 24/25 segmentos (blockchain ausente); formato `.agent.md`/`.instructions.md`/`SKILL.md` próximo ao do Claude Code. Mapa: instructions de security, qa, devops, a11y, code-review, spec-driven; agents ADR/debug/plan; skills `breakdown-*`, `documentation-writer`, `conventional-commit`; plugins `*-mcp-development`, `openapi-to-application-*`.
- Ressalva: viés Microsoft/Azure/Power Platform; muitos instructions de 700–1.000 linhas: portar destilando; o README alerta para inspecionar customizações de terceiros antes de instalar.
[seg:product-discovery-specs] [seg:architecture-design] [seg:web-frontend] [seg:backend-api] [seg:devops-cloud-infra] [seg:qa-testing] [seg:security-appsec] [seg:llm-ai-agents] [seg:automation-integrations] [seg:technical-writing-docs] [seg:git-workflow-release]

### R-cross-15 — Meta-guias do awesome-copilot
`instructions/instructions.instructions.md`, `instructions/agents.instructions.md`, `AGENTS.md` · B (7) · MIT · Verificado no raw.
- "Instruction altitude": começar mínimo, adicionar restrição após falha real; banir "should/might"; exemplos bom/ruim; testar com prompts reais; agents: tools mínimas, handoffs limitados, corpo <30.000 caracteres.
- Lit. (MIT, github/awesome-copilot): "Add constraints after observed failures, not hypothetical edge cases" · "Fewer tools = clearer agent purpose and better performance" · "Do not add rules for failures that have not occurred" · "Total content under 30,000 characters"
- Portar a disciplina, não campos específicos (`handoffs`, `target`, `mcp-servers`).
[seg:automation-integrations] [seg:technical-writing-docs] [seg:llm-ai-agents] [seg:code-quality-refactoring]

### R-cross-16 — `security-and-owasp.instructions.md`
`instructions/security-and-owasp.instructions.md` · B (7) · MIT · Verificado (~32 KB).
- Molde `ID · severidade · detecção (regex/comando) · referência OWASP · correção`; níveis CRITICAL/IMPORTANT/SUGGESTION; OWASP Top 10 2025; seção AI/LLM; checklist final.
- Lit. (MIT): "Frontend guards are UX only. ALWAYS verify on server." · "Never trust LLM output as safe." · "Always verify webhook signatures (Stripe, GitHub HMAC, etc.)." · "Use httpOnly cookies for tokens."
- Ressalva: regexes são heurísticas; ~1.000 linhas → vira skill/`references/` com resumo em regra `paths`-scoped.
[seg:security-appsec] [seg:llm-ai-agents] [seg:backend-api] [seg:web-frontend] [seg:fintech-payments]

### R-cross-17 — QA (`qa-engineering-best-practices`, `playwright-typescript`)
https://github.com/github/awesome-copilot/tree/main/instructions · B (7) / B (6) · MIT · não reabertos pelo validador.
- Pirâmide 60–70/20–30/5–10; determinismo; asserção de valor exato; mock na borda; flaky: retry 1x e sinalizar; seletores role→label→test-id→text; sem `sleep`; cobertura para achar lacunas, não métrica; Playwright: asserções web-first, loop executar→analisar→refinar→confirmar estabilidade.
- Lit. (MIT): "Deterministic tests: Tests must produce the same result on every run." · "Mock at the boundary (HTTP clients, DB adapters, message queues) — not deep inside business logic." · "Use accessible selectors in order of preference: role → label → test-id → text."
- Ressalva: sem page objects/contract/mutation em detalhe; cruzar com `brains/qa`.
[seg:qa-testing] [seg:web-frontend]

### R-cross-18 — DevOps (GitHub Actions + Terraform)
`instructions/github-actions-ci-cd-best-practices.instructions.md` (Verificado) · `instructions/terraform.instructions.md` · B (7) / B (6) · MIT.
- Pin por SHA completo; `permissions` mínimas (`contents: read`); OIDC em vez de credenciais longas; não construir/imprimir segredos; cache com `hashFiles`; `fetch-depth: 1`; environments com aprovação e rollback. Terraform: `sensitive = true`, módulos só para grupos de recursos, `description`/`type`, `fmt`/`validate`/`tflint`/`trivy|checkov`, `.tftest.hcl`.
- Lit. (MIT): "Always pin to a full-length commit SHA for maximum security and immutability." · "Use OIDC for secure, credential-less authentication with cloud providers" · "Always mark sensitive variables as `sensitive = true` in your Terraform configurations."
- Ressalva: Terraform sem constraints de versão/lockfile/state backend; Actions tem ~54 KB: destilar para ~30 linhas + `references/`. Viés Azure.
[seg:devops-cloud-infra] [seg:security-appsec] [seg:git-workflow-release]

### R-cross-19 — Frontend: a11y (WCAG 2.2 AA) e performance (Core Web Vitals)
`instructions/a11y.instructions.md` (Verificado) · `instructions/performance-optimization.instructions.md` · B (7) · MIT.
- Molde severidade+detecção+referência+correção; catálogos de semântica/ARIA/teclado/formulários; LCP/INP/CLS, bundle, imagens.
- Lit. (MIT): "Placeholder is a hint, not a label." · "Test at 320px CSS width." · "Never use array index as key if list can reorder."
- Ressalva: performance é só frontend (sem backend/N+1); nenhum nomeia axe/Lighthouse: acrescentar comandos de verificação.
[seg:web-frontend] [seg:ux-ui-design] [seg:sre-observability]

### R-cross-20 — Code review genérico
`instructions/code-review-generic.instructions.md` · B (6) · MIT · Verificado.
- Três níveis (bloqueia merge / discutir / sugestão), template de comentário (categoria, por que importa, correção, referência), PR grande por blocos (segurança→testes→lógica→estilo), reconhecer o que está bom, criticar o código e não o autor.
- Lit. (MIT): "Be specific: Reference exact lines, files, and provide concrete examples" · "Recognize good practices: Acknowledge well-written code and smart solutions" · "Review large PRs in logical chunks (security → tests → logic → style)"
- Ressalva: trocar emojis de severidade por rótulos textuais (estilo da casa); "funções < 20–30 linhas" é heurística.
[seg:code-quality-refactoring] [seg:security-appsec] [seg:git-workflow-release]

### R-cross-21 — Agentes: ADR, plano, debug, critical thinking
`agents/adr-generator.agent.md`, `agents/implementation-plan.agent.md`, `agents/debug.agent.md` (últimos dois Verificados), `agents/critical-thinking.agent.md` · B (6) · MIT.
- ADR: pede dados e para se faltar; `adr-NNNN-slug.md`; Status/Context/Decision/Consequences/Alternatives (inclui "do nothing"). Plano: sem edições de código, fases com critério mensurável, IDs REQ-/TASK-/RISK-. Debug: reproduzir antes de mudar → hipóteses → fix mínimo + regressão → relatório de causa raiz. Critical thinking: uma pergunta por vez, sem dar respostas.
- Lit. (MIT): "If any required information is missing, ask the user to provide it before proceeding." · "DO NOT make any code edits - only generate structured plans" · "Always reproduce and understand the bug before attempting to fix it."
- Ressalva: `implementation-plan` declara "sem edições" mas lista tools de edição (D8): ao portar, tools somente leitura.
[seg:architecture-design] [seg:product-discovery-specs] [seg:code-quality-refactoring]

### R-cross-22 — Spec-driven workflow e Memory Bank
`instructions/spec-driven-workflow-v1.instructions.md` (Verificado) · `memory-bank.instructions.md` · https://docs.cline.bot/prompting/cline-memory-bank · B (6) / B (5) · MIT (awesome-copilot).
- Artefatos requirements (EARS) / design / tasks; fases ANALYZE→DESIGN→IMPLEMENT→VALIDATE→REFLECT→HANDOFF; gate por confiança (>85% implementa; 66–85% PoC; <66% pesquisa); VALIDATE exige evidência.
- Lit. (MIT): "Format: WHEN [a condition or event], THE SYSTEM SHALL [expected behavior]" · "Code in small, testable increments."
- Ressalva: "Never skip any step" é rígido (usar como modo completo); Memory Bank custa tokens e tem tom dramático; Claude Code já tem auto memory.
[seg:product-discovery-specs] [seg:technical-writing-docs] [seg:automation-integrations]

### R-cross-23 — GitHub Copilot oficial + VS Code
https://docs.github.com/en/copilot/tutorials/use-custom-instructions · https://code.visualstudio.com/docs/copilot/customization/custom-agents · A (8) · Dest. · Verificado parcialmente.
- `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md` com `applyTo`, `AGENTS.md`; teto ~1.000 linhas por arquivo (confirmado); não incluir: links externos (copiar o conteúdo), metas vagas, formatação de saída do produto, mudança de função central; começar com 10–20 instruções.
- VS Code lê `.claude/agents` e `.prompt.md` está em depreciação (do original; não reconferido: **Inferido**). **[corr]** `excludeAgent` não aparece na página do tutorial reconferida: **Não verificado**.
- O teto de 1.000 linhas é frouxo frente à evidência (R-cross-02); adotar o menor.
[seg:automation-integrations] [seg:git-workflow-release] [seg:code-quality-refactoring]

### R-cross-24 — Cline e Roo Code (docs oficiais)
https://docs.cline.bot/features/cline-rules · https://roocodeinc.github.io/Roo-Code/features/custom-instructions · B (7) · Dest. · não reverificado pelo validador.
- Um tema por arquivo com prefixo numérico → `.claude/rules/<nn>-<tema>.md`; regras condicionais com `paths:`; Roo: regras por modo → subagent + regras `paths`.
- O repo `cline/prompts` é rejeitado como fonte (ver tabela).
[seg:automation-integrations] [seg:code-quality-refactoring]

### R-cross-25 — Windsurf / Devin
https://docs.devin.ai/desktop/cascade/memories · B (7) · Dest. · Verificado.
- Limites: global 6.000 chars; arquivo de workspace 12.000 chars; `.devin/rules/` preferido, `.windsurf/rules/` fallback; `trigger`: `always_on`/`model_decision`/`glob`/`manual`; recomenda bullets curtos, pular conselho genérico e agrupar regras em tags XML.
- Uso: orçamento de referência (~100 linhas sempre ativas) e blocos `<tema>` XML em CLAUDE.md.
[seg:technical-writing-docs] [seg:automation-integrations]

### R-cross-26 — Aider `CONVENTIONS.md` (docs)
https://aider.chat/docs/usage/conventions.html · B (6) · Dest. · não reverificado.
- Convenções como arquivo read-only cacheado (`--read`); exemplo mínimo (httpx em vez de requests + type hints) com efeito observável: bom exemplo pedagógico. Repo `Aider-AI/conventions` rejeitado (ver tabela).
[seg:git-workflow-release] [seg:code-quality-refactoring]

### R-cross-27 — Matriz dos demais ecossistemas
Docs: continue.dev, kiro.dev, geminicli.com (Verificado em parte), zed.dev, junie.jetbrains.com, ampcode.com, opencode.ai, Thoughtworks Radar (Verificado) · B (6–7); goose/Augment/Factory/Devin = C (snippet) · Dest.
- Regras de compatibilidade para o `AGENTS.md` gerado: Markdown puro sem frontmatter na raiz; caminhos em texto E `@path` (nem todos expandem); não depender de `AGENTS.override.md` (só Codex); um AGENTS.md por pacote; sem link externo sem resumo.
- Gemini CLI: banner confirma substituição pelo Antigravity CLI para o tier gratuito em 2026-06-18: tratar como instável. Kiro: trio product/tech/structure vai contra a evidência de que overview não ajuda.
- Linhas goose/Augment/Factory/Devin permanecem **Não verificadas**.
[seg:automation-integrations] [seg:technical-writing-docs] [seg:cli-desktop-tooling]

### R-cross-28 — Receitas de porte: ruler, spec-kit, `@AGENTS.md`
https://github.com/intellectronica/ruler · https://github.com/github/spec-kit · B (6) ruler, B (7) spec-kit · Dest.
- **[corr] Verificado via API:** ruler MIT, 2.941★, push 2026-09-30; spec-kit MIT, 140.622★ (o atlas dizia 72k–115k, não verificado), push 2026-10-10.
- Receita: inventariar arquivos de regra → classificar por frontmatter (tabela R-cross-04) → reduzir pelo checklist R-cross-02 → deduplicar com `/doctor prompt-audit` → `CLAUDE.md` com `@AGENTS.md` → ruler só com ≥3 ferramentas (cópias estáticas envelhecem).
- spec-kit: comandos constitution/specify/plan/tasks/implement, artefatos em `.specify/` (README; não reconferido).
[seg:product-discovery-specs] [seg:automation-integrations] [seg:git-workflow-release]

### R-cross-29 — Praticantes e comunidade
https://fabiensanglard.net/agent.md/index.html · trigger.dev/blog/cursor-rules · Cursor Forum/TabNews (snippets) · B (6) Sanglard; C (4) demais.
- Sanglard (**[corr]** página datada 2026-08-21; HN 415/176 em 2026-08-23, Verificado). Sem licença: destilado. Bug fix = teste que falha primeiro; 7 regras de commit; nova sessão por feature e recarregar o agent.md quando a qualidade cai ("diluição de contexto").
- trigger.dev: fixar versão, exemplos completos, padrões depreciados com substituto, terminar com verificação passa/falha.
- Higiene de contexto: regra sempre ativa curta; regra operacional de ambiente (flox, uv, pnpm) vale mais que dez de estilo; usar Conventional Commits OU as 7 linhas, nunca ambas.
- Fórum/TabNews: anedótico (snippets).
[seg:git-workflow-release] [seg:code-quality-refactoring] [seg:qa-testing]

---

## Rejeitados

| Item / trecho | Motivo |
| --- | --- |
| R-cross-30 `x1xhlol/system-prompts-and-models-of-ai-tools` (143.932★, GPL-3.0, push 2026-08-11; metadados Verificados) | Prompts de sistema vazados de produtos comerciais: autoria e licença de terceiros não resolvidas (a GPL do repo não cobre o conteúdo), risco de takedown e reputacional; popularidade não é qualidade. Não portar, não citar, não linkar como referência (reprovação automática: cópia sem licença). |
| R-cross-24 repo `cline/prompts` | Sem licença (`license: null`, Verificado), 1.211★, push 2026-02-27; arquivos individuais não abertos. Só docs oficiais aprovadas. |
| R-cross-26 repo `Aider-AI/conventions` | 207★, push 2025-06-25 (>15 meses), arquivos não abertos. Só docs aprovadas. |
| R-cross-06 `cursor.directory` / `cursor/community-plugins` | Site não lido (429); repo-fonte sem licença (Verificado, 4.000★): destilar apenas. |
| R-cross-13 anti-exemplos `unity-cursor-ai-c-…`, `go-backend-scalability-…`, `nextjs15-react19-…` | Regra de projeto único; persona sem diretiva Go; arquivo truncado. Servem só de calibração negativa. |
| R-cross-21 `api-architect.agent.md` | Classe C: depende de tool inexistente no Claude Code, exige código completo sem testes. |
| R-cross-29 PostHog `.cursorrules` (conteúdo) | MIT confirmado no LICENSE, mas abertura em CAPS agressivo (D10) e só a regra `flox` é de projeto. Aceito só como anti-exemplo de tom e dica `flox activate -- bash -c`. |
| R-cross-27 linhas goose/Augment CLI/Factory/Devin | Apenas snippets; não usar como base. |
| Afirmações não reverificadas: "ETH: gerados pioram 5 de 8 cenários, humanos +4 p.p." (R-cross-02); Lulla et al. arXiv 2601.20404; nomes de arquivos de `cline/prompts` | Cobertura secundária/snippet; não citar números em plugins sem abrir o paper. |

---

## Princípios / achados transversais

- Cada linha do arquivo de contexto deve ser algo que o agente não descobre lendo o repositório: comandos, limites, convenções divergentes, verificação (arXiv 2602.11988; addyosmani.com/blog/agents-md; code.claude.com/docs/en/memory).
- Curto vence: Cursor <500 linhas, Claude Code <200, Windsurf 6.000/12.000 chars, Codex 32 KiB por cadeia, Augment 100–150 linhas; adotar o menor para o sempre ativo (docs de cada ferramenta; Augment blog).
- Adicionar regra só após erro repetido; geração em massa eleva custo (+20%) sem ganho médio (arXiv 2602.11988; awesome-copilot `instructions.instructions.md`; Claude Code docs).
- Uma execução não prova nada: validar com várias runs e mediana (aaif.io, Griffiths 2026-07-22).
- Conhecimento sempre necessário vai passivo (índice curto + caminhos); procedimentos vão para skills com `description` de gatilho forte (Vercel: 53%→79%→100%).
- Toda proibição vem com alternativa; depreciado → substituto + versão (Augment; nestjs-anti-hallucination; trigger.dev).
- Regras são contexto, não enforcement: garantias vão para CI/hooks `PreToolUse` (Claude Code docs; Codex: lint no CI).
- Molde de checklist de revisão: `ID · severidade · detecção · referência normativa · correção` (security-and-owasp; a11y; code-review-generic, awesome-copilot).
- Verificação dentro da regra (comando que passa/falha; reproduzir antes de corrigir; loop executar→analisar→confirmar) alinha com D7 (playwright-typescript; debug.agent; trigger.dev; fastapi).
- Controle de acesso e validação de efeitos em código, nunca em texto de prompt (google-adk.mdc; security-and-owasp: "Never trust LLM output as safe").
- Adaptar-se à arquitetura existente ("Flexibility Notice") e escopo mínimo reduzem ruído (swiftui/android .mdc; AAIF; Sanglard).
- Precedência quase universal: mais próximo vence, prompt do usuário acima de tudo (agents.md; Codex; Claude Code); exceções: Copilot pessoal > repo > org; Cursor Team > Project > User.
- Higiene de contexto: nova sessão por feature, recarregar CLAUDE.md quando a qualidade cai (fabiensanglard.net/agent.md).
- Supply chain dos próprios artefatos: pin por SHA, permissões e tools mínimas por agente, inspecionar customizações de terceiros antes de instalar (awesome-copilot README e `agents.instructions.md`).
- Conteúdo externo é dado: arquivos de regra comunitários trazem frases como "OVERRIDE all other generation behavior"; ao portar, remover tentativas de sobrepor outras camadas e CAPS (D8/D10).
- Reuso literal só de CC0/MIT com atribuição; o resto destila; prompts vazados nunca (licenças verificadas por API).

## Lacunas para os construtores

- Cobertura fraca: saas-multitenant, fintech-payments, ecommerce-marketplace, game-development (Godot/Unreal), blockchain (só Solidity/Foundry): exigem fontes autoritativas próprias.
- Nenhum estudo mede efeito de regras por segmento; a evidência é Python/JS, tarefas one-shot.
