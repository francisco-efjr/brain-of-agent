# Exemplos de Airflow para `airflow-dag-workflow`

Redação própria, destilada de V-13 (documentação oficial do Airflow, stable = 3.3.2 na data da pesquisa), V-14 (Astronomer, Apache-2.0, ideias reescritas) e V-15 (Dagster). Os trechos de código são ilustrativos e escritos para este plugin; imports e nomes de parâmetros mudam entre versões, então confira a versão instalada (Inferido). Nada aqui foi executado.

## Sumário

1. DAG com problemas (caso E-03)
2. DAG corrigida (Airflow 3)
3. Teste de import e de forma
4. Variações para Airflow 2
5. Relatório de depuração (exemplo ilustrativo)
6. Plano de backfill (exemplo ilustrativo)
7. Dagster: asset particionado (Inferido)

## 1. DAG com problemas

```python
from airflow import DAG
from airflow.models import Variable
from datetime import datetime
import pandas as pd

BUCKET = Variable.get("bucket")                                   # banco de metadados a cada parse
df = pd.read_sql("select * from raw.orders",                      # leitura de produção no parse
                 "postgresql://app:<senha>@db/prod")              # segredo no código

def load(ti, **_):
    day = datetime.now().date()                                   # now() no filtro
    rows = df[df.created_at.dt.date == day]
    ti.xcom_push(key="rows", value=rows.to_dict("records"))       # volume no XCom
    conn.execute("insert into mart.orders select ...")            # INSERT cego

with DAG("orders", schedule="@daily", start_date=datetime(2024, 1, 1)):  # catchup e retries não decididos
    ...
```

Achados (V-13): perguntas 1, 2, 3, 4, 5, 6, 7 e 12 do checklist falham; 8 e 9 não se aplicam; 10 e 11 ficam "não verificado" até o topo do arquivo parar de acessar o banco.

## 2. DAG corrigida (Airflow 3)

```python
import datetime as dt

import pendulum
from airflow.sdk import dag
from airflow.providers.common.sql.operators.sql import SQLCheckOperator, SQLExecuteQueryOperator

INTERVALO = (
    "created_at >= TIMESTAMP '{{ data_interval_start }}' "
    "AND created_at < TIMESTAMP '{{ data_interval_end }}'"        # cast conforme o warehouse
)


@dag(
    dag_id="orders_daily",
    schedule="@daily",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),           # fixa, nunca dinâmica
    catchup=False,                                                # decisão explícita; backfill é plano à parte
    max_active_runs=1,
    default_args={
        "retries": 3,
        "retry_delay": dt.timedelta(minutes=5),
        "retry_exponential_backoff": True,                        # confira o tipo do parâmetro na versão
        "max_retry_delay": dt.timedelta(hours=1),
    },
    tags=["orders", "mart"],
)
def orders_daily():
    carregar = SQLExecuteQueryOperator(
        task_id="carregar_intervalo",
        conn_id="warehouse",                                      # Connection no secrets backend
        sql=f"""
            MERGE mart.orders AS t
            USING (SELECT order_id, customer_id, amount, created_at
                   FROM raw.orders WHERE {INTERVALO}) AS s
            ON t.order_id = s.order_id
            WHEN MATCHED THEN UPDATE SET customer_id = s.customer_id,
                                         amount = s.amount, created_at = s.created_at
            WHEN NOT MATCHED THEN INSERT (order_id, customer_id, amount, created_at)
                 VALUES (s.order_id, s.customer_id, s.amount, s.created_at)
        """,
    )
    nao_vazio = SQLCheckOperator(
        task_id="checar_nao_vazio",
        conn_id="warehouse",
        sql=f"SELECT COUNT(*) > 0 FROM mart.orders WHERE {INTERVALO}",
    )
    chaves_unicas = SQLCheckOperator(
        task_id="checar_chaves_unicas",
        conn_id="warehouse",
        sql=f"SELECT COUNT(*) = COUNT(DISTINCT order_id) FROM mart.orders WHERE {INTERVALO}",
    )
    carregar >> [nao_vazio, chaves_unicas]


orders_daily()
```

Por que assim:
- Intervalo vem do contexto (`data_interval_start`/`data_interval_end`, renderizados pelo Jinja nos campos de template do operador), então um retry ou backfill de um dia reprocessa exatamente aquele dia (V-13).
- `MERGE` por chave torna a segunda execução inofensiva. Limitação: `MERGE` não remove linhas que sumiram da origem dentro do intervalo; se a origem apaga linhas, use apagar-o-intervalo-e-inserir dentro de uma transação (a sintaxe de transação multi-instrução depende do warehouse) e documente a escolha.
- Sem rede, banco ou `Variable` no topo: o arquivo só declara a DAG. Variáveis entram por Jinja (`{{ var.value.chave }}`) em campos de template ou dentro de uma tarefa.
- Segredo vive na Connection `warehouse`.
- Dado em volume nunca passa por XCom. Se for preciso Python, a tarefa grava o lote em armazenamento de objetos e devolve só o caminho (claim-check).
- `SQLCheckOperator` avalia a primeira linha da consulta; valor falso reprova a tarefa. `SQLColumnCheckOperator` e `SQLTableCheckOperator` do mesmo provider cobrem checks declarativos (Inferido: confira se os campos de partição são templated na sua versão).
- Retries com backoff e `max_active_runs=1` evitam tempestade de reexecuções na origem.

## 3. Teste de import e de forma

Execute somente depois que o topo dos arquivos deixou de acessar rede ou banco, porque importar roda o código do módulo.

```python
# tests/test_dags.py  (pytest; DagBag existe nas versões 2 e 3, confira o caminho de import)
from airflow.models import DagBag


def _bag():
    return DagBag(dag_folder="dags", include_examples=False)


def test_importa_sem_erro():
    assert _bag().import_errors == {}


def test_orders_daily_forma():
    dag = _bag().get_dag("orders_daily")
    assert dag is not None
    assert dag.catchup is False and dag.max_active_runs == 1
    assert all(t.retries >= 1 for t in dag.tasks)
```
Também serve `airflow dags list-import-errors` (CLI). Nenhum dos dois executa tarefas. `airflow dags test` e `airflow tasks test` executam tarefas e gravam dados: só com consentimento, em dev.

## 4. Variações para Airflow 2

Pontos a conferir (Inferido): `from airflow.decorators import dag, task` em vez de `airflow.sdk`; `schedule=` substitui `schedule_interval=` desde o 2.4; `Dataset` em vez de `Asset`; SubDAG ainda existe mas é desencorajado (TaskGroup); `execution_date` ainda existe como alias, prefira `data_interval_start`/`end` e `logical_date`; `PythonOperator` e `BashOperator` vêm do core.

## 5. Relatório de depuração (exemplo ilustrativo, dados fictícios)

```text
Sintoma: run 2026-10-08 de orders_daily falhou em carregar_intervalo; checar_* ficaram upstream_failed
Classificação: dependência (provável)
Evidência: log, última exceção: "ModuleNotFoundError: No module named 'x'" (Verificado no log fornecido)
           run verde 2026-10-07 usava imagem 2.9.3-py3.11; a de 08/10 usa tag "latest" (Verificado nos dois logs de cabeçalho)
Causa provável: drift de imagem por tag latest (Inferido; falta o diff de requirements)
Correção mínima (não aplicada): fixar a versão da imagem e do pacote; reconstruir
Impacto: mart.orders sem dados do dia 08; dashboards "Vendas D-1" defasados (Suposição, sem acesso ao BI)
Prevenção: pin de imagem, check de contagem do dia, alerta de falha
Não verificado: nenhuma reexecução foi feita; peça autorização para reexecutar em dev
```
O foco em `upstream_failed` é a tarefa raiz (`carregar_intervalo`), não os checks.

## 6. Plano de backfill (exemplo ilustrativo)

```text
Objetivo: reprocessar mart.orders de 2024-01-01 a 2024-06-30 após correção da regra de desconto
Idempotência: MERGE por order_id por intervalo diário (segunda execução não muda contagem)
Custo: estimativa de bytes por dia via dry_run = <preencher>; total = dias x estimativa
Ensaio em dev: 3 dias (2024-01-01..03), comparar contagem e soma de amount com a origem
Concorrência: max_active_runs=2, pool "warehouse" com 4 slots; janela fora do horário de pico
Pós-carga: contagem por dia origem vs destino; unicidade de order_id; soma de amount
Rollback: restaurar a partir do snapshot/time travel do warehouse (conferir retenção)
Aprovação humana: <nome> aprova antes de qualquer execução
Execução: feita pelo usuário (comando do orquestrador da versão instalada); este plano não executa
```

## 7. Dagster: asset particionado (Inferido; páginas de asset checks e partições não foram lidas)

```python
import dagster as dg

diaria = dg.DailyPartitionsDefinition(start_date="2024-01-01")


@dg.asset(partitions_def=diaria, deps=["raw_orders"], code_version="2")
def orders_mart(context: dg.AssetExecutionContext) -> None:
    inicio, fim = context.partition_time_window   # janela explícita; nunca "agora"
    # MERGE por chave limitado a [inicio, fim) via recurso de warehouse do projeto
```
Sequência de verificação (V-15): `dg check`, `dg list defs`, `dg launch` local do asset alterado, só então o ambiente publicado. Todo asset idempotente; acrescente um asset check de frescor e de contagem. Os comandos e a API mudam por versão; `dg launch`, `dg api` e `dg plus` alteram estado e exigem autorização.
