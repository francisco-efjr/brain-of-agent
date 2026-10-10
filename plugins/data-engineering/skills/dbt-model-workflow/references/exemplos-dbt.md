# Exemplos de dbt para o fluxo `dbt-model-workflow`

Material de apoio com redação própria, destilado de V-05, V-07 a V-10 e V-27 (dbt Labs, docs.getdbt.com, Altimate AI; sem texto literal de terceiros). Onde o detalhe depende de versão do dbt ou do adapter, o rótulo é Inferido: as páginas oficiais de snapshots, incrementais, contratos e testes unitários não foram lidas na pesquisa (lacuna L-04). Confira na documentação da versão instalada (https://docs.getdbt.com) antes de afirmar.

## Sumário

1. Staging e YAML de testes
2. Mudança quebrável: modelo versionado
3. Incremental
4. Snapshot (SCD2)
5. Mart dimensional: fato e dimensões com grain explícito
6. Erros comuns: sintoma, causa provável, como confirmar

## 1. Staging e YAML de testes

```sql
-- models/staging/shop/stg_shop__orders.sql  (tipos dependem do adapter)
with source as (
    select * from {{ source('shop', 'orders') }}
),
renamed as (
    select
        cast(id as string)             as order_id,      -- PK, string
        cast(customer_id as string)    as customer_id,   -- FK
        status                         as order_status,
        cast(total as numeric(18, 2))  as total_amount,  -- moeda em decimal
        cast(created_at as timestamp)  as created_at     -- UTC
    from source
)
select * from renamed
```

```yaml
version: 2
models:
  - name: stg_shop__orders
    description: "Pedidos da loja, uma linha por pedido. Só renomeia e tipa."
    columns:
      - name: order_id
        description: "Identificador do pedido na origem."
        data_tests: [unique, not_null]        # use `tests:` se o projeto ainda usa essa chave
      - name: customer_id
        description: "Cliente que fez o pedido."
        data_tests:
          - not_null
          - relationships:
              to: ref('stg_shop__customers')
              field: customer_id
      - name: order_status
        description: "Situação do pedido."
        # accepted_values omitido de propósito: valores pendentes de confirmação do dono do dado
```

Notas: em versões recentes o dbt move os argumentos de testes genéricos para uma chave `arguments:` e emite aviso para a forma antiga (Inferido); imite o YAML que o projeto já usa. Frescor da fonte (`freshness` e `loaded_at_field` em `sources:`) cabe aqui quando a origem tem carimbo de carga (Inferido).

## 2. Mudança quebrável: modelo versionado

Caso: renomear `cust_id` para `customer_id` em `customers`, com consumidores `orders_enriched` e `marts_ltv`.

Passos:
1. `grep -rnE "ref\(['\"]customers['\"]" models tests analyses macros` e exposures. Resultado esperado: os dois consumidores, com arquivo:linha.
2. Criar a versão nova do modelo sem apagar a antiga:

```yaml
models:
  - name: customers
    latest_version: 2
    versions:
      - v: 1            # arquivo customers_v1.sql (convenção <modelo>_v<N>), mantém cust_id
      - v: 2            # arquivo customers_v2.sql, expõe customer_id
    columns:
      - name: customer_id
        data_tests: [unique, not_null]
```

3. Consumidores migram um a um: `{{ ref('customers', v=2) }}`; enquanto isso fixam `v=1`. Quando todos migrarem (incluindo BI fora do repositório, que é Suposição até o usuário confirmar), registre a data de descontinuação da versão 1.
4. Verificação (dev, com consentimento): `dbt build --select customers+`; contagem de `customers_v1` igual à de `customers_v2`; `customer_id` sem nulos.

Por que não editar no lugar: o `dbt build` do projeto pode ficar verde por acaso (coluna removida que ninguém selecionava) enquanto dashboards externos quebram em silêncio (V-07). A sintaxe exata de `versions` (colunas incluídas/excluídas, `defined_in`, descontinuação) varia por versão; conferir antes de escrever (recurso disponível a partir do dbt 1.5, Inferido).

Alternativa quando a organização aceita: migração coordenada em um único PR, com todos os consumidores do repositório alterados e a lista de consumidores externos avisados. Registre a escolha e o motivo.

## 3. Incremental

```sql
{{ config(
    materialized = 'incremental',
    unique_key = 'order_id',
    on_schema_change = 'fail'
) }}

select order_id, customer_id, total_amount, updated_at
from {{ ref('stg_shop__orders') }}
{% if is_incremental() %}
  -- janela de reprocessamento de 3 dias para dado atrasado (macro dbt.dateadd é multi-adapter)
  where updated_at >= (select {{ dbt.dateadd('day', -3, 'max(updated_at)') }} from {{ this }})
{% endif %}
```

Perguntas obrigatórias antes de entregar (Inferido, L-04):
- Qual é o `unique_key` e ele é de fato único na origem? Duas linhas da origem para a mesma chave fazem o merge falhar ou duplicar, conforme o adapter.
- Qual a estratégia (`merge`, `delete+insert`, `insert_overwrite`, `microbatch`) e o adapter a suporta? Estratégias disponíveis dependem do adapter e da versão.
- Qual a janela para dado atrasado e quem decide? Sem janela, atualização tardia nunca entra.
- O que acontece no primeiro build e na segunda execução sem dados novos? A segunda não pode mudar a contagem.
- `--full-refresh` apaga e recria a tabela: destrutivo (S-06). Só em dev, com contagem e confirmação.

Verificação em dev (cada execução com consentimento):
1. `dbt build --select <modelo>`: guarde a contagem C1.
2. Repita o mesmo comando sem mudar a origem: contagem C2 deve ser igual a C1 e `count(*) - count(distinct order_id)` deve ser 0.
3. Equivalência com a carga completa: em schema de dev, `dbt build --select <modelo> --full-refresh` e comparar contagem e soma de controle com o acumulado incremental. Diferença sem explicação reprova.

## 4. Snapshot (SCD2)

Duas formas existem conforme a versão. Bloco clássico (Inferido):

```sql
{% snapshot customers_snapshot %}
{{ config(
    target_schema = 'snapshots',
    unique_key = 'customer_id',
    strategy = 'check',
    check_cols = ['name', 'email', 'segment']
) }}
select * from {{ source('shop', 'customers') }}
{% endsnapshot %}
```

Em versões recentes (1.9 ou superior, Inferido) o snapshot pode ser declarado em YAML com `relation`, `config.unique_key`, `config.strategy`, `config.check_cols`. Confira na doc.

Pontos que o relato do rmoff mostrou falharem em silêncio (V-05):
- `check_cols` que não cobre todos os campos que importam historicamente (no relato, coordenadas ficaram de fora). Confira por consulta: colunas da origem menos `check_cols` = lista de campos não rastreados; cada um precisa de decisão registrada.
- Segunda execução sem mudança na origem não pode criar linha nova: compare `count(*)` antes e depois.
- Mudança de um campo rastreado, feita na origem de dev, deve gerar exatamente uma linha nova, fechar a anterior (`dbt_valid_to` preenchido) e manter `dbt_valid_to` nulo na vigente.
- Unicidade: por `unique_key` só uma linha com `dbt_valid_to is null`.

## 5. Mart dimensional: fato e dimensões com grain explícito

Fonte: V-27 (Kimball Group, só títulos de técnicas; grain, aditividade e conformação não foram lidos, então este roteiro é Inferido).

Passo 1: declare o grain em uma frase antes do SQL.
> `fct_order_items`: uma linha por item de pedido (pedido + produto + linha), em UTC.

Passo 2: classifique as medidas.

| Medida | Aditividade | Observação |
| --- | --- | --- |
| `quantity` | aditiva | soma por qualquer dimensão |
| `line_amount` (quantidade x preço) | aditiva | decimal, moeda explícita |
| `unit_price` | não aditiva | média ponderada, nunca soma |
| `account_balance` (se houver snapshot periódico) | semiaditiva | soma entre contas, não entre datas |

Passo 3: escolha o tipo de fato (transação, snapshot periódico, snapshot acumulado) e o tipo de SCD de cada dimensão pela pergunta "preciso do valor histórico daquele atributo?". Segmento do cliente que precisa do valor da época do pedido = tipo 2 (snapshot); nome corrigido sem histórico = tipo 1 (sobrescreve).

Passo 4: chaves e fatos sem dimensão correspondente. Dimensão com chave substituta (hash da chave natural, via pacote que o projeto já usa; senão, uma macro do projeto). Pedido sem cliente cadastrado (chegada tardia) vai para uma linha "desconhecido" da dimensão em vez de linha perdida no join interno.

Premissa do exemplo: `stg_shop__order_items` traz `customer_id` e `created_at` do pedido. Se a origem tiver esses campos só em `stg_shop__orders`, junte a ela no grão do pedido (uma linha por `order_id`) antes de ligar à dimensão, e confira que a contagem da fato não mudou.

```sql
-- models/marts/fct_order_items.sql
select
    oi.order_item_id,                       -- PK da fato (grain)
    oi.order_id,                            -- dimensão degenerada
    coalesce(c.customer_key, 'unknown') as customer_key,
    oi.product_id,
    cast(oi.created_at as date)         as order_date,
    oi.quantity,
    oi.quantity * oi.unit_price         as line_amount
from {{ ref('stg_shop__order_items') }} oi
left join {{ ref('dim_customers') }} c
    on oi.customer_id = c.customer_id
   and oi.created_at >= c.valid_from and oi.created_at < coalesce(c.valid_to, timestamp '9999-12-31')
```

Testes do mart (V-09): `order_item_id` `unique` + `not_null`; `customer_key` `relationships` para `dim_customers`; teste singular de reconciliação: `select 1 where (select sum(line_amount) from {{ ref('fct_order_items') }}) <> (select sum(quantity * unit_price) from {{ ref('stg_shop__order_items') }})`. O join por intervalo de vigência não pode multiplicar linhas: `count(*)` da fato igual ao da origem.

## 6. Erros comuns: sintoma, causa provável, como confirmar

| Sintoma | Causa provável | Como confirmar |
| --- | --- | --- |
| `Compilation Error: Model 'a' depends on a node named 'b' which was not found` | nome do `ref` errado, `enabled: false`, pacote não instalado, pasta fora de `model-paths` | `dbt ls --select b`; `grep -rn "name: b" models`; `model-paths` em `dbt_project.yml` |
| `Database Error ... column not found` | coluna renomeada no upstream | SQL compilado em `target/compiled/`; `dbt show --select <upstream> --limit 5` |
| `'dbt_utils' is undefined` ou macro não encontrada | pacote ausente (`dbt deps` não rodou) | `packages.yml` vs pasta de pacotes; `dbt deps` baixa código: peça consentimento |
| `dbt found two resources with the name ...` | nomes de modelo repetidos entre pastas ou pacotes | `grep -rn` pelo nome; renomear um |
| `Found a cycle` ou dependência circular | `ref` mútuo entre modelos | `dbt ls --select +a+` e inspecionar |
| Teste `unique` falhou | duplicidade real na origem, join que multiplica linhas | compilar o teste (SQL em `target/compiled/`), rodar como consulta agregada com consentimento; contar `group by chave having count(*) > 1` |
| Teste `relationships` falhou | filho sem pai (dado atrasado, filtro no pai) | contar órfãos; decidir entre corrigir carga, ajustar dado atrasado ou aceitar com `warn` e número |
| Incremental duplica ou falha no merge | `unique_key` não único na origem, estratégia incompatível | contar chaves repetidas na consulta do modelo; conferir estratégia do adapter |
| `Could not find profile named ...` | `profile:` de `dbt_project.yml` não existe no ambiente do usuário | peça ao usuário para conferir; não abra `profiles.yml` |
| Build verde, número errado | join com fan-out, filtro de data/fuso, coluna descartada | reconciliar com a origem (skill `pipeline-acceptance`) |
