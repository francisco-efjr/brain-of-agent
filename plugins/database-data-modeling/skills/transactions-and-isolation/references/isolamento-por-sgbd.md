# Isolamento por SGBD: o que o padrão garante e o que muda

Conferido em 2026-10-10 contra V-08 (PostgreSQL 18.6 `transaction-iso`, Verificado), V-09 (MySQL 8.4 `innodb-transaction-isolation-levels` e SQL Server `ALTER DATABASE SET` / `snapshot_option`, Verificado; só 100 mil de 271 mil caracteres da página do SQL Server lidos), V-10 (deadlock no PostgreSQL), V-19 e o brain `dados-e-migracoes.md` (MIT, Brain of Agent: "não deduzir isolamento pelo nome transação"). Códigos de erro e comportamentos sem V-nn são conhecimento estável do domínio, rotulados Inferido: conferir na doc da versão instalada.

Sumário
1. Tabela resumo
2. PostgreSQL
3. MySQL/InnoDB
4. SQL Server
5. SQLite, MongoDB, DynamoDB, Redis
6. Erros que pedem retry
7. Como descobrir o nível efetivo

## 1. Tabela resumo

| SGBD | Nível padrão | Mecanismo | O que muda ao subir/descer | Rótulo |
| --- | --- | --- | --- | --- |
| PostgreSQL | READ COMMITTED | MVCC; cada instrução vê o que estava confirmado no início dela | REPEATABLE READ: snapshot da transação, falha com `40001` em atualização concorrente; SERIALIZABLE: SSI com predicate locks que não bloqueiam e podem abortar com `40001` | V-08 |
| MySQL (InnoDB) | REPEATABLE READ | Snapshot da primeira leitura da transação + gap/next-key locks em leituras com lock | READ COMMITTED: menos gap locks, admite phantoms, exige binlog row-based; SERIALIZABLE: `SELECT` simples vira `FOR SHARE` com autocommit desligado | V-09 |
| SQL Server | READ COMMITTED com locks (padrão) | Locks compartilhados em leitura | `READ_COMMITTED_SNAPSHOT ON` usa versionamento de linha no lugar de locks; `ALLOW_SNAPSHOT_ISOLATION` habilita `SNAPSHOT` | V-09 (RCSI); padrão: Inferido |
| SQLite | SERIALIZABLE efetivo (um escritor por vez) | Lock no arquivo/banco | Modo WAL altera concorrência de leitura/escrita; sem fonte lida | Inferido; L-08 |
| MongoDB, DynamoDB, Redis | n/a nesta base | Transações existem com limites próprios | Sem fonte validada | L-07 |

## 2. PostgreSQL (V-08)

- `READ UNCOMMITTED` se comporta como `READ COMMITTED` (que é o padrão).
- `REPEATABLE READ`: a transação vê um snapshot; ao tentar atualizar linha alterada por transação concorrente confirmada, falha com "could not serialize access due to concurrent update" (SQLSTATE `40001`).
- `SERIALIZABLE`: usa SSI (Serializable Snapshot Isolation) com predicate locks **que não bloqueiam**; detecta padrões perigosos e aborta com `40001`.
- **Repetir a transação inteira** ao receber `40001`; em REPEATABLE READ só transações que escrevem precisam de retry; em SERIALIZABLE, mesmo o que uma transação só de leitura leu só vale após o commit, exceto em `READ ONLY DEFERRABLE` (V-08).
- `SERIALIZABLE READ ONLY DEFERRABLE` é o único caso em que serializable bloqueia (espera um snapshot seguro).
- O custo do SSI depende da carga: Suposição a medir.
- Deadlock: o PostgreSQL detecta e aborta uma das transações (V-10), SQLSTATE `40P01` (Inferido). Em READ COMMITTED, `UPDATE ... WHERE stock >= ?` concorrente: o segundo espera o primeiro e reavalia o `WHERE` na linha atualizada (comportamento documentado do READ COMMITTED; Inferido para este detalhe).
- RLS em READ COMMITTED: subconsulta em política pode ter condição de corrida (V-12): ver `rls-tenant-review`.

## 3. MySQL/InnoDB (V-09)

- Padrão `REPEATABLE READ`: a **leitura consistente** usa o snapshot estabelecido na primeira leitura da transação. Leituras com lock (`SELECT ... FOR UPDATE`, `FOR SHARE`) e escritas (`UPDATE`, `DELETE`) operam sobre os dados mais recentes confirmados (leitura "atual", Inferido para esta formulação), e usam gap/next-key locks para impedir phantoms.
- Consequência para o padrão check-then-act: `SELECT stock` mostra o snapshot; `UPDATE stock = stock - ?` aplica sobre o valor atual. Duas sessões podem ler 1 e ambas decrementar: estoque -1. A correção é transformar a checagem em parte da instrução (`AND stock >= ?`) ou travar a linha com `FOR UPDATE` antes de decidir.
- A doc avisa contra misturar leituras com e sem lock em REPEATABLE READ (resultados difíceis de raciocinar).
- `READ COMMITTED`: reduz gap locks, admite phantoms, exige binlog em formato row-based.
- `SERIALIZABLE`: converte `SELECT` simples em `SELECT ... FOR SHARE` quando o autocommit está desligado.
- A página não traz guia de retry; há página separada de deadlocks, não lida (L-03). Deadlock: o InnoDB escolhe uma vítima e devolve erro 1213, SQLSTATE `40001` (Inferido): repetir a transação inteira.
- Lock wait timeout: erro 1205 (`innodb_lock_wait_timeout`, Inferido); não é deadlock: investigar quem segura o lock.
- Sem DDL transacional (V-30): uma migração que falha no meio deixa estado parcial.

## 4. SQL Server (V-09)

- `READ_COMMITTED_SNAPSHOT ON` (RCSI): leituras em READ COMMITTED usam versionamento de linha em vez de locks compartilhados. Ativar exige que não haja outras conexões ativas no banco.
- `ALLOW_SNAPSHOT_ISOLATION ON`: gera versões de linha mesmo quando ninguém usa `SNAPSHOT`; a mudança de estado espera transações ativas.
- A página não fala do version store no `tempdb` (V-09, ressalva): não afirmar custo ou tamanho.
- Padrões de lock e dicas (`UPDLOCK`, `ROWLOCK`) para o equivalente de `FOR UPDATE`: Inferido; conferir a doc. Deadlock: erro 1205 (vítima); conflito de atualização em SNAPSHOT: erro 3960 (Inferido).
- Cobertura desta base para SQL Server é rasa (L-02): "sem fonte validada" para o resto.

## 5. SQLite, MongoDB, DynamoDB, Redis

- SQLite: um escritor por vez; o comportamento de leitores concorrentes depende do modo de journal (WAL). A fonte lida (planner) não cobre isso: "sem fonte validada" (L-08).
- MongoDB, DynamoDB, Redis: existem transações/atomicidade com escopos e limites próprios (documento único, transação multi-documento, `TransactWriteItems`, `MULTI/EXEC` e scripts). Nenhuma foi validada nesta base (L-07); recomende desenhar para operações atômicas em item/documento/chave único e confira a doc da versão.

## 6. Erros que pedem retry

| Engine | Condição | Código | Ação |
| --- | --- | --- | --- |
| PostgreSQL | falha de serialização | SQLSTATE `40001` (V-08) | repetir a transação inteira |
| PostgreSQL | deadlock detectado | SQLSTATE `40P01` (Inferido) | repetir a transação inteira |
| PostgreSQL | lock indisponível com `lock_timeout` | SQLSTATE `55P03` (Inferido) | backoff e nova tentativa (migrações, V-18) |
| MySQL | deadlock | erro 1213 / SQLSTATE `40001` (Inferido) | repetir a transação inteira |
| MySQL | lock wait timeout | erro 1205 (Inferido) | investigar; repetir com cuidado |
| SQL Server | vítima de deadlock | erro 1205 (Inferido) | repetir a transação inteira |

Política de retry (Inferido): máximo de tentativas (ex.: 3 a 5), espera exponencial com jitter, métrica de quantas tentativas ocorreram, e alerta se a taxa de retry crescer. Sem efeito externo dentro da transação.

## 7. Como descobrir o nível efetivo

Pedir ao usuário (somente leitura; ambiente de teste ou réplica):

| Engine | Comando |
| --- | --- |
| PostgreSQL | `SHOW transaction_isolation;` ou `SELECT current_setting('transaction_isolation');` (dentro da transação do app, via log) |
| MySQL 8 | `SELECT @@transaction_isolation;` |
| SQL Server | `SELECT name, is_read_committed_snapshot_on, snapshot_isolation_state_desc FROM sys.databases;` (Inferido) |

No código: procure configuração do ORM/driver (`isolation_level`, `SET TRANSACTION ISOLATION LEVEL`, anotações `@Transactional(isolation = ...)`, opções de `BEGIN`). O nível efetivo pode diferir do padrão da engine por configuração do framework: Verificado só com a leitura da configuração ou saída do comando.
