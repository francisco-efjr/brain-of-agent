# Classes de vazamento, padrões de código e exemplo completo

Validado em 2026-10-10. Redação própria; base: documentação do scikit-learn 1.9.1 (V-12), regra de ordem temporal da skill `leakage-auditor` de pitcany (V-13, MIT, destilada). Classes agrupadas em seis famílias; o agrupamento fino é do plugin (Inferido).

## Sumário
1. Classes e como detectar
2. Código errado e código certo
3. Exemplo completo: churn mensal
4. Perguntas prontas ao usuário

## 1. Classes e como detectar

| Família | Variante | Como detectar | Correção |
| --- | --- | --- | --- |
| Alvo | Feature derivada do rótulo (`cancel_reason`, `status_final`, `refund_amount` para prever fraude) | Nome ou origem posterior ao desfecho; AUC de feature única perto de 1,0 | Remover; se for útil só depois da decisão, é outro problema de negócio |
| Alvo | Proxy do rótulo (flag criada pelo processo que reage ao desfecho) | Pergunte quem escreve a coluna e quando | Remover ou usar valor da data de decisão |
| Temporal | Valor escrito depois da decisão (snapshot "atual" em vez de na data) | Tabela de disponibilidade; SQL sem filtro `<= data_decisão` | Reconstruir point-in-time (ver `ds-time-series-backtest`) |
| Temporal | Split aleatório com dado dependente do tempo | `KFold(shuffle=True)`, `train_test_split` sem ordem | Origem rolante, `TimeSeriesSplit`, corte por data |
| Temporal | Janela que olha para frente | `rolling(center=True)`, `shift(-n)`, `bfill`, `interpolate` global | Janela só com passado; `closed`/`shift(+n)` |
| Pré-processamento | `fit` fora do fold (scaler, imputer, PCA, seletor, TF-IDF, encoder supervisionado, SMOTE) | Grep `fit_transform` antes de `train_test_split`/`cross_val_score` | `Pipeline` inteiro dentro da CV |
| Pré-processamento | Seleção de features com `y` no dataset inteiro | `SelectKBest`/`RFE` antes do split | Seletor dentro do Pipeline |
| Pré-processamento | Estatística global (média por grupo, contagem total) usada como feature | `groupby().transform` no dataset inteiro | Calcular dentro do fold ou só com passado |
| Pré-processamento | Target encoding com prior ou média do dataset inteiro | Encoder próprio sem `fit`/`transform` | Prior dentro do fold, cross-fitting (ver `ds-model-evaluation`) |
| Grupo/entidade | Mesma entidade em treino e teste | Contar `id` em ambos os lados da partição | `GroupKFold`, `StratifiedGroupKFold`, `GroupShuffleSplit` |
| Grupo/entidade | Linhas correlacionadas (sessões do mesmo usuário, exames do mesmo paciente) | Mesmo | Agrupar pela unidade independente |
| Duplicatas | Duplicatas exatas ou quase idênticas entre partições | `duplicated()` e hash de colunas normalizadas; texto com variações | Deduplicar antes do split, agrupar por cluster |
| Derivado do futuro | Artefato calculado depois (modelo de recomendação treinado com dados atuais, embedding atualizado, score de outro modelo) | Pergunte a data de treino do insumo | Usar versão do insumo vigente na data da decisão |
| Derivado do futuro | Filtro de coorte pelo desfecho (só clientes com 12 meses de histórico) | Leia o `WHERE` e o `.query()` | Definir coorte pelo que se sabe na decisão |
| Escolha com o teste | Limiar, modelo, hiperparâmetro, early stopping ou feature escolhidos olhando o teste | Grep `eval_set`, `best_`, `threshold`; fluxo do notebook | Escolher na validação; teste uma vez |

Evidência empírica (só corrobora): ablação da feature suspeita; uma feature concentrando a importância; métrica sob split temporal ou por grupo bem abaixo da atual.

## 2. Código errado e código certo

Errado (vazamento de seleção e de escala; padrão do exemplo E-01):

```python
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

X = StandardScaler().fit_transform(X)               # fit em todas as linhas
X = SelectKBest(f_classif, k=20).fit_transform(X, y)  # usa y de todas as linhas
scores = cross_val_score(RandomForestClassifier(random_state=0), X, y, cv=5, scoring="roc_auc")
```

Certo (tudo que aprende, dentro do Pipeline; a CV recebe o Pipeline):

```python
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("select", SelectKBest(f_classif, k=20)),
    ("clf", RandomForestClassifier(random_state=0)),
])
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
scores = cross_val_score(pipe, X, y, cv=cv, scoring="roc_auc")
```

Observação: o escalonamento é inócuo para floresta aleatória; ele está no exemplo para mostrar a regra, que vale para qualquer passo que aprende.

Grupo (entidades repetidas):

```python
from sklearn.model_selection import StratifiedGroupKFold
cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=0)
scores = cross_val_score(pipe, X, y, groups=df["customer_id"], cv=cv, scoring="roc_auc")
```

Tempo (nunca embaralhar): `TimeSeriesSplit(n_splits=5, gap=<dias entre decisão e rótulo>)` ou corte manual por data. Detalhes em `ds-time-series-backtest`.

Janela com vazamento e correção:

```python
df["m7_errado"] = df["vendas"].rolling(7, center=True).mean()  # usa 3 dias do futuro
df["m7"] = df["vendas"].shift(1).rolling(7).mean()            # só passado até t-1
```

Checagem rápida de sobreposição de entidades (rode se puder; senão, peça ao usuário):

```python
overlap = set(train["customer_id"]) & set(test["customer_id"])
print(len(overlap))  # esperado 0 quando o split é por cliente
```

## 3. Exemplo completo: churn mensal

Contexto: decisão no dia 1 de cada mês (ação de retenção); rótulo `churned` = cancelou em até 30 dias. Features: `plan`, `tenure_months`, `support_tickets`, `monthly_charge`, `cancel_reason`, `last_login_days`.

| Feature | Valor escrito em | Disponível na decisão? | Evidência |
| --- | --- | --- | --- |
| `plan` | cadastro; muda por evento | sim, se lida com a versão da data | `features.sql:7` usa `plans_current` (estado atual) |
| `tenure_months` | calculado | pergunta: até hoje ou até o dia 1? | `features.sql:12` usa `CURRENT_DATE` |
| `support_tickets` | contagem acumulada | pergunta: janela termina no dia 1? | `features.sql:15` sem filtro de data |
| `cancel_reason` | preenchido no cancelamento | não | só existe para quem cancelou; escrito depois da decisão |
| `last_login_days` | calculado | sim, se até o dia 1 | `features.sql:20` filtra `<= decision_date` |

Achados:
- `[blocker] cancel_reason | alvo | features.sql:9 | preenchido quando o cliente cancela, depois do dia 1 em que o modelo decide | infla | remover`.
- `[high + pergunta] tenure_months | temporal | features.sql:12 | se CURRENT_DATE é a data de execução da extração, o valor é escrito depois da decisão | infla levemente | recalcular com decision_date`.
- `[high] plan | temporal | features.sql:7 | plans_current reflete o plano atual; um downgrade feito depois da decisão por intenção de cancelar entra como feature | infla | usar histórico de planos com validade`.

(Exemplo ilustrativo construído para este arquivo; nenhum dado real.)

## 4. Perguntas prontas ao usuário

1. "A coluna X é preenchida por que processo e quando, em relação à decisão?"
2. "A janela de `<feature>` termina na data de decisão ou na data da extração?"
3. "A tabela Y guarda o histórico (com validade) ou só o estado atual?"
4. "Uma mesma pessoa/loja/dispositivo pode aparecer em mais de uma linha? Qual é a unidade independente?"
5. "Há dados posteriores à data de corte do teste dentro do treino?"
