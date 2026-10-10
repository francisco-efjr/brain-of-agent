---
name: revisao-plano-design
description: Mede se o plugin faz desafio de escopo, apresenta decisões D-n com opções e dono humano, e revisa sem implementar quando o plano é desproporcional ao problema.
tags: [architecture-design, design-review, scope]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Desafia o escopo, aponta a falta de requisito que justifique cada peça, entrega decisões D-n com 2 a 4 opções incluindo não mudar nada, tabela de pendências com dono, e não escreve arquivos."
model: sonnet
---
Vamos começar a implementar na segunda. Podem revisar o plano abaixo antes de a gente codar?

Plano: cadastro de clientes internos. Hoje é uma tabela `customers` no Postgres do ERP, com cerca de 50 usuários internos e uns 30 cadastros ou alterações por dia.

1. Criar o serviço `customer-command-service` (Node) para receber os comandos de criar e alterar cliente.
2. Criar o serviço `customer-query-service` (Node) com banco de leitura em MongoDB.
3. Criar o serviço `customer-projection-service`, que consome eventos e atualiza o MongoDB.
4. Adotar event sourcing: o estado do cliente passa a ser reconstruído a partir de eventos no Kafka (tópico `customer-events`, retenção infinita).
5. Subir um cluster Kafka com 3 brokers e Schema Registry em Kubernetes. O time de plataforma ainda não opera Kafka.
6. Migrar os 120 mil clientes atuais gerando um evento `CustomerImported` por registro.
7. Expor tudo por GraphQL federado, por meio de um gateway novo.
8. Meta declarada: "ficar pronto para escalar para 10 milhões de clientes".

Prazo: 6 semanas. Time: 3 devs, só 1 com experiência em Kafka. Critério de pronto: todos os serviços no ar em produção.
