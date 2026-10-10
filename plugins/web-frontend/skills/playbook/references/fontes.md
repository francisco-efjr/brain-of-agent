# Fontes do plugin web-frontend

Bibliografia validada. Classe A = oficial (Anthropic, mantenedor da tecnologia, norma); B = prática reconhecida (empresa, autor conhecido, repositório mantido); C = comunidade, só como ideia. Todas consultadas em 2026-10-10 (pesquisa e validação do plugin; mesma família de modelo, independência parcial). "Sem licença de reuso verificada" significa: o conteúdo deste plugin é destilação com redação própria, sem texto copiado. IDs `V-nn` referem-se à validação que sustenta cada item.

## Sumário

- [Claude Code e Anthropic](#claude-code-e-anthropic)
- [Normas e plataforma web](#normas-e-plataforma-web)
- [Frameworks e bibliotecas](#frameworks-e-bibliotecas)
- [Testes, medição e ferramentas](#testes-medição-e-ferramentas)
- [Repositórios e práticas B](#repositórios-e-práticas-b)
- [Comunidade classe C](#comunidade-classe-c)
- [Base própria e terceiros incorporados](#base-própria-e-terceiros-incorporados)
- [Dados de repositório](#dados-de-repositório)
- [Fontes rejeitadas ou sem aproveitamento](#fontes-rejeitadas-ou-sem-aproveitamento)

## Claude Code e Anthropic

| V | Título | URL | Classe | Licença | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-04 | Claude Code: boas práticas | https://code.claude.com/docs/en/best-practices | A | documentação, sem licença de reuso verificada | verificação executável, plano opcional, revisor em contexto limpo |
| V-01 | Skill `frontend-design` (anthropics/skills; cópia idêntica em anthropics/claude-code/plugins) | https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md | A | Apache-2.0 (`LICENSE.txt` da skill, lido); repositório sem LICENSE raiz | brief, plano com tokens, anti-genérico, piso de qualidade |
| V-02 | Blog: Improving frontend design through skills (12 nov 2025) | https://claude.com/blog/improving-frontend-design-through-skills | B | artigo, sem licença de reuso verificada | altitude do prompt, convergência para o genérico |
| V-03 | Prompting best practices (seção de frontend) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | A | idem | bloco de direção estética, anti-overengineering (cita Opus 4.5 e 4.6) |
| V-05 | Documentação de Skills | https://code.claude.com/docs/en/skills | A | idem | frontmatter, `allowed-tools` pré-aprova |
| V-06 | Documentação de Subagentes | https://code.claude.com/docs/en/sub-agents | A | idem | campos, plugin ignora hooks/mcpServers/permissionMode |
| V-07 | Claude Code com Chrome | https://code.claude.com/docs/en/chrome | A | idem | verificar UI com navegador, requisitos e riscos |
| V-09 | Anthropic Engineering: harness para apps longos (24 mar 2026) | https://www.anthropic.com/engineering/harness-design-long-running-apps | A | idem | avaliador cético, 4 critérios, custo |
| V-29 | Repositório de plugins oficiais | https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/README.md | A | idem | aviso "leia antes de instalar" |
| V-30 | Memória: CLAUDE.md, `.claude/rules`, AGENTS.md | https://code.claude.com/docs/en/memory | A | idem | meta abaixo de 200 linhas, `paths` |
| V-31 | Guia de hooks | https://code.claude.com/docs/en/hooks-guide | A | idem | hook PostToolUse de formatação (desativado) |
| V-08 | Skill `webapp-testing` (anthropics/skills) | https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md | B (rebaixada de A) | Apache-2.0 (`LICENSE.txt` da pasta) | só o procedimento `browser-recon`; `networkidle` não adotado |

## Normas e plataforma web

| V | Título | URL | Classe | Licença | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-16 | WCAG 2.2 e "novidades da 2.2" (W3C) | https://www.w3.org/TR/WCAG22/ · https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ | A | licença de documento W3C: Não verificado | alvo normativo, 9 critérios novos, 2.5.8 |
| V-45 | WCAG Understanding: 3.3.1, 3.3.2, 3.3.3, 3.3.4 | https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html · .../labels-or-instructions.html · .../error-suggestion.html · .../error-prevention-legal-financial-data.html | A | idem | erros de formulário |
| V-45 | web.dev Learn Forms: validação e acessibilidade (2021) | https://web.dev/learn/forms/validation · https://web.dev/learn/forms/accessibility | A (rebaixada pela data) | Não verificado | validação nativa, `aria-describedby` |
| V-58 | ARIA in HTML (Recomendação W3C, 11 ago 2026) | https://www.w3.org/TR/html-aria/ | A | idem | HTML nativo antes de ARIA |
| V-58 | Using ARIA (Discontinued Draft, 24 fev 2026) | https://www.w3.org/TR/using-aria/ | A (descontinuado) | idem | leitura das quatro regras |
| V-24 | WAI-ARIA APG: padrões | https://www.w3.org/WAI/ARIA/apg/patterns/ | A | idem | teclado e foco por widget |
| V-15 | web.dev: limiares de CWV, optimize LCP, INP | https://web.dev/articles/defining-core-web-vitals-thresholds · https://web.dev/articles/optimize-lcp · https://web.dev/articles/inp | A | Não verificado | orçamentos e subpartes do LCP |
| V-59 | MDN: CSP e Trusted Types | https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP · https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API | A | Não verificado | CSP estrita, Report-Only, Trusted Types |
| V-59 | web.dev: strict CSP (2024-09-13) | https://web.dev/articles/strict-csp | B | Não verificado | nonce com `strict-dynamic` |
| V-59 | web.dev: CSP (2012-06-15) | https://web.dev/articles/csp | B (obsoleto em parte) | Não verificado | não vira regra |
| V-23 | MDN: `prefers-reduced-motion` | https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion | A | Não verificado | contrapartida de movimento |
| V-53 | MDN: container queries | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries | A | Não verificado | `container-type`, unidades `cq*` |
| V-22 | OWASP: DOM-based XSS Prevention | https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html | A | Não verificado | lista de sinks |
| V-54 | DTCG: formato de design tokens (rascunho de 08 set 2026) | https://www.designtokens.org/tr/drafts/format/ | B (rascunho) | Não verificado | só vocabulário |

## Frameworks e bibliotecas

| V | Título | URL | Classe | Licença | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-13 | React: You Might Not Need an Effect | https://react.dev/learn/you-might-not-need-an-effect | A | Não verificado | checklist "Preciso de Effect?" |
| V-44 | React: TypeScript (v19.3) · TypeScript Handbook: JSX | https://react.dev/learn/typescript · https://www.typescriptlang.org/docs/handbook/jsx.html | A | Não verificado | 8 regras de tipos em TSX |
| V-46 | React: useActionState · Next.js: Forms | https://react.dev/reference/react/useActionState · https://nextjs.org/docs/app/guides/forms | A | Não verificado | form com estado de erro |
| V-14 | Next.js: Server e Client Components (16.4.0) | https://nextjs.org/docs/app/getting-started/server-and-client-components | A | Não verificado | fronteira client/server |
| V-51 | Next.js: Caching, ISR, ISR com Cache Components | https://nextjs.org/docs/app/getting-started/caching · https://nextjs.org/docs/app/guides/incremental-static-regeneration · https://nextjs.org/docs/app/guides/incremental-static-regeneration-cache-components | A | Não verificado | dois modelos de cache |
| V-59 | Next.js: Content Security Policy (2026-03-20) | https://nextjs.org/docs/app/guides/content-security-policy | A | Não verificado | nonce exige renderização dinâmica |
| V-48 | TanStack Query: important defaults | https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults | A | Não verificado | `staleTime`, `gcTime`, retries |
| V-25 | Vue: production deployment | https://vuejs.org/guide/best-practices/production-deployment.html | A | Não verificado | build de produção |
| V-52 | Vue: SSR · Nuxt 4: rendering | https://vuejs.org/guide/scaling-up/ssr.html · https://nuxt.com/docs/4.x/guide/concepts/rendering | A | Não verificado | poluição entre requisições, `routeRules` |
| V-49 | Nuxt 4: data fetching (v4.6.0) | https://nuxt.com/docs/4.x/getting-started/data-fetching | A | Não verificado | `useFetch`, `useAsyncData`, chave |
| V-27 | Svelte 5: best practices | https://svelte.dev/docs/svelte/best-practices | A | Não verificado | runes |
| V-50 | SvelteKit: load | https://svelte.dev/docs/kit/load | A | Não verificado | `load`, `invalidate`, `redirect` |
| V-26 | Angular: signals | https://angular.dev/guide/signals | A | Não verificado | `computed`, `effect` |
| V-47 | Angular: forms e reactive forms | https://angular.dev/guide/forms · https://angular.dev/guide/forms/reactive-forms | A | Não verificado | escolha de formulário |
| V-53 | Tailwind CSS v4: theme e responsive design | https://tailwindcss.com/docs/theme · https://tailwindcss.com/docs/responsive-design | A | Não verificado | `@theme`, breakpoints, `@container` |

## Testes, medição e ferramentas

| V | Título | URL | Classe | Licença | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-20 | Playwright: best practices · page.goto | https://playwright.dev/docs/best-practices · https://playwright.dev/docs/api/class-page#page-goto | A | Não verificado | locators, web-first, `networkidle` desaconselhado |
| V-56 | Playwright: accessibility testing e snapshots · axe API | https://playwright.dev/docs/accessibility-testing · https://playwright.dev/docs/test-snapshots · https://raw.githubusercontent.com/dequelabs/axe-core/develop/doc/API.md | A | Não verificado (axe-core: MPL-2.0) | axe por rota, baseline visual |
| V-21 | Testing Library: queries | https://testing-library.com/docs/queries/about/ | A | Não verificado | prioridade de queries |
| V-55 | Storybook: writing tests · Vitest Browser Mode | https://storybook.js.org/docs/writing-tests · https://vitest.dev/guide/browser/ | A | Não verificado | teste de componente |
| V-57 | Lighthouse (overview) · Lighthouse CI getting started | https://developer.chrome.com/docs/lighthouse/overview · https://raw.githubusercontent.com/GoogleChrome/lighthouse-ci/main/docs/getting-started.md | A | Lighthouse CI: Apache-2.0 | medição e orçamentos |
| V-60 | Figma MCP: guia, ferramentas, instalação remota | https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server · https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/ | A | Não verificado | design-to-code em leitura |
| V-28 | axe-core (Deque) | https://github.com/dequelabs/axe-core | B | MPL-2.0 (usar o pacote, não copiar) | automação de a11y |
| V-32 | AGENTS.md (formato aberto) | https://agents.md/ | B | Não verificado | importar com `@AGENTS.md` |

## Repositórios e práticas B

| V | Título | URL | Classe | Licença | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-10, V-11 | vercel-labs/agent-skills (`react-best-practices`, `composition-patterns`) | https://github.com/vercel-labs/agent-skills | B | MIT declarado, não confirmado (sem LICENSE raiz) | ordem de revisão React, API de componentes (destilado) |
| V-12 | vercel-labs/web-interface-guidelines | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | B | MIT, "Copyright (c) 2025 Vercel Labs" (LICENSE lido) | diretrizes de interface destiladas; o padrão de buscar a URL em runtime foi rejeitado |
| V-17, V-18, V-19, V-61 | github/awesome-copilot: instruções e agentes de a11y, performance, segurança | https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/a11y.instructions.md | B | MIT, "Copyright GitHub, Inc." (LICENSE raiz lido) | severidade e detecção; base dos agentes (reescritos) |
| V-35 | pbakaus/impeccable | https://github.com/pbakaus/impeccable | B | Apache-2.0 (LICENSE lido) | taxonomia de modos e lista de anti-padrões (destilada); `npx impeccable install` não adotado |
| V-34 | amplifying.ai: What Claude Code actually chooses (fev 2026) | https://amplifying.ai/research/claude-code-picks | B | não verificada | motivação de declarar a stack (modelos antigos) |
| V-33 | HumanLayer: Writing a good Claude.md (25 nov 2025) | https://www.humanlayer.dev/blog/writing-a-good-claude-md | B | artigo | estrutura what/why/how |
| V-36 | lackeyjb/playwright-skill | https://raw.githubusercontent.com/lackeyjb/playwright-skill/main/skills/playwright-skill/SKILL.md | B | MIT (página do repositório) | só o procedimento; ferramentas amplas não adotadas |
| V-37 | Simon Willison: Agentic Engineering Patterns, teste manual agentic | https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/ | B | artigo | nota de verificação com comando e saída |
| V-38 | Cursor: project rules | https://cursor.com/docs/context/rules | B | documentação | regra nasce de erro repetido (o escopo no Claude Code é `paths`, não `globs`) |
| V-62 | HN 45642911 (Show HN playwright-skill) e HN 47499672 (ProofShot) | https://news.ycombinator.com/item?id=45642911 · https://news.ycombinator.com/item?id=47499672 | B | posts | riscos de navegador; agente coleta evidência, humano decide estética |

## Comunidade classe C

Usadas só como ideias, sempre com apoio em fonte A.

| V | Título | URL | Licença | Ideia aproveitada |
| --- | --- | --- | --- | --- |
| V-39 | Rulestack: teste de estrutura para CLAUDE.md | https://dev.to/rulestack/we-cut-claudemd-to-33kb-eighteen-days-later-it-was-45kb-again-what-a-size-cap-missed-and-a-3ha8 | não verificada | checklist de CI do CLAUDE.md |
| V-40 | yureki_lab: migração Cypress para Playwright com arquivo de regras | https://dev.to/yureki_lab/how-i-migrated-90-cypress-tests-to-playwright-with-claude-code-in-4-days-1im6 | não verificada | `regras-migracao-testes.md` |
| V-41 | buildthisnow: regressão visual com Playwright (27 jul 2026) | https://www.buildthisnow.com/blog/guide/development/claude-code-visual-regression-tests | não verificada | configuração determinística, regra de baseline |
| V-42 | claudecode-lab: prompt de revisão de acessibilidade | https://claudecode-lab.com/en/blog/claude-code-accessibility/ | não verificada | prompt com escopo (reescrito) |
| V-43 | claudecode-lab: shadcn/ui com agente | https://claudecode-lab.com/en/blog/claude-code-shadcn-ui/ | não verificada | propriedade de primitivos, drift |
| V-63 | Simon Willison: Kākāpō Party | https://simonwillison.net/2026/Sep/26/kakapo-party/ | artigo | receita de gravação de interação |
| V-64 | dev.to: skill `/wizard` | https://dev.to/_vjk/i-made-claude-code-think-before-it-codes-heres-the-prompt-bf | sem licença declarada | revisão adversarial do próprio diff |

## Base própria e terceiros incorporados

| Origem | Licença | Uso |
| --- | --- | --- |
| Repositório do usuário `francisco-efjr/brain-of-agent` (snapshot de 2026-10-09): `brains/fullstack/references/frontend-e-estado.md`, `apple-design.md`, `protocolo-completo.md`, templates `adr`, `handoff-checkpoint`, `plano-incremento`; `brains/qa/references/acessibilidade.md`, `automacao-web.md`, template `registro-evidencias-qa` | MIT (conteúdo próprio do autor) | incorporado e adaptado a este plugin; versões de Playwright 1.63, Cypress 16, Selenium 4.50 e WebdriverIO 9 do brain são Não verificadas por este plugin; números normativos e de WebAIM Million do brain ficaram Inferidos |
| gstack `design-html` (Garry Tan e contribuidores; licença MIT em `vendor/gstack/LICENSE` do brain; material derivado Apache-2.0 de impeccable e DESIGN.md) | MIT / Apache-2.0 | inspiração de processo (detectar contexto, spec, verificação em 3 viewports, lista anti-slop, edições cirúrgicas), com redação própria e sem cópia; nada do preâmbulo, telemetria ou dependências por CDN |
| Apple Human Interface Guidelines (citadas no brain, páginas não relidas por este plugin): https://developer.apple.com/design/human-interface-guidelines/ | conteúdo da Apple, sem reuso | apenas como preferência de acabamento, sem métricas copiadas |

## Dados de repositório

Lidos em 2026-10-10 pela página HTML do repositório e pelo feed de commits (a API REST estava indisponível); podem mudar.

| Repositório | Estrelas | Último commit na branch principal | Licença verificada |
| --- | --- | --- | --- |
| anthropics/skills | 180.198 | 2026-10-09 18:45Z | sem LICENSE na raiz; `skills/frontend-design/LICENSE.txt` Apache-2.0 |
| vercel-labs/agent-skills | 32.136 | 2026-08-28 13:36Z | sem LICENSE na raiz; MIT só declarado |
| github/awesome-copilot | 39.873 | 2026-10-09 05:48Z | LICENSE raiz MIT |
| pbakaus/impeccable | 79.069 | 2026-10-09 04:19Z | LICENSE raiz Apache-2.0 |
| lackeyjb/playwright-skill | 3.181 | 2026-08-14 13:51Z | MIT |
| AmElmo/proofshot | 866 | 2026-04-14 04:20Z | MIT (instalação não adotada) |

Estrelas não provam qualidade; servem só como sinal de adoção.

## Fontes rejeitadas ou sem aproveitamento

awesome-cursorrules (qualidade desigual); frontend-visualqa (envia capturas a serviço de terceiro); interface-design (Dammyjay93); iannuttall/claude-agents (sem licença); abhishekray07/claude-md-templates (sem licença); lista Claude-Code-Frontend-Design-Toolkit (sem código próprio); thread HN do setup do criador do Claude Code (conteúdo do tweet não lido); `gem-browser-tester` (sem porquê, acoplado a orquestrador). Reddit (403), X e YouTube não foram lidos: o sinal de comunidade deste plugin é fraco e declarado assim.
