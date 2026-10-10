# Exemplo de contrato: pedidos

Sumário: 1. Pedido de exemplo · 2. Trecho OpenAPI 3.1 · 3. Payloads de erro e de página · 4. Fluxo de Idempotency-Key · 5. Operação assíncrona com 202 · 6. Revisão do contrato antigo · 7. Gotchas

Exemplo ilustrativo e fictício (domínio, domínios de URL e números inventados). Fontes de método: V-39, V-40, V-41, N-02 (RFC 9457), N-03 (rascunho expirado), N-04. Os blocos JSON abaixo foram validados por parse (json.loads) em 2026-10-10 (Verificado); o trecho YAML foi escrito à mão e **não** foi validado por lint de OpenAPI (Não verificável aqui: rode o linter de sua escolha; comandos em `ferramentas-e-mcp.md` do playbook).

## 1. Pedido de exemplo

> "Defina o contrato de `GET /orders` com cerca de 10 milhões de linhas que mudam o tempo todo, paginação, filtro por status e erros de validação; hoje usamos `{error: 'msg'}`."

Decisões: cursor opaco com ordenação `(created_at DESC, id DESC)`; filtro `status`; `limit` padrão 50 e máximo 100 (Suposição, ajustar com medição); erros em `application/problem+json`; mudança de formato de erro tratada como quebrante, com expand/contract (seção 6).

## 2. Trecho OpenAPI 3.1

```yaml
openapi: 3.1.0
info:
  title: Orders API
  version: 1.0.0
paths:
  /orders:
    get:
      summary: Lista pedidos com paginação por cursor
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, paid, shipped, cancelled]
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 50
        - name: cursor
          in: query
          description: Cursor opaco devolvido em next_cursor. Não montar nem interpretar.
          schema:
            type: string
      responses:
        "200":
          description: Página de pedidos
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/OrderPage"
        default:
          $ref: "#/components/responses/Problem"
    post:
      summary: Cria um pedido (idempotente por Idempotency-Key)
      parameters:
        - name: Idempotency-Key
          in: header
          required: true
          description: Valor único por tentativa lógica, gerado pelo cliente.
          schema:
            type: string
            maxLength: 255
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/NewOrder"
      responses:
        "201":
          description: Pedido criado
          headers:
            Location:
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Order"
        default:
          $ref: "#/components/responses/Problem"
components:
  responses:
    Problem:
      description: Erro no formato Problem Details (RFC 9457)
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/Problem"
  schemas:
    Order:
      type: object
      required: [id, status, created_at]
      properties:
        id:
          type: string
        status:
          type: string
        created_at:
          type: string
          format: date-time
    NewOrder:
      type: object
      required: [items]
      properties:
        items:
          type: array
          minItems: 1
          items:
            type: object
            required: [sku, quantity]
            properties:
              sku:
                type: string
              quantity:
                type: integer
                minimum: 1
    OrderPage:
      type: object
      required: [items, next_cursor]
      properties:
        items:
          type: array
          items:
            $ref: "#/components/schemas/Order"
        next_cursor:
          type: [string, "null"]
    Problem:
      type: object
      required: [type, title, status]
      properties:
        type:
          type: string
          format: uri-reference
        title:
          type: string
        status:
          type: integer
        detail:
          type: string
        instance:
          type: string
          format: uri-reference
        errors:
          type: array
          items:
            type: object
            properties:
              pointer:
                type: string
              detail:
                type: string
```

Observações: a RFC 9457 torna todos os membros opcionais (o `type` padrão é `about:blank`); exigir `type`, `title` e `status` é escolha do contrato local. A extensão `errors` com ponteiro JSON é estrutura local: a RFC permite membros de extensão. Valores monetários, quando existirem, em inteiro (centavos) ou string decimal.

## 3. Payloads de erro e de página

Erro de validação (`422`, `Content-Type: application/problem+json`):

```json
{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Os dados enviados são inválidos.",
  "status": 422,
  "detail": "2 campos falharam na validação.",
  "instance": "/orders",
  "errors": [
    { "pointer": "/items/0/quantity", "detail": "deve ser maior ou igual a 1" },
    { "pointer": "/items/1/sku", "detail": "campo obrigatório" }
  ]
}
```

Recurso inexistente (`404`):

```json
{
  "type": "https://api.example.com/problems/order-not-found",
  "title": "Pedido não encontrado.",
  "status": 404,
  "detail": "Nenhum pedido com o identificador informado.",
  "instance": "/orders/ord_9z"
}
```

Conflito de versão (`412`, requisição com `If-Match` desatualizado):

```json
{
  "type": "https://api.example.com/problems/stale-version",
  "title": "A versão do pedido mudou.",
  "status": 412,
  "detail": "Releia o pedido e reaplique a alteração.",
  "instance": "/orders/ord_9z"
}
```

Página de resultados e última página:

```json
{
  "items": [
    { "id": "ord_9z", "status": "paid", "created_at": "2026-10-10T12:00:03Z" },
    { "id": "ord_9y", "status": "paid", "created_at": "2026-10-10T12:00:01Z" }
  ],
  "next_cursor": "eyJjIjoiMjAyNi0xMC0xMFQxMjowMDowMVoiLCJpIjoib3JkXzl5In0"
}
```

```json
{
  "items": [
    { "id": "ord_01", "status": "shipped", "created_at": "2026-01-02T09:00:00Z" }
  ],
  "next_cursor": null
}
```

Os `type` usam um domínio reservado para exemplos (`example.com`); em produção devem apontar para documentação estável.

## 4. Fluxo de Idempotency-Key (convenção; semântica local)

Convenção ampla, sem RFC (rascunho do IETF expirado, N-03). Defina no contrato:

| Situação | Comportamento sugerido | Estado de verificação |
| --- | --- | --- |
| Primeira requisição com a chave K | Processa e armazena (K, hash do corpo, resposta) | Padrão de prática (Inferido) |
| Repetição com K e o mesmo corpo | Devolve a resposta original, sem novo efeito | Inferido |
| Chave ausente em endpoint que a exige | Rejeita com 400 | Verificado no rascunho 07 (SHOULD) |
| K reutilizada com corpo diferente | Rejeita com 422 | Verificado no rascunho 07 (SHOULD) |
| Repetição enquanto a original ainda processa | Rejeita com 409 | Verificado no rascunho 07 (SHOULD) |
| Escopo e retenção | Chave vale por credencial e endpoint; TTL de retenção declarado (Suposição: 24 h) | Decisão local |

Implementação: marcador (credencial, chave) com restrição de unicidade, gravado na mesma transação do efeito (consumidor idempotente, skill `resilience-and-consistency`).

## 5. Operação assíncrona com 202

Pedido de relatório pesado:

```text
POST /reports            -> 202 Accepted, Location: /reports/rep_1/status
GET  /reports/rep_1/status -> 200 {"state":"running"}   (ou 200 {"state":"done","result":"/reports/rep_1"})
```

Estados documentados (`queued`, `running`, `done`, `failed` com problem+json no campo de erro); `Retry-After` orienta o polling; limite de tempo de retenção do resultado.

## 6. Revisão do contrato antigo (`{error: 'msg'}`)

Achados (formato `ARQ-nn`, confianças ilustrativas):

| ID | Severidade | Evidência | Cenário | Ação |
| --- | --- | --- | --- | --- |
| ARQ-01 | Médio | formato de erro atual | Clientes só podem comparar texto livre; mensagem muda e quebra tratamento | Adotar RFC 9457 com catálogo de `type` |
| ARQ-02 | Alto | `GET /orders?page=N` | Offset em 10 milhões de linhas voláteis: páginas profundas lentas e itens repetidos ou omitidos | Cursor com ordenação estável (seção 5 do checklist) |
| ARQ-03 | Alto | `POST /orders` sem chave | Retry de rede cria pedido duplicado | `Idempotency-Key` com escopo e TTL |

Migração do formato de erro sem quebrar clientes (expand/contract, N-04): (1) expandir: manter `error` e acrescentar os membros de Problem Details no mesmo corpo, com `Content-Type` ainda `application/json` para clientes antigos; (2) migrar: publicar `application/problem+json` para clientes que o pedirem via `Accept`, medir uso; (3) contrair: remover `error` após o prazo de depreciação comunicado. Cada etapa é um deploy separado.

## 7. Gotchas

- Mesmo código de status com corpos de formatos diferentes entre endpoints é o defeito mais comum em APIs antigas: padronize o erro na camada comum, não por endpoint.
- Exemplo de erro sem `instance` ou `type` estável não ajuda quem faz suporte.
- `next_cursor: null` na última página é mais claro que omitir o campo.
- Os códigos 400, 422 e 409 vêm do texto da revisão 07 do rascunho (https://www.ietf.org/archive/id/draft-ietf-httpapi-idempotency-key-header-07.html, conferido em 2026-10-10). O rascunho expirou sem virar RFC: registre a escolha no contrato local.
