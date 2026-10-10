# Migração gerada por ORM é rascunho (Alembic, Django e demais)

Conferido em 2026-10-10 contra V-30 (docs oficiais do Alembic `autogenerate` e do Django `topics/migrations`, Verificado pelo validador), V-11, V-29 e V-35. Cobertura honesta: só Alembic e Django têm fonte A nesta base. Para Prisma, Drizzle, TypeORM, Entity Framework, Flyway, Liquibase e Atlas há lacuna (L-04): a seção 4 lista **o que revisar**, rotulado Inferido, e manda abrir a doc da versão instalada. Não codifique fluxos específicos dessas ferramentas a partir de memória: a doc do Prisma Migrate mudou de fluxo e o fluxo coletado de comunidade não se confirmou (rejeitado na validação).

Sumário
1. Regra geral e checklist
2. Alembic
3. Django
4. Outras ferramentas (lacuna L-04)
5. Exemplo: migração autogerada com renome e índice

## 1. Regra geral e checklist

Ferramenta compara o modelo com o banco e emite DDL. Ela não conhece volume, tráfego, locks nem versões coexistentes da aplicação. Portanto: **o arquivo gerado é um rascunho que um humano (ou o agente, em modo revisão) lê e corrige antes de qualquer `upgrade`** (V-30).

Checklist de revisão de migração gerada:

- [ ] O SQL real foi lido (modo offline/`sqlmigrate`/`--sql`), não só o código Python/C#/TS da migração.
- [ ] Renomeações: a ferramenta emitiu drop+add (perda de dado)? Se sim, trocar por rename declarado ou por expand/contract.
- [ ] Constraints têm nome explícito (constraint sem nome não é detectada no diff futuro, V-30).
- [ ] Cada DDL tem lock declarado (ver `checklist-postgres.md` ou `mysql-online-ddl.md`).
- [ ] Índices em tabela existente: `CONCURRENTLY` e fora de transação (PostgreSQL).
- [ ] `server_default`/default: constante ou volátil? A ferramenta pode omitir ou emitir default impreciso (V-30).
- [ ] Enums: tipo nativo ou CHAR+CHECK? Alteração de enum é delicada (V-18).
- [ ] NOT NULL em coluna existente sem backfill? Reescrever em etapas.
- [ ] Transação implícita: a ferramenta embrulha a migração em transação? Isso quebra `CONCURRENTLY` e mantém locks de backfill.
- [ ] Reversão: existe `downgrade`/reverse, e ela é honesta sobre perda de dado?
- [ ] Uma mudança por arquivo; migração já aplicada em algum ambiente não é editada (criar corretiva).
- [ ] Auto-DDL do ORM (`synchronize`, `create_all`) desligado em produção (V-29).

## 2. Alembic (V-30)

Fatos verificados na doc de autogenerate:
- "Não pretende ser perfeito": sempre revisar e corrigir.
- Renomeação de tabela ou coluna aparece como add/drop.
- Constraints sem nome não são detectadas; sequências não são implementadas; PK e exclusão só "eventualmente".
- Comparação de tipos ligada por padrão (padrão `True` desde 1.12.0); `server_default` desligado por padrão e impreciso.
- `Enum` sem suporte nativo vira CHAR + CHECK.
- Detecção de CHECK é opcional, por nome, e nunca por expressão.

Práticas:
- Defina `naming_convention` no `MetaData` do modelo para que todas as constraints tenham nome estável.
- Revise o SQL antes: `alembic upgrade <rev_anterior>:<rev> --sql` gera o SQL em modo offline (Inferido: confira o `--help` da versão instalada).
- Índice concorrente no PostgreSQL (confirme na doc da versão instalada, Inferido):

```python
def upgrade():
    with op.get_context().autocommit_block():
        op.create_index(
            "ix_orders_customer_created", "orders", ["customer_id", "created_at"],
            postgresql_concurrently=True,
        )
```

- CHECK `NOT VALID` e `VALIDATE`: se a versão instalada não oferece opção própria, use `op.execute("ALTER TABLE ... NOT VALID")` e `op.execute("ALTER TABLE ... VALIDATE CONSTRAINT ...")` (SQL do `checklist-postgres.md`).
- Renomear coluna só com `op.alter_column(..., new_column_name=...)` quando todas as versões da aplicação puderem conviver; senão expand/contract.
- Backfill em job separado ou em migração `autocommit`, nunca dentro da migração transacional que também faz DDL.

## 3. Django (V-30)

Fatos verificados na doc de migrações:
- `sqlmigrate <app> <migração>` mostra o SQL antes de aplicar.
- `RunPython` deve usar modelos históricos via `apps.get_model()`; o callable reverso é opcional (sem ele, reverter gera exceção).
- PostgreSQL e SQLite têm DDL transacional; MySQL não ("pode exigir desfazer à mão").
- `atomic = False` na migração desliga a transação.
- `squashmigrations` com lançamento em duas versões.

Práticas:
- Índices concorrentes no PostgreSQL: `AddIndexConcurrently` / `RemoveIndexConcurrently` de `django.contrib.postgres.operations`, com `atomic = False` na classe `Migration` (Inferido: conhecimento estável; confirmar na doc da versão).

```python
from django.contrib.postgres.operations import AddIndexConcurrently
from django.db import migrations, models

class Migration(migrations.Migration):
    atomic = False
    dependencies = [("shop", "0041_previous")]
    operations = [
        AddIndexConcurrently(
            model_name="order",
            index=models.Index(fields=["customer", "-created_at"], name="order_cust_created_idx"),
        ),
    ]
```

- Renomear campo: o `makemigrations` pergunta se foi renomeação; mesmo com `RenameField`, a versão antiga da aplicação quebra durante o deploy: use expand/contract quando houver rolling deploy.
- `RunSQL` com `reverse_sql` explícito para `NOT VALID`/`VALIDATE` (confira se a sua versão do Django tem operações próprias em `django.contrib.postgres.operations` antes de usar `RunSQL`; Inferido).
- `RunPython` grande: faça em lotes e fora da transação (`atomic = False`) ou em comando de gerenciamento separado.

## 4. Outras ferramentas (lacuna L-04; rótulo Inferido: abra a doc da versão instalada)

| Ferramenta | O que revisar sempre | Como obter o SQL antes de aplicar (conferir) |
| --- | --- | --- |
| Entity Framework Core | renomeação costuma sair como drop+add; `HasData`/seed; operações que reescrevem tabela; migração dentro de transação | `dotnet ef migrations script` (opção para script idempotente existe: conferir) |
| Liquibase | `changeSet` sem `runInTransaction`/contexto adequados; `rollback` escrito à mão | comando `updateSQL` (conferir) |
| Flyway | migração versionada é imutável depois de aplicada (checksum): corrigir com nova migração; SQL puro é seu: lock e `CONCURRENTLY` por sua conta | arquivos `.sql` já são o SQL; para `CONCURRENTLY`, a ferramenta precisa permitir rodar fora de transação: conferir a opção da versão |
| TypeORM | `migration:generate` a partir do diff: revisar; `synchronize` fora de produção; métodos `down` honestos | arquivos gerados em TS contêm `queryRunner.query("...")` com o SQL |
| Prisma | gerar sem aplicar e ler o SQL; não presumir fluxo de comandos de memória | abrir a doc atual de Prisma Migrate; "gerar SQL e revisar" é o princípio |
| Drizzle, Atlas | idem: princípio "ler o SQL planejado antes de aplicar" | conferir a doc da ferramenta |

Princípio comum que vale mesmo sem fonte: leia o SQL emitido, nomeie constraints, trate renomeação, ensaie em cópia.

## 5. Exemplo: migração autogerada com renome e índice

Cenário (caso de eval E-02): PostgreSQL 14, tabela `users` com 30 milhões de linhas, migração do Alembic autogerada:

```python
def upgrade():
    op.drop_column("users", "fullname")                              # <- era um renome: perde os dados
    op.add_column("users", sa.Column("full_name", sa.String()))
    op.create_index("ix_users_email", "users", ["email"])           # <- build comum, bloqueia escrita, dentro da transação
```

Diagnóstico (item violado -> risco -> alternativa):

| Item | Risco | Alternativa | Rótulo |
| --- | --- | --- | --- |
| `drop_column("fullname")` + `add_column("full_name")` | Apaga o dado existente; `ACCESS EXCLUSIVE`; quebra versão antiga da app | Expand: adicionar `full_name` nulável; backfill em lotes; migrar leitura; contract em migração separada (`expand-contract-e-backfill.md`) | Verificado (V-30 para drop+add; V-20 para o padrão) |
| `create_index` sem `postgresql_concurrently` | Build comum bloqueia escrita (leitura passa) durante a criação (V-11) | Migração separada, `autocommit_block` + `postgresql_concurrently=True`; depois checar `indisvalid` | Verificado (V-11); API do Alembic: Inferido, conferir a versão |
| Transação implícita da migração | `CREATE INDEX CONCURRENTLY` não roda dentro de bloco de transação (V-11) | `autocommit_block` isola o comando | Verificado |

Corrigida, etapa 1 (arquivo A, expand):

```python
def upgrade():
    op.add_column("users", sa.Column("full_name", sa.String(), nullable=True))

def downgrade():
    op.drop_column("users", "full_name")       # seguro: coluna nova ainda sem leitores
```

Etapa 2 (arquivo B, índice, separado do DDL de coluna):

```python
def upgrade():
    with op.get_context().autocommit_block():
        op.create_index("ix_users_email", "users", ["email"], postgresql_concurrently=True)

def downgrade():
    with op.get_context().autocommit_block():
        op.drop_index("ix_users_email", table_name="users", postgresql_concurrently=True)
```

Depois: job de backfill, verificação, troca de leitura, contract. Entregue com "O que falta para concluir": versão exata do Alembic, resultado de `alembic ... --sql`, ensaio em cópia.
