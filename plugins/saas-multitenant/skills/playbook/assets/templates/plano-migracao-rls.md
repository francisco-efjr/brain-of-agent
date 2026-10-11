# Plano de migração para RLS por tenant

Escopo autorizado: **escrever scripts e plano**. A execução é humana, em homologação primeiro; nada de DDL em produção feito pelo agente. Fontes: `V-01`, `V-34`, `V-45`, `V-47`, `V-48`, `V-49`; detalhes em `references/rls-postgres.md`.

Banco: [PostgreSQL versão] · Pooler: [PgBouncer modo transaction | nenhum | outro] · ORM/driver: [..] · Tabelas no escopo: [..] · Janela máxima de indisponibilidade: [..] · Escritor antigo ainda ativo? [sim/não]

## 1. Inventário

| Tabela | Classe (tenant / global / ponte) | Linhas | `tenant_id` hoje | FKs entre tenants | Uniques globais a corrigir | Observação |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## 2. Roles

| Role | Papel | Atributos esperados | Verificação (`pg_roles`) |
| --- | --- | --- | --- |
| `app_migrator` | dona do schema; só a ferramenta de migração | NOSUPERUSER, NOBYPASSRLS | |
| `app_runtime` | aplicação | NOSUPERUSER, NOBYPASSRLS; não dona de tabela; privilégios mínimos | |

Senhas e segredos: cofre. Não registre aqui.

## 3. Passos (expand/contract)

| # | Passo | Script | Validação | Reversão | Dono |
| --- | --- | --- | --- | --- | --- |
| 1 | Adicionar `tenant_id` nullable + índice (`CONCURRENTLY` em tabela grande) | | `\d tabela` | `DROP INDEX`, `DROP COLUMN` | |
| 2 | Aplicação passa a gravar `tenant_id` e a abrir transação com `set_config(..., true)` (leituras incluídas) | | teste de pool de tamanho 1 | reverter deploy | |
| 3 | Backfill em lotes (tamanho: [..]; estimativa: [..]) | | `COUNT(*) WHERE tenant_id IS NULL = 0` | n/a (idempotente) | |
| 4 | `NOT NULL` (ex.: `CHECK ... NOT VALID` + `VALIDATE`, depois `SET NOT NULL`) só quando nenhum escritor antigo grava NULL | | inserção de teste | `DROP CONSTRAINT` | |
| 5 | Constraints por tenant: `UNIQUE (tenant_id, x)`, FK composta | | tentativa de duplicata e de FK cruzada | recriar constraint antiga | |
| 6 | `ENABLE` + `FORCE` + policy com `USING` e `WITH CHECK`, uma tabela por vez | | testes T1 a T5 de `rls-postgres.md` § 10 com a role da aplicação | `DISABLE ROW LEVEL SECURITY` (quem decide: [..]) | |
| 7 | Views com `security_invoker = true` (PG 15+) | | consulta pela view com dois tenants | recriar | |

## 4. Testes (com a role da aplicação)

| Teste | Esperado | Resultado (saída colada) | Rótulo |
| --- | --- | --- | --- |
| Tenant A insere e vê só o seu | 1 linha | | |
| Tenant B não vê nada de A | conjunto vazio | | |
| Insert cruzado | erro de policy | | |
| Update trocando `tenant_id` | erro de policy | | |
| Sem contexto | zero linhas ou erro, conforme a policy: [qual] | | |
| Pool de tamanho 1: A, B, sem contexto | cada um vê só o seu | | |
| Mutação: remover policy/filtro em homologação | teste falha (vermelho confirmado) | | |

## 5. Muitos tenants

Execução por tenant com falha isolada e reexecutável; versão de schema por tenant registrada (V-23). Plano de repetição: [..].

## 6. Riscos e janela

| Risco | Mitigação | Gatilho de reversão |
| --- | --- | --- |
| Linhas com `tenant_id` NULL invisíveis após RLS | `NOT NULL` antes de ligar | contagem > 0 |
| Leitura sem contexto no ORM | helper `withTenant` para todo acesso | testes falham |
| Role de aplicação com `BYPASSRLS` em algum ambiente | checar `pg_roles` por ambiente | atributo divergente |
| Locks em tabela grande | `CONCURRENTLY`, lotes pequenos | latência acima de [..] |

Proibido: `sync({alter:true})`, `force:true` ou DDL manual em ambiente implantado.

## 7. Aprovação

[ ] Plano revisado por `tenant-isolation-reviewer` · [ ] Executado em homologação por [nome] em [data] · [ ] Humano autoriza produção em [data]
