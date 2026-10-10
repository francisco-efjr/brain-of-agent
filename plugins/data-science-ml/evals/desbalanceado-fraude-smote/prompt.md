---
name: desbalanceado-fraude-smote
description: Caso de disparo e de fidelidade técnica. Mede se o plugin reconhece acurácia inútil em fraude de 0,4 por cento, aponta SMOTE antes do split como vazamento, propõe PR-AUC e recall com precisão fixa, pesos antes de reamostrar, reamostragem dentro do fold e limiar escolhido na validação.
tags: [data-science-ml, ds-model-evaluation, imbalance, smote, threshold]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Diz que a acurácia de 99,6 por cento é enganosa com prevalência de 0,4 por cento, identifica SMOTE antes de train_test_split como vazamento que invalida recall 0,93 e precisão 0,91 medidos em teste reamostrado, recomenda PR-AUC ou recall com precisão fixa, pesos antes de reamostrar, reamostragem só dentro do fold e limiar na curva precisão-recall de validação."
model: sonnet
---
Estou construindo um detector de fraude em transações de cartão (284 mil transações, só 0,4% são fraude). Meu primeiro modelo deu 99,6% de acurácia, mas quando olhei só pegava 31% das fraudes (recall 0,31). Aí apliquei SMOTE e agora o teste mostra recall 0,93 e precisão 0,91. Parece ótimo, mas queria ajuda para melhorar mais e saber se posso levar isso para a equipe de risco. O custo de deixar passar uma fraude é cerca de 20 vezes o custo de revisar uma transação suspeita à mão.

```python
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

df = pd.read_csv("transacoes.csv")
X, y = df.drop(columns="fraude"), df["fraude"]

X_res, y_res = SMOTE(random_state=42).fit_resample(X, y)
X_tr, X_te, y_tr, y_te = train_test_split(X_res, y_res, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_tr, y_tr)
pred = clf.predict(X_te)
print(accuracy_score(y_te, pred), precision_score(y_te, pred), recall_score(y_te, pred))
```

Não rode nada; quero seu parecer e o plano do que eu deveria fazer em seguida.
