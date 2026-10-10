---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Tem os três blocos: comportamento atual (carrinho de R$ 200,00 com DEZ10 aplicado duas vezes resulta em R$ 162,00), comportamento esperado (R$ 180,00 com o cupom contado uma vez) e comportamento inalterado.
2. O bloco inalterado lista pelo menos três itens concretos e verificáveis (por exemplo: DEZ10 aplicado uma vez continua dando R$ 180,00; cupom inválido ou expirado continua recusado com a mesma mensagem; remover o cupom restaura R$ 200,00; outros cupons seguem as regras atuais) ou levanta como pergunta a regra de combinar cupons.
3. Traz reprodução mínima e um critério de pronto com um check que falha antes da correção e passa depois, mais o check dos itens inalterados.
4. Trata a causa (clique duplo, requisição repetida sem idempotência, estado local) como hipótese rotulada Suposição, e lista perguntas abertas, incluindo se o comportamento é o mesmo no site e no app (canais) e se a repetição também ocorre por chamada direta de API.
5. Não afirma ter reproduzido o bug, lido o código ou corrigido nada, e não escreve código de correção.
FAIL if qualquer um ocorrer: pula o bloco inalterado; troca os valores do bug por outros; declara a causa raiz como fato; escreve a correção; afirma execução que não houve.
