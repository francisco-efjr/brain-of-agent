# Endpoint SCIM: contrato, exemplos e aceite

Redação própria; fontes: RFC 7643 e 7644 (IETF), atualizadas pelas RFC 9865 (paginação por cursor) e 9967 (perfil para SETs), Entra e Okta (V-10, V-36, V-54, V-55). Conferido em 2026-10-10. Rótulos: Verificado (lido na fonte), Inferido (nosso), Não verificável. Limites de leitura: RFC 7644 lida nos primeiros 100 mil de 194 mil caracteres na primeira rodada e a seção 7 na segunda; RFC 7643 lida até a seção 4.2 (V-36). Antes de implementar, leia os trechos de schema que faltam.

## 1. Escopo do token e do tenant

- Um token SCIM pertence a um único tenant. O tenant da requisição sai do token, nunca da URL, do corpo ou de header livre. Se houver prefixo no caminho (`/scim/v2/{slug}/Users`), ele só é aceito se corresponder ao tenant do token; divergência responde 404 (Inferido).
- O token é um segredo com entropia e vida limitada; guarde só o hash; rotacionável; uso registrado na auditoria. TLS 1.2 ou superior; Basic evitado; nunca em log (RFC 7644 §§ 2 e 7, V-10, V-36).
- Recursos de outro tenant respondem 404 igual a "não existe". Teste: token do tenant A em `GET /Users/{id do B}` dá 404.

## 2. Recursos e semântica (Verificado nas RFCs lidas)

| Tema | Regra |
| --- | --- |
| `userName` | obrigatório, único no provedor, sem diferenciar maiúsculas (RFC 7643) |
| `id` e `meta` | atribuídos pelo servidor, somente leitura |
| `externalId` | opcional, definido pelo cliente (IdP); guarde para correlação |
| `active` | status administrativo; o significado final é do provedor |
| `groups` no User | somente leitura; muda pelo recurso Group |
| Group | exige `displayName` |
| POST create | 201 com `Location`; duplicata de `userName` responde 409 com `scimType` `uniqueness` (RFC 7644 § 3.3; V-10 marcou como Inferido, confira) |
| PUT | substitui, não cria |
| PATCH | operações add, remove e replace; `add` de valor existente e `remove` de membro inexistente não alteram nada e devolvem sucesso |
| Filtros | `eq`, `co`, `sw`, `pr`, `gt` |
| Paginação | `startIndex` (padrão 1) e `count`; por cursor com `cursor` e `nextCursor`, e erros `invalidCursor`, `expiredCursor`, `invalidCount` (HTTP 400) pela RFC 9865 |
| Busca | `POST /.search` para filtro com dado pessoal; o servidor pode responder 403 com `scimType` `sensitive` (RFC 7644 § 7) |

## 3. Exemplos de mensagens

Criação:

```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
  "userName": "ana.souza@acme-ltda.test",
  "externalId": "00u1abcDEF",
  "name": { "givenName": "Ana", "familyName": "Souza" },
  "emails": [{ "value": "ana.souza@acme-ltda.test", "primary": true }],
  "active": true
}
```

Resposta 201 (cabeçalho `Location: .../Users/<id>`):

```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
  "id": "9f3c7a40-1b2d-4e8a-9c55-0d6e2a7b1f10",
  "externalId": "00u1abcDEF",
  "userName": "ana.souza@acme-ltda.test",
  "active": true,
  "meta": { "resourceType": "User" }
}
```

Desativação (desprovisionar):

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
  "Operations": [{ "op": "Replace", "path": "active", "value": false }]
}
```

Busca por e-mail sem expor dado pessoal em URL:

```json
POST /scim/v2/Users/.search
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:SearchRequest"],
  "filter": "userName eq \"ana.souza@acme-ltda.test\"",
  "count": 10
}
```

Erro de unicidade:

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "status": "409",
  "scimType": "uniqueness",
  "detail": "userName já existe neste tenant"
}
```

Os valores `op` chegam em capitalizações diferentes conforme o IdP (o Entra envia Add, Replace e Remove; V-54): normalize antes de comparar.

## 4. Desprovisionamento é `active=false` (V-55)

| Passo | Regra |
| --- | --- |
| 1 | `active=false` não apaga o usuário, o papel nem os vínculos de grupo |
| 2 | Revogar na mesma operação: sessões, refresh tokens, chaves de API pessoais e convites pendentes do membro |
| 3 | Estado do membro vira `inactive` (V-31) |
| 4 | Registrar `member.deprovisioned` na auditoria com `actor_id` do token SCIM |
| 5 | `GET` do usuário desativado continua devolvendo o objeto com `active=false` (o Entra espera isso; só deixa de devolver no hard delete, V-54) |
| 6 | Exclusão definitiva segue a política de retenção (skill `tenant-data-lifecycle`), não o SCIM |
| 7 | `active=true` reativa e restaura o acesso, com os grupos preservados (o comportamento do Entra ao reativar grupos é Não verificável: teste) |

O Okta não executa DELETE em usuários no app SCIM: envia pedido que define `active=false` (PATCH em integrações novas do OIN, PUT em integrações customizadas); usuário só suspenso no Okta não dispara desprovisionamento (V-55).

## 5. Aceite do endpoint no Entra (V-54, Verificado na página)

- Criar usuários (RFC 7644 § 3.3), PATCH (§ 3.5.2), `excludedAttributes=members` em grupo (§ 3.4.2.2), listagem e paginação (§ 3.4.2.4), `/Schemas` (RFC 7643 § 7) e um único bearer token para o Entra.
- Soft delete: o objeto "should be returned" ativo ou não ("should", não "must").
- Test Connection: o Entra busca um usuário e um grupo aleatórios; as chamadas DELETE de teste só ocorrem se o hard delete for suportado.
- Checklist: usuário desativado volta com `active=false`; PATCH aceita Add, Replace e Remove em qualquer capitalização; token escopado a um tenant; `/Schemas` exposto; Test Connection passa sem dado real de cliente.

## 6. Limites e resiliência

- Responda 429 com `Retry-After` quando limitar (o Okta aplica backoff dobrando e até 10 tentativas; isso é comportamento do Okta, não do padrão; V-36).
- Idempotência: `add` repetido e `remove` inexistente devolvem sucesso sem mudança; POST repetido do mesmo `externalId` não cria duplicata (usar `externalId` ou `userName` para detectar; a RFC não exige idempotência de POST, Inferido).
- Operação de grupo com muitos membros: processe em lote com limite de tempo e reexecução segura.
- Eventos SCIM como SETs e `Prefer: respond-async` (RFC 9967) são opcionais: só implemente se o IdP exigir.

## 7. Matriz de testes

| Teste | Esperado |
| --- | --- |
| criar usuário duas vezes com o mesmo `userName` | 409 `uniqueness` na segunda; uma linha |
| `PATCH active=false` | sessões revogadas na hora; usuário e grupos preservados |
| `GET` do desativado | objeto com `active=false` |
| `PATCH active=true` | acesso restaurado |
| PATCH com `op` em minúsculas e maiúsculas | ambos aceitos |
| token do tenant A em recurso do B | 404 |
| token expirado ou revogado | 401 |
| busca com e-mail por GET na URL | recusada ou orientada para `/.search` |
| paginação com cursor expirado | 400 `expiredCursor` e o cliente recomeça |
| excesso de requisições | 429 com `Retry-After` |
| `/Schemas` | exposto |
| auditoria | evento por operação, sem token |
