# llm-ai-agents — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR). Este é o segmento mais coberto do atlas; a lista é seleção, não inventário completo.
Pista é ponto de partida: reabrir a URL antes de citar. Princípios consolidados: `docs/foundation/prompt-principles.md` (P-01 a P-40).

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| Prompting best practices (AO-01, PC-26) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | A | Contexto/motivação, 3 a 5 exemplos em `<example>`, dados no topo, dial back de linguagem agressiva, prefill removido em 4.6+, `budget_tokens` → adaptive thinking. Verificado. |
| Prompting Claude Fable 5.1 (AO-03) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 | A | Terminar a tarefa inteira, escopo = pedido, compaction preserva decisões e pendências. |
| Effective context engineering + Claude 5 rules (AO-16, PC-27) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | A | Menor conjunto de tokens de alto sinal; regras → julgamento; progressive disclosure. Claude 5 rules: https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/ |
| Building effective agents (AO-15) | https://www.anthropic.com/engineering/building-effective-agents | A | 5 padrões, ACI, poka-yoke. |
| Writing tools for agents (AO-17) | https://www.anthropic.com/engineering/writing-tools-for-agents | A | Descrição como fator principal, consolidar operações, `concise|detailed`. |
| Multi-agent research system (AO-18) | https://www.anthropic.com/engineering/multi-agent-research-system | A | Delegar com objetivo, formato, tools e fronteiras; 90,2% e ~15× tokens (eval interna). |
| Harnesses de longa duração (AO-20) | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | A | `features.json`, rotina de início de sessão, avaliador cético separado. |
| Demystifying evals (AO-21) | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | A | 20 a 50 tarefas reais, pass^k, ler transcripts. |
| Code execution with MCP + workflows (AO-22) | https://www.anthropic.com/engineering/code-execution-with-mcp | A | Tools como APIs de código. |
| Segurança, auto mode (AO-23) | https://www.anthropic.com/engineering/claude-code-auto-mode | A | Classificador não vê tool results; falso-negativo 17% em ações overeager (n=52). |
| System prompts publicados, Fable 5.1 (AO-27) | https://platform.claude.com/docs/en/release-notes/system-prompts/claude-fable-5-1 | A | Só técnica (XML, razão nas regras); prompt consumer, não copiar. |
| claude-cookbooks (AO-25) | https://github.com/anthropics/claude-cookbooks | A | `patterns/agents`, evals, caching. MIT. |
| anthropics/skills (AO-28) | https://github.com/anthropics/skills | A | skill-creator (loop de otimização de `description`), mcp-builder, claude-api; licença por skill. |
| GPT-4.1/5/5.1/5.5, Gemini, Microsoft (PC-01 a PC-10) | https://developers.openai.com/api/docs/guides/latest-model/gpt-5.5 | A | Contraste entre labs; "reconstruir do menor prompt"; antigos arquivados. |
| Hamel / Eugene Yan / Shankar (PC-14 a PC-18) | https://hamel.dev/blog/posts/llm-judge/ | A/B | Evals: binário + crítica, judge validado, análise de erros. |
| Willison, lethal trifecta (PC-21) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | A | Dados privados + conteúdo não confiável + saída externa; 6 padrões de design (arXiv 2506.08837). |
| Chip Huyen, Agents (PC-19) | https://huyenchip.com/2025/01/07/agents.html | B | Validar plano antes de executar; prompt injection em write actions. |
| Papers: CoT, ReAct, Reflexion, LLM-as-judge (PC-22 a PC-24) | https://arxiv.org/abs/2306.05685 | A | Vieses de juiz; CoT mencionou a dica em 25% e 39% (https://www.anthropic.com/research/reasoning-models-dont-say-think). Pré-thinking. |
| CLAUDE.md research (CP-05, CT-02) | https://arxiv.org/abs/2608.11095 | B | 247.694 instruções; comentários de raciocínio; autor único. arXiv 2602.11988 (ETH): contexto +20% custo. |
| AGENTS.md e portabilidade (CT-01, CT-04) | https://agents.md/ | A | Esqueleto; ponte `@AGENTS.md`. |
| awesome-copilot meta-guias (CT-15) | https://github.com/github/awesome-copilot | B | "Add constraints after observed failures"; tools mínimas. MIT. |
| Google ADK .mdc (CT-11) | https://github.com/PatrickJS/awesome-cursorrules | B | Acesso controlado em código, não em prompt. CC0. |
| Brex Prompt Engineering Guide (PC-29) | https://github.com/brexhq/prompt-engineering | B | "Assume that any content in a hidden prompt can be seen by the user."; MIT; datado. |

## 2. Repositórios e arquivos a abrir
- `anthropics/claude-cookbooks/patterns/agents`; `anthropics/skills/skill-creator` e `mcp-builder`.
- `anthropics/claude-code/plugins` (agent-sdk-dev, plugin-dev, hookify) e `claude-plugins-official/plugins/skill-creator`.
- `github/awesome-copilot/instructions/instructions.instructions.md` e `agents.instructions.md`.
- `dair-ai/Prompt-Engineering-Guide`, `stanfordnlp/dspy`, `openai/openai-cookbook` (MIT).
- Piebald-AI/claude-code-system-prompts (classe B, só destilar; texto é da Anthropic) e x1xhlol (rejeitado: nunca usar).

## 3. Materiais oficiais Anthropic pertinentes
AO-01 a AO-04, AO-11 (`claude plugin eval`), AO-12, AO-15 a AO-23, AO-25 a AO-31. Mais: https://code.claude.com/docs/en/subagents · https://code.claude.com/docs/en/plugin-evals.

## 4. Padrões da comunidade
- Subagentes: um escritor por arquivo, revisor read-only, não encadear (CP-16).
- Handoff e compactação intencional (CP-06, CP-18).
- Hooks para o obrigatório, CLAUDE.md curto (CP-01, CP-04, CP-08).
- Loop sem back pressure é anti-padrão; Ralph só em sandbox (CP-17).
- Dissidentes: Dan Luu, Lars Faye (CP-20).

## 5. O que o brain-of-agent já oferece
- `brains/fullstack/references/agentes-e-ia.md`, `brains/qa/references/ia-e-llm.md`, `docs/research/agentes-desenvolvimento.md`.
- BR-05 (formato de evals → `claude plugin eval`), BR-04, BR-11, BR-12, BR-15 (Completion Status), BR-26 (modelo de segurança de automação), BR-27 a BR-29 (formato de plugin, eval, best practices; Verificados).
- BR-03: modo `IA-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte aprovada para RAG de ponta a ponta (chunking, reranking), custo/latência/caching, observabilidade de LLM, fine-tuning.
- Itens de PC marcados não reverificados: R-02, 04, 05, 08, 10, 13, 15, 18 a 20.
- Guias OpenAI antigos estão arquivados; conselhos de 2023 a 2024 estão obsoletos (`prompt-principles.md` §4).
- Metaprompt oficial (`metaprompt.ipynb`) não verificável; não usar.
