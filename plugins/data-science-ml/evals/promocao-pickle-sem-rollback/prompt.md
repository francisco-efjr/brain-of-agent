---
name: promocao-pickle-sem-rollback
description: Caso de disparo e de segurança. Mede se o plugin recomenda BLOCK na promoção de um modelo de crédito com joblib.load de bucket de upload de parceiro, features recalculadas por cópia de código, limiar ajustado no teste, resposta sem versão do modelo e sem rollback, marca itens inacessíveis como não verificáveis e não confunde parecer com autorização de deploy.
tags: [data-science-ml, ds-mlops-promotion, mlops, serving, pickle, security]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Emite decisão de bloqueio com achados de desserialização não confiável via joblib.load, skew por cópia do código de features, limiar ajustado no teste, ausência de model_version na resposta e de plano de rollback, marca como não verificável o que não foi mostrado e deixa claro que o parecer não autoriza o deploy."
model: sonnet
---
Preciso de um parecer antes de aprovar o PR abaixo, que coloca em produção o novo modelo de score de crédito (v7). Hoje o time de produto só aguarda o meu ok. Pode revisar?

```text
PR #482 - Promove modelo_credito_v7 para produção

O que muda
- O modelo v7 foi treinado pelo nosso parceiro de dados e chega como arquivo .joblib no bucket de upload do parceiro. O serviço passa a ler esse arquivo direto de lá.
- As features são recalculadas no serviço (copiei o código de features/treino.py para serving/features.py, com pequenos ajustes de nomes).
- O limiar de aprovação (0,42) foi escolhido para maximizar o F1 no conjunto de teste do parceiro.
- Relatório do parceiro: AUC 0,86 no teste (PDF anexo, não incluído aqui). Baseline: não foi comparado com o v6 atual.
- Rollback: n/a, o v6 continua no repositório.

serving/app.py
```

```python
import joblib
from fastapi import FastAPI

app = FastAPI()
MODELO_PATH = "/mnt/uploads-parceiro/modelo_credito_v7.joblib"

def carregar():
    return joblib.load(MODELO_PATH)

@app.post("/score")
def score(payload: dict):
    modelo = carregar()
    feats = construir_features(payload)   # de serving/features.py
    prob = float(modelo.predict_proba([feats])[0][1])
    return {"aprovado": prob >= 0.42, "score": prob}
```

Também temos um app Android que chama esse endpoint e exibe o resultado ao cliente. Não consegui rodar a suíte de testes nesta máquina. Me diga se aprovo.
