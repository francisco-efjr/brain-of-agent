---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Os testes conferem o `total` contra um valor calculado à parte (por exemplo 2 x 24,95 + 1 x 12,00 = 61,90 como string decimal ou equivalente), e não copiam o esperado da resposta.
2. Verificam status exato (201 na criação, 400 sem chave, 422 para corpo divergente), não "2xx", e que a criação persistiu (um GET devolve o pedido).
3. Testam o replay: mesma `Idempotency-Key` e mesmo corpo devolvem o mesmo pedido e deixam um só pedido (conferido por listagem pela `referencia`); mesma chave com corpo diferente dá 422.
4. Testam erro de validação com `Content-Type` `application/problem+json` e comparam por `type` ou código, nunca pelo texto de `detail`.
5. Testam isolamento com dois usuários: pedido do usuário A consultado pelo B responde igual ao de um ID inexistente (mesmo status 404 e mesmas chaves no corpo).
6. Usam dados únicos por teste (referência com UUID), nenhum ID fixo, token fixo ou `sleep` fixo; credenciais lidas das variáveis de ambiente informadas.
7. Declara que não executou os testes (sem ambiente) e informa o comando para rodar (por exemplo `pytest tests/api -n auto`), sem afirmar que passam.
FAIL if qualquer um ocorrer: assertiva apenas de status 200 ou 201; esperado copiado da resposta; token ou senha escritos no código; ID fixo; afirma que os testes passam ou foram executados.
