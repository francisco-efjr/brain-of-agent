---
name: sqli-order-by
description: "Mede se o plugin encontra injeção SQL em valor e em identificador (ORDER BY) num endpoint Express com pg, propõe parametrização e allow-list e não se contenta com escape ou regex."
tags: [database-data-modeling, db-schema-and-sql, security, sql-injection]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta injeção no valor category e nos identificadores sort e dir, parametriza o valor com $1, usa allow-list de colunas e direção para ORDER BY, recomenda privilégio mínimo e erros sem SQL, e não sugere apenas escapar."
model: sonnet
---
Esse endpoint de listagem de produtos é só pra paginar e ordenar, mas funciona? É Express com `pg` (node-postgres) e Postgres 16.

```js
app.get('/products', async (req, res) => {
  const { cat, sort, dir } = req.query;
  const sql = `SELECT id, name, price FROM products WHERE category = '${cat}' ORDER BY ${sort} ${dir} LIMIT 20`;
  try {
    const { rows } = await pool.query(sql);
    res.json(rows);
  } catch (e) {
    res.status(500).json({ error: e.message, sql });
  }
});
```

A conexão do `pool` usa o usuário `postgres` (o mesmo da instalação).
