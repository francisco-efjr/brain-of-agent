# Migrações, locks e DDL sem downtime

Sumário: 1 Método · 2 Locks do PostgreSQL · 3 Operação → lock → alternativa (PG) · 4 Timeouts e fila de locks · 5 CONCURRENTLY e índice INVALID · 6 MySQL Online DDL · 7 Expand/contract · 8 Backfill · 9 Ensaio em cópia · 10 Migração gerada por ORM · 11 Particionamento · 12 Rollback × restauração · 13 Ferramentas de terceiros (só conceito) · 14 Lacunas

Rótulos: Verificado = conferido por validador em fonte A/B (item V-nn em `fontes.md`); Inferido = conhecimento estável do domínio ou leitura minha; Suposição = precisa de medição. Versões: PostgreSQL 18 e MySQL 8.4 foram as páginas lidas. Confira a documentação da versão instalada (`https://www.postgresql.org/docs/<versão>/sql-altertable.html`, `https://dev.mysql.com/doc/refman/<versão>/en/innodb-online-ddl-operations.html`).

## 1. Método

1. Identifique engine, versão, ferramenta de migração, tamanho da tabela, réplicas e pooler.
2. Para cada comando DDL, escreva o lock esperado e se bloqueia leitura ou escrita. Sem essa linha, a revisão não terminou.
3. Reescreva o comando em etapas que seguram lock curto (seções 3 e 6).
4. Defina orçamento (lock, duração, espaço) e critério de interrupção antes de rodar.
5. Ensaie em cópia com volume e distribuição reais. "Rápido no meu banco local" não prova "sem downtime" (brain; V-22 como exemplo motivador, classe C).
6. A aplicação em qualquer ambiente é ação do usuário. O plugin entrega plano e SQL revisado.

## 2. Locks do PostgreSQL (V-10)

Oito modos, do mais fraco ao mais forte. Só `ACCESS EXCLUSIVE` bloqueia um `SELECT` simples. Comandos típicos (documentação de locking; conferir na versão):

| Modo | Tomado por (exemplos) | Bloqueia |
| --- | --- | --- |
| ACCESS SHARE | `SELECT` | só ACCESS EXCLUSIVE |
| ROW SHARE | `SELECT … FOR UPDATE/SHARE` | EXCLUSIVE e ACCESS EXCLUSIVE |
| ROW EXCLUSIVE | `INSERT`, `UPDATE`, `DELETE` | SHARE e acima |
| SHARE UPDATE EXCLUSIVE | `VACUUM` simples, `ANALYZE`, `CREATE INDEX CONCURRENTLY`, `VALIDATE CONSTRAINT` | ele mesmo e acima (não bloqueia leitura nem escrita) |
| SHARE | `CREATE INDEX` sem CONCURRENTLY | escrita (INSERT/UPDATE/DELETE); leitura passa |
| SHARE ROW EXCLUSIVE | `ADD FOREIGN KEY` (nas duas tabelas), `CREATE TRIGGER` | escrita |
| EXCLUSIVE | `REFRESH MATERIALIZED VIEW CONCURRENTLY` | tudo menos ACCESS SHARE |
| ACCESS EXCLUSIVE | maioria dos `ALTER TABLE`, `DROP TABLE`, `TRUNCATE`, `VACUUM FULL`, `REINDEX` | tudo, inclusive `SELECT` |

Regras que mudam decisões (Verificado V-10): `ALTER TABLE` usa `ACCESS EXCLUSIVE` salvo exceção; ao combinar subcomandos vale o mais forte; deadlock é detectado e uma das transações é abortada.

## 3. Operação → lock/efeito → alternativa (PostgreSQL)

| Operação | Efeito | Alternativa em etapas | Rótulo |
| --- | --- | --- | --- |
| `ADD COLUMN` sem default ou com default constante | só metadado; lock exclusivo curto | direto, com `lock_timeout` | Verificado (V-10: default não volátil não reescreve) |
| `ADD COLUMN` com default volátil (ex.: `clock_timestamp()`) | reescreve a tabela inteira | adicionar nullable → backfill em lotes → `SET DEFAULT` para linhas novas | Verificado V-10 |
| `SET NOT NULL` direto | scan da tabela sob ACCESS EXCLUSIVE | `ADD CONSTRAINT c CHECK (col IS NOT NULL) NOT VALID` → backfill dos NULLs → `VALIDATE CONSTRAINT c` → `SET NOT NULL` (pula o scan se há CHECK válido) → `DROP CONSTRAINT c` | Verificado V-10, V-18; PG 18 documenta `NOT VALID` direto para not-null, versões anteriores usam o caminho via CHECK |
| `ADD CONSTRAINT … CHECK` | valida todas as linhas sob lock forte | `NOT VALID`, depois `VALIDATE CONSTRAINT` (SHARE UPDATE EXCLUSIVE) | Verificado V-10 |
| `ADD FOREIGN KEY` | SHARE ROW EXCLUSIVE nas duas tabelas e scan | `NOT VALID` + `VALIDATE CONSTRAINT`; índice na coluna filha (PG não cria) | Verificado V-10, V-32 |
| `ADD UNIQUE` / `ADD PRIMARY KEY` | constrói índice sob lock forte | `CREATE UNIQUE INDEX CONCURRENTLY` e então `ADD CONSTRAINT … USING INDEX` | Inferido (documentado em ALTER TABLE; conferir) |
| `CREATE INDEX` | bloqueia escrita durante o build | `CREATE INDEX CONCURRENTLY`, fora de transação | Verificado V-11 |
| `DROP INDEX` | ACCESS EXCLUSIVE | `DROP INDEX CONCURRENTLY` (também fora de transação) | Inferido |
| `ALTER COLUMN TYPE` (ex.: `int` → `bigint`) | normalmente reescreve a tabela sob ACCESS EXCLUSIVE | expand/contract (seção 7). Exceções sem reescrita existem; conferir a tabela da versão | Inferido; V-22 relata parada de ~8,8 s num caso de 4 milhões de linhas (classe C) |
| `RENAME COLUMN/TABLE` | metadado rápido, mas quebra versões antigas da aplicação | expand/contract ou view de compatibilidade | Inferido |
| `DROP COLUMN` | metadado rápido, mas quebra leitores antigos | só na fase de limpeza (seção 7) | Inferido |
| `ALTER TYPE … ADD VALUE` (enum) | restrições dependem da versão (uso do valor na mesma transação) | conferir a doc da versão; preferir tabela de domínio quando o conjunto muda | Inferido |
| `ATTACH PARTITION` | scan com ACCESS EXCLUSIVE se faltar CHECK equivalente | criar CHECK antes, anexar, remover o CHECK | Verificado V-13 |
| `DETACH PARTITION … CONCURRENTLY` | exige só SHARE UPDATE EXCLUSIVE | usar para retenção em vez de `DELETE` em massa | Verificado V-13 |

Exemplo completo (PG 15, `orders.customer_id` com NULLs, 80 milhões de linhas):

```sql
-- Fase 1: restrição sem validar (lock exclusivo muito curto)
SET lock_timeout = '5s';
ALTER TABLE orders ADD CONSTRAINT orders_customer_id_nn
  CHECK (customer_id IS NOT NULL) NOT VALID;
-- Fase 2: corrigir os NULLs em lotes (seção 8); novas linhas já são checadas
-- Fase 3: validar (SHARE UPDATE EXCLUSIVE; leitura e escrita continuam)
ALTER TABLE orders VALIDATE CONSTRAINT orders_customer_id_nn;
-- Fase 4: com CHECK válido, o scan é dispensado
ALTER TABLE orders ALTER COLUMN customer_id SET NOT NULL;
ALTER TABLE orders DROP CONSTRAINT orders_customer_id_nn;
```

Rótulo do exemplo: SQL conforme V-10; duração real é Suposição até o ensaio.

## 4. Timeouts e fila de locks

- DDL que espera lock bloqueia as consultas que chegam depois dele, mesmo as que seriam compatíveis com quem segura o lock (Verificado V-19: a espera de DDL bloqueia consultas posteriores). Uma transação aberta esquecida basta para formar fila.
- Ponto de partida (Inferido; valores do README do strong_migrations, V-18): na sessão da migração `lock_timeout = 10s` e `statement_timeout = 1h`; no app `connect_timeout 5`, `statement_timeout 15s`, `lock_timeout 10s`. Meça no ensaio; não aprove valor sem volume. A página oficial de `lock_timeout` não foi lida (L-05).
- `lock_timeout` curto + retry transforma "fila bloqueando produção" em "tentativa falhou, tente de novo". Repita o comando fora do pico.
- `idle_in_transaction_session_timeout` limita transações ociosas (V-19).
- Pooler em modo transaction (PgBouncer): `SET` de sessão vaza para outro cliente; defina timeouts por `ALTER ROLE migrador SET lock_timeout = '10s'` (V-18). Migre por conexão direta, não pooled (V-35).
- Antes de confirmar, olhe `pg_locks` e `pg_stat_activity` por esperas (V-19, V-22).

## 5. CONCURRENTLY e índice INVALID (V-11)

- Não roda dentro de bloco de transação. Duas varreduras e espera por transações antigas; só um build concorrente por tabela.
- Falha deixa índice `INVALID`: ignorado pelas consultas, mas custa escrita. Detecção: `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;`. Correção: `DROP INDEX CONCURRENTLY nome;` e nova tentativa, ou `REINDEX INDEX CONCURRENTLY nome;`.
- `CREATE INDEX CONCURRENTLY IF NOT EXISTS` pode ignorar o comando quando já existe um índice INVALID de mesmo nome (Inferido; sem fonte oficial). Cheque `indisvalid` depois.
- Tabela particionada: construir concorrentemente em cada partição, depois criar o índice do pai sem CONCURRENTLY (só metadados) (Verificado V-11).
- Ferramentas de migração: Alembic e Django envolvem a migração em transação em PostgreSQL por padrão. Alembic: `with op.get_context().autocommit_block(): op.create_index(..., postgresql_concurrently=True)`. Django: `from django.contrib.postgres.operations import AddIndexConcurrently` e `atomic = False` na classe `Migration`. Confirme na doc da versão instalada. Flyway, Liquibase, Prisma, EF: comportamento não validado (L-04); abra a doc.

## 6. MySQL Online DDL (V-16, válido para 8.4)

| Operação | Algoritmo/lock | Observação |
| --- | --- | --- |
| `ADD COLUMN`, `DROP COLUMN` | `INSTANT` (padrão no 8.4) | não vale com `ROW_FORMAT=COMPRESSED` nem com FULLTEXT |
| `ADD INDEX` secundário | `INPLACE` com DML concorrente | consome I/O; acompanhe réplicas |
| `ADD COLUMN … AUTO_INCREMENT` | mínimo `INPLACE, LOCK=SHARED` | sem DML concorrente |
| Mudar tipo de coluna | só `ALGORITHM=COPY`; sem DML concorrente | reduzir `VARCHAR` também exige COPY |
| Adicionar PK | reconstrói a tabela | |
| Remover PK sem criar outra | só COPY | |

- Declare `ALGORITHM=` e `LOCK=` explicitamente: se a operação não suporta, o comando falha em vez de degradar sem aviso (visto nos exemplos da doc; não enunciado como regra universal).
- MySQL não tem DDL transacional; uma migração que falha no meio pode precisar de desfazimento manual (V-30). Uma mudança por arquivo.
- Em 8.0 e 9.x o quadro difere: confirme na versão. Para tabelas grandes com mudança de tipo, a ideia de gh-ost (binlog, sem triggers, `--test-on-replica`, pausa e throttle, V-17) é referência conceitual; não instalar sem revisão do usuário.

## 7. Expand → backfill → verify → migrate → contract

Princípio (brain; V-20): durante o deploy, versões antigas e novas da aplicação coexistem; migração só no startup de todas as réplicas e rollback de aplicação não desfazem schema.

| Fase | Ação | Saída verificável | Rollback |
| --- | --- | --- | --- |
| 1 Expand | criar estrutura nova sem remover a antiga; aplicação escreve nas duas | escrita dupla sem erro por N dias | parar a escrita nova |
| 2 Backfill | copiar em lotes, idempotente, retomável, fora de transação longa | contagem e amostra conferidas | interromper; dado antigo intacto |
| 3 Verify | comparar leituras antiga e nova sem alterar a resposta | divergência abaixo do limite acordado | n/a |
| 4 Migrate | trocar a leitura por flag, em fração crescente | métricas estáveis em cada faixa | voltar a flag |
| 5 Contract (escrita) | escrita só no novo caminho; código legado lança erro por um ciclo | nenhum acesso ao caminho antigo nos logs | reativar escrita dupla |
| 6 Limpeza | remover coluna/tabela/trigger/view antiga em migração separada, após a janela | registro do que foi removido | restaurar de backup (seção 12) |

Dual-write sem atomicidade pode divergir: exige reconciliação periódica (brain). Exemplo `nome` → `nome_completo`: fase 1 `ALTER TABLE users ADD COLUMN full_name text;` e a aplicação grava ambos; fase 2 backfill; fase 4 leitura de `full_name`; fase 6 `DROP COLUMN name`. Revisão em camadas (V-36): ferramenta/IA, engenheiro (regra de negócio), colega.

Critério de interrupção (brain): duração ou lock acima do orçamento, crescimento inesperado de erro, divergência entre campos, esgotamento de capacidade (disco, WAL, lag de réplica).

## 8. Backfill

Requisitos: lotes pequenos e observáveis, checkpoint, idempotência, não sobrescrever dado mais novo (V-38), commit por lote.

```sql
-- PostgreSQL; o script do usuário repete até retornar 0 linhas e guarda o maior id como checkpoint
WITH lote AS (
  SELECT id FROM users
  WHERE full_name IS NULL AND id > :checkpoint
  ORDER BY id
  LIMIT 5000
  FOR UPDATE SKIP LOCKED
)
UPDATE users u SET full_name = u.name
FROM lote WHERE u.id = lote.id
RETURNING u.id;
```

Rodar duas vezes não muda o resultado (a condição `full_name IS NULL` é o critério de conflito). Ajuste o tamanho do lote à latência observada e pause se `replay_lag` ou o p95 da aplicação subir. Depois, valide (prompt P-24): contagem origem × destino, unicidade, nulos.

## 9. Ensaio em cópia

Cópia com volume e distribuição reais (duplicatas, NULLs, linhas largas), conexão direta, mesma versão do servidor. Em outra sessão, observe `pg_stat_activity` (`wait_event_type = 'Lock'`) e meça: duração, pico de lock, crescimento de WAL, lag de réplica. Compare contagens antes e depois. Sem cópia: declare "sem downtime" como Suposição. Dados pessoais na cópia seguem minimização (brain).

## 10. Migração gerada por ORM é rascunho (V-30)

- Alembic: autogenerate "não pretende ser perfeito"; renomeação aparece como `drop_column` + `add_column` (perda de dados); constraints sem nome não são detectadas; `server_default` é impreciso; `Enum` sem suporte nativo vira CHAR + CHECK; detecção de CHECK é por nome, nunca por expressão. `alembic upgrade head --sql` mostra o SQL (Inferido; confirme).
- Django: `sqlmigrate` mostra o SQL; `RunPython` usa modelos históricos (`apps.get_model()`); callable reverso é opcional (sem ele, reverter gera exceção); PostgreSQL e SQLite têm DDL transacional, MySQL não; `atomic = False` desliga.
- Checklist: ler o SQL, nomear constraints, conferir renomeações, `server_default`, enums, ordem entre tabelas, e se a ferramenta embrulha em transação.
- `synchronize`/`create_all` desligados em produção; sem `DROP`/`TRUNCATE` dentro de migração (V-29, redação própria).
- Prisma, Drizzle, TypeORM, EF, Flyway, Liquibase, Atlas: sem fonte validada (L-04). Abra a doc da versão instalada antes de afirmar qualquer passo.

## 11. Particionamento (PostgreSQL, V-13)

Range, list, hash. Poda depende da chave, não de índices. Escolha a chave pelo `WHERE` e pela retenção. PK e UNIQUE devem incluir todas as colunas da chave, que não pode ter expressões. "Até alguns milhares" de partições funcionam com poda; "nunca assuma que mais partições é melhor". Retenção: `DROP`/`DETACH` evita o custo de VACUUM de um `DELETE` em massa. Migrar tabela existente para particionada exige tabela nova + backfill + troca (expand/contract); sharding e particionamento fora do PG: sem fonte (L-09).

## 12. Rollback × restauração

Rollback de aplicação não desfaz schema nem dado transformado (brain). Distinga: reverter código; manter compatibilidade entre versões; restaurar dados. `DROP COLUMN` ou conversão com perda exige backup e plano de restauração (ver `operacao-e-seguranca-de-dados.md`), não uma migration "down". Não prometa rollback de dados perdidos.

## 13. Ferramentas de terceiros (conceito; não instalar pelo plugin)

strong_migrations (V-18, Ruby, MIT): lista de operações perigosas; backfill perigoso não é detectado. gh-ost (V-17, MIT): MySQL via binlog. pgroll (V-21, Apache-2.0, só PG): schemas versionados com views e triggers bidirecionais, com custo. Todas são código de terceiros: o usuário revisa e decide.

## 14. Lacunas

`lock_timeout` sem página oficial lida (L-05); VACUUM/bloat, `pg_stat_statements`, PgBouncer sem fonte; upgrade de versão maior (`pg_upgrade`, réplica lógica) sem fonte; MySQL 8.0/9.x e SQL Server sem fonte de DDL online; ORMs além de Alembic e Django (L-04).

Atribuição: seções 1, 7 (princípio, interrupção), 8 e 12 adaptam texto de Brain of Agent, `brains/fullstack/references/dados-e-migracoes.md` (MIT, © 2026 Brain of Agent contributors).
