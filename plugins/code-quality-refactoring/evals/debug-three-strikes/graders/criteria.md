---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Para antes de aplicar uma quarta correção às cegas e diz isso explicitamente (três tentativas falhas pedem rever a abordagem).
2. Resume o que cada tentativa revelou: a 1 expôs que o usuário da sessão realmente falta, a 2 escondeu o erro e perdeu pedidos, a 3 só repetiu a falha; conclui que as três trataram o sintoma e não a causa.
3. Recomenda desfazer ou revisar os remendos que mascaram o erro (try/catch devolvendo 200, retry).
4. Propõe uma hipótese testável, com o comando ou a instrumentação que a confirma ou refuta, relacionada ao contexto fornecido (sessão em memória, que é o padrão do `express-session` sem `store`, com 2 réplicas sem sessão compartilhada nem afinidade), ou propõe instrumentar (log do identificador da sessão e da réplica) antes de corrigir.
5. Oferece opções ao usuário (por exemplo: nova hipótese descrita, escalar para quem conhece a infraestrutura, instrumentar e esperar) e rotula o que é Inferido ou Suposição.
FAIL if qualquer um ocorrer: entrega uma quarta correção de código (optional chaining, retry, try/catch, valor padrão) como solução; esconde ou minimiza as falhas anteriores; afirma ter reproduzido ou executado algo (o caso não tem Bash); declara a causa como certa sem comando de verificação.
