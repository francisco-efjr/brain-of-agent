# qa-testing — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR). Segmento mais bem coberto pelo brain do usuário.
Pista é ponto de partida: reabrir a URL antes de citar. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| superpowers TDD (EC-01, CP-09) | https://github.com/obra/superpowers | A | Iron Law: sem produção sem teste vermelho pelo motivo certo; verde com suíte inteira; bug = teste antes do fix; tabelas de racionalização; red flags. MIT; tom a calibrar. |
| mattpocock/skills (CP-10) | https://github.com/mattpocock/skills | B | Anti-padrões de teste (acoplado à implementação, tautológico, fatiamento horizontal); testar por interface pública. MIT; 282.946★. |
| Willison, agentic patterns (CP-11) | https://simonwillison.net/guides/agentic-engineering-patterns/ | B | Red/green TDD e confirmar o vermelho; testes manuais agentic; registrar comando + saída real. |
| anthropics/skills `webapp-testing` (AO-28) | https://github.com/anthropics/skills | A | Reconhecimento → ação com Playwright. Conferir LICENSE. |
| Demystifying evals (AO-21) | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | A | pass@k × pass^k, graders de resultado, ler transcripts. |
| `claude plugin eval` (AO-11, BR-28) | https://code.claude.com/docs/en/plugin-evals | A | 3 execuções, baseline, 6 tipos de grader; caso "ignora pedido não relacionado". Claude Code ≥ 2.1.269. |
| Best practices Claude Code (AO-06) | https://code.claude.com/docs/en/best-practices | A | Verificação em 4 graus; pedir evidência. |
| qa-engineering-best-practices e playwright-typescript (CT-17) | https://github.com/github/awesome-copilot/tree/main/instructions | B | Pirâmide 60-70/20-30/5-10; determinismo; mock na borda; seletores role → label → test-id → text. MIT. Não reabertos. |
| playwright-e2e e gherkin (CT-13) | https://github.com/PatrickJS/awesome-cursorrules | B | `page.route`, auto-wait; Gherkin em linguagem de negócio. CC0. |
| Hamel / Shreya evals (PC-16, PC-17) | https://hamel.dev/blog/posts/evals-faq/ | A | Binário + crítica; asserção em código antes de LLM-judge. |
| Eugene Yan, evaluators (PC-15) | https://eugeneyan.com/writing/llm-evaluators/ | B | Vieses de judge. |
| Harness longa duração (AO-20) | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | A | `features.json` com `passes`; avaliador separado e cético. |
| Compilador C, saída de teste para o modelo (AO-31) | https://www.anthropic.com/engineering/building-c-compiler | A | Console mínimo, log em arquivo. |
| Dan Luu (CP-20) | https://danluu.com/ai-coding/ | B | Fuzzing vs LLM; "pronto" sem saída de comando não vale. |
| Ralph loop, back pressure (CP-17) | https://ghuntley.com/ralph/ | B (5) | Testes + tipos/lint como back pressure; proibido afrouxar testes. Só sandbox. |
| ykdojo `TESTING.md` (CP-18) | https://github.com/ykdojo/claude-code-tips | B | Agente documenta o que testou, comando, saída, e o que não testou. NOASSERTION: destilar. |
| gstack `/qa`, `/qa-only`, `/test-audit` (BR-18, BR-24) | https://github.com/garrytan/gstack | B | Tiers por risco, "value card" com "Não coberto", retirement card de testes de baixo valor. |
| Subagentes na prática (CP-16) | https://hamy.xyz/blog/2026-02_code-reviews-claude-subagents | B | test-author separado do implementer, proibido enfraquecer testes. |
| Ask HN e Sanity (CP-21, CP-22) | https://www.sanity.io/blog/first-attempt-will-be-95-garbage | B | Revisão em 3 camadas; regra das 3 tentativas. |
| Mobile SwiftUI .mdc (CT-12) | https://github.com/PatrickJS/awesome-cursorrules | B | Mocks por protocolo, warnings como erros. |

## 2. Repositórios e arquivos a abrir
- `obra/superpowers/skills/test-driven-development` e `verification-before-completion` (nomes citados no atlas; abrir e verificar).
- `mattpocock/skills` (arquivos auxiliares não lidos).
- `github/awesome-copilot/instructions/qa-engineering-best-practices*`, `playwright-typescript*`.
- `anthropics/skills/webapp-testing`; `claude-code/plugins` (pr-review-toolkit; nome não detalhado no atlas: Não verificado).
- Playwright/Cypress/Vitest/Jest docs, ISTQB, mutation testing não estão no atlas (ISTQB BVA não rechecado).

## 3. Materiais oficiais Anthropic pertinentes
AO-02, AO-06, AO-09, AO-11, AO-20, AO-21, AO-28, AO-29, AO-30, AO-31, CP-13, CP-14.

## 4. Padrões da comunidade
- Confirmar o vermelho; testes por interface pública; nomes no glossário do domínio (CP-10, CP-11).
- Anti-padrões: testes tautológicos, acoplados à implementação, fatiamento horizontal (CP-10).
- Teste-autor separado; sem enfraquecer testes (CP-16, CP-17).
- Flaky: retry 1x e sinalizar (CT-17); ≥3 execuções para avaliar abordagem (CP-20).
- Evidência de teste gerada na sessão, não relato (CP-20).

## 5. O que o brain-of-agent já oferece
- `brains/qa/SKILL.md` (283 linhas, v0.3.0), `protocolo-qa-completo.md`, `estrategia.md`, `design-de-testes.md`, `unitarios-e-integracao.md`, `bugs-e-relatorios.md`, `brains/fullstack/references/testes-e-debugging.md`, `vendor/gstack/qa/SKILL.md`, `qa-only`, `test-audit`.
- BR-01 (molde de playbook), BR-04, BR-05 (evals → `claude plugin eval`), BR-06 (9 templates QA), BR-08 (BVA, tabela de decisão, pairwise, SBTM/SFDPOT), BR-10 (scripts stdlib: `pairwise.py`, `valores_limite.py`, `repetir_teste.py`), BR-12, BR-18, BR-24.
- Ressalva: skill `qa` colide com o namespace; no plugin usar `playbook`.
- BR-03: modo `QA-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte aprovada para property-based, mutation, contrato (Pact), performance (k6), flaky além de retry.
- Superpowers tem tom de "1% de chance"; calibrar (D10).
- Brain `metadata` do SKILL.md é inerte no Claude Code; não depender.
