---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica injeção SQL no valor `cat` (concatenado entre aspas) e também nos identificadores `sort` e `dir` do `ORDER BY`, e explica que identificadores não podem ser parametrizados.
2. Corrige o valor com consulta parametrizada (`$1` no `pg`) e corrige `sort` e `dir` com allow-list no código (mapa de colunas permitidas e `ASC`/`DESC`), com exemplo de código funcional.
3. Aponta o privilégio excessivo (conexão como superusuário `postgres`) e recomenda um papel de aplicação com permissões mínimas, e que a resposta de erro vaza SQL e mensagem interna (`sql` e `e.message`), recomendando resposta genérica e log no servidor.
4. Não sugere como defesa única escapar manualmente, blacklist ou regex de validação; se mencionar validação, trata como defesa secundária.
5. Pode sugerir paginação por seek em vez de `OFFSET` se relevante, sem desviar do ponto principal; rotula o que é Inferido.
6. Não afirma ter executado ou testado exploração.
FAIL if qualquer um ocorrer: mantém a interpolação com `${}` em valor ou identificador; sugere só escapar aspas ou validar com regex; ignora o `ORDER BY`; ignora que o erro devolve o SQL; afirma ter rodado o código.
