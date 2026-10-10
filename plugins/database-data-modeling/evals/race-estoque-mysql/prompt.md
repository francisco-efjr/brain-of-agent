---
name: race-estoque-mysql
description: "Mede se o plugin desmonta a premissa 'está numa transação então é seguro' em MySQL 8 InnoDB, explica o isolamento efetivo e propõe correção atômica com teste concorrente coordenado, sem extrapolar do PostgreSQL."
tags: [database-data-modeling, transactions-and-isolation, mysql, concurrency]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Explica que a transação não basta porque o SELECT é uma leitura de snapshot sem trava sob REPEATABLE READ, propõe UPDATE condicional com checagem de linhas afetadas ou FOR UPDATE, e um teste com duas sessões coordenadas, sem extrapolar o comportamento do PostgreSQL."
model: sonnet
---
Clientes estão reclamando que compraram o último item e depois recebemos aviso de estoque negativo. O dev responsável diz que o código "está dentro de uma transação, então é seguro". É Node com mysql2, MySQL 8 InnoDB, configuração padrão. O código:

```js
async function reservar(itemId, qty) {
  const conn = await pool.getConnection();
  try {
    await conn.beginTransaction();
    const [[item]] = await conn.query('SELECT stock FROM items WHERE id = ?', [itemId]);
    if (item.stock >= qty) {
      await conn.query('UPDATE items SET stock = stock - ? WHERE id = ?', [qty, itemId]);
      await conn.commit();
      return true;
    }
    await conn.rollback();
    return false;
  } finally {
    conn.release();
  }
}
```

Ele tem razão? Como corrijo e como eu provo que ficou certo?
