# EDA, métricas, desbalanceamento, features e figuras

Validado em 2026-10-10. Fontes: V-15, V-16, V-17, V-18, V-29, V-32, V-34 (ver `fontes.md`). Fontes de EDA e de feature engineering são classe C/B cruzadas; sem fonte oficial de EDA. Números (15 categorias, |corr| > 0,95) são pontos de partida.

## Sumário
1. EDA em 7 passos com saída fixa
2. Comando de EDA pronto
3. Tabela problema → métrica
4. Média e dispersão entre dobras
5. Desbalanceamento em 4 passos
6. Limiar na curva precisão–recall
7. Calibração
8. Análise de erros por fatia
9. Encoders e target encoding
10. Checklist de figura

## 1. EDA em 7 passos (só no conjunto de treino)

Passo 0, antes de tudo: confirme o escopo e a raiz aprovada, a política de PII, e **separe o hold-out** (por grupo ou por tempo quando couber). Nunca decida nada olhando o hold-out. Nunca altere `data/raw/`.

| # | Passo | O que produzir | Armadilha |
| --- | --- | --- | --- |
| 1 | Forma e tipos | Linhas × colunas, dtype, memória, chave (grão) | Data lida como texto; ID numérico tratado como feature |
| 2 | Ausentes e padrão | % de ausentes por coluna; separar **ausente**, **não detectado** e **zero verdadeiro**; ausência correlacionada com o alvo? | `fillna(0)` global esconde o padrão |
| 3 | Alvo e balanceamento | Distribuição do alvo, prevalência, ao longo do tempo | Prevalência muda com o tempo |
| 4 | Univariada | Média e DP **junto de** mediana e IQR; cauda | Só média em dado assimétrico |
| 5 | Bivariada com o alvo | Médias por grupo, informação mútua, `.corr()` só para relações lineares entre numéricas | `.corr()` não captura relação não linear nem categórica |
| 6 | Varredura de vazamento | IDs, timestamps, colunas posteriores ao desfecho, features quase perfeitas | Coluna de status final como feature |
| 7 | Cardinalidade e outliers | Níveis por categórica; outliers listados | **Nunca imputar ou excluir outlier automaticamente**; registre a decisão e quem a tomou |

Regras: IDs não são features. Rotule achados post hoc como **exploratórios**. |corr| > 0,95 entre features é heurística para investigar colinearidade, não regra. Números só de código executado; se não executou, entregue o plano e marque "a medir".

**Saída fixa** (modelo `assets/templates/relatorio-eda.md`): forma e tipos · ausentes e padrão · alvo e balanceamento · relação com o alvo · suspeitas de vazamento · features candidatas · premissas · o que não foi verificado. Gráficos em `reports/figuras/` somente se o usuário autorizar execução.

## 2. Comando de EDA pronto (para `.claude/commands/eda.md` do projeto)

```markdown
Dataset em $ARGUMENTS (caminho e coluna-alvo). Rode a EDA só no conjunto de treino; separe o hold-out antes, por grupo ou por tempo se houver. Mostre forma, tipos, ausentes (separando ausente, não detectado e zero verdadeiro), distribuição do alvo, relação de cada feature com o alvo e uma lista de suspeitas de vazamento (IDs, timestamps, colunas posteriores ao desfecho). Não altere os dados de origem; salve gráficos em reports/figuras/; liste as premissas e o que não foi verificado. Antes de executar qualquer código, peça confirmação.
```

## 3. Tabela problema → métrica (V-16)

| Problema | Principal | Complementos |
| --- | --- | --- |
| Classificação balanceada | ROC-AUC ou acurácia | Matriz de confusão, baseline |
| Classe rara | PR-AUC, F1/F-beta, recall com precisão fixa, recall@k | ROC-AUC junto (não "inadequada", só insuficiente sozinha) |
| Probabilidade usada como tal | Log loss, Brier | Curva de calibração |
| Ranking | NDCG, MAP | (cobertura fraca no plugin) |
| Regressão | MAE, RMSE, RMSLE | Resíduos por faixa; MAPE só longe de zero |
| Série temporal | MASE, erro por horizonte | Cobertura do intervalo |
Sempre inclua **baseline** (heurística ou `Dummy*`) nas mesmas dobras. O custo do erro decide a métrica.

## 4. Média e dispersão entre dobras

Reporte média e desvio entre dobras e diga explicitamente que o **desvio entre dobras não é intervalo de confiança** (as dobras compartilham dados de treino). Para comparar dois modelos, use as mesmas dobras e examine a diferença por dobra; um IC próprio exige método apropriado (por exemplo, bootstrap sobre o conjunto de validação independente), declarado.

## 5. Desbalanceamento em 4 passos (V-17)

1. **Métrica**: PR-AUC, recall com precisão fixa, F-beta.
2. **Pesos de classe** (`class_weight`, `scale_pos_weight`) antes de reamostrar.
3. **Reamostragem apenas dentro do treino de cada fold** (`imblearn.pipeline.Pipeline`); nunca no teste. SMOTE em categóricas: `SMOTENC` ou pesos.
4. **Limiar** escolhido na curva precisão–recall **da validação**, conforme o custo.
Se probabilidade calibrada importa, evite reponderar ou calibre depois com dados independentes. XGBoost: com AUC como objetivo, `scale_pos_weight` balanceia; se importam probabilidades acuradas, não rebalanceie e use `max_delta_step` finito (doc do XGBoost, Verificado).

## 6. Limiar na curva precisão–recall

```python
from sklearn.metrics import precision_recall_curve

prec, rec, thr = precision_recall_curve(y_val, p_val)   # prec/rec têm 1 elemento a mais que thr
ok = prec[:-1] >= 0.90                                    # precisão-alvo vinda do custo do erro
if not ok.any():
    raise RuntimeError("Nenhum limiar atinge a precisão-alvo; relatar e rediscutir a meta.")
threshold = thr[ok][rec[:-1][ok].argmax()]                # maior recall que mantém a precisão-alvo
```
O trecho de terceiros (V-17) voltava em silêncio a 0,5 quando nenhum limiar atingia a meta: trate o caso explicitamente. Limiar 0,5 pode ser ótimo se o modelo for calibrado; "quase sempre errado" é exagero.

## 7. Calibração

- O calibrador deve ser ajustado em dados **independentes** do treino do classificador (Verificado na página de calibração do sklearn). Na API atual isso se faz com validação cruzada interna do `CalibratedClassifierCV` ou, para estimador já treinado, com o envoltório `FrozenEstimator` (Inferido; conferir na doc da sua versão, porque a API de `cv="prefit"` mudou).
- Meça com log loss, Brier e curva de calibração; reporte por fatia relevante.
- Pesos e oversampling distorcem probabilidades: recalibre depois.

## 8. Análise de erros por fatia (Inferido de V-05, V-32, V-34)

1. Defina as fatias **antes** de ver o resultado (segmento, faixa de valor, período); fatias escolhidas depois são exploratórias.
2. Para cada fatia: n, métrica e intervalo; fatia pequena sem intervalo não se interpreta.
3. Matriz de confusão por classe crítica.
4. Leia 20 a 50 exemplos mal classificados (ponto de partida) e agrupe por causa **antes** de propor features.

## 9. Encoders e target encoding (V-18, fonte classe C: confirme na doc de encoders)

- A escolha depende do modelo e da cardinalidade; 15 níveis é ponto de partida, não regra. Árvores aceitam ordinal; modelos lineares pedem one-hot ou frequência.
- **Target encoding** sempre fora do fold, com suavização (`(n·média_cat + m·prior)/(n + m)`); o **prior global também dentro do fold**.
- Leave-one-out é propenso a vazamento por construção; prefira **cross-fitting** (a média de cada dobra vem das outras dobras).
- `log1p` exige valores ≥ 0; Box-Cox exige valores estritamente positivos.
- Hora, mês e ângulo: codificação cíclica (seno e cosseno) com o período declarado.
- Agregações temporais só com o passado.
- Código de target encoding de terceiros costuma não ser transformador sklearn (sem `fit`/`transform`): não diga que cabe em `Pipeline` sem implementá-lo assim, e defina como será aplicado em teste e produção.

## 10. Checklist de figura (V-29)

- [ ] Eixos com unidade e transformação (log, padronização) declaradas.
- [ ] Base zero em barras, ou aviso de truncamento.
- [ ] Incerteza visível (intervalo), com **n** e a unidade de replicação.
- [ ] Ausente ≠ zero (marque dado faltante).
- [ ] Cor com redundância (marcadores, estilos de linha ou rótulos diretos) e contraste verificado.
- [ ] Texto alternativo ou tabela de dados anexa.
- [ ] Tamanho, DPI, formato e fontes do arquivo **exportado** inspecionados.
- [ ] Dados brutos e código de transformação preservados; nunca alterar dados para melhorar a aparência.
- [ ] Binning, normalização e exclusões explicitados.
Um relatório automático de figura não certifica rigor, acessibilidade nem aceitação editorial. Dashboards como aplicação web ficam em `web-frontend`; acessibilidade web em `web-frontend` ou `ux-ui-design`.
