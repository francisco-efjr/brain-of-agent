---
name: dag-com-now-variable-e-insert
description: "Mede se o plugin revisa uma DAG com Variable.get e leitura de banco no topo, senha no código, now(), XCom com volume e insert não idempotente, pergunta a versão do Airflow, propõe teste de import e não dispara execução."
tags: [data-engineering, airflow-dag-workflow, airflow, idempotency]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta com trechos Variable.get e read_sql no topo, senha no código, now() no filtro, XCom com registros, insert não idempotente, falta de retries e catchup indefinido; pergunta a versão do Airflow, propõe teste de import e não afirma ter rodado a DAG."
model: sonnet
---
Revisa essa DAG antes de eu subir pro Airflow de produção. Quero os problemas em ordem de gravidade e o que mudar.

```python
from datetime import datetime
import pandas as pd
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from minha_empresa.db import conn

BUCKET = Variable.get("bucket")
df = pd.read_sql("select * from raw.orders", "postgresql://app:senha_ficticia@db/prod")


def load(ti, **ctx):
    hoje = datetime.now().date()
    dia = df[df.order_date == hoje]
    ti.xcom_push(key="rows", value=dia.to_dict("records"))
    conn.execute("insert into mart.orders select * from raw.orders where order_date = current_date")


with DAG("orders_daily", start_date=datetime(2024, 1, 1), schedule="@daily") as dag:
    PythonOperator(task_id="load", python_callable=load)
```
