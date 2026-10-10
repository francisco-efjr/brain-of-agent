# Documentação de API: contrato, checklist e changelog

Conteúdo: 1 princípios · 2 checklist de campo e operação · 3 esqueleto OpenAPI · 4 exemplo de operação documentada · 5 deprecação · 6 changelog de API · 7 limites.

Fontes (redação própria): AIP-192 do Google (CC BY 4.0; escrito para protobuf), "OpenAPI Best Practices" da OpenAPI Initiative (CC BY 4.0), especificação OpenAPI 3.2.1 (V-24), estrutura do changelog da Stripe (só estrutura; termos não lidos). Itens V-24 e V-41. Rótulo: Verificado nas fontes; o exemplo é ilustrativo.

## 1. Princípios

- **Uma única fonte da verdade.** Descrição no contrato versionado ou nas anotações do código, não nos dois. Com duas fontes, checagem de consistência no CI.
- Escreva a descrição antes do código quando possível; trate-a como código-fonte (versionada, revisada, validada em CI) e publique-a para os consumidores.
- Reutilize com `components` e `$ref`; agrupe operações com `tags`; divida arquivos grandes pela hierarquia de URL.

## 2. Checklist de campo e operação

Para cada operação, parâmetro, corpo e campo, responda em uma ou duas frases (omita o que não se aplica, mas decida conscientemente):

- [ ] **O que é** (primeira frase, sem sujeito, terceira pessoa do presente: "Cria um pedido para o cliente informado.").
- [ ] **Como é usado** e por quem; relação com outros campos.
- [ ] **Unidade, formato e faixa** (centavos, ISO 8601, 1 a 100).
- [ ] **Presença:** sempre presente, opcional, nulo?
- [ ] **Valor padrão** quando omitido.
- [ ] **Efeitos colaterais** (envia e-mail, cobra, cria recurso derivado).
- [ ] **Erros comuns** e o que significam (códigos de status e causas).
- [ ] **Sucesso e falha:** o que o cliente recebe em cada caso.
- [ ] **Idempotência:** repetir a chamada é seguro? Como (chave de idempotência, PUT)?
- [ ] **Deprecação:** alternativa e data, se houver.

Para comentários em protobuf (AIP-192): CommonMark, sem títulos, tabelas nem HTML bruto, sem arte ASCII (use link para imagem). Essa sintaxe é do AIP; em OpenAPI o checklist vale, as restrições de sintaxe seguem o que o seu renderizador aceita.

## 3. Esqueleto OpenAPI mínimo

```yaml
openapi: "3.2.1"   # entre aspas: "3.1" sem aspas viraria número em YAML
info:
  title: API de Pedidos
  version: "2026-10-10"   # versão do DOCUMENTO, não da API nem da especificação
paths: {}
```

Campos obrigatórios da raiz: `openapi` e `info` (com `title` e `version`), mais ao menos um entre `paths`, `components`, `webhooks` (V-24). Compatibilidade das ferramentas do projeto com 3.2.x: Não verificada; confira o suporte antes de adotar a versão.

## 4. Exemplo de operação documentada (ilustrativo, não validado)

```yaml
openapi: "3.2.1"
info:
  title: API de Pedidos
  version: "2026-10-10"
tags:
  - name: pedidos
    description: Criação e consulta de pedidos.
paths:
  /pedidos:
    post:
      tags: [pedidos]
      operationId: criarPedido
      summary: Cria um pedido
      description: >-
        Cria um pedido para o cliente informado e reserva o estoque dos itens.
        Cobra o pagamento somente após a confirmação em `POST /pedidos/{id}/confirmacao`.
        Chamadas repetidas com o mesmo `Idempotency-Key` devolvem o pedido original
        sem criar outro.
      parameters:
        - name: Idempotency-Key
          in: header
          required: true
          description: >-
            Identificador único da tentativa, até 64 caracteres. Reaproveitar a chave
            com outro corpo devolve 409.
          schema: { type: string, maxLength: 64 }
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/NovoPedido" }
      responses:
        "201":
          description: Pedido criado. O corpo traz o `id` e o status `aguardando_pagamento`.
        "409":
          description: Chave de idempotência reutilizada com corpo diferente.
components:
  schemas:
    NovoPedido:
      type: object
      required: [clienteId, itens]
      properties:
        clienteId:
          type: string
          description: Identificador do cliente, no formato UUID. Sempre obrigatório.
        itens:
          type: array
          minItems: 1
          maxItems: 100
          description: Itens do pedido. Cada item reserva estoque ao criar o pedido.
          items:
            type: object
            required: [sku, quantidade]
            properties:
              sku: { type: string, description: Código do produto no catálogo. }
              quantidade: { type: integer, minimum: 1, description: Unidades desejadas. }
```

O que a descrição mostra: efeito colateral (reserva estoque), quando cobra, idempotência e seu erro (409), faixas (`minItems`, `maxLength`), obrigatoriedade. `Idempotency-Key` e os caminhos são fictícios: no uso real, cada afirmação vem do código ou do contrato lido. O YAML não foi validado por ferramenta de OpenAPI.

## 5. Deprecação

```yaml
      deprecated: true
      description: >-
        Deprecated: use `POST /v2/pedidos`, que aceita cupom e frete. Esta operação
        será removida após 2027-03-31.
```

`deprecated: true` é o campo; a primeira linha "Deprecated:" com alternativa e prazo é a convenção do AIP-192. Datas e prazos vêm do dono da API; não os invente.

## 6. Changelog de API (tabela)

Estrutura inspirada no changelog da Stripe (versões datadas, indicação de quebra), em formato simples:

| Data | Mudança | Área afetada | Quebra? | Canal |
| --- | --- | --- | --- | --- |
| 2026-10-10 | Campo `cupom` opcional em `POST /pedidos` | pedidos | Não | estável |
| 2026-10-10 | `GET /v1/pedidos` removido | pedidos | Sim | estável |

Quebra de compatibilidade sempre marcada. Quem decide o que é quebra e a política de versionamento: plugin `backend-api`. Texto para o usuário final do produto: `escrever-changelog-release`.

## 7. Limites

- Não há skill ou prompt validado de coleta para docs de API (V-41): este fluxo é redação própria.
- A página da Stripe foi lida em parte (100 mil de 225 mil caracteres) e seus termos não foram lidos: só a estrutura serve de inspiração.
- As Microsoft REST API Guidelines tratam de projeto de API, não de autoria de documentação.
