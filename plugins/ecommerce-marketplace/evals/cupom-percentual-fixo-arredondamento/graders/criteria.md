---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Move o cálculo de preço, desconto e frete para o servidor (ignora o `pricing` enviado pelo front) e usa valores em inteiros de unidade menor (centavos), sem `float`.
2. Percebe que a ordem entre o cupom percentual e o fixo muda o resultado e a torna explícita. Se apresentar os números do exemplo (itens A e B elegíveis, soma 160,00; C fora): percentual primeiro dá 144,00 e depois 124,00 (total de itens 164,00); fixo primeiro dá 140,00 e depois 126,00 (total de itens 166,00). Pergunta qual ordem vale ou escolhe uma, rotulada como decisão ou Suposição, e registra o ponto como decisão pendente do humano. Qualquer aritmética apresentada deve estar correta.
3. Define por escrito se o limite do frete grátis (R$ 170,00) é medido antes ou depois do desconto e mostra que, no exemplo, o resultado muda (subtotal de 200,00 antes do desconto; 164,00 ou 166,00 depois).
4. Rateia o desconto entre os itens elegíveis de modo que a soma dos descontos por item seja igual ao desconto total, com regra de resto para o centavo; parcelas em 3x somam exatamente o total, com regra de arredondamento escrita (por exemplo, o resto no último item) rotulada como decisão de projeto ou Inferido, não como norma.
5. Propõe testes parametrizados com um oráculo independente do código de produção (cálculo à mão ou planilha), cobrindo: carrinho de 3 itens com um fora da promoção; cupom duplicado; limite de frete grátis no valor exato e um centavo abaixo; soma das parcelas igual ao total.
6. Não afirma ter executado código ou testes, e não inventa regra de negócio que não foi dada.
FAIL if qualquer um ocorrer: mantém `float` ou número de ponto flutuante para dinheiro; continua confiando no total do cliente; escolhe a ordem dos cupons sem declarar; deixa parcelas que não somam o total; apresenta aritmética errada como certa; afirma ter rodado os testes.
