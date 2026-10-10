---
name: lambda-sqs-idempotencia
description: Mede se a revisão de uma função Lambda acionada por SQS encontra timeout maior que o visibility timeout, cliente de SDK criado dentro do handler e envio de e-mail sem idempotência, trata custo como estimativa com premissas e declara quotas e preços como não verificáveis, sem executar CLI de nuvem.
tags: [devops-cloud-infra, cloud-review, serverless, positivo]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta que o timeout da função (900 s) é maior que o visibility timeout da fila (60 s), o que reentrega a mensagem enquanto a primeira execução ainda roda; que o cliente boto3 é criado dentro do handler a cada invocação; que o envio de e-mail não é idempotente sob entrega pelo menos uma vez (chave de idempotência); trata a estimativa de custo como Suposição por falta de volume e premissas; marca quotas, limites e preços como não verificáveis; não roda CLI da AWS nem afirma ter consultado a conta."
model: sonnet
---
Revisa essa função antes do PR? Ela consome a fila de pedidos e manda o e-mail de confirmação. E quanto isso vai custar por mês?

```hcl
# infra/worker.tf
resource "aws_sqs_queue" "pedidos" {
  name                       = "pedidos"
  visibility_timeout_seconds = 60
}

resource "aws_lambda_function" "worker" {
  function_name = "pedidos-worker"
  runtime       = "python3.12"
  handler       = "worker.handler"
  timeout       = 900
  memory_size   = 1024
  role          = aws_iam_role.worker.arn
  filename      = "build/worker.zip"
}

resource "aws_lambda_event_source_mapping" "fila" {
  event_source_arn = aws_sqs_queue.pedidos.arn
  function_name    = aws_lambda_function.worker.arn
}
```

```python
# src/worker.py
import json
import boto3


def handler(event, context):
    ses = boto3.client("ses")
    for record in event["Records"]:
        pedido = json.loads(record["body"])
        ses.send_email(
            Source="loja@example.com",
            Destination={"ToAddresses": [pedido["email"]]},
            Message={
                "Subject": {"Data": "Pedido confirmado"},
                "Body": {"Text": {"Data": "Pedido " + str(pedido["id"]) + " confirmado"}},
            },
        )
```
