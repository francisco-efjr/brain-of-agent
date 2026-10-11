# Testes de RLS, plano de execução e reversão

Redação própria. Base: V-01, V-34, V-47, V-48, V-49, V-58, V-65, V-23. Conferido em 2026-10-10. Nada foi executado nesta pesquisa; os scripts são esqueletos para homologação com dados sintéticos.

## 1. Testes em SQL (psql, role da aplicação)

Conecte como `app_runtime` (nunca superusuário nem dona; V-01). Uma única conexão `psql` e transações sequenciais simulam pool de tamanho 1: o contexto de uma transação não pode vazar para a próxima.

```sql
\set a '''aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'''
\set b '''bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'''

-- Fixture: tenants com nomes parecidos (Acme Ltda / Acme Ltd), criados pela role de seed autorizada
-- ou pelo próprio runtime dentro do contexto de cada tenant (WITH CHECK permite).
BEGIN;
SELECT set_config('app.tenant_id', :a, true);
INSERT INTO customers (id, tenant_id, name) VALUES ('a0000000-0000-0000-0000-000000000001', :a, 'Acme Ltda');
INSERT INTO invoices  (id, tenant_id, customer_id, number)
VALUES ('a1000000-0000-0000-0000-000000000001', :a, 'a0000000-0000-0000-0000-000000000001', 'INV-001');
COMMIT;

BEGIN;
SELECT set_config('app.tenant_id', :b, true);
INSERT INTO customers (id, tenant_id, name) VALUES ('b0000000-0000-0000-0000-000000000001', :b, 'Acme Ltd');
INSERT INTO invoices  (id, tenant_id, customer_id, number)
VALUES ('b1000000-0000-0000-0000-000000000001', :b, 'b0000000-0000-0000-0000-000000000001', 'INV-001');
COMMIT;

-- T1: leitura bloqueada afirma conjunto vazio (V-58)
BEGIN;
SELECT set_config('app.tenant_id', :b, true);
DO $$ BEGIN
  ASSERT (SELECT count(*) FROM invoices WHERE id = 'a1000000-0000-0000-0000-000000000001') = 0,
         'T1 falhou: tenant B leu fatura do tenant A';
  ASSERT (SELECT count(*) FROM invoices) = 1, 'T1 falhou: tenant B deveria ver exatamente 1 fatura';
END $$;
COMMIT;

-- T2: escrita cruzada é rejeitada (SQLSTATE 42501, insufficient_privilege)
BEGIN;
SELECT set_config('app.tenant_id', :a, true);
DO $$ BEGIN
  INSERT INTO invoices (id, tenant_id, customer_id, number)
  VALUES (gen_random_uuid(), 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'b0000000-0000-0000-0000-000000000001', 'X');
  RAISE EXCEPTION 'T2 falhou: insert cruzado foi aceito';
EXCEPTION WHEN insufficient_privilege THEN
  NULL;  -- esperado
END $$;
COMMIT;

-- T3: UPDATE que tenta mover linha para outro tenant é rejeitado
BEGIN;
SELECT set_config('app.tenant_id', :a, true);
DO $$ BEGIN
  UPDATE invoices SET tenant_id = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb' WHERE id = 'a1000000-0000-0000-0000-000000000001';
  RAISE EXCEPTION 'T3 falhou: update cruzado foi aceito';
EXCEPTION WHEN insufficient_privilege THEN
  NULL;
END $$;
COMMIT;

-- T4: sem contexto falha fechado, na mesma sessão que acabou de servir A e B (pool de tamanho 1)
BEGIN;
DO $$ BEGIN
  ASSERT (SELECT count(*) FROM invoices) = 0, 'T4 falhou: sem contexto, linhas apareceram';
END $$;
COMMIT;
-- Se a policy for do tipo "erro explícito" (current_setting sem missing_ok), o SELECT acima falha com erro:
-- aceite apenas esse resultado e registre qual dos dois a policy produz (V-65).

-- T5: FK não cruza tenants (se a FK composta foi criada)
BEGIN;
SELECT set_config('app.tenant_id', :a, true);
DO $$ BEGIN
  INSERT INTO invoices (id, tenant_id, customer_id, number)
  VALUES (gen_random_uuid(), 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'b0000000-0000-0000-0000-000000000001', 'Y');
  RAISE EXCEPTION 'T5 falhou: FK cruzou tenants';
EXCEPTION WHEN foreign_key_violation OR insufficient_privilege THEN
  NULL;  -- a FK composta recusa (23503); a RLS pode recusar antes dependendo da ordem
END $$;
COMMIT;
```

Observação do `ASSERT`: depende de `plpgsql.check_asserts` ligado (padrão). Se o ambiente desligar, use `IF ... THEN RAISE EXCEPTION`.

## 2. Teste com o pooler real

A tabela de recursos do PgBouncer lista `SET`/`RESET` como "Never" em modo transaction e não menciona `SET LOCAL` (V-47). Logo, "funciona atrás do pooler" é Não verificável até o teste. Roteiro para homologação:

1. Configure o PgBouncer com `pool_mode = transaction` e `default_pool_size = 1` (nomes de parâmetros conforme a documentação da sua versão: https://www.pgbouncer.org/config.html).
2. Aponte o teste de aplicação (ou o `psql`) para o PgBouncer, não direto para o PostgreSQL.
3. Execute em sequência a partir de dois clientes: requisição do tenant A; requisição do tenant B; requisição sem contexto. Cada uma deve ver só o que lhe cabe; a terceira, zero linhas ou erro.
4. Repita sob concorrência leve (dois clientes alternando) para provocar a reutilização da mesma conexão de servidor.
5. Registre o resultado como Verificado, com a versão do PgBouncer e do PostgreSQL.

## 3. Vermelho confirmado

Em homologação: `ALTER TABLE invoices DISABLE ROW LEVEL SECURITY;` (ou `DROP POLICY tenant_isolation ON invoices;`), rode T1 a T4: T1 e T4 devem falhar. Religue e veja tudo verde. Um teste que passa com a RLS desligada não prova nada (PAD-07).

Teste negativo adicional por role: conecte como a dona e como a role de manutenção e veja que elas, de fato, divergem do runtime (a dona sob `FORCE` é filtrada; `BYPASSRLS` não). Isso documenta quem pode contornar e por quê.

## 4. Plano de execução (modelo)

| Passo | Ambiente | Quem executa | Verificação | Reversão |
| --- | --- | --- | --- | --- |
| 0010 roles | homologação, depois produção | administrador | consultas 2, 3, 4 do catálogo | `DROP ROLE` só se nada depender; reverter owner das tabelas |
| 0020 a 0021 expand | homologação, depois produção | migrator | coluna e índices válidos (`indisvalid`) | `DROP INDEX`, `DROP COLUMN` (coluna é nullable e sem uso) |
| 0022 backfill | homologação, depois produção, em janela de baixa carga | script do usuário | zero NULL; zero linha entre tenants | reexecutável; pode voltar a NULL se necessário |
| Deploy da aplicação com contexto por transação | homologação, depois produção | time | testes de aplicação; nenhum acesso sem `set_config` | rollback do deploy |
| 0030 a 0032 contract | homologação, depois produção | migrator | zero NULL; FKs válidas | `DROP CONSTRAINT`, `ALTER COLUMN DROP NOT NULL` |
| 0040 RLS, tabela por tabela | homologação, depois produção | migrator | testes T1 a T5; pooler real | ver abaixo |

Ponto de não retorno: o ponto em que a aplicação depende do `tenant_id` NOT NULL e das FKs compostas. Antes dele, tudo reverte sem perda; depois, reverter exige rollback da aplicação também. Registre-o no plano.

## 5. Reversão da RLS (por tabela)

```sql
DROP POLICY IF EXISTS tenant_isolation ON invoices;
ALTER TABLE invoices NO FORCE ROW LEVEL SECURITY;
ALTER TABLE invoices DISABLE ROW LEVEL SECURITY;
```

Efeito: o isolamento volta a depender só do filtro da aplicação. Mantém `tenant_id` e índices (o expand é compatível com a versão anterior). Registre a reversão como incidente de segurança de baixa gravidade e agende a correção.

## 6. Muitos tenants ou muitos deployments (silo)

Quando a migração roda por banco ou por tenant: registrar o resultado em tabela de controle (`schema_version`, `status`, `started_at`, `finished_at`, `error`); executar em lotes de tenants; falha isola o tenant e não bloqueia os demais; reexecução é segura (comandos idempotentes); nenhum tenant fica em estado misto (migração parcial é revertida ou concluída antes de liberar tráfego); aplicação aceita a versão anterior do schema durante a janela (V-33, V-23). Teste com 1.000 tenants sintéticos, um falhando no meio.

## 7. Evidências a anexar no plano

Saída das consultas de catálogo antes e depois; contagens de NULL e de linhas entre tenants; saída dos testes T1 a T5 com a role da aplicação; resultado do roteiro do pooler com versões; saída do vermelho confirmado. Sem essas saídas, o status é "SQL escrito; não verificado".
