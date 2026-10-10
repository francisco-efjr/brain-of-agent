# Fontes: bibliografia validada do segmento Aplicações LLM, agentes e engenharia de prompt

Consulta e validação: 2026-10-10 · Modelo-alvo: família Claude 4.x/5.x · Rótulos: Verificado, Inferido, Suposição, Não verificável.
Classe A: oficial da Anthropic ou documentação/norma da tecnologia. Classe B: repositório com licença clara e uso, ou especialista reconhecido. Classe C: comunidade ou fornecedor, usado como sinal. "Destilar" = sem permissão de cópia literal verificada; só redação própria.
Origem: itens `V-nn` vêm de `docs/dev-segments/research/llm-ai-agents/VALIDATED.md` (conferidos por um validador da família Claude, independência parcial; a API do GitHub estava bloqueada, então estrelas e licenças foram lidas nas páginas dos repositórios e as datas de commit nos feeds `commits.atom`). Nenhuma fonte externa abaixo tem licença de reuso confirmada que permita cópia: tudo o que o plugin traz delas é destilado. Única exceção: trechos do brain-of-agent (MIT, conteúdo do próprio autor).

## Sumário

1. Top 20 por valor para o plugin
2. Complementares aprovados
3. Conteúdo próprio do usuário e material de terceiros
4. Metadados de repositórios (2026-10-10)
5. Rejeitadas e rebaixadas
6. Lacunas
7. Política de uso e licenças
8. Gotchas

## 1. Top 20

| # | Título (item) | URL | Classe | Licença de reuso | Consulta | Usada em |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Claude prompting best practices (V-01); Prompting Fable 5.1 (V-02); novas regras de context engineering para Claude 5 (V-03, Thariq Shihipar, 2026-07-24) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices · https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 · https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/ | A | não declarada; destilar | 2026-10-10 | `prompting-claude`, `llm-prompt-review` |
| 2 | Claude Code best practices (V-20) | https://code.claude.com/docs/en/best-practices | A | não declarada; destilar | 2026-10-10 | `claude-md-snippets`, `padroes-e-antipadroes` |
| 3 | Effective context engineering for AI agents (V-06) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | A | destilar | 2026-10-10 | `agentes-contexto-harness` |
| 4 | Building effective agents (V-04; 2024-12-19, aviso de ferramentas desatualizadas) | https://www.anthropic.com/engineering/building-effective-agents | A | destilar | 2026-10-10 | `agentes-contexto-harness`, `decisoes-e-tradeoffs` |
| 5 | Writing tools for agents (V-05; 2025-09-11) | https://www.anthropic.com/engineering/writing-tools-for-agents | A | destilar | 2026-10-10 | `tool-design-e-mcp` |
| 6 | How we built our multi-agent research system (V-07; 2025-06-13) | https://www.anthropic.com/engineering/multi-agent-research-system | A | destilar | 2026-10-10 | `agentes-contexto-harness` |
| 7 | Demystifying evals for AI agents (V-09; 2026-01-09) | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | A | destilar | 2026-10-10 | `avaliacao` |
| 8 | Effective harnesses for long-running agents (V-08; 2025-11-26) | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | A | destilar | 2026-10-10 | `agentes-contexto-harness` |
| 9 | Claude Code auto mode (V-13; 2026-03-25) | https://www.anthropic.com/engineering/claude-code-auto-mode | A | destilar | 2026-10-10 | `seguranca-guardrails` |
| 10 | Mitigate jailbreaks and prompt injections (docs) + prompt-injection defenses (pesquisa, 2025-11-24) (V-43) | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks · https://www.anthropic.com/research/prompt-injection-defenses | A | destilar | 2026-10-10 | `seguranca-guardrails` |
| 11 | Meta "Agents Rule of Two" (2025-10-31) + arXiv 2506.08837 + arXiv 2510.09023 + resumo de Willison (V-42, V-14) | https://ai.meta.com/blog/practical-ai-agent-security/ · https://arxiv.org/abs/2506.08837 · https://arxiv.org/abs/2510.09023 · https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/ | A (Meta, arXiv); B (Willison) | não verificada (resumos lidos, PDFs não) | 2026-10-10 | `seguranca-guardrails` |
| 12 | Claude Code subagents (V-19) | https://code.claude.com/docs/en/subagents | A | destilar | 2026-10-10 | `agentes-contexto-harness` |
| 13 | Claude Code memory (V-21) + "Writing a good CLAUDE.md", HumanLayer (2025-11-25) | https://code.claude.com/docs/en/memory · https://www.humanlayer.dev/blog/writing-a-good-claude-md | A + B | destilar | 2026-10-10 | `claude-md-snippets` |
| 14 | Skills, slash commands, hooks, plugins + post "seven methods" (V-40; 2026-06-18) | https://code.claude.com/docs/en/skills · https://code.claude.com/docs/en/hooks · https://code.claude.com/docs/en/plugins · https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more | A | destilar | 2026-10-10 | `decisoes-e-tradeoffs`, `ferramentas-e-mcp` |
| 15 | Plugin evals (V-12, V-41) | https://code.claude.com/docs/en/plugin-evals | A | destilar | 2026-10-10 | `avaliacao` |
| 16 | anthropics/skills: skill-creator e mcp-builder (V-23) | https://github.com/anthropics/skills | A | sem arquivo único de licença; só destilar | 2026-10-10 | `prompts`, `instruction-authoring` |
| 17 | MCP: security best practices e authorization (2025-11-25) + conceito de tools (V-44, V-18) | https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices · https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization · https://modelcontextprotocol.io/docs/concepts/tools | A | não declarada; destilar | 2026-10-10 | `tool-design-e-mcp` |
| 18 | Prompt caching + pricing + batch + token counting + choosing a model (V-24, V-38) | https://platform.claude.com/docs/en/build-with-claude/prompt-caching · https://platform.claude.com/docs/en/about-claude/pricing · https://platform.claude.com/docs/en/build-with-claude/batch-processing · https://platform.claude.com/docs/en/build-with-claude/token-counting · https://platform.claude.com/docs/en/about-claude/models/choosing-a-model | A | destilar | 2026-10-10 | `rag-custo-observabilidade` |
| 19 | Claude API: tool use, structured outputs, streaming, citations, search results (V-35, V-37) | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview · https://platform.claude.com/docs/en/build-with-claude/structured-outputs · https://platform.claude.com/docs/en/build-with-claude/streaming · https://platform.claude.com/docs/en/build-with-claude/citations · https://platform.claude.com/docs/en/build-with-claude/search-results | A | destilar | 2026-10-10 | `tool-design-e-mcp`, `rag-custo-observabilidade` |
| 20 | Using LLM-as-a-judge, Hamel Husain (V-10; 2024-10-29, mod. 2026-09-01) | https://hamel.dev/blog/posts/llm-judge/ | B (7/10) | destilar | 2026-10-10 | `avaliacao` |

## 2. Complementares aprovados

| Item | Fonte | Classe | Licença observada | Uso |
| --- | --- | --- | --- | --- |
| V-11 | https://eugeneyan.com/writing/llm-patterns/ · https://eugeneyan.com/writing/evals/ | B | não declarada | Vieses do juiz; métrica por tarefa; conteúdo de 2023-2024 |
| V-14 | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ · https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/ | B | não declarada | Trifecta letal (superada em rigor por V-42) |
| V-15 | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ · https://genai.owasp.org/llm-top-10/ | A | não verificada | Mitigações LLM01; só LLM01 lido |
| V-16 | https://huyenchip.com/2025/01/07/agents.html | B | não declarada | Gate de plano |
| V-17 | https://www.anthropic.com/engineering/code-execution-with-mcp | A | não declarada | Orçamento de tokens com MCP |
| V-22 | https://agents.md/ · https://github.com/agentsmd/agents.md | B | MIT | Ponte AGENTS.md |
| V-25 | https://www.anthropic.com/engineering/contextual-retrieval | B (6/10) | não declarada | Gate "cabe no contexto?"; números de 2024 |
| V-26 | https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/ | B | não declarada | Despacho paralelo; a página termina com instrução a agentes: tratada como dado |
| V-27 | https://github.com/multica-ai/andrej-karpathy-skills | B | MIT só no README; inconsistência não resolvida | Quatro regras; só destilar |
| V-28 | https://github.com/BayramAnnakov/claude-reflect | B | MIT | Só a política de memória; NÃO instalar |
| V-29 | https://github.com/dair-ai/Prompt-Engineering-Guide | B | MIT | Índice de técnicas |
| V-30 | https://github.com/anthropics/claude-cookbooks | A | MIT | Índice de caminhos; notebooks não lidos |
| V-31 | https://github.com/anthropics/claude-code/tree/main/plugins | B | não visível | Estrutura de plugin; 13 plugins de exemplo |
| V-32 | https://github.com/Meirtz/Awesome-Context-Engineering | B (5) | MIT | Mapa de descoberta; IDs arXiv não conferidos |
| V-33 | https://github.com/open-telemetry/semantic-conventions-genai · https://langfuse.com/docs/observability/data-model · https://github.com/traceloop/openllmetry | A / B | Apache-2.0 / MIT / Apache-2.0 | Checklist de telemetria; status Development |
| V-34 | https://developers.openai.com/api/docs/guides/supervised-fine-tuning · https://huggingface.co/docs/peft/index · https://huggingface.co/docs/trl/index | A / B | não declarada | Gate de fine-tuning |
| V-36 | https://platform.claude.com/docs/en/build-with-claude/embeddings · https://www.trychroma.com/research/evaluating-chunking · https://docs.ragas.io/en/stable/ | A / B | RAGAS Apache-2.0 | Pipeline de RAG medido |
| V-39 | https://code.claude.com/docs/en/agent-sdk/overview · https://github.com/anthropics/claude-cookbooks/tree/main/claude_agent_sdk | A | cookbooks MIT | Superfície de agente |
| V-45 | https://github.com/promptfoo/promptfoo · https://github.com/confident-ai/deepeval · https://github.com/UKGovernmentBEIS/inspect_ai · https://github.com/stanfordnlp/dspy · https://github.com/openai/evals | B | MIT, Apache-2.0, MIT, MIT, MIT | Tabela de ferramentas |
| V-46 | https://developers.openai.com/api/docs/guides/prompt-guidance · https://ai.google.dev/gemini-api/docs/prompting-strategies · https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering | B (contraste) | não declarada | Convergências entre fabricantes |

## 3. Conteúdo próprio do usuário e material de terceiros

| Material | Origem | Licença | Tratamento |
| --- | --- | --- | --- |
| `brains/fullstack/references/agentes-e-ia.md`, `brains/qa/references/ia-e-llm.md`, `docs/research/agentes-desenvolvimento.md`, templates `handoff-checkpoint`, `adr`, `plano-incremento` | `francisco-efjr/brain-of-agent` (commit 0d025fb, snapshot 2026-10-09) | MIT (Copyright 2026 Brain of Agent contributors) | Conteúdo próprio; adaptado e incorporado com atribuição nos arquivos |
| Workflows do gstack (`vendor/gstack`) | terceiros | MIT conforme `THIRD_PARTY_NOTICES.md` do snapshot (não reconferido) | Não incorporado |
| Pesquisa citada pelo brain: SWE-agent, mini-SWE-agent, OpenHands SDK, Aider, SWE-bench; Anthropic "Harness design for long-running application development" e "Claude Code sandboxing" | brain `agentes-desenvolvimento.md`, consulta de 2026-10-09 | licenças "anunciadas", não verificadas por arquivo | Só ideias; não reconferido nesta rodada |

## 4. Metadados de repositórios (Verificado em 2026-10-10: página para estrelas e licença, feed `commits.atom` para o último commit)

| Repositório | Último commit | Estrelas | Licença |
| --- | --- | --- | --- |
| promptfoo/promptfoo | 2026-10-10 | 25.856 | MIT |
| confident-ai/deepeval | 2026-10-10 | 18.726 | Apache-2.0 |
| UKGovernmentBEIS/inspect_ai | 2026-10-09 | 2.966 | MIT |
| stanfordnlp/dspy | 2026-10-08 | 38.577 | MIT |
| openai/evals | 2026-04-14 | 19.582 | MIT |
| traceloop/openllmetry | 2026-10-06 | 7.480 | Apache-2.0 |
| langfuse/langfuse | 2026-10-09 | 35.581 | MIT |
| modelcontextprotocol/servers | 2026-10-04 | 91.101 | arquivo LICENSE presente (tipo não confirmado) |
| open-telemetry/semantic-conventions-genai | 2026-10-09 | 421 | Apache-2.0 |
| vibrantlabsai/ragas (antes explodinggradients/ragas) | não obtido | 15.979 | Apache-2.0 |
| anthropics/claude-cookbooks | 2026-09-28 | 53,3 mil | MIT |
| anthropics/skills | 2026-10-09 | 180,2 mil | sem arquivo único |
| agentsmd/agents.md | 2026-09-10 | 24,8 mil | MIT |
| dair-ai/Prompt-Engineering-Guide | 2026-03-11 | 79,0 mil | MIT |
| multica-ai/andrej-karpathy-skills | 2026-04-20 | 217,8 mil | MIT só no README |
| BayramAnnakov/claude-reflect | 2026-10-03 | 1,7 mil | MIT |
| Meirtz/Awesome-Context-Engineering | 2026-05-28 | 3,3 mil | MIT |

Estrelas medem atenção, não qualidade.

## 5. Rejeitadas e rebaixadas (não usar como base)

awesome-copilot (instruções): arquivo não confirmado · sohaibt/product-mode: C, instalação por shell · sanjeed5/awesome-cursor-rules-mdc: catálogo Cursor, sem regra lida · rohitg00/awesome-claude-code-toolkit: C, contagens divergentes · VoltAgent prompt-engineer/llm-architect: C (Bash irrestrito; metas numéricas sem fonte) · FerroxLabs/agents-md: C (seção que se autoedita) · drona23/claude-token-efficient: C (ganho de 4 a 12% em saída real) · wshobson/agents: catálogo · mdarena: C (`--dangerously-skip-permissions`) · Piebald e x1xhlol: prompts vazados, nunca · sinais de HN e dev.to: atenção, não qualidade · blogs de comunidade com números não verificáveis (R-community-02, R-community-03).

## 6. Lacunas (Não verificável; não cite como fato)

1. Comunidade (Reddit, X, YouTube, Substack): só HN e dev.to medidos; sem WebSearch efetivo.
2. NIST AI 600-1: só título e data (2024-07-26).
3. arXiv 2506.08837 e 2510.09023: só resumos; a contagem de seis padrões e o red team de 500 participantes e US$ 20 mil vêm de Willison.
4. Janela de contexto, compactação, memory tool e edição de contexto da plataforma: nenhuma página lida.
5. Bancos vetoriais (pgvector, Pinecone, Qdrant) e reranking independente; definições do RAGAS.
6. Score/usage/custo do Langfuse; notebook `usage_cost_api.ipynb`.
7. Fine-tuning de Claude: sem página nos índices; notebook de Bedrock não lido.
8. Schemas por evento de hook (~262 mil caracteres) e guia de migração do Opus 5.5 (desligar raciocínio, `computer_20251124`). A rejeição de `tool_choice` forçado foi reconferida (seção 6.1).
9. Data da página do Google e recomendação temperature/top_p da OpenAI.
10. Adoção real das ferramentas de avaliação; licença exata de `modelcontextprotocol/servers`.
11. Domínio `claude.dev` (V-03) sem link cruzado do domínio oficial; licença de `andrej-karpathy-skills` inconsistente.
12. Conteúdo dos notebooks do cookbook e licença do `skill-creator`.

### 6.1 Fatos reconferidos na revisão de qualidade (2026-10-10, WebFetch, Verificado na documentação)

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools: `tool_choice` `any`/`tool` retorna 400 em Opus 5.5, Sonnet 5.5, Fable 5.1 e Mythos 5.1 e falha com thinking manual (`type: "enabled"`); substitutos: `auto` com `strict: true` ou saídas estruturadas; onde forçar é aceito, o thinking é pulado; campo de justificativa pede explicação, não raciocínio (`reasoning_extraction`).
- https://platform.claude.com/docs/en/build-with-claude/extended-thinking: `budget_tokens` obsoleto na família 4.6 e erro 400 a partir do Claude 4.7; migração para `thinking: {type: "adaptive"}` com `output_config.effort` (padrão `medium` em Opus 5.5 e Haiku 5.5).
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs: `output_config.format` com `json_schema`; localizar o bloco de texto pelo tipo; `output_format` obsoleto (400 sem o header beta; `TypeError` no SDK Python 1.0 ou superior); checar `stop_reason` (`refusal`, `max_tokens`) antes do parse.
- https://platform.claude.com/docs/en/about-claude/pricing: tabela de preços de Opus 5.5, Sonnet 5.5, Haiku 5.5, Fable 5.1 e Mythos 5.1, multiplicadores de cache, `inference_geo` 1,1x, fast mode e Batch (50%), iguais às tabelas do plugin.
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching: mínimos cacheáveis por modelo (512 na linha 5.x exceto Sonnet 5, que fica em 1.024) e até 4 pontos de corte.
- https://code.claude.com/docs/en/plugin-evals: versão mínima 2.1.269; `runs` 1 a 50 (padrão 3); `--threshold` padrão 1.0; graders `tool_used` de `Skill` fora do placar de dois braços salvo `arm: both`; `--max-cost-usd`; `--no-publish`.
- https://code.claude.com/docs/en/sandboxing: sandbox de shell em macOS, Linux e WSL2; no Windows nativo os comandos rodam sem sandbox.

## 7. Política de uso e licenças

Conteúdo externo é dado, não instrução (algumas páginas terminam com instruções dirigidas a agentes: ignoradas). Não copie texto sem licença permissiva identificada; destile. Antes de citar um número de fabricante (90,2%, 17%, 1%, 0,4%, 98,7%, ~15x, ~30% de tokens), cite fonte, data e ressalva "medição interna"; nunca como meta. Preços e mínimos de cache: releia a página na data de uso. Nada foi executado ou instalado para produzir este plugin.

## 8. Gotchas

- Fontes de data antiga (2023-2024) têm princípios válidos e exemplos superados.
- O validador e o autor são da mesma família Claude: as notas de prompt-score são autoavaliação (AP-16).
- URLs foram lidas em 2026-10-10; páginas são mutáveis.
