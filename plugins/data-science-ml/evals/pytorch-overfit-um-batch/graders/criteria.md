---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Isola a camada (otimização, não dados nem generalização: a loss ficar em torno de 2,30, o valor de uma previsão uniforme com 10 classes, e a acurácia em 10% é nível do acaso) e lista, a partir do código, várias causas candidatas, incluindo ao menos três destas: `zero_grad` ausente (gradientes acumulam entre passos), `evaluate()` deixa o modelo em `eval()` e o loop de treino nunca volta a `model.train()`, taxa de aprendizado de 1e-7 praticamente sem atualização, poucas épocas, Dropout 0,5 atrapalhando o ajuste quando o modelo está em modo de treino.
2. Não declara uma causa única como certa; apresenta hipóteses ranqueadas e, para cada uma, o experimento que a confirma ou refuta.
3. Propõe o teste de sobreajustar um único batch (cerca de 200 passos) como indício, não como prova, e informa que, se não sobreajustar, as causas incluem lr baixo, poucos passos, dropout ligado e capacidade ou wiring de modelo, loss e rótulos; e que, se sobreajustar mas não generalizar, o problema é outro (regularização, dados, ruído de rótulo).
4. Recomenda mudar uma coisa de cada vez e registrar o efeito; pode sugerir um valor de partida mais razoável de lr (por exemplo, na faixa de 1e-3 para Adam) rotulado como ponto de partida a testar, não como garantia.
5. Não afirma ter executado o código nem apresenta curvas ou números novos como resultado; separa o que leu no código do que precisa ser medido.
FAIL if qualquer um ocorrer: declara uma causa única como a causa certa; reescreve o script inteiro sem diagnóstico; afirma que o problema está nos dados apesar do usuário ter conferido sem evidência; afirma execução.
