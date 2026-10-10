---
name: leakage-scaler-seletor-fora-do-cv
description: Caso de disparo e de fidelidade técnica. Mede se o plugin audita um experimento com StandardScaler e SelectKBest ajustados na tabela inteira antes da validação cruzada, AUC de 0,97 e vários exames por paciente, propõe Pipeline e validação por grupo e separa leitura de código de execução.
tags: [data-science-ml, ds-leakage-audit, leakage, cross-validation, pipeline]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta scaler e seleção de features supervisionada ajustados em todo o X antes de cross_val_score como causa provável de inflação do AUC 0,97, propõe Pipeline dentro da validação cruzada, levanta o risco de grupo por paciente e de tempo, separa o que leu no código do que não verificou e não afirma ter rodado nada."
model: sonnet
---
Vou apresentar este modelo ao time clínico na quinta e queria uma segunda opinião antes. Ele prevê se um exame indica a condição X a partir de 2000 marcadores de laboratório. Temos 5000 exames de cerca de 1800 pacientes (alguns pacientes têm vários exames, coletados em datas diferentes). O AUC deu 0,97, bem acima do que a literatura reporta. Posso reportar esse número como desempenho esperado?

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

df = pd.read_csv("exames.csv")  # 5000 linhas; colunas: paciente_id, data_coleta, alvo e 2000 marcadores m0001..m2000
X = df.drop(columns=["paciente_id", "data_coleta", "alvo"])
y = df["alvo"]

X = StandardScaler().fit_transform(X)
X = SelectKBest(f_classif, k=20).fit_transform(X, y)

modelo = RandomForestClassifier(n_estimators=300, random_state=0)
scores = cross_val_score(modelo, X, y, cv=5, scoring="roc_auc")
print(scores.mean())  # 0.97
```

Não consigo rodar nada agora, então me diga o que você consegue concluir só pelo código e o que ficou sem verificar.
