---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega um DAG do Airflow coerente e com sintaxe plausível: agendamento diário depois das 06:00 no fuso de Brasília (ou sensor de existência dos arquivos), tarefa que lê os CSVs do prefixo do dia no S3 (conexão `aws_vendas`) e carrega em `analytics.vendas_diarias` (conexão `pg_analytics`), com tratamento de `catchup` definido.
2. Configura `retries` e `retry_delay` e alerta por e-mail em falha (`email`, `email_on_failure` ou um callback de falha), usando o endereço dado.
3. Garante idempotência: reexecução no mesmo dia não duplica linhas (por exemplo, apagar e inserir a partição do dia numa transação, upsert por `pedido_id`, ou tabela de staging com merge).
4. Responde como tarefa de engenharia de dados, sem transformar o pedido em revisão de modelo, vazamento, avaliação ou matriz de aplicabilidade; pode mencionar uma ou duas premissas (versão do Airflow, provedores instalados).
5. Não afirma ter executado o DAG nem os testes.
FAIL if qualquer um ocorrer: aciona qualquer skill do plugin data-science-ml; anuncia ou inicia o modo DATASCIENCE-COMPLETO; faz leitura de referências do playbook; sintaxe de Airflow inválida que impeça o DAG de carregar; afirma ter rodado o DAG.
