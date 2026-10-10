# Template: esqueleto OpenAPI com descrições

Fontes: OpenAPI Specification 3.2.1 (V-24; publicada em 2026-09-10), OpenAPI Best Practices da OAI (CC BY 4.0, V-41), checklist de campo inspirado no AIP-192 (CC BY 4.0, redação própria). Antes de usar, descubra a **fonte única da verdade** da API: se já existe contrato, edite-o em vez de criar outro. Compatibilidade das ferramentas do projeto com 3.2.x: Não verificada; confira a versão suportada. Valide o contrato com a ferramenta do projeto (não executado aqui).

````yaml
openapi: "3.2.1"      # entre aspas: 3.1 sem aspas viraria número no YAML
info:
  title: [NOME DA API]
  version: "[VERSÃO DO DOCUMENTO]"   # versão do documento, não da API nem da spec
  description: >
    [O que a API faz e para quem, em duas frases.]
tags:
  - name: pedidos
    description: [Operações sobre pedidos.]
paths:
  /pedidos/{id}:
    get:
      tags: [pedidos]
      summary: Obtém um pedido
      description: >
        Retorna o pedido com o identificador informado. Não altera estado e é idempotente.
        Erros comuns: 404 se o pedido não existe; 403 se pertence a outro cliente.
      operationId: obterPedido
      parameters:
        - name: id
          in: path
          required: true
          description: Identificador do pedido (UUID v4).
          schema:
            type: string
            format: uuid
      responses:
        "200":
          description: Pedido encontrado.
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Pedido"
        "404":
          description: Pedido inexistente.
components:
  schemas:
    Pedido:
      type: object
      required: [id, total]
      properties:
        id:
          type: string
          format: uuid
          description: Identificador único do pedido. Sempre presente.
        total:
          type: integer
          description: Valor total em centavos. Sempre presente; maior ou igual a zero.
````

## Boas práticas (OAI)

- Escreva a descrição antes do código quando possível; trate-a como código-fonte versionado e validado em CI.
- Uma única fonte da verdade; com duas, checagem de consistência.
- Reutilize com `components` e `$ref`; agrupe com `tags`; divida arquivos grandes pela hierarquia de URL.
- Exemplos de requisição e resposta só de execuções reais ou marcados "ilustrativo".
- Deprecação: `deprecated: true` e primeira linha "Deprecated:" com a alternativa.

O esqueleto acima é ilustrativo (estrutura comum a OpenAPI 3.x); não foi validado por ferramenta nesta etapa.
