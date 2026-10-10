# code-quality-refactoring — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| claude-code `plugins/` (AO-29) | https://github.com/anthropics/claude-code/tree/main/plugins | A | Esqueleto de revisor: Papel · Escopo (diff) · Checks · Pontuação 0–100 · `path:linha` · Não reportar; limiar ≥ 80; "em dúvida, não flagre"; paralelismo de 2 a 4 agentes. Destilar. |
| claude-plugins-official (AO-30) | https://github.com/anthropics/claude-plugins-official | A | `code-simplifier` ("never change what the code does"), `code-modernization`, `claude-md-management`. Apache-2.0. |
| Skill /simplify e /batch (CP-14) | https://support.claude.com/en/articles/14554000-claude-code-power-user-tips | A | Comandos nativos para simplificação e mudanças em lote. |
| Migração em massa (AO-31) | https://claude.com/blog/ai-code-migration | A | Construir o juiz primeiro, rulebook, fila em disco, revisão adversarial, paridade comportamental. |
| Best practices Claude Code (AO-06) | https://code.claude.com/docs/en/best-practices | A | Revisor adversarial "gaps, não estilo"; padrões de falha. |
| Common workflows (AO-14) | https://code.claude.com/docs/en/common-workflows | A | Refactor incremental, bug com repro e stack. |
| Prompting Fable 5.1 (AO-03) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 | A | Pedido = escopo; bugs vizinhos viram follow-up; edições cirúrgicas. |
| superpowers (EC-01) | https://github.com/obra/superpowers | A | Debug sistemático; parar após 3 correções. |
| VoltAgent subagents (EC-09) | https://github.com/VoltAgent/awesome-claude-code-subagents | B | Revisores com tools somente leitura. |
| wshobson `debugger.md` e git-pr-workflows (EC-10) | https://github.com/wshobson/agents | B | 5 passos; sem `tools`: corrigir. |
| code-review-generic (CT-20) | https://github.com/github/awesome-copilot | B | Três níveis, template de comentário, PR grande por blocos (segurança → testes → lógica → estilo). Trocar emojis por rótulos. |
| Codex Code Review Rules (CT-03) | https://learn.chatgpt.com/docs/agent-configuration/agents-md | A | Uma linha = comportamento a sinalizar + exceção segura; lint fica no CI. |
| NestJS anti-hallucination (CT-08) | https://github.com/PatrickJS/awesome-cursorrules | B | Tabela de substitutos por versão. CC0. |
| Debug.agent e critical-thinking (CT-21) | https://github.com/github/awesome-copilot | B | Reproduzir antes de mudar; fix mínimo + regressão. |
| Sanglard (CT-29) | https://fabiensanglard.net/agent.md/index.html | B | Bug = teste que falha primeiro; nova sessão por feature. Sem licença. |
| vercel-labs/agent-skills (EC-07) | https://github.com/vercel-labs/agent-skills | A- | Regras com motivo, ruim e bom. |
| agent-os (EC-17) | https://github.com/buildermethods/agent-os | B | Extrair standards do codebase. |
| Boris Tane e Dex Horthy (CP-03, CP-06) | https://boristane.com/blog/how-i-use-claude-code/ | B | Plano → implementação mecânica com typecheck; handoff. |
| gstack `/review`, `/investigate`, `/health` (BR-16, 17, 24) | https://github.com/garrytan/gstack | B | Achado com severidade, confiança 1–10, `arquivo:linha`, cenário e ação AUTO-FIX/ASK/INFO; máx. 3 ciclos. |
| Dan Luu e Lars Faye (CP-20) | https://danluu.com/ai-coding/ | B | Limitar o diff ao que se revisa. |
| Sanity, 95% garbage (CP-22) | https://www.sanity.io/blog/first-attempt-will-be-95-garbage | B | Marcar código editado por humano; 3 camadas de revisão. |
| Reflexion, Self-Refine (PC-23) | https://arxiv.org/abs/2303.11366 | A | Autoavaliação não é validação externa. |

## 2. Repositórios e arquivos a abrir
- `anthropics/claude-code/plugins` (code-review, feature-dev, pr-review-toolkit se existir: não detalhado no atlas), `claude-plugins-official/plugins/code-simplifier`, `code-modernization`.
- `obra/superpowers/skills/systematic-debugging/SKILL.md` (Verificado).
- `github/awesome-copilot/instructions/code-review-generic.instructions.md`, `agents/debug.agent.md`.
- `wshobson/agents/plugins/debugging-toolkit`.
- Livros e normas (Clean Code, Refactoring, Working Effectively with Legacy Code) não estão no atlas; só docs/autores aprovados.

## 3. Materiais oficiais Anthropic pertinentes
AO-03, AO-06, AO-14, AO-20, AO-26 (revisão em CI), AO-29, AO-30, AO-31 (migração), AO-18. Mais: https://github.com/anthropics/claude-code-action.

## 4. Padrões da comunidade
- Revisor read-only, por severidade, em contexto novo (CP-16).
- Escopo cirúrgico; PR pequeno; não gerar mais do que se revisa (CP-20).
- Re-planejar em vez de empilhar correção; `/clear` após 2 correções (AO-06, CP-14).
- Judge-first em migração: paridade comportamental (AO-31).
- Vozes críticas sobre repro falso (CP-20).

## 5. O que o brain-of-agent já oferece
- `brains/fullstack/references/testes-e-debugging.md`, `vendor/gstack/review/SKILL.md` (1.118 linhas), `investigate/SKILL.md`, `health/SKILL.md`.
- BR-16 (`/review`), BR-17 (`/investigate`; unificar com `testes-e-debugging.md`), BR-24 (`/test-audit`, `/health`), BR-15 (Completion Status: DONE/DONE_WITH_CONCERNS/BLOCKED/NEEDS_CONTEXT), BR-12 (tabela resposta a revisão).
- BR-03: modo `QUALIDADE-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte aprovada para análise estática por linguagem, upgrades de framework/dependência, métricas de complexidade.
- Em agente somente leitura, tudo vira ASK (BR-16).
- Superpowers e gstack têm preâmbulos longos e tom CAPS; destilar.
- Hook-development do claude-code tem exemplo inconsistente com a doc de hooks (AO-29).
