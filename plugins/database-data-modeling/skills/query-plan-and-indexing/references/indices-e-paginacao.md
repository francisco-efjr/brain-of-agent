# Índices e paginação por seek

Conferido em 2026-10-10 contra V-23 (Use The Index, Luke: `no-offset` e busca case-insensitive, © Winand, direitos reservados: só destilação aqui; PostgreSQL 18 `indexes-multicolumn`, Verificado), V-24 (SQLite `queryplanner`), V-11 (CREATE INDEX), V-32 (convenções, B6) e V-31 (hierarquia de categorias, MIT, só conceito). Itens sem V-nn são conhecimento estável, rotulados Inferido. SQL conceitual: adaptar e testar na engine do projeto.

Sumário
1. Regras de desenho de índice
2. Receitas por padrão de consulta
3. Paginação por seek (keyset)
4. Custo de escrita e remoção
5. Prioridade e formato "incorreto -> correto -> EXPLAIN"
6. Por engine

## 1. Regras de desenho de índice

1. **Ordem das colunas**: igualdade à esquerda, depois faixa e ordenação. Em PostgreSQL, o índice multicoluna serve melhor com condições nas colunas à esquerda; suporta até 32 colunas; existe skip scan na doc atual; "índices com mais de três colunas raramente ajudam" (V-23).
2. **Um índice por padrão de acesso real**, não por coluna. Parta da ficha de acesso (Q-n).
3. **FK**: indexar o lado filho; PostgreSQL não cria (V-32).
4. **Função na coluna indexada** (`UPPER(col)`, `lower(col)`, `date(col)`) inutiliza o índice comum (V-23). Remédios: PostgreSQL = índice de expressão com a **mesma** expressão da consulta; MySQL/SQL Server = coluna gerada/computada indexada ou collation case-insensitive (V-23: a página diz que essas engines não suportam índice funcional como descrito).
5. **Covering**: incluir colunas só para leitura com `INCLUDE` (PostgreSQL, SQL Server) evita ir à tabela; em SQLite um índice composto cobre (V-24).
6. **Parcial**: `CREATE INDEX ... WHERE condição` quando o filtro é fixo e seletivo (ex.: `status = 'pending'`, `deleted_at IS NULL`) (Inferido).
7. **Redundância**: um índice cujo prefixo é outro índice costuma ser dispensável; no SQLite a doc diz "nunca tenha dois índices em que um é prefixo do outro" (V-24). Em outras engines, confirme com medição antes de remover.
8. **Estatística**: sem `ANALYZE` a escolha entre índices pode ser arbitrária (SQLite, V-24) e planos erram em PostgreSQL (V-07).

## 2. Receitas por padrão de consulta

| Padrão | Consulta | Índice (PostgreSQL) | Observação |
| --- | --- | --- | --- |
| Igualdade + ordenação | `WHERE customer_id = ? ORDER BY created_at DESC` | `(customer_id, created_at DESC)` | Evita `Sort` |
| Igualdade + faixa | `WHERE customer_id = ? AND created_at >= ?` | `(customer_id, created_at)` | Igualdade antes da faixa |
| Busca case-insensitive | `WHERE lower(email) = lower($1)` | `CREATE INDEX ... ON users (lower(email))` | A consulta repete a expressão (V-23) |
| Filtro fixo seletivo | `WHERE status = 'pending'` | `(created_at) WHERE status = 'pending'` | Menor e mais barato de manter |
| Só leitura de poucas colunas | `SELECT status, total WHERE customer_id = ?` | `(customer_id) INCLUDE (status, total)` | `Index Only Scan` (precisa visibility map saudável, Inferido) |
| Prefixo de texto | `WHERE name LIKE 'abc%'` | índice com opclass/collation adequada (`text_pattern_ops` em PostgreSQL com collation não-C, Inferido) | `LIKE '%abc'` não usa índice B-tree comum |
| `OR` | `WHERE a = ? OR b = ?` | índice em `a` e outro em `b` (bitmap OR) | SQLite: cada termo precisa de índice (V-24) |

Criação em tabela existente: `CREATE INDEX CONCURRENTLY` fora de transação, depois conferir `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;` (V-11). Detalhes em `safe-migrations`.

## 3. Paginação por seek (keyset)

Problema do `OFFSET`: a engine lê e descarta as linhas puladas (custo cresce com a página) e a lista "deriva" quando há inserções entre uma página e outra, gerando duplicatas ou saltos (V-23). Seek/keyset usa o último item visto como âncora: é mais rápido e estável, mas **não permite pular para página arbitrária** (V-23).

PostgreSQL (comparação de linha), com desempate pela PK (a página `no-offset` não trata empates; incluir a PK é prática comum, Inferido):

```sql
-- índice que atende filtro + ordenação + desempate
CREATE INDEX CONCURRENTLY posts_author_created_id_idx ON posts (author_id, created_at DESC, id DESC);

-- 1ª página
SELECT id, created_at, title FROM posts
WHERE author_id = $1
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- próxima página: âncora = (created_at, id) do último item da página anterior
SELECT id, created_at, title FROM posts
WHERE author_id = $1 AND (created_at, id) < ($2, $3)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Regras:
- `created_at` deve ser `NOT NULL` (NULL complica a ordem e a comparação).
- O token de cursor devolvido ao cliente é opaco (codifique `created_at` e `id`); valide e trate-o como entrada não confiável (parâmetros, nunca concatenação).
- Total de páginas/contagem exata é outra consulta (cara); mostre "tem mais" em vez de "página 3 de 800" se o produto aceitar.
- Engines sem boa otimização de comparação de linha: reescreva `(created_at < $2) OR (created_at = $2 AND id < $3)` e confira o plano (Inferido).
- Direção mista (um campo ASC, outro DESC) exige índice com as mesmas direções.
- Contrato com o frontend (cursor em vez de número de página): segmento web-frontend.

## 4. Custo de escrita e remoção

- Cada índice adiciona custo em INSERT, UPDATE (colunas indexadas) e DELETE, além de espaço e tempo de backup/restore. Liste "quantos índices a mais" em tabelas de escrita intensa.
- Remoção: só após medição. Não remover um índice apenas porque um relatório de "não usado" o lista (V-35): ele pode servir a rotinas raras, à integridade (UNIQUE/PK) ou a réplicas. Plano seguro: `DROP INDEX CONCURRENTLY` em janela, com a definição guardada para recriar.
- Índice `INVALID` (build concorrente que falhou) é ignorado pelas consultas mas continua custando escrita (V-11): apague e refaça, ou `REINDEX INDEX CONCURRENTLY`.
- Tabela particionada: índice concorrente em cada partição e depois no pai sem `CONCURRENTLY` (só metadados) (V-11).

## 5. Prioridade e formato "incorreto -> correto -> EXPLAIN"

Hierarquia de categorias de skills de comunidade (V-31, Supabase, MIT; só conceito, sem copiar texto): Query Performance, Connection Management e Security/RLS (críticas), Schema Design (alta), Concurrency/Locking (média-alta), Data Access Patterns (média), Monitoring (baixa-média), Advanced (baixa). Utilidade para o agente: tratar primeiro o que causa mais dano.

Formato recomendado de achado (Inferido, inspirado em V-31):

```text
Incorreto:  SELECT ... FROM order_items WHERE order_id = $1;      -- Seq Scan, 4,1 s (plano colado pelo usuário)
Correto:    CREATE INDEX CONCURRENTLY order_items_order_id_idx ON order_items (order_id);
EXPLAIN:    peça o plano depois; compare "Execution Time" e o nó (Index Scan esperado)
Rótulo:     Verificado (plano antes); Suposição (ganho depois)
```

Não repita promessas de ganho ("100 a 1000x") de skills de terceiros: Não verificável (V-31).

## 6. Por engine

| Engine | Cobertura nesta base | Postura |
| --- | --- | --- |
| PostgreSQL | Boa (V-07, V-11, V-23) | Regras acima |
| SQLite | Planner/índices (V-24) | `EXPLAIN QUERY PLAN` e pragmas sem fonte lida (L-08) |
| MySQL | Só online DDL e isolamento (V-16, V-09) | Índice funcional via coluna gerada/collation (V-23); EXPLAIN e índices: "sem fonte validada" (L-03) |
| SQL Server | Só RCSI e a nota de V-23 (L-02) | Coluna computada/collation (V-23); planos: "sem fonte validada" |
| MongoDB / DynamoDB / Redis | Ver `nosql-data-modeling` | Índices ESR do Mongo e capacidade do DynamoDB são lacuna (L-07) |
