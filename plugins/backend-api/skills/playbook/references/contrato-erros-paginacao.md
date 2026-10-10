# Contrato, erros, paginação e evolução

Referência para `api-contract-design` e para o agente `api-contract-reviewer`. Parte vem do brain-of-agent (`backend-e-contratos.md`, MIT), enriquecida com fontes validadas (`V-nn` em `fontes.md`). Rótulos: **Verificado**, **Inferido**, **Suposição**.

## Sumário

- [1. Contrato antes da integração](#1-contrato-antes-da-integração)
- [2. OpenAPI: o que conferir](#2-openapi-o-que-conferir)
- [3. Representação de dados](#3-representação-de-dados)
- [4. Erros: RFC 9457](#4-erros-rfc-9457)
- [5. gRPC: status e retry](#5-grpc-status-e-retry)
- [6. GraphQL: contrato](#6-graphql-contrato)
- [7. Paginação](#7-paginação)
- [8. Condicionais, ETag e cache HTTP](#8-condicionais-etag-e-cache-http)
- [9. Operações longas](#9-operações-longas)
- [10. Compatibilidade e deprecação](#10-compatibilidade-e-deprecação)

## 1. Contrato antes da integração

Inventarie consumidores, métodos, schemas, códigos de resposta, autenticação, autorização, limites, paginação, ordenação e política de compatibilidade. Um exemplo JSON não é contrato: defina ausência x `null`, limites numéricos, representação monetária, fuso, precisão e campos desconhecidos. Schema válido não garante regra de negócio. Use a versão do OpenAPI compatível com as ferramentas do projeto em vez de atualizar apenas por ser a mais recente (brain; V-11).

Consumidores desconhecidos (API pública) exigem a postura mais conservadora: tudo que foi publicado é contrato.

## 2. OpenAPI: o que conferir

Verificado em V-11 (OpenAPI 3.1.1): `openapi` e `info` obrigatórios, mais ao menos um entre `paths`, `components`, `webhooks`. `security` no nível raiz é uma lista de **alternativas** (basta satisfazer uma; `{}` na lista torna a autenticação opcional); `security` na operação **substitui** a global; `[]` na operação a remove (endpoint público).

```yaml
openapi: 3.1.0
info: { title: Pedidos, version: "1.4.0" }
security:
  - bearerAuth: []
paths:
  /health:
    get:
      security: []          # público de propósito; sem isto herdaria bearerAuth
      responses: { "200": { description: ok } }
  /orders:
    post:
      operationId: createOrder
      parameters:
        - { name: Idempotency-Key, in: header, required: true, schema: { type: string, maxLength: 255 } }
      responses:
        "201": { description: criado, headers: { Location: { schema: { type: string } } } }
        "400": { $ref: "#/components/responses/Problem" }
        "409": { $ref: "#/components/responses/Problem" }
        "422": { $ref: "#/components/responses/Problem" }
components:
  securitySchemes:
    bearerAuth: { type: http, scheme: bearer, bearerFormat: JWT }
  responses:
    Problem:
      description: erro (RFC 9457)
      content:
        application/problem+json:
          schema: { $ref: "#/components/schemas/Problem" }
```

Regras: respostas de sucesso **e** de erro por operação; componentes reutilizáveis; exemplos conferidos contra serializers reais; regra que o código não mostra marcada "a confirmar"; tipo genérico (`any`) listado, não inferido; validador do projeto (Spectral ou Redocly, se instalado) como critério de saída, com a saída colada (V-32). Existem OpenAPI 3.2.0 e 3.2.1; confirme o que o validador suporta.

## 3. Representação de dados

| Tema | Regra | Fonte |
| --- | --- | --- |
| Dinheiro | String decimal (`"49.90"`) ou inteiro em centavos com a moeda; nunca float | brain |
| Data e hora | ISO 8601 com fuso (`2026-10-10T14:00:00Z`); datas de fim de intervalo documentadas como inclusivas ou exclusivas | brain |
| Ausente x `null` | Defina: em `PATCH`, `null` limpa o campo e ausente não mexe | brain |
| Campo desconhecido na entrada | Rejeitar (400/422) ou ignorar, conforme contrato; nunca aplicar | brain, V-09 (BOPLA) |
| Campo novo na saída | Compatível; clientes devem ignorar o que não conhecem (RFC 9457 pede o mesmo para extensões) | V-14 |
| IDs | Estáveis e opacos; sem dado pessoal; UUID quando previsibilidade for risco | V-15 (chave sem dado pessoal), *Inferido* |
| Enum | Novo valor **em resposta** quebra consumidor com `switch` exaustivo; documente política de valores desconhecidos | brain, V-35 |

## 4. Erros: RFC 9457

Verificado em V-14: media type `application/problem+json`; membros `type` (URI; padrão `about:blank`), `title`, `status`, `detail`, `instance`; `status` é consultivo e o gerador deve usar o mesmo código do HTTP; extensões são permitidas e clientes ignoram extensões e membros com tipo errado. A RFC 9457 obsoleta a 7807 (a doc do ASP.NET ainda cita 7807, V-22).

```json
{
  "type": "https://api.exemplo.com.br/erros/validacao",
  "title": "Requisição inválida",
  "status": 422,
  "detail": "O campo itens[0].quantidade deve ser um inteiro entre 1 e 10000.",
  "instance": "/orders",
  "erros": [{ "campo": "itens[0].quantidade", "codigo": "fora_da_faixa" }]
}
```

Regras do plugin: `title` estável (não traduza dinamicamente); `type` é URI documentada e estável (clientes decidem por ela, não pelo texto); `detail` sem stack trace, SQL, hostname, caminho de arquivo ou dado pessoal; mesmo formato em todos os endpoints, inclusive 404 de rota, 405, 413, 415, 429 e exceção não prevista; JSON malformado devolve 400 nesse formato. Tabela exceção → status → `type` em `assets/templates/politica-de-erros.md`. Estruturas diferentes por provedor (Azure: `error.code`, `message`, `target`, `details`, V-35) são aceitáveis se o projeto as adotou; o importante é a consistência.

## 5. gRPC: status e retry

V-17 (*Verificado*): 17 códigos, de 0 a 16. A coluna "só da aplicação" lista os sete que a biblioteca gRPC nunca gera sozinha. O mapeamento HTTP não está na página oficial: a coluna é do brain (*Inferido*, aproximado).

| Código | Nome | Só da aplicação | HTTP aprox. | Retry |
| --- | --- | --- | --- | --- |
| 0 | OK | não | 200 | n/a |
| 1 | CANCELLED | não | 499 / 408 | decisão do cliente |
| 2 | UNKNOWN | não | 500 | não, sem entender |
| 3 | INVALID_ARGUMENT | sim | 400 | não até corrigir a entrada |
| 4 | DEADLINE_EXCEEDED | não | 504 | só se idempotente; operação pode ter completado |
| 5 | NOT_FOUND | sim | 404 | não |
| 6 | ALREADY_EXISTS | sim | 409 | não |
| 7 | PERMISSION_DENIED | não | 403 | não |
| 8 | RESOURCE_EXHAUSTED | não | 429 | com backoff, respeitando orientação do servidor |
| 9 | FAILED_PRECONDITION | sim | 400 / 409 | **não** até o estado do sistema mudar |
| 10 | ABORTED | sim | 409 | repetir em nível superior (ler-modificar-gravar de novo) |
| 11 | OUT_OF_RANGE | sim | 400 | não |
| 12 | UNIMPLEMENTED | não | 501 | não |
| 13 | INTERNAL | não | 500 | cuidado |
| 14 | UNAVAILABLE | não | 503 | com backoff; nem sempre seguro para não idempotentes |
| 15 | DATA_LOSS | sim | 500 | não |
| 16 | UNAUTHENTICATED | não | 401 | após renovar credencial |

Toda chamada precisa de deadline; o servidor propaga o prazo restante às chamadas que faz; operação com efeito precisa ser idempotente porque o cliente não sabe se completou (brain). Compatibilidade de `.proto`: nunca reutilize número de campo, marque removidos como `reserved`, rode `buf breaking` no CI (*Inferido*, brain). Limite padrão de ~4 MB por mensagem varia por implementação.

## 6. GraphQL: contrato

Verificado em V-30 (schema) e brain (operação):

- Nulabilidade **intencional**: `[Tipo!]!` para listas; campo anulável só quando a ausência é parte do modelo.
- Listas sem limite viram **conexão** com `first` padrão; páginas por cursor (`pageInfo`, `edges`).
- Mutações com **um** argumento `input`, retornando o objeto afetado, modeladas por ação de negócio (`approveOrder`, não `updateOrder`).
- Depreciar (`@deprecated`) antes de remover; argumento novo com padrão ou anulável; IDs globais e interface `Node`.
- Erros de execução vêm em `errors` com **HTTP 200** e `data` possivelmente parcial: asserções começam por `errors` ausente.
- Segurança e desempenho (brain): limite de profundidade e complexidade; aliases em massa driblam rate limit por requisição; N+1 resolvido com DataLoader e provado por contagem de consultas; introspecção desligada em produção; autorização no resolver do **campo**, não só na entrada; persisted queries como allowlist (APQ sozinho é cache, não segurança).

## 7. Paginação

Regras (V-34, AIP-158, *Verificado*):

1. `page_size` opcional; ausente ou 0 usa o padrão documentado; acima do máximo é reduzido; negativo devolve erro.
2. `page_token` opaco; `next_page_token` vazio sinaliza o fim.
3. Os demais argumentos (filtros, ordenação) devem permanecer iguais entre páginas.
4. Token em base64 transparente não é obfuscação suficiente, e **token não concede autorização**: revalide o acesso a cada página.
5. `total_size` é opcional e pode ser estimativa.
6. Paginação existe desde o primeiro dia: adicionar depois quebra clientes.

Variante Azure (V-35): lista em `value` e `nextLink` absoluto, omitido na última página. Escolha uma forma por API.

```json
{ "itens": [{ "id": "...", "criado_em": "2026-10-10T14:00:00Z" }], "proxima_pagina": "eyJ0IjoiMjAyNi0xMC0xMFQxNDowMDowMFoiLCJpIjo0Mn0" }
```

Ordenação determinística: `ORDER BY criado_em, id`; o cursor codifica o par do último item (codificação interna, assinada se necessário). Casos de teste: `limit` 0, -1, máximo+1 e 10^9; última página; cursor adulterado devolve 400; inserção entre páginas não duplica nem pula.

## 8. Condicionais, ETag e cache HTTP

- `ETag` no `GET`; `If-Match` no `PUT`/`PATCH`/`DELETE`: desatualizado devolve **412**, ausente quando exigido devolve **428**; `If-None-Match` no `GET` devolve **304** (V-35, brain).
- `Cache-Control` (RFC 9111, V-36): `private` para resposta por usuário, `public`/`s-maxage` só para conteúdo realmente compartilhável; `no-store` em dado sensível (V-10); `no-cache` exige revalidação; `must-revalidate` impede servir obsoleto; atenção a cache poisoning e a `Vary`.
- Requisição insegura (`POST`/`PUT`/`DELETE`) invalida cache do alvo.
- Cache de aplicação (cache-aside, TTL, invalidação, stampede, chave com usuário/tenant) está em `idempotencia-resiliencia.md` (*Inferido*).

## 9. Operações longas

Quando o p99 passa de ~1 s (convenção Azure, V-35): `202 Accepted` com `Location`/`operation-location` para o monitor e `Retry-After`; estados terminais explícitos; monitor mantido por no mínimo 24 h; criação do job idempotente; cancelamento definido. Polling com prazo no teste, nunca `sleep` fixo.

## 10. Compatibilidade e deprecação

Compatibilidade é do **significado**. Classificação (brain, V-35, V-30):

| Mudança | Classe |
| --- | --- |
| Campo opcional novo na entrada ou campo novo na saída | compatível |
| Endpoint novo | compatível |
| Campo obrigatório novo na entrada | **breaking** |
| Remover ou renomear campo; mudar tipo, formato ou unidade | **breaking** |
| Novo valor de enum em resposta | **breaking** para consumidor com `switch` exaustivo (política de default no cliente pode neutralizar) |
| Mudar ordenação padrão, tamanho de página padrão ou semântica de `null` | **breaking** |
| Apertar validação (rejeitar o que antes aceitava) | **breaking** |
| Mudar código de status de um cenário | **breaking** |
| `.proto`: reutilizar número de campo | **breaking** (binário) |

Fluxo de deprecação: anunciar com data e substituto; sinalizar nos cabeçalhos `Deprecation` e `Sunset` (RFC 9745: `Deprecation: @<epoch>` e `Link` com `rel="deprecation"`; RFC 8594: `Sunset: <HTTP-date>`, não anterior ao `Deprecation`; Verificado em 2026-10-10); medir uso por versão; manter a versão antiga enquanto houver consumidor; remover só após a data. Diff de spec com oasdiff e `buf breaking` em CI quando disponíveis (`ferramentas-e-mcp.md`); sem a ferramenta, a classificação é manual e rotulada **Inferido**.

Validado em 2026-10-10. Conferir versões de OpenAPI, validadores e RFCs citadas antes de publicar.
