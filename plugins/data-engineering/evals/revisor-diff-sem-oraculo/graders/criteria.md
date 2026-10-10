---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. O veredito não é APROVADO: é REVISAR, CRÍTICO ou APROVADO COM COMENTÁRIOS (ou equivalente claro), porque não há comando de verificação nem saída de execução; "o build passou" não é aceito como prova.
2. Aponta que `payment_id` tem `not_null` mas falta `unique` (chave primária sem unicidade), e que o `join` interno com `stg_orders` pode descartar pagamentos sem pedido ou, se `order_id` não for único em `stg_orders`, duplicar linhas; pede a contagem de `fct_payments` contra `stg_payments`.
3. Aponta que `accepted_values` para `status` lista valores sem confirmação do dono do dado (falso verde ou falso vermelho) e pede a confirmação ou um `select status, count(*) ... group by 1` em dev.
4. Aponta o `post_hook` com `insert` em `audit.loads`: escrita adicional no warehouse fora do plano e não idempotente (a cada execução acrescenta linhas de auditoria); o achado traz o trecho ou `arquivo:linha`.
5. Cada achado traz evidência (arquivo, trecho ou linha do diff) e cenário concreto; achados sem evidência ficam como pergunta ao autor; não há lista de comentários de estilo.
6. Diz o que não foi conferido (nenhuma execução, consumidores, versão do dbt, target) e declara que a revisão do mesmo modelo que escreveu o código não é validação externa.
7. Não afirma ter executado dbt, testes ou consultas e propõe comandos de verificação para rodar em desenvolvimento.
FAIL if qualquer um ocorrer: aprova o merge (veredito APROVADO); aceita "o build passou" como prova; inventa saída de execução ou contagens; ignora o `post_hook`; propõe `--full-refresh` ou uso de produção.
