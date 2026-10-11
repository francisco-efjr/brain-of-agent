# Notas e incertezas

- Não li `loja/pedidos.py` (não existe no ambiente). Toda conclusão sobre `calcular_total` e `criar_pedido` vem só do uso nos testes. A demo usa uma implementação fictícia minha, com bugs injetados; ela prova que os TESTES não detectam essas classes de defeito, não que o código real tem esses bugs.
- Comportamento do `patch`: confirmado empiricamente na demo que `m.calcular_total` continua sendo o objeto original durante o `patch("loja.pedidos.calcular_total")`. Logo o mock é inócuo e o teste exercita a função real por acidente. Se o código real fizer algo diferente (ex.: `loja.pedidos` reexportar de outro lugar), a conclusão continua valendo para o nome já importado.
- `test_criar_pedido` com `status_code == 200`: não sei se o contrato real é 200 ou 201. No arquivo revisado mantive 200 com TODO.
- O token JWT: decodifiquei só o payload (`sub: qa-admin`). Não sei se é real, expirado ou de brinquedo; recomendei revogar "se for real". Não repeti o token na resposta.
- `test_pedidos_revisado.py` NÃO foi executado: pytest e requests não estão instalados e não instalei pacotes. Só passou em `py_compile`. Pode ter erro de lógica/fixture que só aparece rodando. Os valores esperados dos totais foram calculados à mão: 50*3=150; 10.1*3+0.2=30.5; DEZ sobre 50*2 = 90; DEZ sobre (10*3+20)=50 -> 45.
- Premissas inventadas no arquivo revisado e sinalizadas como TODO: exceção `EstoqueInsuficiente`, campos `itens`/`status`, valor `"CANCELADO"`, 409/422 para cancelamento duplo e falta de estoque na API, header `Idempotency-Key` (remover se não existir), regra de desconto "sobre o total" (assumi que o cupom DEZ é 10% sobre o total do pedido).
- Regras de ruff citadas (B011, PT015, PT017, B017): citadas de memória; confirmar nos nomes/versões da versão instalada. Disse que não conheço regra padrão para "teste sem assert"; pode existir plugin que eu não lembre.
- Não li `evals/` além do arquivo indicado, nem as skills, conforme instruído. O arquivo `eval_metadata.json` apareceu na listagem da pasta de trabalho, mas não foi aberto.
- Opinião, não fato: afirmei que "a maioria dos bugs escapados deve cair nas lacunas de caminho feliz". É hipótese, sem ter visto os bugs reais. Na resposta pedi a lista deles para validar.
- A cobertura de linha da suite não foi medida (sem pytest-cov / sem código real).
