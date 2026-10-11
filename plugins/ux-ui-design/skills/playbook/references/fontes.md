# Fontes do plugin ux-ui-design

Bibliografia validada. Classe A = oficial (Anthropic, mantenedor da tecnologia, norma); B = prática reconhecida (empresa, autor conhecido, repositório mantido); C = comunidade, só como ideia. Todas as URLs abaixo foram abertas pela validação do segmento em 2026-10-10 (pesquisador e validador da mesma família de modelo: independência parcial). Os códigos `V-nn` identificam o item de validação que sustenta cada fonte; as referências deste plugin os citam. "Destilar" significa: o conteúdo do plugin é redação própria, sem texto copiado, porque a licença do original é desconhecida ou proprietária. Estrelas, forks e datas de push mudam: não os use como prova de qualidade (confira com `gh api` ou na página do repositório, na data do uso).

## Sumário

- [Claude Code e Anthropic](#claude-code-e-anthropic)
- [Normas e plataformas](#normas-e-plataformas)
- [Pesquisa, heurísticas e escrita](#pesquisa-heurísticas-e-escrita)
- [Design systems e tokens](#design-systems-e-tokens)
- [Repositórios e práticas B](#repositórios-e-práticas-b)
- [Base própria e inspiração com atribuição](#base-própria-e-inspiração-com-atribuição)
- [Não usar como regra](#não-usar-como-regra)
- [Datas, versões e onde reconferir](#datas-versões-e-onde-reconferir)

## Claude Code e Anthropic

| V | Título | URL | Classe | Licença | Consulta |
| --- | --- | --- | --- | --- | --- |
| V-01 | Skill `frontend-design` (anthropics/skills) | https://github.com/anthropics/skills/tree/main/skills/frontend-design | A | Apache-2.0 via `LICENSE.txt` da skill (a API do repositório devolve licença nula) | 2026-10-10 |
| V-02 | Cookbook "Prompting for frontend aesthetics" | https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics | B | sem licença declarada: destilar | 2026-10-10 |
| V-02 | Blog "Improving frontend design through skills" | https://claude.com/blog/improving-frontend-design-through-skills | B | sem licença declarada: destilar | 2026-10-10 |
| V-03 | Harness design for long-running apps (Anthropic Engineering, 2026-03-24) | https://www.anthropic.com/engineering/harness-design-long-running-apps | B | destilar | 2026-10-10 |
| V-04 | Claude Code best practices | https://code.claude.com/docs/en/best-practices | A | docs Anthropic: destilar | 2026-10-10 |
| V-05 | Agent Skills best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | A | destilar | 2026-10-10 |
| V-06 | `skill-creator` SKILL.md | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md | A | não declarada: destilar | 2026-10-10 |
| V-07 | Output styles | https://code.claude.com/docs/en/output-styles | A | destilar | 2026-10-10 |
| V-13 | `ux-copy` (anthropics/knowledge-work-plugins) | https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/design/skills/ux-copy/SKILL.md | A | Apache-2.0 (repositório: https://github.com/anthropics/knowledge-work-plugins) | 2026-10-10 |
| V-15 | `user-research` (anthropics/knowledge-work-plugins) | https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/design/skills/user-research/SKILL.md | A | Apache-2.0 | 2026-10-10 |

## Normas e plataformas

| V | Título | URL | Classe | Licença | Consulta |
| --- | --- | --- | --- | --- | --- |
| V-08 | WCAG 2.2 (Recommendation de 2024-12-12) | https://www.w3.org/TR/WCAG22/ | A | documento W3C, licença de documento não verificada: destilar | 2026-10-10 |
| V-08 | WCAG 2.2 Quick Reference | https://www.w3.org/WAI/WCAG22/quickref/ | A | idem | 2026-10-10 |
| V-10 | ARIA APG: diálogo modal | https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ | A | W3C: destilar | 2026-10-10 |
| V-09 | `a11y.instructions.md` (github/awesome-copilot) | https://github.com/github/awesome-copilot/blob/main/instructions/a11y.instructions.md | A | MIT (API do repositório) | 2026-10-10 |
| V-36 | web.dev: Interaction to Next Paint (publicado 2022-05-06, atualizado 2025-09-02) | https://web.dev/articles/inp | A | destilar | 2026-10-10 |
| Q-01 | web.dev: Cumulative Layout Shift (atualizado 2023-04-12; conferido pelo validador de qualidade, fora de VALIDATED) | https://web.dev/articles/cls | A | destilar | 2026-10-10 |
| V-38 | web.dev: prefers-reduced-motion (atualização exibida: 2019-03-11) | https://web.dev/articles/prefers-reduced-motion | B | destilar | 2026-10-10 |
| V-39 | Apple HIG: Accessibility (conteúdo lido pelo endpoint de dados `https://developer.apple.com/tutorials/data/design/human-interface-guidelines/accessibility.json`, não documentado) | https://developer.apple.com/design/human-interface-guidelines/accessibility | B | © Apple: só destilar | 2026-10-10 |
| V-34 | Primer: acessibilidade (GitHub) | https://primer.style/accessibility/ | B | não declarada | 2026-10-10 |
| V-35 | Inclusive Components (Heydon Pickering, artigos de 2017 a 2018) | https://inclusive-components.design/ | B | não declarada | 2026-10-10 |
| V-37 | Storybook: testes de acessibilidade | https://storybook.js.org/docs/writing-tests/accessibility-testing | B | documentação oficial; licença não verificada | 2026-10-10 |
| B-01 | Apple HIG (raiz), Designing for macOS, Materials | https://developer.apple.com/design/human-interface-guidelines/ (e `/designing-for-macos/`, `/materials`) | B | © Apple: só destilar | citada pelo brain-of-agent em 2026-10-09; não reaberta neste plugin |
| B-02 | W3C APG: padrões | https://www.w3.org/WAI/ARIA/apg/patterns/ | A | W3C: destilar | citada pelo brain-of-agent; não reaberta |
| B-03 | U.S. Access Board: Revised 508 Standards | https://www.access-board.gov/ict/ | A | domínio público federal dos EUA (Inferido) | citada pelo brain-of-agent; não reaberta |

## Pesquisa, heurísticas e escrita

| V | Título | URL | Classe | Licença | Consulta |
| --- | --- | --- | --- | --- | --- |
| V-11 | NN/g: 10 Usability Heuristics (1994, revisado 2024-01-30) | https://www.nngroup.com/articles/ten-usability-heuristics/ | A | © NN/g: destilar | 2026-10-10 |
| V-11 | NN/g: How to Conduct a Heuristic Evaluation (Moran e Gordon, 2023-06-25) | https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/ | A | © NN/g | 2026-10-10 |
| V-11 | NN/g: How to Rate the Severity of Usability Problems (Nielsen, 1994-11-01) | https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/ | A | © NN/g | 2026-10-10 |
| V-12 | NN/g: Error Message Guidelines (2023-05-14) | https://www.nngroup.com/articles/error-message-guidelines/ | B | © NN/g | 2026-10-10 |
| V-14 | GOV.UK: understand content design | https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/understand-content-design | B | não verificada | 2026-10-10 |
| V-14 | Microsoft Writing Style Guide (só a página de entrada foi lida) | https://learn.microsoft.com/en-us/style-guide/welcome/ | B | não verificada | 2026-10-10 |
| V-16 | `ux-research` (rampstackco/claude-skills) | https://raw.githubusercontent.com/rampstackco/claude-skills/main/skills/ux-research/SKILL.md | B | MIT (API) | 2026-10-10 |
| V-17 | NN/g: Usability Testing 101 (2019-12-01, revisado 2026-07-15) | https://www.nngroup.com/articles/usability-testing-101/ | A | © NN/g | 2026-10-10 |
| V-18 | NN/g: Design Critiques (2016-10-23) | https://www.nngroup.com/articles/design-critiques/ | B | © NN/g | 2026-10-10 |
| V-19 | NN/g: Card Sorting vs Tree Testing (Tankala, 2024-02-23) | https://www.nngroup.com/articles/card-sorting-tree-testing-differences/ | B | © NN/g | 2026-10-10 |
| V-19 | Complementos vistos só em resultados de busca (não lidos na íntegra): `/articles/tree-testing/`, `/articles/card-sorting-terminology-matches/`, `/articles/ia-study-guide/` (mesmo domínio) | https://www.nngroup.com/articles/tree-testing/ | B | © NN/g | não lidos |

## Design systems e tokens

| V | Título | URL | Classe | Licença | Consulta |
| --- | --- | --- | --- | --- | --- |
| V-20 | W3C DTCG: Design Tokens Format Module 2025.10 (relatório final de comunidade, 2025-10-28, não é padrão W3C) | https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/ | A | W3C Community Final Specification Agreement | 2026-10-10 |
| V-20 | Reconferência do validador de qualidade: a spec 2025.10 não define `$schema` (só diz que o grupo explora um JSON Schema); `dimension` = `{ value, unit }` com `px` ou `rem` | https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/ | A | idem | 2026-10-10 (primeiros 100 mil caracteres) |
| V-20 | DTCG: rascunho (2026-09-08, "preview, não implemente") | https://www.designtokens.org/tr/drafts/format/ | A | idem | 2026-10-10 |
| V-21 | Figma Help: tokens, variáveis e estilos | https://help.figma.com/hc/en-us/articles/18490793776023-Update-1-Tokens-variables-and-styles | B | documentação da ferramenta: destilar | 2026-10-10 |
| V-21 | Blog claudecode-lab sobre design system (autor não identificado; só como exemplo de arquitetura, com defeitos listados em `design-tokens.md`) | https://claudecode-lab.com/en/blog/claude-code-design-system | C | sem licença | 2026-10-10 |
| V-22 | Style Dictionary | https://styledictionary.com/ | B | não declarada na página; só referência | 2026-10-10 |
| V-23 | design.md (google-labs-code), formato alpha | https://github.com/google-labs-code/design.md | A | Apache-2.0 (API) | 2026-10-10 |
| V-32 | design-system-ops | https://github.com/murphytrueman/design-system-ops | B | MIT | 2026-10-10 |
| V-40 | cult-ui (Nolly Studio): registro shadcn, 134 páginas MDX, `check-registry.mts`, 141 componentes; base do contrato de componente e de doc | https://github.com/nolly-studio/cult-ui · https://www.cult-ui.com | B | MIT (© Jordan Gilliam) | 2026-10-11 (branch `main`, push de 2026-10-01) |
| V-41 | Skiper UI (Gurvinder Singh): 107 componentes, registro `https://skiper-ui.com/r/{name}.json`, CSS compilado do site; estéticas D4 a D6 e D10 e presets de movimento | https://skiper-ui.com | B | free com atribuição obrigatória; Pro pago; sem repositório público: só valores e ideias, sem código copiado | 2026-10-11 |
| V-42 | OriginKit (Lander Studio): 593 componentes, 58 seções, `tweakSchema`, presets, CLI e MCP; estética D7 e D8 e filtros de direção | https://www.originkit.dev · https://www.originkit.dev/docs/licensing | B | proprietária (só a CLI `originkit` no npm é MIT); proíbe uso em design system ou UI kit: só taxonomia e processo, sem código | 2026-10-11 |

## Repositórios e práticas B

| V | Título | URL | Classe | Licença | Observação |
| --- | --- | --- | --- | --- | --- |
| V-24 | Impeccable (pbakaus): só o padrão "detector determinístico + julgamento" | https://github.com/pbakaus/impeccable | B | Apache-2.0 (API) | instalador e hook não entram |
| V-25 | ux-ui-agent-skills (plugin87), gates e crítico adversarial | https://github.com/plugin87/ux-ui-agent-skills | B | MIT | evidência autorrelatada |
| V-26 | gstack (garrytan): `design-review`, `plan-design-review`, `design-consultation` | https://github.com/garrytan/gstack | B | MIT (copyright de Garry Tan, 2026; licença no snapshot do brain-of-agent) | só categorias e princípios, com atribuição |
| V-27 | web-interface-guidelines (vercel-labs) | https://github.com/vercel-labs/web-interface-guidelines | B | MIT | estrelas e último commit não verificados |
| V-28 | `critique-visual-hierarchy` (Owl-Listener/designer-skills) | https://raw.githubusercontent.com/Owl-Listener/designer-skills/main/visual-critique/skills/critique-visual-hierarchy/SKILL.md | B | MIT | |
| V-29 | `ui-designer` (VoltAgent/awesome-claude-code-subagents) | https://raw.githubusercontent.com/VoltAgent/awesome-claude-code-subagents/main/categories/01-core-development/ui-designer.md | B | MIT | original depende de agente inexistente |
| V-30 | ui-ux-pro-max-skill (nextlevelbuilder) | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | B | MIT | só o formato de brief; scripts não entram |
| V-31 | accessibility-agents (Community-Access) e accessibility-scanner (github) | https://github.com/Community-Access/accessibility-agents · https://github.com/github/accessibility-scanner | B | MIT | só o padrão de roteador e a política de triagem |
| V-33 | qiaomu-design (joeseesun) | https://github.com/joeseesun/qiaomu-design | B | MIT | só o fluxo diagnosticar, propor, implementar |

## Base própria e inspiração com atribuição

- **brain-of-agent** (Francisco Edson, MIT, snapshot de 2026-10-09 no repositório de fábrica): `brains/fullstack/references/apple-design.md` e `brains/qa/references/acessibilidade.md` foram adaptados em `apple-e-plataformas.md`, `wcag-aa.md` e `checklist-completo.md`. O estilo da casa (rótulos epistêmicos, proporcionalidade, keyword de modo completo, handoff) vem do mesmo repositório.
- **gstack** (Garry Tan, MIT): categorias de auditoria, teste de tronco, classificador de superfície, princípios de revisão de plano e a calibração "os três looks" inspiraram `ui-audit`, `padroes-e-antipadroes.md` e a skill `design-brief`, em redação própria. Aviso de licença de terceiros: "Copyright (c) 2026 Garry Tan, MIT License". Nenhum bloco foi copiado; instaladores, telemetria, commits automáticos e binários do gstack não foram adotados.
- **Apache-2.0** (anthropics/skills, anthropics/knowledge-work-plugins, google-labs-code/design.md, pbakaus/impeccable): usados como fonte de ideias e processo; o texto do plugin é redação própria.

## Não usar como regra

| Item | Motivo |
| --- | --- |
| Material Design 3 (`m3.material.io`) | Páginas só renderizam com JavaScript; a regra de 48 dp só apareceu em trechos de busca. Lacuna declarada (rótulo: Não verificável). |
| Laws of UX | Sem autoria nem licença na página; "7±2" é debatido. Só como lista de perguntas de revisão (C). |
| hig-doctor, refactoring-ui-skill, oh-my-design, c2d2c | Congelado ou sem licença, `npx -y` sem versão, conteúdo de terceiros sem direito, write-back automático. |
| Superdesign, MindStudio, Composio, QASkills | Conteúdo promocional; contagens de instalação conflitantes. As ideias úteis já estão em fonte A (V-04). |
| Reddit, X, YouTube | Sem leitura direta nesta rodada (lacuna). |
| Texto literal da HIG e do livro Refactoring UI | Direitos de terceiros. |

## Datas, versões e onde reconferir

| Item | Valor na consulta (2026-10-10) | Onde reconferir |
| --- | --- | --- |
| WCAG 2.2 | Recommendation de 2024-12-12; 86 critérios (78 do 2.1, mais 9 novos, menos 4.1.1) | https://www.w3.org/TR/WCAG22/ |
| WCAG 3 | Rascunho, não é norma (informado pelo brain-of-agent; Não verificado nesta rodada) | página de status do W3C WAI, a localizar na data do uso |
| DTCG | 2025.10, relatório de comunidade; rascunho de 2026-09 | links da seção de tokens |
| design.md | alpha | README do repositório |
| Claude Code | CLI local da fábrica: 2.1.128; `claude plugin eval` exige 2.1.269 ou superior; `/output-style` e estilo Concise exigem versões recentes (V-07) | `claude --version` e https://code.claude.com/docs |
| Modelo-alvo | guias medidos em modelos Claude 4.x e 5.x | docs de prompting da Anthropic |
| cult-ui, Skiper UI, OriginKit | consulta de 2026-10-11; catálogos, preços e licenças mudam | V-40 a V-42; `direcoes-de-estilo.md` seção 8 |
| axe-core | `web-frontend` registra 4.14.0; o brain cita 4.10.2 em script de QA | `npm ls axe-core` no projeto ou a página do pacote, na data do uso |
