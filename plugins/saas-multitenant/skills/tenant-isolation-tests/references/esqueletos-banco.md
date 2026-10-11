# Esqueletos de teste de banco: role, RLS, falha fechada e pool de tamanho 1

Esqueletos escritos para esta skill (Python com pytest e psycopg 3; variante Node com `pg`). Confirme as APIs na versão instalada (PAD-13). Nada foi executado nesta pesquisa. Base: V-01, V-34, V-47, V-49, V-58, V-65. Conferido em 2026-10-10.

Variáveis de ambiente: `APP_RUNTIME_DSN` (role da aplicação, a mesma que a produção usaria) e `SEED_DSN` (role autorizada a criar a fixture, apenas em homologação). Nunca coloque DSN com senha em arquivo versionado.

## 1. Python (pytest + psycopg 3)

```py
# tests/isolation/test_rls.py
import os
import psycopg
import pytest

A = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
B = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"


@pytest.fixture(scope="session")
def conn():
    # Uma única conexão reutilizada por todos os testes = pool de tamanho 1:
    # o contexto de uma transação não pode vazar para a seguinte.
    with psycopg.connect(os.environ["APP_RUNTIME_DSN"], autocommit=True) as c:
        yield c


def test_guard_role_nao_e_privilegiada(conn):
    row = conn.execute(
        "SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user"
    ).fetchone()
    assert row == (False, False), f"a role de teste contorna a RLS: {row}"
    owned = conn.execute(
        "SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace "
        "WHERE n.nspname = 'public' AND c.relkind = 'r' AND pg_get_userbyid(c.relowner) = current_user"
    ).fetchone()[0]
    assert owned == 0, "a role de teste é dona de tabelas; sob FORCE ela seria filtrada, sem FORCE ignoraria a RLS"


def test_todas_as_tabelas_de_tenant_tem_rls_forcada(conn):
    rows = conn.execute(
        "SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace "
        "JOIN pg_attribute a ON a.attrelid = c.oid AND a.attname = 'tenant_id' AND NOT a.attisdropped "
        "WHERE n.nspname = 'public' AND c.relkind IN ('r','p') "
        "AND NOT (c.relrowsecurity AND c.relforcerowsecurity)"
    ).fetchall()
    assert rows == [], f"tabelas com tenant_id sem ENABLE e FORCE: {rows}"


def test_b_nao_ve_dados_de_a_e_ve_os_proprios(conn):
    with conn.transaction():
        conn.execute("SELECT set_config('app.tenant_id', %s, true)", (B,))
        ids = [r[0] for r in conn.execute("SELECT id::text FROM invoices").fetchall()]
    assert ids, "controle positivo: o tenant B deveria ver as próprias faturas"
    assert not any(i.startswith("a1") for i in ids), "tenant B leu fatura do tenant A"


def test_insert_cruzado_e_rejeitado(conn):
    with pytest.raises(psycopg.errors.InsufficientPrivilege):
        with conn.transaction():
            conn.execute("SELECT set_config('app.tenant_id', %s, true)", (A,))
            conn.execute(
                "INSERT INTO invoices (id, tenant_id, customer_id, number) "
                "VALUES (gen_random_uuid(), %s, %s, 'X')",
                (B, "b0000000-0000-4000-8000-000000000001"),
            )


def test_update_nao_move_linha_para_outro_tenant(conn):
    with pytest.raises(psycopg.errors.InsufficientPrivilege):
        with conn.transaction():
            conn.execute("SELECT set_config('app.tenant_id', %s, true)", (A,))
            conn.execute("UPDATE invoices SET tenant_id = %s WHERE number = 'INV-001'", (B,))


def test_sem_contexto_falha_fechado_depois_de_servir_a_e_b(conn):
    # Mesma conexão que acabou de servir A e B: o contexto não pode ter ficado para trás.
    try:
        with conn.transaction():
            rows = conn.execute("SELECT id FROM invoices").fetchall()
    except psycopg.Error:
        return   # policy de "erro explícito" (current_setting sem missing_ok): aceitável, documente
    assert rows == [], "sem contexto, linhas apareceram (falha aberta)"
```

Notas:
- Os testes usam o bloco `with conn.transaction()` explícito, que fecha a transação mesmo com exceção.
- `psycopg.errors.InsufficientPrivilege` corresponde ao SQLSTATE 42501, o mesmo da violação de policy de RLS; confirme na documentação do psycopg da sua versão.
- Se a policy do projeto produz erro explícito sem contexto, converta o último teste em `pytest.raises(psycopg.Error)` e remova o ramo permissivo, para o teste afirmar um resultado só (V-65).
- Os prefixos de ID (`a1...`, `b1...`) vêm da fixture: ajuste para a regra de pertencimento da sua fixture.

## 2. Node (`pg`; Vitest ou Jest)

```ts
import { Client } from 'pg';

const A = 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa';
const B = 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb';
let c: Client;

beforeAll(async () => { c = new Client({ connectionString: process.env.APP_RUNTIME_DSN }); await c.connect(); });
afterAll(async () => { await c.end(); });

async function inTenant<T>(tenant: string | null, fn: () => Promise<T>): Promise<T> {
  await c.query('BEGIN');
  try {
    if (tenant) await c.query("SELECT set_config('app.tenant_id', $1, true)", [tenant]);
    const out = await fn();
    await c.query('COMMIT');
    return out;
  } catch (e) { await c.query('ROLLBACK'); throw e; }
}

it('guarda: a role de teste não contorna a RLS', async () => {
  const r = await c.query('SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user');
  expect(r.rows[0]).toEqual({ rolsuper: false, rolbypassrls: false });
});

it('B vê o que é dele e nada de A (mesma conexão)', async () => {
  const rowsB = await inTenant(B, async () => (await c.query('SELECT id::text FROM invoices')).rows);
  expect(rowsB.length).toBeGreaterThan(0);
  expect(rowsB.some((r) => r.id.startsWith('a1'))).toBe(false);
});

it('insert cruzado é rejeitado (42501)', async () => {
  await expect(inTenant(A, () => c.query(
    "INSERT INTO invoices (id, tenant_id, customer_id, number) VALUES (gen_random_uuid(), $1, $2, 'X')",
    [B, 'b0000000-0000-4000-8000-000000000001']))).rejects.toMatchObject({ code: '42501' });
});

it('sem contexto, na mesma conexão que serviu A e B: zero linhas ou erro', async () => {
  let rows: unknown[] = [];
  try { rows = await inTenant(null, async () => (await c.query('SELECT id FROM invoices')).rows); }
  catch { return; }
  expect(rows).toEqual([]);
});
```

## 3. Pooler real

Tudo acima, apontando `APP_RUNTIME_DSN` para o PgBouncer em modo `transaction` com `default_pool_size = 1`. Compare o resultado com o da conexão direta; diferença é achado. Sem o teste, "funciona atrás do pooler" é Não verificável (V-47: a página não lista `SET LOCAL`). Registre as versões do PgBouncer, do driver e do PostgreSQL com o resultado.

## 4. Teste de migração por tenant (linha "Migrações")

```py
def test_migracao_em_lote_com_falha_isolada(run_migration, tenants_1000):
    result = run_migration(fail_on=tenants_1000[500])
    assert result.failed == [tenants_1000[500]]
    assert result.applied == len(tenants_1000) - 1
    assert all(t.schema_version in ("antes", "depois") for t in result.tenants)      # sem estado misto
    again = run_migration()                                                          # reexecutável
    assert again.failed == []
```

`run_migration` é o runner do projeto. Se o produto não usa banco por tenant, a linha vira "Não aplicável" com a justificativa.
