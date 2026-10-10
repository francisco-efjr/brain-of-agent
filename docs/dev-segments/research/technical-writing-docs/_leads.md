# technical-writing-docs — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. Princípios comuns: `docs/foundation/prompt-principles.md`. Inclui documentação para agentes (CLAUDE.md/AGENTS.md), onde o atlas é denso.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| CLAUDE.md / rules / memory (AO-07) | https://code.claude.com/docs/en/memory | A | CLAUDE.md é contexto, não enforcement; < 200 linhas; `.claude/rules` com `paths`; `@imports` (até 4 saltos); `/doctor`. Estrutura mínima: Comandos · Convenções divergentes · Fluxo · Armadilhas. Verificado (CT-04). |
| AGENTS.md (CT-01) | https://agents.md/ | A | Markdown puro; o mais próximo prevalece; regra de ouro: só o que o agente não descobre lendo o repo. Repo https://github.com/agentsmd/agents.md (MIT, 24.846★). |
| Evidência sobre arquivos de contexto (CT-02) | https://arxiv.org/abs/2602.11988 | A/B | Contexto +20% de custo sem ganho médio; checklist do que merece uma linha. Também: https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files (100–150 linhas), https://addyosmani.com/blog/agents-md. |
| Writing a good CLAUDE.md, HumanLayer (CP-04) | https://www.humanlayer.dev/blog/writing-a-good-claude-md | B | WHAT/WHY/HOW; raiz curta; `agent_docs/`; ponteiros `arquivo:linha`. |
| Why does CLAUDE.md keep growing? (CP-05) | https://arxiv.org/abs/2608.11095 | B | Comentário de motivo por regra; poda a cada troca de modelo; autor único. |
| Skill authoring best practices (AO-04) | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | A | Limites de name/description/linhas; Verificado. |
| Agent Skills spec (AO-05) | https://agentskills.io/specification | A | Campos name, description, license, compatibility (≤500), metadata, allowed-tools. |
| Thariq, 9 dicas de skills (CP-07) | https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/main/tips/claude-thariq-tips-17-mar-26.md | A | Checklist de SKILL.md; compilação MIT. |
| Piebald `claude-md-creation` (EC-08) | https://github.com/Piebald-AI/claude-code-system-prompts | B | Incluir comandos e arquitetura de alto nível; excluir conselho genérico. Destilar (texto é da Anthropic). |
| claude-md-management (AO-30) | https://github.com/anthropics/claude-plugins-official | A | Plugin oficial; Apache-2.0. |
| README e commits (CT-13) | https://github.com/PatrickJS/awesome-cursorrules | B | "Write READMEs like landing pages, not API docs."; exemplo funcional nas 5 primeiras linhas. CC0. Conventional Commits: citar conventionalcommits.org. |
| Spec-driven e memory bank (CT-22) | https://docs.cline.bot/prompting/cline-memory-bank | B | Memory Bank custa tokens; Claude Code tem auto memory. |
| Windsurf/Devin limites (CT-25) | https://docs.devin.ai/desktop/cascade/memories | B | Orçamento de ~100 linhas sempre ativas; blocos XML por tema. |
| Output styles (AO-13) | https://code.claude.com/docs/en/output-styles | A | Estilo de escrita técnica. |
| Prompting best practices (AO-01) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | A | Formato mínimo; sem excesso de listas. |
| Google whitepaper (PC-07) | https://www.kaggle.com/whitepaper-prompt-engineering | B | Ficha de documentação de prompt; cópia lida não oficial. |
| awesome-copilot `documentation-writer` e `breakdown-*` (CT-14) | https://github.com/github/awesome-copilot | A | Skills de documentação (nomes citados; conteúdo não lido). |
| Sanglard (CT-29) | https://fabiensanglard.net/agent.md/index.html | B | Higiene de contexto, recarregar o agent.md. |
| gstack `/document-release` (BR-19) | https://github.com/garrytan/gstack | B | Coverage map Diátaxis; checklist pré-PR. |
| Thariq e Anthropic skills lessons (AO-31) | https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/ | A | Gotchas; description = gatilho. |

## 2. Repositórios e arquivos a abrir
- `agentsmd/agents.md` (exemplos), `Piebald-AI/.../agent-prompt-claude-md-creation.md`.
- `github/awesome-copilot`: `instructions/instructions.instructions.md`, `agents.instructions.md`, skill `documentation-writer`.
- `PatrickJS/awesome-cursorrules/rules/readme-best-practices-…mdc`.
- `anthropics/claude-plugins-official/plugins/claude-md-management`.
- Diátaxis, Keep a Changelog, OpenAPI, Mermaid/C4, Google Developer Documentation Style Guide: não estão no atlas (Diátaxis aparece só no coverage map do gstack): lente authoritative.

## 3. Materiais oficiais Anthropic pertinentes
AO-01, AO-04, AO-05, AO-07, AO-13, AO-14, AO-26 (doc sync em CI), AO-27, AO-30, AO-31, CP-14.

## 4. Padrões da comunidade
- Regra comportamental com comentário de motivo e data (CP-05).
- `agent_docs/` com progressive disclosure e ponteiros `arquivo:linha` (CP-04).
- `@AGENTS.md` como fonte única entre ferramentas (CP-05, CT-04).
- Regras sem "don'ts" soltos: sempre o "do" (CT-02).
- Docs de agentes tratados como potencialmente públicos, sem credenciais (EC-04).

## 5. O que o brain-of-agent já oferece
- `vendor/gstack/document-release/SKILL.md`, `document-generate/SKILL.md`, `brains/fullstack/assets/templates/handoff-checkpoint.md`.
- BR-11 (briefing portátil), BR-06/07 (templates), BR-12 (tabela de resposta a revisão), BR-19 (coverage map Diátaxis), BR-25 (devex).
- BR-03: modo `DOCS-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte aprovada para documentação de API (OpenAPI), tutoriais, changelog, Mermaid/C4 além do que cita o gstack.
- Benchmarks de AGENTS.md são de poucos casos e de fornecedores.
- Textos de ferramentas concorrentes (Cursor, Devin) têm limites próprios: usar só como orçamento de referência.
