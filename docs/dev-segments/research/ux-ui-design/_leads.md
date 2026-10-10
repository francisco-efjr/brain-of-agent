# ux-ui-design — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. Cobertura do atlas é fraca para UX de pesquisa e design visual. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| anthropics/skills `frontend-design` (AO-28, EC-03) | https://github.com/anthropics/skills | A | Definir produto e público antes do visual; plano de tokens antes de codar; lista de anti-padrões genéricos (anti AI-slop); reduced motion e foco visível; revisar screenshots. Conferir LICENSE da skill antes de literal. |
| Improving frontend design through skills (AO-31) | https://claude.com/blog/improving-frontend-design-through-skills | A | Blog oficial; não relido pelo validador. |
| Blog "lessons from building Claude Code" (AO-31) | https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/ | A | Skills de design: description como gatilho, Gotchas. Verificado (2026-06-03). |
| Output styles (AO-13) | https://code.claude.com/docs/en/output-styles | A | Estilo "design reviewer"; estilo não é garantia. |
| a11y.instructions.md, WCAG 2.2 AA (CT-19) | https://github.com/github/awesome-copilot | B (7) | Semântica, ARIA, teclado, formulários; "Placeholder is a hint, not a label"; "Test at 320px CSS width." MIT. Acrescentar axe/Lighthouse. |
| gstack design (BR-23) | https://github.com/garrytan/gstack | B | Notas 0 a 10 por dimensão com "o que seria um 10"; lista anti-slop; `impeccable/DESIGN.md` Apache-2.0 por THIRD_PARTY_NOTICES. |
| gstack `plan-eng-review` / design reviews (EC-11) | https://github.com/garrytan/gstack | B | Revisão antes de construir; só revisa. |
| Willison, agentic patterns (CP-11) | https://simonwillison.net/guides/agentic-engineering-patterns/ | B | Browser automation e screenshots como evidência de UI. |
| How Anthropic teams use Claude Code (CP-15) | https://claude.com/blog/how-anthropic-teams-use-claude-code | B | Equipe de design: descrever comportamento observado. Não reverificado. |
| Harnesses para apps (AO-20) | https://www.anthropic.com/engineering/harness-design-long-running-apps | A | Avaliador separado e cético também para qualidade visual. |
| anthropics/skills `canvas-design` e outros (AO-28) | https://github.com/anthropics/skills | A | Existem entre as 19 skills (listadas); propósito Inferido só pelo nome. |
| Aider conventions (CT-26) | https://aider.chat/docs/usage/conventions.html | B | Exemplo mínimo com efeito observável como técnica pedagógica. Não reverificado. |
| Ask HN (CP-21) | https://news.ycombinator.com/item?id=46691243 | B | Não específico: usar só como calibração de expectativa. |
| awesome-copilot performance (CT-19) | https://github.com/github/awesome-copilot | B | CLS/INP como parte de UX. MIT. |

## 2. Repositórios e arquivos a abrir
- `anthropics/skills/frontend-design` (SKILL.md, LICENSE.txt).
- `garrytan/gstack/design-review`, `design-consultation`, `plan-design-review` (também no snapshot) e `impeccable/DESIGN.md`.
- `github/awesome-copilot/instructions/a11y.instructions.md`.
- Apple HIG, Material, WCAG 2.2, Nielsen heuristics, Refactoring UI e docs de Figma/tokens (W3C Design Tokens) não estão no atlas: lente authoritative.

## 3. Materiais oficiais Anthropic pertinentes
AO-13, AO-28, AO-31, AO-20, AO-06 (verificação visual); `design:` skills do ambiente não são fonte do atlas (não citar).

## 4. Padrões da comunidade
- Tokens e produto antes do código; lista de anti-padrões genéricos (AO-28, BR-23).
- Screenshots como evidência; teste de a11y automatizado + manual (CP-11, CT-19).
- Notas por dimensão com descrição do 10 (BR-23).
- `apple-design.md` como preferência de acabamento, não imposição (BR-23).

## 5. O que o brain-of-agent já oferece
- `brains/fullstack/references/apple-design.md`, `brains/qa/references/acessibilidade.md`, `vendor/gstack/design-review/SKILL.md`, `design-consultation/SKILL.md`, `plan-design-review/SKILL.md`.
- BR-10: `auditoria_axe.py`; BR-14: WebAIM Million 2026 (não rechecado), EAA e NBR 17060 (não verificados).
- BR-23, BR-18 (value card com "Não coberto").
- BR-03: modo `UXUI-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte aprovada para pesquisa com usuários, arquitetura de informação, heurísticas de Nielsen, UX writing, motion, handoff.
- Nenhuma lente de comunidade aprovada para UX (gap declarado em CP).
- Avaliação visual por LLM é subjetiva: usar rubrica binária com critérios (PC-16) e rotular Inferido.
