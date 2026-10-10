# Snippets de avaliação: baseline, CV, desbalanceamento, limiar, calibração, fatias

Validado em 2026-10-10. Redação própria. Não executados no plugin (Não verificado): rode no ambiente do projeto e cole saída e versões (`pip show scikit-learn imbalanced-learn`). Onde a API muda por versão, há comentário.

## Sumário
1. Baseline e CV com várias métricas
2. Pipeline completo com pré-processamento
3. Reamostragem dentro do fold
4. Limiar na curva precisão-recall
5. Calibração
6. Fatias com intervalo de Wilson
7. Target encoding sem vazar

## 1. Baseline e CV com várias métricas

```python
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate

SEED = 42  # importe de config.py no projeto
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
scoring = {"pr_auc": "average_precision", "roc_auc": "roc_auc", "neg_brier": "neg_brier_score"}

base = DummyClassifier(strategy="prior")          # prevalência como probabilidade
res = cross_validate(base, X_train, y_train, cv=cv, scoring=scoring)
for k in scoring:
    v = res[f"test_{k}"]
    print(k, round(v.mean(), 4), "+-", round(v.std(ddof=1), 4), "(desvio entre dobras, não é IC)")
```

Entidade repetida: troque por `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)` e passe `groups=` para `cross_validate`.

## 2. Pipeline completo com pré-processamento

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

prep = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
])
pipe = Pipeline([("prep", prep), ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))])
res = cross_validate(pipe, X_train, y_train, cv=cv, scoring=scoring)   # o Pipeline inteiro vai à CV
```

`class_weight="balanced"` é o passo 2 do desbalanceamento (pesos antes de reamostrar). Em GBM use `scale_pos_weight` (XGBoost/LightGBM) ou `class_weight` (API sklearn do LightGBM).

## 3. Reamostragem dentro do fold (apenas numéricas)

```python
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline   # NÃO o Pipeline do sklearn

pipe_smote = ImbPipeline([
    ("sc", StandardScaler()),
    ("smote", SMOTE(random_state=SEED)),     # só é aplicado no fit, nunca no predict/score
    ("clf", LogisticRegression(max_iter=1000)),
])
res = cross_validate(pipe_smote, X_train_num, y_train, cv=cv, scoring=scoring)
```

Regras: o teste/validação de cada dobra nunca é reamostrado; com colunas categóricas use pesos ou `SMOTENC` (que exige informar os índices das colunas categóricas e dados ainda não codificados em one-hot); depois de reamostrar, as probabilidades deixam de ser calibradas e 0,5 deixa de ter sentido.

## 4. Limiar na curva precisão-recall (da validação)

```python
from sklearn.metrics import precision_recall_curve

def pick_threshold(y_val, p_val, min_precision):
    """Maior recall com precisão >= min_precision. Retorna None se nenhum limiar atinge."""
    prec, rec, thr = precision_recall_curve(y_val, p_val)
    # prec e rec têm len(thr)+1 pontos; o último (precisão 1, recall 0) não tem limiar
    ok = np.where(prec[:-1] >= min_precision)[0]
    if ok.size == 0:
        return None            # sinalize no relatório; não caia em silêncio para 0,5
    best = ok[np.argmax(rec[:-1][ok])]
    return {"threshold": float(thr[best]), "precision": float(prec[best]), "recall": float(rec[best])}

pick = pick_threshold(y_val, p_val, min_precision=0.30)
print(pick or "Nenhum limiar atinge a precisão-alvo: discutir meta, sinal ou fila de revisão")
```

Para capacidade fixa (revisar K casos): `top = np.argsort(-p_val)[:K]; recall_at_k = y_val[top].sum() / y_val.sum()` (com `y_val` e `p_val` como arrays NumPy).

Aplique o limiar escolhido **uma vez** ao teste, sem reajustar.

## 5. Calibração

```python
from sklearn.calibration import CalibratedClassifierCV, CalibrationDisplay
from sklearn.metrics import brier_score_loss

# Calibrador em dados independentes do treino do classificador (CV interna faz isso por dobra).
# Parâmetro: estimator= (scikit-learn >= 1.2; antes: base_estimator=). Confira a versão.
cal = CalibratedClassifierCV(estimator=pipe, method="sigmoid", cv=5)   # "isotonic" com mais dados
cal.fit(X_train, y_train)
p_val = cal.predict_proba(X_val)[:, 1]
print("Brier:", brier_score_loss(y_val, p_val))
CalibrationDisplay.from_predictions(y_val, p_val, n_bins=10, strategy="quantile")   # curva de confiabilidade
```

Modelo já treinado e congelado: a documentação do scikit-learn removeu o caminho `cv="prefit"` em favor de `FrozenEstimator` (scikit-learn 1.6+, Inferido; confira na versão instalada). Em qualquer caso, use dados que o classificador não viu.

## 6. Fatias com intervalo de Wilson

```python
import pandas as pd
from statsmodels.stats.proportion import proportion_confint

def slice_report(df, slice_col, y_true, y_pred):
    rows = []
    for level, g in df.groupby(slice_col, observed=True):
        n = len(g)
        correct = int((g[y_true] == g[y_pred]).sum())
        lo, hi = proportion_confint(correct, n, alpha=0.05, method="wilson")
        rows.append({slice_col: level, "n": n, "acc": correct / n, "ic95_lo": lo, "ic95_hi": hi})
    return pd.DataFrame(rows).sort_values("n", ascending=False)
```

Acurácia por fatia serve para o formato; troque por recall/precisão da classe rara quando fizer sentido (proporção de positivos recuperados em cada fatia). Fatias com `n` pequeno têm intervalos largos: reporte-os, não os esconda. Defina as fatias antes de ver os resultados.

## 7. Target encoding sem vazar

```python
from sklearn.preprocessing import TargetEncoder   # scikit-learn >= 1.3 (confira)

prep_te = ColumnTransformer([
    ("te", TargetEncoder(target_type="binary", smooth="auto", cv=5, random_state=SEED), high_card_cols),
    ("num", StandardScaler(), num_cols),
])
```

No `fit_transform` (treino), o encoder usa cross-fitting interno; no `transform` (validação/teste/produção) usa a codificação ajustada no treino inteiro. Por isso ele deve ser chamado via Pipeline, nunca `fit` e depois `transform` no mesmo treino (isso reintroduz vazamento). Verifique a assinatura (`target_type`, `smooth`, `cv`) na versão instalada. Para implementação própria: prior calculado dentro do fold, suavização `(n * média_categoria + m * prior) / (n + m)`, cross-fitting em vez de leave-one-out.
