# Idempotência de pagamentos: DDL, esboço executado e lista de rejeição

Sumário: 1. Esquema · 2. Esboço executado (Python + SQLite) · 3. Contraexemplo medido · 4. Fingerprint · 5. Lista de rejeição de 13 itens · 6. Perguntas ao fornecedor

Origem: V-01 (Stripe, Adyen, post de 2017), V-02 (quatro desfechos, fingerprint, tombstone, fencing, lista de rejeição; skill de praticante, Apache-2.0, 1 estrela, valendo só cruzada com V-01), V-44 (Pix). O texto e o código abaixo são redação própria. Conferido em 2026-10-10.

## 1. Esquema (Postgres; esboço, não executado neste ambiente)

```sql
CREATE TABLE payment_idempotency (
  scope           text        NOT NULL,   -- conta/tenant + operação, ex.: 'acct_42:charge.create'
  idem_key        text        NOT NULL,   -- gerada uma vez por intenção de negócio
  fingerprint     text        NOT NULL,   -- 'v1:' || sha256 do corpo canônico (ver seção 4)
  state           text        NOT NULL CHECK (state IN ('started','succeeded','failed_final','indeterminate')),
  provider        text        NOT NULL,
  provider_ref    text,                   -- id devolvido pelo provedor (pagamento, txid, e2eid)
  response_status smallint,
  response_body   jsonb,                  -- pode ser apagado após a retenção; o tombstone (linha) permanece
  lease_owner     text,
  lease_until     timestamptz,
  fencing_token   bigint      NOT NULL DEFAULT 0,
  provider_retention interval,            -- retenção documentada do provedor para esta chave
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (scope, idem_key)
);
-- Reserva atômica (uma linha devolvida = você é o dono; nenhuma = outra requisição já reservou):
-- INSERT INTO payment_idempotency (scope, idem_key, fingerprint, state, provider)
-- VALUES ($1,$2,$3,'started',$4) ON CONFLICT (scope, idem_key) DO NOTHING RETURNING idem_key;
```

Significado dos estados: `started` (reservada, chamada externa possivelmente em voo); `succeeded` (resultado final guardado); `failed_final` (falha definitiva, sem efeito no provedor; repetir devolve a mesma falha); `indeterminate` (timeout ou resposta perdida; resolver só por consulta ao provedor).

## 2. Esboço executado (Python 3 + sqlite3, stdlib)

Executado em 2026-10-10 em Python 3.14 (Windows): 8 threads com a mesma chave deram 1 `created` e 7 `replayed`; `linhas charges = 1`, `chamadas ao provedor = 1`; repetir devolveu `replayed`; corpo diferente devolveu `conflict`. SQLite serializa com `BEGIN IMMEDIATE`; em Postgres a garantia vem de `ON CONFLICT` na chave primária.

```python
import hashlib, json, sqlite3

def fingerprint(body: dict, version: int = 1) -> str:
    canon = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return f"v{version}:" + hashlib.sha256(canon.encode()).hexdigest()

def charge(path, scope, key, body, provider_call):
    """Retorna (status, payload): created | replayed | in_progress | conflict."""
    fp, db = fingerprint(body), sqlite3.connect(path, timeout=10, isolation_level=None)
    try:
        db.execute("BEGIN IMMEDIATE")
        cur = db.execute("INSERT INTO idempotency(scope, idem_key, fingerprint, state) VALUES (?,?,?, 'started') "
                         "ON CONFLICT(scope, idem_key) DO NOTHING", (scope, key, fp))
        reservou = cur.rowcount == 1
        db.execute("COMMIT")                          # reserva persistida ANTES da chamada externa
        if not reservou:
            fp0, estado, resp = db.execute("SELECT fingerprint, state, response FROM idempotency "
                                           "WHERE scope=? AND idem_key=?", (scope, key)).fetchone()
            if fp0 != fp:      return "conflict", None          # mesma chave, corpo diferente
            if estado == "succeeded": return "replayed", json.loads(resp)
            return "in_progress", None                          # 'indeterminate': consultar o provedor
        ref = provider_call(key, body)                # fora de transação com lock
        db.execute("BEGIN IMMEDIATE")
        db.execute("INSERT INTO charges(scope, idem_key, amount_minor, currency) VALUES (?,?,?,?)",
                   (scope, key, body["amount_minor"], body["currency"]))
        db.execute("UPDATE idempotency SET state='succeeded', provider_ref=?, response=? WHERE scope=? AND idem_key=?",
                   (ref, json.dumps({"provider_ref": ref}), scope, key))
        db.execute("COMMIT")
        return "created", {"provider_ref": ref}
    finally:
        db.close()
```

Tabelas mínimas do exemplo: `idempotency(scope, idem_key, fingerprint, state, provider_ref, response, PRIMARY KEY (scope, idem_key))` e `charges(id, scope, idem_key, amount_minor, currency)`. O teste dispara N threads com a mesma `idem_key` e afirma `SELECT count(*) FROM charges` igual a 1 e uma única chamada ao provedor (stub local, nunca o provedor real).

Lacunas deste esboço, a tratar no código real: o gancho entre `started` e o resultado precisa de recuperação (um processo que morre após reservar deixa a linha em `started`; um varredor promove a `indeterminate` depois de um prazo e consulta o provedor); a gravação do efeito e a mudança de estado devem ficar na mesma transação; o tamanho do corpo guardado e a retenção vêm da política do projeto.

## 3. Contraexemplo medido (mutação)

Padrão "checar e inserir" sem restrição única, com 50 ms entre a checagem e a gravação, 8 threads, mesma chave: `linhas charges = 8 | chamadas = 8` (executado em 2026-10-10). É esse o resultado que o teste do passo 7 da skill precisa reprovar. Trocar a restrição por um SELECT prévio, cache em memória ou lock em processo único reproduz o defeito sempre que há duas réplicas ou um reinício.

## 4. Fingerprint canônico

- Entradas: somente campos que mudam a semântica da operação (valor em inteiro na menor unidade, moeda, destino, referência do pedido, método de pagamento). Exclua timestamps, ids de requisição e ordem de campos.
- Serialize em forma canônica (chaves ordenadas, sem espaços, UTF-8), aplique SHA-256 e prefixe com a versão do algoritmo; mudar o algoritmo cria `v2` e mantém `v1` válido para chaves em retenção.
- Valor sempre inteiro: `10.0` e `10` não podem gerar fingerprints diferentes por serialização de float (por isso dinheiro nunca é float, ver `money-ledger-design`).
- O fingerprint compara requisições do **seu** cliente com o que você já aceitou. Não o confunda com o `Idempotency-Key` do provedor.

## 5. Lista de rejeição para revisão de design (13 itens, V-02)

Cada item reprova o design até haver mitigação. Coluna "como detectar" é sugestão de busca no código (Grep), não regra do provedor.

| # | Rejeitar quando | Como detectar |
| --- | --- | --- |
| 1 | Cache em memória ou lock distribuído é a única proteção | `dict`, `Map`, `lru_cache`, `redis.set(nx)` sem tabela durável |
| 2 | Checa existência antes do insert sem restrição única | `SELECT ... WHERE idem` seguido de `INSERT` |
| 3 | Aceita parâmetros diferentes sob a mesma chave | ausência de comparação de fingerprint |
| 4 | Trata timeout como falha | `except Timeout` que marca `failed` e libera nova tentativa com nova chave |
| 5 | Gera nova chave do provedor a cada retry | `uuid4()` dentro do laço de retry |
| 6 | Cacheia toda falha sem separar as anteriores à execução (validação) | resposta de 4xx de validação guardada como resultado final |
| 7 | Retém menos que a janela de retry | TTL da chave menor que o backoff total |
| 8 | Promete exactly-once entre sistemas | texto de contrato, comentário ou ADR |
| 9 | Supõe escopo de idempotência entre regiões ou gerações de API sem documentação | mesma chave usada em v1 e v2 ou em endpoints regionais |
| 10 | Deixa a expiração apagar a identidade da operação | `DELETE` por TTL sem tombstone |
| 11 | Reexibe resposta sensível guardada sem reautorizar | replay devolve corpo completo a outro chamador |
| 12 | Usa lease sem fencing token | `lease_until` sem comparação de token na escrita |
| 13 | Trata "não encontrado" imediato como prova de que não executou | ausência na consulta vira reenvio automático |

## 6. Perguntas ao fornecedor (quando a matriz tem "não documentado")

- Cabeçalho de idempotência existe? É obrigatório? Em quais endpoints?
- Retenção da chave? O que acontece com corpo diferente sob a mesma chave? O que acontece se a original ainda está em processamento?
- A consulta por referência externa é consistente imediatamente depois de um timeout, ou há defasagem?
- Quais erros o provedor classifica como transitórios (seguros para repetir com a mesma chave)?

Registre as respostas com data e fonte (documento, ticket, e-mail) na tabela de provedores do playbook; sem resposta, a célula continua "não documentado".
