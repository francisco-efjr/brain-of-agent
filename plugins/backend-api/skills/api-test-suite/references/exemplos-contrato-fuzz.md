# Testes de GraphQL, gRPC, contrato (Pact, OpenAPI) e fuzz (Schemathesis)

Origem: brain-of-agent, `brains/qa/references/automacao-api.md` (autor Francisco Edson / francisco-efjr, licença MIT; conteúdo próprio do usuário, incorporado e adaptado). Código de exemplo: confira as APIs das bibliotecas na versão instalada no projeto (as versões não foram reverificadas nesta cadeia: **Inferido**). Exemplos nunca devem rodar contra produção; credenciais entram por variável de ambiente.

Notas de verificação: a sintaxe de Pact (`PactV3`, `Verifier`, `pact-broker`), Schemathesis (`st run`, `schemathesis.openapi.from_path`), Prism, oasdiff e buf vem do brain e **não foi reverificada** contra a documentação atual; versões maiores dessas ferramentas mudaram APIs no passado, então confirme na versão instalada. "Dredd arquivado em novembro de 2024" é fato do brain não reverificado (Inferido). Fuzz e estado só em ambiente descartável e autorizado.

## Sumário

- GraphQL
- gRPC
- Teste de contrato (Pact; contrato por schema; quando escolher)
- Fuzzing com Schemathesis

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
