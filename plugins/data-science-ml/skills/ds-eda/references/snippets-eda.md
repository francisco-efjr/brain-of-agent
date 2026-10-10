# Snippets de EDA (pandas, NumPy, scikit-learn)

Validado em 2026-10-10. Redação própria. Os snippets não foram executados no plugin (Não verificado): rode-os num ambiente do projeto, com a seed de `config.py`, e cole a saída no relatório. Ajuste nomes de colunas; nada aqui instala pacotes nem toca `data/raw/`.

## Sumário
0. Partição
1. Forma e tipos
2. Ausentes
3. Alvo
4. Univariada
5. Bivariada
6. Varredura de vazamento
7. Cardinalidade e outliers
8. Salvar o relatório

## 0. Partição

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, train_test_split

SEED = 42  # no projeto, importe de config.py
TARGET, ENTITY, DATE = "churned", "customer_id", "signup_date"

df = pd.read_csv("data/raw/churn.csv", parse_dates=[DATE])  # leitura; nunca grave de volta em data/raw

# (a) decisão no futuro: corte por data (80% mais antigo = treino de EDA)
cut = df[DATE].quantile(0.8)
train, holdout = df[df[DATE] <= cut].copy(), df[df[DATE] > cut].copy()

# (b) entidade repetida: split por entidade
# gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEED)
# tr_idx, ho_idx = next(gss.split(df, groups=df[ENTITY]))
# train, holdout = df.iloc[tr_idx].copy(), df.iloc[ho_idx].copy()

# (c) i.i.d. sem entidade: estratificado
# train, holdout = train_test_split(df, test_size=0.2, stratify=df[TARGET], random_state=SEED)

print(len(train), len(holdout))
```

Dentro do corte por data, o holdout é o período mais recente; a EDA usa apenas `train`. Se o alvo só é conhecido após um atraso (ex.: 30 dias), deixe uma folga entre `cut` e o início do holdout.

## 1. Forma e tipos

```python
print(train.shape)
print(train.dtypes.to_frame("dtype").join(train.nunique().rename("nunique")))
print("duplicatas exatas:", train.duplicated().sum())
print("duplicatas por entidade:", train.duplicated(subset=[ENTITY]).sum())
const = [c for c in train.columns if train[c].nunique(dropna=False) <= 1]
quase_const = [c for c in train.columns if train[c].value_counts(normalize=True, dropna=False).iloc[0] > 0.99]
print("constantes:", const, "| quase constantes (>99% em um valor):", quase_const)
```

## 2. Ausentes e sentinelas

```python
miss = train.isna().mean().sort_values(ascending=False)
print(miss[miss > 0])

# a ausência depende do alvo? (dica de mecanismo, não prova)
for col in miss[miss > 0].index:
    print(col, train.groupby(train[col].isna())[TARGET].mean().to_dict())

# sentinelas comuns (revise com o dono do dado; zero pode ser verdadeiro)
for col in train.select_dtypes("number"):
    frac_zero = (train[col] == 0).mean()
    frac_neg1 = (train[col] == -1).mean()
    frac_9999 = (train[col] == 9999).mean()
    if max(frac_zero, frac_neg1, frac_9999) > 0.05:
        print(col, {"zero": round(frac_zero, 3), "-1": round(frac_neg1, 3), "9999": round(frac_9999, 3)})
for col in train.select_dtypes("object"):
    print(col, train[col].isin(["", "N/A", "NA", "null", "None", "?"]).mean())
```

## 3. Alvo

```python
print(train[TARGET].value_counts())
print(train[TARGET].value_counts(normalize=True))   # prevalência = baseline de PR-AUC
# regressão: print(train[TARGET].describe(percentiles=[.01, .05, .5, .95, .99]), (train[TARGET] == 0).mean())
```

## 4. Univariada (média e DP junto de mediana e IQR)

```python
num = train.select_dtypes("number").drop(columns=[TARGET], errors="ignore")
q = num.quantile([0.25, 0.5, 0.75])
res = pd.DataFrame({
    "mean": num.mean(), "std": num.std(),
    "median": q.loc[0.5], "iqr": q.loc[0.75] - q.loc[0.25],
    "p01": num.quantile(0.01), "p99": num.quantile(0.99),
    "skew": num.skew(),
})
print(res.round(3))
for col in train.select_dtypes("object"):
    print(col, train[col].value_counts(dropna=False).head(5).to_dict())
print(train[DATE].min(), train[DATE].max())
```

## 5. Bivariada com o alvo (classificação binária 0/1)

```python
from sklearn.feature_selection import mutual_info_classif

# numéricas: alvo médio por decil (qcut descarta decis repetidos)
for col in num.columns:
    bins = pd.qcut(train[col], 10, duplicates="drop")
    print(col, train.groupby(bins, observed=True)[TARGET].agg(["mean", "count"]).round(3).to_dict("list"))

# informação mútua (imputação só para este cálculo, com mediana do treino)
X = num.fillna(num.median())
mi = pd.Series(mutual_info_classif(X, train[TARGET], random_state=SEED), index=X.columns)
print(mi.sort_values(ascending=False).round(4))

# categóricas: alvo médio e contagem por nível
for col in train.select_dtypes("object"):
    print(train.groupby(col, dropna=False)[TARGET].agg(["mean", "count"]).sort_values("count", ascending=False).head(10))
```

Leitura: relações vistas aqui são exploratórias. Informação mútua em `random_state` fixo para reproduzir.

## 6. Varredura de vazamento

```python
import re
from sklearn.metrics import roc_auc_score

suspeitas_nome = [c for c in train.columns
                  if re.search(r"(^id$|_id$|date|time|_at$|cancel|reason|status|result|outcome|after|post|final)", c, re.I)
                  and c != TARGET]
print("revisar nome/origem:", suspeitas_nome)

# AUC de feature única: perto de 1,0 ou 0,0 merece pergunta (indício, não prova)
aucs = {}
for col in num.columns:
    s = train[[col, TARGET]].dropna()
    if s[TARGET].nunique() == 2 and s[col].nunique() > 1:
        a = roc_auc_score(s[TARGET], s[col])
        aucs[col] = max(a, 1 - a)
print(pd.Series(aucs).sort_values(ascending=False).head(10).round(3))
```

Para cada coluna sinalizada, escreva a pergunta de ordem temporal ("quando é escrita vs quando decidimos?") e encaminhe para `ds-leakage-audit`.

## 7. Cardinalidade e outliers (somente sinalizar)

```python
cat = train.select_dtypes("object").nunique().sort_values(ascending=False)
print(cat)   # 15 níveis é ponto de partida para trocar one-hot por outro encoder, não regra

iqr = num.quantile(0.75) - num.quantile(0.25)
low, high = num.quantile(0.25) - 1.5 * iqr, num.quantile(0.75) + 1.5 * iqr
flag = ((num < low) | (num > high)).mean().sort_values(ascending=False)
print(flag[flag > 0].round(4))   # fração sinalizada por coluna; nada é removido
```

Para cada coluna com muitos sinalizados, pergunte o que o valor significa (erro de entrada, caso legítimo raro, unidade diferente) antes de qualquer tratamento.

## 8. Salvar o relatório

```python
from pathlib import Path
Path("reports/figuras").mkdir(parents=True, exist_ok=True)
res.round(4).to_csv("reports/eda_univariada.csv")
```

Gravar em `reports/` é o único destino de escrita previsto; qualquer outro destino pede confirmação. Em figuras, siga o checklist de figura (eixos com unidade, n, incerteza, ausente diferente de zero, cor com redundância).
