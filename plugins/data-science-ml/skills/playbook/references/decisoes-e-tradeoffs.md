# Decisões e trade-offs em ciência de dados e ML

Validado em 2026-10-10. Cada seção é uma árvore de decisão curta: condição, escolha, porquê, e o custo da escolha. Números são pontos de partida (V-nn = `fontes.md`). Onde a fonte é fraca, está dito.

## Sumário
1. Pipeline fixo vs agente aberto
2. Código vs juiz LLM
3. Métrica por tipo de problema
4. Desbalanceamento: pesos, reamostragem, calibração
5. Encoders por cardinalidade
6. Busca de hiperparâmetros
7. Método causal pelo mecanismo de atribuição
8. Holm/Bonferroni vs Benjamini–Hochberg
9. ML vs heurística
10. Stages vs aliases no registro
11. Onde colocar a regra (hook, CLAUDE.md, skill)
12. Quantos exemplos para validar um juiz
13. Um juiz forte vs painel
14. Reprodutibilidade exata vs tolerância

## 1. Pipeline fixo vs agente aberto (V-07, V-34)
| Tarefa | Escolha | Porquê |
| --- | --- | --- |
| Repetível, formato fixo (relatório semanal, treino com etapas, ETL) | Pipeline com checagem entre etapas | Previsível, depurável, barato |
| Aberta (investigar queda de métrica) | Agente com ferramentas somente leitura, limite de passos e revisão humana antes de escrever | Agentes vão mal em análise aberta sem guia (relato de Dan Luu, Não verificável de forma independente) |
| Incerto | Uma chamada única com exemplos antes de orquestrar | "Comece pela solução mais simples" (Anthropic, 2024-12-19; a própria página avisa que o ferramental mudou) |
Custo: pipeline perde flexibilidade; agente perde previsibilidade e custa mais tokens.

## 2. Código vs juiz LLM (V-01, V-05)
1. Existe regra determinística (JSON válido, igualdade, regex, schema, registro existente)? Use asserção em código.
2. A falha é subjetiva e persistente após as asserções? Um juiz LLM binário com crítica, **um por modo de falha**.
3. Impacto alto ou juiz não validado? Humano por amostragem.
Custo: código não captura nuance; juiz exige validação (seção 12) e rótulos de especialista.

## 3. Métrica por tipo de problema (V-16)
| Problema | Métrica principal | Notas |
| --- | --- | --- |
| Classificação balanceada | ROC-AUC ou acurácia | Sempre com baseline |
| Classe rara | PR-AUC, F1/F-beta, recall com precisão fixa, recall@k | ROC-AUC junto, não no lugar; acurácia é taxa-base |
| Probabilidade usada como tal | Log loss, Brier, curva de calibração | Calibrador em dados independentes do treino do classificador |
| Ranking | NDCG, MAP | Métricas de ranking/recomendação: cobertura fraca neste plugin (lacuna) |
| Regressão | MAE, RMSE, RMSLE | MAPE é fraco perto de zero (use MASE em séries, RMSLE conforme o caso) |
| Série temporal | MASE, erro por horizonte, cobertura do intervalo | Baseline sazonal-naive |
O custo do erro desempata: se um falso negativo custa 10 vezes um falso positivo, escolha a métrica e o limiar por esse custo.

## 4. Desbalanceamento (V-17)
Ordem: **métrica → pesos de classe → reamostragem dentro do fold → limiar na curva PR de validação.**
- Precisa de probabilidade calibrada? Evite reponderar; ou calibre depois com dados independentes. Para XGBoost com AUC como objetivo, `scale_pos_weight` balanceia; se probabilidades acuradas importam, não rebalanceie e use `max_delta_step` finito (doc do XGBoost, Verificado).
- Reamostragem só no treino de cada fold (`imblearn.pipeline.Pipeline`); nunca no teste.
- Categóricas: `SMOTENC` ou pesos, não `SMOTE`.
- Se nenhum limiar atinge a precisão-alvo, relate isso; não caia silenciosamente em 0,5.
Custo: pesos podem distorcer a probabilidade; reamostragem aumenta tempo e risco de vazamento se mal posicionada.

## 5. Encoders por cardinalidade (V-18)
| Situação | Escolha | Cuidado |
| --- | --- | --- |
| Baixa cardinalidade (≤ ~15: ponto de partida) | One-hot | Modelos de árvore podem aceitar ordinal |
| Alta cardinalidade | Target encoding com suavização, ou frequência | Prior global e médias dentro do fold; cross-fitting em vez de LOO |
| Hora, mês, ângulo | Codificação cíclica (seno/cosseno) | Declare o período |
| Valores assimétricos ≥ 0 | `log1p` | Box-Cox exige estritamente positivos |
O código de target encoding de terceiros costuma não ser transformador do sklearn: defina como será aplicado em teste e produção antes de dizer que cabe em `Pipeline`. Fonte classe C; confira na doc de encoders da versão instalada (Não verificado).

## 6. Busca de hiperparâmetros (V-21)
| Condição | Escolha |
| --- | --- |
| Poucos parâmetros, treino barato | Grid |
| Muitos parâmetros | Random |
| Modelo caro | Optuna/TPE; poda exige `trial.report()` e `trial.should_prune()` durante o treino |
Regras: Pipeline inteiro na CV; escala log para taxa de aprendizado e regularização; espaço largo e depois estreito; `n_estimators` por early stopping em validação separada; seeds no sampler e no splitter; `n_trials` e `timeout` limitados; 3 a 5 parâmetros; mesma CV com e sem tuning; teste uma vez. LightGBM: `num_leaves` abaixo de `2^max_depth`, `min_data_in_leaf` como guarda contra overfitting. XGBoost: `max_depth`, `min_child_weight`, `gamma`, `subsample`, `eta`. CatBoost não foi pesquisado. Não prometa percentual de ganho com tuning (a afirmação "5 a 15%" foi removida por falta de fonte).

## 7. Método causal pelo mecanismo de atribuição (V-28; fonte classe C + abstract do DoWhy)
| Como o tratamento foi atribuído | Método | Premissa a checar |
| --- | --- | --- |
| Randomizado | Diferença de médias | Integridade da randomização (SRM) |
| Limiar em variável de corrida | RDD | Teste de manipulação antes de estimar |
| Data única de adoção | DiD e event study | Tendências paralelas; ausência de antecipação |
| Datas variáveis | Decomposição de Bacon; estimadores robustos (Callaway-Sant'Anna, Sun-Abraham) | Heterogeneidade temporal |
| Uma unidade tratada | Controle sintético | Ajuste pré-tratamento; inferência por permutação |
| Instrumento | IV (efeito local) | Força da primeira etapa; exclusão |
| Observáveis ricos | Matching, IPW, DML | Sobreposição; não controlar colisores |
| Nenhum dos anteriores | Linguagem associativa | — |
Agrupe o erro-padrão no nível da atribuição; poucos clusters tornam o erro robusto instável. Sempre ao menos uma refutação ou sensibilidade (placebo, DoWhy: Model, Identify, Estimate, Refute). Lacuna: Hernán & Robins, EconML e a doc do DoWhy não foram lidos.

## 8. Holm/Bonferroni vs Benjamini–Hochberg (V-26 com correção do validador)
- **Família confirmatória** (decide lançar): Holm ou Bonferroni (controle de FWER).
- **Triagem exploratória**: BH (controle de FDR), rotulando os achados como exploratórios.
- Sempre conte a família: métricas × variantes × segmentos × olhadas. Vinte testes independentes a 5% dão cerca de 64% de chance de ao menos um falso positivo (1 − 0,95^20).

## 9. ML vs heurística (V-31)
Comece com uma heurística como baseline e lance sem ML se bastar. Use ML quando a heurística mede pior no custo do erro e existe dado rotulado confiável. Antes: métrica definida, infraestrutura testada independentemente do modelo, corte temporal no teste (Regra 33 do guia do Google). Custo: o modelo traz dívida técnica (dependências de dados e de configuração, laços de realimentação, consumidores não declarados; Sculley et al., 2015).

## 10. Stages vs aliases no registro (V-22)
Prefira **versão + alias** (`models:/<nome>@<alias>`). A página de registry do MLflow ainda cita transição por stages no trecho OSS e não declara stages obsoletos; **não afirme obsolescência**. Exigência de assinatura (`set_signature`) é do Unity Catalog, não do OSS. Confira `mlflow --version` e a doc da versão.

## 11. Onde colocar a regra (V-09, V-10)
1. **Deve valer sempre?** Hook (`PreToolUse`) ou permissão `deny`: garantia, não pedido.
2. **Fato universal e curto que o agente não deduz?** `CLAUDE.md` (bloco de dados com ~40 linhas ou menos; teste de remoção).
3. **Procedimento ocasional?** Skill.
4. **Revisão com contexto novo?** Subagente somente leitura.
5. **Acesso a sistema externo?** MCP (desativado por padrão; ver `ferramentas-e-mcp.md`).
Regra nova só depois da segunda ocorrência do mesmo erro.

## 12. Quantos exemplos para validar um juiz (V-04, V-05)
Etapas distintas, não conflitantes: 30 a 50 exemplos de **cada rótulo** em dev e teste para validar o juiz; 100 a 200 por modo de falha para sustentar o juiz de um modo específico; 50 aprovados e 50 reprovados ao depurar. Declare a escolha e o custo de rotulagem.

## 13. Um juiz forte vs painel (V-06)
Comece com **um juiz binário por modo de falha, validado**. Painel de juízes menores só se a validação falhar e houver orçamento; as magnitudes dos estudos citados são de modelos antigos e não devem ser usadas.

## 14. Reprodutibilidade exata vs tolerância (V-20)
Critério de aceite: reexecutar com a mesma configuração reproduz a métrica **dentro de tolerância declarada**. Seeds e `use_deterministic_algorithms(True)` reduzem a variação, mas o PyTorch não garante resultados idênticos entre versões, commits, plataformas ou CPU/GPU. `torch.manual_seed` cobre CPU e CUDA; `random` e NumPy precisam de seed própria.
