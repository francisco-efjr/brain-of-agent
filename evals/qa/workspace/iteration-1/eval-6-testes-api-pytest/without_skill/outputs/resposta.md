Montei a suíte em pytest + requests para os dois endpoints (`GET /contas/{contaId}/extrato` e `POST /transferencias`): 89 casos, 34 no extrato e 55 em transferências. Ainda não rodei contra a homolog nem com o pytest real (detalhes no fim), então espere ajustes na primeira execução.

```
pytest.ini  requirements.txt  .env.example  .gitignore
tests/
  conftest.py            fixtures: config por env, clientes dos usuários A e B, checagem do ambiente
  cliente.py             cliente HTTP, leitura de saldo/extrato, esperas por consistência eventual
  contratos.py           validação das respostas contra os schemas do OpenAPI
  test_extrato.py
  test_transferencias.py
```

**Como rodar**
1. `pip install -r requirements.txt`
2. `cp .env.example .env`, preencha e carregue com `set -a; source .env; set +a`. Preciso do token e do UUID da conta dos dois usuários e da chave PIX da conta B (destino das transferências de A).
3. `pytest` roda tudo. `pytest -m "not muta_estado"` roda só leituras e recusas.

O spec não tem endpoint de login, então os tokens vêm de variável de ambiente. Se na homolog eles expiram rápido, troque os fixtures `api_a` e `api_b` do `conftest.py` por uma chamada ao seu provedor de identidade.

**Atenção: os testes movem dinheiro.** Os marcados `muta_estado` fazem transferências reais de R$ 0,01 (algumas de R$ 0,02) de A para B, sem como desfazer. Uma execução completa move poucos centavos. A suíte recusa rodar se a URL não tiver "homolog" e não pode rodar em paralelo (`-n`).

**O que cobre**
- Extrato: contrato do 200, `tamanho` (padrão 20, limites 1 e 100, 400 fora disso), datas inválidas, período vazio, paginação por `proximaPagina` sem repetição, 401 em quatro formas, token adulterado, 404 ao ler a conta do outro titular (nos dois sentidos), conta alheia indistinguível de inexistente.
- Transferências: contrato do 201, débito na origem e crédito no destino (com espera por consistência), lançamento no extrato, idempotência (replay devolve 200 com a mesma transferência, não debita de novo, chaves diferentes geram transferências diferentes, requisições simultâneas com a mesma chave), 422 por saldo, limite diário e chave inválida, entradas malformadas, 401, e 404 ao transferir da conta de outro titular conferindo que o saldo dele não mudou.

**Pontos que dependem de você**
- Os testes marcados `premissa` verificam comportamento que o spec não define (período invertido, cursor inválido, mesma chave com corpo diferente, simultaneidade, isolamento da chave entre usuários). Se algum falhar, pode ser o spec incompleto e não bug: `-m "not premissa"` os exclui.
- O spec só documenta 422 para o POST. Para campo ausente ou formato errado aceito 400 ou 422. Vale documentar qual é o certo.
- O teste do limite diário só roda se a conta A tiver pelo menos 5000.01 de saldo; com menos, o 422 poderia vir da regra de saldo e o teste não provaria nada, então ele é pulado e aparece como skip. O teste do limite acumulado gasta o limite do dia e só roda com `RODAR_TESTES_LIMITE_DIARIO=1`. Ele assume que o limite vale para a soma do dia, o que o spec não deixa claro.
- Não assumi o sinal do `valor` no débito do extrato (o pattern permite negativo).

**O que foi verificado**
O pytest não está instalado aqui e não pude instalar. Compilei os arquivos e executei tudo com um mini-substituto do pytest contra uma API simulada em memória que escrevi a partir do OpenAPI: 89 passaram, e bugs injetados (conta alheia devolvendo 200, transferência sem crédito, débito duplo no replay, chave de idempotência vazando entre usuários, `tamanho` sem limite) foram pegos. Isso valida a lógica dos testes, não o comportamento real da homolog nem detalhes do pytest (ids, marcadores).

Ficou de fora: ordenação dos lançamentos (o spec não diz), transferência para a própria conta, token expirado de verdade, o caminho assíncrono que termina em `RECUSADA` (não há `GET /transferencias/{id}` para acompanhar) e carga.
