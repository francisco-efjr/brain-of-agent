# Fontes

Bibliografia do plugin `product-discovery-specs`. Todas as consultas e verificações datam de **2026-10-10** (pesquisa e validação da fábrica dev-segments; por tratar-se de leitura por ferramenta de modelos, a independência é parcial e a revisão humana continua recomendada). Estrelas, licenças e datas vêm das fontes indicadas e podem ter mudado: confira antes de citar.

Classes (rubrica da casa): **A** = oficial ou normativa ou repositório de alta autoridade; **B** = especialista, repositório bem avaliado ou documento secundário confiável; **C** = sinal de comunidade, nunca prova única. Nenhum trecho literal de terceiros foi reproduzido; tudo é destilado com redação própria, salvo conteúdo próprio do autor (MIT).

## Sumário

- [1. Fontes aprovadas V-01 a V-45](#1-fontes-aprovadas-v-01-a-v-45)
- [2. Base própria e inspirações](#2-base-própria-e-inspirações)
- [3. Sinais C e fontes não usadas](#3-sinais-c-e-fontes-não-usadas)
- [4. Lacunas de evidência](#4-lacunas-de-evidência)
- [5. Créditos e licenças](#5-créditos-e-licenças)

## 1. Fontes aprovadas V-01 a V-45

"Licença" indica o que se sabe sobre reuso do texto; onde consta "destilar", só redação própria é permitida.

| ID | Título | URL | Classe | Licença | Consulta |
| --- | --- | --- | --- | --- | --- |
| V-01 | Best practices for Claude Code, seção "Let Claude interview you" | https://code.claude.com/docs/en/best-practices | A | não verificada; destilar | 2026-10-10 |
| V-02 | Best practices for Claude Code, "Explore first, then plan, then code" e "Give Claude a way to verify its work" | https://code.claude.com/docs/en/best-practices | A | não verificada; destilar | 2026-10-10 |
| V-03 | Best practices for Claude Code, "Add an adversarial review step" | https://code.claude.com/docs/en/best-practices | A | não verificada; destilar | 2026-10-10 |
| V-04 | Skill authoring best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | A | não verificada; destilar | 2026-10-10 |
| V-05 | `skill-creator` (anthropics/skills) | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md | A | Apache-2.0, Copyright 2026 Anthropic, PBC (`LICENSE.txt` da pasta) | 2026-10-10 |
| V-06 | Effective harnesses for long-running agents (2025-11-26) | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | A | não verificada; destilar | 2026-10-10 |
| V-07 | How we built our multi-agent research system (2025-06-13) | https://www.anthropic.com/engineering/multi-agent-research-system | A | não verificada; destilar | 2026-10-10 |
| V-08 | Estudo de expertise em Claude Code (2026-06-16) | https://www.anthropic.com/research/claude-code-expertise | B | não verificada; destilar (apenas como princípio descritivo) | 2026-10-10 |
| V-09 | spec-kit, `spec-template.md` | https://raw.githubusercontent.com/github/spec-kit/main/templates/spec-template.md | A | MIT, Copyright GitHub, Inc. | 2026-10-10 |
| V-10 | spec-kit, `tasks-template.md` | https://raw.githubusercontent.com/github/spec-kit/main/templates/tasks-template.md | A | MIT, Copyright GitHub, Inc. | 2026-10-10 |
| V-11 | Spec-driven development with AI (GitHub Blog, Den Delimarsky, 2025-09-02) | https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/ | B | não verificada; destilar | 2026-10-10 |
| V-12 | awesome-copilot, `spec-driven-workflow-v1.instructions.md` | https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/spec-driven-workflow-v1.instructions.md | B | MIT no repositório; arquivo sem licença própria | 2026-10-10 |
| V-13 | awesome-copilot, `implementation-plan.agent.md` | https://raw.githubusercontent.com/github/awesome-copilot/main/agents/implementation-plan.agent.md | B (nota 5) | MIT no repositório | 2026-10-10 |
| V-14 | awesome-copilot, `adr-generator.agent.md` | https://raw.githubusercontent.com/github/awesome-copilot/main/agents/adr-generator.agent.md | B | MIT no repositório | 2026-10-10 |
| V-15 | obra/superpowers, `brainstorming/SKILL.md` | https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md | A | MIT, Copyright (c) 2025 Jesse Vincent | 2026-10-10 |
| V-16 | Gherkin reference (Cucumber) | https://cucumber.io/docs/gherkin/reference/ | A | sem licença de reuso declarada; destilar | 2026-10-10 |
| V-17 | Writing better Gherkin (Cucumber) | https://cucumber.io/docs/bdd/better-gherkin/ | A | idem | 2026-10-10 |
| V-18 | INVEST (Agile Alliance); alternativa MIT: phuryn/pm-skills `user-stories` | https://agilealliance.org/glossary/invest | A | glossário sem licença declarada; destilar. As perguntas-teste são Inferido | 2026-10-10 |
| V-19 | User stories (Mountain Goat Software; atualizada 2026-07-12) | https://www.mountaingoatsoftware.com/agile/user-stories | B | destilar | 2026-10-10 |
| V-20 | EARS (síntese; original: Mavin et al., RE'09, não lido) | https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax | B | Wikipedia; destilar | 2026-10-10 |
| V-21 | RICE (Sean McBride, Intercom, 2018-01-05) | https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/ | B | destilar | 2026-10-10 |
| V-22 | Kano model | https://en.wikipedia.org/wiki/Kano_model | B | Wikipedia; destilar; conferir original | 2026-10-10 |
| V-23 | MoSCoW method | https://en.wikipedia.org/wiki/MoSCoW_method | B | Wikipedia; destilar | 2026-10-10 |
| V-24 | phuryn/pm-skills, `prioritization-frameworks` (inclui ICE) | https://raw.githubusercontent.com/phuryn/pm-skills/main/pm-execution/skills/prioritization-frameworks/SKILL.md | B | MIT | 2026-10-10 |
| V-25 | The Four Big Risks (Marty Cagan, SVPG, 2017-12-04) | https://www.svpg.com/four-big-risks/ | B | destilar | 2026-10-10 |
| V-26 | Shape Up (Ryan Singer, Basecamp/37signals) | https://basecamp.com/shapeup | B | Copyright 1999-2026 37signals LLC; **nunca reproduzir**, apenas destilar | 2026-10-10 |
| V-27 | How Not To Run an A/B Test (Evan Miller, 2010-04-18) | https://www.evanmiller.org/how-not-to-run-an-ab-test.html | B | destilar | 2026-10-10 |
| V-28 | 10 lessons for agentic coding (Drew Breunig, 2026-05-04) | https://www.dbreunig.com/2026/05/04/10-lessons-for-agentic-coding.html | B | destilar | 2026-10-10 |
| V-29 | anthropics/claude-code, plugin `feature-dev` (comando `feature-dev.md`) | https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/feature-dev/commands/feature-dev.md | A | licença do repositório não visível; destilar | 2026-10-10 |
| V-30 | `feature-dev`, agente `code-architect.md` | https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/feature-dev/agents/code-architect.md | A | idem | 2026-10-10 |
| V-31 | claude-plugins-official, plugin `code-modernization` (RULE-NNN) | https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization | A | Apache-2.0 | 2026-10-10 |
| V-32 | Opportunity Solution Tree (Teresa Torres, Product Talk); implementação MIT em phuryn/pm-skills | https://www.producttalk.org/opportunity-solution-tree/ | B | Product Talk sem licença de reuso; skill phuryn MIT | 2026-10-10 |
| V-33 | phuryn/pm-skills, `interview-script` | https://raw.githubusercontent.com/phuryn/pm-skills/main/pm-product-discovery/skills/interview-script/SKILL.md | B | MIT | 2026-10-10 |
| V-34 | awesome-copilot, skill `prd` | https://raw.githubusercontent.com/github/awesome-copilot/main/skills/prd/SKILL.md | B | MIT (frontmatter) | 2026-10-10 |
| V-35 | phuryn/pm-skills, `create-prd` (e `breakdown-feature-prd` do awesome-copilot) | https://raw.githubusercontent.com/phuryn/pm-skills/main/pm-execution/skills/create-prd/SKILL.md | B | MIT | 2026-10-10 |
| V-36 | product-on-purpose/pm-skills, `deliver-acceptance-criteria` | https://raw.githubusercontent.com/product-on-purpose/pm-skills/main/skills/deliver-acceptance-criteria/SKILL.md | B | Apache-2.0 | 2026-10-10 |
| V-37 | snarktank/ralph, skill `prd` | https://raw.githubusercontent.com/snarktank/ralph/main/skills/prd/SKILL.md | B | MIT | 2026-10-10 |
| V-38 | nurettincoban/ai-prd-workflow (README) | https://raw.githubusercontent.com/nurettincoban/ai-prd-workflow/main/README.md | B (nota 5) | MIT; o README oferece `curl ... \| bash`, não recomendado | 2026-10-10 |
| V-39 | Understanding Spec-Driven-Development: Kiro, spec-kit and Tessl (Birgitta Böckeler, 2025-10-15) | https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html | A | sem licença de reuso; destilar | 2026-10-10 |
| V-40 | How I use Claude Code (Boris Tane, 2026-02-10) | https://boristane.com/blog/how-i-use-claude-code/ | B | destilar | 2026-10-10 |
| V-41 | Kiro, Specs (atualizada em 2026-10-02) | https://kiro.dev/docs/specs/ | B | texto de vendor; destilar | 2026-10-10 |
| V-42 | brain-of-agent, `brains/qa/references/requisitos-e-bdd.md` | `docs/foundation/brain-of-agent-snapshot/brains/qa/references/requisitos-e-bdd.md` (repositório da fábrica) | A (base própria) | MIT, do autor; literal permitido | 2026-10-10 |
| V-43 | Set goals with OKRs (Google re:Work) | https://rework.withgoogle.com/intl/en/guides/set-goals-with-okrs | B | destilar | 2026-10-10 |
| V-44 | The Scrum Guide 2020 (Schwaber e Sutherland) | https://scrumguides.org/scrum-guide.html | B | licença do texto não verificável; destilar | 2026-10-10 |
| V-45 | Now-Next-Later roadmap (ProdPad) | https://www.prodpad.com/blog/invented-now-next-later-roadmap/ | B (nota 5) | autoatribuída, comercial; destilar | 2026-10-10 |

## 2. Base própria e inspirações

| Fonte | Uso | Licença |
| --- | --- | --- |
| brain-of-agent (github.com/francisco-efjr/brain-of-agent), `brains/qa/references/requisitos-e-bdd.md` | Base de `criterios-e-historias.md` e dos templates `revisao-de-historia.md`, `exemplo.feature` | MIT, do autor |
| brain-of-agent, `brains/fullstack/assets/templates/handoff-checkpoint.md`, `adr.md`, `plano-incremento.md` | Base dos templates `handoff.md`, `decisao-produto.md`, `plano-entrega.md` | MIT, do autor |
| brain-of-agent, `docs/contexto/brain-of-agent-contexto-completo.md` | Campos da mensagem inicial sugerida; convenções (proporcionalidade, rótulos epistêmicos, keyword de modo completo) | MIT, do autor |
| brain-of-agent, `brains/qa/references/protocolo-qa-completo.md` | Estrutura do contrato de ativação, leitura em lotes e revalidação do modo PRODUTO-COMPLETO | MIT, do autor |
| gstack (github.com/garrytan/gstack), workflows `office-hours`, `plan-ceo-review`, `spec` | Inspiração de processo (premissas, alternativas, posturas de escopo, ledger de decisões, rodadas de especificação); **sem cópia de texto**, sem binários, telemetria nem jargão de marca | MIT, Copyright (c) 2026 Garry Tan (`vendor/gstack/LICENSE` do snapshot) |

Seções complementares do gstack citadas pelos workflows (`sections/*.md`) não estavam no snapshot e são **Não verificáveis**.

## 3. Sinais C e fontes não usadas

| Fonte | Decisão | Motivo |
| --- | --- | --- |
| Hacker News: "Ask HN: still using SDD?" (2026-02-03), "still pay off with frontier models?" (2026-09-24), listagens de spec-driven | Sinal C | Baixo engajamento, opiniões individuais; incorporado só como calibração em V-39 |
| deanpeters/Product-Manager-Skills (`user-story`, `jobs-to-be-done`) | **Texto não usado** | Licença CC BY-NC-SA 4.0, incompatível com redistribuição comercial |
| aakashg (CLAUDE.md de PM), "PRD-driven context engineering", Pimzino (Claude Code Spec Workflow) | Sinal C | Modelo promocional, instalação por script não lido, projeto com foco migrado |
| Dwyer, SPEC.md curto | **Rejeitado** | Recomenda `--dangerously-skip-permissions` como padrão |
| Blogs promocionais de SDD (Medium, DataCamp, DEV) | Rejeitado como fonte | Promocionais, artefatos "reais" não verificáveis |
| Reddit | Lacuna | Bloqueado para a ferramenta; nenhum post lido |

## 4. Lacunas de evidência

Conteúdo correspondente sai rotulado B ou Inferido:

1. JTBD sem fonte primária (Christensen, Ulwick, forças de progresso de Moesta); Mom Test sem o livro lido.
2. Experimentação: sem OEC, métricas de guarda, SRM nem análise sequencial além de V-27.
3. Métricas de produto: North Star, HEART, AARRR sem fonte aprovada.
4. Roadmap: Now-Next-Later é a única fonte (autoatribuída); sem roadmap por resultado.
5. Refinamento, three amigos e Example Mapping: fonte é a base própria (V-42); falta fonte A (Cucumber, Matt Wynne). A definição de "ready" não é prescrita pelo Scrum Guide 2020: `story-ready` é construção do plugin.
6. Priorização: WSJF e Kano original sem fonte primária; ICE só via phuryn (V-24).
7. Português do Brasil: nenhum prompt ou repositório de PRD ou spec em pt-BR foi encontrado; todo o texto em português é tradução e destilação nossa.
8. Licenças pendentes: `anthropics/claude-code` (feature-dev) e `anthropics/skills` (nível de repositório) sem licença visível; docs da Anthropic e do Cucumber sem licença de reuso declarada: só destilar.
9. Construções nossas, sem fonte: critério de conclusão por fase do plano (V-13 não o tem), `story-ready`, limiares N0 a N4, limite de 3 perguntas, perguntas-teste do INVEST, definição operacional de métrica.

## 5. Créditos e licenças

| Projeto | Licença | Como é usado aqui |
| --- | --- | --- |
| GitHub spec-kit | MIT, Copyright GitHub, Inc. | Estrutura de spec e de tarefas, reescrita |
| obra/superpowers | MIT, Copyright (c) 2025 Jesse Vincent | Fluxo de brainstorming com gate, reescrito sem o tom de proibição |
| github/awesome-copilot | MIT | Ideias de PRD, plano com IDs e ADR, reescritas |
| anthropics/skills (`skill-creator`), anthropics/claude-plugins-official (`code-modernization`) | Apache-2.0, Anthropic | Ciclo de avaliação de skills e `RULE-NNN`, destilados |
| phuryn/pm-skills | MIT | Roteiro de entrevista, PRD enxuto, priorização, árvore de oportunidades, destilados |
| product-on-purpose/pm-skills | Apache-2.0 | Checklist de critérios Given/When/Then, destilado |
| snarktank/ralph | MIT | Regras de tamanho de história e de formato de perguntas, destiladas |
| brain-of-agent | MIT, Francisco Edson | Incorporado, com adaptação |
| gstack | MIT, Copyright (c) 2026 Garry Tan | Inspiração de processo, com atribuição |

Textos de Anthropic (docs e engenharia), Cucumber, Intercom, Shape Up, SVPG, Evan Miller, Mountain Goat, Breunig, Torres, Google re:Work, Scrum Guide, ProdPad e Kiro foram apenas destilados com redação própria.
