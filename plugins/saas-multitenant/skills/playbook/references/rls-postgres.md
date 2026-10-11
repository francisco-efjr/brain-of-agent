# RLS e contexto de tenant no PostgreSQL

Escopo: modelo **pool** (tabelas compartilhadas com `tenant_id`) em PostgreSQL. Serve a revisão de schema e policies, migração para RLS, testes de banco e decisão silo x pool. Itens `V-nn` estão em `fontes.md`. Documentação do PostgreSQL conferida na série 18.x em 2026-10-10; confirme na versão do seu servidor (`SELECT version();`). Nada aqui é executado pelo plugin: scripts SQL são para revisão humana e execução em homologação.

## Sumário

- [1. Modelo mental em 6 linhas](#1-modelo-mental-em-6-linhas)
- [2. SQL base](#2-sql-base)
- [3. Checklist de 10 pontos](#3-checklist-de-10-pontos)
- [4. Contexto por transação e pooler](#4-contexto-por-transação-e-pooler)
- [5. Falhar fechado sem contexto](#5-falhar-fechado-sem-contexto)
- [6. Canais laterais que RLS não cobre](#6-canais-laterais-que-rls-não-cobre)
- [7. Detecção por catálogo](#7-detecção-por-catálogo)
- [8. Desempenho de policy e `security definer`](#8-desempenho-de-policy-e-security-definer)
- [9. Revisar exemplo de RLS de terceiro](#9-revisar-exemplo-de-rls-de-terceiro)
- [10. Testes de banco (com a role da aplicação)](#10-testes-de-banco-com-a-role-da-aplicação)
- [11. Migração para RLS em tabela existente](#11-migração-para-rls-em-tabela-existente)
- [12. Silo, bridge, pool: quando sair do pool](#12-silo-bridge-pool-quando-sair-do-pool)
- [13. Ordem de revisão de banco](#13-ordem-de-revisão-de-banco)

## 1. Modelo mental em 6 linhas

1. RLS ligado sem policy nega tudo (default deny); `USING` filtra linhas existentes, `WITH CHECK` valida linhas gravadas, e sem `WITH CHECK` vale o `USING` (V-01, Verificado).
2. O **dono da tabela** ignora RLS, a menos que haja `FORCE ROW LEVEL SECURITY`; **superusuário e `BYPASSRLS` sempre ignoram**, mesmo com `FORCE` (V-01, V-49).
3. Policies permissivas combinam por OR; restritivas por AND (V-01).
4. Unique, PK e FK checam sem RLS: canal oculto de existência (V-01).
5. `row_security = off` faz a consulta falhar em vez de esconder linhas (V-01).
6. RLS é a **segunda barreira**; a primeira é o filtro e a autorização na aplicação (V-33 AWS: no modelo pool, RLS é necessário; V-63: isolamento mora em mecanismo compartilhado, não em cada função).

## 2. SQL base

Redação própria; corrige o exemplo da AWS (V-48), que não traz `FORCE`, nem `missing_ok`, nem `WITH CHECK` explícito. Substitua `invoices` e os nomes de role. Senhas de role vêm do cofre, nunca deste arquivo.

```sql
-- Roles (revisão humana; homologação primeiro)
-- app_migrator: dona do schema, usada só pela ferramenta de migração.
-- app_runtime : usada pela aplicação; nunca dona de tabela, nunca BYPASSRLS.
CREATE ROLE app_migrator LOGIN NOSUPERUSER NOBYPASSRLS;      -- senha via cofre
CREATE ROLE app_runtime  LOGIN NOSUPERUSER NOBYPASSRLS;      -- senha via cofre

-- Tabela de tenant (criada e alterada por app_migrator, nunca por app_runtime)
CREATE TABLE invoices (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id  uuid NOT NULL,
  number     text NOT NULL,
  UNIQUE (tenant_id, number),            -- unicidade por tenant, não global
  UNIQUE (tenant_id, id)                 -- alvo de FK composta (seção 6)
);
CREATE INDEX invoices_tenant_idx ON invoices (tenant_id);   -- coluna da policy é indexada (V-45)

ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices FORCE  ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON invoices
  USING      (tenant_id = NULLIF(current_setting('app.tenant_id', true), '')::uuid)
  WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id', true), '')::uuid);

GRANT SELECT, INSERT, UPDATE, DELETE ON invoices TO app_runtime;   -- privilégio mínimo (V-45)
```

Por que `NULLIF(..., '')`: `current_setting(nome, true)` devolve NULL se a variável nunca foi definida (V-34, Verificado), mas depois de um `set_config(..., true)` numa transação anterior a mesma conexão pode devolver string vazia em vez de NULL (comportamento de variável customizada, conhecimento estável, **Inferido**: confira na sua versão). A conversão `''::uuid` falharia com erro; o `NULLIF` transforma ambos os casos em NULL, e `tenant_id = NULL` não casa nenhuma linha.

Roles diferentes: o exemplo da AWS (V-48) prefere variável de runtime a um usuário de banco por tenant; adote variável.

## 3. Checklist de 10 pontos

Cada ponto é verificável por leitura de migration ou consulta de catálogo (seção 7).

| # | Verificação | Falha típica |
| --- | --- | --- |
| 1 | Toda tabela com `tenant_id` tem `ENABLE` **e** `FORCE` | só `ENABLE`: o dono da tabela passa por cima |
| 2 | A aplicação conecta com role que não é dona e não tem `BYPASSRLS` nem superusuário; migração usa outra role | uma única role "postgres" para tudo |
| 3 | Toda policy de escrita tem `WITH CHECK` explícito; `FOR` declarado quando o comando importa | `INSERT` aceita linha de outro tenant |
| 4 | O contexto é definido por `set_config('app.tenant_id', $1, true)` dentro de `BEGIN`, inclusive para leituras | `SET` de sessão; ORM abre transação só na escrita |
| 5 | Sem contexto, a consulta falha fechada (zero linhas ou erro), e o teste afirma qual dos dois | teste que só cobre o caminho feliz |
| 6 | Atributos da role da aplicação conferidos em `pg_roles`, não só no código (V-49) | role migra de "app" para superusuário em um ambiente |
| 7 | Testes rodam com a role da aplicação e dois tenants sintéticos de nomes parecidos | teste com superusuário passa por engano |
| 8 | Backfill de `tenant_id` e `NOT NULL` antes de ativar RLS em tabela existente | linhas com `tenant_id` NULL ficam invisíveis ou inalcançáveis |
| 9 | Views sobre tabelas com RLS usam `security_invoker = true` (PostgreSQL 15 ou superior); views materializadas não aplicam RLS | view de dono contorna a policy (conhecimento estável, **Inferido**; conferir a doc da versão) |
| 10 | Funções `security definer` só com as quatro salvaguardas (seção 8) | função que roda como dono devolve linhas de qualquer tenant |

## 4. Contexto por transação e pooler

```sql
BEGIN;
SELECT set_config('app.tenant_id', $1, true);   -- $1 vem da identidade validada (V-32), nunca do corpo
-- consultas da requisição, inclusive leituras
COMMIT;
```

Fatos (V-34, V-47, V-49):

- `set_config(nome, valor, is_local)`: `true` vale até o fim da transação; `false` até o fim da sessão. `set_config` aceita parâmetro ligado; `SET` não aceita (conhecimento estável, **Não verificado** nesta pesquisa).
- O OWASP Multi-Tenant Cheat Sheet manda usar `SET LOCAL` ou `set_config(..., true)` refeito a cada transação, avisa que configuração de sessão pode vazar para a próxima requisição num pool e manda falhar fechado se faltar (V-49, Verificado).
- PgBouncer em modo transaction: a conexão só é atribuída durante a transação.

| Recurso | PgBouncer, modo transaction (V-47, Verificado em 2026-10-10) |
| --- | --- |
| `SET` / `RESET` de sessão | Never |
| `LISTEN`, `WITH HOLD CURSOR`, `PREPARE`/`DEALLOCATE` (SQL), `LOAD` | Never |
| Advisory locks de sessão, temp tables `PRESERVE`/`DELETE ROWS` | Never |
| `NOTIFY`, `WITHOUT HOLD CURSOR`, temp tables `ON COMMIT DROP` | Yes |
| Prepared plans de protocolo | Yes, com `max_prepared_statements` diferente de zero |
| `SET LOCAL` / `set_config(..., true)` | **não listado na página: Não verificável sem teste** |

Consequência: o desenho é seguro por construção (contexto morre no `COMMIT`), mas a compatibilidade com **o seu** pooler e driver se prova com teste de pool de tamanho 1 (seção 10). Relatos de praticantes sugerem `DISCARD ALL` ao devolver a conexão (V-44, sinal classe B: não é documentação).

Regras de uso:

1. ORM que abre transação só para escrita deixa leituras sem contexto: embrulhe todo acesso num helper `withTenant` (exemplo em `autorizacao-e-tenant-context.md`).
2. Job em lote abre **uma transação por tenant**; contexto global em job é erro de revisão.
3. Worker de webhook de billing resolve `tenant_id` pelo `customer` e define o contexto na mesma transação que grava o resultado.
4. `COMMIT` ocorre **antes** de a resposta sair; commit em `res.on("finish")` deixa a resposta ir com dado não persistido (V-57, classe C, só como checklist).

## 5. Falhar fechado sem contexto

Dois desenhos legítimos, ambos fecham (conflito C2 de `decisoes-e-tradeoffs.md`):

| Desenho | Efeito sem contexto | Fonte |
| --- | --- | --- |
| `current_setting('app.tenant_id')` sem `missing_ok` | **erro** na consulta | exemplo da AWS (V-48) |
| `NULLIF(current_setting('app.tenant_id', true), '')::uuid` | **zero linhas**; escrita rejeitada pelo `WITH CHECK` | V-01 |

Padrão do plugin: usar o segundo na policy **e** uma guarda na aplicação (`withTenant` lança se o tenant for vazio ou não for UUID), para a falha ser audível em vez de silenciosa. O teste afirma o resultado que a policy produz; "nunca linhas" é o invariante (V-65).

## 6. Canais laterais que RLS não cobre

- **Unique, PK e FK** ignoram RLS: um `UNIQUE (email)` global revela, por erro de duplicata, que o e-mail existe em outro tenant. Use `UNIQUE (tenant_id, email)`.
- **FK entre tenants**: `FOREIGN KEY (parent_id)` simples permite apontar para linha de outro tenant. Use FK composta `(tenant_id, parent_id) REFERENCES parent (tenant_id, id)` (por isso o `UNIQUE (tenant_id, id)` na seção 2). Padrão de design estável, **Inferido**.
- **Subconsultas em policy** podem gerar corrida e vazamento (V-01): prefira policy que compare só a coluna da própria linha.
- **Agregados e estatísticas**: mensagens de erro e planos de execução não devem ecoar valores de outros tenants; logs de SQL sem parâmetros.
- **Role `service`/bypass**: a service role de plataformas ignora RLS por completo; usar num endpoint público "por desempenho" foi o quase-incidente de V-58 (classe C, sinal). Restrinja a jobs, documente a role e audite o uso.
- **Particionamento**: confirme em teste que o acesso direto à partição respeita a policy esperada (**Não verificado** nesta pesquisa).

## 7. Detecção por catálogo

Consultas somente leitura, executáveis em homologação com a role da aplicação ou de auditoria. Resultado esperado: zero linhas nas duas primeiras.

```sql
-- Tabelas com tenant_id sem ENABLE+FORCE
SELECT c.relname, c.relrowsecurity AS enable_rls, c.relforcerowsecurity AS force_rls
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN pg_attribute a ON a.attrelid = c.oid AND a.attname = 'tenant_id' AND NOT a.attisdropped
WHERE c.relkind IN ('r','p') AND n.nspname = 'public'
  AND NOT (c.relrowsecurity AND c.relforcerowsecurity);

-- Policies de escrita sem WITH CHECK
SELECT tablename, policyname, cmd
FROM pg_policies
WHERE schemaname = 'public' AND cmd IN ('ALL','INSERT','UPDATE') AND with_check IS NULL;

-- Atributos da role que a aplicação usa (esperado: rolsuper=false, rolbypassrls=false)
SELECT rolname, rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user;

-- Dono das tabelas (esperado: app_migrator, nunca app_runtime)
SELECT c.relname, pg_get_userbyid(c.relowner) AS owner
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind = 'r';
```

Em `pg_policies`, `with_check IS NULL` com `USING` presente é aceitável tecnicamente (vale o `USING`), mas o checklist do plugin exige `WITH CHECK` explícito para a intenção ficar legível (V-01). Nomes de catálogo (`relrowsecurity`, `relforcerowsecurity`, `pg_policies`) são conhecimento estável, **Inferido**; confira na versão.

## 8. Desempenho de policy e `security definer`

V-45 (regras `security-*` do `supabase/agent-skills`, MIT, Verificado nos arquivos lidos):

- Envolver a chamada de função em `(select ...)` para ela rodar uma vez por consulta, não uma vez por linha. Adaptação ao nosso contexto: `tenant_id = (SELECT NULLIF(current_setting('app.tenant_id', true), '')::uuid)`; ganho a medir com `EXPLAIN (ANALYZE, BUFFERS)` (**Inferido**; o arquivo lido usa `(select auth.uid())`).
- **Indexar toda coluna usada na policy.** Índice composto começando por `tenant_id` é adequado; a ordem exata depende das consultas (Suposição a confirmar com `EXPLAIN`).
- Função `security definer`: schema não exposto, `search_path` vazio (ou fixado), checagem de identidade no corpo e `EXECUTE` revogado de roles que não devem chamá-la. As quatro salvaguardas juntas; sem elas, a função vira uma porta de bypass.
- Privilégios: menor privilégio, nada de superusuário na aplicação; revogar acesso público ao schema (testar antes: pode quebrar apps que dependem dele).
- Pool: o modo transaction é recomendado para a maioria dos apps; modo session para prepared statements e tabelas temporárias (V-45 `conn-pooling`). Cuidado: o título "multi-tenant" da skill do Supabase não é sustentado pelo corpo, que isola por `user_id`.

## 9. Revisar exemplo de RLS de terceiro

Aplique a qualquer trecho de blog, skill ou gerado por IA antes de aproveitar uma ideia. Origem: V-57 e V-58 (classe C como fonte; úteis só como lista de defeitos, nunca como regra ou código).

1. `COMMIT` acontece **antes** de a resposta sair?
2. Leitura por ID (`findUnique`) passa pelo mesmo filtro que a listagem? Middleware de ORM que pula `findUnique` é defeito conhecido.
3. A role de bypass existe, está documentada e restrita a jobs? (`SET LOCAL role = 'admin_bypass'` sem criar a role não funciona.)
4. O `tenant_id` vindo do claim do JWT tem vínculo conferido com o usuário (membership), ou é só texto do token?
5. Toda policy de escrita tem `WITH CHECK`? Policy `USING` sem `FOR` e `WITH CHECK` só no `INSERT` deixa `UPDATE` trocar o `tenant_id`.
6. A role da aplicação é sem `BYPASSRLS` e sem superusuário? Superusuário e `BYPASSRLS` ignoram RLS mesmo com `FORCE`.
7. UUID aleatório não é controle de acesso: o fato de ID não ser sequencial não substitui a checagem de dono (correção de V-57).

## 10. Testes de banco (com a role da aplicação)

Dois tenants sintéticos de nomes parecidos (por exemplo "Acme Ltda" e "Acme Ltd"). Execute conectado como `app_runtime` (nunca superusuário). Cada bloco é uma transação separada, porque um erro aborta a transação.

```sql
-- T1: tenant A insere e vê só o que é seu
BEGIN; SELECT set_config('app.tenant_id', '<UUID-A>', true);
INSERT INTO invoices (tenant_id, number) VALUES ('<UUID-A>', 'A-001');
SELECT count(*) FROM invoices;                 -- esperado: 1
COMMIT;

-- T2: tenant B não vê nada de A (conjunto vazio, não erro)
BEGIN; SELECT set_config('app.tenant_id', '<UUID-B>', true);
SELECT count(*) FROM invoices;                 -- esperado: 0
COMMIT;

-- T3: insert cruzado é rejeitado
BEGIN; SELECT set_config('app.tenant_id', '<UUID-B>', true);
INSERT INTO invoices (tenant_id, number) VALUES ('<UUID-A>', 'X-999');
-- esperado: ERROR  new row violates row-level security policy
ROLLBACK;

-- T4: update não consegue trocar o tenant da linha
BEGIN; SELECT set_config('app.tenant_id', '<UUID-A>', true);
UPDATE invoices SET tenant_id = '<UUID-B>' WHERE number = 'A-001';
-- esperado: ERROR  (WITH CHECK)
ROLLBACK;

-- T5: sem contexto (nova transação, mesma conexão): falha fechada
BEGIN; SELECT count(*) FROM invoices;          -- esperado: 0 (ou erro, conforme a policy escolhida)
COMMIT;
```

No nível da aplicação, repita com **pool de tamanho 1**: requisição do tenant A, depois do tenant B, depois uma terceira sem contexto, todas na mesma conexão. Prova mínima de que o contexto não vaza entre requisições (V-34, V-65). Teste de mutação: remover a policy (ou o filtro da aplicação) em homologação e confirmar que o teste falha ("vermelho confirmado", PAD-07). Registre a saída colada; sem execução, o rótulo é Não verificado.

## 11. Migração para RLS em tabela existente

Expand/contract; a skill `tenant-rls-migration` só escreve scripts e plano, a execução é humana em homologação (brain `migracao-rollback`: janela de indisponibilidade máxima e escritor antigo ainda ativo exigem expand/contract).

1. **Inventário**: classifique cada tabela em tenant, global ou ponte; liste FKs entre tenants e uniques globais a corrigir.
2. **Expand**: `ADD COLUMN tenant_id uuid` nullable + índice (`CREATE INDEX CONCURRENTLY` em tabela grande, fora de transação); backfill em lotes com estimativa de duração e plano de reversão; versão antiga da aplicação ainda pode inserir NULL.
3. **Roles**: separar migração e runtime; conferir `pg_roles` (seção 7).
4. **Aplicação primeiro**: o código passa a abrir transação com `set_config(..., true)` e a gravar `tenant_id` **antes** de ligar RLS.
5. **Contract**: `NOT NULL` só quando nenhum escritor antigo grava NULL (ex.: `ADD CONSTRAINT ... CHECK (tenant_id IS NOT NULL) NOT VALID` seguido de `VALIDATE CONSTRAINT`, depois `SET NOT NULL`; padrão estável, **Inferido**).
6. **Ligar**: `ENABLE` + `FORCE` + policies, uma tabela por vez, com teste da seção 10 em cada passo.
7. **Reversão**: `DISABLE ROW LEVEL SECURITY` está no plano, e o plano diz quem decide acioná-lo.
8. **Muitos tenants**: execução por tenant com falha isolada e reexecutável; versão de schema registrada por tenant (V-23).
9. **Proibido**: `sync({alter:true})`, `force:true` ou DDL manual em ambiente implantado (anti-padrões rejeitados em V).

## 12. Silo, bridge, pool: quando sair do pool

Resumo; decisão completa em `decisoes-e-tradeoffs.md` (D1) e no template `adr-modelo-tenancy.md`.

| Modelo | Vantagens | Desvantagens | Fonte |
| --- | --- | --- | --- |
| Pool (tabelas compartilhadas + RLS) | agilidade, custo, densidade | impacto entre tenants, compliance mais difícil, disponibilidade tudo-ou-nada | V-33 (AWS) |
| Silo (banco/instância por tenant) | alinhamento a compliance, sem impacto entre tenants, ajuste por tenant | custo, implantação complexa, automação obrigatória | V-33 (AWS, Azure) |
| Bridge (híbrido) | pool para planos comuns, silo para exigências | duas operações para manter | V-33 |

Regras de ADR: pool com RLS para planos comuns; silo para chave própria, residência de dados ou isolamento físico contratado; **nunca** tabela ou coluna por tenant; migração de schema automatizada com versão por tenant e aplicação compatível com a versão anterior (V-33). Schema por tenant tem prós (apagar por tenant para GDPR, backup e restore, índices menores) e contras (código de migração, extensões, limite de locks, memória) apenas em relatos de praticantes (V-44, classe B/C): rotule "relato de praticante".

## 13. Ordem de revisão de banco

Roles e privilégios → RLS com `FORCE` e `WITH CHECK` → contexto por transação e pooler → desempenho da policy (índice, `(select ...)`) → funções `security definer` → consultas e índices → schema (uniques, FKs) → locks e migração (V-24, V-45). Saída de revisão: tabela `ID · severidade · arquivo:linha · cenário · correção · rótulo`, com `pg_roles` marcado Não verificado quando não houver banco.

Gotchas resumidos: teste com superusuário ou dono passa por engano; `FORCE` não vale para `BYPASSRLS`; `SET` de sessão atrás de pooler; ORM sem transação em leitura; unique global como canal de existência; view de dono contornando a policy.
