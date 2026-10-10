---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega uma query PostgreSQL correta: agrega o valor por região e vendedor no último trimestre (filtro de data coerente com `data_venda`), aplica `RANK()`, `DENSE_RANK()` ou `ROW_NUMBER()` com `PARTITION BY regiao ORDER BY` a soma em ordem decrescente, e filtra o top 3 por região (em subquery ou CTE, pois o filtro sobre a função de janela não pode ficar no mesmo `WHERE`).
2. Responde direto como tarefa de banco de dados, sem tratar o pedido como desenvolvimento de jogos, sem mencionar GDD, engine, QA de jogo ou perfil de performance de jogo.
3. Se explicar a diferença entre `RANK`, `DENSE_RANK` e `ROW_NUMBER` em empates, a explicação está correta; não é obrigatório.
4. Não afirma ter executado a query em um banco.
FAIL if qualquer um ocorrer: aciona qualquer skill do plugin game-development; lê arquivos de referências do playbook; sintaxe SQL inválida que impeça o funcionamento (por exemplo filtrar a função de janela diretamente no WHERE); afirma ter rodado a query.
