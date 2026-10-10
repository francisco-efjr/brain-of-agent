---
name: negativo-deploy-aws
description: "Caso negativo de fronteira com outro segmento: pedido de workflow de GitHub Actions para deploy na AWS (ECS Fargate) com autenticação sem chaves de longa duração. É tema de devops, não de git, colaboração ou release; nenhuma skill do plugin deve ser acionada, em especial release-cut."
tags: [git-workflow-release, negative, near-miss, devops]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Responde diretamente com a abordagem de deploy (OIDC com role-to-assume em vez de chave de acesso nos secrets, permissões id-token write e contents read, passos de build, push ao ECR e atualização do serviço ECS) ou indica que o tema é de infraestrutura e pipeline, sem acionar nenhuma skill do plugin."
model: sonnet
---
Preciso de um workflow do GitHub Actions que faça deploy da minha API Node.js na AWS (ECS Fargate) quando eu fizer push na `main`. Já tenho o `Dockerfile` e um repositório no ECR chamado `pedidos-api`, na região `sa-east-1`. Como configuro a autenticação com a AWS sem guardar chave de acesso nos secrets do GitHub?
