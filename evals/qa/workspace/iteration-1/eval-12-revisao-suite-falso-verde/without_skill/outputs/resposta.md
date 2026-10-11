Li o `test_pedidos.py` inteiro. O "tudo verde" do time é real, mas significa pouco: dos 6 testes, 3 não conseguem falhar de jeito nenhum, 2 dependem de outro teste ter rodado antes, e o único que verifica regra de negócio testa um cenário só. Por isso bug escapa.

Não tive acesso ao `loja/pedidos.py`, então a análise é só do que está no arquivo. Para não ficar no achismo, rodei os testes offline contra uma versão fictícia de `loja.pedidos` com bugs injetados (script e saída abaixo).

## Resultado teste a teste

| Teste | O que acontece | Consegue pegar bug? |
|---|---|---|
| `test_pedido_sem_estoque` | `assert False` está dentro do `try`, e o `except Exception` engole o `AssertionError`. Passa se `criar_pedido` não levantar nada, e também se levantar qualquer erro (`TypeError`, falha de conexão...). | Não, nunca falha |
| `test_total_varios_itens` | Compara `calcular_total(x)` com `calcular_total(x)`. O esperado é a própria função. | Não, nunca falha |
| `test_cancelar_pedido` | Só tem `print(r.json())`. Sem assert no status nem no estado do pedido. Com a API devolvendo 500 + JSON, fica verde. | Não, nunca falha |
| `test_consultar_pedido` | Usa o global `pedido_id` preenchido por outro teste. Rodando sozinho, ou fora de ordem, chama `/pedidos/None`. Tem `sleep(5)` fixo. | Só confere "status 200" |
| `test_criar_pedido` | Só confere `status_code == 200`. Não olha itens, total, status nem se o pedido foi persistido. | Muito pouco |
| `test_total_com_desconto` | Ver o ponto 2 abaixo. | Parcial, 1 cenário |

## Principais problemas, por prioridade

**1. Três testes que não podem falhar** (tabela acima). Na demo, com `criar_pedido` sem checagem de estoque, `criar_pedido` quebrado com `TypeError` ou `calcular_total` ignorando a quantidade, esses testes continuam verdes.
Correção: `with pytest.raises(EstoqueInsuficiente):` (exceção específica, nunca `Exception`); comparar o total com um valor calculado à mão; assertar o status HTTP do cancelamento e depois consultar o pedido para ver se está cancelado.

**2. O `patch` do desconto está no alvo errado.** `patch("loja.pedidos.calcular_total")` troca o atributo no módulo `loja.pedidos`, mas o teste usa o nome que `from loja.pedidos import calcular_total` já tinha copiado. O patch não tem efeito, e o teste só funciona porque, por acidente, chama a função real (confirmei na demo). Se alguém "arrumar" o patch, o teste vira tautologia: mocka a função e depois confere o valor que o próprio mock devolveu. Mocke dependências (banco, API de cupom), nunca a função sob teste. Além disso, o cenário usa `qtd: 1`: um bug que ignora a quantidade passa batido (ficou verde na demo).

**3. Encadeamento por variável global.** Criar, consultar e cancelar só funcionam na ordem do arquivo. Com `pytest-xdist`, `pytest-randomly`, `-k` ou re-run de um teste que falhou, quebram ou, pior, passam contra `/pedidos/None`. Cada teste deve criar o que precisa (fixture) e limpar no fim. Hoje também fica lixo em homologação.

**4. Só caminho feliz, e só status code.** Faltam: 401 sem token, acesso a pedido de outro usuário (403/404), quantidade 0 ou negativa, SKU inexistente, estoque no limite, cupom inválido/expirado, cancelar duas vezes, cancelar pedido já enviado. É esse tipo de caso que costuma escapar para produção. Cruze com os bugs que escaparam: é provável que boa parte caia em uma dessas lacunas (é hipótese, não vi os bugs).

**5. Dinheiro em `float`.** `10.1*3 + 0.2` dá `30.499999999999996`. Se `calcular_total` devolve float, o arredondamento do total pode divergir do que o cliente vê, e um teste que compara função com ela mesma nunca mostraria isso. Use `Decimal` ou centavos inteiros no código e nos testes.

**6. `time.sleep(5)`.** Lento quando está tudo bem e flaky quando a API demora mais. Troque por polling com prazo (`esperar_ate` no arquivo revisado).

**7. Higiene e segurança do ambiente de teste.**
- O token JWT está no código. Decodificado, é `sub: qa-admin`. Se for um token real, está vazado no repositório: revogue e passe por variável de ambiente.
- Testar sempre como admin esconde bugs de autorização. Use um usuário comum, e um segundo para testar acesso cruzado.
- `requests` sem `timeout`: uma API pendurada trava o pipeline.
- Testes unitários (`calcular_total`) misturados com testes que chamam homologação, sem marcador. Separe com `@pytest.mark.integration` para o feedback rápido não depender de rede.

## Como evitar que volte

- **Quebre de propósito.** Antes de aprovar um teste, injete o bug que ele deveria pegar e veja se fica vermelho. Mutation testing (`mutmut`) automatiza isso e mede o que cobertura de linha não mede (a cobertura desta suite pode estar alta e ainda assim inútil).
- **Linter:** `ruff` com as regras `B011`, `PT015`, `PT017` e `B017` pega `assert False`, `assert` dentro de `except` e `pytest.raises(Exception)`. Não conheço regra padrão para "teste sem assert"; vale revisão de PR com essa pergunta.
- **CI:** rodar em ordem aleatória (`pytest-randomly`), com `pytest-timeout` e `pytest-socket` nos testes unitários.
- Cada bug que escapa para produção vira um teste de regressão no mesmo PR da correção.

## Arquivos que deixei na pasta de saída

- `demo_falso_verde.py` e `saida_demo.txt`: carrega seu arquivo original (somente leitura), simula bugs em `loja.pedidos` e mostra quais testes continuam verdes. Roda sem rede e sem pytest.
- `test_pedidos_revisado.py`: proposta de reescrita com parametrização, `pytest.raises` específico, fixtures com limpeza, polling, token por variável de ambiente, `timeout` e marcador `integration`. Os pontos que dependem do contrato real estão marcados com `TODO` (nome da exceção, campos do JSON, status HTTP, valores de status). Ele passa na checagem de sintaxe, mas **não foi executado**: o ambiente não tem pytest, rede nem o módulo `loja`.

Se você me passar `loja/pedidos.py`, a lista dos últimos bugs que foram para produção e o formato do JSON da API, eu fecho os TODOs e mapeio cada bug a um teste que o teria pego.
