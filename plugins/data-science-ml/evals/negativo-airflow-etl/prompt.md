---
name: negativo-airflow-etl
description: Caso negativo de fronteira. Pedido de engenharia de dados (DAG do Airflow que carrega CSVs do S3 para o Postgres) com vocabulário que lembra dados. Mede se nenhuma skill do plugin de ciência de dados dispara, nenhuma referência do playbook é lida e o pedido é respondido como tarefa de ETL.
tags: [data-science-ml, negative, data-engineering, scope]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um DAG do Airflow diário com carga do S3 para o Postgres, retries, alerta por e-mail em falha e carga idempotente, sem acionar nenhuma skill do plugin de ciência de dados, sem ler as referências do playbook e sem transformar o pedido em auditoria de modelo."
model: sonnet
---
Preciso de um DAG do Airflow que carregue todo dia os CSVs de vendas do S3 para o Postgres, com retry e alerta por e-mail se falhar.

Detalhes: os arquivos chegam em `s3://vendas-bruto/AAAA/MM/DD/*.csv` até as 06:00 (horário de Brasília), com as colunas `pedido_id, loja_id, data_pedido, valor, status`. A tabela de destino é `analytics.vendas_diarias` no Postgres (conexão `pg_analytics`; a conexão do S3 é `aws_vendas`). Se o job rodar duas vezes no mesmo dia, não pode duplicar linhas. Equipe de dados: dados@empresa.example.test.
