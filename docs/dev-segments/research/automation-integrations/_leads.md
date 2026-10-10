# automation-integrations — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR). Segmento denso no atlas, sobretudo em autoria de skills, plugins, hooks e MCP; fraco em n8n/Zapier/Make e webhooks gerais.
Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| Skill authoring best practices (AO-04, BR-29) | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | A | Limites e graus de liberdade; nomes MCP `Server:tool`. Verificado. |
| Plugins + `claude plugin eval` (AO-11, BR-28) | https://code.claude.com/docs/en/plugin-evals | A | 3 execuções, baseline, 6 graders, caso negativo. Verificado. |
| Manifest reference (BR-27) | https://code.claude.com/docs/en/plugins/manifest-reference | A | `name` único obrigatório; `agents`/`commands` substituem scan, `skills` adiciona; sem `bin/`. Verificado. |
| Skills, hooks, subagentes (AO-08, AO-09, AO-10) | https://code.claude.com/docs/en/hooks | A | Campos extras; exit 2 bloqueia; plugins ignoram hooks e mcpServers em agentes. |
| Extend Claude Code + Steering (AO-12) | https://code.claude.com/docs/en/features-overview | A | Hook → CLAUDE.md → regra → skill → subagente → MCP. |
| Writing tools for agents e define tools (AO-17) | https://www.anthropic.com/engineering/writing-tools-for-agents | A | Consolidar operações, erros acionáveis. |
| Code execution with MCP (AO-22) | https://www.anthropic.com/engineering/code-execution-with-mcp | A | Tools como APIs de código; filtrar dados no ambiente. |
| Equipping agents with Agent Skills (AO-19) | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | A | Scripts fora do contexto; auditar skills de terceiros. |
| anthropics/skills `mcp-builder`, `skill-creator` (AO-28) | https://github.com/anthropics/skills | A | 10 perguntas de eval independentes; otimização da `description`. Licença por skill. |
| claude-plugins-official e claude-code `plugins/` (AO-29, AO-30) | https://github.com/anthropics/claude-plugins-official | A | `mcp-server-dev`, `plugin-dev`, `hookify` (regras `event/pattern/action`). Hook-development tem exemplo inconsistente: seguir AO-10. |
| claude-code-action (AO-26) | https://github.com/anthropics/claude-code-action | A | Triagem de issues, doc sync, manutenção por cron; MIT. |
| Blog "lessons from building Claude Code" (AO-31) | https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/ | A | Nove categorias de skill, Gotchas; medir uso. |
| Thariq, 9 dicas de skills (CP-07) | https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/main/tips/claude-thariq-tips-17-mar-26.md | A | Checklist de SKILL.md; hooks sob demanda. |
| shanraisshan/claude-code-best-practice (CP-08) | https://github.com/shanraisshan/claude-code-best-practice | B | Tabela "onde colocar cada coisa". MIT; compilação de terceiros. |
| hesreallyhim/awesome-claude-code e listas (EC-20) | https://github.com/hesreallyhim/awesome-claude-code | B | Só descoberta; licença NOASSERTION. ComposioHQ e VoltAgent/awesome-agent-skills: conteúdo promocional ou impossível de vetar. |
| Trail of Bits config (EC-12) | https://github.com/trailofbits/claude-code-config | B | `.mcp.json` de projeto desativado por padrão. |
| Hooks guardrail (CP-19) | https://aitmpl.com/blog/secure-git-workflow/ | B | Padrões PreToolUse/PostToolUse/Stop/PostCompact; script stdlib. |
| agents.md e porte entre ferramentas (CT-04, CT-28) | https://github.com/intellectronica/ruler | B | Tabela de porte de regras; ruler só com ≥ 3 ferramentas. |
| awesome-copilot meta-guias (CT-15) | https://github.com/github/awesome-copilot | B | Tools mínimas; "do not add rules for failures that have not occurred". |
| Cline/Roo, Aider (CT-24, CT-26) | https://docs.cline.bot/features/cline-rules | B | Um tema por arquivo; regras por modo → subagente. |
| Willison, lethal trifecta (PC-21) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | A | Conteúdo de webhook/API é não confiável; padrões de design. |
| gstack `/scrape`, `/skillify` (BR-26) | https://github.com/garrytan/gstack | B | Ler livre, agir com confirmação; credenciais nunca passam pelo agente; registrar o que sai antes de enviar. |

## 2. Repositórios e arquivos a abrir
- `anthropics/skills/mcp-builder`; `claude-plugins-official/plugins/mcp-server-dev`, `skill-creator`, `claude-code-setup`.
- `anthropics/claude-code/plugins/plugin-dev`, `hookify`.
- `trailofbits/claude-code-config`; `shanraisshan/claude-code-best-practice/tips`.
- `github/awesome-copilot` plugins `*-mcp-development` (nomes citados).
- Docs de n8n, Zapier, Make, spec MCP e boas práticas de webhooks (assinatura, idempotência, retry) não estão no atlas: lente authoritative. Verificação de assinatura aparece só em security-and-owasp (CT-16).

## 3. Materiais oficiais Anthropic pertinentes
AO-04, AO-05, AO-08 a AO-12, AO-17, AO-19, AO-22, AO-26, AO-28 a AO-31, CP-07, CP-14. Doc de segurança: https://code.claude.com/docs/en/security.

## 4. Padrões da comunidade
- Hooks como guardrails determinísticos, documentados com evento, matcher, script, exit codes, teste e desativação (CP-19).
- Skills pequenas e componíveis; `disable-model-invocation` para efeitos (CP-10, AO-08).
- Ralph só em sandbox, com back pressure (CP-17).
- Supply chain: pin por SHA, inspecionar customizações de terceiros (CT transversais).
- Skill/instalador de terceiros (ECC, gstack `setup`): documentar, não executar (EC).

## 5. O que o brain-of-agent já oferece
- `vendor/gstack/scrape/SKILL.md`, `vendor/gstack/skillify/SKILL.md`.
- BR-13 (router + `registry/skills.json`, 64 entradas; "selecionar `ship` não autoriza merge/deploy"), BR-26, BR-27 a BR-29 (Verificados), BR-05, BR-15.
- BR-03: modo `AUTOMACAO-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte aprovada para n8n/Zapier/Make, webhooks (retry, replay), scraping responsável, bots, jobs agendados além de CI.
- Não ativar hooks nem `.mcp.json` por padrão; documentar em `references/`.
- Alegação de "20% de submissões maliciosas" (ClawHub) é de fornecedor, Não verificada.
