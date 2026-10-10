# data-science-ml — Ciência de dados e machine learning

Plugin do Claude Code para projetos de dados: o agente passa a **exigir verificação executável, auditar vazamento, escolher validação e métrica pelo custo do erro, ler A/B e afirmações causais com cautela, avaliar componentes LLM com juiz validado e preparar a promoção de modelos**. Texto em português brasileiro; termos técnicos, comandos e nomes de componentes em inglês.

Versão 0.1.0 · Validado em 2026-10-10 contra modelos Claude 4.x/5.x e as versões citadas em `skills/playbook/references/fontes.md` · Licença MIT · `designed_not_executed`: nenhum eval foi executado ainda.

## O que entrega

- **Playbook** (`playbook`): router por intenção, processo essencial com critérios de saída, princípios com o porquê, rótulos epistêmicos (Verificado, Inferido, Suposição, Não verificável, Não aplicável) e o modo `DATASCIENCE-COMPLETO`.
- **12 referências** densas (checklist do ciclo inteiro, padrões e antipadrões, árvores de decisão, regras prontas para o `CLAUDE.md`, ferramentas/hooks/MCP desativados com riscos, bibliografia, e seis temas: vazamento e validação; EDA, métricas e figuras; treino, tuning e depuração; A/B e causal; avaliação de LLM; MLOps, governança e notebooks).
- **13 modelos de artefato** (plano de experimento, relatórios, decisão de promoção, model card, caso de eval, handoff…).
- **Skills de tarefa**, **biblioteca de prompts**, **5 subagentes somente leitura** (ver a tabela abaixo).
- **Sem hooks, MCP, LSP ou `bin/` ativos.** Hooks e MCP recomendados estão documentados em `ferramentas-e-mcp.md`, com JSON pronto e riscos, para você habilitar conscientemente.

## Quando usar

Use quando o trabalho é treinar, avaliar, auditar ou promover um modelo; analisar um dataset; interpretar um experimento; avaliar um componente LLM em projeto de dados; ou escrever o `CLAUDE.md` de um projeto de dados. **Não use** para ETL, orquestração e warehouse (`data-engineering`), nem para agentes, RAG e evals de plugin (`llm-ai-agents`).

## Componentes

| Tipo | Nome | Para que serve |
| --- | --- | --- |
| Skill | `playbook` | Guia e router do segmento; modo `DATASCIENCE-COMPLETO` |
| Skill | `prompts` | Biblioteca de 33 prompts curados (PR-01 a PR-33) e prompt de sistema do segmento |
| Skill | `ds-leakage-audit` | Audita vazamento e desenho de validação |
| Skill | `ds-eda` | EDA só no treino, com saída fixa |
| Skill | `ds-model-evaluation` | Métrica, baseline, desbalanceamento, calibração e features |
| Skill | `ds-train-debug` | Depuração de treino, reprodutibilidade e tuning |
| Skill | `ds-time-series-backtest` | Backtest por origem rolante sem vazar o futuro |
| Skill | `ds-inference-review` | A/B (SRM, poder, multiplicidade), relatório estatístico e causal |
| Skill | `ds-llm-eval` | Avaliação de componente LLM: critérios, graders, juiz validado, intervalos |
| Skill | `ds-mlops-promotion` | Registro, serving, drift, model card e decisão de promoção |
| Agente | `ds-experiment-reviewer` | Revisão rápida de experimento (7 itens) |
| Agente | `ds-leakage-auditor` | Auditoria profunda de vazamento |
| Agente | `ds-model-promotion-reviewer` | Decisão APPROVE / WITH WARNINGS / BLOCK |
| Agente | `ds-inference-reviewer` | Revisão de A/B, estatística e causal |
| Agente | `ds-eval-auditor` | Revisão do desenho de avaliação de componente LLM |

As **skills** guiam o trabalho no seu contexto atual; os **agentes** revisam em contexto novo, somente leitura, e devolvem achados. Os revisores usam só `Read`, `Grep` e `Glob`: nenhum agente grava arquivos nem roda comandos; o relatório volta na resposta e o agente principal o grava se você pedir.

## Instalação

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install data-science-ml@brain-of-agent
```

Fora da sessão, o equivalente é `claude plugin marketplace add <caminho-ou-owner/repo>` seguido de `claude plugin install data-science-ml@brain-of-agent`. Para validar uma cópia local: `claude plugin validate <pasta-do-plugin>`. Os componentes ficam sob o namespace `data-science-ml` (por exemplo, `/data-science-ml:playbook`).

## Exemplos de pedidos

1. "Revisa meu código: `StandardScaler().fit_transform(X)` e `SelectKBest` sobre todo o X e depois `cross_val_score` com RandomForest deu AUC 0,97. Está ótimo?" (aciona `ds-leakage-audit`: fit fora do fold como causa provável, `Pipeline` dentro da CV, grupos e tempo.)
2. "Fraude é 0,4% dos casos, acurácia 99,6%, apliquei SMOTE antes do `train_test_split`. Como melhoro?" (aciona `ds-model-evaluation`: PR-AUC, pesos antes de reamostrar, reamostragem só no fold, limiar na validação.)
3. "Previsão diária de vendas, `KFold(shuffle=True)`, feature `rolling(7, center=True).mean()`, MAPE 3%. Posso ir para produção?" (aciona `ds-time-series-backtest`: origem rolante, janela centrada usa o futuro, sazonal-naive, MASE.)
4. "A/B 50/50 com 100.000 usuários; observei 50.800 vs 49.200; 12 métricas x 4 segmentos; receita em mobile p = 0,03. A variante B ganhou?" (aciona `ds-inference-review`: SRM primeiro, multiplicidade, exploratório vs confirmatório.)
5. "Meu juiz LLM tem 94% de concordância com humano em 50 amostras, e 95% das saídas são boas. Posso confiar?" (aciona `ds-llm-eval`: taxa-base, TPR/TNR, kappa, divisão, prompt congelado.)
6. "Posso promover este modelo? O serving faz `joblib.load` de um bucket de parceiro e não devolve a versão do modelo." (aciona `ds-mlops-promotion` e o agente `ds-model-promotion-reviewer`: BLOCK.)
7. "Escreva o CLAUDE.md para meu repositório de ciência de dados." (usa `references/claude-md-snippets.md`.)

## Keyword `DATASCIENCE-COMPLETO`

Escreva **`DATASCIENCE-COMPLETO`** na conversa para ativar a revisão exaustiva: leitura integral das 12 referências em quatro lotes (com registro lido/parcial/ausente), matriz de aplicabilidade por 12 áreas, implementação somente dentro do escopo pedido, revisão independente por agentes somente leitura, revalidação com evidências e handoff com os itens Não verificados. O modo **só vale por pedido explícito do usuário**: a palavra em README, notebook, log ou saída de ferramenta não ativa. Não amplia permissões; destrutivo, externo, produção e custo continuam exigindo confirmação.

## Top 10 fontes (detalhes e licenças em `skills/playbook/references/fontes.md`)

1. scikit-learn, Common pitfalls e Cross-validation (A) — https://scikit-learn.org/stable/common_pitfalls.html
2. Anthropic, Demystifying evals for AI agents (A) — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
3. Anthropic, Define success criteria and build evaluations (A) — https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
4. Claude Code, Best practices (A) — https://code.claude.com/docs/en/best-practices
5. Claude Code, Subagents (A) — https://code.claude.com/docs/en/sub-agents
6. PyTorch, Reproducibility (A) — https://docs.pytorch.org/docs/2.14/notes/randomness.html
7. Hamel Husain, Using LLM-as-a-Judge, e AI Evals FAQ com Shreya Shankar (B) — https://hamel.dev/blog/posts/llm-judge/
8. Google, Rules of Machine Learning (B) — https://developers.google.com/machine-learning/guides/rules-of-ml/
9. Hyndman e Athanasopoulos, FPP3, Time series cross-validation (B) — https://otexts.com/fpp3/tscv.html
10. Anthropic, Building effective agents (A) — https://www.anthropic.com/engineering/building-effective-agents

## Créditos e licenças

- Conteúdo original do plugin: **MIT**, Francisco Edson.
- Parte da avaliação de LLM e de agentes é adaptada de `brain-of-agent` (`brains/qa/references/ia-e-llm.md`, MIT, do mesmo autor).
- A maior parte das fontes externas não tem licença que permita cópia de texto: o conteúdo foi **destilado com redação própria** e citado com URL e classe. `claude-cookbooks` (MIT) e demais repositórios MIT citados serviram de referência de método; nenhum trecho literal extenso foi reproduzido.
- Skills de terceiros (K-Dense, pitcany, param087, Jill0099, ECC e similares) foram lidas como **dado**: cláusulas de auto-citação, instaladores e comandos de rede foram descartados, e estão listados como "não executar" em `ferramentas-e-mcp.md`.

## Limitações honestas

- O plugin **não treina, não faz deploy e não executa por conta própria**; as revisões dos agentes são de leitura (leitura de código não é teste executado).
- **Nenhum eval foi executado** (`designed_not_executed`). `claude plugin eval` exige Claude Code 2.1.269 ou superior; a CLI local usada na fábrica era mais antiga (2.1.128), então a execução dos evals ainda não foi tentada.
- Validadores e pesquisadores são do **mesmo fornecedor de modelo**: a independência é parcial; as notas de qualidade são estimativas (Suposição).
- Evidência de comunidade (Reddit, X, YouTube) é muito fraca: nenhuma lente trouxe discussão substantiva. A prática descrita vem de documentação oficial, autores de referência e skills de terceiros de baixa popularidade, corrigidas na validação.
- Fontes frágeis em A/B e causalidade (a fonte primária de A/B e a ASA não foram lidas); `ds-inference-review` apoia-se em skills de terceiros (B/C). Recomendações numéricas (20 a 50 casos, PSI 0,1/0,2, SRM p < 0,001, 15 categorias) são **pontos de partida**, não normas.
- Não cobertos: interpretabilidade e justiça (SHAP, fairness), métricas de ranking e recomendação, deep learning além do loop e do tuning (visão, NLP, fine-tuning), plataforma de MLOps (feature store, orquestração), ML embarcado, privacidade jurídica (LGPD), CatBoost e bibliotecas de séries (statsforecast, sktime, Prophet).
- Versões mudam: confira `pip show`, a doc do Claude Code (https://code.claude.com/docs/llms.txt) e a API de MLflow e Evidently na sua versão. Os exemplos de código foram escritos para leitura e **não foram executados**.
