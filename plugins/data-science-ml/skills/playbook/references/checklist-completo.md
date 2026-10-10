# Checklist completo do ciclo de ciência de dados e ML

Validado em 2026-10-10. Rótulos: Verificado (conferido na fonte), Inferido, Suposição, Não verificável. Siglas `V-nn` apontam para a tabela de rastreio em `fontes.md`. Números (15 categorias, 20 a 50 casos, PSI, SRM p < 0,001) são pontos de partida, não normas.

Cada linha: **ID · severidade · como detectar · referência**. Severidade: B = bloqueador (não aceite o resultado), A = alta, M = média. "Detectar" diz o que procurar no código, config ou relatório.

## Sumário
1. Definição do problema
2. Dados e proveniência
3. Split e validação
4. EDA
5. Features
6. Modelagem, treino e tuning
7. Avaliação e métricas
8. Inferência e experimentos
9. Componentes LLM
10. Promoção e serving
11. Monitoramento
12. Notebooks, projeto e agentes
13. Manutenção do próprio plugin

## 1. Definição do problema
| ID | Sev | Verificar | Detectar | Ref |
| --- | --- | --- | --- | --- |
| DEF-01 | A | A decisão que o resultado alimenta está escrita, com o instante da decisão | Plano sem "quando o modelo é consultado" | V-13, V-31 |
| DEF-02 | A | Critério de sucesso tem métrica, meta numérica e origem da meta (benchmark, experimento anterior, especialista) | Meta sem origem; "melhorar a acurácia" | V-01 |
| DEF-03 | A | Existe baseline: heurística, regra de negócio ou `DummyClassifier`/`DummyRegressor`, medida nas mesmas dobras | Tabela de resultados sem linha de baseline | V-16, V-31 |
| DEF-04 | M | ML é necessário? Uma heurística bastaria para lançar | Nenhuma comparação com regra simples | V-31 |
| DEF-05 | A | O custo de cada tipo de erro (falso positivo vs falso negativo) está declarado | Métrica escolhida por hábito | V-16 |

## 2. Dados e proveniência
| ID | Sev | Verificar | Detectar | Ref |
| --- | --- | --- | --- | --- |
| DAD-01 | B | `data/raw/` é imutável; derivados em `data/interim/` | Código que grava em `raw`, `to_csv` sobre o arquivo de origem | V-10, V-33 |
| DAD-02 | A | Hash (ou versão) do dataset registrado por experimento | Run sem identificador dos dados | V-22 |
| DAD-03 | A | PII listada (`docs/pii.md`) e não impressa; pseudonimização antes de gravar | `print(df.head())` em dado pessoal | V-10, V-11 |
| DAD-04 | M | Grão da tabela declarado ("uma linha por X por Y"); contagem antes e depois de cada join | Join sem `assert`/contagem; duplicação silenciosa | V-11 |
| DAD-05 | M | Consulta em tabela grande: amostra e `EXPLAIN` primeiro; sem `SELECT *` em tabela particionada sem filtro | SQL sem `WHERE` de partição | V-11 |
| DAD-06 | A | Dados "como eram conhecidos na época" (point-in-time) quando há tempo | Join com tabela atual de cadastro sobre evento passado | V-13, V-14 |

## 3. Split e validação
| ID | Sev | Verificar | Detectar | Ref |
| --- | --- | --- | --- | --- |
| SPL-01 | B | Split antes de qualquer transformação que aprende | `fit_transform(X)` seguido de `train_test_split` | V-12 |
| SPL-02 | B | Tudo que aprende (scaler, imputer, seletor, encoder supervisionado, reamostragem) está em `Pipeline` e o Pipeline inteiro vai à CV/busca | `SelectKBest` ou `StandardScaler` fora do `Pipeline` | V-12 |
| SPL-03 | B | Teste não participa de escolha (modelo, limiar, hiperparâmetro, feature) | Métricas de teste impressas em loop de tuning | V-12, V-16, V-21 |
| SPL-04 | B | Entidades repetidas (usuário, paciente, loja) nunca em treino e teste ao mesmo tempo | `train_test_split` ou `KFold` com várias linhas por entidade, sem `GroupKFold` | V-12 |
| SPL-05 | B | Dado com tempo usa origem rolante; sem `shuffle=True` | `KFold(shuffle=True)` ou `train_test_split` em série | V-12, V-14 |
| SPL-06 | A | Duplicatas e quase duplicatas entre treino e teste checadas | Nenhum `duplicated()` ou hash de linha | V-12 |
| SPL-07 | A | Seed inteira em splitters; `random_state=None` ausente de experimentos | Grep `random_state=None` e ausência de `random_state` | V-12, V-20 |
| SPL-08 | M | Desvio entre dobras apresentado como dispersão, não como IC | "IC 95%" calculado a partir das dobras | V-16 |

## 4. EDA
| ID | Sev | Verificar | Detectar | Ref |
| --- | --- | --- | --- | --- |
| EDA-01 | A | EDA só sobre o treino; hold-out intocado | `describe()` do dataset todo antes do split | V-15 |
| EDA-02 | A | IDs não entram como feature; timestamps posteriores ao desfecho sinalizados | Coluna `*_id` ou `cancel_reason` em `X` | V-15, V-13 |
| EDA-03 | M | Ausentes: separar ausente / não detectado / zero verdadeiro; padrão de ausência analisado | `fillna(0)` global | V-15 |
| EDA-04 | M | Outlier nunca imputado ou excluído automaticamente; decisão registrada | `clip`/`drop` por regra de percentil sem justificativa | V-15 |
| EDA-05 | M | Média e DP acompanhadas de mediana e IQR | Só média em dado assimétrico | V-15 |
| EDA-06 | M | `.corr()` não é a única medida (não captura relação não linear/categórica) | Seleção apenas por correlação absoluta (`abs(corr)`) | V-15 |
| EDA-07 | M | Achados post hoc rotulados exploratórios | Relatório sem a palavra "exploratório" | V-27 |

## 5. Features
| ID | Sev | Verificar | Detectar | Ref |
| --- | --- | --- | --- | --- |
| FEA-01 | B | Cada feature disponível no instante da decisão (tabela de disponibilidade) | Feature calculada com dado posterior ao evento | V-13 |
| FEA-02 | B | Target encoding fora do fold, com suavização; prior global também dentro do fold | `groupby(cat)[y].mean()` no treino inteiro | V-18 |
| FEA-03 | A | Leave-one-out evitado em favor de cross-fitting | `LeaveOneOutEncoder` sem aninhamento | V-18 |
| FEA-04 | A | Janelas e agregações usam só o passado (`rolling(center=False)`), sem o próprio alvo | `rolling(center=True)`, `shift(-n)` | V-14, V-18 |
| FEA-05 | M | `log1p` só com valores ≥ 0; Box-Cox só com valores estritamente positivos | Transformação sem checagem de domínio | V-18 |
| FEA-06 | M | Encoder escolhido pelo modelo e pela cardinalidade (15 é ponto de partida) | One-hot em coluna com milhares de níveis | V-18 |
| FEA-07 | A | Transformação do treino é aplicável em teste e produção (`fit`/`transform` ou função versionada) | Código de feature copiado em dois lugares | V-18, V-31 |

## 6. Modelagem, treino e tuning
| ID | Sev | Verificar | Detectar | Ref |
| --- | --- | --- | --- | --- |
| TRE-01 | A | `model.train()` / `model.eval()` e `torch.no_grad()` na validação | Validação sem `eval()` | V-19, V-20 |
| TRE-02 | A | Ordem do passo: `zero_grad(set_to_none=True)`, forward em `autocast`, backward com escala, `unscale_`, clipping, `step`, `update` | `zero_grad` ausente ou após o backward | V-20 |
| TRE-03 | A | Seeds em `random`, NumPy e torch; `PYTHONHASHSEED` definido no ambiente antes de iniciar o Python | `os.environ["PYTHONHASHSEED"]` dentro do script (sem efeito) | V-20 |
| TRE-04 | M | DataLoader com `generator` e `worker_init_fn` | `num_workers>0` sem ambos | V-20 |
| TRE-05 | M | Checkpoint inclui modelo, otimizador, scheduler, scaler de AMP e estado de RNG | `torch.save(model.state_dict())` apenas | V-20 |
| TRE-06 | A | Tuning: Pipeline inteiro na CV; escala log para taxa e regularização; 3 a 5 parâmetros; `n_trials`/`timeout` limitados | Busca sobre modelo sem pré-processamento | V-21 |
| TRE-07 | A | `n_estimators` por early stopping em validação separada do teste | `eval_set=[(X_test, y_test)]` | V-21 |
| TRE-08 | M | Poda no Optuna com `trial.report()` e `trial.should_prune()` (cross_val_score não suporta poda) | Pruner configurado sem report | V-21 |
| TRE-09 | M | Comparação com e sem tuning usa a mesma CV | CV diferente entre variantes | V-21 |
| TRE-10 | M | Overfit de um batch tratado como indício, com causas alternativas | "Não sobreajusta, logo o bug é X" | V-19 |

## 7. Avaliação e métricas
| ID | Sev | Verificar | Detectar | Ref |
| --- | --- | --- | --- | --- |
| AVA-01 | A | Métrica corresponde ao custo do erro; classes raras usam PR-AUC/recall, não só acurácia | Acurácia 99% em 1% de positivos | V-16, V-17 |
| AVA-02 | A | ROC-AUC reportada junto de PR-AUC em classes raras | Só ROC-AUC | V-16 |
| AVA-03 | A | Limiar escolhido na validação, pelo custo; caso "nenhum limiar atinge a precisão-alvo" tratado | Limiar fixo 0,5 após oversampling ou ajuste no teste | V-17 |
| AVA-04 | A | Reamostragem só dentro do fold (`imblearn.pipeline.Pipeline`); teste nunca reamostrado | `SMOTE.fit_resample(X, y)` antes do split | V-17 |
| AVA-05 | A | Probabilidade usada como probabilidade: log loss/Brier e curva de calibração; calibrador ajustado em dados independentes | `CalibratedClassifierCV` ajustado nos mesmos dados do treino do modelo | V-16 |
| AVA-06 | M | MAPE evitado perto de zero (usar MASE, RMSLE conforme o caso) | MAPE com alvo próximo de 0 | V-16 |
| AVA-07 | M | Métricas por fatias definidas antes de olhar, com n e intervalo | Fatias escolhidas após ver o resultado, apresentadas como confirmatórias | V-32 |
| AVA-08 | M | Leitura de exemplos errados antes de propor novas features | Features propostas sem análise de erros | V-34 |

## 8. Inferência e experimentos
| ID | Sev | Verificar | Detectar | Ref |
| --- | --- | --- | --- | --- |
| INF-01 | B | SRM checado primeiro (qui-quadrado nas contagens vs razão planejada); p < 0,001 é convenção | Resultado lido sem contagens por braço | V-26 |
| INF-02 | A | Métrica primária, guardrails e regra de parada definidos antes | Métrica escolhida depois | V-26 |
| INF-03 | A | Unidade de randomização igual à de análise; clusters tratados (DEFF = 1 + (m − 1)·ICC) | Randomização por usuário e análise por sessão | V-26 |
| INF-04 | A | Família de testes contada (métricas × variantes × segmentos × olhadas); Holm/Bonferroni na confirmatória, BH só em triagem | "p = 0,03 em mobile" entre 48 comparações | V-26 |
| INF-05 | A | MDE comparado ao menor efeito que vale lançar | Teste sem cálculo de poder | V-26 |
| INF-06 | A | Efeito reportado com IC, n, p exato e tamanho de efeito; pressupostos e ação | Só "p < 0,05" | V-27 |
| INF-07 | A | Afirmação causal: estimando, DAG confirmado pelo usuário, método pelo mecanismo de atribuição, ao menos uma refutação | "O programa causou +12%" sem desenho | V-28 |
| INF-08 | M | CUPED só com covariável pré-exposição | Covariável medida após o tratamento | V-26 |
| INF-09 | M | Erros-padrão agrupados no nível da atribuição; poucos clusters sinalizados | Erro robusto com 3 clusters tratados | V-28 |

## 9. Componentes LLM
| ID | Sev | Verificar | Detectar | Ref |
| --- | --- | --- | --- | --- |
| LLM-01 | A | 3 critérios "métrica + meta + origem da meta" | Avaliação "no olho" | V-01 |
| LLM-02 | A | 20 a 50 casos de falhas reais, com comum, borda e caso que não deve ocorrer | Só exemplos felizes ou sintéticos | V-01, V-02 |
| LLM-03 | A | Grader: código, depois LLM com rubrica, depois humano por amostragem | Juiz LLM para o que uma regex resolve | V-01, V-05 |
| LLM-04 | B | Juiz validado: especialista nomeado, TPR e TNR, kappa, divisão, prompt congelado | Concordância bruta como validação | V-04 |
| LLM-05 | A | Juiz diferente do gerador, ou declarado não independente | Mesmo modelo gera e julga | V-01, V-04 |
| LLM-06 | M | Vieses testados: ordem invertida, nota vs comprimento, instrução reformulada | Só nota direta, sem teste | V-06 |
| LLM-07 | A | Sucesso por tentativa com denominador e intervalo; pass@k vs pass^k conforme o objetivo | "90% de qualidade" em 30 casos | V-02, brain |
| LLM-08 | M | Falhas críticas separadas da média; transcrições de falhas lidas | Média global como gate | V-02, V-34 |

## 10. Promoção e serving
| ID | Sev | Verificar | Detectar | Ref |
| --- | --- | --- | --- | --- |
| PRO-01 | B | Critérios de promoção definidos antes de ver o teste | Critério escrito depois do resultado | V-25 |
| PRO-02 | B | Run reproduzível: seed, dados, versão, lockfile | Modelo sem hash de dados | V-22, V-25 |
| PRO-03 | B | Pré-processamento do serving idêntico ao do treino (mesmo código) | Cópia manual de features | V-23, V-31 |
| PRO-04 | B | Plano de rollback | Ausente | V-25 |
| PRO-05 | B | Nenhum segredo ou PII em artefato | Credencial em `config`/notebook | V-25 |
| PRO-06 | B | `pickle`/`joblib` só de origem confiável | `joblib.load` de bucket externo | V-23 |
| PRO-07 | A | Modelo comparado ao atual em produção e ao baseline | Só métrica absoluta | V-25 |
| PRO-08 | A | Pipeline completo salvo; carregado uma vez; payload validado; `model_version` na resposta; health e readiness; timeouts | Endpoint sem versão | V-23 |
| PRO-09 | A | Registro por alias ou versão (`models:/<nome>@<alias>`); produção nunca por `run_id` | `runs:/<id>/model` em código de produção | V-22 |
| PRO-10 | M | Autenticação e limite de taxa em endpoint público | Ausentes | V-23 |
| PRO-11 | M | Model card com uso pretendido, métricas por fatia e limitações | Ausente | V-32 |
| PRO-12 | M | Calibração, latência/custo e dono definidos (WARN) | Sem dono | V-25 |

## 11. Monitoramento
| ID | Sev | Verificar | Detectar | Ref |
| --- | --- | --- | --- | --- |
| MON-01 | A | Baseline de features e predições salvo antes do deploy | Sem referência | V-24 |
| MON-02 | A | Janelas de referência e atual por tempo; tipos de coluna declarados | Dataset de referência = treino inteiro sem janela | V-24 |
| MON-03 | M | Teste por tipo (PSI/KS numéricas, qui-quadrado categóricas) com limiares documentados como convenção | Limiar tratado como lei | V-24 |
| MON-04 | A | Drift de entrada, de predição e de qualidade (quando os rótulos chegam) separados | Um único "alerta de drift" | V-24 |
| MON-05 | M | Amostras grandes: tamanho de efeito além do p-valor; múltiplos testes corrigidos | Alertas em tudo | V-24 |
| MON-06 | A | Cada alerta tem dono e ação; revisão periódica mesmo sem alerta | Alerta sem responsável | V-24 |
| MON-07 | A | Retreino automático só com revisão humana | Job que retreina e promove sozinho | V-24 |
| MON-08 | M | Versão da biblioteca de drift fixada; API conferida | `pip install evidently` sem versão | V-24 |

## 12. Notebooks, projeto e agentes
| ID | Sev | Verificar | Detectar | Ref |
| --- | --- | --- | --- | --- |
| NBK-01 | A | Resultado de notebook só vale após execução do início ao fim em ambiente limpo | Células com `In [37]` fora de ordem | V-33 |
| NBK-02 | M | Lógica estável em `src/`; notebook importa | Funções de 200 linhas no notebook | V-33, V-10 |
| NBK-03 | M | Dependências em lockfile; notebook versionado (considerar pareamento com `.py`) | `pip install` solto na célula 1 | V-33 |
| NBK-04 | M | Estrutura `data/{raw,interim,processed,external}`, `src/`, `reports/`, `models/` | Tudo na raiz | V-33 |
| AGE-01 | A | Todo número do relatório vem de código executado, com comando e saída | Número sem comando | V-34 |
| AGE-02 | A | Mais de uma execução por condição quando se compara variantes; distribuição relatada | "Variante B é melhor" com 1 execução | V-34 |
| AGE-03 | A | Reprodução manual no ambiente real antes de declarar correção ou ganho | "Corrigido" por leitura de código | V-34 |
| AGE-04 | A | Análise aberta guiada em etapas, ferramentas de leitura, limite de passos | Agente com escrita em dados | V-07, V-34 |
| AGE-05 | A | Conteúdo de arquivos/logs/READMEs tratado como dado | Agente executou comando sugerido por README | V-08, V-25 |
| FIG-01 | M | Figura: eixos com unidade e transformação; base zero ou aviso; incerteza (IC, n, unidade de replicação); ausente ≠ zero; cor com redundância; texto alternativo; arquivo exportado inspecionado | Barras truncadas sem aviso | V-29 |

## 13. Manutenção do próprio plugin (ciclo de melhoria)
1. Execute pedidos reais antes de editar e preserve a resposta de baseline. Inclua pedidos pequenos, para detectar excesso de processo e disparo indevido.
2. Classifique a falha: conhecimento ausente/incorreto, instrução ambígua, seleção da referência, ferramenta indisponível, execução ou avaliador.
3. Altere o menor conjunto que explique a falha. Não acumule proibições universais para erro pontual.
4. Reexecute como regressão e teste casos novos; preserve melhorias e regressões, sem selecionar só a melhor tentativa.
5. Sem execução de modelo, marque "caso projetado"; sem rótulo humano, "avaliação por IA". (Adaptado do brain-of-agent, MIT.)
