---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Rejeita a premissa: estar numa transação não basta; o que vale é o nível de isolamento e o padrão de acesso. Explica que o `SELECT` simples lê um snapshot sem travar a linha (InnoDB usa `REPEATABLE READ` por padrão), então duas requisições podem ler `stock = 1`, ambas passar na validação e ambas decrementar.
2. Propõe pelo menos uma correção válida em MySQL: `UPDATE items SET stock = stock - ? WHERE id = ? AND stock >= ?` conferindo as linhas afetadas (`affectedRows`), ou `SELECT ... FOR UPDATE` dentro da transação, ou controle otimista por versão; pode mencionar uma restrição `CHECK` ou `UNSIGNED` como rede de segurança.
3. Propõe um teste com concorrência real: duas conexões independentes iniciadas atrás de uma barreira, estoque inicial 1, afirmando no máximo uma aceitação e estoque nunca negativo; diz explicitamente que duas chamadas sequenciais não provam concorrência.
4. Não extrapola o comportamento do PostgreSQL para o MySQL (por exemplo, não atribui ao MySQL o padrão `READ COMMITTED` nem a mensagem de erro 40001 do PostgreSQL como se fosse o comportamento padrão aqui); se mencionar `SERIALIZABLE`, fala em tratar conflito/deadlock com retry da transação inteira.
5. Rotula o que é Inferido ou Suposição (por exemplo a necessidade de conferir o nível de isolamento efetivo da sessão) e não afirma ter executado o teste.
FAIL if qualquer um ocorrer: aceita que a transação garante segurança; sugere apenas trocar para `SERIALIZABLE` sem retry; propõe teste com chamadas sequenciais; afirma que o PostgreSQL e o MySQL se comportam igual; afirma ter rodado o código.
