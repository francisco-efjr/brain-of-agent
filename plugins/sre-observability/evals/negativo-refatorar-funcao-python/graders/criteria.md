---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega uma versão mais legível da função (por exemplo compreensão de lista com nomes descritivos) que preserva o comportamento: devolve os quadrados dos números pares, na mesma ordem.
2. A resposta é curta e proporcional ao pedido.
3. Não menciona SLO, alertas, incidentes, testes de carga, observabilidade nem outros temas do plugin sre-observability.
FAIL if qualquer um ocorrer: muda o comportamento da função; transforma o pedido em revisão de confiabilidade; aciona skill ou agente do plugin sre-observability.
