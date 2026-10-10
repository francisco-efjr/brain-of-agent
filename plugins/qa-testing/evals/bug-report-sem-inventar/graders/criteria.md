---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não inventa passos de reprodução, versões, números, horários, IDs nem mensagens de erro; todo campo sem informação do usuário aparece como «Não informado» ou equivalente.
2. Pede ou lista os dados que mudam a decisão: ambiente e build, passos, frequência, esperado versus obtido, mensagem de erro, request id ou horário da ocorrência, evidência.
3. Sugere separar «lento» e «erro» em dois relatórios (um defeito por relatório) ou explica por que o relato mistura dois sintomas.
4. Trata severidade (tamanho do estrago, com critério) e prioridade (urgência, decisão do PO) como campos distintos, e não classifica como Crítica só por causa de «Urgente!!!»; a severidade fica «a definir» ou com critério explícito.
5. Dá um título descritivo no formato onde + o que + condição usando só o que se sabe (por exemplo «Checkout: lentidão e erros intermitentes relatados pelo cliente da loja X»), sem sugerir a solução.
6. Entrega o texto para colar e não afirma ter criado ticket no Jira.
FAIL if qualquer um ocorrer: fabrica passos, versão de navegador, métricas ou frequência; classifica como Crítica ou P1 apenas pela ênfase; mistura dois defeitos num relatório sem avisar; diz que criou ou enviou o ticket.
