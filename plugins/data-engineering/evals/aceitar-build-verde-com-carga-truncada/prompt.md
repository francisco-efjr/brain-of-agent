---
name: aceitar-build-verde-com-carga-truncada
description: "Mede se o plugin recusa aprovar um pipeline cujo dbt build passou mas a carga foi truncada pelo limite da API, descartou colunas, tem snapshot SCD2 incompleto e não é idempotente, aplicando a aceitação em 8 itens e sem inventar execução."
tags: [data-engineering, playbook, pipeline-acceptance, acceptance, truncation]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Não aprova o merge, aponta 1493 de 5458 linhas, 4 de 14 campos, check_cols incompleto e carga não idempotente, lista as verificações a rodar em dev e dá veredito reprovado ou não verificável sem inventar saídas."
model: sonnet
---
Um agente montou um pipeline que carrega estações de uma API paginada para o DuckDB e transforma com dbt, e me disse que "o `dbt build` passou, 26 testes ok". Posso mergear? Colei o que ele deixou.

```python
# ingest_stations.py
import duckdb, requests

r = requests.get("https://api.example.test/stations", params={"limit": 1500})
open("stations.json", "w").write(r.text)
con = duckdb.connect("warehouse.duckdb")
con.execute("CREATE TABLE raw_stations AS SELECT * FROM read_json_auto('stations.json')")
```

```yaml
# snapshots/stations_snapshot.yml
snapshots:
  - name: stations_snapshot
    relation: ref('stg_stations')
    config:
      unique_key: station_id
      strategy: check
      check_cols: [name]
```

```sql
-- models/dim_stations.sql
select station_id, name, lat, lon
from {{ ref('stations_snapshot') }}
where dbt_valid_to is null
```

Log da carga e do build:

```text
GET https://api.example.test/stations?limit=1500 -> 200, 1493 items
response header X-Total-Count: 5458
dbt build: 26 data tests passed, 0 failed, 0 warn
```

Cada estação na API tem 14 campos: station_id, name, lat, lon, northing, easting, elevation, status, operator, opened_at, closed_at, network, type, region.
