# Correções de concorrência e retry

Conferido em 2026-10-10 contra V-08 (PostgreSQL: níveis, SSI, `40001`), V-09 (MySQL/SQL Server), V-10 (deadlock, locks de linha/tabela), V-19 (ordem de locks e migrações) e o brain `dados-e-migracoes.md` (MIT, Brain of Agent; exemplo do estoque adaptado). Sintaxe de `SKIP LOCKED`, `ON CONFLICT`, `OUTPUT`, `UPDLOCK` e códigos de erro: conhecimento estável do domínio, rotulado Inferido; confirmar na doc da versão. SQL conceitual: adaptar e testar na engine do projeto, em banco de teste.

Sumário
1. Estoque/saldo: UPDATE condicional
2. Lock pessimista e ordem de locks
3. Controle otimista por versão
4. Unicidade, upsert e idempotência no banco
5. Write skew e SERIALIZABLE
6. Fila com SKIP LOCKED (fronteira)
7. Retry em código (Python e Node)
8. Árvore de decisão

## 1. Estoque/saldo: UPDATE condicional

Problema (antes): leitura e escrita separadas deixam duas sessões passarem na validação.

```sql
-- sessão A e B, ambas:
SELECT stock FROM items WHERE id = 1;                 -- ambas leem 1
UPDATE items SET stock = stock - 1 WHERE id = 1;      -- ambas decrementam -> -1
```

Depois (a checagem vira parte da escrita, atômica numa instrução):

```sql
-- PostgreSQL: RETURNING dá o novo saldo; 0 linhas = sem saldo
UPDATE items SET stock = stock - $1 WHERE id = $2 AND stock >= $1 RETURNING stock;

-- MySQL: use o número de linhas afetadas (rowsAffected = 1 aceita, 0 recusa)
UPDATE items SET stock = stock - ? WHERE id = ? AND stock >= ?;

-- SQL Server (Inferido): OUTPUT inserted.stock ou @@ROWCOUNT
UPDATE items SET stock = stock - @q OUTPUT inserted.stock WHERE id = @id AND stock >= @q;
```

Regras:
- Sempre verifique linhas afetadas. Zero linhas é um resultado de negócio (sem saldo), não sucesso.
- Em MySQL, "linhas afetadas" pode contar apenas linhas **alteradas** conforme a opção do driver (`CLIENT_FOUND_ROWS`, Inferido); como o `UPDATE` acima sempre muda o valor quando casa, a contagem funciona; para updates que podem manter o mesmo valor, confira a semântica do driver.
- Rede de segurança no banco: `ALTER TABLE items ADD CONSTRAINT items_stock_nonneg CHECK (stock >= 0);` (em tabela existente, use `NOT VALID` + `VALIDATE`; ver `safe-migrations`). Com o CHECK, o erro é explícito em vez de saldo negativo silencioso.
- Funciona sob PostgreSQL READ COMMITTED (o segundo `UPDATE` espera o primeiro e reavalia o `WHERE`, Inferido), sob MySQL REPEATABLE READ (a escrita opera sobre o dado mais recente confirmado, Inferido) e em REPEATABLE READ do PostgreSQL com retry de `40001` (V-08).

## 2. Lock pessimista e ordem de locks

Quando a regra entre leitura e escrita é complexa demais para uma instrução:

```sql
BEGIN;
SELECT stock FROM items WHERE id = $1 FOR UPDATE;     -- trava a linha até o COMMIT/ROLLBACK
-- código valida a regra de negócio com o valor lido
UPDATE items SET stock = stock - $2 WHERE id = $1;
COMMIT;
```

- SQL Server: dicas `UPDLOCK, ROWLOCK` na leitura cumprem papel parecido (Inferido).
- Várias linhas: sempre na **mesma ordem** (`ORDER BY id`), senão A trava 1 e pede 2 enquanto B trava 2 e pede 1: deadlock (V-10: o PostgreSQL detecta e aborta uma das transações).

```sql
SELECT id, stock FROM items WHERE id = ANY($1) ORDER BY id FOR UPDATE;   -- PostgreSQL
```
- Mantenha a transação curta: não chamar rede, fila ou usuário com o lock segurado.
- MySQL REPEATABLE READ: `FOR UPDATE` em condição de faixa usa gap/next-key locks e pode bloquear inserções vizinhas (V-09); prefira chaves exatas.

## 3. Controle otimista por versão

```sql
-- leitura: guarda version
SELECT id, stock, version FROM items WHERE id = $1;
-- escrita: só vale se ninguém mexeu
UPDATE items SET stock = $2, version = version + 1 WHERE id = $1 AND version = $3;
-- rowcount = 0 -> conflito: reler e repetir (com limite)
```

Indicado para edições longas e baixa contenção. Em alta contenção gera muitos retries: prefira o UPDATE condicional. A coluna `version` pode ser inteiro ou `xmin`/token de linha, conforme a engine (Inferido).

## 4. Unicidade, upsert e idempotência no banco

- Duplicata sob concorrência se resolve com `UNIQUE`, não com `SELECT` antes do `INSERT`. Trate a violação de unicidade como resultado esperado.
- PostgreSQL:
```sql
INSERT INTO processed_events (event_id) VALUES ($1) ON CONFLICT (event_id) DO NOTHING;   -- rowcount 0 = já processado
INSERT INTO counters (key, n) VALUES ($1, 1) ON CONFLICT (key) DO UPDATE SET n = counters.n + 1;
```
- MySQL: `INSERT ... ON DUPLICATE KEY UPDATE ...` (exige chave única).
- A chave `UNIQUE` de idempotência é a parte de banco; desenho do endpoint, TTL de chaves e reenvio ficam em backend-api.
- Em transação com retry, a inserção em `processed_events` e o efeito de negócio devem ocorrer na **mesma** transação (atomicidade).

## 5. Write skew e SERIALIZABLE

Invariante entre várias linhas (ex.: "sempre ao menos um médico de plantão"):

```sql
-- A e B: SELECT count(*) FROM oncall WHERE on_duty;  -> 2  (ambas veem 2)
-- A: UPDATE oncall SET on_duty = false WHERE doctor = 'ana';
-- B: UPDATE oncall SET on_duty = false WHERE doctor = 'bia';
-- ambas confirmam -> 0 de plantão (anomalia de serialização)
```

Em READ COMMITTED e REPEATABLE READ nada impede (linhas diferentes, sem conflito de escrita). Correções: (a) `SERIALIZABLE` com retry de `40001` (PostgreSQL: SSI detecta e aborta uma, V-08); (b) travar a "linha pai" comum (`SELECT ... FOR UPDATE` num registro de grupo) para serializar; (c) restrição declarativa quando possível. Custo do SSI sob carga: Suposição a medir (V-08).

```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;   -- PostgreSQL
-- ... mesma lógica ...
COMMIT;                                 -- pode falhar com 40001 -> repetir TODA a transação
```

## 6. Fila com SKIP LOCKED (fronteira com backend-api)

```sql
-- PostgreSQL (SKIP LOCKED também existe no MySQL 8.0+, Inferido)
WITH next AS (
  SELECT id FROM jobs WHERE state = 'ready' ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED
)
UPDATE jobs SET state = 'running', started_at = now()
FROM next WHERE jobs.id = next.id
RETURNING jobs.*;
```
Vários consumidores pegam jobs distintos sem esperar uns pelos outros. Reentrega, DLQ e visibilidade são desenho de fila (segmento backend-api).

## 7. Retry em código

Princípios: repetir a **unidade inteira** (abrir transação, ler, decidir, escrever, confirmar); limite de tentativas; espera exponencial com jitter; só para condições transitórias (`40001`, `40P01`; MySQL 1213); nenhum efeito externo dentro (e-mail, HTTP, publicar evento); registrar contagem de tentativas.

Python (psycopg 3 + psycopg_pool; nomes de exceção conferidos de memória, confirmar na versão):

```python
import random, time
from psycopg import errors

RETRYABLE = (errors.SerializationFailure, errors.DeadlockDetected)   # 40001, 40P01

def run_tx(pool, fn, attempts=5, isolation=None):
    for i in range(attempts):
        try:
            with pool.connection() as conn:
                if isolation:
                    conn.isolation_level = isolation     # ex.: psycopg.IsolationLevel.SERIALIZABLE
                with conn.transaction():
                    return fn(conn)                      # fn deve ser repetível: sem efeito externo
        except RETRYABLE:
            if i == attempts - 1:
                raise
            time.sleep(min(0.05 * 2 ** i, 1.0) * random.uniform(0.5, 1.5))
```

Node (node-postgres; `err.code` traz o SQLSTATE):

```js
async function withRetry(pool, fn, { attempts = 5, isolation = null } = {}) {
  for (let i = 0; i < attempts; i++) {
    const client = await pool.connect();
    try {
      await client.query(isolation ? `BEGIN ISOLATION LEVEL ${isolation}` : 'BEGIN'); // isolation vem de lista fixa no código
      const result = await fn(client);
      await client.query('COMMIT');
      return result;
    } catch (err) {
      await client.query('ROLLBACK').catch(() => {});
      const transient = ['40001', '40P01'].includes(err.code);
      if (!transient || i === attempts - 1) throw err;
      await new Promise(r => setTimeout(r, Math.min(50 * 2 ** i, 1000) * (0.5 + Math.random())));
    } finally {
      client.release();
    }
  }
}
```

ORMs: Django `transaction.atomic()` não repete sozinho; SQLAlchemy `Session` precisa de laço externo; frameworks Java com `@Retryable` repetem o método transacional (Inferido; confirmar). Não repita dentro de uma transação já abortada.

## 8. Árvore de decisão

1. A invariante cabe numa instrução (saldo >= 0, unicidade)? -> UPDATE condicional / UNIQUE (+ CHECK).
2. Regra entre leitura e escrita é complexa e a contenção é média/alta? -> `FOR UPDATE` com ordem fixa de locks.
3. Contenção baixa e edição longa? -> versão otimista.
4. Invariante entre várias linhas e sem linha comum para travar? -> SERIALIZABLE + retry (PostgreSQL) ou lock de linha de grupo.
5. Sempre: transação curta, retry limitado, teste com concorrência real.
