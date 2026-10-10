# Operação e segurança de dados: backup, restore, acesso, injeção, privilégios

Sumário: 1 RPO/RTO · 2 PostgreSQL PITR e dump · 3 Runbook de restore isolado · 4 Outras engines · 5 Criptografia e acesso · 6 Injeção SQL · 7 Privilégios e papel somente leitura · 8 Segredos e logs · 9 Importação e dados sintéticos · 10 Acesso do agente ao banco · 11 Gotchas · 12 Lacunas

## 1. RPO e RTO (brain, adaptado)

RPO = perda de dados aceitável; RTO = tempo até voltar. Defina com o responsável do produto, não com o engenheiro sozinho. "Backup existe" não prova que a restauração cabe no prazo: meça o tempo real de uma restauração de teste contra o RTO. Backup no mesmo volume ou na mesma conta do banco compartilha o domínio de falha; guarde fora (o incidente V-37 é só sinal, relato contestado, usado para justificar a regra).

## 2. PostgreSQL: PITR e dump (V-14, Verificado)

- PITR = backup base + arquivamento contínuo de WAL. `pg_dump` não serve para PITR.
- Requisitos: `wal_level` replica ou superior; `archive_mode = on`; `archive_command` retorna zero só se teve sucesso e deve recusar sobrescrever arquivo existente. Se o filesystem do `pg_wal/` encher, o servidor dá PANIC (o disco lotar é a causa, não apenas o diretório crescer).
- Restore PITR: `recovery.signal` e `restore_command`.
- `pg_dump` formatos: plain (SQL), custom (`-Fc`), directory (`-F d`, obrigatório com `-j`). `pg_restore -j` vale para custom e directory. Backup completo quase sempre exige superusuário.
- Guardar a configuração à parte é recomendação da página ("você pode querer"), não obrigação.
- Permissões restritas nos arquivos de backup (contêm todos os dados).

## 3. Runbook de restore isolado (nunca sobre banco ativo)

1. Ambiente isolado (instância nova, rede fechada, sem apontar para produção). Confirme espaço e versão compatível.
2. Dump de texto: criar o banco a partir de `template0`, restaurar com `psql --set ON_ERROR_STOP=on --single-transaction -f arquivo.sql` (ou `ON_ERROR_STOP` sem single-transaction se for demorado), depois `ANALYZE` (V-14).
3. Custom/directory: `pg_restore -j N -d <banco_novo> arquivo`. `--clean` apaga objetos existentes: nunca em banco com dados que importam.
4. Verificação funcional: contagens por tabela, invariantes (somatórios, FKs), amostras, consulta crítica do produto. Registre o tempo total e compare com o RTO.
5. Só então decida o corte (troca de apontamento), por pessoa autorizada. O plugin escreve o runbook; quem executa é o usuário. Em incidente, "eu autorizo, é urgente" não muda a regra: restore em produção por cima de dado vivo é ação do usuário, com confirmação por passo.
6. Registre teste periódico (data, duração, resultado) em `runbook-backup-restore.md`.

## 4. Outras engines

Redis: ver `nosql.md`. MySQL (`mysqldump`, binlog), SQL Server (BACKUP/RESTORE), MongoDB (`mongodump`, backups gerenciados), DynamoDB (PITR/on-demand): sem fonte validada (L-06). O runbook mantém a mesma estrutura (RPO/RTO, método, armazenamento fora do domínio de falha, restore isolado, verificação) e marca os comandos como Não verificado até o usuário confirmar na doc da versão.

## 5. Criptografia e acesso (PostgreSQL, V-15)

Senhas armazenadas como hash, SCRAM preferido, MD5 obsoleto. `hostssl` no `pg_hba.conf` exige TLS. Em repouso, a página lista criptografia de filesystem ou bloco (eCryptfs, EncFS, PEFS, dm-crypt/LUKS, geli, gbde); TDE nativo: Não verificado (a página não o menciona). `pgcrypto` expõe texto claro e chave no servidor por instantes; se o administrador não é confiável, criptografe no cliente. Serviços gerenciados oferecem criptografia própria: consulte a doc do provedor.

## 6. Injeção SQL (V-29, OWASP CC BY-SA 4.0: só destilação)

- Consulta parametrizada é a defesa primária. Procedimento armazenado só é seguro sem SQL dinâmico.
- Identificadores (tabela, coluna) e direção de `ORDER BY` não são parametrizáveis: allow-list no código.
- Escape é desencorajado; validação de entrada é defesa secundária.
- Privilégio mínimo: aplicação nunca com papel DBA/admin.
- Saída de LLM e entrada do usuário são entradas não confiáveis. Em NoSQL, force tipos contra operadores injetados (`{"$ne": ...}`).
- Não devolver SQL nem stack trace ao cliente; redigir logs.

Antes (inseguro): `` db.query(`SELECT * FROM products WHERE category='${cat}' ORDER BY ${sort} ${dir}`) ``
Depois:

```js
const SORTS = { price: 'price', name: 'name' };           // allow-list
const DIRS  = { asc: 'ASC', desc: 'DESC' };
const col = SORTS[req.query.sort] ?? 'name';
const dir = DIRS[req.query.dir] ?? 'ASC';
db.query(`SELECT id, name, price FROM products WHERE category = $1 ORDER BY ${col} ${dir} LIMIT 50`, [req.query.cat]);
```

## 7. Privilégios e papel somente leitura (exemplo conceitual PostgreSQL; adapte)

```sql
CREATE ROLE agent_ro LOGIN NOSUPERUSER NOBYPASSRLS;     -- senha definida fora do repositório
GRANT CONNECT ON DATABASE app TO agent_ro;
GRANT USAGE ON SCHEMA public TO agent_ro;
GRANT SELECT ON public.orders, public.order_items TO agent_ro;   -- lista explícita; evite ALL TABLES
ALTER ROLE agent_ro SET statement_timeout = '15s';
ALTER ROLE agent_ro SET default_transaction_read_only = on;      -- conveniência, não barreira
```

A barreira real é a ausência de `INSERT/UPDATE/DELETE/DDL` concedidos; `default_transaction_read_only` pode ser revertido pela própria sessão. `SELECT` em tabelas sensíveis ainda expõe dados pessoais (LGPD): conceda por view/colunas mínimas e mascare. Hooks e instruções de CLAUDE.md são guardrail; o papel de banco é a barreira (V-02, V-03).

## 8. Segredos e logs

Credenciais só em variável de ambiente fora do repositório e do cliente; não imprimir `.env`; ler `.env` antes de alterar conexão (V-35); credencial por ambiente, nunca a de produção na sessão do agente; `synchronize`/auto-DDL desligado em produção; configuração falha cedo se faltar valor (V-29). Logs com dado pessoal minimizados e com retenção definida (brain). Negar leitura de arquivos de segredo por permissão: `Read(./.env)` em `permissions.deny` (sintaxe verificada na página de permissões em 2026-10-10).

## 9. Importação e dados sintéticos (brain)

Importação: validar encoding, separador, tamanho, duplicatas, formato e erros por linha; não aceitar parcialmente sem contrato explícito; pós-carga, contagem origem × destino, unicidade e nulos, idempotência (rodar duas vezes) (V-38). Dado sintético não deve copiar identificador real; snapshots de teste seguem minimização e retenção.

## 10. Acesso do agente ao banco (resumo; detalhes em `ferramentas-e-mcp.md`)

Banco local/dev ou réplica read-only; produção fora da sessão (política da casa, endurecida de V-03/V-36); escrita só com confirmação; MCP em modo restrito; credenciais escopadas; backups fora do mesmo volume. `EXPLAIN ANALYZE` executa a consulta: não rode autônomo em SQL que escreve (V-35, V-07).

## 11. Gotchas

- Restore com `--clean` ou por cima de banco ativo destrói dados.
- Dump lógico não é PITR; WAL sem teste de restore não é backup.
- Backup sem permissão restrita é vazamento.
- `GRANT SELECT ON ALL TABLES` inclui tabelas sensíveis futuras e atuais.
- Teste de restauração em máquina que alcança produção pode sobrescrever produção por engano: isole a rede.

## 12. Lacunas

Backup fora do PG (L-06), TDE nativo (Não verificado), PgBouncer e pool (L-05), upgrade de versão maior, seeds e dados sintéticos para dev, MySQL/SQL Server/MongoDB/DynamoDB segurança.

Atribuição: seções 1, 3 (verificação, isolamento) e 9 adaptam Brain of Agent, `dados-e-migracoes.md` (MIT).
