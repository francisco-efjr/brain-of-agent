# Exemplos para `sql-review`

Redação própria, destilada de V-18 (Google Cloud, BigQuery) e V-19 (Altimate AI, MIT na página; arquivos sem licença, por isso destilado). Dialeto dos exemplos: BigQuery GoogleSQL, salvo indicação. Nada foi executado; os números de bytes dependem das suas tabelas e só valem depois de um `dry_run`.

## Sumário

1. Custo: antes e depois
2. Tabela de equivalência: o que muda o resultado
3. Reescritas com ressalva
4. Comparar resultado original vs reescrita
5. Outros warehouses (lacuna L-07)

## 1. Custo: antes e depois

Antes:
```sql
SELECT * FROM sales.events LIMIT 10;
```
Problema: `LIMIT` não reduz os dados lidos nem o faturamento em `SELECT *` (V-18). Em tabela de 2 TB isso escaneia as colunas todas da tabela inteira.

Depois:
```sql
SELECT event_id, user_id, event_ts
FROM sales.events
WHERE event_date = DATE '2026-10-09'   -- coluna de partição, direto
LIMIT 10;
```
Confirmação para o usuário: `bq query --use_legacy_sql=false --dry_run '<consulta>'` imprime os bytes que seriam processados, sem executar. Compare os dois números e cole-os no relatório. Quando o objetivo é só espiar linhas, a visualização de tabela do console ou `bq head` não executa consulta (Inferido, estável).

Outras trocas de custo (V-18), cada uma com o motivo:
- Tabela fragmentada `events_20261009` → tabela particionada: menos metadados e permissões a avaliar por consulta.
- Junção em chave STRING → chave INT64 quando houver equivalente: comparação mais barata.
- Auto-junção → função de janela (exemplo na seção 3).
- `UPDATE` linha a linha em laço → um `MERGE` em lote.
- Transformação repetida em 5 consultas → modelo/tabela derivada materializada (um `WITH` não garante materialização).
- `ORDER BY` dentro de subconsulta → só no nível externo; em ordenação grande, `LIMIT`.

## 2. Tabela de equivalência: o que muda o resultado

| Reescrita | Risco | Condição para ser equivalente |
| --- | --- | --- |
| `NOT IN (subconsulta)` → `NOT EXISTS` | NULL na coluna externa ou interna, subconsulta vazia | as duas colunas não aceitam NULL (constraint ou verificação de contagem de NULL = 0) |
| `UNION` → `UNION ALL` | remove duplicatas | proibido, a menos que as ramificações sejam comprovadamente disjuntas e o dono confirme |
| `DATE(ts) = d` → intervalo em `ts` | fuso | intervalo construído no mesmo fuso que a função usava |
| Subconsulta repetida → CTE | nenhum, se for a mesma consulta | texto idêntico e não determinística (`RAND`, `CURRENT_TIMESTAMP`) avaliada uma vez muda o resultado |
| Join vírgula → `JOIN ... ON` | nenhum, se a condição vai para o `ON` | `WHERE` de junção movido para `ON` em `INNER JOIN` |
| Auto-junção → `LAG`/janela | empates na ordenação | a combinação (partição, ordenação) é única |
| Agregar antes de juntar | fan-out e métricas não aditivas | `SUM` com chave de junção do lado agregado única; `COUNT(*)`, `AVG`, `COUNT(DISTINCT)` mudam |
| Correlacionada → join | semântica de duplicidade e NULL | proibido nesta skill sem prova |

As cinco verificações para cada mudança: NULL, duplicidade, tipo (cast implícito muda comparação), fuso, ordem (inclui empates sob `LIMIT`).

## 3. Reescritas com ressalva

### 3.1 `NOT IN` para `NOT EXISTS` (E-06)

Original:
```sql
SELECT o.order_id FROM sales.orders o
WHERE o.customer_id NOT IN (SELECT b.customer_id FROM sales.blocked b);
```
Comportamento do original com NULL: se `blocked.customer_id` tiver um único NULL, `x NOT IN (...)` nunca é verdadeiro e a consulta devolve zero linhas. Se `o.customer_id` for NULL e a subconsulta não estiver vazia, essa linha também é excluída. Subconsulta vazia: todas as linhas passam.

Reescrita candidata:
```sql
SELECT o.order_id FROM sales.orders o
WHERE NOT EXISTS (SELECT 1 FROM sales.blocked b WHERE b.customer_id = o.customer_id);
```
Com NULLs ela devolve linhas que o original não devolvia. Veredito: **equivalente somente se `o.customer_id` e `b.customer_id` não aceitam NULL**. Para saber: `SELECT COUNTIF(customer_id IS NULL) FROM sales.blocked` e o mesmo em `sales.orders`. Se `blocked.customer_id` aceita NULL (o caso do pedido), devolva a original e escreva: "Não são equivalentes; o original devolve vazio quando há NULL em blocked (provável defeito). Se o comportamento desejado é o de NOT EXISTS, confirme com o dono e trate como correção de bug com evidência".

### 3.2 Função de data no filtro vira intervalo

```sql
-- original
WHERE DATE(event_ts) = DATE '2026-10-09'
-- reescrita (fuso UTC, o padrão de DATE(timestamp) no BigQuery)
WHERE event_ts >= TIMESTAMP '2026-10-09 00:00:00+00'
  AND event_ts <  TIMESTAMP '2026-10-10 00:00:00+00'
```
Se o original era `DATE(event_ts, 'America/Sao_Paulo')`, o intervalo precisa nascer no mesmo fuso (`TIMESTAMP('2026-10-09', 'America/Sao_Paulo')` e o dia seguinte), senão o resultado muda em 3 horas de dados. Benefício: a comparação direta com a coluna de partição ou de cluster permite poda; confirme com `dry_run` (Suposição até medir).

### 3.3 Auto-junção para função de janela

```sql
-- original: valor do pedido anterior do mesmo cliente
SELECT a.order_id, a.amount, b.amount AS prev_amount
FROM sales.orders a
LEFT JOIN sales.orders b
  ON b.customer_id = a.customer_id
 AND b.created_at = (SELECT MAX(c.created_at) FROM sales.orders c
                     WHERE c.customer_id = a.customer_id AND c.created_at < a.created_at);

-- reescrita
SELECT order_id, amount,
       LAG(amount) OVER (PARTITION BY customer_id ORDER BY created_at) AS prev_amount
FROM sales.orders;
```
Equivalente se `(customer_id, created_at)` é único. Com empate de `created_at` no mesmo cliente, o original duplica linhas (join em dois pedidos com mesmo carimbo) e `LAG` escolhe um: resultados diferentes. Peça a evidência: `SELECT customer_id, created_at, COUNT(*) FROM sales.orders GROUP BY 1,2 HAVING COUNT(*) > 1 LIMIT 5`. Note que o original ainda usa uma subconsulta correlacionada: o ganho de custo é provável, a equivalência depende dos empates.

### 3.4 Agregar antes de juntar

```sql
-- original
SELECT c.segment, SUM(o.amount) AS receita
FROM sales.orders o JOIN sales.customers c USING (customer_id)
GROUP BY c.segment;

-- reescrita: reduz as linhas que entram no join
SELECT c.segment, SUM(o.total) AS receita
FROM (SELECT customer_id, SUM(amount) AS total FROM sales.orders GROUP BY customer_id) o
JOIN sales.customers c USING (customer_id)
GROUP BY c.segment;
```
Para `SUM`, equivale ao original mesmo que `customers` repita a chave (os dois lados multiplicam igual). Para `COUNT(*)`, `AVG` e `COUNT(DISTINCT)` a reescrita muda o resultado. Verifique também clientes sem cadastro: ambos usam `INNER JOIN`, então ambos os descartam.

## 4. Comparar resultado original vs reescrita

Para o usuário rodar em dev, em intervalo curto ou amostra. Estime os bytes das duas consultas antes (`dry_run`).

```sql
-- (a) mesmo conjunto de linhas? (zero linhas = igual; EXCEPT DISTINCT trata NULL como igual)
(SELECT * FROM (<original>) EXCEPT DISTINCT SELECT * FROM (<reescrita>))
UNION ALL
(SELECT * FROM (<reescrita>) EXCEPT DISTINCT SELECT * FROM (<original>));

-- (b) mesma multiplicidade? (a diferença simétrica acima ignora duplicatas)
SELECT (SELECT COUNT(*) FROM (<original>))  AS n_original,
       (SELECT COUNT(*) FROM (<reescrita>)) AS n_reescrita;

-- (c) soma de controle de uma medida
SELECT (SELECT SUM(receita) FROM (<original>))  AS soma_original,
       (SELECT SUM(receita) FROM (<reescrita>)) AS soma_reescrita;
```
A ordem não é comparada por (a)-(c); `ORDER BY` e `LIMIT` da consulta original são preservados por regra. Resultado diferente reprova a reescrita; resultado igual numa amostra é evidência, não prova (rotule "Verificado na amostra X").

## 5. Outros warehouses (lacuna L-07)

Sem fonte validada para Snowflake, Redshift e Databricks SQL nesta pesquisa. Princípios gerais (Inferido, conferir a doc do seu engine):
- Leia o plano ou o perfil da consulta do próprio warehouse antes de reescrever (Snowflake: Query Profile; Redshift: `EXPLAIN`; Databricks/Spark: `EXPLAIN FORMATTED`, ver `spark-streaming-review`).
- Filtros diretos em colunas de partição/cluster, sem função sobre elas.
- Evitar `SELECT *` em views e modelos consumidos por muitos usuários.
- Cuidado com `CREATE OR REPLACE TABLE` como "idempotência": apaga dados e grants (X-05); prefira `MERGE` por chave.
- Não importar regras do `.mdc` Snowflake do awesome-cursorrules: contêm erros verificados (idempotência de `CREATE OR REPLACE`, JSON null em VARIANT, multi-cluster que exige edição Enterprise).
