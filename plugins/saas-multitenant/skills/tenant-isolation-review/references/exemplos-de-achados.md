# Exemplos de achados e de relatório

Código dos exemplos é sintético e escrito para esta skill (sem cópia de terceiros). Os rótulos mostram o nível de certeza possível só com leitura. Conferido em 2026-10-10.

## Exemplo 1: IDOR em handler Express com Prisma (caso `autorizacao-tenant` do brain)

Entrada do usuário: "posso subir hoje? não há ambiente para executar".

```ts
// src/routes/invoices.ts
router.get('/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await prisma.invoice.findUnique({ where: { id: req.params.id } });
  if (!invoice) return res.status(404).json({ error: 'not found' });
  return res.json(invoice);
});
```

Contexto assumido: modelo pool; a sessão tem `req.auth.tenantId` (confirmado em `src/middleware/auth.ts`, linha lida); `invoices` tem `tenant_id`; RLS: Não verificado (nenhuma migration lida).

| ID | Severidade | Confiança | arquivo:linha | Pedido que exploraria | Correção mínima | Ref. | Rótulo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | crítico | 9 | src/routes/invoices.ts:3 | `GET /invoices/<id de fatura do tenant B>` com token do tenant A devolve a fatura inteira | Escopar a consulta pelo tenant da sessão e responder 404 se não houver linha | V-11, V-21 | Inferido (leitura; nenhum teste executado) |
| F2 | importante | 6 | migrations/ (não lida) | Se `invoices` não tiver RLS com `FORCE`, nada barra um `WHERE` esquecido em outra rota | Segunda barreira: RLS com `USING` e `WITH CHECK` | V-01 | Não verificado |

Correção mínima para F1:

```ts
const invoice = await prisma.invoice.findFirst({
  where: { id: req.params.id, tenantId: req.auth.tenantId },
});
if (!invoice) return res.status(404).json({ error: 'not found' });
```

Mesmo erro e mesmo corpo para "não existe" e "é de outro tenant": não distinguir. Teste que falta: tenant A pede o ID de B e recebe 404; tenant B pede o próprio e recebe 200 (matriz de dois tenants, linha "Isolamento por ID").

Resposta ao "posso subir hoje?": não, com F1 aberto; F1 se corrige em uma linha e o teste negativo cabe em 10 linhas. Nenhum teste foi executado nesta revisão.

## Exemplo 2: contexto de tenant com `SET` de sessão atrás de PgBouncer (caso `rls-pooler-contexto`)

```js
// db.js
async function withTenant(tenantId, fn) {
  const client = await pool.connect();
  try {
    await client.query(`SET app.tenant_id = '${tenantId}'`);
    return await fn(client);
  } finally {
    client.release();
  }
}
```

| ID | Severidade | Confiança | arquivo:linha | Pedido que exploraria | Correção mínima | Ref. | Rótulo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | crítico | 8 | db.js:4 | `tenantId` concatenado: um valor com aspas altera o SQL (injeção) e, se vier de fonte não validada, define outro tenant | Parâmetro ligado via `set_config` | V-34 | Inferido |
| F2 | crítico | 8 | db.js:4 | `SET` sem `LOCAL` é de sessão: a conexão devolvida ao pool mantém o tenant anterior; em PgBouncer modo transaction, `SET`/`RESET` de sessão são "Never" suportados e a conexão muda entre transações | Contexto por transação | V-34, V-47 | Verificado na documentação; efeito no seu ambiente: Não verificado |
| F3 | importante | 7 | db.js:5 | Leituras fora de transação rodam sem contexto, ou com o de outro cliente | Toda consulta dentro de `BEGIN ... COMMIT` | V-44 (relato) | Inferido |

Correção:

```js
async function withTenant(tenantId, fn) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    await client.query("SELECT set_config('app.tenant_id', $1, true)", [tenantId]);
    const result = await fn(client);
    await client.query('COMMIT');
    return result;
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}
```

Nota de rótulo: o escopo de transação de `set_config(..., true)` e a falha fechada sem contexto têm fonte (OWASP, V-49). A tabela de recursos do PgBouncer não lista `SET LOCAL` (V-47), então "funciona atrás do pooler" fica Não verificável até o teste com pool de tamanho 1 (skill `tenant-isolation-tests`). Se o usuário disser que já aplicou em produção: esta skill não aplica nada; recomende parar, reverter para o estado anterior com o plano da skill `tenant-rls-migration` e testar em homologação.

## Exemplo 3: job que perde o contexto e cache sem tenant

```py
# workers/reports.py
def nightly_report():
    for tenant in Tenant.query.all():
        rows = db.session.execute(text("SELECT * FROM invoices WHERE paid = false")).all()
        cache.set(f"report:{tenant.id}", render(rows), ttl=600)

# api/reports.py
@app.get("/reports/<report_id>")
def get_report(report_id):
    key = f"report:{report_id}"
    cached = cache.get(key)
    return cached or build_report(report_id, g.tenant_id)
```

| ID | Severidade | Confiança | arquivo:linha | Pedido que exploraria | Correção mínima | Ref. | Rótulo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | crítico | 9 | workers/reports.py:4 | A consulta não filtra por tenant: o relatório de cada tenant contém faturas de todos e fica em cache | Uma transação por tenant com contexto definido, ou filtro explícito no repositório | V-34, V-23 | Inferido |
| F2 | crítico | 8 | api/reports.py:4 | A chave usa só `report_id`: qualquer tenant que conheça ou adivinhe o ID recebe o valor em cache | Tenant (e permissão, se o relatório variar) na chave; autorizar antes de ler | V-49 | Inferido |
| F3 | importante | 6 | api/reports.py:5 | `cached or build_report(...)`: o ramo em cache nunca passa pela checagem de dono | Checar o dono antes da leitura do cache | V-11, V-49 | Inferido |

Teste que falta: relatório do tenant A em cache, pedido do tenant B com o mesmo `report_id` devolve 404; job noturno com dois tenants produz saídas disjuntas.

## Exemplo 4: relatório sem achados

Um relatório honesto também é entregável. Formato:

```text
Resumo: nenhum achado confirmado em 6 arquivos lidos; 2 pontos Não verificados (dependem de banco real).
Inspecionado e sem achados: src/routes/projects.ts (origem do tenant: claim validado, linha 12;
  filtro: repositório base, linhas 8 a 30), src/repos/base.ts, src/middleware/tenant.ts, ...
Não verificado: RLS efetivo (nenhuma migration no escopo); role da aplicação (depende de pg_roles).
Testes que faltam: "Isolamento por ID" e "Jobs em lote" não têm teste neste escopo.
```

Evite "parece seguro" sem a lista do que foi lido.

## O que não reportar

- Estilo, nomes, formatação, preferências de arquitetura.
- Rate limiting ou DoS genéricos sem caminho de exploração entre tenants (para noisy neighbor existe revisão própria, V-09).
- Open redirect, validação genérica sem impacto de isolamento (fora do escopo desta skill; encaminhe para o segmento `security-appsec`).
- Achado sem `arquivo:linha` lido: vai para "Não verificado".
