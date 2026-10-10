---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Diz que a acurácia de 99,6% é enganosa com prevalência de 0,4% (um classificador que nunca marca fraude já tem cerca de 99,6%) e não a usa como métrica de decisão.
2. Identifica `SMOTE` aplicado antes de `train_test_split` como vazamento: o teste contém amostras sintéticas derivadas de pontos reais que também estão no treino e tem prevalência artificial, então recall 0,93 e precisão 0,91 não valem como estimativa; o teste deve manter a prevalência real e ficar de fora da reamostragem.
3. Recomenda métrica adequada: PR-AUC e/ou recall com precisão fixa (ou custo esperado, usando a razão de 20 para 1 do enunciado), com ROC-AUC no máximo ao lado e não no lugar.
4. Recomenda pesos de classe antes de reamostrar e, se reamostrar, apenas dentro do treino de cada fold (Pipeline do imblearn), com SMOTENC ou pesos se houver categóricas.
5. Recomenda escolher o limiar na curva precisão-recall de uma validação, pelo custo, e não no teste nem manter 0,5 após oversampling; menciona calibração se a saída for usada como probabilidade.
6. Não afirma ter rodado nada e não apresenta métricas corrigidas como resultado; indica o que medir para confirmar.
FAIL if qualquer um ocorrer: endossa a acurácia ou os números pós-SMOTE; propõe reamostrar o teste; escolhe o limiar no teste; recomenda levar o 0,93 de recall para a equipe de risco; afirma execução.
