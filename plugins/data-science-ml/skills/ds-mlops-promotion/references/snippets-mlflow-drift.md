# Snippets: MLflow (log, alias, carga) e drift (PSI, KS, qui-quadrado)

Validado em 2026-10-10. Base: página do MLflow Model Registry (aliases, URI `models:/<nome>@<alias>`, `set_signature`; V-22, Verificado), AWS MLOPS01-BP03 e skill de drift de timwukp (Apache-2.0; limiares 0,1/0,2 são convenção; V-24). Funções de PSI/KS/qui-quadrado são conhecimento estatístico estável, escritas pelo plugin. Nada foi executado (Não verificado). **Este arquivo é para o humano executar com permissão no próprio ambiente**; a skill não registra nem promove modelos. Confira `mlflow --version`, `pip show evidently scipy`.

## Sumário
1. Registrar um run com rastreabilidade
2. Alias e carga por URI
3. PSI com bins definidos pela referência
4. KS e qui-quadrado com tamanho de efeito
5. Relatório de drift por coluna
6. Esqueleto de Evidently (versão a fixar)

## 1. Registrar um run com rastreabilidade

```python
import hashlib, subprocess
import numpy as np
import mlflow

def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()

def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()

with mlflow.start_run(run_name="churn-lgbm-2026-10-10") as run:
    mlflow.log_params({"seed": 42, "learning_rate": 0.03, "num_leaves": 31})
    mlflow.set_tags({
        "data_sha256": sha256_file("data/processed/train.parquet"),
        "git_commit": git("rev-parse", "HEAD"),
        "git_dirty": str(bool(git("status", "--porcelain"))),    # sem isso o SHA engana
    })
    for fold, auc in enumerate(fold_pr_auc):                     # métricas por dobra
        mlflow.log_metric("pr_auc_fold", auc, step=fold)
    mlflow.log_metric("pr_auc_cv_mean", float(np.mean(fold_pr_auc)))
    mlflow.log_artifact("uv.lock")                                # ou poetry.lock, conda-lock, pip freeze
    # Pipeline COMPLETO (pré-processamento + modelo). O nome do argumento do caminho do artefato varia por versão
    # do MLflow (artifact_path em 2.x; versões novas podem usar name=): confira a assinatura instalada.
    mlflow.sklearn.log_model(pipe, artifact_path="model", signature=signature)
```

Não passe `registered_model_name` aqui se a política exigir que um humano registre/promova. O SHA do commit sem a flag de diretório sujo não identifica o código que rodou (V-22).

## 2. Alias e carga por URI

Ação do humano autorizado a promover:

```python
from mlflow import MlflowClient

client = MlflowClient()
# registro: a partir do run (uma vez, por quem tem permissão)
mv = mlflow.register_model(f"runs:/{run.info.run_id}/model", "churn-clf")
client.set_registered_model_alias("churn-clf", "challenger", mv.version)
# promoção: mover o alias que a produção lê (quem promove deve estar registrado na política)
client.set_registered_model_alias("churn-clf", "champion", mv.version)
```

No serving, carregue por alias ou versão, **nunca por `run_id`**:

```python
import mlflow.pyfunc
model = mlflow.pyfunc.load_model("models:/churn-clf@champion")      # ou "models:/churn-clf/7"
```

`set_registered_model_alias` e a URI com `@alias` aparecem na documentação do registry (URI Verificada em V-22; o nome exato do método de cliente é conhecimento estável, Inferido: confira). Rollback = mover o alias `champion` de volta para a versão anterior. Carregar um modelo do registro executa a desserialização do artefato: o controle de escrita no registro é parte da segurança (Inferido).

## 3. PSI com bins definidos pela referência

```python
import numpy as np

def psi(ref, cur, bins=10, eps=1e-6):
    """Population Stability Index numérico. Bins por quantis da REFERÊNCIA, pontas abertas."""
    ref, cur = np.asarray(ref, float), np.asarray(cur, float)
    ref, cur = ref[~np.isnan(ref)], cur[~np.isnan(cur)]
    edges = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        return float("nan")            # quantis degenerados (muitos valores repetidos): use bins fixos ou trate como categórica
    edges[0], edges[-1] = -np.inf, np.inf
    r = np.histogram(ref, edges)[0] / len(ref)
    c = np.histogram(cur, edges)[0] / len(cur)
    r, c = np.clip(r, eps, None), np.clip(c, eps, None)
    return float(np.sum((c - r) * np.log(c / r)))
```

Faixas usadas por convenção (não por derivação): ~0,1 atenção, ~0,2 alerta. Documente como convenção do time e ajuste ao custo do alerta. Com valores muito repetidos (zeros), os quantis colapsam; o `nan` devolvido é um aviso, não um zero.

## 4. KS e qui-quadrado com tamanho de efeito

```python
import pandas as pd
from scipy import stats

def ks_report(ref, cur):
    res = stats.ks_2samp(ref, cur)
    return {"ks_D": float(res.statistic), "p": float(res.pvalue)}      # D é o tamanho de efeito (0 a 1)

def chi2_report(ref, cur):
    """Categóricas: tabela de contingência nível x janela; devolve p e V de Cramér."""
    tab = pd.crosstab(pd.concat([ref, cur], ignore_index=True),
                      np.r_[np.zeros(len(ref)), np.ones(len(cur))])
    chi2, p, dof, _ = stats.chi2_contingency(tab)
    n = tab.to_numpy().sum()
    v = np.sqrt(chi2 / (n * (min(tab.shape) - 1)))
    return {"chi2": float(chi2), "p": float(p), "cramers_v": float(v)}
```

Com amostras grandes o p-valor sempre fica pequeno: decida pelo **tamanho de efeito** (D, V, PSI) e pelo impacto na métrica, e corrija múltiplos testes quando varrer muitas colunas (Holm ou BH conforme o uso; ver `ds-inference-review`). Níveis raros (contagens esperadas < 5) pedem agrupamento antes do qui-quadrado.

## 5. Relatório de drift por coluna

```python
def drift_table(ref_df, cur_df, num_cols, cat_cols):
    rows = []
    for c in num_cols:
        k = ks_report(ref_df[c].dropna(), cur_df[c].dropna())
        rows.append({"coluna": c, "tipo": "num", "psi": psi(ref_df[c], cur_df[c]), "efeito": k["ks_D"], "p": k["p"]})
    for c in cat_cols:
        x = chi2_report(ref_df[c].astype(str), cur_df[c].astype(str))
        rows.append({"coluna": c, "tipo": "cat", "psi": np.nan, "efeito": x["cramers_v"], "p": x["p"]})
    return pd.DataFrame(rows).sort_values("efeito", ascending=False)
```

Interprete em três camadas: drift de **entrada** (colunas), de **predição** (distribuição do score) e de **qualidade** (quando os rótulos chegam). Drift sem perda de desempenho pode ser benigno; perda sem drift de entrada aponta mudança no conceito ou nos rótulos. O alerta precisa de dono e ação; o retreino é decisão humana.

## 6. Esqueleto de Evidently (versão a fixar)

A página de quickstart consultada (V-24) não declara a versão da API. Fixe a versão no lockfile e confira a documentação dela antes de copiar:

```python
# pip install evidently==<VERSÃO FIXADA>   (instalação por quem opera o ambiente, com o gerenciador do projeto)
import pandas as pd
from evidently import Dataset, DataDefinition, Report
from evidently.presets import DataDriftPreset

definition = DataDefinition(numerical_columns=num_cols, categorical_columns=cat_cols)
ref = Dataset.from_pandas(ref_df, data_definition=definition)
cur = Dataset.from_pandas(cur_df, data_definition=definition)
report = Report([DataDriftPreset()])
result = report.run(cur, ref)      # (atual, referência); confira a ordem na versão instalada
# exportação para JSON/HTML: veja a documentação da versão fixada
```

Nomes e caminhos de importação acima seguem o quickstart lido (`Dataset.from_pandas` com `DataDefinition` explícito, `Report([DataDriftPreset()])`, `report.run(...)`); como a versão não foi declarada, trate como Inferido e valide no ambiente.
