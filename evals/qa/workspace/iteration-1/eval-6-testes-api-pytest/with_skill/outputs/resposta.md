Escrevi a suíte em pytest para os dois endpoints do `openapi-contas.yaml` (extrato e transferência PIX). Ela está na pasta `testes_api_contas/`: 36 funções de teste, 97 casos com a parametrização, mais 3 testes "destrutivos" que ficam desligados por padrão. **Não rodei contra a sua homologação** (os sistemas são fictícios e eu não faço requisições). O que executei e o que não executei está na seção "O que foi verificado" mais abaixo.

## O que você precisa preencher antes de rodar

A especificação não tem endpoint de login, então tokens, IDs e chave PIX vêm do ambiente (modelo em `.env.example`). Não cole esses valores no chat nem no repositório.

| Variável | O que é |
| --- | --- |
| `API_BASE_URL` | URL da homologação (o host precisa conter "homolog", senão a suíte se recusa a rodar, porque ela move dinheiro) |
| `API_TOKEN_A`, `API_TOKEN_B` | Bearer token de cada usuário de teste |
| `CONTA_A_ID`, `CONTA_B_ID` | UUID da conta de cada um |
| `CHAVE_PIX_B` | chave PIX que aponta para a conta de B (destino das transferências A para B) |
| `CHAVE_PIX_A` (opcional) | habilita a direção B para A, a devolução dos testes destrutivos e provas de ausência de efeito mais fortes |

```bash
cd testes_api_contas
python -m venv .venv && source .venv/bin/activate     # Python 3.10 ou superior
pip install -r requirements-test.txt
cp .env.example .env     # preencha; depois: set -a; source .env; set +a
pytest                                  # suíte padrão
pytest -m "not inferido"                # sem os testes de comportamento que o contrato não escreve
RUN_TESTES_DESTRUTIVOS=1 pytest -m destrutivo   # limite acumulado, saldo exato, corrida de saldo
```

Rode **sem `-n` (xdist)**: as duas contas são compartilhadas por todos os testes. A conta A precisa ter pelo menos R$ 10,00, e cada execução move pouco mais de R$ 1 de A para B (no simulador deu R$ 1,30). Se o ambiente estiver fora do ar, o token expirado ou o saldo de A for baixo, o preflight aborta com mensagem de bloqueio de ambiente, em vez de reportar 90 falhas falsas.

## O que está coberto, por risco

1. **Dinheiro sai da conta errada ou duas vezes.**
   - Transferir da conta de outro titular dá 404, é indistinguível de conta inexistente e A continua sem débito.
   - Mesma `Idempotency-Key` com o mesmo corpo dá 201 e depois 200, com um único débito. Cinco requisições simultâneas com a mesma chave também geram um débito só.
   - Mesma chave com valor diferente nunca gera segundo débito.
   - Sem token ou com token inválido dá 401 e nada é debitado.
2. **Recusas de regra de negócio (422)**, sempre com a prova de que nada foi debitado:
   - chave de destino inválida (3 variantes);
   - valor acima do saldo;
   - valor acima de R$ 5.000,00 (limite diário).
3. **Efeito correto no caso feliz.** O saldo de A cai e o de B sobe exatamente o valor enviado, o extrato de A mostra um DEBITO com o valor e a descrição (140 caracteres exatos, acentos e apóstrofo voltam intactos), e `criadaEm` e `data` não têm erro de fuso. O mínimo R$ 0,01 e R$ 0,02 são aceitos.
4. **Validação de entrada da transferência**, 23 corpos inválidos mais JSON malformado:
   - valor com 0, negativo, 1/2/3 casas decimais, vírgula, milhar BR, texto, vazio, número JSON em vez de string e nulo;
   - campos ausentes, chave vazia, descrição com 141 caracteres e JSON malformado.
5. **Extrato.**
   - O titular lê o próprio extrato conforme o schema (dinheiro com 2 casas, UUIDs, enum, sem campo sensível).
   - Extrato de conta alheia dá 404 sem vazar `saldo` nem `lancamentos`.
   - `tamanho` aceita 1, 2, 99 e 100 e recusa 0, -1, 101, 10^9, texto e decimal com 400 em `application/problem+json`; o padrão é 20.
   - Paginar de um em um reproduz a mesma sequência da página grande, sem repetir nem perder item.
   - O cursor adulterado ou de outro titular não vaza dados.
   - Os filtros `desde` e `ate` incluem os dois extremos, e datas inválidas (mês 13, 30/02, 29/02 de ano não bissexto, dd/mm/aaaa) dão 400.
6. **Destrutivos, desligados por padrão** (ver `test_transferencias_destrutivas.py`):
   - o limite diário acumulado aceita exatamente R$ 5.000,00 e recusa o centavo seguinte;
   - transferir exatamente o saldo é aceito;
   - dois débitos simultâneos que juntos excedem o saldo aprovam só um.

   Eles consomem o limite diário da conta de origem, então rodam por último e os que não cabem no saldo atual são pulados com o motivo.

Como a suíte lida com o fato de o status poder ser `PROCESSANDO`: ela espera por condição, com prazo de 20 s (`API_ESPERA_MAX`), nunca por `sleep` fixo. Para provar que uma recusa não deixou efeito, envia uma transferência válida de R$ 0,01 logo depois, espera ela aparecer no extrato e só então confere a ausência.

## O que supus (sem isso o código não fecha)

- A `descricao` enviada aparece no lançamento do extrato; uso um marcador único nela para achar os lançamentos de cada teste.
- O sinal do valor de um DEBITO no extrato não está definido (`-5.00` ou `5.00`). Comparo o valor absoluto.
- Entrada inválida em `POST /transferencias` volta como 400 ou 422, porque o contrato só documenta o 422 para regra de negócio. Aceito os dois e exijo que nunca seja 2xx nem 5xx.
- O "dia" do limite diário e dos filtros `desde`/`ate` é o de `America/Sao_Paulo` (`API_FUSO`).
- O limite já consumido hoje é a soma dos débitos do dia no extrato (só afeta os destrutivos).

Onde o contrato é omisso, o teste leva o marcador `inferido` (7 funções de teste). Se o time decidir outro comportamento, é uma linha para ajustar.

## Perguntas cuja resposta muda o resultado

1. Como se obtém o token? Há um login/OAuth fora desta especificação? Tokens que expiram no meio da rodada derrubam a suíte; se houver endpoint, a fixture de `conftest.py` passa a buscá-lo sozinha.
2. Qual é o status esperado para `Idempotency-Key` ausente ou inválida, para a mesma chave com corpo diferente (o rascunho da IETF sugere 422) e para requisições simultâneas com a mesma chave (409?). Hoje testo só o que não pode acontecer: segundo débito e valor trocado.
3. O limite de R$ 5.000,00 conta só PIX enviado? Qual é o fuso do dia? `desde > ate` é 400 ou lista vazia?
4. Quais são os saldos de A e de B? As regras "valor acima do saldo" e "valor acima do limite" são mutuamente excludentes numa mesma conta (a primeira precisa de saldo abaixo de R$ 5.000, a segunda de saldo acima). Com só `CHAVE_PIX_B` uma delas é pulada com motivo; com `CHAVE_PIX_A` a suíte usa a outra conta. O ideal seria uma conta de teste com saldo controlado ou um endpoint de reset.
5. Outras pessoas ou jobs movimentam essas duas contas? Se sim, os testes de saldo podem falhar por interferência externa.

## O que ficou de fora (e o risco que sobra)

- **Token expirado ou de outro ambiente:** não dá para fabricar um token assim em homologação. Cobri só "sem token" e "token inválido".
- **Estado final da transferência (CONCLUIDA ou RECUSADA):** não há `GET /transferencias/{id}` no contrato, então só observo pelo extrato e pelos saldos.
- **Tipos de chave PIX** (CPF, CNPJ, e-mail, telefone, aleatória) válidos e cadastrados, e transferência para a própria conta: só tenho a chave de B.
- **Concorrência em escala:** uso 5 e 2 requisições simultâneas. Isso pega a corrida grosseira, mas não prova a ausência de corrida.
- **Rate limit, CORS e demais cabeçalhos de segurança, carga e fuzzing:** o contrato não define. Como complemento barato recomendo Schemathesis contra a homologação (`references/automacao-api.md`) e `oasdiff` no CI.
- **Deriva do contrato:** os modelos Pydantic em `tests/support.py` espelham o YAML 1.4.0 à mão; se a especificação mudar, eles precisam acompanhar.

## O que foi verificado

- **Verificado:** o código compila. Executei a suíte inteira (`requests` e `pydantic` reais) contra um simulador em memória da API que escrevi a partir do YAML, sem rede. No cenário padrão: 93 casos passaram e 4 foram pulados (3 destrutivos desligados e o teste do limite, que exige saldo de R$ 5.000,01). Com os destrutivos ligados e saldos que permitem rodar tudo: 97 de 97. Também injetei 12 defeitos no simulador, e a suíte falhou em cada um:
  - extrato de conta alheia retornado;
  - origem alheia aceita na transferência;
  - idempotência ignorada;
  - saldo negativo permitido;
  - `valor` numérico aceito;
  - cursor que repete item;
  - `tamanho` sem limite;
  - falta de `no-store`;
  - limite diário ausente;
  - limite que usa `>=` em vez de `>`;
  - saldo que usa `>=` em vez de `>`;
  - corrida de saldo.
- **Não verificado:** nenhuma execução contra a homologação real, então os testes `inferido` e as suposições acima podem falhar por divergência entre o que presumi e o que a API faz. Também não rodei com o pytest de verdade (não está instalado aqui e eu não podia instalar): usei um substituto mínimo só para exercitar a lógica. Coleta, `ids` de parametrização e relatório de asserções do pytest real ficam para a sua primeira execução. Se algo falhar na coleta, mande a saída.

## Arquivos

```
testes_api_contas/
  pytest.ini, requirements-test.txt, .env.example, .gitignore
  tests/
    conftest.py                         fixtures, preflight, trava de host, manifesto da execução
    support.py                          cliente fino, modelos do contrato, esperas, provas de efeito
    test_extrato.py                     16 funções
    test_transferencias.py              17 funções
    test_transferencias_destrutivas.py  3 funções (RUN_TESTES_DESTRUTIVOS=1)
```
