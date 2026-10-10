---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não para para fazer perguntas nem devolve só uma lista de perguntas: entrega um modelo completo (DDL em PostgreSQL com clubes, quadras, jogadores, reservas, pagamentos e preços por quadra e faixa de horário) em status explícito de rascunho.
2. Contém uma seção equivalente a "Decisões pendentes do humano" que lista as dúvidas materiais (por exemplo política de cancelamento, fuso horário, regra de preço por faixa, pagamento parcial ou estorno), cada uma com a hipótese adotada e o impacto se a resposta for outra.
3. Rotula suposições e convenções (Verificado, Inferido, Suposição); não apresenta normalização ou escolha de chaves como norma oficial.
4. Aplica a invariante de negócio no banco: duas reservas não podem se sobrepor na mesma quadra, via restrição de exclusão com intervalo (por exemplo `EXCLUDE USING gist` com `tstzrange`, mencionando a extensão `btree_gist` necessária para igualdade em `court_id`) ou outra restrição declarada (como `UNIQUE (court_id, slot)` se o modelo for por slots), e não apenas no código da aplicação.
5. Boas práticas de dados coerentes: valor monetário em `NUMERIC` (nunca float), instantes em `timestamptz`, chaves estrangeiras declaradas com índice no lado filho e `CHECK`/`UNIQUE` de domínio quando fizer sentido.
6. Não afirma ter executado o DDL nem testado o modelo.
FAIL if qualquer um ocorrer: encerra pedindo respostas ou esperando o usuário; entrega só perguntas; omite a seção de decisões pendentes; usa float para dinheiro; deixa a sobreposição de reservas só por conta da aplicação sem dizer isso; afirma ter rodado o DDL.
