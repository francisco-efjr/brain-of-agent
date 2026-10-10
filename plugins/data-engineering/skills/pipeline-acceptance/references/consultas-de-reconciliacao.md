# Consultas de reconciliação para `pipeline-acceptance`

Redação própria, derivada dos 8 itens de V-05 (rmoff, classe B) e do oráculo antes/depois de `brains/qa/references/dados-ambientes-ci.md` (brain-of-agent, MIT, do autor do plugin). As consultas usam SQL quase padrão; ajuste ao dialeto do warehouse (Inferido). Todas são leituras, mas consomem bytes/crédito: estime custo (`dry_run` no BigQuery, `EXPLAIN` nos demais), filtre por partição ou por data de corte, execute só em desenvolvimento e com consentimento por execução. Nunca cole resultados que contenham dados pessoais; agregue ou mascare.

## Sumário

1. Contagem por partição (item 1)
2. Campos vs colunas (item 2)
3. Segunda execução: foto antes e depois (item 3)
4. Chaves nos dados carregados (item 4)
5. SCD2 e snapshots (item 5)
6. `warn` com número (item 6)
7. Métrica à mão e valores trocados entre entidades (item 7)
8. Modelo de lista "não verificado" (item 8)

Notação: `:corte` é a data/hora de corte fixada no manifesto de execução; `src` é a origem; `dw` é o destino em dev.

## 1. Contagem por partição

Origem e destino no mesmo sistema:

```sql
with s as (
  select cast(created_at as date) as d, count(*) as n
  from src.orders where created_at < :corte group by 1),
t as (
  select cast(created_at as date) as d, count(*) as n
  from dw.fct_orders where created_at < :corte group by 1)
select coalesce(s.d, t.d) as d, s.n as n_origem, t.n as n_destino,
       coalesce(s.n, 0) - coalesce(t.n, 0) as diferenca
from s full outer join t on s.d = t.d
where coalesce(s.n, 0) <> coalesce(t.n, 0)
order by d;
```
Resultado esperado: zero linhas. Linhas devolvidas são os dias com diferença; cada uma precisa de explicação (filtro declarado, dado atrasado, perda).

Sistemas diferentes (API, arquivo, outro banco): obtenha a contagem oficial da fonte por quem tem acesso e compare na mão. Para API paginada, o plugin não chama a API; peça o log com linhas por página e o total informado pela fonte (por exemplo um cabeçalho de total), e confira três coisas: soma das páginas igual ao total da fonte; nenhuma página com tamanho igual ao `limit` seguida de ausência de próxima página (sinal de truncamento); contagem no destino igual à soma.

Exclusões deliberadas: some a contagem excluída por regra (`where status = 'cancelled'` etc.) e confirme `destino + excluídas = origem`.

## 2. Campos vs colunas

```sql
-- colunas do destino (PostgreSQL, Snowflake, Redshift e similares; no BigQuery use <dataset>.INFORMATION_SCHEMA.COLUMNS)
select column_name, data_type
from information_schema.columns
where table_schema = 'dw' and table_name = 'dim_stations'
order by ordinal_position;
```
Compare com a lista de campos da origem (contrato, schema da API, DDL). Produza a tabela `campo | chegou? | coluna destino | decisão registrada`. Três sinais de problema: campo sem coluna e sem decisão; duas colunas para o mesmo conceito (por exemplo `lat` e `latitude`, ambas com os mesmos valores); tipo mais estreito que o da origem (`cast` para inteiro de campo decimal, texto truncado).

## 3. Segunda execução: foto antes e depois

Rode antes da segunda carga e depois dela, sem mudar a origem:

```sql
select count(*)                        as n,
       count(distinct order_id)        as n_chaves,
       sum(total_amount)               as soma_valor,
       min(updated_at)                 as min_upd,
       max(updated_at)                 as max_upd
from dw.fct_orders;
```
Esperado: as cinco colunas idênticas. `n` maior que `n_chaves` indica duplicidade.

Checksum de linha (opcional, exemplos por dialeto, Inferido; valide antes de confiar):

```sql
-- BigQuery: use SOMA, não XOR; duas linhas idênticas se anulam em XOR e escondem a duplicidade
select count(*) as n,
       sum(cast(farm_fingerprint(to_json_string(t)) as numeric)) as checksum
from dw.fct_orders as t;

-- PostgreSQL
select count(*) as n,
       sum((('x' || substr(md5(t::text), 1, 16))::bit(64)::bigint)::numeric) as checksum
from dw.fct_orders as t;
```
Em Snowflake, Redshift e Databricks use a função de hash agregada da plataforma e confira na documentação se ela é sensível à ordem e a duplicatas. Se a coluna inclui carimbo de carga (`_loaded_at`), exclua-a do hash.

## 4. Chaves nos dados carregados

```sql
-- duplicidade da PK
select order_id, count(*) as n from dw.fct_orders group by 1 having count(*) > 1 limit 20;
-- nulos na PK e nas FKs
select count(*) as pk_nula from dw.fct_orders where order_id is null;
select count(*) as fk_nula from dw.fct_orders where customer_id is null;
-- órfãos (FK sem pai)
select count(*) as orfaos
from dw.fct_orders f left join dw.dim_customers d on f.customer_id = d.customer_id
where d.customer_id is null and f.customer_id is not null;
```
Chave composta: `group by` todas as colunas do grain. A garantia vem destes resultados; um `unique` declarado no YAML só vale se o teste foi executado e aparece na saída.

## 5. SCD2 e snapshots

Nomes de colunas abaixo seguem o snapshot do dbt (`dbt_valid_from`, `dbt_valid_to`, `dbt_scd_id`); troque pelos do seu projeto.

```sql
-- no máximo uma versão vigente por chave
select customer_id, count(*) from dw.customers_snapshot
where dbt_valid_to is null group by 1 having count(*) > 1;

-- sem sobreposição de vigência para a mesma chave
select a.customer_id
from dw.customers_snapshot a
join dw.customers_snapshot b
  on a.customer_id = b.customer_id and a.dbt_scd_id <> b.dbt_scd_id
 and a.dbt_valid_from < coalesce(b.dbt_valid_to, timestamp '9999-12-31')
 and b.dbt_valid_from < coalesce(a.dbt_valid_to, timestamp '9999-12-31')
limit 20;
```
Campos não rastreados: liste as colunas da origem e subtraia `check_cols` (ou o campo `updated_at` da estratégia por tempo, que só detecta o que muda `updated_at`). Cada campo restante precisa de decisão ("não importa historicamente") registrada.

Ensaio de mudança (somente em dev, em cópia da origem): altere um campo rastreado de uma chave, rode o snapshot e espere exatamente uma linha nova, a anterior fechada e uma só vigente. Altere um campo não rastreado e espere nenhuma linha nova (se a decisão foi essa).

## 6. `warn` com número

- Saída do `dbt build`: linhas `WARN` por teste, com o número de linhas que falharam.
- Arquivo `target/run_results.json`: cada resultado traz `status` e, para testes, a contagem de falhas (leitura de arquivo, sem custo; confira o campo na versão instalada).
- Expectativas de outras ferramentas: relatório da ferramenta, com a contagem de violações por regra e a ação (`warn`, `drop`, `fail`).

Tabela de saída: `teste/regra | ação | linhas violadoras | % do total | dono | prazo`. Linha sem número fica "pendente de medição", nunca "ok".

## 7. Métrica à mão e valores trocados entre entidades

Contagens iguais não impedem valores trocados entre clientes (brain). Duas defesas baratas:

```sql
-- (a) soma de controle por balde de chave: acha QUAL faixa diverge sem varrer linha a linha
select mod(abs(farm_fingerprint(order_id)), 64) as balde,   -- BigQuery; adapte a função de hash
       count(*) as n, sum(total_amount) as soma
from dw.fct_orders group by 1 order by 1;
-- rode a consulta equivalente na origem e compare balde a balde; refine o balde divergente
```

```sql
-- (b) invariante por entidade: total de um cliente conhecido bate com o relatório estabelecido
select customer_id, count(*) as pedidos, sum(total_amount) as total
from dw.fct_orders where customer_id in (<3 a 5 ids de amostra, sintéticos ou mascarados>)
group by 1;
```
Escolha as amostras com casos de borda: cliente com muitos pedidos, pedido com valor zero, registro legado com nulos, dia de virada de mês, fuso. Registre qual relatório ou fonte serviu de referência e a data dele.

## 8. Modelo de lista "não verificado"

```text
Não verificado:
- Segunda execução do job de estações: sem permissão para executar no dev; previsão pela leitura do SQL (Inferido).
- Contagem oficial da fonte: o usuário vai fornecer o total do cabeçalho (pendente).
- Consumidores fora do repositório (dashboard "Vendas"): fora do alcance (Não verificável por mim).
Para fechar: <comando> em <target>, por <responsável>.
```
