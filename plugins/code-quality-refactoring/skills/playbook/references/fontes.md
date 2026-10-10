# Fontes: bibliografia validada

Consulta: 2026-10-10 (documentação viva da Anthropic: datas de publicação Não verificáveis). Classe A = oficial/alta autoridade e atual; B = referência reconhecida ou oficial com ressalva; C = sinal de prática, uso como ideia. Licença = o que foi observado na pesquisa; "destilar" significa que o plugin usa só redação própria com citação da fonte, sem texto literal. Notas de direitos: nenhum texto literal de fonte sem licença permissiva está neste plugin; as únicas exceções são os rótulos do Conventional Comments (CC BY 3.0, atribuídos) e o material próprio do usuário (MIT).

Sumário: 1 Top 20 · 2 Demais fontes · 3 Fontes rejeitadas ou proibidas de instalar · 4 Base própria e de terceiros MIT · 5 Lacunas de fonte

## 1. Top 20 (por valor para o plugin)

| # | Título | URL | Classe | Licença | Consulta | Itens | Uso |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Claude Code, Best practices | https://code.claude.com/docs/en/best-practices | A | não declarada; destilar | 2026-10-10 | V-01, V-02 | Verificação, revisão adversarial, parada após 2 correções, teste de poda |
| 2 | Claude Code, Common workflows | https://code.claude.com/docs/en/common-workflows | A | não declarada; destilar | 2026-10-10 | V-03 | Receitas de bug, refatoração e testes |
| 3 | obra/superpowers, systematic-debugging | https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md | A | MIT (página do repositório) | 2026-10-10 | V-04 | Quatro fases, regra dos três; texto original usa CAPS, reescrito |
| 4 | anthropics/claude-code, plugin code-review (code-review.md) | https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/commands/code-review.md | A | proprietária ("All rights reserved"); destilar | 2026-10-10 | V-06 | Pipeline de nove passos e filtro de alto sinal |
| 5 | Claude Code, Subagents | https://code.claude.com/docs/en/sub-agents | A | não declarada; destilar | 2026-10-10 | V-09 | Frontmatter, `tools`, limites em plugin |
| 6 | How Anthropic runs large-scale code migrations with Claude Code (2026-07-16) | https://claude.com/blog/ai-code-migration | A | destilar | 2026-10-10 | V-14 | Juiz, rulebook, piloto, fila, paridade |
| 7 | Prompting Claude Fable 5.1 (seção de escopo) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 | A | destilar | 2026-10-10 | V-10 | Pedido = escopo; específico de versão |
| 8 | Claude prompting best practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | A | destilar | 2026-10-10 | V-11 | Anti-overengineering, anti-gaming de teste |
| 9 | anthropics/claude-code-action (+ docs/solutions.md) | https://github.com/anthropics/claude-code-action | A | MIT (página) | 2026-10-10 | V-27 | Revisão de PR em CI (referência) |
| 10 | anthropics/claude-plugins-official, code-simplifier | https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/code-simplifier/agents/code-simplifier.md | B | Apache-2.0 na raiz; por plugin: Inferido | 2026-10-10 | V-12 | "Mudar o como, nunca o quê" |
| 11 | anthropics/claude-plugins-official, code-modernization | https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization | B | Apache-2.0 | 2026-10-10 | V-15 | Uplift/transform/reimagine, veredito de paridade |
| 12 | anthropics/claude-code, pr-review-toolkit (code-reviewer e README) | https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/pr-review-toolkit/agents/code-reviewer.md | B | proprietária no repositório (README diz MIT: conflito); destilar | 2026-10-10 | V-07, V-08 | Faixas de confiança, revisão por aspecto |
| 13 | Google Engineering Practices, what to look for / standard / small CLs | https://google.github.io/eng-practices/review/reviewer/looking-for.html | B | "open source" sem licença nomeada; destilar | 2026-10-10 | V-17, V-18 | Dimensões de revisão, padrão de aprovação, mudança pequena |
| 14 | Michael Feathers, Characterization Testing; Fowler, Self-Testing Code | https://michaelfeathers.silvrback.com/characterization-testing | B | destilar | 2026-10-10 | V-36 | Testes de caracterização |
| 15 | Martin Fowler, Technical Debt e Debt Quadrant | https://martinfowler.com/bliki/TechnicalDebt.html | B | copyright, sem licença; destilar | 2026-10-10 | V-20 | Quadrantes, frequência de mudança |
| 16 | Fowler, Parallel Change; Strangler Fig; catálogo de refatorações | https://martinfowler.com/bliki/ParallelChange.html | B | destilar | 2026-10-10 | V-37, V-21, V-22 | Expandir/migrar/contrair; substituição incremental; vocabulário |
| 17 | OWASP, Secure Code Review Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html | B | CC BY-SA 4.0 (literal exigiria compartilhar igual); destilar | 2026-10-10 | V-38 | Passada de segurança por diff |
| 18 | Conventional Comments | https://conventionalcomments.org/ | B | CC BY 3.0 (literal com atribuição) | 2026-10-10 | V-19 | Rótulos de comentário |
| 19 | brain-of-agent, testes-e-debugging.md (base própria) | `docs/foundation/brain-of-agent-snapshot/brains/fullstack/references/testes-e-debugging.md` | base própria | MIT | 2026-10-09 | V-33 | Revalidação em cinco passos, investigação reproduzível |
| 20 | Dan Luu, Agentic test processes... (AI coding notes) | https://danluu.com/ai-coding/ | B | sem licença; destilar | 2026-10-10 | V-23 | Evidência executável; relato anedótico, sinal |

## 2. Demais fontes usadas

| Título | URL | Classe | Licença | Itens | Uso |
| --- | --- | --- | --- | --- | --- |
| Claude Code power-user tips (Central de Ajuda) | https://support.claude.com/en/articles/14554000-claude-code-power-user-tips | B | destilar | V-13 | `/simplify`, `/batch`, "descartar e refazer"; dependem da versão |
| Building effective agents (2024-12-19) | https://www.anthropic.com/engineering/building-effective-agents | B | destilar | V-16 | Avaliador-otimizador com parada |
| Ruff, Linter | https://docs.astral.sh/ruff/linter/ | B | não verificado | V-39 | Correções seguras, supressões |
| Tricorder (ICSE 2015) | https://research.google/pubs/tricorder-building-a-program-analysis-ecosystem/ | B | não verificado | V-39 | Existência da plataforma de análise; princípios do artigo: Não verificados |
| Sonar, Cognitive Complexity | https://www.sonarsource.com/resources/cognitive-complexity/ | B | "All rights reserved" | V-39 | Só existência; regras não lidas |
| OpenRewrite docs | https://docs.openrewrite.org/ | B | não verificado | V-40 | Receitas determinísticas |
| About Dependabot version updates | https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates | B | destilar | V-40 | PRs de versão; espera de 3 dias |
| Fowler, Technical Debt Quadrant | https://martinfowler.com/bliki/TechnicalDebtQuadrant.html | B | destilar | V-20 | Quatro casos |
| Fowler, Strangler Fig | https://martinfowler.com/bliki/StranglerFigApplication.html | B | destilar | V-21 | Substituição incremental |
| Refactoring catalog | https://refactoring.com/catalog/ | B | não verificado; só nomes | V-22 | Vocabulário de 16 refatorações |
| Fowler, Self-Testing Code | https://martinfowler.com/bliki/SelfTestingCode.html | B | destilar | V-36 | Confiança para mudar |
| Google, standard of code review | https://google.github.io/eng-practices/review/reviewer/standard.html | B | destilar | V-17 | Padrão de aprovação |
| Google, small CLs | https://google.github.io/eng-practices/review/developer/small-cls.html | B | destilar | V-18 | Mudança pequena |
| OpenAI Codex, Custom instructions with AGENTS.md | https://learn.chatgpt.com/docs/agent-configuration/agents-md | B | destilar | V-34 | Formato `Code Review Rules` |
| buildermethods/agent-os | https://github.com/buildermethods/agent-os | B | MIT (página) | V-32 | Só a ideia de descobrir convenções; não instalar |
| github/awesome-copilot, debug.agent.md | https://raw.githubusercontent.com/github/awesome-copilot/main/agents/debug.agent.md | B | MIT na página do repositório; o arquivo não traz texto de licença | V-05 | Ideia de fases do debug |
| github/awesome-copilot, code-review-generic.instructions.md | https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/code-review-generic.instructions.md | C | idem | V-19 | Severidades (emojis removidos) |
| wshobson/agents, debugger.md | https://raw.githubusercontent.com/wshobson/agents/main/plugins/debugging-toolkit/agents/debugger.md | B | MIT (página) | V-05 | Relatório de causa raiz |
| vercel-labs/agent-skills, composition-patterns | https://github.com/vercel-labs/agent-skills | A (React) | MIT | V-28 | Pacote opcional de refatoração React; fora do núcleo |
| Sanity, "First attempt will be 95% garbage" | https://www.sanity.io/blog/first-attempt-will-be-95-garbage | C | destilar | V-24 | Revisão de código de IA em três camadas |
| Boris Tane, How I use Claude Code | https://boristane.com/blog/how-i-use-claude-code/ | C | destilar | V-25 | research → plan → execução |
| Fabien Sanglard, agent.md | https://fabiensanglard.net/agent.md/index.html | C | destilar | V-26 | Três regras de CLAUDE.md |
| PatrickJS/awesome-cursorrules | https://github.com/PatrickJS/awesome-cursorrules | C | CC0-1.0 | V-29 | Ideia de regras anti-alucinação de API |
| garrytan/gstack (README, ideias) | https://github.com/garrytan/gstack | C | MIT; instalação proibida | V-30 | Auditoria de testes; `/investigate`, `/review`, `/health` como ideias |
| Reflexion (Shinn et al., arXiv 2303.11366) | https://arxiv.org/abs/2303.11366 | C | não verificado | V-31 | Reflexão por tentativa com sinal externo |
| Hacker News, itens 49992857, 48963926, 49293760, 48863990 | https://news.ycombinator.com/item?id=49992857 (e os demais ids) | C | comentários; destilar | V-35 | Armadilhas de revisão por IA; anedótico |

## 3. Fontes rejeitadas ou proibidas de instalar

| Fonte | Decisão | Motivo |
| --- | --- | --- |
| VoltAgent (agentes `code-reviewer`, `refactoring-specialist`, `legacy-modernizer`) | Rejeitado como item | Ferramentas amplas em revisores e métricas de exemplo fabricadas (V-09, aviso 5) |
| Instalação do gstack e do agent-os | Proibida | Executa `./setup`, hooks, telemetria (aviso 3) |
| Hooks/telemetria de `code-modernization` | Proibidos | Aviso 4 |
| Regras de estilo de Sanglard (enum, tamanho de função, chaves) | Rejeitadas | Opinião da casa (V-26) |
| README do `pr-review-toolkit` como licença | Não confiável | Diz MIT, mas o repositório é "All rights reserved" (aviso 1) |

## 4. Base própria e de terceiros MIT

- francisco-efjr/brain-of-agent (MIT, base do usuário): `testes-e-debugging.md` incorporado (adaptado), `handoff-checkpoint.md` adaptado em `assets/templates/handoff-checkpoint.md`, convenções de modo completo e rótulos.
- garrytan/gstack (MIT, copyright 2026 Garry Tan, `vendor/gstack/LICENSE` no snapshot): `/investigate`, `/review`, `/health` como inspiração em redação própria; nenhum script, hook, binário ou telemetria copiado.
- obra/superpowers (MIT): ideia das quatro fases do debug, reescrita sem CAPS.
- Conventional Comments (CC BY 3.0): rótulos literais em `revisao-de-codigo.md`, com atribuição.

## 5. Lacunas de fonte (declaradas)

1. Comunidade: só quatro comentários do Hacker News; nenhuma fonte de Reddit, X, YouTube, dev.to ou newsletter.
2. Upgrades: nenhum guia oficial de migração por framework lido; licença do OpenRewrite não verificada.
3. Análise estática por linguagem: ESLint, SonarQube (regras), Semgrep, mypy e o artigo completo do Tricorder não lidos.
4. Clean code por linguagem: nenhum guia de estilo oficial lido (PEP 8, Google style guides, Effective Go); os livros "Clean Code" e "Refactoring" não foram lidos.
5. Dívida técnica quantitativa: nenhum método além de Fowler; frequência x dor é prática derivada (Inferido).
6. Nenhum item tem eval próprio; as eficácias citadas são "da fonte" (V-01, V-10).
7. Datas de publicação de páginas vivas da Anthropic: Não verificável; confira a versão atual antes de citar.
