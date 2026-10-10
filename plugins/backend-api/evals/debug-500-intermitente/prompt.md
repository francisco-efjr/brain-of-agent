---
name: debug-500-intermitente
description: Mede se o plugin segue depuração por causa raiz diante de 500 intermitente sob carga, identifica engine e pool criados por requisição, desfaz patches de sintoma, propõe teste de regressão e declara o que não reproduziu.
tags: [backend-api, backend-debugging]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Investiga antes de corrigir, formula a hipótese de engine/pool por requisição e conexões não devolvidas, propõe engine único com pool limitado e sessão fechada por dependência, reverte os patches de sintoma, descreve teste de regressão, declara não reproduzido e cita a parada após três correções falhas."
model: sonnet
---
Tenho 500 intermitente em `GET /reports`, só sob carga (acontece nos horários de pico). Já tentei duas coisas: aumentei o timeout do proxy de 30 para 120 segundos e depois envolvi todo o handler em `try/except Exception`. Piorou: agora a API demora mais e ainda dá erro. Log:

```text
psycopg2.OperationalError: FATAL:  remaining connection slots are reserved for non-replication superuser connections
```

Código (FastAPI + SQLAlchemy + Postgres):

```python
def get_db():
    return create_engine(DB_URL).connect()

@app.get("/reports")
def reports(db=Depends(get_db)):
    try:
        return db.execute(text("select * from report_rows limit 5000")).mappings().all()
    except Exception:
        return []
```

Resolva. Não tenho acesso ao servidor agora; trabalhe só com o que escrevi.
