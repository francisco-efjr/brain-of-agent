# Vazamento de dados e desenho de validação

Validado em 2026-10-10 (scikit-learn docs 1.9.1; confira a versão instalada). Fontes: V-12, V-13, V-14, V-31 (ver `fontes.md`). Rótulos: Verificado (lido na fonte), Inferido (conhecimento estável do domínio, não reconferido nesta rodada).

## Sumário
1. Regra de ouro e vocabulário
2. Classes de vazamento
3. Tabela de disponibilidade das features
4. As quatro checagens de split
5. Splitters do scikit-learn: quando usar cada um
6. Receita: Pipeline dentro da validação
7. Backtest rolante para séries temporais
8. Checklist de séries (8 itens)
9. Previsão com LLM
10. Evidência empírica: só corrobora
11. Severidade e saída

## 1. Regra de ouro e vocabulário

Defina dois instantes: **instante da decisão** (quando o modelo é consultado em produção) e **instante do rótulo** (quando o alvo fica conhecido). Vazamento é qualquer informação usada no treino ou na seleção que não estaria disponível, do mesmo jeito, no instante da decisão.

**Toda alegação de vazamento, ou de ausência de vazamento, traz uma frase de ordem temporal:** "o valor de `X` é escrito em `<quando>`; a decisão ocorre em `<quando>`". Sem a frase, o item vira **pergunta ao usuário** e entra como severidade "high + pergunta", nunca como bloqueador (V-13).

## 2. Classes de vazamento

Agrupadas (a fonte de V-13 lista 12 classes; esta é a agregação do plugin, Inferido):

| Classe | Exemplo | Como aparece |
| --- | --- | --- |
| Alvo | Coluna derivada do desfecho (`cancel_reason`, `refund_amount`) | Feature quase perfeita; importância concentrada em uma coluna |
| Temporal | Feature calculada com dado posterior à decisão; `rolling(center=True)`; `shift(-1)` | Desempenho cai muito no deploy |
| Pré-processamento | `fit_transform` de scaler, imputer, seletor, encoder supervisionado ou PCA antes do split | Métrica inflada; rótulos aleatórios chegam a ~0,76 de acurácia com seleção fora do fold (exemplo da doc do sklearn) |
| Grupo/entidade | Várias linhas do mesmo usuário em treino e teste | Teste "fácil"; `GroupKFold` derruba a métrica |
| Duplicatas | Linhas idênticas ou quase (reenvio, versões de documento) entre treino e teste | Acerto perfeito em parte do teste |
| Derivados do futuro | Agregados de cadastro atual aplicados a evento passado; filtros de coorte definidos pelo desfecho; tuning e seleção no teste | Join com tabela "atual" sobre evento histórico |

Também verifique reamostragem antes do split (SMOTE) e reamostragem aplicada ao teste (V-17).

## 3. Tabela de disponibilidade das features

Modelo em `assets/templates/tabela-disponibilidade-features.md`. Uma linha por feature (ou grupo): **feature · valor escrito em · disponível na decisão? (sim / não / pergunta) · evidência (arquivo:linha)**. Exemplo:

| feature | valor escrito em | disponível na decisão? | evidência |
| --- | --- | --- | --- |
| `tickets_30d` | ao fechar cada ticket | sim, se a janela termina na decisão | `features.py:41` |
| `cancel_reason` | no cancelamento (o desfecho) | não | `schema.sql:12` |
| `plan_current` | tabela cadastro, sobrescrita diariamente | pergunta: é o plano na data do evento? | `join_cadastro.sql:7` |

## 4. As quatro checagens de split (passa/falha, com caminho:linha)

1. **Pré-processamento depois do split**: todo `fit` só no treino, dentro de `Pipeline`/fold.
2. **Grupo**: nenhuma entidade em treino e teste ao mesmo tempo (`GroupKFold`).
3. **Tempo**: quando há tempo, treino sempre anterior ao teste (origem rolante).
4. **Teste intocado**: sem uso do teste em escolha de modelo, limiar, hiperparâmetro ou feature.

## 5. Splitters do scikit-learn

| Situação | Splitter | Nota |
| --- | --- | --- |
| i.i.d., regressão | `KFold` | `KFold` e `ShuffleSplit` assumem i.i.d. |
| Classe desbalanceada | `StratifiedKFold` | Mantém a proporção por dobra |
| Várias linhas por entidade | `GroupKFold` | Passe `groups=` |
| Entidade e classe rara | `StratifiedGroupKFold` | Conhecimento estável, Inferido; confirme na doc da versão |
| Dados com tempo | `TimeSeriesSplit` | Treinos crescentes, sem `shuffle`; parâmetros `gap`, `test_size`, `max_train_size` |
Embaralhar documentos ordenados no tempo infla a validação (doc de cross-validation, §3.1.3, Verificado). Passe **inteiros** como `random_state` nos splitters e cuidado com `RandomState` em estimadores: `clone` de estimador com `RandomState` não produz cópia exata (Verificado). A página de pitfalls não cobre ordem das amostras nem desbalanceamento; a de cross-validation cobre estratificação, grupos e tempo.

## 6. Receita: Pipeline dentro da validação

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, cross_val_score

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("select", SelectKBest(f_classif, k=20)),
    ("clf", LogisticRegression(max_iter=1000)),
])
scores = cross_val_score(
    pipe, X_train, y_train, groups=groups_train,
    cv=GroupKFold(n_splits=5), scoring="average_precision",
)
```

Contrato: o `Pipeline` **inteiro** vai para `cross_val_score` e para `GridSearchCV`/Optuna; o hold-out (`X_test`) só aparece uma vez no fim. Antes dessa célula, `X_train` já veio de um split por tempo ou por grupo. Para reamostragem use `imblearn.pipeline.Pipeline`, que reamostra apenas o treino de cada dobra (V-17).

## 7. Backtest rolante para séries temporais (V-14)

Origem rolante: em cada origem `t`, treine só com dados até `t` e avalie no horizonte `t+1 … t+h` da decisão. Janela **crescente** (usa todo o passado) ou **deslizante** (últimos N pontos): declare qual e por quê. Erro por horizonte, não um único agregado. Escolha o modelo pelo erro de validação cruzada temporal, não pelo resíduo no treino (Hyndman e Athanasopoulos, FPP3, Verificado; exemplos do livro em R).

```python
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=6, test_size=28, gap=0)   # horizonte de 28 dias
for train_idx, test_idx in tscv.split(X):
    ...  # ajuste em X[train_idx]; erro por passo à frente em X[test_idx]
```

## 8. Checklist de séries (8 itens, V-14)

1. Horizonte e decisão definidos (o horizonte de avaliação é o da decisão).
2. Origem rolante com tipo de janela declarado.
3. Covariáveis **conhecidas na origem**; covariáveis futuras só se forem planejadas e disponíveis na decisão (calendário, preço planejado).
4. Dados "como eram conhecidos na época" (point-in-time), inclusive revisões de dados.
5. Baseline **sazonal-naive** nas mesmas dobras (política de revisão do plugin, não necessidade estatística).
6. **MASE** (MAPE é fraco perto de zero) e erro por horizonte.
7. Cobertura empírica do intervalo (por exemplo, 80%) por horizonte.
8. Retreino vs modelo congelado espelhando a produção.

Bloqueadores: split aleatório em dado temporal; janela ou estatística que usa o futuro (`rolling(center=True)`, `shift(-n)`). Fuso horário e horário de verão: Não verificado (veio de snippet).

## 9. Previsão com LLM

Para modelo de linguagem prevendo eventos: inclua o timestamp "as-of" no prompt e filtre o corpus por data. **Não** afirme ausência de vazamento por comparar desempenho antes e depois da data de corte: o controle não separa recência de memorização (Inferido do abstract de arXiv 2608.02985; segundo trabalho citado: arXiv 2506.00723, apenas existência conferida).

## 10. Evidência empírica: só corrobora

Ablação da feature suspeita, concentração de importância e queda no hold-out temporal reforçam a hipótese, mas **não provam ausência**. "AUC alto" não prova vazamento; "AUC baixo depois da correção" também não prova que o desenho esteja certo. Registre o que foi medido e o que é indício.

## 11. Severidade e saída

- **blocker**: vazamento com frase de ordem temporal confirmada, split sem tempo/grupo quando deveria, teste usado em escolha.
- **high**: plausível mas sem prova (vira "high + pergunta"), duplicatas não checadas, agregados com janela ambígua.
- **medium**: risco menor ou higiene (seed ausente, duplicatas improváveis).

Saída: `assets/templates/relatorio-auditoria-vazamento.md`. Cada achado: `[sev] título | classe | arquivo:linha | frase de ordem temporal | direção do viés | correção`. Inclua "Não verificado".

Limitações: a escala de severidade da fonte não tem critérios completos (V-13); a daqui é do plugin. A skill de terceiros usa `LogTransform` sem importar numpy (exemplos não rodam como estão).
