# GraphQL: schema, erros, desempenho e segurança

Fontes: skill `graphql-schema` de apollographql/skills (V-30, MIT, versão 1.0.2; checklist original reescrito em tom calmo, com redação própria); brain-of-agent `automacao-api`, seção GraphQL (MIT, incorporado); OWASP API Security Top 10 2023 (V-09). A skill do Apollo cobre **só schema**: N+1/DataLoader, autorização em resolvers, profundidade e persisted queries vêm do brain e de conhecimento estável do domínio (Inferido; lacuna registrada em `fontes.md` do playbook). Confira a documentação do servidor GraphQL usado (Apollo Server, graphql-java, Hot Chocolate, gqlgen, Strawberry etc.) na versão instalada.

## Sumário

1. Checklist de schema
2. Exemplo de schema
3. Erros
4. Desempenho: N+1 e custo de consulta
5. Segurança
6. Testes
7. Evolução e deprecação

## 1. Checklist de schema

- [ ] **Nulabilidade intencional**: campo é `T!` só se sempre existe; listas como `[Tipo!]!` (lista e elementos não nulos) salvo motivo (V-30).
- [ ] Listas sem limite natural viram **conexão** com `first` padrão e máximo (paginação por cursor); lista crua só para conjuntos pequenos e fechados (V-30).
- [ ] Mutations com um único argumento `input`, retornando o objeto afetado (e, se necessário, erros de domínio tipados), modeladas por **ação de negócio** (`cancelOrder`, não `updateOrder`) (V-30).
- [ ] IDs globais e interface `Node` quando o cliente refaz busca por ID (V-30).
- [ ] Argumento novo com valor padrão ou anulável; senão quebra queries existentes (V-30).
- [ ] **Depreciar antes de remover** (`@deprecated(reason:)`), com medição de uso (V-30).
- [ ] Autorização no **resolver do campo** (ou camada de domínio), não no ponto de entrada: o mesmo dado é alcançável por vários caminhos (brain).
- [ ] Limites de profundidade, complexidade e **aliases em massa**; introspecção desligada em produção; persisted queries como allowlist (brain).
- [ ] N+1 resolvido por batching (DataLoader) e provado por contagem de consultas.
- [ ] Erro em `errors` com `extensions.code` estável; HTTP 200 não indica sucesso (brain).

## 2. Exemplo de schema

```graphql
interface Node { id: ID! }

type Order implements Node {
  id: ID!
  status: OrderStatus!
  total: Money!
  customer: Customer!          # pode disparar N+1: use DataLoader
  items(first: Int = 20, after: String): OrderItemConnection!
}

enum OrderStatus { PENDING PAID CANCELLED }   # enum de saída é aberto na prática: cliente tolera valor novo

type OrderConnection { edges: [OrderEdge!]!  pageInfo: PageInfo! }
type OrderEdge { node: Order!  cursor: String! }
type PageInfo { hasNextPage: Boolean!  endCursor: String }

type Query {
  order(id: ID!): Order                       # anulável: alheio e inexistente indistinguíveis (null)
  orders(first: Int = 20, after: String, status: OrderStatus): OrderConnection!
}

input CancelOrderInput { orderId: ID!  reason: String! }
type CancelOrderPayload { order: Order  userErrors: [UserError!]! }
type UserError { code: String!  message: String!  field: [String!] }

type Mutation {
  cancelOrder(input: CancelOrderInput!): CancelOrderPayload!
}
```

Notas: `order(id)` anulável porque "não existe ou não é seu" devolve `null` (equivalente ao 404 indistinguível do REST). `first` com padrão **e máximo no servidor** (o SDL não expressa máximo). Dinheiro como escalar customizado `Money` serializado como string decimal.

## 3. Erros

- Erro de execução chega em `errors` com **HTTP 200** e `data` possivelmente parcial (`null` nos campos que falharam) (brain). Clientes e testes começam por `errors` ausente; só o status é falso verde garantido.
- Erros de negócio esperados (saldo insuficiente, pedido não cancelável) vão no payload tipado (`userErrors`), não como exceção; erros inesperados vão em `errors` com `extensions.code` estável e sem stack/SQL.
- Falha de autenticação/transporte (token inválido) pode usar o status HTTP 401 antes de executar a query; documente a escolha do projeto.
- Não devolva mensagens do banco nem sugestões de campo ("Did you mean ...") em produção: vazam o schema (brain).

## 4. Desempenho: N+1 e custo de consulta

- N+1: lista com campo aninhado sem batching dispara uma consulta por item. Prova: contar consultas com 1 e com 50 itens; devem ser (quase) constantes. DataLoader (ou equivalente do servidor) agrupa buscas por chave dentro do mesmo tick/pedido; o loader é **por requisição** (cache de loader global vaza dado entre usuários).
- Recuse consultas aninhadas demais (`pedido { cliente { pedidos { cliente { ... } } } }`) e listas dentro de listas **antes** de executar: limite de profundidade e de complexidade/custo estimado (brain).
- Aliases em massa (`a1: login(...) ... a1000: login(...)`) driblam rate limit por requisição: limite a quantidade de campos/aliases e aplique rate limit por operação (brain).
- Paginação obrigatória nas conexões; `first` máximo no servidor; tempo máximo de execução por consulta.

## 5. Segurança

- **Autorização por campo**: `pedido.cliente.cpf` e `usuario.cpf` são caminhos diferentes para o mesmo dado: a regra mora no resolver do campo (ou no domínio), testada em **cada caminho** com perfil sem acesso (brain). BOLA continua valendo: `order(id)` filtra por dono.
- **Introspecção** em produção: `{ __schema { types { name } } }` deve falhar (brain); verifique também as sugestões de campo.
- **Persisted queries** em produção: aceite só documentos registrados (allowlist). APQ (automatic persisted queries) sozinho é otimização de cache, **não** controle de segurança (brain).
- Mutations repetíveis (cobrança, envio) aceitam chave de idempotência (`input.idempotencyKey` ou header); ver `idempotency-and-resilience`.
- Upload, subscriptions e federation: não cobertos pelas fontes; trate como lacuna e declare "Não verificado".

## 6. Testes

- Toda asserção começa por `errors` ausente; depois confira `data` com oráculo independente.
- Contagem de consultas ao banco com 1 e 50 itens (N+1).
- Profundidade acima do limite é recusada; 1.000 aliases são recusados; introspecção falha em produção; campo protegido falha para cada caminho com perfil sem acesso.
- Compatibilidade do schema: diff do SDL contra a versão publicada em CI (a ferramenta depende do servidor; confira o ecossistema do projeto).

Exemplos de código de teste: `${CLAUDE_PLUGIN_ROOT}/skills/api-test-suite/references/exemplos-contrato-fuzz.md`.

## 7. Evolução e deprecação

Depreciar com motivo e substituto antes de remover; medir uso do campo (registro de operações/persisted queries) antes de qualquer remoção; argumento novo com padrão ou anulável; valor novo em `enum` de saída é breaking para consumidor com `switch` exaustivo; mudar nulabilidade de saída tem risco nos dois sentidos. Regras completas: `${CLAUDE_PLUGIN_ROOT}/skills/api-contract-design/references/compatibilidade.md`.
