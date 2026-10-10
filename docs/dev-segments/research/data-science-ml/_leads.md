# data-science-ml — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| Prompt engineering overview + define success criteria (AO-02) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | A | Critérios mensuráveis, eval set com casos de borda, grader por código/humano/LLM (modelo diferente do gerador). |
| Demystifying evals (AO-21) | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | A | pass@k × pass^k; 20 a 50 tarefas de falhas reais; calibrar juiz LLM com humanos. Verificado. |
| claude-cookbooks (AO-25) | https://github.com/anthropics/claude-cookbooks | A | `patterns/agents`, evals, tool_use, caching. MIT. Cursos e tutorial: só destilar. |
| Hamel Husain, LLM-as-a-Judge (PC-16) | https://hamel.dev/blog/posts/llm-judge/ | A | 7 passos: especialista principal, dataset diverso, pass/fail + crítica, judge validado contra especialista. Verificado. |
| Hamel e Shreya, AI Evals FAQ (PC-17) | https://hamel.dev/blog/posts/evals-faq/ | A | 60 a 80% do tempo em análise de erros; 100 a 200 exemplos rotulados; asserção em código antes de LLM-judge. |
| Shankar et al., Who Validates the Validators? (PC-18) | https://arxiv.org/abs/2404.12272 | A | Criteria drift; alinhar judges iterativamente. Não reverificado. |
| Eugene Yan, LLM evaluators (PC-15) | https://eugeneyan.com/writing/llm-evaluators/ | B | Vieses de judge (posição, verbosidade, autopreferência); binário. Não reverificado. |
| The Prompt Report (PC-12) | https://arxiv.org/abs/2406.06608 | A | Taxonomia; ≥3 execuções por variante (F1 varia até 0,04 entre execuções, Inferido). |
| Lost in the Middle e Prompt Formatting (PC-25) | https://arxiv.org/abs/2307.03172 | B | Posição da informação; formato muda desempenho até 40% em GPT-3.5. |
| DSPy, otimização automática (PC-30) | https://github.com/stanfordnlp/dspy | B | Otimização exige métrica e exemplos; MIT. |
| Gemini prompt design strategies (PC-06) | https://ai.google.dev/gemini-api/docs/prompting-strategies | A | Few-shot com estrutura idêntica; CC BY 4.0. Reasoning best practices da OpenAI (PC-04, zero-shot primeiro): https://developers.openai.com/api/docs/guides/reasoning-best-practices (não reverificado). |
| Dan Luu, AI coding (CP-20) | https://danluu.com/ai-coding/ | B | Repro falso veio do Codex, não do Claude (Verificado); variância alta entre execuções; avaliar com ≥3 execuções. |
| K-Dense scientific skills (EC-21) | https://github.com/K-Dense-AI/claude-scientific-skills | B | Coleção científica, não lida. MIT. |
| Power user tips (CP-14) | https://support.claude.com/en/articles/14554000-claude-code-power-user-tips | A | Tag data-science: `/loop`, worktrees, `/batch`. |
| pandas e python-llm-ml (CT-11) | https://github.com/PatrickJS/awesome-cursorrules | C (4) | Sem leakage/CV, sem eval/custo: só sinal. Calibração negativa. |
| Google ADK .mdc (CT-11) | https://github.com/PatrickJS/awesome-cursorrules | B | "Validate tool arguments before performing side effects." CC0. |
| Google whitepaper (PC-07) | https://www.kaggle.com/whitepaper-prompt-engineering | B | Ficha de documentação de experimento/prompt; cópia lida não oficial. |

## 2. Repositórios e arquivos a abrir
- `anthropics/claude-cookbooks` (evals, `patterns/agents`); `stanfordnlp/dspy` (README).
- `K-Dense-AI/claude-scientific-skills`; `wshobson/agents` (plugin de ML citado).
- `dair-ai/Prompt-Engineering-Guide` (MIT, 79,0k★) para taxonomia de técnicas.
- Documentação de scikit-learn, PyTorch, MLflow, métricas, vazamento de dados, inferência causal e séries temporais não está no atlas: lente authoritative.

## 3. Materiais oficiais Anthropic pertinentes
AO-02, AO-21, AO-25, AO-01 (documentação de experimentos), AO-06; para evals de agentes: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents. Think tool: superado por thinking adaptativo (Inferido, AO-17).

## 4. Padrões da comunidade
- Resultados de análise rotulados Inferido até reexecução; loop humano (CP-20).
- ≥3 execuções e distribuição em vez de uma execução (CP-20, CT-02 AAIF).
- Pipeline de dados reconciliado antes de modelar (CP-26).
- Seed e versões registradas no notebook: princípio Inferido, sem fonte no atlas.

## 5. O que o brain-of-agent já oferece
- `brains/qa/references/ia-e-llm.md` (testes de IA/LLM; próprio, MIT).
- BR-05: formato de evals `claude plugin eval` (`designed_not_executed`, caso negativo); BR-08: BVA e pairwise para casos de teste de dados; BR-10: scripts stdlib.
- BR-04: rótulos epistêmicos. BR transversais: data-science raso no brain.
- BR-03: modo `DATASCIENCE-COMPLETO`.

## 6. Lacunas e cuidados
- Atlas é forte em avaliação de LLM e fraco em ML clássico (EDA, leakage, CV, drift, MLOps): pesquisa própria obrigatória.
- Regras pandas/sklearn do atlas são genéricas.
- Vieses de avaliação com juiz do mesmo modelo: declarar não independente.
- Números de papers pré-thinking (CoT, ToT) são de modelos antigos.
