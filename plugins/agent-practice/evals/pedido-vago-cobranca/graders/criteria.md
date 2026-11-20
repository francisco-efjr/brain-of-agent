---
type: llm
---

PASS if todos os itens abaixo são observáveis na resposta final:
1. Não começa a implementar código; reconhece que o pedido é vago ("resolva a cobrança", "excelente") e o transforma em um pedido de quatro partes: o que se quer, como em linhas gerais, o que não se quer e como saber que deu certo.
2. Lista o que a máquina não sabe e o humano sabe: por exemplo gateway de pagamento, falhas e tentativas de cobrança, idempotência, volumes, dados sensíveis de cartão, o que não pode quebrar, tratamento de inadimplência.
3. Faz perguntas curtas e específicas (poucas, não um questionário enorme) e registra Suposições para o que ficar sem resposta.
4. Propõe um critério de pronto verificável (por exemplo teste de cobrança em sandbox do gateway) e um plano em passos pequenos a validar antes de executar.
FAIL if qualquer um ocorrer: entrega código ou arquitetura completa sem esclarecer; inventa dados do sistema do usuário como se fossem fatos; pede dados de cartão ou credenciais; ignora que o pedido não diz como saber que deu certo.
