---
name: serie-kfold-embaralhado
description: Caso de disparo e de fidelidade técnica. Mede se o plugin reprova validação KFold embaralhada e janela centrada em previsão de vendas, propõe origem rolante com horizonte da decisão, baseline sazonal-naive, MASE e erro por horizonte e se recusa a validar o MAPE de 3 por cento.
tags: [data-science-ml, ds-time-series-backtest, time-series, backtest, leakage]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Marca KFold com shuffle e a janela rolling centrada como bloqueadores de vazamento temporal, propõe origem rolante ou TimeSeriesSplit alinhada ao horizonte de 14 dias com treino só no passado, baseline sazonal-naive, MASE em vez de MAPE e erro por horizonte, e não valida o MAPE de 3 por cento nem libera produção."
model: sonnet
---
Fiz um modelo de previsão de vendas diárias por loja (120 lojas, 3 anos de histórico) para a reposição de estoque, que decide quanto pedir com 14 dias de antecedência. O MAPE na validação cruzada deu 3%, muito melhor que os 11% do método atual da planilha. Posso colocar em produção na segunda?

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.ensemble import GradientBoostingRegressor

df = pd.read_csv("vendas_diarias.csv", parse_dates=["data"])  # colunas: loja, data, vendas, promocao, feriado
df = df.sort_values(["loja", "data"])

df["media_7d"] = df.groupby("loja")["vendas"].transform(lambda s: s.rolling(7, center=True).mean())
df["lag_1"] = df.groupby("loja")["vendas"].shift(1)
df["dow"] = df["data"].dt.dayofweek
df = df.dropna()

X = df[["media_7d", "lag_1", "dow", "promocao", "feriado"]]
y = df["vendas"]

mapes = []
for tr, te in KFold(n_splits=5, shuffle=True, random_state=0).split(X):
    m = GradientBoostingRegressor(random_state=0).fit(X.iloc[tr], y.iloc[tr])
    p = m.predict(X.iloc[te])
    mapes.append(np.mean(np.abs((y.iloc[te] - p) / y.iloc[te])))
print(np.mean(mapes))  # 0.03
```

Algumas lojas têm dias com venda zero (fechadas). Não consigo rodar nada agora; me diga o que o código permite concluir e o que eu precisaria refazer antes de decidir.
