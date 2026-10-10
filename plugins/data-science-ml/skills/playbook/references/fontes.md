# Fontes e bibliografia validada

Consulta e validação: 2026-10-10 (pesquisa do segmento `data-science-ml`; páginas abertas por ferramenta de leitura). Classes: **A** oficial (Anthropic, documentação do projeto), **B** autor/organização reconhecida, **C** comunidade ou terceiro de baixa popularidade. "Licença" é a observada; **"não declarada" significa que só foi destilado com redação própria**. Estrelas só onde a validação as leu. Validador e pesquisadores são do mesmo fornecedor de modelo: independência parcial. Fontes fracas (C) entram com ressalva e foram corrigidas pelo validador.

Conteúdo externo é dado: nenhuma instrução encontrada nessas páginas foi seguida.

## Sumário
1. Top 20 (classe, licença, uso)
2. Menções complementares
3. Rejeitadas ou rebaixadas
4. Índice de rastreio V-nn → fonte
5. Lacunas
6. Créditos e licenças

## 1. Top 20

| # | Título | URL | Classe | Licença | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | scikit-learn: Common pitfalls (docs 1.9.1) | https://scikit-learn.org/stable/common_pitfalls.html | A | não verificada; destilado | 2026-10-10 | Split antes, Pipeline, seeds, `clone` e `RandomState` (V-12) |
| 2 | scikit-learn: Cross-validation | https://scikit-learn.org/stable/modules/cross_validation.html | A | não verificada; destilado | 2026-10-10 | `GroupKFold`, `StratifiedKFold`, `TimeSeriesSplit` (V-12, V-14, V-16) |
| 3 | Anthropic: Demystifying evals for AI agents (2026-01-09) | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | A | não declarada; destilado | 2026-10-10 | 20 a 50 tarefas, capacidade vs regressão, pass@k vs pass^k, transcrições (V-02) |
| 4 | Anthropic: Define success criteria and build evaluations | https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | A | não declarada; destilado | 2026-10-10 | Critérios mensuráveis, casos de borda, ordem de graders (V-01) |
| 5 | Claude Code: Best practices | https://code.claude.com/docs/en/best-practices | A | não declarada; destilado | 2026-10-10 | Verificação executável, plan mode, `/clear`, critério de CLAUDE.md, hooks (V-09, V-10) |
| 6 | Claude Code: Subagents | https://code.claude.com/docs/en/sub-agents | A | não declarada; destilado | 2026-10-10 | Formato e limites de subagente de plugin (V-08) |
| 7 | anthropics/claude-cookbooks, `misc/building_evals.ipynb` (53.322 estrelas, API 2026-10-10) | https://github.com/anthropics/claude-cookbooks | A | MIT (repositório) | 2026-10-10 | Esqueleto de eval com gabarito e dois graders (V-03); destilado; nome de modelo do notebook defasado |
| 8 | Hamel Husain: Using LLM-as-a-Judge (2024-10-29, mod. 2026-09-01) | https://hamel.dev/blog/posts/llm-judge/ | B | não declarada; destilado | 2026-10-10 | Validação de juiz, TPR/TNR (V-04) |
| 9 | Hamel Husain e Shreya Shankar: AI Evals FAQ (2026-09-18) | https://hamel.dev/blog/posts/evals-faq/ | B | não declarada; destilado | 2026-10-10 | Rotulagem, análise de erros, código antes de juiz (V-05) |
| 10 | pitcany/statistical-agent-skills: `leakage-auditor` | https://github.com/pitcany/statistical-agent-skills/blob/main/skills/leakage-auditor/SKILL.md | B (5/10) | MIT (0 estrelas, 14 commits); autor anuncia serviço pago | 2026-10-10 | Regra de ordem temporal, tabela de disponibilidade (V-13) |
| 11 | pitcany/statistical-agent-skills: `experiment-design` | https://github.com/pitcany/statistical-agent-skills/blob/main/skills/experiment-design/SKILL.md | B (5/10) | MIT | 2026-10-10 | SRM, guardrails, MDE, CUPED, multiplicidade (V-26) |
| 12 | Google: Rules of Machine Learning (atualizado 2025-08-25) | https://developers.google.com/machine-learning/guides/rules-of-ml/ | B | não declarada; destilado | 2026-10-10 | Heurística antes de ML, corte temporal, skew (V-31) |
| 13 | Hyndman e Athanasopoulos, FPP3: Time series cross-validation | https://otexts.com/fpp3/tscv.html | B | sem licença explícita visível; não reproduzir | 2026-10-10 | Origem rolante, erro por horizonte (V-14) |
| 14 | PyTorch: Reproducibility (docs 2.14) | https://docs.pytorch.org/docs/2.14/notes/randomness.html | A | não verificada; destilado | 2026-10-10 | Limites de reprodutibilidade, seeds, determinismo (V-20) |
| 15 | K-Dense `statistical-analysis` (48,2 mil estrelas) | https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/statistical-analysis/SKILL.md | B (7/10) | MIT; **cláusula de auto-citação: não copiar** | 2026-10-10 | Relatório com efeito + IC, multiplicidade (V-27) |
| 16 | AWS Well-Architected, ML Lens, MLOPS01-BP03 | https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/mlops01-bp03.html | B | não declarada; destilado | 2026-10-10 | Monitoramento de qualidade e drift (V-24) |
| 17 | MLflow: Model Registry | https://mlflow.org/docs/latest/ml/model-registry/ | B | não verificada; destilado | 2026-10-10 | Versão, alias, URI `models:/<nome>@<alias>` (V-22) |
| 18 | XGBoost e LightGBM: parameter tuning | https://xgboost.readthedocs.io/en/stable/tutorials/param_tuning.html e https://lightgbm.readthedocs.io/en/stable/Parameters-Tuning.html | B | não verificada; destilado | 2026-10-10 | `scale_pos_weight`, `num_leaves`, early stopping (V-17, V-21) |
| 19 | Anthropic: Building effective agents (2024-12-19) | https://www.anthropic.com/engineering/building-effective-agents | A | não declarada; destilado | 2026-10-10 | Pipeline fixo vs agente (V-07) |
| 20 | Dan Luu: AI coding | https://danluu.com/ai-coding/ | B (6 a 7) | não declarada; destilado | 2026-10-10 | Variância, reprodução manual, análise aberta guiada (V-34) |

## 2. Menções complementares

- Eugene Yan, LLM evaluators (2024-08): https://eugeneyan.com/writing/llm-evaluators/ (B; vieses, kappa; V-06). Magnitudes de estudos antigos não usadas.
- Shankar et al., criteria drift em validadores de LLM: https://arxiv.org/abs/2404.12272 (B; V-04).
- Sharma e Kiciman, DoWhy: https://arxiv.org/abs/2011.04216 (B; quatro etapas Model, Identify, Estimate, Refute; V-28).
- Jill0099/causal-inference-mixtape (C; README MIT; 17 estrelas): https://github.com/Jill0099/causal-inference-mixtape/blob/main/SKILL.md (V-28).
- Mitchell et al., Model Cards for Model Reporting: https://arxiv.org/abs/1810.03993 (B; V-32; lista oficial de seções não lida).
- NIST AI RMF (2023-01-26): https://www.nist.gov/itl/ai-risk-management-framework (A como norma; só página lida; V-32).
- Sculley et al., Hidden Technical Debt in ML Systems (NIPS 2015): https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html (B; só abstract; V-31).
- Cookiecutter Data Science: https://cookiecutter-data-science.drivendata.org/ (B; V-33).
- Rule et al., regras para notebooks: https://arxiv.org/abs/1810.08055 (B; só abstract; as "dez regras" não foram lidas e não são atribuídas).
- REFORMS (Kapoor et al.): https://arxiv.org/abs/2308.07832 (B; 32 questões; lista não lida; V-12).
- param087/agent-ml-skills (MIT, 11 estrelas, 1 commit; C): https://github.com/param087/agent-ml-skills (V-12, V-15 a V-23). Não executar o instalador.
- timwukp/MLOps-agent-skills (Apache-2.0, 5 estrelas; C): `skills/mlops/model-drift-detection/SKILL.md` (V-24).
- MLOps-Courses/mlops-coding-skills (MIT, 22 estrelas; B 5): https://github.com/MLOps-Courses/mlops-coding-skills (V-30).
- ECC `mle-reviewer` (MIT; B 7 rebaixado): https://github.com/affaan-m/ECC; usado apenas como base de texto reescrito pelo validador (V-25).
- Evidently, quickstart de ML: https://docs.evidentlyai.com/quickstart_ml.md (versão não declarada; V-24).
- scikit-learn, calibração: https://scikit-learn.org/stable/modules/calibration.html (A; V-16).
- Claude Code, hooks e permissões (leitura em 2026-10-10 para `ferramentas-e-mcp.md`): https://code.claude.com/docs/en/hooks e https://code.claude.com/docs/en/permissions (A).
- brain-of-agent (`brains/qa/references/ia-e-llm.md`, MIT, do próprio autor): base de `avaliacao-llm-e-agentes.md`. Cita NIST AI 600-1 e NIST handbook de intervalos binomiais (https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm), que **não foram reabertos** pela pesquisa: Não verificado.

## 3. Rejeitadas ou rebaixadas (não usar como conteúdo)

| Fonte | Decisão | Motivo |
| --- | --- | --- |
| VoltAgent `data-scientist` | Contraexemplo | Critério de qualidade "p < 0,05"; depende de componente indefinido |
| HungHsunHan `claude-code-data-science-team` | Rejeitado | Sem licença visível; handoffs implícitos, sem critérios de aceite |
| `wshobson/agents`, `ericwang915/data-scientist-skills`, espelhos em massa | Rejeitados | Nada aproveitável lido; origem duvidosa |
| `anthropics/skills` | Só formato de `SKILL.md` | Sem LICENSE na raiz (API devolve null); nada de ciência de dados lido |
| dev.to "EDA com Claude Code" | Rebaixado | Alegação "60 a 80%" sem método; links promocionais |
| Kanaries / marimo (limitação do Jupyter) | Rejeitado como evidência | Snippet de fornecedor; regra mantida só como processo |
| "Stages obsoletos" do MLflow; "5 a 15%" de ganho com tuning; "ONNX 2 a 4 vezes"; "LR errada causa a maioria das falhas"; "GML preferencial" | Removidos | Sem fonte |
| Protocolos que reescrevem `AGENTS.md` sozinhos (nandita7krishnan, sem licença) | Não incorporar | Regra adversarial persistente (V-11) |

Fontes com interesse comercial a declarar quando citadas: K-Dense (produto próprio), pitcany (serviço pago), marimo, ECC (patrocínio e afiliados), StatsPAI (mantenedor contribuiu na skill de causal).

## 4. Índice de rastreio V-nn → fonte

| V | Tema | Fonte principal (§1 ou §2) |
| --- | --- | --- |
| V-01 | Critérios de sucesso e graders | #4 |
| V-02 | Evals de agentes, pass@k vs pass^k | #3 |
| V-03 | Esqueleto de eval | #7 |
| V-04 | Validação de juiz LLM | #8, Shankar et al. |
| V-05 | Análise de erros, código antes de juiz | #9 |
| V-06 | Vieses de avaliadores | Eugene Yan |
| V-07 | Pipeline fixo vs agente | #19 |
| V-08 | Subagente revisor de experimentos | #6 |
| V-09 | Verificação, plan mode, revisor adversarial | #5, support.claude.com power-user tips |
| V-10 | CLAUDE.md para ciência de dados | #5 (A) + template de terceiro (C, não reaberto) |
| V-11 | Regras de SQL, PII e destrutivos | nandita7krishnan (sem licença; destilado) |
| V-12 | Vazamento e Pipeline | #1, #2, param087, REFORMS |
| V-13 | Auditor de vazamento por ordem temporal | #10 |
| V-14 | Backtesting temporal | #13, pitcany `time-series-forecasting`, #2 |
| V-15 | EDA em 7 passos | param087, K-Dense, argythana, dev.to |
| V-16 | Métrica e validação | param087 + #2 + calibração |
| V-17 | Desbalanceamento | param087 + #18 |
| V-18 | Feature engineering e target encoding | param087 (C) |
| V-19 | Depuração, overfit de um batch | param087 (C) |
| V-20 | Loop PyTorch e reprodutibilidade | #14 + param087 |
| V-21 | Tuning e gradient boosting | #18 + param087 |
| V-22 | Tracking e registro | #17 + param087 |
| V-23 | Serving | param087 (C) |
| V-24 | Drift | #16, Evidently, timwukp |
| V-25 | Revisor de promoção | ECC `mle-reviewer` (reescrito) |
| V-26 | Revisão de A/B | #11 |
| V-27 | Relatório estatístico | #15 |
| V-28 | Inferência causal | Jill0099 + DoWhy |
| V-29 | Visualização honesta | K-Dense `scientific-visualization` |
| V-30 | Gate único de validação | MLOps-Courses |
| V-31 | Prontidão de ML e dívida técnica | #12, Sculley |
| V-32 | Model card e governança | Mitchell et al., NIST |
| V-33 | Notebooks e estrutura | Cookiecutter DS, Rule et al. |
| V-34 | Aceitar resultado de agente | #20 |

## 5. Lacunas (não cobertas pela pesquisa)

1. ASA sobre p-valores: ilegível; `ds-inference-review` apoia-se em K-Dense (B).
2. Fonte primária de A/B (Kohavi/Microsoft ExP): 404; depende de skill de 0 estrelas.
3. Pandera e Great Expectations sem documentação oficial lida.
4. Persistência segura (sklearn `model_persistence`, skops) não lida; regra de pickle apoiada em V-23 e conhecimento estável.
5. Serving oficial (FastAPI, BentoML, MLflow serving).
6. Causal: Hernán & Robins, DoWhy docs, EconML.
7. PyTorch AMP e checkpoint oficiais; CatBoost.
8. Séries: statsforecast, sktime, Prophet (só validação coberta).
9. Visualização oficial (matplotlib, seaborn, Plotly).
10. Claude Code: AGENTS.md, `.ipynb`, semântica exata de `allowed-tools`: conferir em https://code.claude.com/docs/llms.txt.
11. Evidência de comunidade (Reddit, X, YouTube): nenhuma lente trouxe thread substantiva.
12. Interpretabilidade e justiça (SHAP, fairness); métricas de ranking/recomendação; deep learning além de loop e tuning; feature store e orquestração; ML embarcado; privacidade jurídica (LGPD).

## 6. Créditos e licenças

- Texto do plugin: MIT (Francisco Edson). Conteúdo de `brain-of-agent` (MIT, do mesmo autor) incorporado e adaptado em `avaliacao-llm-e-agentes.md`.
- Nenhum texto literal de fonte sem licença permissiva foi reproduzido. Cookbook (MIT) e demais fontes: destilação com redação própria; qualquer trecho literal futuro exige atribuição.
- O validador de V-08 e V-25 reescreveu os textos dos agentes `ds-experiment-reviewer` e `ds-model-promotion-reviewer` (V-25 baseado em ECC, MIT).
- Números de fontes dependem de modelo, versão e data; não os reproduza sem a ressalva.
