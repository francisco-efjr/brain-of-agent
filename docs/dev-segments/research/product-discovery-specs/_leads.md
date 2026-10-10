# product-discovery-specs — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO = anthropic-official, EC = claude-code-ecosystem item nn, CT = cross-tool-rules, PC = prompt-engineering-canon, CP = community-pulse, BR = brain-of-agent).
Regra: pista é ponto de partida, não fonte final. O pesquisador do segmento reabre a URL antes de citar. Rótulos: Verificado / Inferido / Não verificável; "Dest." = destilar com redação própria.
Princípios de prompt comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| spec-kit, `templates/spec-template.md` (EC-02) | https://github.com/github/spec-kit | A | Histórias P1/P2/P3 testáveis em separado com Given/When/Then; `FR-NNN`, `SC-NNN` sem tecnologia; Assumptions; `[NEEDS CLARIFICATION]` (Verificado). MIT. Só o template foi lido. |
| superpowers, brainstorming (EC-01, CP-09) | https://github.com/obra/superpowers | A | Decisão inicial (pedido completo: fazer; faltou algo: conversar), uma pergunta por mensagem, "play back" curto, gate duro de aprovação, design doc revisado por subagente novo. MIT; adaptar o tom "MUST". |
| Best practices for Claude Code (AO-06, CP-02) | https://code.claude.com/docs/en/best-practices | A | Prompt de entrevista (AskUserQuestion) → `SPEC.md` → sessão nova; Explore → Plan → Implement → Commit. Dest. |
| Agentic coding and persistent returns to expertise (CP-13) | https://www.anthropic.com/research/claude-code-expertise | A | Todo pedido gerado traz escopo, verificação literal, critério de pronto e o que não mudar. Achados preliminares. |
| Spec-driven workflow v1 (CT-22) | https://github.com/github/awesome-copilot | B | EARS ("WHEN … THE SYSTEM SHALL …"), fases ANALYZE → … → HANDOFF, gate por confiança (>85% / 66–85% / <66%). MIT. "Never skip any step" é rígido. |
| Implementation-plan e ADR agents (CT-21) | https://github.com/github/awesome-copilot | B | Plano sem edições, fases com critério mensurável, IDs `REQ-/TASK-/RISK-`; ADR pede dados e para se faltar. Ao portar, tools somente leitura. |
| Code-modernization, claude-plugins-official (AO-30) | https://github.com/anthropics/claude-plugins-official | A | Regras de negócio em Given/When/Then com `file:line`; aprovação humana antes de construir. Apache-2.0. |
| feature-dev, claude-code `plugins/` (AO-29) | https://github.com/anthropics/claude-code/tree/main/plugins | A | Paradas obrigatórias: perguntas, escolha de arquitetura, aprovação. Repo sem licença: destilar. |
| Harness para longa duração (AO-20) | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | A | `features.json` com `passes` (só ele muda), rotina de início de sessão. Evidência qualitativa. |
| Multi-agent research system (AO-18) | https://www.anthropic.com/engineering/multi-agent-research-system | A | Orquestrador delega com objetivo, formato, tools e fronteiras; útil para pesquisa de descoberta. |
| 10 Lessons for Agentic Coding, Breunig (CP-23) | https://www.dbreunig.com/2026/05/04/10-lessons-for-agentic-coding.html | B | Três artefatos vivos (SPEC.md, e2e comportamentais, notas de intenção); diffar spec vs construído. Ensaio sem dados. |
| SPEC.md curto, Dwyer (CP-25) | https://www.dwyer.co.za/static/claude-code-is-all-you-need.html | B | SPEC ≤ ~500 palavras: problema, usuários, requisitos testáveis, fora de escopo, interfaces, restrições, verificação. Ignorar `--dangerously-skip-permissions`. |
| Boris Tane, research → plan (CP-03) | https://boristane.com/blog/how-i-use-claude-code/ | B | `research.md` → `plan.md` → anotação humana → checklist de fases. |
| Ask HN: evidência de agentic coding (CP-21) | https://news.ycombinator.com/item?id=46691243 | B | Texto de calibração para README: organiza processo, não promete ganhos. |
| BMAD, ccpm, OpenSpec, SuperClaude (EC-14, 15, 16, 18) | https://github.com/Fission-AI/OpenSpec | B | Deltas de spec (adicionado/modificado/removido); papéis ágeis; PRD → épico → issues. BMAD (NOASSERTION) e ccpm (último push 2026-03-18) só ideias. |
| gstack plan-eng-review (EC-11) | https://github.com/garrytan/gstack | B | Scope Challenge antes da revisão; só revisa. Não executar `bin/` nem `setup`. |

## 2. Repositórios e arquivos a abrir
- `github/spec-kit`: `plan` e `tasks` não foram lidos pelo atlas; abrir `templates/` completo e a pasta `.specify/` (README, não reconferido).
- `obra/superpowers`: `skills/brainstorming/SKILL.md` (~228 linhas no original).
- `github/awesome-copilot`: `instructions/spec-driven-workflow-v1.instructions.md`, `agents/implementation-plan.agent.md`, `agents/adr-generator.agent.md`, skills `breakdown-*`.
- `anthropics/claude-code`: `plugins/feature-dev`. `anthropics/claude-plugins-official`: `plugins/code-modernization`.
- `anthropics/skills`: `skill-creator` (captura de intenção, entrevista de bordas; conferir LICENSE antes de literal).
- PatrickJS/awesome-cursorrules `gherkin-style-testing-…mdc` (CC0) para critérios de aceite (CT-13).

## 3. Materiais oficiais Anthropic pertinentes
AO-06 (entrevista → SPEC), AO-13 (output styles, para modo de entrevista), AO-18, AO-20, AO-29, AO-30, CP-13. Docs: https://code.claude.com/docs/en/best-practices · https://code.claude.com/docs/en/common-workflows (AO-14, bug com repro e stack).

## 4. Padrões da comunidade
- Pergunta única por mensagem e gate de aprovação antes de construir (CP-09, EC-01).
- Spec revisada → sessão nova só com a spec → registrar divergências no fim (CP-25, CP-23).
- Spec sem detalhes de implementação, com marcador de dúvida aberta (EC-02, EC-18).
- Pré-loop tipo Ralph: critérios na spec revisada por humano, um item por iteração (CP-17); só em sandbox.
- Calibração: não prometer ganhos; medir em mais de uma execução (CP-21, CT-02 AAIF).

## 5. O que o brain-of-agent já oferece
- Arquivos de `segments.json`: `brains/qa/references/requisitos-e-bdd.md`; `vendor/gstack/office-hours/SKILL.md`, `plan-ceo-review/SKILL.md`, `spec/SKILL.md` (gstack, MIT, destilar com atribuição).
- BR-20: premissas e alternativas antes da solução; esqueleto de spec (problema, resultado mensurável, não-objetivos, `REQ-NN`, bordas, aceite, perguntas abertas). `spec` cria issue: exigir autorização; tirar jargão "CEO/10-star".
- BR-06/07 templates: ADR, plano de incremento, handoff-checkpoint. BR-11: esqueleto de briefing (produto, pedido, escopo, stack, fontes, ambiente, restrições, entrega, aceite).
- BR-03: modo `PRODUTO-COMPLETO` por keyword explícita.

## 6. Lacunas e cuidados
- Sem fonte A sobre JTBD, RICE/ICE/MoSCoW/Kano, OKRs, experimentos A/B e roadmap: o atlas global não cobre; exigir pesquisa própria do segmento.
- Fontes de comunidade são de praticantes de código, não de produto.
- Gate de aprovação conflita com autonomia: deixar o gate configurável e documentado.
- Não copiar BMAD (NOASSERTION); ccpm desatualizado e o próprio projeto desaconselha uso em debug/teste/review.
