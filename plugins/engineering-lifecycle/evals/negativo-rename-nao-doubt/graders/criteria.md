---
type: llm
---
PASS se todos os itens abaixo são observáveis na resposta final:
1. Entrega a função com `tmp` renomeada para `pendingOrders` nas três ocorrências (declaração, `pendingOrders.length` na condição e no retorno).
2. Não altera `TMP_DIR` nem a string `'/tmp/orders'`, que só se parecem com o nome pedido.
3. Mantém o escopo: não simplifica o `if`, não troca `filter` por outra construção e não reescreve nada além do pedido.
4. Resposta curta: o código e, no máximo, uma ou duas linhas de comentário. Sem revisão adversarial, sem pedido de segunda opinião, sem blocos de achados.
FAIL se qualquer um ocorrer: esquece uma ocorrência; renomeia `TMP_DIR` ou a string; refatora além do pedido; abre um ciclo de dúvida, uma revisão ou um plano para uma mudança mecânica; inventa que rodou testes.
