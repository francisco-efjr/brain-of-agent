# Ler um plano de execução do PostgreSQL

Conferido em 2026-10-10 contra V-07 (`using-explain`, PostgreSQL 18.6; Verificado pelo validador), V-23 (índices multicoluna) e V-24 (SQLite). O glossário de nós e as opções além das citadas em V-07 são conhecimento estável do domínio, marcados Inferido: conferir a doc da versão instalada. Números nos exemplos são **ilustrativos, não medições**.

Sumário
1. Comandos (o que pedir ao usuário)
2. Glossário de nós e campos
3. Exemplo anotado: antes e depois
4. Sequência de leitura (6 passos)
5. Outras engines (limites de fonte)

## 1. Comandos (o que pedir ao usuário)

Sempre em réplica ou banco de desenvolvimento com volume parecido; nunca em produção.

```sql
-- SELECT: executa a consulta de verdade (V-07)
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;

-- DML: descartar o efeito
BEGIN;
EXPLAIN (ANALYZE, BUFFERS) UPDATE orders SET status = 'paid' WHERE id = 42;
ROLLBACK;

-- só o plano estimado, sem executar (seguro para qualquer SQL):
EXPLAIN SELECT ...;
```

Notas:
- `BUFFERS` é ativado implicitamente por `ANALYZE` na doc atual (V-07); em versões antigas pode não ser. Pedir explicitamente evita dúvida.
- Opção `SERIALIZE` (existe em versões recentes; conferir a sua) mede apenas a conversão da saída; a transmissão pela rede nunca entra no tempo (V-07).
- O custo (`cost=`) está em unidades arbitrárias, com `seq_page_cost = 1.0` como convenção (V-07); não é milissegundo.
- `FORMAT JSON`/`FORMAT TEXT`: peça texto para leitura humana; JSON só se for colar em ferramenta de visualização.
- Peça junto: `SELECT version();`, DDL das tabelas e índices (`\d+ tabela` no `psql`) e quando foi o último `ANALYZE` (`SELECT relname, last_analyze, last_autoanalyze FROM pg_stat_user_tables WHERE relname = 'tabela';`, Inferido).

## 2. Glossário de nós e campos

| Item | Significado | O que observar |
| --- | --- | --- |
| `Seq Scan` | Lê a tabela inteira | Em tabela grande com filtro seletivo, procure índice; em tabela pequena é normal |
| `Index Scan` | Percorre o índice e busca a linha na tabela | Bom para poucas linhas; `Index Cond` mostra o que o índice resolveu |
| `Index Only Scan` | Responde só pelo índice (covering) | `Heap Fetches` alto indica visibilidade desatualizada (Inferido) |
| `Bitmap Index/Heap Scan` | Combina índices e lê páginas em ordem física | Comum para muitos resultados ou `OR` |
| `Nested Loop` | Para cada linha externa, busca na interna | Perigoso com interna sem índice: multiplique por `loops` |
| `Hash Join` | Monta tabela hash de um lado | Bom para grandes volumes sem ordem |
| `Merge Join` | Une duas entradas ordenadas | Aproveita índices/ordenação |
| `Sort` | Ordena | `Sort Method: external merge Disk` = não coube em memória (`work_mem`, Inferido) |
| `Rows Removed by Filter` | Linhas lidas e descartadas | Alto = índice melhor poderia filtrar antes |
| `rows=` em `(cost=...)` | **Estimativa** do planner | Compare com `rows=` em `(actual ...)` |
| `actual time=a..b` | ms até a 1ª linha .. até a última, **por execução do nó** | Multiplique por `loops` (V-07) |
| `loops=N` | Quantas vezes o nó executou | Total do nó = tempo e linhas por execução x `loops` (V-07) |
| `Buffers: shared hit/read` | Páginas do cache / lidas de fora do cache | `read` alto = I/O |
| `Planning Time`, `Execution Time` | Tempos totais | Execução não inclui rede |

## 3. Exemplo anotado: antes e depois

Cenário (caso de eval E-03): `order_items` sem índice em `order_id`; consulta: pedidos do cliente 42 com seus itens.

Antes (ilustrativo):

```text
Nested Loop  (cost=0.43..61234.50 rows=1200 width=40) (actual time=0.05..4098.7 rows=2412 loops=1)
  Buffers: shared hit=312 read=58211
  ->  Index Scan using orders_customer_id_created_at_idx on orders o  (cost=0.43..120.40 rows=12 width=8) (actual time=0.02..0.5 rows=12 loops=1)
        Index Cond: (customer_id = 42)
  ->  Seq Scan on order_items oi  (cost=0.00..5100.00 rows=100 width=40) (actual time=0.8..340.1 rows=201 loops=12)
        Filter: (order_id = o.id)
        Rows Removed by Filter: 2399799
Execution Time: 4102.3 ms
```

Leitura:
1. `orders` está bem: `Index Scan` com `Index Cond`, 12 linhas.
2. O nó caro é `Seq Scan on order_items`: 340,1 ms **por execução** x `loops=12` = cerca de 4.081 ms, quase todo o `Execution Time` (V-07: multiplicar por `loops`).
3. `Rows Removed by Filter: 2399799` (por execução): cada uma das 12 voltas lê a tabela inteira para devolver 201 linhas. Falta índice em `order_items(order_id)`.
4. Estimado `rows=100` por volta vs real `201`: fator 2, tolerável. Se fosse 1.200 vs 2,4 milhões, o primeiro passo seria `ANALYZE order_items;` e novo plano (V-07, Art. E).

Proposta (DDL online, fora de transação; Suposição quanto ao ganho):

```sql
CREATE INDEX CONCURRENTLY order_items_order_id_idx ON order_items (order_id);
ANALYZE order_items;
```

Depois (o que o usuário deve colar para fechar o ciclo; ilustrativo):

```text
Nested Loop  (... rows=2412 loops=1)
  ->  Index Scan using orders_customer_id_created_at_idx on orders o  (... rows=12 loops=1)
  ->  Index Scan using order_items_order_id_idx on order_items oi  (actual time=0.02..0.04 rows=201 loops=12)
        Index Cond: (order_id = o.id)
```

Registre no relatório os dois `Execution Time` **reais do usuário**; os números acima não são resultado de medição.

## 4. Sequência de leitura (6 passos; Art. E)

1. `EXPLAIN` primeiro; `EXPLAIN ANALYZE` executa (DML só em `BEGIN ... ROLLBACK`, nunca em produção).
2. Compare linhas estimadas e reais por nó; diferença grande = estatística desatualizada: `ANALYZE` e comparar de novo.
3. Procure `Seq Scan` em tabela grande e veja se há índice de suporte (ordem das colunas, V-23).
4. Multiplique tempo e linhas por `loops`; use `BUFFERS` para I/O.
5. Lembre que o tempo não inclui a rede.
6. Repita a medição com o mesmo volume e registre antes e depois.

## 5. Outras engines (limites de fonte)

| Engine | O que esta base cobre | O que dizer |
| --- | --- | --- |
| SQLite | Planner e índices (V-24): busca binária em índice, multicoluna com AND nas colunas à esquerda, covering, "nunca dois índices em que um é prefixo do outro", `OR` só usa índice se cada termo tiver o seu, `ORDER BY` pode ser atendido pelo índice, sem `ANALYZE` a escolha é arbitrária | A página do planner **não** menciona `EXPLAIN QUERY PLAN` (V-24, correção); o comando existe (Inferido); consulte `sqlite.org/eqp.html` na versão em uso (L-08) |
| MySQL | Nada sobre EXPLAIN (L-03) | "Sem fonte validada": peça `EXPLAIN` (e `EXPLAIN ANALYZE` se a versão suportar) e leia com princípios gerais: tipo de acesso, linhas estimadas, uso de índice |
| SQL Server | Nada sobre planos (L-02) | "Sem fonte validada": peça o plano real (actual execution plan) e aplique os mesmos princípios |

Quando a engine não tem fonte validada, diga isso na saída e limite as recomendações ao que o SQL e o DDL provam.
