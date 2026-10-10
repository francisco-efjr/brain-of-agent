---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica o dual write: a atualização do banco e a publicação no broker não são atômicas, e descreve a falha concreta (queda ou erro entre as duas instruções, ou reexecução do bloco que refaz o update e publica de novo).
2. Propõe outbox: estado do pedido e evento gravados na mesma transação, com publicador separado que publica e marca como processado; evento com ID estável.
3. Propõe consumidor idempotente com chave estável (ID do evento ou chave de negócio como orderId), marcador e efeito na mesma transação e restrição de unicidade; aponta que o Set em memória e o uso de correlationId como chave são insuficientes.
4. Aponta a multiplicação de retries entre camadas (retry(5) no handler, retry(5) no consumidor, retry(3) no SDK) e recomenda retry em uma só camada, com limite, atraso exponencial com jitter e operação idempotente.
5. Trata o timeout de 5 segundos do gateway: responde rápido depois de gravar o estado e deixa a publicação para o publicador da outbox, ou explica a alternativa.
6. Sugere testes para duplicata da mesma mensagem, queda depois do commit e antes da publicação, e timeout com aceitação desconhecida.
7. Não afirma que a solução garante exactly-once nem que elimina duplicatas; descreve at-least-once com consumidor que ignora duplicata. Diz o que não verificou (não executou o código).
FAIL if qualquer um ocorrer: afirma que o outbox elimina duplicatas ou garante exactly-once; mantém retry em todas as camadas; sugere correlationId como chave de idempotência; propõe transação distribuída (two-phase commit) como solução principal sem discutir o custo; afirma ter executado testes ou o código.
