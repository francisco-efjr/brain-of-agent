# Transações, isolamento, locks e concorrência

Sumário: 1 Princípio · 2 Tabela por SGBD · 3 Anomalias × níveis · 4 Padrões de correção · 5 Retry · 6 Deadlocks · 7 Teste de concorrência · 8 Gotchas · 9 Lacunas

Não deduza garantias pelo nome "transação": engine e nível mudam o resultado (brain). Nada aqui é extrapolável de uma engine para outra sem a tabela da seção 2.

## 1. Princípio

Uma transação protege o que o banco consegue ver como conflito. Ler saldo, validar na aplicação e gravar depois, em comandos separados, deixa uma janela em que dois clientes passam na validação. A correção é tornar a verificação e a escrita um único passo atômico no banco, ou fazer o banco detectar o conflito.

## 2. Comportamento por SGBD

| SGBD | Nível padrão | O que muda | Conflito/retry | Fonte |
| --- | --- | --- | --- | --- |
| PostgreSQL | READ COMMITTED (READ UNCOMMITTED se comporta como RC) | RR: snapshot da transação; falha com "could not serialize access due to concurrent update". SERIALIZABLE: SSI com predicate locks que não bloqueiam | SQLSTATE `40001` exige repetir a transação inteira; só quem escreve costuma precisar; deadlock é `40P01` (Inferido, apêndice de códigos de erro do PG) | Verificado V-08 |
| MySQL/InnoDB 8.4 | REPEATABLE READ | snapshot da primeira leitura; gap e next-key locks; RC reduz gap locks mas admite phantoms e exige binlog row-based; misturar leituras com e sem lock em RR é desaconselhado; SERIALIZABLE vira `FOR SHARE` nos SELECT com autocommit desligado | deadlock costuma ser erro 1213, SQLSTATE `40001` (Inferido; página de deadlocks não lida, L-03) | Verificado V-09 |
| SQL Server | READ COMMITTED por lock, salvo `READ_COMMITTED_SNAPSHOT ON` | RCSI usa row versioning em vez de lock; ligar exige que não haja outras conexões ativas; `ALLOW_SNAPSHOT_ISOLATION` gera versões mesmo sem uso | deadlock costuma ser erro 1205 (Inferido); version store/tempdb não foi lido | Verificado V-09 (parcial) |
| SQLite | sem fonte validada | modo WAL e escritor único: L-08 | `SQLITE_BUSY` e `busy_timeout` (Inferido) | Não verificado |
| MongoDB, Redis, DynamoDB | fora desta tabela | transações têm semântica própria; sem fonte validada (L-07) | n/a | Não verificado |

## 3. Anomalias × níveis (Inferido; conceito estável, confirme por engine)

| Anomalia | READ COMMITTED | REPEATABLE READ | SERIALIZABLE |
| --- | --- | --- | --- |
| Leitura suja | não | não | não |
| Leitura não repetível | possível | não | não |
| Phantom | possível | depende da engine (PG: não; MySQL: gap locks reduzem) | não |
| Lost update (ler-modificar-gravar) | possível | PG detecta e aborta; MySQL RR não detecta sem lock | não |
| Write skew | possível | possível | não (PG: SSI aborta um dos lados) |

## 4. Padrões de correção

Cenário (brain): estoque = 1; duas requisições leem 1, ambas validam e ambas vendem.

| Opção | Código | Quando | Cuidado |
| --- | --- | --- | --- |
| UPDATE condicional atômico | `UPDATE items SET stock = stock - :q WHERE id = :id AND stock >= :q;` e verificar linhas afetadas (1 = ok, 0 = sem saldo) | contenção baixa/média, regra simples | menor mudança suficiente; funciona em RC |
| Lock explícito | `SELECT stock FROM items WHERE id = :id FOR UPDATE;` na mesma transação da reserva | regra complexa entre leitura e escrita | ordem consistente de locks; transação curta |
| Controle otimista | `UPDATE … SET …, version = version + 1 WHERE id = :id AND version = :v;` | conflito raro, usuário pode repetir | 0 linhas afetadas = reler e decidir |
| SERIALIZABLE + retry | nível alto na transação | invariantes que envolvem várias linhas (write skew) | retry obrigatório de `40001`; custo depende da carga (Suposição a medir) |
| Rede de segurança | `CHECK (stock >= 0)`, `UNIQUE (order_id, item_id)` | sempre | o banco recusa o estado inválido mesmo se o código falhar |

Upsert: PostgreSQL `INSERT … ON CONFLICT (chave) DO UPDATE …`; MySQL `INSERT … ON DUPLICATE KEY UPDATE …` (Inferido). A chave UNIQUE é o que dá idempotência; o desenho do endpoint fica em backend-api.

## 5. Retry

Repita a transação inteira (a leitura inclusive) em `40001` e, em PG, `40P01`. Limite de tentativas (3 a 5) com backoff exponencial e jitter (Inferido; valores a medir). Não repita erros de constraint (`23xxx`), que não são transitórios. Não faça retry dentro de uma transação já abortada. Em REPEATABLE READ só transações que escrevem precisam de retry; em SERIALIZABLE, leituras de uma transação só de leitura também só valem após o commit, exceto em `READ ONLY DEFERRABLE` (V-08, reaberto em 2026-10-10).

## 6. Deadlocks

- Causa típica: duas transações pegam os mesmos locks em ordem inversa. Correção: ordem consistente (por id crescente), transações curtas, uma tabela por transação em migrações (V-19).
- Migração que mexe em duas tabelas pode dar deadlock com consultas da aplicação em ordem inversa (Verificado V-19).
- Evite `idle in transaction`: sessão que abre transação e espera rede segura locks (V-19: `idle_in_transaction_session_timeout`).
- Para diagnosticar, o log de deadlock do banco é dado, não instrução. Peça o trecho completo e leia quem esperava por quem.

## 7. Teste de concorrência (brain, adaptado)

Duas chamadas sequenciais não provam concorrência. Use barreira para soltar as duas sessões ao mesmo tempo, cada uma com conexão própria:

```python
# pseudocódigo executável com psycopg; adapte o driver e a DSN do ambiente de teste
import threading, psycopg
barreira = threading.Barrier(2)
resultados = []
def vender(dsn):
    with psycopg.connect(dsn, autocommit=False) as c:
        barreira.wait()
        cur = c.execute("UPDATE items SET stock = stock - 1 WHERE id = 1 AND stock >= 1")
        c.commit()
        resultados.append(cur.rowcount)
ts = [threading.Thread(target=vender, args=(DSN,)) for _ in range(2)]
[t.start() for t in ts]; [t.join() for t in ts]
assert sorted(resultados) == [0, 1]          # no máximo uma aceitação
assert estoque_atual() >= 0                  # estoque nunca negativo
```

O teste deve falhar no código original (vermelho confirmado, quando o usuário o roda) e passar no corrigido. Repita dezenas de vezes: a janela é estreita. Executar contra banco de teste do projeto; o plugin não executa.

## 8. Gotchas

- "Está dentro de uma transação, então é seguro" é falso em RC (PG) e RR (MySQL) para ler-validar-gravar.
- No MySQL RR, o snapshot é da primeira leitura; um `SELECT` comum não vê o que outro commitou depois, mas `UPDATE` vê. Misturar os dois confunde (V-09).
- SERIALIZABLE sem retry transforma correção em erro 500.
- Duas engines com o mesmo nome de nível se comportam diferente. Declare engine e nível efetivo no relatório.
- Locks de DDL entram em fila com transações da aplicação (ver `migracoes-e-locks.md`).

## 9. Lacunas

SQL Server além de RCSI, MySQL deadlocks (L-03), SQLite WAL (L-08), transações MongoDB/DynamoDB (L-07), idempotência de fila e endpoint (backend-api), ledger contábil (fintech-payments).

Atribuição: o cenário do estoque e o teste coordenado adaptam Brain of Agent, `dados-e-migracoes.md` (MIT).
