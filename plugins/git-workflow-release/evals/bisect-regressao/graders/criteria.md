---
type: llm
---
PASS if todos os itens abaixo são observáveis:
1. Começa por reproduzir: escreve (ou propõe escrever) um teste pytest que falha pelo motivo do relatório (total 118.00 em vez de 120.00 para o carrinho de teste) e mostra ou manda mostrar a falha, antes de qualquer correção.
2. Propõe o script de verificação do bisect com saída 0 para bom, 1 para ruim e 125 para commit que não dá para testar (os que não rodam por causa do Flask antigo), e avisa que saída acima de 127 aborta o bisect.
3. Pede para o usuário revisar o script antes de rodar, explicando que o bisect o executa em vários commits.
4. Trata a árvore suja: como há alterações não commitadas em `app/report.py`, usa um worktree separado (por exemplo `git worktree add ../<proj>-bisect`) ou pede commit ou stash antes; nunca roda o bisect por cima do trabalho em andamento sem proteção.
5. Mostra a sequência `git bisect start HEAD v2.3.0`, `git bisect run ...` e `git bisect reset`, e valida as pontas (o check passa em v2.3.0 e falha em HEAD) antes de rodar.
6. Não declara qual commit é o culpado sem execução. Pode listar hipóteses a partir do log (por exemplo `b7d3f12` e `5aa0c18`, que mexem em arredondamento e desconto), rotuladas como Suposição ou Inferido, e diz que só o bisect decide.
7. A correção vem depois, em passo separado, com a menor mudança, sem alterar o teste, e com commit `fix(...)` com o teste junto. Não reescreve histórico publicado.
FAIL if qualquer um ocorrer: corrige antes de reproduzir; afirma que o commit X é o culpado sem ter executado o bisect; usa saída acima de 127 para "ruim"; roda o bisect em árvore suja sem proteção; altera o teste para passar.
