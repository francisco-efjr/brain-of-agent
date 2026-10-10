# RLS no PostgreSQL: SQL de referência e testes de dois tenants

Conferido em 2026-10-10 contra V-12 (`ddl-rowsecurity`, PostgreSQL 18.6, Verificado: RLS sem política nega tudo; `USING` filtra e `WITH CHECK` valida escrita, `USING` sozinho vale como `WITH CHECK`; permissivas por OR, restritivas por AND; superusuário e `BYPASSRLS` ignoram sempre; dono ignora salvo `FORCE`; unicidade e FK ignoram RLS; `row_security=off` gera erro quando a consulta seria filtrada; subconsulta em política pode ter condição de corrida em READ COMMITTED; `TRUNCATE` e `REFERENCES` não são cobertos) e Art. G reescrito em `VALIDATED.md`. O checklist de apoio do repositório troykelly/claude-skills (MIT, Classe C) serviu só como ideia; o texto abaixo é redação própria. Sintaxe e nomes de parâmetros além do que V-12 verificou são conhecimento estável (Inferido): conferir na doc da versão. **Tudo é SQL para o usuário rodar em banco de teste**, nunca em produção.

Sumário
1. Papéis
2. Tabela, RLS e políticas
3. Contexto do tenant por transação
4. Views, funções e materialized views
5. Índices e desempenho
6. Testes de dois tenants
7. Diagnóstico (consultas de leitura)
8. Ligar RLS em tabela existente

## 1. Papéis

```sql
-- Dono do schema/tabelas e migrador: NÃO é o papel da aplicação.
-- Papel da aplicação: sem superusuário e sem BYPASSRLS (senha definida fora deste arquivo).
CREATE ROLE app_rw LOGIN NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE;
GRANT CONNECT ON DATABASE app TO app_rw;
GRANT USAGE ON SCHEMA public TO app_rw;
GRANT SELECT, INSERT, UPDATE, DELETE ON invoices TO app_rw;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_rw;
-- não conceder TRUNCATE nem REFERENCES (não são cobertos por RLS, V-12)
```

Checagem de leitura: `SELECT rolname, rolsuper, rolbypassrls FROM pg_roles WHERE rolname = 'app_rw';` deve mostrar `f` e `f`.

## 2. Tabela, RLS e políticas

```sql
CREATE TABLE invoices (
  id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id  BIGINT NOT NULL,
  number     TEXT   NOT NULL,
  total      NUMERIC(12,2) NOT NULL,
  CONSTRAINT invoices_tenant_number_key UNIQUE (tenant_id, number)   -- unicidade por tenant (não global)
);

ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices FORCE ROW LEVEL SECURITY;      -- o dono também obedece (V-12); necessário se o dono consulta pela app

-- função auxiliar: lê o tenant do contexto; vazio/ausente -> NULL -> nenhuma linha casa (falha fechada)
CREATE FUNCTION app_tenant_id() RETURNS bigint
LANGUAGE sql STABLE
AS $$ SELECT NULLIF(current_setting('app.tenant_id', true), '')::bigint $$;

CREATE POLICY tenant_isolation ON invoices
  AS PERMISSIVE FOR ALL TO app_rw
  USING      (tenant_id = (SELECT app_tenant_id()))
  WITH CHECK (tenant_id = (SELECT app_tenant_id()));
```

Notas:
- Sem política com RLS ligado, todo acesso de papéis sujeitos a RLS é negado (V-12); por isso cada tabela com dado de tenant precisa da sua política.
- `(SELECT app_tenant_id())` embrulhado em subselect permite ao planner avaliar a função uma vez por consulta, em vez de por linha (técnica comum, Inferido: confirme no plano).
- `WITH CHECK` explícito torna a intenção legível, embora `USING` sozinho já valha como `WITH CHECK` (V-12).
- Política restritiva (`AS RESTRICTIVE`) combina por AND com as permissivas (V-12); use para regras extras, como "linha não arquivada".
- Política sem subconsulta em outras tabelas, quando possível. Se precisar consultar outra tabela, a condição de corrida em READ COMMITTED exige mitigação (`FOR SHARE`, função `SECURITY DEFINER` documentada ou lock) (V-12).

## 3. Contexto do tenant por transação

Regra: definir o tenant **dentro de cada transação**, com `set_config(..., true)` (3º argumento `true` = local à transação). Equivale a `SET LOCAL`, mas aceita parâmetro; `SET LOCAL app.tenant_id = $1` não funciona porque `SET` não aceita parâmetros (V-12, Art. G).

```sql
BEGIN;
SELECT set_config('app.tenant_id', '42', true);   -- no código: parâmetro $1
-- consultas da requisição ...
COMMIT;                                            -- ao final, o valor deixa de valer
```

Por que não `SET` de sessão: com PgBouncer em modo transação, a mesma conexão física serve clientes diferentes; um `SET app.tenant_id` de sessão pode vazar para outro cliente (Inferido; V-18/V-35 tratam o mesmo risco para outros `SET`). Padrão no código (Node, exemplo):

```js
const client = await pool.connect();
try {
  await client.query('BEGIN');
  await client.query("SELECT set_config('app.tenant_id', $1, true)", [String(tenantId)]);   // tenantId validado como inteiro
  const r = await client.query('SELECT id, number, total FROM invoices ORDER BY id LIMIT 50');
  await client.query('COMMIT');
  return r.rows;
} catch (e) { await client.query('ROLLBACK'); throw e; } finally { client.release(); }
```

O tenant vem da identidade autenticada no servidor (token/sessão), nunca de parâmetro livre da requisição.

## 4. Views, funções e materialized views

```sql
-- view que respeita as políticas de quem consulta (PostgreSQL 15+)
CREATE VIEW invoices_open WITH (security_invoker = true) AS
  SELECT id, tenant_id, number, total FROM invoices WHERE total > 0;
```
Sem `security_invoker`, a view roda com os privilégios do dono e pode atravessar RLS (Inferido; conferir na doc da versão). Em PostgreSQL < 15 evite views sobre tabelas com RLS ou use funções cuidadosas.

```sql
-- SECURITY DEFINER: search_path fixo e sem receber o id do tenant como parâmetro livre
CREATE FUNCTION invoice_total(p_invoice_id bigint) RETURNS numeric
LANGUAGE sql STABLE SECURITY DEFINER
SET search_path = pg_catalog, public
AS $$
  SELECT total FROM public.invoices
  WHERE id = p_invoice_id AND tenant_id = public.app_tenant_id()   -- usa o contexto da transação, não um parâmetro livre
$$;
REVOKE ALL ON FUNCTION invoice_total(bigint) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION invoice_total(bigint) TO app_rw;
```
- Materialized views **não** têm RLS: o conteúdo é o do momento do refresh, com os privilégios de quem o executou. Não exponha materialized view agregada de todos os tenants ao papel da aplicação; mantenha uma por tenant ou filtre por uma view com `tenant_id` e controle de acesso (Inferido).
- Exportações, relatórios e jobs que usam papel privilegiado ficam fora do RLS: liste-os e revise a quem entregam.

## 5. Índices e desempenho

- Índices começando por `tenant_id` nas consultas filtradas por tenant: `CREATE INDEX CONCURRENTLY invoices_tenant_created_idx ON invoices (tenant_id, created_at DESC);` (ver `safe-migrations` para criar em tabela existente).
- Colunas usadas na política precisam de índice (Art. G).
- Confira no `EXPLAIN` que a condição da política aparece como `Filter`/`Index Cond` e que não há `Seq Scan` por falta de índice.

## 6. Testes de dois tenants

Conecte **como `app_rw`** (preferível) ou use `SET LOCAL ROLE app_rw` a partir de um papel privilegiado (neste caso confirme que a política está sendo aplicada; Inferido). Dados de teste: tenants 1 e 2, ao menos duas faturas cada, inseridos por papel dono em banco de teste.

```sql
-- T1: leitura isolada
BEGIN; SELECT set_config('app.tenant_id', '1', true);
SELECT count(*) FROM invoices;                              -- esperado: só as do tenant 1
SELECT count(*) FROM invoices WHERE tenant_id = 2;          -- esperado: 0 (acesso cruzado)
ROLLBACK;

-- T2: escrita no próprio tenant
BEGIN; SELECT set_config('app.tenant_id', '1', true);
INSERT INTO invoices (tenant_id, number, total) VALUES (1, 'T1-900', 10);   -- esperado: ok
ROLLBACK;

-- T3: escrita cruzada (INSERT com outro tenant)
BEGIN; SELECT set_config('app.tenant_id', '1', true);
INSERT INTO invoices (tenant_id, number, total) VALUES (2, 'X-1', 10);
-- esperado: ERRO "new row violates row-level security policy"
ROLLBACK;

-- T4: UPDATE tentando mover linha para outro tenant
BEGIN; SELECT set_config('app.tenant_id', '1', true);
UPDATE invoices SET tenant_id = 2 WHERE tenant_id = 1;
-- esperado: ERRO (WITH CHECK)
ROLLBACK;

-- T5: sem contexto definido
BEGIN;
SELECT count(*) FROM invoices;                              -- esperado: 0 (falha fechada, com NULLIF/missing_ok)
ROLLBACK;

-- T6: contexto não vaza entre transações na mesma conexão
BEGIN; SELECT set_config('app.tenant_id', '1', true); COMMIT;
BEGIN; SELECT count(*) FROM invoices; ROLLBACK;             -- esperado: 0 (valor local expirou)

-- T7: vazamento por unicidade (tabela hipotética `users`, se existir UNIQUE global)
BEGIN; SELECT set_config('app.tenant_id', '1', true);
INSERT INTO users (tenant_id, email) VALUES (1, 'alice@exemplo.com');
-- se UNIQUE(email) global e o e-mail existe no tenant 2: ERRO de unicidade revela a existência. Esperado: sem erro com UNIQUE (tenant_id, email)
ROLLBACK;
```

Registre por linha: esperado, obtido (do usuário), rótulo. Sem saída do usuário, "teste proposto, não executado".

## 7. Diagnóstico (consultas de leitura)

```sql
SELECT rolname, rolsuper, rolbypassrls FROM pg_roles WHERE rolname IN ('app_rw', current_user);
SELECT c.relname, c.relrowsecurity AS rls, c.relforcerowsecurity AS forced
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind = 'r' ORDER BY c.relname;      -- tabelas sem RLS ligado
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check FROM pg_policies;
SELECT tablename FROM pg_tables t WHERE schemaname = 'public'
  AND NOT EXISTS (SELECT 1 FROM pg_policies p WHERE p.schemaname = t.schemaname AND p.tablename = t.tablename);   -- sem política
```

Cruze com a lista de tabelas que têm `tenant_id` (`information_schema.columns WHERE column_name = 'tenant_id'`).

## 8. Ligar RLS em tabela existente

1. Adicionar `tenant_id` (se faltar) e preencher em lotes (ver `safe-migrations`).
2. Criar índices começando por `tenant_id` com `CONCURRENTLY`.
3. Criar o papel da aplicação sem `BYPASSRLS` e migrar a conexão para ele **antes** de ligar RLS.
4. Criar políticas e só então `ENABLE ROW LEVEL SECURITY` (RLS ligado sem política nega tudo, V-12: janela de indisponibilidade).
5. Rodar os testes da seção 6 com o papel real em ambiente de teste; só depois em produção, por decisão do usuário.
6. Plano de reversão: `ALTER TABLE ... DISABLE ROW LEVEL SECURITY` (cuidado: reabre acesso total aos papéis com privilégio) e política anterior preservada.
