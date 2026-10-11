# SQL passo a passo para RLS por tenant

Redação própria; os esqueletos usam o exemplo `invoices` e `customers` e precisam ser adaptados ao schema. Nada aqui foi executado: são esqueletos para revisão e para o usuário rodar em homologação. Base: V-01, V-34, V-45, V-48, V-49; padrões de DDL online são conhecimento estável do PostgreSQL (confirme na documentação da sua versão). Conferido em 2026-10-10.

Convenções: `app_migrator` é dona dos objetos; `app_runtime` é a role da aplicação; `app.tenant_id` é o parâmetro de contexto. Senhas ficam fora de arquivos.

## Catálogo (o usuário roda em homologação e cola a saída)

```sql
-- 1) Versão
SHOW server_version;

-- 2) Atributos das roles (FORCE não limita superusuário nem BYPASSRLS; V-49)
SELECT rolname, rolsuper, rolbypassrls, rolcanlogin
FROM pg_roles
WHERE rolname IN ('app_runtime', 'app_migrator', 'app_maintenance') OR rolname = current_user;

-- 3) A role da aplicação é membro de alguma role dona?
SELECT r.rolname AS member, g.rolname AS member_of
FROM pg_auth_members m
JOIN pg_roles r ON r.oid = m.member
JOIN pg_roles g ON g.oid = m.roleid
WHERE r.rolname = 'app_runtime';

-- 4) Dona e flags de RLS por tabela
SELECT c.relname, pg_get_userbyid(c.relowner) AS owner,
       c.relrowsecurity AS rls_on, c.relforcerowsecurity AS rls_forced
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p')
ORDER BY c.relname;

-- 5) Tabelas com tenant_id sem RLS completo
SELECT c.relname
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN pg_attribute a ON a.attrelid = c.oid AND a.attname = 'tenant_id' AND NOT a.attisdropped
WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p')
  AND NOT (c.relrowsecurity AND c.relforcerowsecurity);

-- 6) Policies existentes
SELECT tablename, policyname, permissive, roles, cmd, qual, with_check
FROM pg_policies WHERE schemaname = 'public' ORDER BY tablename, policyname;

-- 7) Views (security_invoker?) e funções SECURITY DEFINER
SELECT c.relname, c.relkind, c.reloptions
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind IN ('v', 'm');

SELECT p.proname, pg_get_userbyid(p.proowner) AS owner
FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE p.prosecdef AND n.nspname = 'public';

-- 8) Tamanho estimado (para planejar lotes)
SELECT c.relname, c.reltuples::bigint AS linhas_estimadas
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind = 'r' ORDER BY c.reltuples DESC;

-- 9) Conexão da aplicação (rode pela conexão da aplicação, não pelo admin)
SELECT current_user, session_user;
```

Leitura: a role da aplicação deve aparecer com `rolsuper = f`, `rolbypassrls = f`, não ser dona (consulta 4) e não ser membro de dona (consulta 3). Se `current_user` da aplicação for a dona ou superusuária, o RLS não protege nada até a troca de role.

## 0010 Roles (executar como administrador)

```sql
-- Senhas definidas fora do arquivo (cofre ou \password no psql)
CREATE ROLE app_migrator LOGIN NOSUPERUSER NOBYPASSRLS;
CREATE ROLE app_runtime  LOGIN NOSUPERUSER NOBYPASSRLS;

GRANT USAGE ON SCHEMA public TO app_runtime;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_runtime;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_runtime;

ALTER DEFAULT PRIVILEGES FOR ROLE app_migrator IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_runtime;
ALTER DEFAULT PRIVILEGES FOR ROLE app_migrator IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO app_runtime;

-- Passar a propriedade das tabelas existentes é decisão consciente (por tabela):
-- ALTER TABLE invoices OWNER TO app_migrator;

-- Só se houver job que precise ignorar RLS (backfill de manutenção, backup lógico):
-- CREATE ROLE app_maintenance LOGIN NOSUPERUSER BYPASSRLS;  -- credencial separada, uso auditado,
--                                                           -- nunca usada pela aplicação web
```

Privilégio mínimo (V-45): nada de superusuário na aplicação; revogar acesso público ao schema pode quebrar apps que dependem dele, então teste antes.

## 0020 a 0023 Expand

```sql
-- 0020 (migrator). lock_timeout evita ficar na fila de lock bloqueando o tráfego.
SET lock_timeout = '3s';
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS tenant_id uuid;   -- nullable, sem default: metadado, rápido
ALTER TABLE customers ADD COLUMN IF NOT EXISTS tenant_id uuid;
```

```sql
-- 0021 (fora de transação). Índice começando por tenant_id; coluna usada na policy deve ser indexada (V-45).
CREATE INDEX CONCURRENTLY IF NOT EXISTS invoices_tenant_id_idx ON invoices (tenant_id, id);
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS customers_tenant_id_id_uidx ON customers (tenant_id, id);
-- Verifique índices inválidos após falha: SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;
```

```sql
-- 0022 Backfill em lotes (cada execução é uma transação curta; repetir até 0 linhas).
-- customers já tem tenant_id preenchido por regra de negócio (ex.: de accounts) antes deste passo.
UPDATE invoices i
SET tenant_id = c.tenant_id
FROM customers c
WHERE i.customer_id = c.id
  AND i.id IN (SELECT id FROM invoices WHERE tenant_id IS NULL ORDER BY id LIMIT 5000);
```

Orientações do backfill: automatize o laço fora do SQL (script do usuário), com pausa entre lotes, observação de `pg_stat_replication` (`replay_lag`) e de bloqueios, e relatório final de linhas que continuam NULL (órfãs: sem pai ou pai sem tenant). Não preencha por palpite. O backfill acontece antes de ligar RLS (com `FORCE`, a dona deixaria de ver as linhas).

```sql
-- 0023 Escritor antigo ainda ativo: deriva o tenant do pai enquanto a versão antiga existir.
-- Funciona só antes de ligar RLS em customers (sob RLS, a leitura do pai sem contexto devolve zero linhas).
CREATE OR REPLACE FUNCTION invoices_derive_tenant() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.tenant_id IS NULL THEN
    SELECT tenant_id INTO NEW.tenant_id FROM customers WHERE id = NEW.customer_id;
  END IF;
  RETURN NEW;
END $$;
DROP TRIGGER IF EXISTS invoices_derive_tenant ON invoices;
CREATE TRIGGER invoices_derive_tenant BEFORE INSERT ON invoices
  FOR EACH ROW EXECUTE FUNCTION invoices_derive_tenant();
-- Remover o trigger no passo 0032, depois que nenhuma versão antiga da aplicação escreve.
```

## 0030 a 0032 Contract

```sql
-- 0030 NOT NULL sem bloquear a tabela por varredura longa (PostgreSQL 12 ou superior reaproveita a CHECK validada)
ALTER TABLE invoices ADD CONSTRAINT invoices_tenant_id_nn CHECK (tenant_id IS NOT NULL) NOT VALID;
ALTER TABLE invoices VALIDATE CONSTRAINT invoices_tenant_id_nn;
ALTER TABLE invoices ALTER COLUMN tenant_id SET NOT NULL;
ALTER TABLE invoices DROP CONSTRAINT invoices_tenant_id_nn;
```

```sql
-- 0031 FK composta: a referência não cruza tenants (FK ignora RLS e revelaria existência; V-01)
ALTER TABLE customers ADD CONSTRAINT customers_tenant_id_id_key UNIQUE USING INDEX customers_tenant_id_id_uidx;
ALTER TABLE invoices ADD CONSTRAINT invoices_customer_same_tenant_fk
  FOREIGN KEY (tenant_id, customer_id) REFERENCES customers (tenant_id, id) NOT VALID;
ALTER TABLE invoices VALIDATE CONSTRAINT invoices_customer_same_tenant_fk;
-- Depois de validar, a FK simples antiga (customer_id) pode ser removida em passo próprio.
```

```sql
-- 0032 Fim da transição: remover o trigger de derivação
DROP TRIGGER IF EXISTS invoices_derive_tenant ON invoices;
DROP FUNCTION IF EXISTS invoices_derive_tenant();
```

Verificação por passo (o usuário cola o resultado): `SELECT count(*) FROM invoices WHERE tenant_id IS NULL;` deve ser 0; linhas entre tenants: `SELECT count(*) FROM invoices i JOIN customers c ON c.id = i.customer_id WHERE i.tenant_id <> c.tenant_id;` deve ser 0.

## 0040 RLS por tabela

```sql
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices FORCE  ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON invoices
  USING      (tenant_id = NULLIF(current_setting('app.tenant_id', true), '')::uuid)
  WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id', true), '')::uuid);
```

Comportamento sem contexto: `current_setting(..., true)` devolve NULL se o parâmetro nunca foi definido e pode devolver texto vazio depois de um `set_config` local que terminou; `NULLIF(..., '')` converte os dois casos em NULL, a comparação não é verdadeira, a leitura devolve zero linhas e a escrita falha no `WITH CHECK` (V-01). O exemplo da AWS usa `current_setting('app.current_tenant')` sem `missing_ok` e falha com erro quando falta contexto (V-48). Escolha um e escreva o teste que afirma o que a policy produz (V-65). O plugin padroniza `NULLIF` mais uma guarda na aplicação que lança erro se o contexto faltar, para a falha ser audível (conflito C2 da síntese; Inferido).

Variante de desempenho (Inferido; meça com `EXPLAIN (ANALYZE, BUFFERS)` no volume real): `tenant_id = (SELECT NULLIF(current_setting('app.tenant_id', true), '')::uuid)` para avaliar a função uma vez (V-45 recomenda esse padrão para `auth.uid()`).

Policies separadas por comando só quando as regras diferirem (por exemplo leitura mais ampla que escrita); policies restritivas combinam por AND, permissivas por OR (V-01).

## Tabelas de resolução de identidade (login, domínio, convite)

Antes de existir contexto de tenant a aplicação precisa achar a quais tenants o usuário pertence. Opções: manter `users` e `memberships` sem RLS, com privilégio mínimo e acesso só pelo módulo de identidade; ou uma função estreita `SECURITY DEFINER` com as quatro salvaguardas de V-45.

```sql
CREATE SCHEMA IF NOT EXISTS private;

CREATE OR REPLACE FUNCTION private.tenants_of_current_user()
RETURNS TABLE (tenant_id uuid)
LANGUAGE sql STABLE SECURITY DEFINER
SET search_path = ''                       -- salvaguarda 1: search_path vazio
AS $$
  SELECT m.tenant_id
  FROM public.memberships m
  WHERE m.user_id = NULLIF(current_setting('app.user_id', true), '')::uuid   -- salvaguarda 2: identidade no corpo
    AND m.status = 'active'
$$;

REVOKE ALL ON FUNCTION private.tenants_of_current_user() FROM PUBLIC;          -- salvaguarda 3: revogar EXECUTE
GRANT EXECUTE ON FUNCTION private.tenants_of_current_user() TO app_runtime;
-- salvaguarda 4: schema "private" não exposto a APIs nem concedido a roles que não devem usá-lo
```

A dona da função (`app_migrator`) precisa conseguir ler `memberships`: se `memberships` tiver RLS com `FORCE`, a dona também é filtrada. Por isso a tabela de associação costuma ficar sem RLS (classificada como ponte) e protegida por privilégio e por esta função. Registre a decisão no plano.

## Contexto na aplicação (esqueleto, adaptar à stack)

```sql
BEGIN;
SELECT set_config('app.tenant_id', $1, true);   -- $1 vem da identidade validada, nunca do corpo (V-32)
-- ... todas as consultas da requisição, inclusive leituras ...
COMMIT;
```

`set_config(nome, valor, is_local)` com `is_local = true` vale até o fim da transação; `false` vale até o fim da sessão (documentação do PostgreSQL, V-34). `SET` não aceita parâmetro ligado, `set_config` aceita (conhecimento estável; não verificado nesta pesquisa).

## Exemplos de ORM (formas comuns; confirme na versão instalada)

```ts
// Prisma: transação interativa
await prisma.$transaction(async (tx) => {
  await tx.$executeRaw`SELECT set_config('app.tenant_id', ${tenantId}, true)`;
  return tx.invoice.findMany();   // sem filtro manual aqui: a RLS é a segunda barreira, o filtro da aplicação continua
});
```

```py
# SQLAlchemy 2.x: o contexto vale na transação da sessão
with Session(engine) as session, session.begin():
    session.execute(text("SELECT set_config('app.tenant_id', :t, true)"), {"t": tenant_id})
    rows = session.scalars(select(Invoice)).all()
```

O filtro na aplicação continua obrigatório: RLS é segunda barreira (V-01, V-33), não substituto.
