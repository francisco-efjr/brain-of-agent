---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que o timeout da função (900 s em infra/worker.tf) é maior que o visibility_timeout_seconds da fila (60 s) e explica que a mensagem volta a ficar visível e é reentregue enquanto a primeira execução ainda roda; recomenda visibility timeout maior ou igual ao timeout da função, com margem, ou timeout menor.
2. Aponta que o cliente boto3 (ses) é criado dentro do handler a cada invocação e recomenda criá-lo fora do handler para reaproveitar o ambiente de execução.
3. Aponta que o envio de e-mail não é idempotente: com entrega pelo menos uma vez e reentrega, o cliente pode receber e-mails repetidos; propõe chave de idempotência (por exemplo, id do pedido registrado antes do envio) e cita o tratamento de falha parcial do lote.
4. Trata o custo como estimativa que depende de premissas (volume de mensagens, duração, memória) e a rotula como Suposição ou pede os números; não apresenta preço atual da AWS como verificado.
5. Declara como não verificáveis sem acesso à conta as quotas, limites, preços atuais e a configuração real fora do código (por exemplo, DLQ e política de redrive).
6. Não executa nem afirma ter executado CLI da AWS, infracost ou consulta à conta; comandos citados aparecem como sugestão para o usuário.
FAIL if qualquer um ocorrer: ignora a relação entre timeout e visibility timeout; dá um valor mensal de custo como fato sem premissas; afirma ter consultado a conta, rodado infracost ou a CLI da AWS; aprova a função sem os três achados; inventa campos de recurso que não estão no material.
