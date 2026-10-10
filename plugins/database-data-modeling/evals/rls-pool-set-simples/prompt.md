---
name: rls-pool-set-simples
description: "Mede se o plugin audita RLS do PostgreSQL 16 e encontra dono da tabela sem FORCE, SET de sessão vazando em PgBouncer em modo transaction e SET que não aceita parâmetro, recomendando set_config por transação e teste de dois tenants."
tags: [database-data-modeling, rls-tenant-review, postgresql, multi-tenant]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta que o dono da tabela ignora RLS sem FORCE, que SET de sessão vaza em pool de modo transaction, que SET não aceita parâmetro, recomenda set_config(..., true) por transação, role sem BYPASSRLS, WITH CHECK e teste com dois tenants, sem declarar o sistema seguro por leitura."
model: sonnet
---
Somos um SaaS multi-tenant (Postgres 16). Ativei RLS na tabela `invoices` e queria saber se está seguro antes de ir para produção. O que temos:

```sql
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON invoices
  USING (tenant_id = current_setting('app.tenant_id')::int);
```

- A aplicação conecta com o usuário `app_owner`, que é o mesmo que criou as tabelas (dono).
- Usamos PgBouncer em `pool_mode = transaction`.
- Em cada requisição, o middleware Node faz isto assim que pega a conexão do pool:

```js
await client.query('SET app.tenant_id = $1', [tenantId]);
```

Está seguro?
