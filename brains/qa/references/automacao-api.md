# Automação de testes de API

Como testar APIs REST, GraphQL, gRPC, mensageria e webhooks, e como garantir o
acordo entre serviços com teste de contrato. Leia ao escrever ou revisar uma
suíte de API, ao escolher entre Pact e OpenAPI, ou quando a API "passa nos
testes" e quebra em produção.

## Sumário

- [Checklist por endpoint](#checklist-por-endpoint)
- [Status HTTP: qual é o esperado](#status-http-qual-é-o-esperado)
- [Estrutura de uma suíte de API](#estrutura-de-uma-suíte-de-api)
- [Exemplo: pytest + httpx + Pydantic](#exemplo-pytest--httpx--pydantic)
- [Exemplo: Playwright APIRequestContext](#exemplo-playwright-apirequestcontext)
- [Exemplo: REST Assured (Java)](#exemplo-rest-assured-java)
- [Exemplo: supertest + Vitest](#exemplo-supertest--vitest)
- [Postman/Newman e Bruno](#postmannewman-e-bruno)
- [GraphQL](#graphql)
- [gRPC](#grpc)
- [Mensageria e eventos](#mensageria-e-eventos)
- [Webhooks](#webhooks)
- [Teste de contrato](#teste-de-contrato)
- [Fuzzing com Schemathesis](#fuzzing-com-schemathesis)
- [Anti-padrões](#anti-padrões)

## Checklist por endpoint

Status 200 não prova nada: `200 {"erro": "..."}` ou um dado gravado errado
passam nesse teste. Priorize pelo risco (dinheiro, dado de terceiros, operação
irreversível) e verifique:

| Aspecto | O que verificar |
| --- | --- |
| Status e corpo | Status exato, não "2xx". Valores de negócio conferidos contra oráculo independente (total calculado à parte, dado semeado), nunca copiados da resposta |
| Schema | Na resposta, aceite campo novo (não é quebra), mas confira que campo sensível não vaza (`senha_hash`, CPF completo, dado interno). Dinheiro como string decimal ou centavos inteiros, nunca float; datas ISO 8601 com fuso |
| Headers | `Content-Type` certo (`application/problem+json` nos erros); `Cache-Control: no-store` em dado pessoal; `Location` no 201; `Allow` no 405; sem versão em `Server`/`X-Powered-By`; HSTS e `X-Content-Type-Options: nosniff` |
| CORS | Só origens da lista; nunca refletir qualquer `Origin` com `Access-Control-Allow-Credentials: true`; preflight `OPTIONS` coerente |
| Erro (RFC 9457) | `type` (URI que identifica o erro), `title`, `status` igual ao HTTP, `detail`, `instance` e extensões (campos inválidos). Mesmo formato em todos os endpoints; sem stack trace, SQL ou hostname. JSON malformado → 400 nesse formato, não 500 |
| Idempotência | `PUT`/`DELETE` repetidos deixam o mesmo estado (o 2º `DELETE` pode dar 204 ou 404, conforme o contrato). `POST` com `Idempotency-Key`: mesma chave e corpo → mesma resposta, sem novo efeito. O draft da IETF (não virou RFC) sugere 422 para chave reutilizada com outro corpo, 409 se a original ainda está em curso, 400 se a chave obrigatória faltar |
| Paginação | `limit` padrão, máximo, 0, negativo, máximo+1, 10^9 (recusar com 400 ou limitar, nunca 500 nem "tudo"); última página sem "próximo"; página além do fim → lista vazia com 200; cursor adulterado → 400; ordenação com desempate (`criado_em, id`), senão itens repetem ou somem; offset pula itens quando há inserção no meio, cursor não |
| Filtros e ordenação | Combinações; sem resultado → lista vazia; acento e caixa ("joão" × "Joao"); fim de intervalo de data inclusivo e no fuso certo; campo de ordenação fora da lista permitida → 400 (vetor de injeção) |
| Validação | Obrigatório ausente; `null` × ausente (em `PATCH`, `null` = limpar, ausente = não mexer); tipo errado; tamanhos; Unicode; corpo enorme → 413. Campo extra: o contrato diz se rejeita ou ignora, mas nunca aplica — `{"papel": "admin"}` ou `{"preco": 0}` é atribuição em massa |
| Autenticação × autorização | Sem token, expirado, assinatura inválida, `alg: none`, token de outro ambiente → 401. Válido sem o escopo → 403. Recurso de outro usuário/tenant → 404 (ou 403 se a existência não for segredo); listagens não trazem itens alheios |
| Rate limit | Acima do limite → 429 com `Retry-After`; limite por cliente, não global. Só em ambiente isolado |
| Versionamento | Versão anterior funciona enquanto houver consumidor; descontinuação com `Deprecation` (RFC 9745) e `Sunset` (RFC 8594). Quebras: remover/renomear campo, mudar tipo, tornar obrigatório campo de entrada, **novo valor de enum na resposta** (quebra `switch` exaustivo no consumidor) |
| Concorrência otimista | `GET` devolve `ETag`; `If-Match` desatualizado → 412; sem `If-Match` quando exigido → 428; conflito de regra (transição inválida, chave única) → 409. Nunca atualização perdida em silêncio |
| Tempo de resposta | Teto folgado (por exemplo, 2 s) só para pegar travamento; percentis ficam no teste de performance — teto apertado aqui gera intermitência |
| Efeito colateral | Depois do `POST`, o `GET` devolve o mesmo dado; a linha certa está no banco; o evento saiu **uma vez** com o payload certo. E o inverso: requisição recusada não deixa registro pela metade |

## Status HTTP: qual é o esperado

| Status | Esperado quando | Confusão comum |
| --- | --- | --- |
| 200 | leitura; atualização que devolve o recurso; ação que não cria nada | `200` com erro no corpo |
| 201 | `POST`/`PUT` que criou recurso, com `Location` | `200` na criação; falta `Location` |
| 202 | processamento assíncrono aceito e ainda não feito; indica onde consultar | tratar 202 como concluído |
| 204 | sucesso sem corpo (`DELETE`, `PUT` sem retorno) | 204 com corpo |
| 400 | requisição malformada: JSON inválido, tipo errado | ver 422 |
| 401 | sem credencial ou credencial inválida/expirada, com `WWW-Authenticate` | 401 para "sem permissão" |
| 403 | autenticado, sem permissão | 403 para token expirado |
| 404 | não existe — ou existe e o chamador não pode saber | 403 em ID alheio revela que o ID existe |
| 405 / 406 / 415 | método não suportado (com `Allow`) / `Accept` impossível / `Content-Type` não suportado | 500 ou 400 genérico |
| 409 | conflito com o estado atual: duplicidade, transição inválida | 409 para erro de validação |
| 412 / 428 | `If-Match` desatualizado / pré-condição exigida e ausente | 409 genérico para os dois |
| 413 | corpo acima do limite | 500 por estouro de memória |
| 422 | sintaxe válida, regra violada (fim antes do início, CPF com dígito errado) | ver abaixo |
| 429 | limite de taxa, com `Retry-After` | 503 sem dizer quando voltar |
| 500 | nunca é o esperado para entrada do cliente | "aceitável porque o dado era inválido" |
| 502 / 503 / 504 | falha de dependência ou gateway; 503 com `Retry-After` em manutenção | — |

**400 × 422:** o defeito é a inconsistência, não a escolha (FastAPI usa 422
para validação por padrão; Spring, 400). Siga o contrato e cobre a mesma regra
em todos os endpoints. **404 × 403 para recurso alheio:** com ID previsível ou
existência sensível (pedido, paciente), "existe mas não é seu" deve ser
indistinguível de "não existe" — mesmo status, mesmo formato de corpo.

## Estrutura de uma suíte de API

- **Cliente fino:** um método por operação que devolve a resposta crua, sem
  asserção nem exceção em 4xx — senão os testes negativos ficam impossíveis.
- **Fábrica de dados:** cada teste cria o que usa, com identificador único,
  para rodar em paralelo e em qualquer ordem; limpa o que criou ou usa ambiente
  descartável.
- **Schema:** JSON Schema, Pydantic ou Zod provam a forma; os valores de
  negócio são conferidos à parte.
- **Autenticação por fixture:** token obtido uma vez por sessão com
  credenciais do ambiente (variáveis do CI, cofre); dois usuários de teste
  para provar isolamento.

## Exemplo: pytest + httpx + Pydantic

```python
# tests/api/conftest.py
import os
import uuid

import httpx
import pytest
from pydantic import BaseModel, ConfigDict

BASE_URL = os.environ["API_BASE_URL"]  # ex.: https://homolog.exemplo.com.br/api/v1


class Pedido(BaseModel):
    model_config = ConfigDict(extra="ignore")  # campo novo na resposta não é quebra
    id: uuid.UUID
    status: str
    total: str  # dinheiro como string decimal, ex.: "49.90"


class Problema(BaseModel):  # RFC 9457
    type: str
    title: str
    status: int
    detail: str | None = None


def novo_pedido(**campos) -> dict:
    # "CAFE-500G" custa 24,95 na massa semeada do ambiente: é o oráculo do total
    return {"referencia": f"teste-{uuid.uuid4().hex[:12]}",
            "itens": [{"sku": "CAFE-500G", "quantidade": 2}]} | campos


def _cliente(usuario_env: str, senha_env: str):
    with httpx.Client(base_url=BASE_URL, timeout=10) as anonimo:
        r = anonimo.post("/auth/token", json={"usuario": os.environ[usuario_env],
                                              "senha": os.environ[senha_env]})
    r.raise_for_status()
    token = r.json()["access_token"]
    return httpx.Client(base_url=BASE_URL, timeout=10, headers={"Authorization": f"Bearer {token}"})


@pytest.fixture(scope="session")
def api():
    with _cliente("API_USUARIO_A", "API_SENHA_A") as cliente:
        yield cliente


@pytest.fixture(scope="session")
def api_outro_cliente():
    with _cliente("API_USUARIO_B", "API_SENHA_B") as cliente:
        yield cliente
```

```python
# tests/api/test_pedidos.py
import uuid

import pytest

from .conftest import Pedido, Problema, novo_pedido


def criar(api, corpo, chave=None):
    return api.post("/pedidos", json=corpo, headers={"Idempotency-Key": chave or str(uuid.uuid4())})


def test_cria_pedido_calcula_total_e_persiste(api):
    r = criar(api, novo_pedido())

    assert r.status_code == 201, r.text
    pedido = Pedido.model_validate(r.json())
    assert (pedido.status, pedido.total) == ("PENDENTE", "49.90")  # 2 × 24,95
    assert r.headers["location"].endswith(f"/pedidos/{pedido.id}")
    lido = api.get(f"/pedidos/{pedido.id}")  # efeito colateral: foi gravado de fato
    assert lido.status_code == 200 and Pedido.model_validate(lido.json()) == pedido


def test_mesma_idempotency_key_nao_cria_segundo_pedido(api):
    chave, corpo = str(uuid.uuid4()), novo_pedido()
    primeira, segunda = criar(api, corpo, chave), criar(api, corpo, chave)

    assert primeira.status_code == segunda.status_code == 201
    assert segunda.json()["id"] == primeira.json()["id"]
    assert len(api.get("/pedidos", params={"referencia": corpo["referencia"]}).json()["itens"]) == 1


@pytest.mark.parametrize("quantidade", [0, -1, 2.5, None, 10_001])  # contrato: inteiro de 1 a 10.000
def test_quantidade_invalida_retorna_problem_details_e_nao_grava(api, quantidade):
    corpo = novo_pedido(itens=[{"sku": "CAFE-500G", "quantidade": quantidade}])
    r = criar(api, corpo)

    assert r.status_code == 422
    assert r.headers["content-type"].startswith("application/problem+json")
    problema = Problema.model_validate(r.json())
    assert problema.status == 422 and problema.type.endswith("/validacao")  # código, não texto
    assert api.get("/pedidos", params={"referencia": corpo["referencia"]}).json()["itens"] == []


def test_pedido_de_outro_cliente_e_indistinguivel_de_inexistente(api, api_outro_cliente):
    alheio_id = criar(api, novo_pedido()).json()["id"]
    alheio = api_outro_cliente.get(f"/pedidos/{alheio_id}")
    inexistente = api_outro_cliente.get(f"/pedidos/{uuid.uuid4()}")

    assert alheio.status_code == inexistente.status_code == 404
    assert alheio.json().keys() == inexistente.json().keys()
```

Rode com `pytest tests/api -n auto` (pytest-xdist); a referência única por
teste é o que permite o paralelismo.

## Exemplo: Playwright APIRequestContext

Útil quando o E2E já é Playwright (mesma configuração, relatório e trace).
Armadilha: o caminho é resolvido como `new URL(caminho, baseURL)`; com
`baseURL` `https://h/api/v1/`, o caminho `/pedidos` vira `https://h/pedidos`.
Termine o `baseURL` com `/` e use caminhos sem barra inicial. `headers()`
devolve nomes em minúsculas.

```typescript
// tests/api/pedidos.spec.ts
import { test as base, expect, type APIRequestContext } from '@playwright/test';

const test = base.extend<{}, { api: APIRequestContext }>({
  api: [async ({ playwright }, use) => {
    const anonimo = await playwright.request.newContext({ baseURL: process.env.API_BASE_URL });
    const login = await anonimo.post('auth/token', {
      data: { usuario: process.env.API_USUARIO_A, senha: process.env.API_SENHA_A },
    });
    await expect(login).toBeOK();
    const { access_token } = await login.json();
    await anonimo.dispose();
    const api = await playwright.request.newContext({
      baseURL: process.env.API_BASE_URL,
      extraHTTPHeaders: { Authorization: `Bearer ${access_token}` },
    });
    await use(api);
    await api.dispose();
  }, { scope: 'worker' }],
});

test('If-Match desatualizado retorna 412 e preserva a alteração anterior', async ({ api }) => {
  const criado = await api.post('pedidos', { data: { itens: [{ sku: 'CAFE-500G', quantidade: 1 }] } });
  expect(criado.status()).toBe(201);
  const { id } = await criado.json();
  const etag = (await api.get(`pedidos/${id}`)).headers()['etag'];
  expect(etag).toMatch(/^(W\/)?".+"$/);

  const primeira = await api.patch(`pedidos/${id}`, { headers: { 'If-Match': etag }, data: { observacao: 'A' } });
  expect(primeira.status()).toBe(200);
  const segunda = await api.patch(`pedidos/${id}`, { headers: { 'If-Match': etag }, data: { observacao: 'B' } });
  expect(segunda.status()).toBe(412);
  expect((await (await api.get(`pedidos/${id}`)).json()).observacao).toBe('A');
});
```

## Exemplo: REST Assured (Java)

Dependências `io.rest-assured:rest-assured` e
`io.rest-assured:json-schema-validator`; schema em
`src/test/resources/schemas/pedido.json`.

```java
import static io.restassured.RestAssured.given;
import static io.restassured.module.jsv.JsonSchemaValidator.matchesJsonSchemaInClasspath;
import static org.hamcrest.Matchers.*;

import io.restassured.builder.RequestSpecBuilder;
import io.restassured.http.ContentType;
import io.restassured.specification.RequestSpecification;
import java.util.*;
import org.junit.jupiter.api.*;

class PedidosApiTest {
    private static final String BASE_URL = System.getenv("API_BASE_URL");
    private static RequestSpecification autenticado;

    @BeforeAll
    static void autenticar() {
        String token = given().baseUri(BASE_URL).contentType(ContentType.JSON)
                .body(Map.of("usuario", System.getenv("API_USUARIO_A"), "senha", System.getenv("API_SENHA_A")))
                .when().post("/auth/token").then().statusCode(200).extract().path("access_token");
        autenticado = new RequestSpecBuilder().setBaseUri(BASE_URL).setContentType(ContentType.JSON)
                .addHeader("Authorization", "Bearer " + token).build();
    }

    @Test
    void criaPedidoConformeSchemaELegivelEmSeguida() {
        String id = given().spec(autenticado).header("Idempotency-Key", UUID.randomUUID().toString())
                .body(Map.of("itens", List.of(Map.of("sku", "CAFE-500G", "quantidade", 2))))
            .when().post("/pedidos")
            .then().statusCode(201)
                .header("Location", containsString("/pedidos/"))
                .body(matchesJsonSchemaInClasspath("schemas/pedido.json"))
                .body("status", equalTo("PENDENTE")).body("total", equalTo("49.90"))
                .extract().path("id");

        given().spec(autenticado).when().get("/pedidos/{id}", id)
            .then().statusCode(200).body("id", equalTo(id)).body("itens[0].quantidade", equalTo(2));
    }

    @Test
    void semTokenRetorna401EmProblemDetailsSemStackTrace() {
        given().baseUri(BASE_URL).when().get("/pedidos")
            .then().statusCode(401).contentType(startsWith("application/problem+json"))
                .body("status", equalTo(401)).body("stackTrace", nullValue());
    }
}
```

## Exemplo: supertest + Vitest

Testa a API Node em processo (sem abrir porta), passando por rotas,
middlewares e serialização. Igual com Jest.

```typescript
// test/pedidos.test.ts — Zod 4
import request from 'supertest';
import { expect, it } from 'vitest';
import { z } from 'zod';
import { criarApp } from '../src/app'; // app Express, sem listen()
import { gerarTokenDeTeste } from './auth'; // assina JWT com o segredo do ambiente de teste

const Pedido = z.object({ id: z.uuid(), status: z.enum(['PENDENTE', 'PAGO', 'CANCELADO']), total: z.string() });
const app = criarApp();
const corpo = { itens: [{ sku: 'CAFE-500G', quantidade: 2 }] };

it('cria pedido para cliente com escopo de escrita', async () => {
  const token = gerarTokenDeTeste({ sub: 'cliente-a', escopos: ['pedidos:escrever'] });
  const res = await request(app).post('/pedidos').set('Authorization', `Bearer ${token}`).send(corpo);
  expect(res.status).toBe(201);
  expect(Pedido.parse(res.body).total).toBe('49.90');
});

it('recusa com 403 quando falta o escopo de escrita', async () => {
  const token = gerarTokenDeTeste({ sub: 'cliente-a', escopos: ['pedidos:ler'] });
  const res = await request(app).post('/pedidos').set('Authorization', `Bearer ${token}`).send(corpo);
  expect(res.status).toBe(403);
  expect(res.headers['content-type']).toMatch(/^application\/problem\+json/);
});
```

## Postman/Newman e Bruno

Servem para exploração, smoke de ambiente publicado e coleção compartilhada
com quem não programa. Para regressão com fábrica de dados, limpeza e lógica
reutilizável, código vence: script de coleção não tem tipo, reaproveita mal e
encadear requisições por variável cria dependência de ordem. Coleção Postman é
um JSON grande com diff ilegível em PR; Bruno grava um arquivo de texto por
requisição, versionável no repositório.

```javascript
// Postman — aba Tests de "Criar pedido"
pm.test('cria pedido com 201 e Location', () => {
  pm.response.to.have.status(201);
  pm.expect(pm.response.headers.get('Location')).to.match(/\/pedidos\/[0-9a-f-]{36}$/);
  pm.expect(pm.response.json().status).to.eql('PENDENTE');
});
```

```bash
# Newman no CI; o segredo entra por variável, nunca salvo no arquivo de ambiente
npx newman run pedidos.postman_collection.json -e homolog.postman_environment.json \
  --env-var "senha=$API_SENHA" --reporters cli,junit --reporter-junit-export resultados/newman.xml
# Bruno (npm i -g @usebruno/cli), dentro da pasta da coleção; teste no .bru:
# test("cria", function () { expect(res.getStatus()).to.equal(201); });
bru run --env homolog --env-var "senha=$API_SENHA" --reporter-junit resultados/bruno.xml
```

## GraphQL

- **Erro com HTTP 200.** Erro de execução vem em `errors`, com status 200 e
  `data` possivelmente parcial (`null` nos campos que falharam). Toda asserção
  começa por `errors` ausente; só status é falso verde garantido.
- **Profundidade e complexidade.** Consulta aninhada
  (`pedido { cliente { pedidos { cliente { … } } } }`) e listas dentro de
  listas devem ser recusadas antes de executar. Teste aliases em massa
  (`a1: login(...)` … `a1000: login(...)`), que driblam rate limit por
  requisição.
- **N+1.** Lista com campo aninhado sem DataLoader dispara uma consulta por
  item. Conte as consultas ao banco com 1 e com 50 itens: deve ser constante.
- **Introspecção em produção.** `{ __schema { types { name } } }` deve
  falhar; confira se sugestões de campo ("Did you mean…") vazam o schema.
- **Autorização por campo.** O mesmo dado é alcançável por vários caminhos
  (`pedido.cliente.cpf`, `usuario.cpf`); a regra mora no resolver do campo, não
  no ponto de entrada. Teste cada caminho com perfil sem acesso.
- **Persisted queries.** Em produção, aceite só documentos registrados
  (allowlist). APQ sozinho é otimização de cache, não controle de segurança.

## gRPC

```bash
grpcurl -plaintext localhost:50051 list                       # requer reflection no servidor
grpcurl -plaintext localhost:50051 describe pedidos.v1.PedidoService
grpcurl -plaintext -max-time 2 -H "authorization: Bearer $TOKEN" \
  -d '{"id": "7f6c2a1e-0000-4000-8000-000000000001"}' localhost:50051 pedidos.v1.PedidoService/ObterPedido
grpcurl -import-path ./proto -proto pedidos/v1/pedidos.proto -plaintext -d '{}' \
  localhost:50051 pedidos.v1.PedidoService/ListarPedidos      # sem reflection
```

O HTTP é 200; o resultado vem no trailer `grpc-status`. Equivalências:
`INVALID_ARGUMENT` (3) ≈ 400, `UNAUTHENTICATED` (16) ≈ 401,
`PERMISSION_DENIED` (7) ≈ 403, `NOT_FOUND` (5) ≈ 404, `ALREADY_EXISTS` (6) ≈
409, `RESOURCE_EXHAUSTED` (8) ≈ 429, `DEADLINE_EXCEEDED` (4) ≈ 504,
`UNAVAILABLE` (14) ≈ 503, `INTERNAL` (13)/`UNKNOWN` (2) ≈ 500. Confusão comum:
`UNAVAILABLE` = pode repetir a chamada; `ABORTED` (10) = repetir um nível
acima (ler-modificar-gravar de novo); `FAILED_PRECONDITION` (9) = não repetir
até o estado do sistema mudar.

- **Deadlines.** Toda chamada precisa de deadline (muitos clientes não têm
  padrão e esperam para sempre). Com deadline curto contra dependência lenta,
  deve voltar `DEADLINE_EXCEEDED` rápido, e o servidor deve propagar o prazo
  restante às chamadas que faz. O cliente não sabe se a operação completou:
  operação com efeito precisa ser idempotente.
- **Streaming.** Cancelar no meio libera recursos no servidor; erro depois de
  N mensagens é tratado pelo cliente; consumidor lento não estoura memória;
  stream longo atrás de proxy precisa de keepalive. Mensagem acima do limite
  de recebimento (4 MB por padrão na maioria das implementações) gera
  `RESOURCE_EXHAUSTED`.
- **Compatibilidade do `.proto`.** Número de campo nunca é reutilizado; campo
  removido vira `reserved`. No CI: `buf breaking --against '.git#branch=main'`.

## Mensageria e eventos

Kafka, RabbitMQ e SQS entregam **pelo menos uma vez**: duplicidade é normal e
o consumidor precisa ser idempotente.

- **Produtor:** publica no destino certo, com chave, headers e schema
  corretos, **uma vez**, e só depois do commit no banco — sem padrão outbox,
  falha entre gravar e publicar perde ou duplica evento (injete essa falha). No
  teste, consuma desde o início (`auto.offset.reset=earliest`, grupo exclusivo)
  e filtre pelo ID criado; com `latest`, a mensagem publicada antes da
  atribuição de partições se perde e o teste fica intermitente.
- **Consumidor:** efeito correto; mesma mensagem duas vezes → um efeito;
  mensagem envenenada vai para a DLQ após N tentativas com o motivo registrado,
  **e as seguintes continuam sendo processadas**.
- **Ordem:** Kafka garante ordem só dentro da partição (mesma chave); SQS
  Standard não garante (FIFO garante por `MessageGroupId` e deduplica em
  janela de 5 minutos); RabbitMQ perde ordem com vários consumidores ou
  reenfileiramento. Teste `pedido.cancelado` chegando antes de `pedido.pago`.
- **Schema registry:** verifique no CI, antes do deploy, a compatibilidade do
  schema novo com o registrado (no Confluent o modo padrão é `BACKWARD`: o
  schema novo lê dados gravados com o anterior).
- **Consistência eventual:** espere pela condição com polling e prazo máximo,
  nunca com `sleep` fixo — curto falha no CI lento, longo desperdiça minutos.

```python
import time


def esperar_ate(condicao, timeout=15.0, intervalo=0.2, descricao="condição"):
    limite = time.monotonic() + timeout
    while not (resultado := condicao()):
        if time.monotonic() >= limite:
            raise AssertionError(f"{descricao} não ocorreu em {timeout} s")
        time.sleep(intervalo)  # intervalo de polling, não espera fixa pelo resultado
    return resultado

# uso: esperar_ate(lambda: repo.buscar(pedido_id).status == "PAGO", descricao="pedido pago")
```

Java: Awaitility, `await().atMost(Duration.ofSeconds(15)).untilAsserted(() ->
assertThat(repo.status(id)).isEqualTo("PAGO"))`. Vitest: `vi.waitFor(fn, {
timeout: 15_000 })`. Playwright: `expect.poll(fn, { timeout: 15_000 })`.
Provar que algo **não** aconteceu exige um marco: espere um evento posterior
processado pelo mesmo consumidor e então confira a ausência.

## Webhooks

- **Assinatura HMAC** sobre o **corpo cru** (bytes recebidos), com timestamp
  dentro do conteúdo assinado e comparação em tempo constante
  (`hmac.compare_digest`). Reserializar o JSON antes de verificar muda os bytes.
- **Casos:** assinatura válida → 2xx; um byte alterado → 401 e nada
  processado; timestamp fora da tolerância (ex.: 5 min) → recusado (replay);
  mesmo ID de evento duas vezes → um efeito; na rotação de segredo, o antigo só
  vale na janela combinada.
- **Retries e ordem:** o emissor reenvia em timeout ou 5xx; responda 2xx
  rápido e processe de forma assíncrona. Eventos chegam fora de ordem: use a
  versão ou o timestamp do evento, ou consulte o estado atual no emissor.

```python
import hashlib, hmac, json, time


def assinar(segredo: bytes, corpo: bytes, ts: int) -> str:
    return hmac.new(segredo, f"{ts}.".encode() + corpo, hashlib.sha256).hexdigest()


corpo, ts = json.dumps({"id": "evt_teste_1", "tipo": "pagamento.aprovado"}).encode(), int(time.time())
r = api.post("/webhooks/pagamentos", content=corpo, headers={"Content-Type": "application/json",
             "X-Timestamp": str(ts), "X-Assinatura": assinar(SEGREDO_DE_TESTE, corpo, ts)})
```

Cabeçalhos e conteúdo assinado variam por provedor; reproduza o do provedor
real. Muitos têm CLI para disparar eventos de teste (ex.:
`stripe trigger payment_intent.succeeded`).

## Teste de contrato

### Consumer-driven com Pact

O consumidor declara o que usa; o Pact gera o contrato rodando o **código real
do cliente** contra um mock; o provedor reproduz cada interação contra a API
verdadeira. Use matchers de tipo e formato: contrato não é teste funcional do
provedor, então regra de negócio não entra nele.

```typescript
// consumidor: test/pedidos.pact.test.ts (Vitest)
import path from 'node:path';
import { MatchersV3, PactV3 } from '@pact-foundation/pact';
import { expect, it } from 'vitest';
import { buscarPedido } from '../src/cliente-pedidos'; // o cliente que vai para produção

const { eachLike, integer, like, regex } = MatchersV3;
const ID = '7f6c2a1e-0000-4000-8000-000000000001';
const provider = new PactV3({ consumer: 'checkout-web', provider: 'pedidos-api',
                              dir: path.resolve(process.cwd(), 'pacts') });

it('obtém um pedido existente', async () => {
  provider
    .given('pedido existe', { id: ID })
    .uponReceiving('consulta de um pedido pelo id')
    .withRequest({ method: 'GET', path: `/pedidos/${ID}`, headers: { Accept: 'application/json' } })
    .willRespondWith({
      status: 200,
      headers: { 'Content-Type': regex('application/json.*', 'application/json') },
      body: { id: like(ID), status: regex('PENDENTE|PAGO|CANCELADO', 'PAGO'), totalCentavos: integer(4990),
              itens: eachLike({ sku: like('CAFE-500G'), quantidade: integer(2) }) },
    });

  await provider.executeTest(async (mock) => {
    expect((await buscarPedido(mock.url, ID)).status).toBe('PAGO');
  });
});
```

```typescript
// provedor: test/pact.verify.test.ts — com a API no ar apontando para um banco de teste
import { Verifier } from '@pact-foundation/pact';
import { it } from 'vitest';
import { semearPedido } from './semear';

it('honra os contratos dos consumidores', async () => {
  await new Verifier({
    provider: 'pedidos-api',
    providerBaseUrl: 'http://localhost:8080',
    pactBrokerUrl: process.env.PACT_BROKER_BASE_URL,
    pactBrokerToken: process.env.PACT_BROKER_TOKEN,
    providerVersion: process.env.GIT_COMMIT,
    providerVersionBranch: process.env.GIT_BRANCH,
    publishVerificationResult: process.env.CI === 'true',
    consumerVersionSelectors: [{ mainBranch: true }, { deployedOrReleased: true }, { matchingBranch: true }],
    enablePending: true,
    stateHandlers: {
      'pedido existe': async (params) => {
        const { id } = params as { id: string };
        await semearPedido({ id, status: 'PAGO', itens: [{ sku: 'CAFE-500G', quantidade: 2 }] });
      },
    },
  }).verifyProvider();
}, 120_000);
```

```bash
# consumidor publica o pact (versão = SHA do commit)
pact-broker publish ./pacts --consumer-app-version "$GIT_COMMIT" --branch "$GIT_BRANCH" \
  --broker-base-url "$PACT_BROKER_BASE_URL" --broker-token "$PACT_BROKER_TOKEN"
# qualquer lado, antes do deploy: é compatível com o que está em produção?
pact-broker can-i-deploy --pacticipant checkout-web --version "$GIT_COMMIT" --to-environment production
# depois do deploy
pact-broker record-deployment --pacticipant checkout-web --version "$GIT_COMMIT" --environment production
```

**Provider states** (`given`) preparam os dados no provedor; parametrize em
vez de depender de um ID que "por acaso" existe. **Pending pacts**
(`enablePending`) impedem que expectativa nova de um consumidor quebre o build
do provedor antes de implementada. Um webhook do broker pode disparar a
verificação no provedor quando um pact muda.

### Contrato por schema (OpenAPI) e quando escolher

- **Schemathesis** gera requisições a partir da especificação e confere as
  respostas (próxima seção).
- **Prism:** `prism mock openapi.yaml` dá um mock para o consumidor;
  `prism proxy openapi.yaml http://localhost:8080 --errors` valida o tráfego
  real contra a especificação.
- **Dredd:** repositório arquivado em novembro de 2024; não use em projeto novo.
- **Quebra de contrato:** compare a especificação nova com a anterior no CI
  (ex.: `oasdiff breaking base.yaml nova.yaml`).

| Situação | Escolha |
| --- | --- |
| Serviços internos, os dois lados sob seu controle, consumidores usando partes diferentes da API | Pact: mostra quem usa o quê e bloqueia o deploy que quebraria alguém |
| API pública ou de parceiros, consumidores desconhecidos | OpenAPI como fonte da verdade + Schemathesis/Prism + diff de especificação |
| Time sem disciplina de broker e versionamento | Comece por schema; Pact mal operado vira contrato velho que ninguém verifica |

Os dois se complementam: conformidade com schema não diz quais campos os
consumidores usam; o Pact não cobre consumidor que não escreveu contrato.

## Fuzzing com Schemathesis

Gera milhares de entradas válidas e inválidas a partir da OpenAPI e encontra
500, resposta fora do schema, validação ausente (`negative_data_rejection`),
autenticação ignorada (`ignored_auth`) e recurso apagado ainda acessível
(`use_after_free`). Todas as checagens vêm ativas por padrão.

```bash
st run openapi.yaml --url http://localhost:8080 -H "Authorization: Bearer $TOKEN" \
  --phases examples,coverage,fuzzing,stateful --max-examples 200 --report junit
```

```python
# tests/test_fuzz_api.py
import os

import schemathesis

schema = schemathesis.openapi.from_path("openapi.yaml")


@schema.parametrize()
def test_api_conforme_a_especificacao(case):
    case.call_and_validate(base_url=os.environ["API_BASE_URL"],
                           headers={"Authorization": f"Bearer {os.environ['API_TOKEN']}"})
```

A fase `stateful` encadeia operações pelos links da OpenAPI (cria → lê →
apaga). Rode em ambiente descartável: fuzzing cria lixo e pode derrubar o
serviço. Cada falha encontrada vira teste de regressão com o caso mínimo.

## Anti-padrões

- **Testar só status:** passa com corpo vazio, valor errado ou erro
  embrulhado em 200.
- **Dependência de ordem:** "criar" guarda o ID em variável global e
  "consultar" usa; falha em paralelo e esconde a causa.
- **Dados compartilhados:** dois testes no mesmo pedido ou usuário colidem em
  paralelo e geram intermitência; cada teste cria o seu.
- **Asserção sobre texto de mensagem:** `detail == "Quantidade inválida"`
  quebra a cada revisão de texto ou tradução; compare `type`/código e o campo.
- **IDs fixos:** `GET /pedidos/123` só funciona no banco de quem escreveu;
  crie o dado ou use provider state.
- **Token fixo no código:** expira, vaza no repositório e mascara falha de
  autenticação; obtenha por fixture com variáveis do ambiente.
- **Oráculo circular:** esperado copiado da resposta anterior ou calculado com
  a mesma função da API.
