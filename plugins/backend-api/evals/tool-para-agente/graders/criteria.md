---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Propõe consolidar por fluxo de negócio (por exemplo buscar pedidos de um cliente com filtro, obter status de entrega, cancelar pedido condicional) em vez de espelhar tabelas, e elimina ou restringe a tool que devolve tudo.
2. Usa nomes com prefixo de serviço ou recurso (por exemplo `orders_search`, `orders_cancel`) e parâmetros sem ambiguidade (`customer_id`, `order_id`).
3. Propõe resposta enxuta com modo `concise` e `detailed` mantendo os IDs para a chamada seguinte, mais paginação, filtros, limite padrão e dica de como refinar quando truncar.
4. Propõe erro acionável que diz o que corrigir e mostra exemplo de entrada válida, no lugar de `Error 500`.
5. Propõe descrição com quatro partes (o que faz e retorna, quando usar, quando não usar, efeito dos parâmetros e limites) e, nas tools que mudam estado (cancelamento), schema estrito (`strict`, `additionalProperties: false`, enums fechados, `required` explícito) e anotações de MCP como `readOnlyHint` para as de leitura e `destructiveHint` para a de cancelamento.
6. Propõe avaliação com cerca de 10 perguntas independentes, somente leitura, realistas e verificáveis, medindo acerto, número de chamadas, tokens e erros, e rotula como desenhada e não executada.
7. Não inventa números de melhoria e não apresenta o limite de 25.000 tokens como regra geral de qualquer cliente.
FAIL if qualquer um ocorrer: apenas renomeia as tools; mantém retorno gigante; mantém `Error 500` como erro; afirma ter medido ou testado; inclui chamadas a provedor diferente do usado sem necessidade.
