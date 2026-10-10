# web-frontend — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. "Dest." = destilar. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| anthropics/skills `frontend-design` (AO-28, EC-03) | https://github.com/anthropics/skills | A | Definir produto e público antes do visual, plano de tokens, lista de anti-padrões genéricos, reduced motion e foco visível, revisar screenshots. Conferir LICENSE da skill antes de literal (Apache-2.0 segundo o pesquisador, parcialmente Inferido). |
| Improving frontend design through skills (AO-31) | https://claude.com/blog/improving-frontend-design-through-skills | A | Blog oficial sobre a skill de frontend; não relido pelo validador. |
| vercel-labs/agent-skills (EC-07) | https://github.com/vercel-labs/agent-skills | A- | 70 regras em 8 categorias ordenadas por impacto (waterfalls e bundle críticos); um arquivo por regra com motivo, exemplo ruim e bom. Licença da API null e SKILL.md diz MIT: formato sim, texto literal só após confirmar LICENSE. |
| a11y.instructions.md, WCAG 2.2 AA (CT-19) | https://github.com/github/awesome-copilot | B | Molde severidade + detecção + referência + correção; "Placeholder is a hint, not a label"; testar a 320px. MIT. |
| performance-optimization.instructions.md (CT-19) | https://github.com/github/awesome-copilot | B | LCP/INP/CLS, bundle, imagens. Só frontend; acrescentar comandos de verificação (Lighthouse). |
| playwright-typescript e qa-engineering (CT-17) | https://github.com/github/awesome-copilot/tree/main/instructions | B | Seletores role → label → test-id → text; asserções web-first; sem `sleep`. Não reabertos pelo validador. |
| playwright-e2e-testing .mdc (CT-13) | https://github.com/PatrickJS/awesome-cursorrules | B | `page.route`, auto-wait, 3 a 5 testes por arquivo. CC0. |
| security-and-owasp.instructions.md (CT-16) | https://github.com/github/awesome-copilot | B | "Frontend guards are UX only. ALWAYS verify on server."; httpOnly cookies. MIT. |
| Amplifying, "What Claude Code actually chooses" (CP-24) | https://amplifying.ai/research/claude-code-picks | B | Declarar stack, hospedagem e bibliotecas antes de gerar; modelo tende a soluções próprias. |
| Boris Cherny setup (CP-01) | https://news.ycombinator.com/item?id=46470017 | A | Formatação por hook PostToolUse; verificação (screenshot/teste) antes de automatizar. |
| Simon Willison, agentic patterns (CP-11) | https://simonwillison.net/guides/agentic-engineering-patterns/ | B | Testes manuais agentic (browser automation, screenshots) e depois teste permanente. |
| Harness para apps longos (AO-20) | https://www.anthropic.com/engineering/harness-design-long-running-apps | A | Avaliador separado e cético para apps; autoelogio de agentes. |
| awesome-cursorrules por stack (CT-06) | https://github.com/PatrickJS/awesome-cursorrules | B | Catálogo CC0 com qualidade desigual; nextjs15-react19 está truncado (calibração negativa). |
| `.cursor/rules` (CT-05) | https://cursor.com/docs/context/rules | A | Triagem ao portar regras `.mdc` para `.claude/rules` com `paths:`. |
| Prompting best practices, frontend (AO-01) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | A | Doc cita aplicação a front-end; ler a seção do modelo-alvo. |

## 2. Repositórios e arquivos a abrir
- `vercel-labs/agent-skills`: pastas de regras, `SKILL.md` e `LICENSE`.
- `anthropics/skills/frontend-design` (SKILL.md + LICENSE.txt).
- `github/awesome-copilot` `instructions/`: `a11y`, `performance-optimization`, `playwright-typescript`, `code-review-generic`.
- `PatrickJS/awesome-cursorrules` `rules/`: `readme-best-practices…`, `playwright-e2e-testing…`.
- `wshobson/agents` (plugins frontend, nome citado; conteúdo não lido); `garrytan/gstack` design (BR-23).
- Docs oficiais de React, Next.js, Vue, Svelte, WCAG e web.dev não estão no atlas global: lente authoritative do segmento.

## 3. Materiais oficiais Anthropic pertinentes
AO-28 (frontend-design, webapp-testing: reconhecimento → ação com Playwright), AO-31 (frontend skill), AO-20, AO-01, AO-24 (security-review aplica a web), AO-06 (verificação por screenshot).

## 4. Padrões da comunidade
- Verificar visualmente: screenshot e teste e2e, não só typecheck (CP-01, CP-11, AO-28).
- Hook de formatação em vez de prosa (CP-01).
- Arquivo por regra com motivo, ruim e bom (EC-07).
- Reduzir slop genérico com lista de anti-padrões e tokens antes de codar (AO-28, BR-23).
- Declarar bibliotecas aceitas para evitar reinvenção (CP-24).

## 5. O que o brain-of-agent já oferece
- `brains/fullstack/references/frontend-e-estado.md`, `apple-design.md` (preferência de acabamento, não imposição), `brains/qa/references/acessibilidade.md`, `automacao-web.md`, `vendor/gstack/design-html/SKILL.md`.
- BR-10: `auditoria_axe.py` (depende de axe-core no browser; chamar por caminho explícito).
- BR-14: OWASP Top 10:2025 verificado; WebAIM Million 2026 não rechecado.
- BR-23: notas 0 a 10 por dimensão com "o que seria um 10", lista anti-slop. BR-18: tiers de QA, "value card" com "Não coberto".
- BR-03: modo `FRONTEND-COMPLETO`.

## 6. Lacunas e cuidados
- Nenhuma fonte do atlas cobre Vue, Svelte, Angular ou estado/data fetching em profundidade; só vercel-labs (React/Next) e a11y/perf genéricas.
- Nenhum item nomeia axe ou Lighthouse como comando: o plugin deve acrescentar.
- Estrelas de vercel-labs (32.134) e licença conflitante: não copiar literal sem LICENSE.
- Benchmarks de Vercel sobre AGENTS.md são do fornecedor (CT-02).
