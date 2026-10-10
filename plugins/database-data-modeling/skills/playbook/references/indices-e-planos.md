# Índices, planos de execução e paginação

Sumário: 1 Ordem de trabalho · 2 EXPLAIN no PostgreSQL · 3 Leitura de um plano · 4 Desenho de índices · 5 Paginação por seek · 6 N+1 e ORM · 7 Hierarquia de prioridade · 8 SQLite · 9 MySQL e SQL Server · 10 Como pedir o plano ao usuário · 11 Gotchas · 12 Lacunas

Índice por intuição é falha comum (brain). Plano primeiro, índice depois, medição de novo no fim. Nenhum ganho numérico entra num relatório sem medição do usuário: a alegação "100 a 1000x" de uma skill de terceiros é Não verificável (V-31).

## 1. Ordem de trabalho

1. Há N+1? Conte consultas por requisição antes de olhar o plano (seção 6).
2. Há plano real? Se não, peça (seção 10) e marque as hipóteses como Suposição.
3. Leia o plano (seção 3), proponha o menor índice ou reescrita, declare o custo de escrita.
4. Crie online (`CREATE INDEX CONCURRENTLY`, ver `migracoes-e-locks.md`).
5. Peça novo plano com o mesmo volume; registre antes e depois em `relatorio-explain.md`.

## 2. EXPLAIN no PostgreSQL (V-07, PG 18)

- `EXPLAIN` mostra o plano estimado. `EXPLAIN ANALYZE` executa a consulta de verdade. Para `INSERT/UPDATE/DELETE`, use `BEGIN; EXPLAIN ANALYZE …; ROLLBACK;` e nunca em produção.
- `BUFFERS` é ativado implicitamente por `ANALYZE` (Verificado V-07). Comando-padrão a pedir: `EXPLAIN (ANALYZE, BUFFERS) <consulta>;`.
- Custos são unidades arbitrárias (`seq_page_cost = 1.0` por convenção). Compare planos, não "segundos" do custo.
- `loops`: tempo e linhas por nó são médias por execução; multiplique por `loops` para o total do nó.
- `SERIALIZE` mede a conversão de saída; a transmissão pela rede nunca entra no tempo (correção de erro de pesquisador, V-07).
- Estimativas mudam após cada `ANALYZE`.

## 3. Leitura de um plano

Exemplo (dados ilustrativos; o formato é o do PG):

```text
Nested Loop  (cost=0.43..9120.10 rows=1200 width=64) (actual time=0.05..4100.2 rows=2400000 loops=1)
  -> Index Scan using orders_pkey on orders o (rows=1 ...) (actual ... rows=1 loops=1)
  -> Seq Scan on order_items i (cost=0.00..8100.00 rows=1200 ...) (actual time=0.02..4090.0 rows=2400000 loops=1)
        Filter: (order_id = o.id)
        Rows Removed by Filter: 38000000
Execution Time: 4101.0 ms
```

Diagnóstico em ordem: (1) estimado 1.200 × real 2,4 milhões: estatística defasada, rode `ANALYZE` e compare de novo; (2) `Seq Scan` com `Rows Removed by Filter` enorme em tabela grande: falta índice de suporte em `order_items(order_id)`; (3) FK sem índice no lado filho é causa comum, o PG não cria (V-32, V-31); (4) `Sort` ou `Hash` com disco (`Sort Method: external merge`): memória de trabalho ou índice que entregue a ordem; (5) muitos `Buffers: read` contra `hit`: I/O frio.

Artefato E, checklist de 6 passos: `EXPLAIN` primeiro · estimado × real por nó · `Seq Scan` em tabela grande + índice de suporte (ordem das colunas) · multiplicar por `loops` · tempo não inclui rede · repetir com o mesmo volume.

## 4. Desenho de índices

| Situação | Regra | Fonte |
| --- | --- | --- |
| Multicoluna | serve melhor com condições nas colunas à esquerda; até 32 colunas; "índices com mais de três colunas raramente ajudam"; PG 18 tem skip scan | Verificado V-23 |
| Igualdade e faixa | coloque colunas de igualdade antes da coluna de faixa/ordenação | Inferido (estável) |
| Função na coluna (`UPPER(email) = …`) | inutiliza o índice comum; PG: índice de expressão com a mesma expressão; MySQL/SQL Server: coluna gerada indexada ou collation case-insensitive | Verificado V-23 |
| Covering | `INCLUDE (col)` evita ir à tabela (PG ≥ 11, conferir) | Inferido, V-32 |
| Parcial | `CREATE INDEX … WHERE status = 'open'` quando o filtro é seletivo e constante | Inferido (estável) |
| FK | indexar a coluna do lado filho | Verificado V-32 (convenção B) |
| Custo | todo índice custa escrita e espaço; um índice prefixo de outro é redundante (SQLite diz isso explicitamente) | Verificado V-24; PG: Inferido |
| Remoção | não remova índice só porque `unused-indexes` o lista; confirme impacto | Verificado V-35 |

Exemplo de pedido-resposta: "`WHERE tenant_id = $1 AND status = 'open' ORDER BY created_at DESC LIMIT 20`" pede `(tenant_id, status, created_at DESC)`: igualdades à esquerda, ordenação por último, o `Sort` some.

## 5. Paginação por seek (V-23)

`OFFSET n` lê e descarta n linhas e sofre "drifting" (duplicatas e saltos quando há inserções). Seek (keyset) usa o último valor visto:

```sql
SELECT id, created_at, title FROM posts
WHERE (created_at, id) < ($1, $2)
ORDER BY created_at DESC, id DESC
LIMIT 20;
-- índice de suporte: (created_at DESC, id DESC)
```

A PK entra como desempate para ordem estável com empates (prática comum, Inferido; a página `no-offset` não trata de empates). Limite: não permite saltar para uma página arbitrária. Em MySQL, verifique no plano que a comparação de linha usa o índice (Inferido). O contrato do cursor com o frontend fica em web-frontend/backend-api.

## 6. N+1 e ORM

Sintoma: latência cresce com o número de itens e o log de SQL mostra a mesma consulta com parâmetros diferentes dentro de um loop. Passos: ativar o log de SQL do ORM no ambiente de teste, contar consultas por requisição antes e depois, trocar por eager loading/JOIN/consulta em lote (`WHERE id IN (…)`), medir. Cuidado com JOIN que multiplica linhas (produto cartesiano em coleções). O plano de cada consulta só importa depois que o número delas está sob controle.

## 7. Hierarquia de prioridade (destilada de V-31, redação própria)

Do mais para o menos impactante: consulta (índices ausentes, `SELECT *`, funções em colunas) → conexões (pool, limites, timeouts) → segurança e RLS → schema (tipos, chaves, normalização) → concorrência e locks → acesso a dados (N+1, lotes, paginação) → monitoramento → recursos avançados. Formato de cada regra no plugin: exemplo incorreto → exemplo correto → `EXPLAIN` que prova. Não carregar tudo para mudança de uma coluna (proporcionalidade).

## 8. SQLite (V-24; EXPLAIN QUERY PLAN: lacuna L-08)

Índice faz busca binária; multicoluna ajuda quando as colunas à esquerda estão ligadas por AND; covering evita consultar a tabela; "nunca tenha dois índices em que um é prefixo do outro"; `OR` só usa índice se cada termo tiver um; `ORDER BY` pode ser atendido pelo índice; sem `ANALYZE` a escolha entre índices é arbitrária. A página do planner não menciona `EXPLAIN QUERY PLAN`; consulte `https://www.sqlite.org/eqp.html` (não lida). WAL e pragmas: sem fonte.

## 9. MySQL e SQL Server (modo genérico, sem fonte validada)

MySQL 8: `EXPLAIN ANALYZE` existe a partir de 8.0.18 (Inferido); `EXPLAIN FORMAT=TREE`; índices invisíveis para testar remoção (Inferido; L-03). SQL Server: plano de execução real no SSMS e `SET STATISTICS IO, TIME ON` (Inferido; L-02). Em ambos diga "sem fonte validada" e peça a saída ao usuário. Para busca case-insensitive use coluna gerada indexada ou collation (Verificado V-23).

## 10. Como pedir o plano ao usuário (P-28)

"Rode em réplica ou ambiente de desenvolvimento, nunca em produção: `EXPLAIN (ANALYZE, BUFFERS) <consulta com parâmetros reais>;`. Se a consulta escreve, use `BEGIN; EXPLAIN (ANALYZE, BUFFERS) …; ROLLBACK;`. Cole a saída completa. Enquanto isso, a hipótese é Suposição." Se há banco local de dev e a consulta só lê, o agente pode executar com autorização da sessão (decisão de design do plugin; o padrão é pedir).

## 11. Gotchas

- `ANALYZE` (comando) atualiza estatísticas; `EXPLAIN ANALYZE` executa a consulta. Nomes parecidos, efeitos diferentes.
- Índice `INVALID` após falha não é usado e custa escrita (V-11).
- Tabela pequena no ensaio escolhe `Seq Scan` com razão; teste com volume.
- Plano com parâmetros fixos pode diferir do plano com prepared statement (Inferido): peça os dois quando suspeitar.

## 12. Lacunas

`pg_stat_statements` e VACUUM/bloat (L-05), MySQL EXPLAIN e SQL Server (L-02, L-03), SQLite `eqp.html` e pragmas (L-08), regra ESR do MongoDB (L-07).
