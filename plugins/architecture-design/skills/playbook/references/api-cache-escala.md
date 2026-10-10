# Contrato de API, cache e escala

Validado em 2026-10-10 · Modelo-alvo: Claude 4.x/5.x · Rótulos: Verificado, Inferido, Suposição, Não verificável.
Fontes: V-39 (Azure Web API design, leitura parcial), V-40 (api-designer, MIT, RFC 7807 corrigida para 9457), V-41 (proyecto26, MIT, regras de bolso = Suposição), V-38 (Cache-Aside, Microsoft), N-02 (RFC 9457, IETF), N-03 (rascunho Idempotency-Key, expirado), N-04 (Parallel Change). Lacunas de fonte primária: RFC 9110, Google AIP, Microsoft REST API Guidelines, idempotência da Stripe, load shedding. Escopo: aqui fica o contrato e a decisão; a implementação em framework, auth detalhada, rate limiting, GraphQL/gRPC/tRPC e geração de OpenAPI a partir de código pertencem a `/backend-api:playbook`.

## Sumário

1. Checklist de revisão de API
2. Modelo de erro RFC 9457
3. Paginação por cursor e filtros
4. Idempotência HTTP
5. Operações assíncronas e concorrência
6. Evolução e versionamento
7. Cache: decisão e checklist
8. Laço de seis fases de system design
9. Taxonomia L0 a L7
10. Ordem de grandeza no texto: exemplo trabalhado
11. Lint de contrato (usuário executa)
12. Gotchas

## 1. Checklist de revisão de API (V-39, V-40, V-41)

Template `api-review.md`. Responda sim, não ou N.A. para cada item.

- [ ] Domínio e consumidores identificados (quem chama, com que frequência, com que restrições).
- [ ] Recursos com nomes de substantivo no plural e hierarquia rasa; verbos HTTP para ações.
- [ ] Métodos com semântica correta; PUT e DELETE idempotentes; códigos de status coerentes (200, 201 com `Location`, 202, 204, 400, 401, 403, 404, 409, 412, 422, 429).
- [ ] Operações longas respondem 202 com recurso de status.
- [ ] Paginação por cursor para dados que mudam muito (`limit` e `offset` só para casos simples).
- [ ] Filtros e ordenação documentados; respostas parciais quando o payload é grande.
- [ ] Versão e depreciação: mudanças aditivas por padrão; política de remoção com prazo.
- [ ] Erro padronizado (RFC 9457) com `type` estável e extensões por campo.
- [ ] Idempotência para POST com efeito (convenção `Idempotency-Key`).
- [ ] Concorrência otimista (ETag e `If-Match`).
- [ ] Autorização por objeto, não só por papel.
- [ ] Tracing (propagar trace context) e ID de correlação na resposta.
- [ ] Contrato escrito (OpenAPI) passa por lint antes da entrega (critério de saída; o usuário executa).

## 2. Erro RFC 9457 (N-02)

RFC 9457 (julho de 2023, Standards Track) obsoleta a RFC 7807. Media type `application/problem+json`. Campos: `type` (URI que identifica o tipo de problema), `title`, `status`, `detail`, `instance`; extensões livres.

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json

{
  "type": "https://example.com/problems/validation-error",
  "title": "Dados inválidos",
  "status": 422,
  "detail": "Um ou mais campos não passaram na validação.",
  "instance": "/orders/req-7f3a",
  "errors": [
    { "field": "items[0].quantity", "detail": "deve ser maior que zero" }
  ]
}
```

Regras: `type` estável e documentado (não a mensagem); `detail` sem dado sensível nem stack trace; `errors` é extensão local; mesmo envelope para todos os erros. Substitui o ad hoc `{ "error": "msg" }`.

## 3. Paginação por cursor e filtros (V-41; páginas de V-39 usam `limit/offset`)

Use cursor opaco quando a coleção é grande e muda o tempo todo (um offset salta ou repete itens entre páginas e fica lento em tabelas grandes: Inferido a partir de V-41).

```http
GET /orders?status=paid&limit=50&cursor=eyJpZCI6MTIzNDV9
200 OK
{
  "data": [ { "id": "ord_12346", "status": "paid" } ],
  "next_cursor": "eyJpZCI6MTI0MDB9",
  "has_more": true
}
```

Regras: cursor codifica a chave de ordenação (não o offset) e é opaco para o cliente; ordenação total e estável (inclua desempate por id); `limit` com máximo; filtros por igualdade e intervalo documentados; contagem total só se barata (ou endpoint separado).

## 4. Idempotência HTTP (V-41, N-03, conflito C8)

`Idempotency-Key` é convenção amplamente usada, sem RFC: o rascunho IETF `draft-ietf-httpapi-idempotency-key-header-07` expirou (revisão de 2025-10-15, página de 2026-04-18). Recomende como convenção (Inferido) e defina no contrato local:

| Decisão | Sugestão (Suposição, ajuste ao domínio) |
| --- | --- |
| Escopo da chave | Por cliente autenticado e endpoint |
| Formato | UUID v4 gerado pelo cliente, por operação de negócio |
| TTL | Maior que a janela de retentativas do cliente (ex.: 24 h) |
| Mesma chave, mesmo corpo | Repetir a resposta original (mesmo status e corpo) |
| Chave ausente onde é obrigatória | Erro 400 (rascunho 07, SHOULD) |
| Mesma chave, corpo diferente | Erro 422 com problema `idempotency-key-reused` (rascunho 07, SHOULD) |
| Mesma chave em andamento | 409 (rascunho 07, SHOULD); `Retry-After` é escolha local |
| Armazenamento | Restrição de unicidade; resultado guardado junto da chave |

PUT e DELETE já são idempotentes por semântica HTTP; POST com efeito exige a chave.

## 5. Assíncrono e concorrência

- **202 Accepted + status:** `POST /exports` responde `202` com `Location: /exports/{id}`; `GET /exports/{id}` devolve `pending|running|done|failed`, resultado ou link, e erro RFC 9457 em `failed`. Evita conexão presa e permite retomar.
- **ETag:** `GET` devolve `ETag`; `PUT` exige `If-Match`; divergência retorna `412 Precondition Failed`. Previne atualização perdida.
- **Autorização por objeto:** a regra "o usuário pode ver este pedido" é verificada no caso de uso a cada acesso, não só no gateway (severidade crítica em `checklist-completo.md`, CK-45).

## 6. Evolução e versionamento (V-39, N-04)

- Mudança aditiva (campo novo opcional, endpoint novo) não exige versão nova.
- Quebra de contrato: expandir (aceitar o antigo e o novo), migrar consumidores, contrair (remover o antigo) (N-04).
- Versionamento por URI, query, cabeçalho ou tipo de mídia (V-39): cada um tem implicações de cache; escolha um e registre em ADR.
- Depreciação: cabeçalho ou campo de aviso, data de remoção, métrica de uso do campo antigo.
- Cliente deve tolerar campos desconhecidos (regra de leitura tolerante).

## 7. Cache: decisão e checklist (V-38, V-41)

Regra: não adicione cache antes de um número mostrar que a leitura é o gargalo (S-17). Medir: QPS de leitura da origem, p95 da consulta, taxa de leitura/escrita.

Checklist:

- [ ] Existe um número (latência, custo, carga) que justifica o cache?
- [ ] Orçamento de obsolescência declarado ("até 60 s de atraso é aceitável").
- [ ] Estratégia: cache-aside como padrão (carrega sob demanda; na escrita, **grava no banco e depois invalida** o item, a ordem importa); write-through quando a leitura logo após a escrita precisa estar fresca.
- [ ] TTL coerente com o padrão de acesso, com variação aleatória para não expirar tudo junto.
- [ ] Proteção contra stampede (muitas requisições na expiração) e contra chave inexistente (cache negativo curto): V-41, Inferido, conferir fonte primária.
- [ ] Aquecimento (priming) após deploy ou esvaziamento.
- [ ] Cache local por instância diverge entre instâncias: aceitável?
- [ ] Sem dado sensível em cache compartilhado.
- [ ] Métricas: taxa de acerto, evictions, QPS da origem; alerta em queda de acerto.
- [ ] Quando NÃO: conjunto estático (use CDN/arquivo), taxa de acerto baixa.

Stampede, penetração e hot key: mitigações usuais são coalescer requisições para a mesma chave (uma única recomputação), TTL com jitter, cache negativo com TTL curto e réplicas ou cache local para chave quente (V-41; Inferido).

## 8. Laço de seis fases de system design (V-41)

1. **Clarificar** (até 5 perguntas): usuários, escala, consistência, time e orçamento, modos de falha.
2. **Estimar** a ordem de grandeza no texto, com premissas rotuladas Suposição.
3. **Desenhar** pelas camadas L0 a L7 com diagrama de 5 a 15 nós.
4. **Trade-offs** em tabela (consistência vs disponibilidade, custo, complexidade) e a alternativa mais simples.
5. **Modos de falha:** o que acontece quando cada dependência cai.
6. **Iterar** e registrar decisões (ADR).

Quando o usuário disser "o que achar melhor", dê a recomendação e peça confirmação.

## 9. Taxonomia L0 a L7 (V-41)

| Camada | Pergunta de revisão |
| --- | --- |
| L0 Enquadramento | Qual problema, quem usa, qual requisito não funcional manda? |
| L1 Borda | DNS/CDN, balanceamento, autenticação, limites de taxa na entrada |
| L2 Serviços | Quais serviços/módulos, qual contrato, síncrono ou assíncrono? |
| L3 Estado | Onde mora cada dado, quem escreve, consistência exigida, cache? |
| L4 Assíncrono | Filas, eventos, retentativas, ordenação, backpressure |
| L5 Correção | Idempotência, transações, invariantes, reconciliação |
| L6 Operação | Observabilidade, deploy, rollback, runbooks, custos |
| L7 Crescimento | Particionamento, multi-região, migração futura, o que NÃO construir agora |

## 10. Ordem de grandeza no texto: exemplo trabalhado

Pedido: serviço de notificações (e-mail e push) para 2 milhões de usuários, pico de 50 mil envios por minuto. A conta vai na resposta; nenhum script é executado (V-41 recomenda não rodar o `botec.py`).

| Grandeza | Conta | Resultado | Rótulo |
| --- | --- | --- | --- |
| Pico em envios/s | 50.000 / 60 | cerca de 833/s | Verificado (aritmética sobre dado do usuário) |
| Divisão por canal | 50/50 | cerca de 417/s e-mail e 417/s push | Suposição |
| Volume diário médio | 2 M usuários x 3 notificações/dia | 6 M/dia = cerca de 69/s | Suposição |
| Razão pico/média | 833 / 69 | cerca de 12x | Inferido (derivada das suposições) |
| Retentativas | 5% de falha transitória, até 3 tentativas | carga efetiva cerca de 1,1x | Suposição |
| Banda | 833/s x 2 KB | cerca de 1,7 MB/s (13 Mbit/s) | Suposição (tamanho de payload) |
| Log de entrega | 6 M/dia x 90 dias x 500 B | cerca de 270 GB | Suposição |
| Workers | 833 / 100 envios/s por worker, +50% folga | 9 no pico, cerca de 13 com folga | Suposição (vazão por worker) |

O número que decide: limites de vazão e de cota do provedor de e-mail/push (Não verificável aqui; obter do contrato do usuário). Decisões decorrentes: fila durável entre API e workers; bulkhead por canal; retry em uma camada com jitter; idempotência por `notification_id`; backpressure quando o provedor limita. Diagrama de até 15 nós em `c4-e-diagramas.md`.

Regras de bolso de V-41 (QPS por nó de cache e similares) são Suposição: se usá-las, diga que são regras de bolso e peça medição.

## 11. Lint de contrato (o usuário executa)

Critério de saída do contrato: passa por lint de OpenAPI. V-40 cita `npx @redocly/cli lint` (lint) e `npx @stoplight/prism-cli` (mock). `npx` baixa e executa código de terceiros: o plugin só documenta; fixe a versão, rode em ambiente isolado e por decisão do usuário (ver `ferramentas-e-mcp.md`).

## 12. Gotchas

- RFC 7807 (citada por V-40) foi obsoleta pela RFC 9457: use 9457. A página de Web API design da Microsoft (V-39) não foi lida por inteiro e a busca por "9457" e "7807" nela não retornou ocorrência: não atribua a ela recomendação sobre RFC.
- A página V-39 usa `limit` e `offset`; a recomendação de cursor vem de V-41 (classe B, 5/10) e é consistente com prática comum (Inferido).
- Rascunho `Idempotency-Key` expirado: não diga "padrão IETF".
- Cache primeiro e medir depois é o erro mais comum; S-17 existe para isso.
- Orçamento de obsolescência é decisão de produto: pergunte ao humano.
- GraphQL, gRPC e tRPC têm trade-offs próprios que este arquivo não cobre; encaminhe a `/backend-api:playbook`.
- Estimativas com premissas inventadas pelo modelo enganam: toda premissa precisa de rótulo e de dono para confirmar.
