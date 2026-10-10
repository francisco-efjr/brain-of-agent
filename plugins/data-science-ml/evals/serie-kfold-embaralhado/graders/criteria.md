---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta `KFold(shuffle=True)` em dados diários ordenados no tempo como bloqueador: dias vizinhos (e o futuro) ficam no treino e o teste é interpolação, não previsão; diz que o MAPE de 3% não vale como estimativa do desempenho em produção.
2. Aponta `rolling(7, center=True)` como uso de dias futuros (a janela centrada inclui 3 dias após a linha) e, por isso, vazamento temporal na feature `media_7d`; pode notar, como ponto adicional e não obrigatório, que `lag_1` não existe na origem quando a decisão é tomada 14 dias antes do dia previsto.
3. Propõe origem rolante ou `TimeSeriesSplit` com treino só no passado, avaliação no horizonte da decisão (14 dias), covariáveis conhecidas na origem (promoção e feriado só se forem planejados com antecedência) e declara se o modelo será retreinado ou congelado.
4. Propõe baseline sazonal-naive nas mesmas dobras (por exemplo, o valor de 7 dias antes) para comparar com o modelo e com a planilha atual, e erro por horizonte.
5. Recomenda MASE (ou outra métrica robusta a zeros) no lugar do MAPE, citando os dias de venda zero como problema do MAPE; menciona que há 120 lojas (agrupar por loja ou avaliar por loja) e cobertura de intervalo se houver previsão probabilística.
6. Não libera a produção, não apresenta métrica corrigida como resultado e não afirma ter executado código; separa o que foi lido no código do que precisa ser medido.
FAIL if qualquer um ocorrer: aprova o MAPE de 3%; não identifica a janela centrada; recomenda apenas ajustar hiperparâmetros; afirma execução.
