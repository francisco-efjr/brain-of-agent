---
name: flink-kafka-elasticsearch-exactly-once
description: "Mede se o plugin desmonta a afirmação de exactly-once ponta a ponta de um job Flink de Kafka para Elasticsearch, montando a tabela fonte, estado e sink, exigindo escrita idempotente e teste de reinício, e rotulando como não verificado o que depende da versão."
tags: [data-engineering, spark-streaming-review, streaming, flink, delivery-guarantees]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Monta a tabela fonte, estado e sink; Kafka como fonte é exactly-once e Elasticsearch como sink é at-least-once; exige escrita idempotente com id determinístico e teste de reinício com checagem de duplicidade; pede a versão do Flink e o conector e rotula como não verificado o que depende da versão."
model: sonnet
---
Temos um job Flink que lê de um tópico Kafka e grava num índice do Elasticsearch. O time diz que é exactly-once "porque o Flink faz checkpoint". Como eu confirmo isso de verdade e o que ajusto se não for?
