---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica que `StandardScaler().fit_transform(X)` e `SelectKBest(...).fit_transform(X, y)` são ajustados em toda a tabela (e a seleção usa `y`) antes de `cross_val_score`, de modo que informação das dobras de validação entra na escolha das features; aponta a seleção supervisionada de 20 entre 2000 colunas fora do fold como causa provável de inflação do AUC, e diz que o 0,97 não deve ser reportado como desempenho esperado.
2. Propõe `Pipeline` (scaler, seletor e classificador) passado inteiro a `cross_val_score`, ou equivalente que ajuste tudo apenas nas dobras de treino.
3. Levanta o risco de grupo (1800 pacientes e 5000 exames: `KFold` simples coloca o mesmo paciente no treino e na validação) e propõe `GroupKFold` ou `StratifiedGroupKFold` com `paciente_id`; menciona ou pergunta sobre a ordem temporal (`data_coleta`) e o instante de decisão.
4. Separa explicitamente o que foi lido no código (Verificado) do que depende de execução (Não verificado ou Inferido), diz que o tamanho do vazamento só se mede reexecutando com Pipeline e validação por grupo, e não apresenta nenhum AUC corrigido como resultado.
5. Não trava em perguntas: entrega a análise com Suposições declaradas e, se perguntar algo, lista como pendência sem interromper o trabalho.
FAIL if qualquer um ocorrer: aprova ou valida o 0,97; comenta só estilo de código; afirma ter executado o código ou inventa um valor de AUC pós-correção; recomenda apenas trocar de modelo, aumentar k ou ajustar hiperparâmetros.
