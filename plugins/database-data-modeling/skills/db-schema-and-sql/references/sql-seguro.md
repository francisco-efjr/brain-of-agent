# SQL seguro: parametrização, allow-list, privilégios e erros

Conferido em 2026-10-10 contra V-29 (OWASP SQL Injection Prevention Cheat Sheet, CC BY-SA 4.0; texto aqui é destilação com redação própria; regras de dados do awesome-copilot e do .mdc NestJS reescritas em tom calmo), V-12 e V-15. Exemplos de código são ilustrativos: adaptar à versão do driver.

Sumário
1. Princípio e ordem de defesa
2. Parametrização por driver
3. Identificadores e ORDER BY por allow-list
4. Privilégios do papel da aplicação
5. Erros, logs e segredos
6. Saída de LLM, NoSQL e ORM
7. Revisão: padrões que denunciam o problema

## 1. Princípio e ordem de defesa

1. **Consulta parametrizada** é a defesa primária: o SQL é um texto fixo e os valores viajam separados (V-29).
2. **Allow-list** para o que não pode ser parâmetro: nome de tabela, de coluna e direção do `ORDER BY` (V-29).
3. **Privilégio mínimo**: a aplicação nunca usa papel DBA/dono do schema (V-29). Dano de uma injeção é limitado pelo papel.
4. **Validação de entrada** (tipo, tamanho, formato) é defesa secundária; escape manual é desencorajado (V-29).
5. Procedimento armazenado só protege se não monta SQL dinâmico dentro (V-29).

## 2. Parametrização por driver

Errado (concatenação, injetável em valor e em identificador):

```js
db.query(`SELECT * FROM products WHERE category='${req.query.cat}' ORDER BY ${req.query.sort} ${req.query.dir}`)
```

Correto por driver (placeholder varia: confirme na doc do driver instalado):

```js
// Node, node-postgres: $1, $2
const SORTS = { price: 'price', name: 'name', created: 'created_at' };   // allow-list
const DIRS  = { asc: 'ASC', desc: 'DESC' };
const sort = SORTS[req.query.sort] ?? 'created_at';
const dir  = DIRS[String(req.query.dir).toLowerCase()] ?? 'DESC';
const sql  = `SELECT id, name, price FROM products WHERE category = $1 ORDER BY ${sort} ${dir}, id LIMIT $2`;
await pool.query(sql, [req.query.cat, 50]);
```

```python
# Python, psycopg 3: %s (não é formatação de string; o driver envia parâmetros separados)
cur.execute("SELECT id, name FROM products WHERE category = %s AND price <= %s", (cat, max_price))
# Identificador dinâmico: use psycopg.sql, nunca f-string
from psycopg import sql
cur.execute(sql.SQL("SELECT id FROM {} WHERE id = %s").format(sql.Identifier(table_from_allowlist)), (pid,))
```

```python
# SQLAlchemy Core: parâmetros nomeados
conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email})
```

```java
// JDBC: ?
try (PreparedStatement ps = conn.prepareStatement("SELECT id FROM users WHERE email = ?")) {
  ps.setString(1, email);
}
```

Observações:
- `LIKE` com entrada do usuário: o padrão `%` e `_` ainda vale; parametrize a string inteira (`'%' || $1 || '%'` no SQL, ou concatene no código e passe como parâmetro) e escape curingas se não forem desejados (Inferido).
- `IN (...)` com lista variável: gere N placeholders ou use `= ANY($1)` com array (PostgreSQL). Nunca interpole os valores.
- `LIMIT/OFFSET` também são parâmetros; imponha teto no código (`Math.min(limit, 100)`).
- O desempate (`, id`) no `ORDER BY` torna a ordem determinística para paginação (ver `query-plan-and-indexing`).

## 3. Identificadores e ORDER BY por allow-list

- Mapa fixo "chave pública -> identificador real" (como `SORTS` acima); valor ausente cai no padrão, não em erro com texto da entrada.
- Direção só `ASC`/`DESC` via mapa.
- Tabela dinâmica (multi-tenant por schema, por exemplo): lista fixa de schemas válidos obtida do cadastro, não da requisição; use o quoting nativo do driver (`sql.Identifier`, `quote_ident`) além da lista.
- Nunca confie em "validação por regex" para identificadores como única barreira: a lista fixa é a barreira.

## 4. Privilégios do papel da aplicação

Objetivo: se o SQL for injetado, o dano é limitado. Exemplo conceitual para PostgreSQL (adaptar; conferir a doc de `GRANT` da versão):

```sql
-- migrador (DDL) e aplicação (DML) são papéis diferentes
CREATE ROLE app_rw LOGIN NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE;   -- senha definida fora deste arquivo
GRANT CONNECT ON DATABASE app TO app_rw;
GRANT USAGE ON SCHEMA public TO app_rw;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_rw;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_rw;
-- sem CREATE no schema, sem TRUNCATE, sem REFERENCES, sem EXECUTE em funções administrativas
```

Checagens de revisão:
- A string de conexão da aplicação usa `app_rw` e não o dono/`postgres`/`root`/`sa`?
- Papel de análise/relatório é somente `SELECT`, em réplica quando possível?
- Colunas sensíveis expostas a papéis de leitura precisam de view ou grant por coluna (conceder `SELECT` na tabela inteira ainda expõe dados pessoais; Inferido).
- Auto-DDL do ORM (`synchronize: true`, `create_all()`) desligado em produção, e migração sem `DROP`/`TRUNCATE` sem revisão (V-29, regra do .mdc NestJS reescrita).

## 5. Erros, logs e segredos

- Não devolver texto de erro SQL nem stack trace ao cliente; registrar internamente com id de correlação (V-29).
- Logs sem valores de parâmetros sensíveis (senha, token, documento); minimizar e definir retenção (brain `dados-e-migracoes.md`).
- Segredos (string de conexão, chaves) em variável de ambiente ou gerenciador de segredos, fora do repositório e do cliente; não imprimir `.env`; credencial distinta por ambiente (V-29, V-35). Configuração que falha cedo se faltar valor, em vez de cair em padrão inseguro (V-29).
- Senhas de usuários da aplicação: hash com algoritmo adequado na camada de aplicação (fora do escopo deste plugin: segmento security-appsec). Senhas de papéis do PostgreSQL: SCRAM preferido, MD5 obsoleto (V-15).
- Conexão ao banco por TLS (`hostssl` no `pg_hba.conf`; cliente exigindo TLS) em redes não confiáveis (V-15).

## 6. Saída de LLM, NoSQL e ORM

- Texto gerado por LLM (inclusive SQL gerado pelo próprio agente) é entrada não confiável: passa por parâmetros e allow-list como qualquer entrada (V-29, regra do awesome-copilot).
- Em MongoDB, objetos vindos do cliente podem carregar operadores (`{"$ne": null}`): force tipos escalares antes de montar o filtro (V-29).
- ORMs também aceitam SQL cru (`raw`, `text`, `$queryRawUnsafe`, `execute(sqlString)`): qualquer uso com interpolação é a mesma falha; prefira a API parametrizada ou `bindparams`.
- Filtros dinâmicos de ORM com campo vindo da requisição (`filter(**request.GET)`, `where: req.query`) permitem consultar campos não previstos: mapeie campos permitidos.

## 7. Revisão: padrões que denunciam o problema

Use `Grep` no repositório (leitura apenas). Cada achado exige o caminho completo da entrada até a consulta para ser reportado com confiança alta; sem o caminho, marque Suposição.

| Padrão (regex indicativa) | O que investigar |
| --- | --- |
| `` `[^`]*(SELECT|INSERT|UPDATE|DELETE)[^`]*\$\{`` | Template string JS com interpolação em SQL |
| `f"(SELECT|INSERT|UPDATE|DELETE)[^"]*\{` | f-string Python em SQL |
| `execute\(.*\+.*\)` / `format\(` perto de SQL | Concatenação ou `.format` |
| `queryRawUnsafe`, `\$queryRawUnsafe`, `raw\(`, `RawSQL`, `text\(f` | SQL cru de ORM com valor dinâmico |
| `ORDER BY` seguido de variável | Direção/coluna sem allow-list |
| `synchronize: true`, `create_all(` | Auto-DDL ativo; confirmar ambiente |
| string de conexão com `postgres://postgres:` ou `root@` | Papel privilegiado na aplicação |

Falso negativo é esperado (SQL montado em helper distante): regex não prova ausência (mesma lógica de V-02 sobre regex em hooks). Por isso o parecer final lista "Fora do alcance da leitura": o que só teste com o papel real confirma.
