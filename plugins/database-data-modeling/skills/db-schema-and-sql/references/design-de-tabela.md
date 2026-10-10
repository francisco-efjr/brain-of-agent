# Design de tabela: checklist, DDL de exemplo e equivalências por engine

Conferido em 2026-10-10 contra V-32 (convenções), V-23, V-24, V-12 e o brain `dados-e-migracoes.md`. Regras de normalização e escolha de chave não têm fonte A nesta base (L-01): tudo marcado Inferido é convenção a justificar, não norma. SQL conceitual: adaptar e testar na engine do projeto.

Sumário
1. Checklist (PostgreSQL)
2. DDL de exemplo (pedidos)
3. Equivalências por engine
4. Decisões frequentes e critério
5. Perguntas que mudam o desenho

## 1. Checklist (PostgreSQL)

Marque cada item com Verificado (visto no schema recebido), Inferido ou Suposição.

- [ ] Cada tabela tem PK. Padrão: `BIGINT GENERATED ALWAYS AS IDENTITY`; UUID só com motivo escrito (geração fora do banco, não enumerável, merge entre bancos). `serial` é legado em guias, mas ainda funciona: citar como preferência, não erro (Inferido).
- [ ] Chave natural que o negócio garante única tem `UNIQUE` (além da PK surrogate).
- [ ] `NOT NULL` onde o dado é obrigatório; `DEFAULT` só para valor comum e estável. Default volátil (`now()` é estável dentro da transação; `random()`, `clock_timestamp()` são voláteis) tem custo em tabela existente: ver `safe-migrations`.
- [ ] Instantes em `timestamptz`. `timestamp` sem fuso só para "data/hora de parede" sem ponto no tempo (ex.: horário de abertura da loja), com a razão registrada.
- [ ] Dinheiro em `NUMERIC(p,s)` ou inteiro de centavos mais coluna de moeda. Nunca `float`/`double precision`. Arredondamento é regra de negócio: registre onde acontece.
- [ ] FK declarada, com ação (`ON DELETE RESTRICT` padrão; `CASCADE` só quando o filho não tem vida própria; `SET NULL` quando a relação é opcional) e **índice no lado filho** (PostgreSQL não cria; V-32).
- [ ] `CHECK` para regra por linha (`total >= 0`, `status IN (...)`, `fim > inicio`). Intervalos que não podem sobrepor: `EXCLUDE USING gist` com `btree_gist` (Inferido; conferir doc de exclusion constraints).
- [ ] Enum de domínio: `CHECK (col IN (...))` ou tabela de domínio com FK; tipo `ENUM` nativo só se valores raramente mudam (renomear/remover valor é DDL delicado, V-18).
- [ ] `JSONB` apenas para atributos opcionais/variáveis que não são filtrados em todo acesso; campo consultado sempre deve virar coluna (V-32).
- [ ] Constraints e índices com nome explícito (`orders_total_nonneg`, `orders_customer_id_created_at_idx`).
- [ ] Índices derivados das consultas reais (ficha de acesso), com custo de escrita listado. `NULLS NOT DISTINCT` só em PostgreSQL 15+ (V-32). Covering com `INCLUDE`.
- [ ] Dados pessoais: coluna só com finalidade; sensíveis marcadas; retenção definida (ver `operacao-e-seguranca-de-dados.md`).
- [ ] Multi-tenant: `tenant_id NOT NULL` em tabela com dado de tenant; índices compostos começando por ele; PK/UNIQUE avaliadas com o tenant incluído (Inferido). Seguir com `rls-tenant-review`.

## 2. DDL de exemplo (pedidos)

Exemplo didático em PostgreSQL 15+. Os nomes e tipos não vêm de fonte; a estrutura segue o checklist.

```sql
CREATE TABLE customers (
  id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email       TEXT        NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT customers_email_len  CHECK (char_length(email) BETWEEN 3 AND 320)
);
-- unicidade sem diferenciar caixa: índice de expressão (a consulta deve usar lower(email))
CREATE UNIQUE INDEX customers_email_lower_key ON customers (lower(email));

CREATE TABLE orders (
  id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id  BIGINT        NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
  status       TEXT          NOT NULL DEFAULT 'pending',
  total        NUMERIC(12,2) NOT NULL,
  created_at   TIMESTAMPTZ   NOT NULL DEFAULT now(),
  CONSTRAINT orders_status_check  CHECK (status IN ('pending','paid','shipped','cancelled')),
  CONSTRAINT orders_total_nonneg  CHECK (total >= 0)
);
-- Q1: pedidos do cliente, mais recentes primeiro (igualdade antes da ordenação)
CREATE INDEX orders_customer_id_created_at_idx ON orders (customer_id, created_at DESC);

CREATE TABLE order_items (
  order_id    BIGINT        NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  line_no     INT           NOT NULL,
  sku         TEXT          NOT NULL,
  qty         INT           NOT NULL,
  unit_price  NUMERIC(12,2) NOT NULL,
  PRIMARY KEY (order_id, line_no),            -- a PK já indexa order_id (coluna à esquerda)
  CONSTRAINT order_items_qty_pos   CHECK (qty > 0),
  CONSTRAINT order_items_price_nonneg CHECK (unit_price >= 0)
);
```

Pontos que o exemplo demonstra e o revisor deve checar em qualquer schema: FK com índice (aqui coberta pela PK composta), constraint de domínio nomeada, unicidade case-insensitive pelo mesmo `lower()` da consulta, dinheiro em `NUMERIC`, ausência de índice supérfluo.

## 3. Equivalências por engine

Fonte: V-23 (índice funcional), V-24 (SQLite), V-16/V-09 (MySQL), restante é conhecimento estável do domínio, marcado Inferido. Conferir a doc da versão instalada.

| Necessidade | PostgreSQL | MySQL (InnoDB) | SQL Server | SQLite |
| --- | --- | --- | --- | --- |
| PK autoincremento | `GENERATED ... AS IDENTITY` | `AUTO_INCREMENT` | `IDENTITY(1,1)` | `INTEGER PRIMARY KEY` (rowid) |
| Instante com fuso | `timestamptz` | `TIMESTAMP` (UTC na sessão) ou `DATETIME` + convenção UTC | `datetimeoffset` | texto ISO-8601 em UTC ou inteiro epoch (convenção) |
| Dinheiro | `NUMERIC(p,s)` | `DECIMAL(p,s)` | `DECIMAL(p,s)` | inteiro de centavos (sem tipo decimal exato nativo, Inferido) |
| Índice sobre expressão | índice de expressão (`lower(email)`) | coluna gerada indexada ou collation case-insensitive (V-23) | coluna computada indexada ou collation (V-23) | índice de expressão suportado (Inferido; conferir) |
| Constraint CHECK | sim | aplicada a partir do MySQL 8.0.16 (Inferido; versões antigas ignoravam) | sim | sim |
| Covering index | `INCLUDE` | índice composto cobre colunas no fim (sem `INCLUDE`) | `INCLUDE` | índice composto (covering por colunas) (V-24) |
| DDL transacional | sim (V-30) | não (V-30) | sim, com ressalvas (Inferido) | sim (V-30) |

## 4. Decisões frequentes e critério

| Decisão | Critério para escolher | Quando mudar de ideia |
| --- | --- | --- |
| Surrogate (`BIGINT`) vs chave natural como PK | Surrogate se a chave natural pode mudar ou é composta e larga; mantenha UNIQUE na natural | Tabela de associação pura: PK composta é suficiente |
| UUID vs `BIGINT` | UUID se o id nasce em clientes/serviços distintos ou não pode ser enumerado | Escrita muito intensa com UUID aleatório fragmenta o índice B-tree: medir, ou usar variante ordenada por tempo (Inferido; conferir suporte do driver/engine) |
| 3FN vs desnormalizar | 3FN até medir um gargalo no `EXPLAIN` de uma consulta crítica | Leitura dominante com junção cara e medida: coluna derivada com regra de atualização documentada |
| Soft delete (`deleted_at`) | Só se há requisito de histórico/restauração | Prefira tabela de histórico/auditoria; soft delete exige filtro em toda consulta e índice parcial (`WHERE deleted_at IS NULL`) |
| `JSONB` vs colunas | Colunas para o que se filtra/une/restringe | Atributos de cardinalidade aberta e rara consulta |

## 5. Perguntas que mudam o desenho (faça uma por vez, só se a resposta alterar a solução)

1. Qual a maior tabela daqui a 12 meses (linhas) e qual a taxa de escrita?
2. Há outro escritor além da aplicação (scripts, outro serviço, ETL)? Se sim, constraints no banco são obrigatórias.
3. Existe requisito de retenção, exclusão sob pedido do titular ou auditoria?
4. A engine/versão é fixa ou há migração planejada?
