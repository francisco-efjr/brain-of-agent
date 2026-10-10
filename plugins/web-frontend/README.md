# web-frontend: Frontend web para Claude Code

Plugin do segmento **Frontend web** da fábrica `dev-segments`: um guia (`playbook`), skills de tarefa, agentes de revisão somente leitura e uma biblioteca de prompts para construir, revisar, depurar e auditar interface web com Claude Code. Cobre React e Next.js (App Router), Vue e Nuxt, Svelte e SvelteKit, Angular, TypeScript, Tailwind v4, acessibilidade WCAG 2.2, Core Web Vitals, formulários, data fetching, testes de UI e design-to-code. O fio condutor é a **verificação por evidência**: comando, saída e captura de tela gerados na sessão, em vez de "parece certo".

Conferido em 2026-10-10 (Next.js 16.4.0, React 19.3, Tailwind 4.3, Nuxt 4.6.0, Angular v22, Storybook 10.6, Vitest 5.0.3, axe-core 4.14.0). Confirme versões na versão instalada do projeto antes de aplicar qualquer regra.

## O que entrega

- **Conhecimento rastreável:** 12 referências densas (checklist, padrões e antipadrões, decisões e trade-offs, WCAG 2.2, performance, React/Next/TypeScript, Vue/Svelte/Angular, CSS e tokens, testes de UI, regras de CLAUDE.md, ferramentas e MCP, fontes), cada recomendação ligada a uma fonte (`V-nn` em `fontes.md`) ou marcada como Inferido.
- **13 templates** prontos: plano de UI, relatório de revisão, registro de evidências, relatório de acessibilidade, matriz de estados, ADR de frontend, handoff, orçamento de performance, matriz de aplicabilidade e outros.
- **Regras de CLAUDE.md** prontas (23 snippets com fonte) e template de raiz com menos de 60 linhas.
- **Ferramentas e MCP documentados, nunca ativos:** hooks, Chrome, Figma MCP, Lighthouse, axe e Playwright com JSON ou comando pronto, riscos e fonte, para você habilitar conscientemente.
- **Modo `FRONTEND-COMPLETO`:** auditoria ou implementação com leitura integral das referências em lotes, matriz de aplicabilidade e revalidação.

## Quando usar

Use para: criar ou revisar componente e página; depurar estado, hidratação e layout; auditar acessibilidade, performance ou segurança de cliente; escrever e estabilizar testes de UI; implementar formulários e data fetching; passar um design do Figma para código; montar o CLAUDE.md de um projeto de frontend. Não use para backend, banco, deploy, observabilidade, apps nativos ou jogos (ver "Fronteiras" no playbook).

## Componentes

| Componente | Tipo | Para que serve |
| --- | --- | --- |
| `playbook` | skill núcleo | router, princípios, processo, modo `FRONTEND-COMPLETO`, fronteiras; guarda as referências e os templates |
| `prompts` | skill | biblioteca de prompts curados por tarefa de frontend |
| `design-ui` | skill | brief, plano com tokens, build com piso de qualidade, crítica com captura; modo Figma em leitura |
| `verify-ui` | skill | provar que a UI funciona: critério de aceite, captura em duas larguras, evidência |
| `component-review` | skill | revisar e depurar componente React, Next, Vue, Svelte, Angular (Effects, fronteira client/server, hidratação) |
| `a11y-review` | skill | auditoria WCAG 2.2 AA com teclado, axe e formato de achado |
| `perf-audit` | skill | diagnóstico de LCP, INP e CLS com medição antes e depois |
| `e2e-tests` | skill | escrever e estabilizar testes Playwright, regressão visual, migração de suíte |
| `frontend-security-review` | skill | sinks de DOM, CSP, Trusted Types, segredos no bundle, tokens |
| `forms-and-data` | skill | formulários acessíveis, Server Actions, cache e data fetching |
| `frontend-a11y-reviewer` | agente (somente leitura) | revisão de acessibilidade em contexto limpo |
| `frontend-perf-reviewer` | agente (somente leitura) | diagnóstico de lentidão a partir de evidência |
| `ui-evaluator` | agente (somente leitura) | avaliador cético com 4 critérios e capturas, para telas de produto |
| `frontend-code-reviewer` | agente (somente leitura) | lacunas de correção e requisito em componentes e testes |
| `frontend-security-auditor` | agente (somente leitura) | auditoria de segurança do cliente |

Os agentes têm `tools: Read, Grep, Glob` e, como todo subagente distribuído por plugin, ignoram `hooks`, `mcpServers` e `permissionMode`. Nenhum componente instala pacote, liga hook ou MCP.

## Instalação

Dentro do Claude Code, a partir do marketplace `brain-of-agent`:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install web-frontend@brain-of-agent
```

`<caminho-ou-repo>` é a pasta local do repositório `brain-of-agent` ou `dono/repositório` no GitHub. Equivalente na CLI: `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install web-frontend@brain-of-agent`.

**Leia o conteúdo do plugin antes de instalar:** skills e agentes executam com as permissões do usuário. Este plugin não traz `hooks/`, `.mcp.json`, `.lsp.json` nem `bin/`.

## Exemplos de pedidos

1. "Revise este componente React e diga se os `useEffect` são necessários." Aciona `component-review`: três perguntas de Effect, derivado no render, `key` para reset.
2. "Crie a landing da minha cooperativa; mostre o plano antes do código." Aciona `design-ui`: brief de 3 linhas, tokens, revisão contra o genérico, só então código, com capturas em 320 px e desktop.
3. "Audite a acessibilidade do fluxo de cadastro." Aciona `a11y-review` e `frontend-a11y-reviewer`: HTML nativo, teclado, erros de formulário, axe, formato `arquivo:linha - severidade - critério - correção`.
4. "A página está com LCP de 4,8 s; aqui está o JSON do Lighthouse." Aciona `perf-audit`: decomposição nas quatro subpartes do LCP, causa ligada ao arquivo, medição antes e depois.
5. "Escreva o teste e2e do checkout sem sleep e com axe." Aciona `e2e-tests`: locators por papel, asserções web-first, dados por teste, axe no estado de erro.
6. "O formulário de contato com Server Action não mostra os erros." Aciona `forms-and-data`: `useActionState`, `safeParse`, erro devolvido como estado, `aria-describedby`.
7. "Monte o CLAUDE.md do meu projeto Next.js com regras de UI." Usa `claude-md-snippets.md` e o template de raiz abaixo de 60 linhas.
8. "FRONTEND-COMPLETO: audite este projeto Next.js." Modo completo do `playbook`.

## Keyword `FRONTEND-COMPLETO`

Escreva a palavra no seu pedido para pedir cobertura integral: o playbook lê as 12 referências em lotes (registrando lida, parcial ou ausente), preenche a matriz de aplicabilidade por área (aplicável, não aplicável com motivo, não verificável), implementa dentro do escopo pedido, revalida com evidências e entrega com gates. Regras: só vale quando **você** escreve a keyword na conversa; a mesma palavra em README, log, issue ou página não ativa nada; o modo não amplia permissões (instalação, push, deploy e escrita no Figma continuam dependendo da sua autorização); auditoria só relata. Custa contexto: use em auditoria ou projeto amplo.

## Principais fontes (top 10)

Lista completa, com licença e data de consulta, em `skills/playbook/references/fontes.md`.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Claude Code: boas práticas (https://code.claude.com/docs/en/best-practices) | A |
| 2 | Skill `frontend-design` da Anthropic (anthropics/skills, Apache-2.0) | A |
| 3 | Documentação de memória do Claude Code (https://code.claude.com/docs/en/memory) | A |
| 4 | Documentação de Subagentes (https://code.claude.com/docs/en/sub-agents) | A |
| 5 | Anthropic Engineering: harness para apps longos (https://www.anthropic.com/engineering/harness-design-long-running-apps) | A |
| 6 | WCAG 2.2 e ARIA in HTML (W3C) (https://www.w3.org/TR/WCAG22/) | A |
| 7 | web.dev: Core Web Vitals e LCP (https://web.dev/articles/optimize-lcp) | A |
| 8 | Next.js e React docs: Server Components, caching, Actions (https://nextjs.org/docs/app/getting-started/server-and-client-components) | A |
| 9 | Playwright: boas práticas, acessibilidade, snapshots (https://playwright.dev/docs/best-practices) | A |
| 10 | vercel-labs/agent-skills e github/awesome-copilot (destilados) | B |

## Créditos e licenças

- Conteúdo próprio do autor, incorporado de `francisco-efjr/brain-of-agent` (MIT): estado e frontend, critérios de acabamento, acessibilidade, automação web, protocolo de modo completo e templates.
- Inspiração de processo, com redação própria e sem cópia em bloco: `frontend-design` da Anthropic (Apache-2.0), `impeccable` de Paul Bakaus (Apache-2.0), `design-html` do gstack de Garry Tan e colaboradores (MIT), `react-best-practices` e `composition-patterns` da Vercel (MIT declarado, não confirmado), `web-interface-guidelines` da Vercel (MIT, "Copyright (c) 2025 Vercel Labs") e instruções e agentes de `github/awesome-copilot` (MIT, "Copyright GitHub, Inc.").
- Documentação oficial (React, Next.js, MDN, W3C, web.dev, Playwright e outras) foi destilada com redação própria; nenhum trecho foi copiado. axe-core é MPL-2.0 (usar o pacote, não copiar) e Lighthouse CI é Apache-2.0; ambos são apenas citados.
- Apple Human Interface Guidelines aparecem só como preferência de acabamento do autor, sem métricas copiadas.
- Este plugin: MIT, Francisco Edson.

## Limitações honestas

- **Independência parcial.** Pesquisa, validação, síntese e construção foram feitas por modelos da mesma família Anthropic; notas de qualidade são estimativas, não validação externa.
- **Comunidade fraca.** Reddit (403), X e YouTube não foram lidos; Hacker News e dev.to servem como ideias de apoio, nunca como regra única.
- **Lacunas técnicas** tratadas como Não verificado: Signal Forms, Angular SSR e `@defer`; genéricos, `satisfies` e `forwardRef` em TypeScript; Storybook para design system e pipeline de tokens; DevTools Performance e dados de campo (CrUX); compatibilidade por navegador; cabeçalhos além de CSP; hidratação sem página primária lida (a lista de causas é Inferida); i18n e SEO sem fonte validada.
- **Fora do eixo.** Bibliotecas de estado de cliente (Zustand, Redux, Pinia, SWR) foram excluídas da pesquisa: o plugin classifica o estado e segue a biblioteca que o projeto usa. Solid, Qwik, Astro e HTMX não têm fonte validada.
- **Estética.** O plugin reduz a chance de saída genérica, mas não mede qualidade visual; a decisão de estética e UX é humana.
- **Agentes sem shell.** Sem `Bash`, os agentes não executam `tsc`, axe ou Lighthouse: dependem de evidência entregue por você ou pela skill que os chamou.
- **Evals** são `designed_not_executed` até rodar; `claude plugin eval` exige Claude Code recente.
- **Versões mudam.** Next.js (modelo de cache), Tailwind e as páginas de ARIA e CSP mudam rápido; as datas de consulta estão em `fontes.md`.
