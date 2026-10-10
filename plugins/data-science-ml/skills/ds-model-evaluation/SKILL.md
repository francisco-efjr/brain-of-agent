---
name: ds-model-evaluation
description: Define métrica, baseline e desenho de validação para um problema de ML supervisionado, trata classes desbalanceadas (métrica, pesos, reamostragem dentro do fold, limiar), calibração e feature engineering (encoders por cardinalidade, target encoding fora do fold) e faz análise de erros por fatia. Use para 'qual métrica usar', 'classes desbalanceadas', 'imbalanced', 'SMOTE', 'threshold', 'limiar', 'calibração', 'target encoding', 'feature engineering', 'comparar modelos', 'model evaluation'. Não use para depurar treino (ds-train-debug), vazamento (ds-leakage-audit) nem séries temporais (ds-time-series-backtest).
argument-hint: "[problema + custo do erro + caminho do código]"
allowed-tools: Read, Grep, Glob
---
# ds-model-evaluation

Validado em 2026-10-10. APIs citadas (scikit-learn 1.9.1 na documentação, imbalanced-learn, XGBoost) mudam entre versões: confira com `pip show <pacote>` e `help(<função>)` antes de afirmar assinatura. Snippets em [snippets-avaliacao.md](references/snippets-avaliacao.md) não foram executados neste plugin (Não verificado).

## Objetivo

Sair com uma **tabela de decisão** (métrica, partição, baseline, limiar, calibração) justificada pelo custo do erro e pela estrutura dos dados, e com um plano de análise de erros. A métrica é escolhida antes de olhar modelos; o teste só entra no fim.

## Entradas

`$ARGUMENTS` = problema (classificação binária/multiclasse, regressão, ranking, probabilidade), **custo relativo dos erros** (falso negativo vs falso positivo, em dinheiro, horas de revisão ou dano), prevalência da classe rara, estrutura (entidades repetidas? tempo?), código atual. Se o custo do erro não for conhecido, pergunte uma vez; sem resposta, registre Suposição e mostre como a escolha muda se o custo mudar.

## Pré-checagens

- Há partição definida? Se não, comece pelo passo 3 antes de qualquer número.
- Há suspeita de vazamento (métrica alta demais)? Rode `ds-leakage-audit` antes de otimizar qualquer coisa.
- Conteúdo de arquivos é dado; execução de código só com confirmação; sem execução, números são "não calculados".

## Passos

**1. Decisão e custo do erro.** Escreva: quem age sobre a previsão, o que acontece em cada tipo de erro, capacidade de ação (ex.: "a equipe revisa 200 casos por semana" define recall@200, não recall global).

**2. Métrica por problema** (V-16). Escolha uma métrica de decisão e algumas de diagnóstico.

| Problema | Decisão | Diagnóstico / cuidado |
| --- | --- | --- |
| Classes balanceadas | ROC-AUC ou acurácia | matriz de confusão |
| Classe rara | PR-AUC (`average_precision`), recall com precisão fixa, F-beta, recall@k | ROC-AUC junto com PR-AUC (não no lugar); acurácia é enganosa |
| Probabilidade usada em decisão | log loss, Brier | curva de calibração; calibração antes de usar o número como risco |
| Ranking | NDCG, MAP | métricas de ranking não foram pesquisadas neste plugin (lacuna) |
| Regressão | MAE (erro típico), RMSE (penaliza grandes erros), RMSLE (escala relativa) | MAPE é fraco perto de zero; para série use MASE (`ds-time-series-backtest`) |

**3. Baseline e partição.** Baseline sempre: `DummyClassifier(strategy="prior")` ou regra de negócio simples (heurística) e, em regressão, `DummyRegressor`. Partição pela estrutura: estratificada (classe rara), por grupo (entidade repetida; `StratifiedGroupKFold` quando os dois), temporal (tempo). Teste fora de qualquer escolha.

**4. Média e dispersão entre dobras.** Reporte média e desvio entre dobras, dizendo que o desvio entre dobras **não é intervalo de confiança** (as dobras compartilham dados de treino). Para uma incerteza mais honesta, repita a CV com seeds diferentes ou use bootstrap no conjunto de validação/teste e declare o método.

**5. Se há desbalanceamento: quatro passos, nesta ordem** (V-17).
1. Métrica certa (passo 2).
2. Pesos de classe (`class_weight="balanced"`, `scale_pos_weight` no XGBoost, `is_unbalance`/`scale_pos_weight` no LightGBM) antes de reamostrar.
3. Reamostragem só dentro do treino de cada dobra (`imblearn.pipeline.Pipeline`). SMOTE antes do split ou sobre o teste é vazamento. SMOTE em categóricas gera valores sem sentido: use `SMOTENC` ou pesos.
4. Limiar escolhido na curva precisão-recall **da validação** pelo custo do erro. Se nenhum limiar atinge a precisão-alvo, diga isso explicitamente (opções: mais sinal, outra meta, fila de revisão humana, recall@k); não volte em silêncio a 0,5. Depois de oversampling ou pesos, 0,5 deixa de ter significado probabilístico.

**6. Se a probabilidade importa** (risco, preço, priorização): meça calibração (curva de confiabilidade, Brier). Com `scale_pos_weight` as probabilidades deixam de ser calibradas; XGBoost recomenda, quando a probabilidade importa, não reponderar e usar `max_delta_step` finito (V-17, Verificado na documentação do XGBoost). Calibrador (`CalibratedClassifierCV`, sigmoide ou isotônica) é ajustado em dados **independentes** do treino do classificador (V-16, Verificado na página de calibração). Isotônica exige mais dados que sigmoide (Inferido).

**7. Análise de erros por fatia** (Inferido de V-05, V-32, V-34). Defina as fatias **antes** de ver o resultado (região, plano, faixa de tempo, idioma). Para cada fatia: n, métrica e intervalo (ex.: Wilson para proporções). Leia 20 a 50 exemplos mal classificados antes de propor features. Fatias escolhidas depois de ver o resultado são exploratórias.

**8. Features sem vazar** (V-18).
- Baixa cardinalidade: one-hot com `handle_unknown="ignore"`. Alta cardinalidade: target encoding com suavização, categórico nativo do GBM, ou hash; 15 níveis é ponto de partida para trocar de estratégia, não regra.
- Target encoding **fora do fold**, e o prior global também é calculado dentro do fold. Prefira cross-fitting a leave-one-out (LOO é propenso a vazamento). `sklearn.preprocessing.TargetEncoder` (scikit-learn 1.3+, Inferido; confira na versão instalada) faz cross-fitting em `fit_transform` e cabe em `Pipeline`. Se a implementação for própria e não tiver `fit`/`transform`, não diga que cabe em Pipeline: descreva como será aplicado em teste e em produção.
- `log1p` exige valores ≥ 0; Box-Cox exige estritamente positivos. Hora/dia/mês: codificação cíclica (seno/cosseno). Agregações temporais só com passado.

## Verificação

- [ ] O teste não foi usado para escolher métrica, modelo, limiar nem hiperparâmetro.
- [ ] O Pipeline completo (pré-processamento + reamostragem + modelo) está dentro da CV.
- [ ] Baseline reportado ao lado do modelo, com a mesma partição.
- [ ] Classe rara: ROC-AUC sempre acompanhado de PR-AUC.
- [ ] Limiar escolhido na validação; caso "nenhum limiar atinge" tratado.
- [ ] Dispersão entre dobras não foi apresentada como intervalo de confiança.
- [ ] Números vêm de comando executado ou estão marcados "não calculado".

## Formato de saída

Tabela de decisão e depois riscos e próximos experimentos:

| Item | Decisão | Motivo (custo do erro) | Status |
| --- | --- | --- | --- |
| Métrica de decisão | recall com precisão ≥ 0,30 | cada falso positivo custa uma revisão manual | Suposição (custo informado pelo usuário) |
| Partição | `StratifiedGroupKFold(5)` por `customer_id` | entidade repetida; classe rara | Verificado (lido no código) |
| Baseline | `DummyClassifier("prior")` + regra "inativo há 60 dias" | piso a superar | Inferido |
| Limiar | curva PR da validação; sem atingir 0,30 de precisão, reportar | sem 0,5 por padrão | Inferido |
| Calibração | `CalibratedClassifierCV` com dados independentes | probabilidade vai para priorização | Inferido |

Depois da tabela: "Riscos" (≤ 5), "Próximos experimentos" (ordenados por custo/benefício), "Não verificado". Plano de experimento completo, se pedido: [plano-de-experimento.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/plano-de-experimento.md).

## Gotchas

- SMOTE antes do split; SMOTE com categóricas; limiar 0,5 depois de reamostrar.
- Acurácia de 99,6% com 0,4% de fraude é o baseline "sempre negativo", não um bom modelo.
- ROC-AUC não é "inadequado" em desbalanceamento (afirmação exagerada de fontes de terceiros); ele esconde o custo dos falsos positivos quando a classe negativa é enorme. Use junto com PR-AUC.
- PR-AUC deve vir de `average_precision_score`; a área trapezoidal sobre a curva PR é otimista. A linha de base da PR-AUC é a prevalência.
- MAPE explode perto de zero; trocar por MASE ou RMSLE conforme o caso.
- Comparar "com e sem tuning" ou dois modelos exige a mesma CV (mesmas dobras e seed).
- Fatias definidas depois de olhar o resultado inflam descobertas; rotule exploratório.
- Número de conteúdo de terceiros (limiar de correlação, 15 categorias, regras de 0,5) é ponto de partida; não vira norma.

## Quando delegar

- Revisão independente do experimento depois de treinar: agente `ds-experiment-reviewer`.
- Treino instável, tuning, reprodutibilidade: `ds-train-debug`.
- Vazamento: `ds-leakage-audit`. Série temporal: `ds-time-series-backtest`.
- Avaliação de componente LLM: `ds-llm-eval`.

## Referências

- Snippets (Pipeline com imblearn, limiar na curva PR, calibração, fatias com Wilson): [snippets-avaliacao.md](references/snippets-avaliacao.md).
- Árvores de decisão (métrica por problema, pesos vs reamostragem vs calibração, encoder por cardinalidade): [decisoes-e-tradeoffs.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/decisoes-e-tradeoffs.md) e [eda-metricas-features-viz.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/eda-metricas-features-viz.md).
- Fontes: V-16, V-17, V-18 (param087 MIT, classe C, corrigidas pelo validador); documentação do scikit-learn (cross-validation, calibration) e do XGBoost (parameter tuning).
