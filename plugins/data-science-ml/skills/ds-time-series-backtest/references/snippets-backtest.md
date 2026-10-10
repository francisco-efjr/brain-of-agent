# Snippets de backtest temporal

Validado em 2026-10-10. Redação própria; conceitos de FPP3 (origem rolante, erro por horizonte; V-14) e `TimeSeriesSplit` do scikit-learn (V-12). Não executados (Não verificado): rode no ambiente do projeto. `forecast_fn` é uma função do projeto que recebe o histórico até a origem e devolve H previsões.

## Sumário
1. Origem rolante manual (expanding ou sliding)
2. `TimeSeriesSplit` com `gap` e `test_size`
3. Baseline sazonal-naive e MASE
4. Erro e cobertura por horizonte
5. Dados point-in-time com `merge_asof`
6. Padrões que usam o futuro

## 1. Origem rolante manual

```python
import numpy as np
import pandas as pd

def rolling_origins(n, min_train, horizon, step, window=None):
    """Gera (train_idx, test_idx). window=None: janela crescente; window=int: deslizante."""
    origin = min_train
    while origin + horizon <= n:
        start = 0 if window is None else max(0, origin - window)
        yield np.arange(start, origin), np.arange(origin, origin + horizon)
        origin += step

y = df["vendas"].to_numpy()          # série ordenada por tempo, sem NaN no treino
H, M = 14, 7                         # horizonte da decisão e período sazonal
preds, actuals = [], []
for tr, te in rolling_origins(len(y), min_train=730, horizon=H, step=7):
    yhat = forecast_fn(y[tr], H)                  # só histórico até a origem
    preds.append(yhat); actuals.append(y[te])
P, A = np.vstack(preds), np.vstack(actuals)       # (n_origens, H)
```

Painel (várias séries): aplique por série ou use datas de corte comuns (`cut_dates`) e filtre `df[df.date < cut]` para treino e `df[(df.date >= cut) & (df.date < cut + horizon)]` para teste, nunca embaralhando linhas.

## 2. `TimeSeriesSplit` com `gap` e `test_size`

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=8, test_size=14, gap=1)    # gap = atraso do rótulo; max_train_size=... para janela deslizante
for tr, te in tscv.split(X):                                # X ordenado por tempo, uma linha por passo
    ...
```

`TimeSeriesSplit` gera treinos crescentes e não aceita `shuffle`. Parâmetros `test_size`, `gap` e `max_train_size` existem nas versões recentes (confira a instalada). Linhas igualmente espaçadas são premissa.

## 3. Baseline sazonal-naive e MASE

```python
def seasonal_naive(train, horizon, m):
    """Repete a última estação de comprimento m ao longo do horizonte."""
    return np.resize(train[-m:], horizon)

def mase(y_true, y_pred, y_train, m=1):
    """Escala pelo erro absoluto médio do naive sazonal DENTRO da amostra de treino."""
    scale = np.mean(np.abs(y_train[m:] - y_train[:-m]))
    return np.mean(np.abs(y_true - y_pred)) / scale

base_P = np.vstack([seasonal_naive(y[tr], H, M) for tr, _ in rolling_origins(len(y), 730, H, 7)])
mase_model = np.mean([mase(A[i], P[i], y[tr], M) for i, (tr, _) in enumerate(rolling_origins(len(y), 730, H, 7))])
mase_base  = np.mean([mase(A[i], base_P[i], y[tr], M) for i, (tr, _) in enumerate(rolling_origins(len(y), 730, H, 7))])
print(round(mase_model, 3), round(mase_base, 3))   # < 1 melhor que o naive sazonal dentro da amostra
```

`np.resize` repete o vetor cíclico: com `horizon > m` a previsão repete a estação. Em séries sem sazonalidade use `m=1` (naive simples). Se a escala for zero (série constante), o MASE é indefinido: reporte MAE.

## 4. Erro e cobertura por horizonte

```python
mae_h = np.abs(A - P).mean(axis=0)               # (H,): erro por passo à frente
print(pd.Series(mae_h, index=range(1, H + 1)).round(3))

# intervalos: LO, HI com forma (n_origens, H), de forecast_fn
cover_h = ((A >= LO) & (A <= HI)).mean(axis=0)   # cobertura empírica por horizonte
width_h = (HI - LO).mean(axis=0)
```

Cobertura nominal 80% com empírica claramente menor indica incerteza subestimada. Reporte também a dispersão do erro entre origens (percentis), não só a média.

## 5. Dados point-in-time com `merge_asof`

```python
decisions = decisions.sort_values("decision_ts")
feat = feat.sort_values("known_at")          # quando o valor ficou disponível, não quando se refere

X = pd.merge_asof(decisions, feat, left_on="decision_ts", right_on="known_at",
                  by="entity_id", direction="backward", allow_exact_matches=True)
```

`direction="backward"` pega o último valor conhecido até a decisão. O que importa é `known_at` (disponibilidade), não a data de referência do valor: um valor de janeiro publicado em março só existe a partir de março. Um `tolerance=pd.Timedelta("7D")` evita usar um valor velho demais como se fosse atual.

## 6. Padrões que usam o futuro

```python
# errado: usa 3 passos do futuro
df["m7_errado"] = df["y"].rolling(7, center=True).mean()
# errado: preenche com o valor seguinte
df["y_filled_errado"] = df["y"].bfill()
# errado: ajuste na série inteira
mean_all, std_all = df["y"].mean(), df["y"].std()

# certo: só passado até t-1
df["m7"] = df["y"].shift(1).rolling(7).mean()
df["lag_7"] = df["y"].shift(7)
# certo: estatísticas de escala ajustadas por origem, só no treino da origem
mu, sd = y[tr].mean(), y[tr].std()
```

Decomposição sazonal, STL e suavizações ajustadas sobre a série inteira também usam o futuro: ajuste dentro de cada origem. Calendário (dia da semana, feriados oficiais) é conhecido de antemão e não vaza.
