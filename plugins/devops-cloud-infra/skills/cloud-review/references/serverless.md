# Serverless: Lambda, Azure Functions e Cloud Run

Base: V-48 (AWS Lambda, classe A), V-49 (Azure Functions, classe A, `ms.date` 2026-09-15), V-50 (Cloud Run, classe B, sem SIGTERM nem segredos), P-18 (nota 75, reforçado aqui com exemplo anotado). Conferido em 2026-10-10. Destilação com redação própria. **Limitação:** três nuvens, fontes de qualidade diferente, e nenhuma quota ou limite de plano foi verificada na conta. Números de exemplo vindos das páginas (como "30 s" de IteratorAge) são exemplos da documentação, não normas.

## Sumário

- [AWS Lambda (LM-nn)](#aws-lambda-lm-nn)
- [Exemplo anotado: worker de fila](#exemplo-anotado-worker-de-fila)
- [Azure Functions (AZ-nn)](#azure-functions-az-nn)
- [Cloud Run (CR-nn)](#cloud-run-cr-nn)

## AWS Lambda (LM-nn)

| ID | Verificar | Detectar | Sev. |
| --- | --- | --- | --- |
| LM-01 | clientes e conexões (SDK, banco) criados **fora** do handler, para reutilizar o ambiente de execução; cache em `/tmp` sem dado de usuário | `boto3.client(`/`new S3Client(` dentro da função | Médio |
| LM-02 | idempotência: event source mappings processam pelo menos uma vez; efeitos externos (e-mail, cobrança) protegidos por chave de deduplicação | `send_`, `charge`, `publish` sem checagem | Alto |
| LM-03 | `timeout` esperado da função não excede o `visibility timeout` da fila SQS | `timeout` vs. `visibility_timeout_seconds` | Alto |
| LM-04 | retries com backoff e jitter; partial batch response em filas e streams para não reprocessar o lote inteiro | `function_response_types`, retorno do handler | Alto |
| LM-05 | concorrência reservada decidida; `0` funciona como parada de emergência contra recursão; evitar função que invoca a si mesma por trigger | `reserved_concurrent_executions` | Médio |
| LM-06 | IAM mínimo: sem `*` em ação nem em recurso | `aws_iam_role_policy`, `aws_iam_policy_document` | Crítico se `*:*` |
| LM-07 | alarmes do CloudWatch (erros, duração, throttles; `IteratorAge` em streams) em vez de métricas calculadas no código; EMF para métricas customizadas; logs em JSON | `aws_cloudwatch_metric_alarm` | Médio |
| LM-08 | memória testada (AWS Lambda Power Tuning) e teste de carga para definir o `timeout`; variáveis de ambiente para configuração; sem APIs não documentadas | leitura | Baixo |
| LM-09 | provisioned concurrency tem custo contínuo: decidir com dado de cold start | `provisioned_concurrent_executions` | Médio |
| LM-10 | Cost Anomaly Detection ligado (alertas podem atrasar até 24 h); Security Hub CSPM e GuardDuty Lambda Protection considerados | Não verificável pelo repositório | Médio |
| LM-11 | janela de batching (até 5 minutos) e tamanho de lote coerentes com o timeout; em Kinesis, shards e paralelismo por shard | `maximum_batching_window_in_seconds`, `parallelization_factor` | Médio |
| LM-12 | dead-letter queue / destino de falha configurado para filas (Inferido: conhecimento estável) | `redrive_policy`, `dead_letter_config` | Alto |

Sobre LM-03: a documentação consultada exige que o timeout esperado não passe do visibility timeout. A orientação da AWS para o mapeamento SQS costuma pedir uma margem bem maior (um múltiplo do timeout da função); isso não está em V: confira na página de event source mapping de SQS (Inferido).

## Exemplo anotado: worker de fila

Entrada (didática; arquivo `src/worker.py`):

```python
import json
import boto3

from mailer import send_email


def handler(event, context):
    s3 = boto3.client("s3")
    for record in event["Records"]:
        body = json.loads(record["body"])
        s3.put_object(Bucket="relatorios", Key=f"{body['id']}.json", Body=json.dumps(body))
        send_email(body["email"], "Seu relatório está pronto")
    return {"ok": True}
```

Entrada (`infra/main.tf`):

```hcl
resource "aws_sqs_queue" "relatorios" {
  name                       = "relatorios"
  visibility_timeout_seconds = 30
}

resource "aws_lambda_function" "worker" {
  function_name = "relatorios-worker"
  handler       = "worker.handler"
  runtime       = "python3.13"
  timeout       = 300
  role          = aws_iam_role.worker.arn
  filename      = "build/worker.zip"
}

resource "aws_lambda_event_source_mapping" "fila" {
  event_source_arn = aws_sqs_queue.relatorios.arn
  function_name    = aws_lambda_function.worker.arn
  batch_size       = 10
}
```

Achados esperados:

| ID | Sev. | Local | Evidência | Correção | Rótulo |
| --- | --- | --- | --- | --- | --- |
| LM-01 | Médio | worker.py:8 | `boto3.client("s3")` dentro do handler: nova conexão a cada invocação | mover para escopo de módulo | Verificado (V-48) |
| LM-02 | Alto | worker.py:12 | `send_email` sem checagem: mensagem reentregue manda e-mail repetido | gravação condicional de uma chave por `id` (por exemplo, DynamoDB com `attribute_not_exists`) antes ou depois do envio; decidir se a falha entre as etapas prefere perder ou duplicar | Verificado (V-48: pelo menos uma vez) |
| LM-03 | Alto | main.tf:10 e main.tf:3 | `timeout = 300` maior que `visibility_timeout_seconds = 30`: a mensagem volta à fila enquanto a primeira execução ainda roda | `visibility_timeout_seconds` ≥ timeout, com margem | Verificado (V-48); margem: Inferido |
| LM-04 | Alto | worker.py:9-13, main.tf:15-19 | uma exceção num registro reprocessa o lote de 10, incluindo e-mails já enviados; o retorno `{"ok": True}` não informa falhas parciais | `function_response_types = ["ReportBatchItemFailures"]` no mapeamento e retorno `{"batchItemFailures": [...]}` | Verificado (V-48: partial batch response) |
| LM-12 | Alto | main.tf:1-4 | fila sem DLQ: mensagem venenosa recircula até expirar | `redrive_policy` com DLQ e `maxReceiveCount` | Inferido |
| LM-07 | Médio | (ausente) | sem alarmes de erro, duração e idade da fila; sem logs estruturados | `aws_cloudwatch_metric_alarm`; logs JSON | Verificado (ausência no trecho) |
| LM-05 | Médio | main.tf:6-13 | sem decisão de concorrência reservada | decidir e registrar (0 = parada de emergência) | Verificado |
| LM-06 | — | main.tf:11 | papel `aws_iam_role.worker` não foi recebido | pedir o arquivo | Não verificável |

Versão corrigida do código:

```python
import json
import boto3

from mailer import send_email

s3 = boto3.client("s3")  # fora do handler: reaproveitado entre invocações


def handler(event, context):
    falhas = []
    for record in event["Records"]:
        try:
            body = json.loads(record["body"])
            s3.put_object(Bucket="relatorios", Key=f"{body['id']}.json", Body=json.dumps(body))
            if reservar_envio(body["id"]):          # gravação condicional; False se já reservado
                send_email(body["email"], "Seu relatório está pronto")
        except Exception:
            falhas.append({"itemIdentifier": record["messageId"]})
    return {"batchItemFailures": falhas}
```

`reservar_envio` é função do projeto (por exemplo, `PutItem` condicional); não é biblioteca. O exemplo mostra a forma, não substitui o desenho da deduplicação.

## Azure Functions (AZ-nn)

| ID | Verificar | Sev. |
| --- | --- | --- |
| AZ-01 | plano de hospedagem escolhido no início (a troca é limitada, sobretudo entre Consumption e Elastic Premium); Flex Consumption quando possível | Médio |
| AZ-02 | storage account na mesma região e **separada por function app** (não compartilhada entre apps); Event Hubs sem Data Lake no mesmo storage | Alto |
| AZ-03 | run from package no deploy | Médio |
| AZ-04 | slots de implantação (ou rolling updates no Flex) para trocas sem indisponibilidade | Médio |
| AZ-05 | funções stateless, sem execuções longas; padrão de retry; teste de integração no pipeline | Médio |
| AZ-06 | `FUNCTIONS_WORKER_PROCESS_COUNT` (padrão 1) decidido com teste de carga | Baixo |
| AZ-07 | cold start tratado por plano: always ready no Flex, warmup trigger no Premium, duas instâncias e Health Check no Dedicated | Médio |
| AZ-08 | Application Insights com amostragem revisada (`excludedTypes`) para não perder falhas | Médio |
| AZ-09 | multirregião para o que é crítico | Informativo |

Amostragem preservando requests e exceções (`host.json`; conferir a sintaxe na versão do runtime):

```json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request;Exception"
      }
    }
  }
}
```

## Cloud Run (CR-nn)

Fonte classe B (V-50). **Não cobre** SIGTERM (encerramento) nem gestão de segredos: marque qualquer afirmação sobre isso como Inferido ou Não verificado.

| ID | Verificar | Sev. |
| --- | --- | --- |
| CR-01 | concorrência por instância (padrão 80) testada com a carga real; o código aguenta requisições simultâneas | Alto |
| CR-02 | o disco local é memória: arquivos temporários consomem a memória da instância | Médio |
| CR-03 | com cobrança por requisição, a CPU após a resposta é limitada: trabalho em background exige cobrança por instância | Alto |
| CR-04 | contêiner com usuário não-root | Alto |
| CR-05 | startup CPU boost e instâncias mínimas contra cold start, com ciência do custo | Médio |
| CR-06 | objetos caros em escopo global são úteis, mas sem garantia de reuso (a instância pode ser descartada) | Baixo |
| CR-07 | encerramento limpo (SIGTERM) e segredos: fora da fonte lida | Não verificado |

Os nomes das configurações no `gcloud` ou no Terraform (por exemplo, `--concurrency`, `--cpu-boost`, `--min-instances`, `--no-cpu-throttling`) são conhecimento estável (Inferido, não lidos em V): confirme na documentação do provider e do `gcloud run deploy --help`. Você não roda `gcloud` contra a conta.
