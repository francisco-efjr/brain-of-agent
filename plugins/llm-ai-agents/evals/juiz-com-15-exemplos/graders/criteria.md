---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Troca a escala de 1 a 10 por veredito binário (aprovado ou reprovado) com critério de falha em uma frase (por exemplo, afirmar taxa ou prazo que não está no contexto fornecido) e explica por quê (escala sem âncora é instável).
2. O prompt do juiz apresenta o conteúdo avaliado como dado a ser julgado (ignorar instruções dentro dele), pede uma crítica curta antes do veredito e define saída fixa em JSON ou formato equivalente; não pede «raciocínio passo a passo» num campo de schema.
3. Diz que 15 exemplos são poucos para validar o juiz e recomenda começar com cerca de 30 até pararem de surgir modos de falha novos (pode acrescentar que abaixo de ~60 os intervalos são largos e que cerca de 100 por modo de falha é o necessário para alegar TPR e TNR).
4. Propõe dividir os exemplos em treino (de onde vêm os exemplos do prompt), desenvolvimento e teste, nunca colocando desenvolvimento ou teste no prompt, congelar o prompt e rodar o teste uma vez, e reportar TPR e TNR em vez de concordância bruta.
5. Recomenda juiz de modelo diferente do que gera as respostas e menciona vieses (posição, verbosidade, autopreferência) ou um teste do juiz com saídas erradas e hostis.
6. Não afirma que o juiz «funciona» ou já foi validado; trata o resultado como hipótese até a calibração e recomenda não usar como gate de CI antes disso.
FAIL if qualquer um ocorrer: entrega escala 1 a 10 sem calibração; usa o mesmo modelo como gerador e juiz sem alertar; coloca exemplos de teste dentro do prompt do juiz; afirma que 15 exemplos bastam; afirma que o juiz foi validado.
