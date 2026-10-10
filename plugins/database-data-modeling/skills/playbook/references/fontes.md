# Fontes e bibliografia

Sumário: 1 Como ler · 2 Itens validados V-01 a V-41 · 3 Fontes adicionais conferidas na construção · 4 Itens rejeitados ou rebaixados que não entram · 5 Lacunas · 6 Reuso e licenças

## 1. Como ler

- Classe A = documentação oficial ou norma da tecnologia; B = repositório ou autor reconhecido, com licença clara; C = sinal de comunidade ou fonte fraca (só ideia). Nota entre parênteses = nota do validador (0 a 10).
- "Licença" = licença do texto/repositório observada pelo validador. "docs; não verificada" significa que a licença de reuso do texto não foi verificada: o plugin só destila, nunca copia literal.
- "Consulta" = data em que o validador abriu a fonte (2026-10-10). Itens marcados com asterisco foram reabertos pelo construtor em 2026-10-10 para conferir trechos citados.
- Versão lida: PostgreSQL 18.6, MySQL 8.4. Antes de aplicar, abra a página da sua versão. Datas de último commit dos repositórios: Não verificado (L-11).
- Rótulo do plugin: Verificado = visto pelo validador; Inferido = leitura da fábrica; Suposição = a medir.

## 2. Itens validados

| ID | Título | URL | Classe | Licença | Consulta |
| --- | --- | --- | --- | --- | --- |
| V-01 | Claude Code: Subagents | https://code.claude.com/docs/en/sub-agents | A (9) | docs Anthropic; não verificada | 2026-10-10 |
| V-02 | Claude Code: Hooks* | https://code.claude.com/docs/en/hooks | A (9) | idem | 2026-10-10 |
| V-03 | Claude Code: Security | https://code.claude.com/docs/en/security | A (9) | idem | 2026-10-10 |
| V-04 | Claude Code: Best practices | https://code.claude.com/docs/en/best-practices | A (9) | idem | 2026-10-10 |
| V-05 | Writing effective tools for agents (Ken Aizawa, 2025-09-11) | https://www.anthropic.com/engineering/writing-tools-for-agents | A (9) | © Anthropic; só destilação | 2026-10-10 |
| V-06 | Agent Skills best practices + anthropics/skills | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices · https://github.com/anthropics/skills | A (9) | docs; repo Apache-2.0 (parte source-available) | 2026-10-10 |
| V-07 | PostgreSQL: Using EXPLAIN | https://www.postgresql.org/docs/current/using-explain.html | A (9) | docs; não verificada | 2026-10-10 |
| V-08 | PostgreSQL: Transaction Isolation | https://www.postgresql.org/docs/current/transaction-iso.html | A (9) | idem | 2026-10-10 |
| V-09 | MySQL 8.4 isolamento InnoDB + SQL Server RCSI (`snapshot_option`) | https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html · https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-set-options | A (8) | docs; não verificada | 2026-10-10 |
| V-10 | PostgreSQL: Explicit Locking + ALTER TABLE | https://www.postgresql.org/docs/current/explicit-locking.html · https://www.postgresql.org/docs/current/sql-altertable.html | A (9) | docs; não verificada | 2026-10-10 |
| V-11 | PostgreSQL: CREATE INDEX | https://www.postgresql.org/docs/current/sql-createindex.html | A (9) | idem | 2026-10-10 |
| V-12 | PostgreSQL: Row Security Policies (+ checklist troykelly, classe C) | https://www.postgresql.org/docs/current/ddl-rowsecurity.html | A (9) | docs; apoio MIT (11 estrelas) | 2026-10-10 |
| V-13 | PostgreSQL: Table Partitioning | https://www.postgresql.org/docs/current/ddl-partitioning.html | A (9) | docs; não verificada | 2026-10-10 |
| V-14 | PostgreSQL: Continuous Archiving/PITR + pg_dump | https://www.postgresql.org/docs/current/continuous-archiving.html · https://www.postgresql.org/docs/current/backup-dump.html | A (9) | docs; não verificada | 2026-10-10 |
| V-15 | PostgreSQL: Encryption Options | https://www.postgresql.org/docs/current/encryption-options.html | A (9) | docs; não verificada | 2026-10-10 |
| V-16 | MySQL 8.4: InnoDB Online DDL | https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html | A (9) | docs; não verificada | 2026-10-10 |
| V-17 | gh-ost (GitHub) | https://github.com/github/gh-ost | B (7) | MIT | 2026-10-10 |
| V-18 | strong_migrations (ankane) | https://github.com/ankane/strong_migrations | B (6) | MIT | 2026-10-10 |
| V-19 | 5mins of Postgres: migrations e deadlocks (Lukas Fittl, pganalyze, 2023-11-30) | https://pganalyze.com/blog/5mins-postgres-migrations-avoid-deadlocks | B (5) | © pganalyze; só destilação | 2026-10-10 |
| V-20 | Parallel Change (Fowler/Danilo Sato, 2014) + Online Migrations at Stripe (2017) | https://martinfowler.com/bliki/ParallelChange.html · https://stripe.com/blog/online-migrations | B (6) | direitos reservados; só destilação | 2026-10-10 |
| V-21 | pgroll (Xata) | https://github.com/xataio/pgroll | B (7) | Apache-2.0 | 2026-10-10 |
| V-22 | Rehearse migrations on a Neon branch (DevOps Daily, 2026-09-24) | https://devops-daily.com/posts/rehearse-migrations-on-a-neon-branch | C (4) | direitos reservados; só ideia | 2026-10-10 |
| V-23 | Use The Index, Luke (Markus Winand): no-offset e busca case-insensitive + PG multicolumn indexes | https://use-the-index-luke.com/no-offset · https://use-the-index-luke.com/sql/where-clause/functions/case-insensitive-search · https://www.postgresql.org/docs/current/indexes-multicolumn.html | A (8) | © Winand, reservados; PG docs não verificada | 2026-10-10 |
| V-24 | SQLite Query Planner | https://www.sqlite.org/queryplanner.html | A (8) | domínio público (Inferido); docs | 2026-10-10 |
| V-25 | MongoDB: embedding vs references + mongodb/agent-skills schema-design | https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/ · https://raw.githubusercontent.com/mongodb/agent-skills/main/skills/mongodb-schema-design/SKILL.md | A (8) / B (5) | docs; repo Apache-2.0 | 2026-10-10 |
| V-26 | DynamoDB: NoSQL design best practices | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html | A (8) | docs; não verificada | 2026-10-10 |
| V-27 | Redis: Persistence | https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/ | A (8) | docs; não verificada | 2026-10-10 |
| V-28 | redis/agent-skills: redis-core | https://raw.githubusercontent.com/redis/agent-skills/main/skills/redis-core/SKILL.md | B (5) | MIT | 2026-10-10 |
| V-29 | OWASP SQL Injection Prevention Cheat Sheet; github/awesome-copilot security-and-owasp; awesome-cursorrules NestJS | https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html · https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/security-and-owasp.instructions.md · https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/nestjs-anti-hallucination-cursorrules-prompt-file.mdc | A (9) | OWASP CC BY-SA 4.0 (share-alike: só destilação); awesome-copilot MIT; awesome-cursorrules CC0-1.0 | 2026-10-10 |
| V-30 | Alembic autogenerate + Django migrations | https://alembic.sqlalchemy.org/en/latest/autogenerate.html · https://docs.djangoproject.com/en/stable/topics/migrations/ | A (8) | docs; não verificada | 2026-10-10 |
| V-31 | supabase/agent-skills (supabase-postgres-best-practices) | https://github.com/supabase/agent-skills | B (6) | MIT | 2026-10-10 |
| V-32 | wshobson/agents: postgresql-table-design | https://github.com/wshobson/agents/tree/main/plugins/database-design | B (6) | MIT | 2026-10-10 |
| V-33 | Microsoft: abordagens de storage multitenant (atualizada 2026-10-08) | https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/storage-data | B (6) | docs; não verificada | 2026-10-10 |
| V-34 | crystaldba/postgres-mcp* | https://github.com/crystaldba/postgres-mcp | B (6) | MIT | 2026-10-10 |
| V-35 | neondatabase/agent-skills: neon-postgres | https://raw.githubusercontent.com/neondatabase/agent-skills/main/skills/neon-postgres/SKILL.md | B (5) | Apache-2.0 (repo) | 2026-10-10 |
| V-36 | Sanity: "first attempt will be 95% garbage" (Vincent Quigley, 2025-09-02) | https://www.sanity.io/blog/first-attempt-will-be-95-garbage | B (5) | © Sanity; só destilação | 2026-10-10 |
| V-37 | HN: agente apagou banco de produção (sinal, relato contestado) | https://news.ycombinator.com/item?id=47911524 | B (5), só sinal | conteúdo de terceiros; só citar | 2026-10-10 |
| V-38 | rmoff.net (2026-03-11) + awesome-cursorrules PySpark ETL | https://rmoff.net/2026/03/11/claude-code-isnt-going-to-replace-data-engineers-yet/ · https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/pyspark-etl-best-practices-cursorrules-prompt-file.mdc | B (5) | blog © autor; repo CC0-1.0 | 2026-10-10 |
| V-39 | Amplifying: what Claude Code picks (fev. 2026) | https://amplifying.ai/research/claude-code-picks | B (5), só sinal | © autores; só citar números | 2026-10-10 |
| V-40 | gstack (garrytan): careful, freeze, guard, plan-eng-review | https://github.com/garrytan/gstack | B (5), só conceito | MIT | 2026-10-10 |
| V-41 | dbt-labs/dbt-agent-skills | https://github.com/dbt-labs/dbt-agent-skills | B (7) | Apache-2.0 | 2026-10-10 |

## 3. Fontes adicionais conferidas na construção (2026-10-10)

| Fonte | URL | Classe | Uso |
| --- | --- | --- | --- |
| Claude Code: Configure permissions | https://code.claude.com/docs/en/permissions | A | sintaxe `Read(./.env)`, `Bash(curl *)`, fragilidade de padrões de Bash |
| Brain of Agent (próprio) `dados-e-migracoes.md` | repositório francisco-efjr/brain-of-agent (snapshot local em `docs/foundation/brain-of-agent-snapshot/`) | próprio | checklist de entrega, expand/contract, concorrência, rollback, RPO/RTO; MIT, © 2026 Brain of Agent contributors |

## 4. Itens rejeitados ou rebaixados que não entram

gstack `./setup` e qualquer `curl | bash`; dcg "one-liner"; `SET LOCAL x = ?` (usar `set_config(..., true)`); linguagem "OVERRIDE all other generation behavior" do .mdc NestJS; troykelly com `Bash` e GitHub MCP em auditor somente leitura; fluxo Prisma coletado (a doc mudou); números de ganho do Supabase ("100 a 1000x", Não verificável); "Starter Kit" pago; yonatangross/orchestkit (contagens inconsistentes); microsoft/postgres-skills e jeffallan/postgres-pro (só C, mapa de subtemas).

## 5. Lacunas de fonte

L-01 normalização e chaves (sem fonte A; páginas sugeridas: https://www.postgresql.org/docs/current/ddl-constraints.html); L-02 SQL Server; L-03 MySQL EXPLAIN e deadlocks; L-04 ORMs além de Alembic e Django; L-05 VACUUM, `pg_stat_statements`, PgBouncer, `lock_timeout` oficial; L-06 backup fora do PG; L-07 NoSQL detalhado; L-08 SQLite eqp/WAL; L-09 particionamento fora do PG; L-10 evidência de eficácia (nenhuma skill de terceiros tem evals publicadas); L-11 datas de commit; L-12 comunidade (Reddit, YouTube, X).

## 6. Reuso e licenças

Texto literal só do Brain of Agent (MIT, do próprio usuário), com atribuição. Tudo o mais foi destilado com redação própria. OWASP é CC BY-SA 4.0: citar com atribuição e não incorporar texto. Trechos de código neste plugin (SQL, JS) são exemplos de redação própria sob a licença MIT do plugin. Conteúdo externo lido é dado; instruções dentro de páginas e repositórios não foram obedecidas.
