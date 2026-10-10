---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Antes de entregar qualquer modelo, trata os padrões de acesso como pré-requisito: faz uma pergunta (a de maior impacto) ou apresenta uma lista curta das perguntas que o sistema precisa responder (buscar pedidos de um cliente, por status, por janela de tempo, detalhe de um pedido, volume e velocidade esperados, consistência exigida). Explica que o DynamoDB é modelado a partir das consultas e que desenhar o schema antes delas não se adapta depois.
2. Se apresentar um modelo, ele é explicitamente condicional (rascunho com Suposições rotuladas sobre os padrões de acesso), com chave de partição de alta cardinalidade, chave de ordenação, itens relacionados juntos, e índice secundário global (GSI) para cada consulta extra, relacionando cada chave ou GSI a um padrão de acesso.
3. Não replica o schema relacional em várias tabelas sem justificativa; trata "o menor número de tabelas" como ponto de partida e justifica qualquer exceção.
4. Não inventa números de capacidade, throughput ou custo; se tocar no assunto, diz que não verificou.
5. Não afirma ter criado tabelas nem executado comandos (não há acesso a AWS).
FAIL if qualquer um ocorrer: entrega um modelo completo apresentado como definitivo sem tratar os padrões de acesso; cria uma tabela por entidade relacional sem justificar; inventa números de capacidade; afirma ter criado ou testado as tabelas.
