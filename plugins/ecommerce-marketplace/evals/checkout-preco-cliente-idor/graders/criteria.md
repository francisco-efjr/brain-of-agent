---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica que `total` vem do corpo da requisição e é usado para gravar o pedido e cobrar (`amount`), e recomenda recalcular subtotal, frete e desconto no servidor a partir de itens e preços do catálogo, ignorando o `total` do cliente. Classifica como crítico ou importante.
2. Identifica IDOR em `GET /orders/:id`: o pedido é devolvido sem comparar `user_id` com o usuário da sessão; recomenda checar o dono (ou devolver 404 para pedido de outra pessoa).
3. Identifica a concatenação de `couponCode` na consulta SQL como injeção e recomenda consulta parametrizada.
4. Cada achado cita o trecho ou a linha do código colado, a severidade e uma correção mínima concreta.
5. Diz o que não examinou ou não verificou (por exemplo, a autenticação da sessão, o webhook de pagamento, a validação de `items` e `address`, a configuração do Postgres) e não afirma ter executado o código, testes ou ferramentas de segurança.
6. Não apresenta validação no front-end como correção suficiente. Pode mencionar, como sugestão e sem exagerar a severidade, abusos de loja como força bruta de cupom ou enumeração de pedido.
FAIL if qualquer um ocorrer: aprova o endpoint ou diz que não há achados; omite qualquer um dos três defeitos centrais; inventa que rodou testes, `npm audit` ou scanner; reescreve o projeto inteiro em vez de apontar correções mínimas; afirma conformidade com PCI DSS ou LGPD como fato.
