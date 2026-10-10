# Tuning: Optuna, early stopping em LightGBM e XGBoost

Validado em 2026-10-10. Fontes: V-21 (skill de param087, MIT, classe C) cruzada com as páginas de parameter tuning do LightGBM e do XGBoost (Verificadas em V-21). APIs de Optuna, LightGBM e XGBoost mudam entre versões: fixe versões no lockfile e confira (`pip show optuna lightgbm xgboost`). Esqueletos não executados (Não verificado). CatBoost não foi pesquisado.

## Sumário
1. Escolha do método e do orçamento
2. Optuna sem poda (modelos de árvore, CV por Pipeline)
3. Optuna com poda (treino iterativo)
4. LightGBM: early stopping e parâmetros-chave
5. XGBoost: early stopping e parâmetros-chave
6. Relato do tuning

## 1. Escolha do método e do orçamento

| Situação | Método | Observação |
| --- | --- | --- |
| 2 a 3 parâmetros, treino barato | grid | cobre o espaço de forma previsível |
| Muitos parâmetros | random (escala log para taxas) | melhor cobertura por tentativa que grid |
| Modelo caro | Optuna (TPE) | defina `n_trials`, `timeout` e `seed` do sampler |
| Rede neural com treino iterativo | Optuna + poda | exige `trial.report()` e `trial.should_prune()` |

Orçamento: declare `n_trials`, tempo máximo e critério de parada antes de começar; registre o espaço de busca no experimento (hash do arquivo de config). 3 a 5 hiperparâmetros por rodada; espaço largo primeiro, depois estreito em torno do melhor.

## 2. Optuna sem poda

`cross_val_score` devolve só a média final: serve a Optuna, mas **não permite poda**.

```python
import numpy as np
import optuna
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
import lightgbm as lgb

SEED = 42
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)   # mesma CV para todas as tentativas e para a comparação com o baseline

def objective(trial: optuna.Trial) -> float:
    params = {
        "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 8, 256, log=True),
        "min_child_samples": trial.suggest_int("min_child_samples", 5, 200, log=True),
        "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10.0, log=True),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "n_estimators": 400,            # fixo aqui; o número final vem do early stopping (passo 4)
        "random_state": SEED, "verbose": -1,
    }
    pipe = Pipeline([("prep", prep), ("clf", lgb.LGBMClassifier(subsample_freq=1, **params))])
    return cross_val_score(pipe, X_train, y_train, cv=cv, scoring="average_precision").mean()

study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=SEED))
study.optimize(objective, n_trials=60, timeout=1800)
print(study.best_params, study.best_value)
```

`subsample` só tem efeito quando `subsample_freq` > 0 no LightGBM (por isso o argumento fixo). Escala log para taxa de aprendizado e regularização; `num_leaves` abaixo de 2^max_depth se `max_depth` for limitado.

## 3. Optuna com poda (treino iterativo)

Exige métrica intermediária reportada a cada passo ou época. Esqueleto para uma rede (funções `train_one_epoch` e `evaluate` do projeto):

```python
def objective(trial):
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
    wd = trial.suggest_float("weight_decay", 1e-8, 1e-2, log=True)
    model = build_model().to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)
    for epoch in range(cfg.max_epochs):
        train_one_epoch(model, opt, train_loader)
        val_metric = evaluate(model, val_loader)       # métrica na validação, nunca no teste
        trial.report(val_metric, step=epoch)
        if trial.should_prune():
            raise optuna.TrialPruned()
    return val_metric

study = optuna.create_study(direction="maximize",
                            sampler=optuna.samplers.TPESampler(seed=SEED),
                            pruner=optuna.pruners.MedianPruner(n_warmup_steps=3))
study.optimize(objective, n_trials=40, timeout=3600)
```

Sem `trial.report()` e `trial.should_prune()` dentro do treino, o pruner nunca age. Seed do sampler não torna o treino determinístico por si só: use também `seed_everything` por tentativa (ver `snippets-treino.md`).

## 4. LightGBM: early stopping e parâmetros-chave

```python
import lightgbm as lgb

model = lgb.LGBMClassifier(n_estimators=5000, learning_rate=0.03, num_leaves=31,
                           min_child_samples=20, subsample=0.8, subsample_freq=1,
                           colsample_bytree=0.8, random_state=SEED, verbose=-1)
model.fit(X_tr, y_tr, eval_set=[(X_es, y_es)], eval_metric="auc",
          callbacks=[lgb.early_stopping(stopping_rounds=100, verbose=False)])
best_iter = model.best_iteration_
```

- `X_es, y_es` é um conjunto de **validação para parada**, separado do conjunto usado para relatar e do teste. Early stopping exige validação; reportar a métrica do mesmo conjunto que decide a parada é otimista.
- Em versões antigas, `early_stopping_rounds` era argumento de `fit`; em 4.x use o callback (confira a versão).
- Parâmetros-chave (documentação do LightGBM, Verificado em V-21): `num_leaves` (mantenha abaixo de 2^max_depth), `min_data_in_leaf`/`min_child_samples` como guarda contra overfitting, `learning_rate` menor com mais árvores, `feature_fraction`/`bagging_fraction`.
- Depois de achar `best_iter`, refaça o modelo final com `n_estimators=best_iter` no treino completo (treino + parada) e avalie uma vez no teste.

## 5. XGBoost: early stopping e parâmetros-chave

```python
import xgboost as xgb

model = xgb.XGBClassifier(n_estimators=5000, learning_rate=0.03, max_depth=6,
                          min_child_weight=1, subsample=0.8, colsample_bytree=0.8,
                          gamma=0.0, tree_method="hist", eval_metric="aucpr",
                          early_stopping_rounds=100, random_state=SEED)
model.fit(X_tr, y_tr, eval_set=[(X_es, y_es)], verbose=False)
best_iter = model.best_iteration
```

- Em XGBoost 2.x, `early_stopping_rounds` fica no construtor; em versões antigas era argumento de `fit` (confira).
- Parâmetros da documentação de tuning (Verificado em V-21): `max_depth`, `min_child_weight`, `gamma`, `subsample`, `eta` (`learning_rate`).
- Desbalanceamento: com AUC como objetivo, `scale_pos_weight`; se a probabilidade calibrada importa, não reponderar e usar `max_delta_step` finito (V-17, Verificado na documentação do XGBoost).

## 6. Relato do tuning

Inclua: espaço de busca, método, `n_trials`, tempo, seed, CV, métrica, melhor valor **e** o valor do baseline sem tuning sob a mesma CV, número de tentativas podadas, versões. Se o ganho for menor que a dispersão entre dobras, escreva "sem ganho distinguível" em vez de promover o resultado. Teste final: uma vez, com a configuração escolhida.
