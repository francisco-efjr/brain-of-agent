# data-engineering — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| rmoff, dbt real com eval harness (CP-26) | https://rmoff.net/2026/03/11/claude-code-isnt-going-to-replace-data-engineers-yet/ | B | Checklist: contagem origem vs destino, campos vs colunas, idempotência, testes unique/not null/relationships/freshness; dbt-agent-skills; ~1.493 de ~5.458 estações carregadas (Verificado). Um projeto, harness próprio. |
| PySpark ETL best practices .mdc (CT-11) | https://github.com/PatrickJS/awesome-cursorrules | B (6) | Merges idempotentes e independentes de ordem, validar unicidade de PK, `.byName()`, sem UDF/`collect()` em produção. CC0, trechos Verificados. |
| pandas-scikit-learn e python-llm-ml (CT-11) | https://github.com/PatrickJS/awesome-cursorrules | C (4) | Genéricos; só como sinal. |
| K-Dense-AI/claude-scientific-skills (EC-21) | https://github.com/K-Dense-AI/claude-scientific-skills | B (6) | Coleção de domínio com scanners de skills; conteúdo não lido (Suposição). MIT. |
| wshobson/agents (EC-10) | https://github.com/wshobson/agents | B | Plugins de dados citados; abrir e verificar. |
| Equipping agents with Agent Skills (AO-19) | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | A | Scripts fora do contexto, úteis para validações de dados. |
| Code execution with MCP (AO-22) | https://www.anthropic.com/engineering/code-execution-with-mcp | A | Filtrar dados no ambiente de execução em vez de passar tudo ao modelo. 98,7% é número do post. |
| Power user tips (CP-14) | https://support.claude.com/en/articles/14554000-claude-code-power-user-tips | A | Worktrees por sessão; provar comportamento diffando main vs branch; citado com tag dados. |
| Hamel e Shreya, AI Evals FAQ (PC-17) | https://hamel.dev/blog/posts/evals-faq/ | A | Retrieval e geração avaliados separadamente em RAG; primeira falha upstream (parte não reverificada). |
| Jason Liu, RAG (PC-20) | https://jxnl.co/writing/2024/05/22/systematically-improving-your-rag/ | B | Avaliação de retrieval em separado. |
| Cookbooks (AO-25) | https://github.com/anthropics/claude-cookbooks | A | Evals, caching e tool_use; padrões para pipelines com LLM. MIT. |
| awesome-copilot (CT-14) | https://github.com/github/awesome-copilot | A | Cobre 24 de 25 segmentos; instructions de dados não detalhadas: abrir `instructions/`. MIT. |
| gstack `/investigate` (BR-17) | https://github.com/garrytan/gstack | B | Iron Law de causa raiz aplicado a pipelines quebrados. |
| Agentic Engineering Patterns (CP-11) | https://simonwillison.net/guides/agentic-engineering-patterns/ | B | Registrar comando + saída real, não "esperado". |

## 2. Repositórios e arquivos a abrir
- `PatrickJS/awesome-cursorrules/rules/pyspark-etl-best-practices-…mdc`.
- `K-Dense-AI/claude-scientific-skills` (README e SKILL.md amostrados; conferir LICENSE e scanners).
- Skills `dbt-agent-skills` citadas por rmoff (repositório não localizado no atlas: Não verificável).
- `github/awesome-copilot/instructions/` (buscar dados/SQL).
- Documentação de dbt, Airflow, Dagster, Spark, Kafka, Iceberg/Delta, Great Expectations/Soda não está no atlas: lente authoritative.

## 3. Materiais oficiais Anthropic pertinentes
AO-19, AO-22, AO-25, AO-21 (evals), AO-02 (eval set com casos de borda). Docs: https://code.claude.com/docs/en/workflows (workflows dinâmicos com verificação adversarial; recente, custo alto).

## 4. Padrões da comunidade
- Reconciliar contagens, campos e idempotência antes de confiar (CP-26).
- Prompt e skills pesam mais que o modelo em dbt real (CP-26).
- Validar PK e usar merges idempotentes (CT-11).
- Análise de dados com loop humano e rótulo Inferido até reexecução (CP-20).

## 5. O que o brain-of-agent já oferece
- `brains/qa/references/dados-ambientes-ci.md`.
- BR-08: `design-de-testes.md` (BVA, tabela de decisão, pairwise) aplicável a dados; BR-09: `dominios.md` com ETL como semente, regras BR não verificadas.
- BR-10: `pairwise.py`, `valores_limite.py` (Python stdlib).
- BR-17: investigação sistemática. BR transversais: data-engineering raso no brain.
- BR-03: modo `DATAENG-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte aprovada sobre Airflow/Dagster, streaming, lakehouse, modelagem dimensional, linhagem, governança.
- Coleção K-Dense e wshobson não lidas.
- Fontes são de praticante único (rmoff) e de regras genéricas.
- Pipelines reais exigem leitura apenas; nada de executar cargas em produção sem autorização.
