---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Faz um desafio de escopo: pergunta ou afirma, com base nos números fornecidos (50 usuários, 30 alterações por dia, 120 mil registros), que uma solução bem menor atende, e identifica o que poderia não ser construído.
2. Aponta que CQRS, event sourcing, Kafka, MongoDB e GraphQL federado não têm requisito que os justifique e que o plano não traz requisitos não funcionais com número; cita o custo operacional (Kafka sem experiência do time) e o risco do prazo.
3. Apresenta pelo menos 2 decisões numeradas (D-1, D-2 ou equivalente) com problema em linguagem simples, o que acontece se errar, recomendação, 2 a 4 opções com prós e contras, e inclui a opção "não mudar nada" ou "manter a tabela atual".
4. Termina com uma tabela ou lista de decisões pendentes com dono humano, sem decidir por preferência do usuário.
5. Não começa a implementar e não cria arquivos.
FAIL if qualquer um ocorrer: aprova o plano sem desafiar; começa a escrever código ou criar arquivos; ignora a opção de não mudar nada; inventa requisitos do negócio que o usuário não deu sem rotulá-los como Suposição.
