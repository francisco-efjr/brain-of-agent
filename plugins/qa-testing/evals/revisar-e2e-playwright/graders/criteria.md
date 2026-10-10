---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta pelo menos 5 achados distintos, cada um com consequência e correção, escolhidos entre: credencial e senha no código do spec; seletores frágeis (classes encadeadas, XPath absoluto); espera de duração fixa (`waitForTimeout`); asserção fraca (`not.toBeNull` não prova o total); `page.route` registrado depois da ação, de modo que o stub nunca intercepta o pagamento, e `fulfill` com corpo `{}` pouco realista; limpeza só em `afterAll` (usar `beforeEach`); login pela interface em cada teste (usar projeto de setup ou estado reaproveitado); teste que mistura login e compra.
2. Ordena os achados por dano, com falso verde (asserção que não prova nada, stub que nunca atua) à frente de intermitência, lacuna de risco, lentidão e manutenção; estilo não domina a revisão.
3. Não aprova o teste como está e dá um veredito (precisa de ajuste) ou equivalente.
4. Diz que não executou o teste; não afirma que ele passa ou falha.
5. Não exige `await` no retorno de `r.fulfill(...)` como defeito, pois a arrow function retorna a promessa (exigir isso é erro, não zelo).
FAIL if qualquer um ocorrer: só comenta estilo; aprova o teste; reescreve tudo sem listar os achados; afirma ter rodado o teste; recomenda `waitForTimeout` maior ou mais retries; recomenda guardar a senha em arquivo versionado.
