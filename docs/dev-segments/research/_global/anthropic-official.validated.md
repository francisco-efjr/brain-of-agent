# Corpus oficial da Anthropic — versão validada (condensada)

Validador independente (Claude Sonnet 5.5; o pesquisador foi outro modelo) · 2026-10-09 · Fonte: `anthropic-official.md` (31 itens R-anthropic-01..31).
Método: reverificação por ferramenta de 15 itens (~48%) priorizando classe A, números e licenças. Nenhuma injeção de prompt encontrada nos conteúdos relidos (security-review.md, system prompt Fable 5.1, docs). Nenhum trecho literal sem licença permissiva: os únicos literais (R-24) são MIT, curtos e com atribuição, e foram confirmados no arquivo original.

Rótulos: **[V]** reverificado agora · **[P]** aprovado com base na leitura do pesquisador, não reverificado (rótulo Inferido para consumo) .

## Correções de metadados (observado agora)

| Repo | ★ agora | Licença (API) | Push |
| --- | --- | --- | --- |
| anthropics/skills | 180.191 | null (licença por skill) | 2026-10-09 |
| anthropics/claude-code | 149.899 | null (destilar apenas) | 2026-10-09 |
| anthropics/claude-cookbooks | 53.310 | MIT | 2026-10-09 |
| anthropics/claude-plugins-official | 37.592 | Apache-2.0 | 2026-10-09 |
| anthropics/claude-code-security-review | 6.329 | MIT | 2026-02-11 |
| anthropics/claude-code-action | 9.457 | MIT | 2026-10-09 |

Diferenças de estrelas vs. relatório são deriva normal (≤ 22). Licenças e datas conferem.

## Itens aprovados

### R-01 Prompting best practices — A
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices · docs proprietárias (destilar) · [V] página existe e cobre Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5 etc.
- Regras reutilizáveis: investigar antes de afirmar; agir quando pedido (imperativo); escopo mínimo; solução geral, não gabarito; confirmar ações destrutivas/visíveis; paralelizar tool calls; estado em JSON + git.
- Contexto/motivação, 3–5 exemplos em `<example>`, docs longos no topo, instruções positivas, sem CAPS excessivo.
- Ressalva: recomendações medidas por modelo; reavaliar com evals.
- [seg:llm-ai-agents] [seg:code-quality-refactoring] [seg:qa-testing] [seg:web-frontend] [seg:technical-writing-docs]

### R-02 Prompt engineering overview + define success criteria/evals — A [P]
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview · .../test-and-evaluate/develop-tests · destilar
- Critérios específicos e mensuráveis; eval set com casos de borda; volume > qualidade; grader por código/humano/LLM (modelo diferente do gerador).
- `metaprompt.ipynb`: não verificável (não usar).
- [seg:llm-ai-agents] [seg:qa-testing] [seg:data-science-ml]

### R-03 Prompting Claude Fable 5.1 — A
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 · [V] existe; descrição lista efforts, progress updates, batching, histórico, compaction, escopo/testes. Destilar.
- Terminar a tarefa inteira; pedido = escopo (bugs vizinhos viram follow-up); testes só onde o repo já mantém.
- Compaction: preservar problemas resolvidos, opções descartadas, decisões exatas, estado, pendências, detalhes difíceis.
- Histórico append-only; edições cirúrgicas.
- Ressalva: específico de modelo/API betas.
- [seg:llm-ai-agents] [seg:code-quality-refactoring] [seg:qa-testing] [seg:automation-integrations]

### R-04 Skill authoring best practices — A (núcleo da fábrica)
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices · [V] integral confere: name ≤64 `[a-z0-9-]` sem "anthropic/claude"; description ≤1024, 3ª pessoa, o que faz + quando; corpo <500 linhas; refs um nível; ≥3 evals; testar Haiku/Sonnet/Opus.
- Graus de liberdade (alto/médio/baixo), feedback loops, plan-validate-execute, nomes MCP `Server:tool`, caminhos com `/`.
- Sem runner oficial para o formato de eval da página.
- [seg:automation-integrations] [seg:technical-writing-docs] [seg:llm-ai-agents] (meta: todos)

### R-05 Agent Skills overview + agentskills.io spec — A [P]
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview · https://agentskills.io/specification
- Campos da spec: name, description, license, compatibility (≤500), metadata, allowed-tools; name = pasta; 3 níveis de carga.
- Fora do Claude Code só campos da spec valem.
- [seg:automation-integrations] [seg:technical-writing-docs]

### R-06 Best practices for Claude Code — A
https://code.claude.com/docs/en/best-practices · [V] integral confere (verificação, explore→plan→code, CLAUDE.md curto, "IMPORTANT" em uma linha, entrevista→SPEC.md, revisor adversarial "gaps, não estilo", padrões de falha).
- Verificação em 4 graus: prompt, `/goal`, Stop hook, subagente verificador. Pedir evidência.
- Após 2 correções, `/clear` + prompt melhor.
- Ressalva: recursos novos (auto mode v2.1.283+, `/goal`, agent teams experimental): checar versão.
- [seg:product-discovery-specs] [seg:qa-testing] [seg:code-quality-refactoring] [seg:git-workflow-release] (todos)

### R-07 CLAUDE.md / rules / memory — A [P]
https://code.claude.com/docs/en/memory
- CLAUDE.md é contexto, não enforcement; <200 linhas; `.claude/rules/*.md` com `paths`; `@imports`; `/doctor` audita.
- Estrutura mínima: Comandos · Convenções divergentes · Fluxo · Armadilhas.
- [seg:technical-writing-docs] [seg:code-quality-refactoring] (todos)

### R-08 Skills no Claude Code — A [P]
https://code.claude.com/docs/en/skills
- Campos extras: `disable-model-invocation`, `allowed-tools`, `context: fork`+`agent`, `paths`, `` !`cmd` ``, `${CLAUDE_PLUGIN_ROOT}`.
- Skill com efeito colateral: `disable-model-invocation: true` + allowed-tools mínimos.
- [seg:automation-integrations] [seg:git-workflow-release] (todos)

### R-09 Subagentes — A [P]
https://code.claude.com/docs/en/subagents
- Frontmatter: tools, model, skills, memory, isolation, maxTurns; plugins ignoram hooks/mcpServers/permissionMode.
- Exemplos: security-reviewer (read-only), db-reader com hook PreToolUse exit 2.
- [seg:security-appsec] [seg:code-quality-refactoring] [seg:qa-testing] [seg:database-data-modeling]

### R-10 Hooks (referência + guia) — A [P]
https://code.claude.com/docs/en/hooks · https://code.claude.com/docs/en/hooks-guide
- exit 2 bloqueia, exit 1 não; `permissionDecision`; `additionalContext` declarativo; hooks com privilégios do usuário.
- Padrões: guardrail PreToolUse, format PostToolUse, gate Stop, contexto factual SessionStart.
- [seg:devops-cloud-infra] [seg:security-appsec] [seg:git-workflow-release] [seg:qa-testing] [seg:automation-integrations]

### R-11 Plugins + `claude plugin eval` — A
https://code.claude.com/docs/en/plugins · https://code.claude.com/docs/en/plugin-evals · [V] página existe; v2.1.269 citada; 3 execuções por caso; graders incl. `tool_order`; declara que skill-creator evals usa formato próprio incompatível.
- Eval por plugin: caso que dispara + caso "ignora pedido não relacionado" + rubrica LLM PASS/FAIL; baseline sem plugin; gate de CI.
- Custo de contexto de nome+description por turno.
- [seg:automation-integrations] [seg:qa-testing] (meta)

### R-12 Extend Claude Code + blog Steering — A [P]
https://code.claude.com/docs/en/features-overview · https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
- Árvore de decisão: hook (sempre) → CLAUDE.md (<10 linhas) → rule com paths → skill → subagente → MCP.
- "Instrução é pedido, hook é enforcement."
- [seg:technical-writing-docs] [seg:automation-integrations] (meta)

### R-13 Output styles — A [P]
https://code.claude.com/docs/en/output-styles · `keep-coding-instructions: true` quando papel segue sendo engenharia; estilo é instrução, não garantia.
- [seg:technical-writing-docs] [seg:architecture-design] [seg:ux-ui-design]

### R-14 Common workflows — A [P]
https://code.claude.com/docs/en/common-workflows · receitas: amplo→específico, bug com repro+stack, refactor incremental, testes de borda, tarefas agendadas com critério de sucesso.
- [seg:code-quality-refactoring] [seg:qa-testing] [seg:git-workflow-release] [seg:technical-writing-docs] [seg:devops-cloud-infra]

### R-15 Building effective agents — A [P]
https://www.anthropic.com/engineering/building-effective-agents (2024-12-19) · workflows × agents; 5 padrões; ACI e poka-yoke. Parte datada (aponta Managed Agents).
- [seg:llm-ai-agents] [seg:architecture-design] [seg:automation-integrations]

### R-16 Effective context engineering — A [P]
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (2025-09-29) · menor conjunto de tokens de alto sinal; just-in-time; compaction, notas, subagentes devolvendo 1–2k tokens.
- [seg:llm-ai-agents] (todos)

### R-17 Writing tools for agents + Define tools + think tool — A [P]
https://www.anthropic.com/engineering/writing-tools-for-agents · https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools · https://www.anthropic.com/engineering/claude-think-tool
- Consolidar operações, namespacing, `concise|detailed`, erros acionáveis, descrição como fator principal. "40%" é experimento interno.
- Think tool: superseded em boa parte por thinking adaptativo (Inferido).
- [seg:automation-integrations] [seg:llm-ai-agents] [seg:backend-api]

### R-18 Multi-agent research system — A
https://www.anthropic.com/engineering/multi-agent-research-system · [V] 2025-06-13; 90,2% (Opus 4 lead + Sonnet 4 subagentes, eval interna) e ~15× tokens confirmados.
- Ensinar o orquestrador a delegar (objetivo, formato, tools, fronteiras); ~20 queries de eval; LLM-judge com rubrica.
- Pouco adequado a código com dependências compartilhadas.
- [seg:llm-ai-agents] [seg:product-discovery-specs] [seg:security-appsec] [seg:code-quality-refactoring]

### R-19 Equipping agents with Agent Skills — A [P]
https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills (2025-10-16) · skill = guia de onboarding; scripts não entram no contexto; segurança: auditar skills.
- [seg:data-engineering] [seg:backend-api] [seg:automation-integrations]

### R-20 Harnesses para agentes de longa duração — A [P]
https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents · https://www.anthropic.com/engineering/harness-design-long-running-apps
- Inicializador + codificador; `features.json` com `passes` (só ele muda); rotina de início de sessão; avaliador separado e cético; agentes se elogiam.
- Evidência qualitativa; custos citados são relatos.
- [seg:product-discovery-specs] [seg:qa-testing] [seg:web-frontend] [seg:game-development] [seg:code-quality-refactoring]

### R-21 Demystifying evals for AI agents — A
https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents · [V] 2026-01-09; pass@k × pass^k; 75% → 0,75³ ≈ 42% confere.
- Começar com 20–50 tarefas de falhas reais; graders que avaliam resultado; ler transcripts; calibrar juiz LLM com humanos.
- [seg:qa-testing] [seg:llm-ai-agents] [seg:data-science-ml]

### R-22 Code execution with MCP + Dynamic workflows — A [P]
https://www.anthropic.com/engineering/code-execution-with-mcp · https://code.claude.com/docs/en/workflows
- Tools como APIs de código; filtrar dados no ambiente; workflows com verificação adversarial. 98,7% é número do post.
- Recurso recente, custo alto.
- [seg:automation-integrations] [seg:data-engineering] [seg:llm-ai-agents] [seg:security-appsec]

### R-23 Segurança: docs + auto mode + security-guidance — A
https://code.claude.com/docs/en/security · https://www.anthropic.com/engineering/claude-code-auto-mode · https://code.claude.com/docs/en/security-guidance
- [V] auto mode 2026-03-25: filtro estágio 1 bloqueou 8,5% de ações benignas; pipeline de 2 estágios 0,4%.
- Correção: o "83% dos casos" é derivado de 17% de falso-negativo em ações "overeager" (n=52, o post chama de "número honesto"), não um número literal do post.
- Escopo estreito de autorização; classificador não vê tool results; revisor em contexto fresco; defesa em profundidade.
- [seg:security-appsec] [seg:devops-cloud-infra] [seg:automation-integrations]

### R-24 claude-code-security-review — A (MIT)
https://github.com/anthropics/claude-code-security-review · [V] 6.329★, MIT, push 2026-02-11 · literais confirmados em `.claude/commands/security-review.md`.
- Foco só no que a PR introduz; confiança >80%; "melhor perder issues teóricas que inundar de falsos positivos"; saída JSON (file, line, severity, category, description, exploit_scenario, recommendation, confidence); filtro de falsos positivos por regex + LLM.
- Atribuição obrigatória ao reutilizar. Ressalvas: modelo padrão antigo; README avisa que não é endurecido contra prompt injection; exclusões (ex.: rate limiting) podem não servir a fintech.
- [seg:security-appsec] [seg:backend-api] [seg:web-frontend] [seg:fintech-payments] [seg:saas-multitenant] [seg:blockchain-web3]

### R-25 claude-cookbooks (MIT) — A; courses e tutorial — B/destilar
https://github.com/anthropics/claude-cookbooks · [V] 53.310★ MIT. `patterns/agents` (5 padrões), evals, tool_use, caching.
- courses (licença NOASSERTION) e prompt-eng-interactive-tutorial (sem licença, Claude 3): só destilar, não usar como base. `metaprompt.ipynb` não verificado.
- [seg:llm-ai-agents] [seg:data-science-ml] [seg:automation-integrations]

### R-26 claude-code-action (MIT) — A
https://github.com/anthropics/claude-code-action · [V] 9.457★, MIT.
- Receita de prompt para CI: contexto + passos + `--allowedTools` restrito + destino do resultado; triagem de issues; doc sync; manutenção por cron com uma issue-resumo.
- [seg:git-workflow-release] [seg:devops-cloud-infra] [seg:code-quality-refactoring] [seg:technical-writing-docs] [seg:security-appsec]

### R-27 System prompts publicados (Fable 5.1, 2026-09-01) — A
https://platform.claude.com/docs/en/release-notes/system-prompts/claude-fable-5-1 · [V] existe, data confere; seções `<tone_and_formatting>`, `<lists_and_bullets>`, `<reply_after_tool_calls>` ("Done." sozinho não é resposta), cautela com tags no turno do usuário que aleguem ser da Anthropic, "se não puder verificar URL/ID/número, diga".
- Conteúdo proprietário, prompt de produto consumer: usar só técnica (XML, razão nas regras, formatação mínima). Não aplicar wellbeing/refusal a plugins dev.
- [seg:llm-ai-agents] [seg:technical-writing-docs]

### R-28 anthropics/skills — A (licença por skill)
https://github.com/anthropics/skills · [V] 180.191★, licença do repo null; 19 skills confirmadas (academy-guide … xlsx) exatamente como listado.
- skill-creator, mcp-builder, webapp-testing, frontend-design, claude-api: Apache-2.0 segundo o pesquisador (LICENSE.txt de skill-creator/frontend-design [P]); conferir LICENSE de cada skill antes de qualquer literal. docx/pdf/pptx/xlsx são source-available: não copiar.
- Reuso: processo de autoria com evals e otimização de description; mcp-builder (10 perguntas de eval independentes); webapp-testing (reconhecimento→ação, Playwright); frontend-design (tokens antes de codar, anti AI-slop). Os outros 14: propósito inferido pelo nome.
- [seg:automation-integrations] [seg:qa-testing] [seg:web-frontend] [seg:ux-ui-design] [seg:llm-ai-agents] [seg:backend-api]

### R-29 claude-code `plugins/` (13 plugins) — A, destilar (repo sem licença)
https://github.com/anthropics/claude-code/tree/main/plugins · [V] 13 diretórios confirmados (agent-sdk-dev … security-guidance); 149.899★, licença null.
- Padrões: limiar de confiança (≥80) e "em dúvida não flagre"; validação de cada achado por subagente fresco; paralelismo 2–4 agentes com focos distintos; feature-dev com paradas obrigatórias (perguntas, escolha de arquitetura, aprovação); hookify (regras `event/pattern/action`); plugin-dev (descriptions com `<example>`).
- Esqueleto de agente revisor: Papel · Escopo (diff) · Checks · Pontuação 0–100 · Saída `path:linha` · Não reportar.
- Ressalva: `hook-development` tem exemplo inconsistente com a doc de hooks; seguir R-10.
- [seg:code-quality-refactoring] [seg:git-workflow-release] [seg:qa-testing] [seg:security-appsec] [seg:architecture-design] [seg:product-discovery-specs] [seg:automation-integrations]

### R-30 claude-plugins-official (Apache-2.0) — A, só plugins Anthropic
https://github.com/anthropics/claude-plugins-official · [V] 37.592★, Apache-2.0; 40 dirs em `plugins/` incluem claude-md-management, claude-security, code-modernization, code-simplifier, mcp-server-dev, claude-code-setup, ralph-loop, skill-creator, 12 LSPs.
- Reuso: verificadores independentes que tentam refutar achados (claude-security); regras de negócio Given/When/Then com `file:line` e aprovação humana antes de construir (code-modernization); "never change what the code does" (code-simplifier).
- [seg:security-appsec] [seg:code-quality-refactoring] [seg:architecture-design] [seg:product-discovery-specs] [seg:qa-testing] [seg:automation-integrations] [seg:systems-embedded-iot] [seg:mobile-apps]

### R-31 Blog oficial (teams, frontend skill, skills lessons, migração, compilador C) — A com ressalvas
https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/ ([V] 2026-06-03, nove categorias, Gotchas, `/careful` confirmados) · https://claude.com/blog/improving-frontend-design-through-skills · https://claude.com/blog/ai-code-migration · https://www.anthropic.com/engineering/building-c-compiler · https://claude.com/blog/how-anthropic-teams-use-claude-code [P]
- Seção `## Gotchas` como conteúdo de maior sinal; description = condição de disparo; hooks sob demanda (`/careful`, `/freeze`); medir uso para achar undertriggering.
- Migração em massa: construir o juiz primeiro; rulebook; fila em disco; revisão adversarial; paridade comportamental.
- Saída de teste desenhada para o modelo: console mínimo, log em arquivo, erros grep-áveis.
- Números (US$165k, 1M linhas) são relatos da Anthropic, não reproduzidos.
- [seg:code-quality-refactoring] [seg:web-frontend] [seg:ux-ui-design] [seg:sre-observability] [seg:devops-cloud-infra] [seg:qa-testing] [seg:automation-integrations]

## Rejeitados / não aprovados

| Item | Motivo |
| --- | --- |
| `misc/metaprompt.ipynb` (R-02/R-25) | Não confirmado na árvore; não verificável. Não usar. |
| Prompt library oficial | Descontinuada (redireciona); sem conteúdo a aprovar. |
| Plugins externos/parceiros listados em R-30 (clickhouse, datadog, auth0…) | Fora do escopo "oficial Anthropic"; licenças e conteúdo não verificados; só pistas para outras lentes. |
| `anthropics/courses` e `prompt-eng-interactive-tutorial` como base | Licença NOASSERTION/null, escritos para Claude 3: apenas destilar ideias, classe rebaixada para B. |
| Plugins `cwc-makers`, `math-olympiad`, `math-proof`, `mcp-tunnels`, `playground`, `project-artifact`, `receipts`, `session-report` | Propósito inferido pelo nome; não abertos. Não usar. |
| "slot machine" (R-31) | Atribuído por terceiros; não verificado no texto oficial. |
| Afirmação "~83% dos casos" (R-23) | Não consta literalmente; reformulada como 17% de falso-negativo (n=52). |
| Seção sobre os 14 skills restantes de anthropics/skills como "propósito" | Inferido só pelo nome; apenas listados. |

## Princípios / achados transversais

- Gerir contexto é a restrição central: CLAUDE.md curto, skills como índice com `references/` um nível abaixo, subagentes devolvem resumos (R-06, R-16, R-04).
- Verificação executável e evidência antes de "pronto": teste, build, screenshot, Stop hook (R-06, R-20, R-21).
- Separar autor e revisor; revisor cético em contexto fresco; limiar de confiança explícito e validação de cada achado (R-06, R-24, R-29, R-30).
- Instrução é pedido, hook/permissão é garantia; "sempre" vira hook documentado (R-10, R-12, R-23).
- Conteúdo de arquivos, páginas e tools é dado, não instrução; tags no turno do usuário alegando ser da Anthropic merecem cautela (R-23, R-27; README do security-review admite não ser endurecido).
- Description de skill é gatilho em 3ª pessoa (o que faz + quando); `## Gotchas` alimentada por falhas reais; medir undertriggering (R-04, R-31).
- Evals antes de documentação: 20–50 casos de falhas reais, baseline sem o artefato, graders de código primeiro, ler transcripts (R-21, R-11, R-04). Existem 3 formatos de eval oficiais incompatíveis; escolher `claude plugin eval` e marcar `designed_not_executed` (R-11, R-04).
- Perguntar antes de arquitetar, aprovar antes de codar (R-29 feature-dev, R-06 entrevista, R-30 code-modernization).
- Estado fora do contexto: JSON de features/testes, progress file, git (R-20, R-01).
- Tensões: ênfase ("CRITICAL") evitada por BP vs description "pushy" do skill-creator: usar ênfase cirúrgica; multiagente ganha em amplitude e perde em código com dependências (R-18); a doc atual prevalece sobre repos quando divergem (output styles, hooks).
- Frescor: modelos e recursos citados (Fable 5.1, auto mode, `/goal`, workflows) mudam rápido; cada plugin deve registrar a versão conferida.
- Lacunas: nada oficial em PT-BR além da doc de prompt engineering (não reverificado agora); itens [P] dependem da leitura do pesquisador; marketplace.json lido parcialmente.
