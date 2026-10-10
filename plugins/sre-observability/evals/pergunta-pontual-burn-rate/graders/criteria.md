---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Informa o burn rate 14,4 para a janela de 1 hora (consumo de 2% do orçamento) e o limiar de taxa de erro de cerca de 1,44% (14,4 x 0,1%), com a conta mostrada (por exemplo 0,02 x 720 h / 1 h = 14,4).
2. Menciona que a página só dispara com a janela curta de 5 minutos também violada (par de janelas em AND), ou que a janela curta é a longa dividida por 12.
3. Avisa que os números valem para 99,9% em 30 dias e devem ser recalculados para outro SLO.
4. É proporcional: a resposta tem no máximo cerca de 25 linhas, sem relatório com muitas seções, sem handoff, sem matriz de aplicabilidade e sem anunciar o modo SRE-COMPLETO.
5. Não afirma ter executado ou validado regra alguma no Prometheus; se oferecer a regra PromQL, diz que seria rascunho a validar com promtool.
FAIL if qualquer um ocorrer: resposta com taxa de erro ou burn rate aritmeticamente errado; omite a conta; produz relatório longo ou handoff para uma pergunta pontual; ativa o modo SRE-COMPLETO; afirma que a regra foi validada.
