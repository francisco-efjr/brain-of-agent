# Checklist OpenAPI e trecho de referência

Uso: ao escrever ou revisar `openapi.yaml`. Conferido em 2026-10-10 contra OpenAPI 3.1.1 (V-11, Apache-2.0), RFC 9457 (V-14), Google AIP-158 (V-34), Azure REST API Guidelines (V-35, CC BY 4.0; texto aqui é redação própria) e o prompt reescrito de documentação (V-32).

## Sumário

1. Campos e semântica que a spec exige
2. Checklist por spec
3. Trecho completo (3.1) para copiar e adaptar
4. Validação e diff
5. Prompt de geração a partir do código
6. Limites desta referência

## 1. Campos e semântica que a spec exige

- Obrigatórios no documento: `openapi` e `info`, mais ao menos um entre `paths`, `components`, `webhooks` (V-11, Verificado).
- `security` no topo é uma lista de **alternativas**: basta satisfazer uma. `security` na operação **substitui** a global; `[]` remove a exigência; um objeto vazio `{}` dentro da lista torna a autenticação opcional (V-11, Verificado).
- 3.1 alinha o schema com JSON Schema: nulabilidade é `type: [string, "null"]`, não `nullable: true` (3.0). `exclusiveMinimum`/`exclusiveMaximum` são números. Webhooks recebidos ficam em `webhooks:` no topo (Inferido a partir da spec; confira na versão que o projeto usa).
- Versão da spec: use a que as ferramentas do projeto suportam. Existem 3.2.0 e 3.2.1; a base mais suportada por ferramentas é 3.1.x (Inferido). Não migre a versão sem checar Spectral/Redocly/gerador de clientes do projeto.

## 2. Checklist por spec

Marque cada item com evidência (linha do arquivo) ou "Não verificado".

- [ ] `info.version` é a versão do **contrato**, não do build; estratégia de versão do ADR respeitada.
- [ ] Toda operação tem `operationId` único e estável (geradores de cliente dependem dele) e `tags`.
- [ ] `security` explícita **por operação** (ou herança global conscientemente documentada); endpoints públicos têm `security: []`.
- [ ] Parâmetros tipados com limites: `minimum`/`maximum`/`maxLength`/`pattern`; `page_size` com `default` e `maximum`.
- [ ] Corpo com `additionalProperties: false` quando o contrato rejeita campo desconhecido; caso contrário, diga "ignorado" na descrição.
- [ ] Respostas de sucesso **e** de erro por operação: 400/401/403/404/409/422/429 conforme o caso, todas com `application/problem+json` apontando para `components/schemas/Problem`.
- [ ] `201` com `Location`; `202` com `Location`/`Retry-After`; `204` sem corpo; `405` com `Allow`; `429` com `Retry-After`.
- [ ] Listas: `next_page_token` (vazio/ausente no fim), `page_token` opaco; sem `total` obrigatório (se existir, documente que é estimativa).
- [ ] Dinheiro: `type: string` com `pattern: '^-?\d+(\.\d{1,2})?$'` (ou inteiro em centavos com nome `amount_cents`); datas: `format: date-time` com fuso.
- [ ] Enums de **resposta** marcados como abertos na descrição ("clientes devem tolerar valores novos"); enums de entrada são fechados.
- [ ] Header `Idempotency-Key` declarado nas operações com efeito, com a política escolhida (códigos 400/409/422) na descrição.
- [ ] `ETag`/`If-Match` declarados onde há concorrência otimista; 412/428 documentados.
- [ ] Exemplos realistas (`examples`), conferidos contra o serializer; nenhum dado pessoal real.
- [ ] Componentes reutilizados via `$ref`; nenhum schema duplicado por cópia.
- [ ] Campos marcados `deprecated: true` trazem na descrição o substituto e a data do `Sunset`.
- [ ] Regra que o código não mostra está marcada "a confirmar"; nada inventado.

## 3. Trecho completo (3.1)

Exemplo mínimo e válido de um recurso `orders`. Adapte nomes, limites e política de erros; as decisões (cursor, códigos, idempotência) são do ADR do projeto.

```yaml
openapi: 3.1.0
info:
  title: Orders API
  version: 1.0.0
servers:
  - url: https://api.exemplo.com.br/v1
security:
  - bearerAuth: []
paths:
  /orders:
    get:
      operationId: listOrders
      tags: [orders]
      summary: Lista pedidos do chamador, mais recentes primeiro.
      parameters:
        - name: page_size
          in: query
          schema: { type: integer, minimum: 1, maximum: 100, default: 25 }
        - name: page_token
          in: query
          description: Token opaco devolvido em next_page_token. Os demais parâmetros devem ser iguais aos da primeira página.
          schema: { type: string, maxLength: 512 }
      responses:
        "200":
          description: Página de pedidos. Ordenação por (created_at desc, id desc).
          content:
            application/json:
              schema: { $ref: "#/components/schemas/OrderPage" }
        "400": { $ref: "#/components/responses/Problem" }
        "401": { $ref: "#/components/responses/Problem" }
        "429": { $ref: "#/components/responses/Problem" }
    post:
      operationId: createOrder
      tags: [orders]
      summary: Cria um pedido. Idempotente por Idempotency-Key.
      parameters:
        - name: Idempotency-Key
          in: header
          required: true
          description: >
            UUID gerado pelo cliente. Mesma chave e mesmo corpo devolvem a resposta original;
            corpo diferente responde 422; original em processamento responde 409. Retenção: 24 h.
          schema: { type: string, format: uuid }
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/OrderCreate" }
      responses:
        "201":
          description: Pedido criado.
          headers:
            Location: { schema: { type: string, format: uri-reference } }
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Order" }
        "400": { $ref: "#/components/responses/Problem" }
        "401": { $ref: "#/components/responses/Problem" }
        "409": { $ref: "#/components/responses/Problem" }
        "422": { $ref: "#/components/responses/Problem" }
        "429": { $ref: "#/components/responses/Problem" }
  /orders/{orderId}:
    get:
      operationId: getOrder
      tags: [orders]
      parameters:
        - name: orderId
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        "200":
          description: O pedido. Pedido de outro cliente responde 404, igual a inexistente.
          headers:
            ETag: { schema: { type: string } }
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Order" }
        "401": { $ref: "#/components/responses/Problem" }
        "404": { $ref: "#/components/responses/Problem" }
components:
  securitySchemes:
    bearerAuth: { type: http, scheme: bearer, bearerFormat: JWT }
  responses:
    Problem:
      description: Erro no formato RFC 9457.
      content:
        application/problem+json:
          schema: { $ref: "#/components/schemas/Problem" }
  schemas:
    Problem:
      type: object
      required: [type, title, status]
      properties:
        type:
          type: string
          format: uri-reference
          description: "URI documentada que identifica o erro."
        title:
          type: string
          description: "Resumo estável; não varia por ocorrência."
        status:
          type: integer
          description: "Igual ao status HTTP da resposta."
        detail:
          type: string
          description: "Explicação desta ocorrência, sem stack trace, SQL, hostname ou dado sensível."
        instance: { type: string, format: uri-reference }
        errors:
          type: array
          description: "Extensão para campos inválidos."
          items:
            type: object
            required: [field, code]
            properties:
              field: { type: string }
              code: { type: string }
    OrderCreate:
      type: object
      additionalProperties: false
      required: [items]
      properties:
        note: { type: [string, "null"], maxLength: 500, description: Ausente não altera; null limpa. }
        items:
          type: array
          minItems: 1
          maxItems: 100
          items:
            type: object
            additionalProperties: false
            required: [sku, quantity]
            properties:
              sku: { type: string, maxLength: 64 }
              quantity: { type: integer, minimum: 1, maximum: 10000 }
    Order:
      type: object
      required: [id, status, total, created_at]
      properties:
        id: { type: string, format: uuid }
        status:
          type: string
          description: Enum aberto; clientes devem tolerar valores novos.
          examples: [PENDING]
        total: { type: string, pattern: '^\d+\.\d{2}$', examples: ["49.90"] }
        created_at: { type: string, format: date-time }
    OrderPage:
      type: object
      required: [items]
      properties:
        items: { type: array, items: { $ref: "#/components/schemas/Order" } }
        next_page_token:
          type: string
          description: Ausente ou vazio na última página.
```

O exemplo usa `examples` em 3.1 (lista). Em 3.0 o campo é `example`. Rode o validador do projeto; o trecho foi escrito para 3.1.0 e não foi executado contra ferramenta nesta sessão (**Não verificado** por validador).

## 4. Validação e diff

Use o que o projeto já tem; confira flags na versão instalada (Não verificado aqui):

```bash
spectral lint openapi.yaml                       # lint de regras (se Spectral instalado)
redocly lint openapi.yaml                        # alternativa
oasdiff breaking base.yaml openapi.yaml          # mudanças que quebram (base = versão publicada)
```

Sem ferramenta instalada, declare **Não verificado**; não instale `npx`/pacotes por conta própria (supply chain). Para obter `base.yaml`, use `git show <tag>:openapi.yaml > base.yaml`.

## 5. Prompt de geração a partir do código

Versão reescrita de V-32 (fonte original: GitHub Docs, prompt "document-api"; redação própria):

```text
Leia os handlers de [ESCOPO] e produza OpenAPI [3.1.x] em YAML.
Inclua para cada operação: parâmetros tipados, corpo, respostas de sucesso e de erro (RFC 9457),
exemplos realistas, security explícita e componentes reutilizáveis.
Não invente regra de negócio que o código não mostra: marque como "a confirmar".
Se um handler usa tipo genérico (any), liste-o em vez de inferir o schema.
Critério de saída: rode o validador de spec do projeto e cole a saída; sem validador, diga "Não verificado".
```

## 6. Limites desta referência

Cerca de 60% do texto da spec 3.1.1 (paths/responses) não foi lido na pesquisa (V-11); os itens de 3.1 sobre `type` array, `examples` e `webhooks` vêm de conhecimento estável do domínio e estão rotulados Inferido. A regra de retenção de 24 h do exemplo é decisão ilustrativa do projeto, não padrão.
