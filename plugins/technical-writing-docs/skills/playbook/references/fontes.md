# Fontes (bibliografia validada)

Consulta: 2026-10-10 (validador claude-sonnet-5-5, independente do pesquisador, mas da mesma família de modelos: independência parcial). Classes pela rubrica de fontes: A (autoridade e evidência fortes), B (boa, com ressalvas), C (pista). A nota entre parênteses é a soma da rubrica. "Uso": **destilado** = redação própria, sem cópia; **literal** = trecho curto (≤ 40 linhas) permitido pela licença, com atribuição. Itens V-nn estão no relatório de validação da fábrica. Datas de último commit vêm de feeds Atom públicos; estrelas, de páginas HTML (a API do GitHub estava indisponível): trate como sinais, não garantias. Informações sobre versões mudam: reabra a fonte antes de reutilizar.

## Legenda dos códigos internos

Os arquivos do plugin citam códigos curtos. Todos têm destino neste plugin ou nesta tabela:

| Código | Significa | Onde ler |
| --- | --- | --- |
| `V-nn` | Item de fonte validado (URL, classe, licença, data) | Linhas "V" das tabelas abaixo; a lista completa fica no relatório de validação da fábrica, fora do plugin |
| `C-nn` | Conflito entre fontes e a regra adotada (C-01 tamanho da raiz do CLAUDE.md; C-02 AGENTS.md × CLAUDE.md; C-03 gerar com `/init`; C-04 brevidade; C-05 tom de venda no README; C-06 estilo de docstring; C-07 completude × economia; C-08 correção factual direta; C-09 explicar no tutorial; C-10 ASCII × Mermaid; C-11 C4 experimental; C-12 changelog manual × gerado; C-13 `keep-coding-instructions`; C-14 JSDoc × TSDoc; C-15 números de fornecedor) | [decisoes-e-tradeoffs](decisoes-e-tradeoffs.md) e a seção citada em cada arquivo |
| `GS-gen`, `GS-rel` | Passos dos workflows `document-generate` e `document-release` do gstack (MIT), destilados | Seção 3 abaixo |
| `G-nn` | Lacuna conhecida de pesquisa | Seção 5 abaixo |
| `T-nn` | Ferramenta ou hook recomendado e desativado | [ferramentas-e-mcp](ferramentas-e-mcp.md) |
| `S-nn` | Snippet pronto para CLAUDE.md | [claude-md-snippets](claude-md-snippets.md) |
| `PD-nn` | Prompt da biblioteca | skill `prompts`, `references/prompt-library.md` |
| `AP-nn` | Antipadrão | [padroes-e-antipadroes](padroes-e-antipadroes.md) |

## Sumário

Legenda dos códigos internos (acima)

1. Top 20
2. Demais fontes usadas
3. Material próprio e de terceiros incorporado
4. Rejeitadas ou rebaixadas (não usar)
5. Lacunas conhecidas

## 1. Top 20

| # | Título | URL | Classe | Licença | Uso | V |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Claude Code: memória (CLAUDE.md, rules, AGENTS.md, auto memory) | https://code.claude.com/docs/en/memory | A (9) | Doc Anthropic | destilado | V-01, V-48 |
| 2 | Agent Skills: boas práticas de autoria | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | A (9) | Doc Anthropic | destilado | V-04 |
| 3 | `claude-md-improver` (plugin `claude-md-management`) | https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/claude-md-management/skills/claude-md-improver/SKILL.md | A (8) | Apache-2.0 (plugin) | destilado | V-02 |
| 4 | MADR 4.0.0 e "Documenting Architecture Decisions" (Nygard) | https://adr.github.io/madr/ · https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions | A (8) | MADR: MIT OR CC0-1.0; Nygard: dedicação CC0 1.0 na página | destilado (literal permitido) | V-30 |
| 5 | Diátaxis (site e repositório do autor) | https://diataxis.fr/ · https://github.com/evildmp/diataxis-documentation-framework | B (7) | CC BY-SA 4.0 (README do repositório do autor) | destilado | V-11, V-46 |
| 6 | Claude: prompting best practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | A (9) | Doc Anthropic | destilado | V-07 |
| 7 | Docstrings Python: PEP 257, guia do Google (3.8), doctest | https://peps.python.org/pep-0257/ · https://google.github.io/styleguide/pyguide.html · https://docs.python.org/3/library/doctest.html | A (9) | PEP 257: domínio público; guia: CC-By 3.0 (README); doctest: PSF v2, exemplos 0BSD | destilado | V-33 |
| 8 | Skill `doc-coauthoring` | https://raw.githubusercontent.com/anthropics/skills/main/skills/doc-coauthoring/SKILL.md | A (8) | Não verificada | destilado | V-10 |
| 9 | Engenharia de contexto para agentes | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | A (9) | Texto Anthropic | destilado | V-09 |
| 10 | AGENTS.md (formato aberto) | https://agents.md/ · https://github.com/agentsmd/agents.md | A (8) | MIT (repo) | destilado | V-06 |
| 11 | "Evaluating AGENTS.md" (arXiv:2602.11988) | https://arxiv.org/abs/2602.11988 | B (6) | Preprint | citado | V-17 |
| 12 | Output styles do Claude Code | https://code.claude.com/docs/en/output-styles | A (8) | Doc Anthropic | destilado | V-08 |
| 13 | Vale e vale-action | https://github.com/errata-ai/vale · https://docs.vale.sh/ · https://github.com/vale-cli/vale-action | A (9) / B (7) | MIT | destilado | V-37 |
| 14 | lychee e lychee-action | https://github.com/lycheeverse/lychee · https://github.com/lycheeverse/lychee-action · https://lychee.cli.rs/guides/cli/ | A (8) / B (7) | Apache-2.0 ou MIT | destilado | V-39 |
| 15 | markdownlint | https://github.com/DavidAnson/markdownlint | A (9) | MIT | destilado | V-38 |
| 16 | Notas de release geradas pelo GitHub | https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes | A (8) | Não verificada | destilado | V-42 |
| 17 | Keep a Changelog 1.1.0 | https://keepachangelog.com/en/1.1.0/ | B (6) | MIT (rodapé) | destilado (literal permitido) | V-13 |
| 18 | AIP-192 e OpenAPI Best Practices (OAI) | https://google.aip.dev/192 · https://learn.openapis.org/best-practices.html | B (6) | CC BY 4.0 (ambos) | destilado com atribuição | V-41 |
| 19 | Google Developer Documentation Style Guide | https://developers.google.com/style · https://developers.google.com/style/tone · /style/word-list · /style/voice · /style/headings | B (7) | CC BY 4.0 (conteúdo), Apache-2.0 (código) | destilado com atribuição | V-20, V-43 |
| 20 | Runbook: templates de `techdocs-authoring`; SRE Workbook (ideias) | https://raw.githubusercontent.com/pkloehn1/techdocs-authoring/main/skills/authoring-reference/references/templates-and-checklists.md · https://sre.google/workbook/on-call/ | B (6) | Templates: MIT; SRE Workbook: CC BY-NC-ND 4.0 (só ideias) | destilado | V-31 |

## 2. Demais fontes usadas

| Título | URL | Classe | Licença | Uso | V |
| --- | --- | --- | --- | --- | --- |
| `/revise-claude-md` | https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/claude-md-management/commands/revise-claude-md.md | B (6) | Apache-2.0 | destilado | V-03 |
| Especificação Agent Skills | https://agentskills.io/specification | B (7) | Não verificada | destilado | V-05 |
| Skill `documentation-writer` (awesome-copilot) | https://raw.githubusercontent.com/github/awesome-copilot/main/skills/documentation-writer/SKILL.md | B (6) | MIT (repo) | destilado | V-12 |
| Conventional Commits 1.0.0 | https://www.conventionalcommits.org/en/v1.0.0/ | B (6) | CC BY 3.0 | destilado com atribuição | V-14 |
| "Writing a good CLAUDE.md" (HumanLayer) | https://www.humanlayer.dev/blog/writing-a-good-claude-md | B (6) | Blog | destilado | V-15 |
| Augment Code e Addy Osmani (AGENTS.md) | https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files · https://addyosmani.com/blog/agents-md | B (5) / C (4) | Blogs | destilado | V-16 |
| "Why Does CLAUDE.md Keep Growing?" (arXiv:2608.11095) | https://arxiv.org/abs/2608.11095 | B (5) | Preprint | citado | V-18 |
| Lições de Thariq sobre skills | https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/ · https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/main/tips/claude-thariq-tips-17-mar-26.md | B (7) | Blog; compilação sem licença no arquivo | destilado | V-19 |
| Modelo C4 | https://c4model.com/ | B (6) | CC BY 4.0 | destilado com atribuição | V-21 |
| Mermaid (intro) | https://mermaid.js.org/intro/ | B (7) | Projeto Mermaid | destilado | V-22 |
| Mermaid C4; GitHub: criando diagramas; skill `c4-architecture` | https://mermaid.js.org/syntax/c4.html · https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams · https://raw.githubusercontent.com/softaworks/agent-toolkit/main/skills/c4-architecture/SKILL.md | B (7) | Docs; skill: MIT (repo) | destilado | V-44 |
| Write the Docs: guia para iniciantes | https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/ | B (6) | Não verificada | destilado | V-23 |
| OpenAPI Specification 3.2.1 | https://spec.openapis.org/oas/latest.html | B (7) | OAI | destilado | V-24 |
| Regra de README "landing page" (awesome-cursorrules) | https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/readme-best-practices-cursorrules-prompt-file.mdc | B (5) | CC0-1.0 | destilado (literal permitido) | V-25 |
| Changelog do Claude Code | https://code.claude.com/docs/en/changelog | A (8) | Doc Anthropic | citado | V-26 |
| Prompt de criação de CLAUDE.md (Piebald-AI) | https://raw.githubusercontent.com/Piebald-AI/claude-code-system-prompts/main/system-prompts/agent-prompt-claude-md-creation.md | B (7) | Repo MIT; texto é da Anthropic | só ideias | V-27 |
| gstack `document-release` (ideia) | https://raw.githubusercontent.com/garrytan/gstack/main/document-release/SKILL.md | C (4) | MIT | só processo | V-28 |
| Regras escopadas (`.instructions.md`, awesome-copilot) | https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/instructions.instructions.md | B (6) | MIT (repo) | destilado | V-29 |
| Avaliação de `techdocs-authoring` | https://github.com/pkloehn1/techdocs-authoring | B (5) | MIT | reescrito, não adotado | V-32 |
| JSDoc e TSDoc | https://jsdoc.app/about-getting-started · https://tsdoc.org/ | B (6) | JSDoc: CC BY-SA 3.0; TSDoc: não declarada | destilado | V-34 |
| Rustdoc | https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html · https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html | B (7) | Não declarada | destilado | V-35 |
| Javadoc (JDK 21) | https://docs.oracle.com/en/java/javase/21/docs/specs/javadoc/doc-comment-spec.html | B (7) | Oracle, direitos reservados | destilado | V-36 |
| Publicação com GitHub Pages | https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site | A (8) | Não verificada | destilado | V-40 |
| Changelog da Stripe (estrutura) | https://docs.stripe.com/changelog | B (5) | Termos não lidos | só estrutura | V-41 |
| Microsoft: dez dicas de estilo e voz | https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice | B (7) | Copyright reservado | destilado | V-43 |
| Skills `crafting-effective-readmes` e `agent-md-refactor` (softaworks) | https://raw.githubusercontent.com/softaworks/agent-toolkit/main/skills/crafting-effective-readmes/SKILL.md · https://raw.githubusercontent.com/softaworks/agent-toolkit/main/skills/agent-md-refactor/SKILL.md | B (5) | MIT (repo) | reescrito, defeito de aprovação corrigido | V-45 |
| Onboarding de contribuidores (Kubernetes) | https://www.kubernetes.dev/docs/onboarding/ | B (6) | Reuso do site ambíguo | só estrutura | V-47 |
| Discussão HN e blog sobre leitura de AGENTS.md | https://blog.szypowi.cz/p/claude-code-reads-agents.md-only-when-telemetry-is-on/ | terceiro | Blog | só cruzamento com a doc oficial | V-48 |

## 3. Material próprio e de terceiros incorporado

- **brain-of-agent** (francisco-efjr, MIT, Copyright (c) 2026 Brain of Agent contributors): `handoff-checkpoint.md` (adaptado em [handoff-checkpoint](../assets/templates/handoff-checkpoint.md)), `adr.md` do fullstack (variante "com validação") e o padrão de keyword de modo completo. Literal permitido; atribuição mantida.
- **gstack** (garrytan/gstack, MIT, Copyright (c) 2026 Garry Tan; versão 1.91.27 e commit `c285d88b90d39116ccfa2b901f80ea0fce0b26eb` registrados em `THIRD_PARTY_NOTICES.md` do brain-of-agent): processo de `document-generate` (arqueologia do código, matriz entidade → quadrantes, ordem de escrita, portões de qualidade) e de `document-release` (mapa de cobertura, regras de CHANGELOG e VERSION) **destilados com redação própria e atribuição**. Não importados: Step 9 (commit e push), scanner de segredos, telemetria, princípio "boil the ocean" como regra geral.

## 4. Rejeitadas ou rebaixadas (não usar)

gstack `document-release` como skill (telemetria, scripts próprios, autodecisão); gerador de ONBOARDING.md do Piebald; compactação agressiva de CLAUDE.md (TechLoom); `claude-token-efficient` e concisão forçada; mdarena fora de sandbox; dungnotnull; PlantUML como recomendação; Cline Memory Bank como método (só serve como lista de "o que documentar para retomar"); limites do Devin/Cascade (não se aplicam ao Claude Code); `developers.google.com/style/release-notes` (é o changelog do guia, não orientação).

## 5. Lacunas conhecidas

Onboarding de equipe sem fonte (G-01); nenhum prompt verificado para docs de API a partir de contrato (G-02); runbooks de PagerDuty e Atlassian não verificados (G-03); C4 renderizado no GitHub não verificado (G-04); páginas de tópicos da Microsoft e guia de estilo em PT-BR (G-05); comunidade (Reddit, X, YouTube) e MCP de documentação não pesquisados (G-06); exemplos oficiais de release notes (G-07); execuções não testadas (`--offline` via `args`, comando do markdownlint-cli2, `pytest --doctest-modules`, versões das actions de Pages, formato de hook) (G-08); escopos não pesquisados: man pages, microcopy, acessibilidade, i18n (G-09).
