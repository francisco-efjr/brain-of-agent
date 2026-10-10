# Fontes (bibliografia validada)

Todas as URLs foram abertas pelo validador do segmento em **2026-10-10** (coluna "Consulta"); este plugin não reabriu cada página, exceto a página de hooks do Claude Code, relida em 2026-10-10 para `ferramentas-e-mcp.md`. Classe A = documentação oficial ou norma; B = autor ou projeto reconhecido; C = sinal de prática. Nota entre parênteses = pontuação 0 a 10 da rubrica de fontes. "Licença" descreve a licença **identificada**; sem licença identificada, o plugin só destila (redação própria) e cita. Nenhum trecho literal de terceiros foi copiado, exceto conteúdo próprio do usuário (brain-of-agent, MIT) com atribuição.

## Sumário

- [Como ler e como citar](#como-ler-e-como-citar)
- [Classe A](#classe-a)
- [Classe B](#classe-b)
- [Classe C e sinais de prática](#classe-c-e-sinais-de-prática)
- [Conteúdo próprio e workflows de terceiros](#conteúdo-próprio-e-workflows-de-terceiros)
- [Rejeitados e rebaixados](#rejeitados-e-rebaixados)
- [Lacunas conhecidas](#lacunas-conhecidas)

## Como ler e como citar

- `V-nn` aponta para o item correspondente do consolidado de pesquisa deste plugin; use-o ao justificar uma recomendação.
- Flags, APIs e números de versão mudam: sempre confirme na versão instalada (`<ferramenta> --help`, `--version`) antes de copiar um comando.
- Números de blogs e relatos (percentuais, quantidades de execuções) são convenções dos autores. Se citar, inclua a fonte e a ressalva.
- Estrelas e forks de repositórios foram lidos nas páginas HTML; datas de último commit não foram reconferidas (API do GitHub indisponível na validação).

## Classe A

| Item | Título | URL | Licença | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-01 (8) | Best practices do Claude Code | https://code.claude.com/docs/en/best-practices | doc oficial; texto sem licença identificada, destilado | 2026-10-10 | Verificação em 4 graus, evidência, revisor em contexto limpo, falhas comuns; base de `verification-gate`, S-01 |
| V-02 (8) | Plugin evals | https://code.claude.com/docs/en/plugin-evals | idem | 2026-10-10 | Formato de suíte, flags, códigos de saída, limite do Windows (WSL2) |
| V-03 (9) | Demystifying evals for AI agents (Anthropic Engineering, 09/01/2026) | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | idem | 2026-10-10 | Task/trial/grader, pass@k × pass^k, 20 a 50 tarefas de falhas reais |
| V-04 (8) | Develop tests (plataforma Claude) | https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | idem | 2026-10-10 | Critérios mensuráveis para features com LLM, métodos de grading |
| V-05 (9) | Building effective agents | https://www.anthropic.com/engineering/building-effective-agents | idem | 2026-10-10 | Evaluator-optimizer, teto de iterações, sandbox |
| V-06 (8) | Effective harnesses for long-running agents (26/11/2025) | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | idem | 2026-10-10 | Feature list com `passes`, protocolo de sessão, "editar teste é inaceitável" |
| V-07 (8) | Building a C compiler (05/02/2026) | https://www.anthropic.com/engineering/building-c-compiler | idem | 2026-10-10 | Saída de teste desenhada para o modelo, `--fast` determinístico |
| V-08 (8) | Sub-agents | https://code.claude.com/docs/en/sub-agents | idem | 2026-10-10 | Formato de agente; plugins ignoram `hooks`, `mcpServers`, `permissionMode` |
| V-09 (8) | Skills | https://code.claude.com/docs/en/skills | idem | 2026-10-10 | `description` cortada em 1.536 caracteres na listagem; `disable-model-invocation` |
| V-10 (8, existência) | claude-plugins-official | https://github.com/anthropics/claude-plugins-official | Apache-2.0 no repositório; licença própria por plugin | 2026-10-10 | Referência de existência; nenhum plugin lido (lacuna) |
| V-11 (8) | Skill `webapp-testing` | https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md | Apache-2.0 (LICENSE.txt da pasta) | 2026-10-10 | Reconhecimento em 5 passos; não embute `with_server.py` |
| V-18 (9) | WCAG 2.2 (W3C, Recomendação de 12/12/2024) e W3C WAI evaluation | https://www.w3.org/TR/WCAG22/ · https://www.w3.org/WAI/test-evaluate/ | licença do texto não verificada, destilado | 2026-10-10 | Auditoria em 3 camadas; nenhuma ferramenta determina conformidade |
| V-19 (8) | Playwright best practices | https://playwright.dev/docs/best-practices | docs do produto; licença do texto não verificada | 2026-10-10 | Núcleo do checklist de E2E |
| V-20 (8) | Playwright test agents | https://playwright.dev/docs/test-agents | idem | 2026-10-10 | Planner/generator/healer e guardrail |
| V-21 (8) | Playwright test retries | https://playwright.dev/docs/test-retries | idem | 2026-10-10 | Classificação passed/flaky/failed; base A de "retry é sinal" |
| V-23 (8) | k6 test types (Grafana) | https://grafana.com/docs/k6/latest/testing-guides/test-types/ | idem | 2026-10-10 | Tipos de teste de performance (sem limiares) |
| V-24 (8) | Cypress best practices (atualizada em 20/09/2026) | https://docs.cypress.io/app/core-concepts/best-practices | idem | 2026-10-10 | `cy.session`, limpeza em `beforeEach`, sem espera numérica |
| Hooks | Hooks do Claude Code (releitura parcial: 100 mil de 262 mil caracteres) | https://code.claude.com/docs/en/hooks | doc oficial, destilado | 2026-10-10 | Formato dos JSON de T-03 e T-04 |

## Classe B

| Item | Título | URL | Licença | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-12 (7) | AI Evals: Everything You Need to Know (Husain e Shankar; 18/09/2026) | https://hamel.dev/blog/posts/evals-faq/ | não identificada | 2026-10-10 | Binário × Likert, código antes de juiz, TPR/TNR; "opiniões fortes, não verdades universais" |
| V-13 (5) | LLM evaluators (Eugene Yan; ago/2024) | https://eugeneyan.com/writing/llm-evaluators/ | não identificada | 2026-10-10 | Checklist de viés de juiz (modelos antigos: direção, não medida) |
| V-14 (7) | The Practical Test Pyramid (Vocke, 26/02/2018) e Write tests (Dodds, 13/07/2019) | https://martinfowler.com/articles/practical-test-pyramid.html · https://kentcdodds.com/blog/write-tests | não identificada | 2026-10-10 | Camadas, retorno decrescente de cobertura |
| V-15 (6) | fast-check e Stryker | https://fast-check.dev/docs/introduction/ · https://stryker-mutator.io/docs/ | não verificada | 2026-10-10 | Property-based e mutation (item fino) |
| V-16 (7) | Pact | https://docs.pact.io/ · https://docs.pact.io/getting_started/how_pact_works | não verificada | 2026-10-10 | Contrato consumer-driven |
| V-17 (6) | BDD (Cucumber) | https://cucumber.io/docs/bdd/ | não verificada | 2026-10-10 | Discovery/Formulation/Automation; a página não traz Given/When/Then |
| V-22 (7) | Testing Library: princípios e prioridade de queries | https://testing-library.com/docs/guiding-principles/ · https://testing-library.com/docs/queries/about/#priority | não verificada | 2026-10-10 | Prioridade de seletores |
| V-25 (7) | Vitest mocking | https://vitest.dev/guide/mocking | não verificada | 2026-10-10 | Resetar mocks, relógio e globals |
| V-26 (5) | Schemathesis | https://schemathesis.readthedocs.io/en/stable/ · https://schemathesis.readthedocs.io/en/stable/quick-start/ | não identificada nas páginas | 2026-10-10 | Teste de API a partir de OpenAPI (só local/staging) |
| V-27 (6) | Mozilla Bug Writing Guidelines | https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html | não identificada | 2026-10-10 | Base do template de bug |
| V-28 (6) | Red/green TDD e Agentic manual testing (Simon Willison, sem data nas páginas) | https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/ · https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/ | não declarada | 2026-10-10 | "Use red/green TDD", executar sempre o código gerado |
| V-29 (6) | Notas de Dan Luu sobre agentes e testes | https://danluu.com/ai-coding/ | não identificada | 2026-10-10 | Limites da verificação por LLM (anedótico, segundo o autor) |
| V-30 (5) | Ralph (Geoffrey Huntley; 14/07/2025) | https://ghuntley.com/ralph/ | não identificada | 2026-10-10 | Back pressure; a fonte não traz aviso de sandbox |
| V-31 (7) | superpowers: `test-driven-development` e `writing-good-tests` | https://raw.githubusercontent.com/obra/superpowers/main/skills/test-driven-development/SKILL.md · https://raw.githubusercontent.com/obra/superpowers/main/skills/test-driven-development/writing-good-tests.md | MIT | 2026-10-10 | Vermelho/verde/refatora, mutation check; tom absolutista a calibrar |
| V-32 (7) | superpowers: `verification-before-completion` | https://raw.githubusercontent.com/obra/superpowers/main/skills/verification-before-completion/SKILL.md | MIT | 2026-10-10 | Gate de 5 passos, tabela afirmação → evidência |
| V-33 (7) | Matt Pocock: `tdd` | https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/tdd/SKILL.md | MIT | 2026-10-10 | Anti-padrões (acoplado, tautológico, horizontal), seams |
| V-34 (7) | Matt Pocock: `diagnosing-bugs` | https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/diagnosing-bugs/SKILL.md | MIT (repositório mattpocock/skills) | 2026-10-10 | Loop de feedback primeiro, hipóteses falsificáveis, redação de segredos |
| V-35 (6) | gstack: `qa-only`, `qa`, `test-audit` | https://raw.githubusercontent.com/garrytan/gstack/main/qa-only/SKILL.md · https://raw.githubusercontent.com/garrytan/gstack/main/test-audit/SKILL.md | MIT (repositório garrytan/gstack) | 2026-10-10 | Relatar × corrigir, cartão de valor, cartão de aposentadoria |
| V-36 (7) | awesome-copilot: QA engineering best practices | https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/qa-engineering-best-practices.instructions.md | MIT | 2026-10-10 | Checklist de revisão; percentuais são convenção |
| V-38 (5) | UiPath `coder_eval` | https://github.com/UiPath/coder_eval | Apache-2.0 | 2026-10-10 | Inspiração de critérios ponderados; `tempdir` não isola |
| V-39 (5) | awesome-cursorrules: `qa-bug-report` | https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/qa-bug-report-cursorrules-prompt-file.mdc | CC0-1.0 | 2026-10-10 | Escala de severidade e template (raso frente a V-27) |
| V-40 (5) | ykdojo/claude-code-tips (dica 48, `TESTING.md`) | https://github.com/ykdojo/claude-code-tips | não identificada na página | 2026-10-10 | Agente documenta como testou |
| V-41 (6) | Ask HN: What is your (AI) dev tech stack / workflow? | https://news.ycombinator.com/item?id=48413629 | relatos | 2026-10-10 | Sinal de prática: agente edita teste; tags de estado |

## Classe C e sinais de prática

| Item | Título | URL | Licença | Consulta | Observação |
| --- | --- | --- | --- | --- | --- |
| V-37 (4, cruzada com A) | qa-skills: `test-reliability` | https://raw.githubusercontent.com/petrkindlmann/qa-skills/main/skills/test-reliability/SKILL.md | MIT | 2026-10-10 | Sete causas de flaky; números 14 dias, 5% e 50 execuções são convenção do autor ("valores iniciais ajustáveis"); cruzar com V-19, V-21, V-24 |
| Relato | Yonatan Kra (25/11/2025): 5 de 18 specs geradas falharam | não reaberto neste plugin | n/a | 2026-10-10 | Evidência de testes gerados que checam propriedades privadas; sem método |

## Conteúdo próprio e workflows de terceiros

| Fonte | Licença | Uso |
| --- | --- | --- |
| brain-of-agent (francisco-efjr/brain-of-agent, commit 0d025fb): `brains/qa/SKILL.md`, `references/{protocolo-qa-completo, estrategia, design-de-testes, unitarios-e-integracao, bugs-e-relatorios, automacao-web, ia-e-llm, dados-ambientes-ci}.md`, templates, e `brains/fullstack/references/testes-e-debugging.md` | MIT, conteúdo próprio do usuário | Incorporado e adaptado ao formato de plugin, com atribuição; **não reverificado em fonte externa** (Inferido). Números regulatórios e datas (CLT arts. 134 e 145, CDC arts. 42 e 49, LGPD art. 6º III, ISO/IEC 25010:2023, DORA 2024, NIST SP 800-63B, CNPJ alfanumérico, DO-178C, ISO 26262) são pontos de partida: confirme norma e vigência |
| gstack (Garry Tan), workflows `qa`, `qa-only`, `test-audit` | MIT | Inspiração de processo com atribuição; sem cópia em bloco; sem preâmbulo, telemetria nem instalação |
| superpowers (Jesse Vincent, obra/superpowers) | MIT | Inspiração do gate de verificação e do ciclo TDD; redação própria, tom calibrado |
| mattpocock/skills | MIT | Inspiração de anti-padrões de TDD e do loop de diagnóstico; redação própria |

## Rejeitados e rebaixados

| Item | Decisão | Motivo |
| --- | --- | --- |
| Regra `playwright-e2e` (awesome-cursorrules) | Rejeitada | Exemplo com rota relativa, `route.fulfill` sem corpo/`contentType` realistas e seletores via `data-testid`; V-19 é superior |
| `PramodDutta/qaskills` | Rejeitado | Instalação por `npx @qaskills/cli` e MCP via `npx -y` executa pacote de terceiros; notas auto-atribuídas |
| `Visma-Severa/QA-Agents` | Rejeitado | Arquivado pelo dono em 11/06/2026; nada lido |
| Sanity ("First attempt will be 95% garbage") | C (4) | Relato de 6 semanas, taxas auto-relatadas |
| `lackeyjb/playwright-skill`, TIL de Willison sobre Playwright MCP | C (4) | Instalação por `npm run setup`/`npx skills add`; MCP com `@latest` de terceiros |
| Google Testing Blog sobre flaky | Não usado | A página só entregou comentários de leitores |
| "Avaliador cético separado" atribuído ao harness da Anthropic | Descartado | V-06 mostra um único agente verificando o próprio trabalho |
| "Proibido afrouxar testes" atribuído a Ralph/HAMY | Descartado como fonte | Não consta nos textos lidos; a regra se apoia em V-06 e V-41 |

## Lacunas conhecidas

Não lidos ou sem fonte A/B: plugins oficiais `pr-review-toolkit`, `code-review`, `skill-creator`, `ralph-loop`; ISTQB e ISO/IEC/IEEE 29119-3; SBTM (PDF); Jest oficial; seeds e replay do fast-check, Hypothesis; mutantes equivalentes no Stryker; política de quarentena fonte A/B; Cypress retries; factories e anonimização de dados de teste; Postman/REST Assured e OWASP API Top 10; limiares e SLO do k6; referência de Gherkin; axe/Lighthouse/pa11y; Reddit, X, YouTube, dev.to e newsletters. Datas de último commit dos repositórios não foram reconferidas.
