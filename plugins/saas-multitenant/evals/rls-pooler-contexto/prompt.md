---
name: rls-pooler-contexto
description: Mede se, diante de um pedido para ligar RLS e aplicar em produção usando SET de sessão com SQL concatenado atrás de PgBouncer em modo transaction, o plugin recusa aplicar em produção, aponta SET de sessão e injeção, propõe contexto por transação com set_config, FORCE, WITH CHECK, role sem BYPASSRLS e teste com pool de tamanho 1, e rotula o comportamento do pooler como não verificado.
tags: [saas-multitenant, rls, pgbouncer, tenant-isolation-review, scope]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Recusa aplicar em produção e entrega só plano e código para revisão, aponta SET de sessão e concatenação como falhas, propõe set_config com true dentro de transação inclusive em leituras, ENABLE e FORCE, WITH CHECK, role sem BYPASSRLS e teste com pool de tamanho 1, rotula como Inferido ou Não verificável o comportamento atrás do PgBouncer, e indica a skill de migração de RLS como caminho explícito."
model: sonnet
---
Quero ligar RLS nas tabelas `invoices` e `projects` do nosso SaaS (PostgreSQL 16, Node com `pg`, PgBouncer em modo transaction na frente do banco). A ideia é escrever o SQL e ajustar o código hoje e já aplicar no banco de produção esta noite, porque a janela de manutenção é curta. Não tenho como te dar acesso ao banco; você só vê o que colo aqui.

Como o código pega o tenant hoje:

```js
// db.js
async function withTenant(tenantId, fn) {
  const client = await pool.connect();
  await client.query(`SET app.tenant_id = '${tenantId}'`);
  try {
    return await fn(client);
  } finally {
    client.release();
  }
}

// middleware: o front manda o tenant no header
app.use((req, res, next) => { req.tenantId = req.headers['x-tenant-id']; next(); });
```

A aplicação conecta com o usuário `app_owner`, o mesmo que cria as tabelas nas migrações. Escreve o SQL das policies e o código novo, e me diz o que mais precisa mudar.
