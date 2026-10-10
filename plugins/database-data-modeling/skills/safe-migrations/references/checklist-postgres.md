# Checklist de migração segura (PostgreSQL)

Conferido em 2026-10-10 contra V-10 (explicit-locking + sql-altertable, PostgreSQL 18.6), V-11 (create-index), V-13 (particionamento), V-18 (strong_migrations, MIT, conceito), V-19 (pganalyze), V-22 (C, só motivação), V-35 e o brain `dados-e-migracoes.md` (MIT, Brain of Agent). Linhas sem V-nn são conhecimento estável do domínio, marcadas Inferido: conferir na doc da versão instalada. SQL conceitual: adaptar e testar na engine do projeto.

Sumário
1. Antes de começar
2. Tabela: DDL -> lock -> custo
3. Checklist de revisão (10 itens)
4. Receitas SQL por mudança
5. Timeouts, retry e conexão
6. Monitoramento durante a migração
7. Roteiro de ensaio em cópia
8. Rollback e critério de interrupção
9. Saída esperada da revisão

## 1. Antes de começar

- Versão do servidor: `SELECT version();`. PostgreSQL 18 documenta `NOT VALID` para not-null; em versões anteriores use CHECK (V-10, Art. C).
- Tamanho e escrita da tabela: `SELECT pg_size_pretty(pg_total_relation_size('public.orders'));` e a taxa de escrita (pergunte). Em tabela pequena e de baixo tráfego o fluxo curto basta.
- Pooler: se houver PgBouncer em modo transação, `SET` de sessão não persiste entre transações; defina timeouts por `ALTER ROLE` e migre por conexão direta (V-18, V-35).
- Réplicas e CDC: DDL e backfill geram lag; defina o limite aceitável.

## 2. Tabela: DDL -> lock -> custo

"Ver" = o que você deve declarar na revisão. Rótulo: V = Verificado em V-nn; I = Inferido (estável, conferir na versão).

| DDL | Lock na tabela | Bloqueia | Custo | Alternativa segura | Rótulo |
| --- | --- | --- | --- | --- | --- |
| `ALTER TABLE` (regra geral) | `ACCESS EXCLUSIVE`, salvo exceção; combinar subcomandos usa o mais forte | até `SELECT` | depende do subcomando | dividir em subcomandos separados; `lock_timeout` | V-10 |
| `ADD COLUMN` sem default ou com default constante | `ACCESS EXCLUSIVE` breve | leitura/escrita só pelo tempo de obter o lock | metadado | `lock_timeout` + retry | V-10 |
| `ADD COLUMN ... DEFAULT <volátil>` | `ACCESS EXCLUSIVE` | tudo | reescreve a tabela | coluna sem default, backfill em lotes, depois default | V-10 |
| `ALTER COLUMN TYPE` | `ACCESS EXCLUSIVE` | tudo | quase sempre reescreve (`int`->`bigint`); alguns casos binary-coercible não | expand/contract com coluna nova | I |
| `SET NOT NULL` direto | `ACCESS EXCLUSIVE` | tudo | scan completo | CHECK `NOT VALID` -> `VALIDATE` -> `SET NOT NULL` (pula o scan se CHECK válido prova ausência de NULL) | V-10 |
| `ADD CONSTRAINT CHECK` válido | `ACCESS EXCLUSIVE` | tudo | scan completo | `NOT VALID` + `VALIDATE CONSTRAINT` | V-10 |
| `VALIDATE CONSTRAINT` | `SHARE UPDATE EXCLUSIVE` | DDL concorrente; não bloqueia leitura/escrita comuns | scan | executar fora do pico | V-10 |
| `ADD FOREIGN KEY` | `SHARE ROW EXCLUSIVE` nas duas tabelas | escrita nas duas | scan | `NOT VALID` + `VALIDATE`; índice no lado filho antes | V-10 |
| `ADD UNIQUE`/`PRIMARY KEY` (cria índice) | `ACCESS EXCLUSIVE` durante o build | tudo | build do índice | `CREATE UNIQUE INDEX CONCURRENTLY` + `ADD CONSTRAINT ... USING INDEX` | I |
| `CREATE INDEX` | `SHARE` | escrita (leitura passa) | build | `CONCURRENTLY` | V-11 |
| `CREATE INDEX CONCURRENTLY` | `SHARE UPDATE EXCLUSIVE` | só DDL/outro build na tabela | duas varreduras; espera transações antigas; pode falhar e deixar `INVALID` | conferir `indisvalid` | V-11 |
| `DROP INDEX` | `ACCESS EXCLUSIVE` | tudo | metadado | `DROP INDEX CONCURRENTLY` (fora de transação) | I |
| `DROP COLUMN` | `ACCESS EXCLUSIVE` breve | tudo (breve) | metadado; espaço só volta com rewrite | parar de ler/escrever na aplicação antes (contract) | I |
| `RENAME COLUMN/TABLE` | `ACCESS EXCLUSIVE` breve | tudo (breve) | metadado | quebra versões antigas da app: expand/contract | I |
| `ATTACH PARTITION` sem CHECK equivalente | `ACCESS EXCLUSIVE` na partição | tudo na partição | scan para validar limite | criar CHECK antes, anexar, remover CHECK | V-13 |
| `DETACH PARTITION CONCURRENTLY` | `SHARE UPDATE EXCLUSIVE` no pai | só DDL | metadado | preferir ao `DELETE` em massa | V-13 |
| `TRUNCATE` | `ACCESS EXCLUSIVE` | tudo | instantâneo, destrutivo | n/a: só com confirmação | I |
| `VACUUM FULL`, `CLUSTER` | `ACCESS EXCLUSIVE` | tudo | reescreve | confirmar impacto antes (V-35); `pg_repack` é ferramenta de terceiros, não avaliada aqui | V-35 (confirmar), I |

Regras que se derivam da tabela:
- Fila de locks: DDL que espera `ACCESS EXCLUSIVE` bloqueia as consultas que chegam depois, mesmo as que não conflitam com a transação antiga que ele espera (V-19). Por isso `lock_timeout` curto + retry em vez de esperar indefinidamente.
- Deadlock: migração que toca duas tabelas na mesma transação pode travar em ordem inversa à da aplicação; o PostgreSQL detecta e aborta uma das duas (V-10, V-19). Uma tabela por transação.

## 3. Checklist de revisão (10 itens, cada um com o porquê)

Marque: ok | violado | não se aplica. Cada violado vira linha na tabela de saída (item, risco, alternativa).

- [ ] **1. Lock declarado** para cada DDL. Por quê: ALTER usa `ACCESS EXCLUSIVE` e bloqueia até `SELECT`; combinar subcomandos adota o mais forte (V-10).
- [ ] **2. Índice com `CONCURRENTLY`, fora de transação, e `INVALID` verificado depois.** Por quê: build comum bloqueia escrita; o concorrente pode falhar e deixar índice inútil que custa escrita (V-11).
- [ ] **3. FK, CHECK, NOT NULL em duas etapas** (`NOT VALID` -> `VALIDATE`). Por quê: validação usa lock mais leve; CHECK válido evita o scan do `SET NOT NULL` (V-10).
- [ ] **4. Coluna nova sem default volátil**; default constante é metadado; backfill em lotes fora de transação longa. Por quê: volátil reescreve (V-10).
- [ ] **5. Mudança de tipo, renome ou remoção em expand/contract** (V-20), nunca DDL direto. Por quê: versões da app coexistem durante o deploy; rollback de código não desfaz schema (brain).
- [ ] **6. `lock_timeout` curto e `statement_timeout`** na sessão da migração, com retry da falha de lock. Valores de partida de V-18 (Inferido, medir). Por quê: evita fila de locks.
- [ ] **7. Uma tabela por transação**, salvo necessidade de atomicidade; nenhuma transação da aplicação fica aberta esperando (`idle_in_transaction_session_timeout`) (V-19).
- [ ] **8. Ensaiada em cópia com volume realista**, com duplicatas e NULLs (V-22 motivação; brain). Por quê: distribuição e tamanho mudam duração e lock.
- [ ] **9. Rollback escrito e ensaiado**; "reverter schema" distinto de "reverter dados" (brain). Por quê: remoção de coluna e conversão com perda exigem restauração, não `down`.
- [ ] **10. Migração gerada por ferramenta revisada à mão**; SQL real lido (`sqlmigrate`/`--sql`) (V-30).

## 4. Receitas SQL por mudança

Todas são texto para o usuário aplicar; nenhuma é executada por esta skill. Substitua os nomes. `lock_timeout` aparece em cada uma porque o `ACCESS EXCLUSIVE` breve também pode enfileirar.

### 4.1 Tornar uma coluna NOT NULL (PostgreSQL < 18, ou versão desconhecida)

```sql
-- Pré-requisito: a aplicação já não grava NULL nessa coluna (fase expand).
SET lock_timeout = '5s';                      -- ponto de partida (Inferido); retry se falhar com 55P03
ALTER TABLE orders ADD CONSTRAINT orders_customer_id_nn CHECK (customer_id IS NOT NULL) NOT VALID;

-- Backfill dos NULLs existentes: job em lotes (ver expand-contract-e-backfill.md), FORA desta migração.
-- O valor a preencher é decisão de negócio: peça ao responsável; não invente.

ALTER TABLE orders VALIDATE CONSTRAINT orders_customer_id_nn;   -- SHARE UPDATE EXCLUSIVE; falha se restar NULL
ALTER TABLE orders ALTER COLUMN customer_id SET NOT NULL;       -- com CHECK válido, sem scan completo
ALTER TABLE orders DROP CONSTRAINT orders_customer_id_nn;       -- opcional, após o SET NOT NULL
```

Em PostgreSQL 18 a doc descreve `NOT VALID` direto para not-null (V-10); mesmo assim confirme a sintaxe na doc de `ALTER TABLE` da 18.x antes de usar (Inferido).

### 4.2 Índice novo

```sql
-- fora de transação: desligue a transação da migração (ver migracao-gerada-por-orm.md)
CREATE INDEX CONCURRENTLY orders_customer_id_created_at_idx ON orders (customer_id, created_at DESC);

-- verificação (deve retornar zero linhas):
SELECT indexrelid::regclass AS indice FROM pg_index WHERE NOT indisvalid;
-- se aparecer: DROP INDEX CONCURRENTLY <nome>; e tente de novo (ou REINDEX INDEX CONCURRENTLY) (V-11)
```

Tabela particionada: construir concorrentemente em cada partição e depois criar o índice no pai **sem** `CONCURRENTLY` (só metadados, V-11).

### 4.3 FK

```sql
CREATE INDEX CONCURRENTLY order_items_order_id_idx ON order_items (order_id);   -- lado filho primeiro
SET lock_timeout = '5s';
ALTER TABLE order_items ADD CONSTRAINT order_items_order_fk
  FOREIGN KEY (order_id) REFERENCES orders(id) NOT VALID;      -- SHARE ROW EXCLUSIVE (curto)
ALTER TABLE order_items VALIDATE CONSTRAINT order_items_order_fk;  -- scan sem bloquear escrita comum
```

### 4.4 Unicidade

```sql
CREATE UNIQUE INDEX CONCURRENTLY customers_email_key_idx ON customers (lower(email));
-- se falhar por duplicata, o índice fica INVALID: resolva as duplicatas (consulta com GROUP BY ... HAVING count(*) > 1) e refaça
ALTER TABLE customers ADD CONSTRAINT customers_email_key UNIQUE USING INDEX customers_email_key_idx;  -- só aceita índice sobre colunas, não expressão
```

Observação: `ADD CONSTRAINT ... USING INDEX` não aceita índice de expressão; para unicidade case-insensitive mantenha o próprio índice único (Inferido).

### 4.5 Coluna nova com default

```sql
SET lock_timeout = '5s';
ALTER TABLE orders ADD COLUMN channel TEXT NOT NULL DEFAULT 'web';   -- default constante: metadado, sem reescrita (V-10)
-- default volátil (ex.: gen_random_uuid()): adicione a coluna sem default, faça backfill em lotes e só então defina o default para novas linhas
```

### 4.6 Trocar tipo (`int` -> `bigint`) ou renomear

Não use DDL direto: siga as seis fases em [expand-contract-e-backfill.md](expand-contract-e-backfill.md). O `ALTER COLUMN TYPE` reescreve a tabela sob `ACCESS EXCLUSIVE` (Inferido; em estudo único o `integer` -> `bigint` parou a aplicação por ~8,8 s num banco de 453 MB, V-22, C: ilustra, não prova).

### 4.7 Remover coluna

Contract em duas implantações: (1) aplicação deixa de ler e escrever a coluna (e de usá-la em `SELECT *` com statements preparados, que podem falhar com "cached plan must not change result type", Inferido); (2) depois da janela de observação, migração separada com `DROP COLUMN` sob `lock_timeout`. Faça backup lógico da coluna antes se houver chance de precisar do dado.

## 5. Timeouts, retry e conexão

Valores de partida (V-18, README do strong_migrations, MIT; Inferido como ponto de partida, medir no ensaio):

| Onde | Parâmetro | Partida | Efeito |
| --- | --- | --- | --- |
| Sessão da migração | `lock_timeout` | `10s` (receitas acima usam `5s`: ajuste) | aborta o DDL se não obtiver o lock, em vez de formar fila |
| Sessão da migração | `statement_timeout` | `1h` | teto para scans/validações longas |
| Sessão da migração | `idle_in_transaction_session_timeout` | definir (V-19 recomenda o parâmetro; valor é seu) | derruba transação esquecida aberta |
| Aplicação | `connect_timeout` 5, `statement_timeout` 15 s, `lock_timeout` 10 s | exemplos do README | protege o app contra espera longa |

Política de retry: se o DDL falhar com SQLSTATE `55P03` (lock indisponível), espere com backoff e jitter e tente de novo, no máximo N vezes (ex.: 5); depois pare e reporte. Em `57014` (statement timeout) não repita automaticamente: investigue. Registre cada tentativa.

Conexão: migre por conexão direta ao servidor, não pelo pooler. Com PgBouncer em modo transação, `SET` de sessão pode vazar para outro cliente; use `ALTER ROLE migrador SET lock_timeout = '10s'` (V-18, V-35).

## 6. Monitoramento durante a migração

Consultas de leitura para o usuário rodar em outra sessão (sem efeito colateral):

```sql
-- quem espera e por quê
SELECT pid, state, wait_event_type, wait_event,
       now() - xact_start AS xact_age, left(query, 100) AS query
FROM pg_stat_activity
WHERE datname = current_database() AND pid <> pg_backend_pid()
ORDER BY xact_start NULLS LAST;

-- quem bloqueia quem
SELECT pid, pg_blocking_pids(pid) AS blocked_by, left(query, 100) AS query
FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid)) > 0;

-- locks mantidos na tabela alvo
SELECT l.pid, l.mode, l.granted FROM pg_locks l WHERE l.relation = 'public.orders'::regclass;
```

Antes de confirmar uma migração com mais de uma tabela, olhe `pg_locks` (V-19). Em réplica: acompanhe lag (`pg_stat_replication.replay_lag` na primária).

## 7. Roteiro de ensaio em cópia

Para o usuário executar em ambiente não produtivo (V-22 como motivação; base nos itens V-10, V-11, V-18):

1. Crie cópia com **tamanho e distribuição reais**: dump/restore anonimizado ou branch/snapshot do provedor. Preserve duplicatas e NULLs, porque são eles que fazem `VALIDATE` e índices únicos falharem.
2. Conecte **direto** ao servidor (sem pooler) com o papel que a migração usará.
3. Gere carga de escrita parecida com a produção na tabela alvo, se possível.
4. Em outra sessão, rode as consultas da seção 6 durante a migração e registre: duração de cada comando, maior tempo de espera, picos de `wait_event_type = 'Lock'`.
5. Compare contagens e invariantes antes e depois (`SELECT count(*)`, `SELECT count(*) WHERE coluna IS NULL`, checagem de unicidade).
6. Rode a migração **duas vezes** (ou o job de backfill duas vezes) para provar idempotência (V-38).
7. Ensaie o rollback de cada fase e registre o que só a restauração resolve.
8. Anote os números reais no plano. Sem este ensaio, durações e "sem downtime" são Suposição.

## 8. Rollback e critério de interrupção

- Reverter código não reverte schema; schema aditivo (expand) é reversível parando de usar; remoção e conversão com perda exigem backup e restauração testada (brain; ver `backup-restore-runbook`).
- Interrompa e reverta a fase se: lock espera acima do orçamento (ex.: 2x o `lock_timeout`), fila crescente em `pg_stat_activity`, taxa de erro da aplicação acima do acordado, divergência de contagem origem x destino, lag de réplica ou espaço em disco acima do limite.
- Quem decide a interrupção deve estar escrito no plano (nome ou papel), e o comando de reversão de cada fase deve estar pronto antes de começar.

## 9. Saída esperada da revisão

Lista de achados com item violado, risco e alternativa em etapas; cada afirmação rotulada Verificado, Inferido ou Suposição. Feche com "O que falta para concluir" (versão, volume, ensaio, aprovações). Template: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/plano-de-migracao.md`.
