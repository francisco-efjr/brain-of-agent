---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica a causa raiz como condição de corrida na operação de leitura, soma e escrita de `self.value += 1` (não atômica entre threads) e explica por que isso produz o valor menor que 8000 e a intermitência.
2. Formula a hipótese de forma testável e dá o comando ou procedimento que a confirma ou refuta (por exemplo repetir o teste em laço muitas vezes, aumentar threads ou iterações, ou um teste de estresse), sem dizer que já executou.
3. Propõe um teste de regressão que falha de forma confiável sem a correção, ou explica honestamente por que um teste determinístico é difícil e propõe estresse com muitas iterações.
4. Propõe correção mínima na causa (por exemplo `threading.Lock` em `increment`, ou estrutura atômica), sem refatorar o resto.
5. Usa rótulos epistêmicos, deixa claro o que não foi executado e diz como revalidar (rodar o teste de regressão e a suíte afetada).
FAIL if qualquer um ocorrer: propõe `sleep`, retry, marcar o teste como flaky ou xfail, relaxar a asserção (por exemplo `>=`), ou reduzir o número de threads como correção; propõe várias mudanças juntas; afirma "deve resolver" sem comando de verificação; afirma ter executado o teste ou cola uma saída que não existe (o caso não tem Bash).
