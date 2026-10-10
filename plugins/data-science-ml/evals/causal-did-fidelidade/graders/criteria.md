---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não confirma causalidade: diz que a evidência apresentada (antes e depois, 3 tratadas contra 20) não basta para afirmar que o programa causou o aumento, e usa linguagem associativa ("associado a") para a conclusão atual.
2. Registra como pergunta pendente, sem travar o restante da resposta, o estimando (efeito em quem, em qual janela) e como as 3 lojas foram escolhidas (se escolhidas por desempenho, localização ou conveniência, há viés de seleção); pode pedir confirmação do grafo causal com confundidores (sazonalidade, promoção de abril, características de Campinas).
3. Propõe diferença em diferenças e nomeia as premissas: tendências paralelas (checadas em vários períodos pré-lançamento, não só nas 8 semanas) e ausência de antecipação; observa que a promoção de abril em todas as lojas é um evento comum e precisa de tratamento (efeito pode ser diferente entre tratadas e controles).
4. Alerta que com apenas 3 lojas tratadas o erro-padrão agrupado por loja é instável e a inferência é frágil; sugere controle sintético, inferência por permutação ou randomização, ou expandir o desenho (por exemplo, expansão escalonada com sorteio) como alternativas.
5. Planeja ao menos um teste de refutação ou sensibilidade (data falsa de lançamento, loja ou período placebo, pré-tendência) e o que mudaria a conclusão.
6. Não inventa números adicionais nem afirma ter executado análise; diz o que precisa dos dados brutos para fazer.
FAIL if qualquer um ocorrer: afirma que o programa causou os 12%; trata o +12% menos +1% como efeito causal confirmado; recomenda expandir com base só nessa comparação; afirma ter rodado código.
