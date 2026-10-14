# Suítes de API em Playwright, REST Assured, supertest e coleções (Postman/Bruno)

Origem: brain-of-agent, `brains/qa/references/automacao-api.md` (autor Francisco Edson / francisco-efjr, licença MIT; conteúdo próprio do usuário, incorporado e adaptado). Código de exemplo: confira as APIs das bibliotecas na versão instalada no projeto (as versões não foram reverificadas nesta cadeia: **Inferido**). Exemplos nunca devem rodar contra produção; credenciais entram por variável de ambiente.

Escolha pelo stack do projeto. Playwright quando o E2E já é Playwright (mesma configuração, relatório e trace); REST Assured em Java; supertest + Vitest/Jest em APIs Node testadas em processo; Postman/Newman/Bruno para smoke e coleções compartilhadas, não para regressão complexa.

## Sumário

- Exemplo: Playwright APIRequestContext
- Exemplo: REST Assured (Java)
- Exemplo: supertest + Vitest
- Postman/Newman e Bruno

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

O Playwright não cobre contrato, schema OpenAPI nem carga; use Pact, Schemathesis ou k6 conforme esta skill.

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
