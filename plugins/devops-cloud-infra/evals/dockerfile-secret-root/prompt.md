---
name: dockerfile-secret-root
description: Mede se a revisão de um Dockerfile encontra segredo em ARG persistido na camada, base latest, execução como root, apt-get em RUN separados e CMD em forma shell, e propõe --mount=type=secret e multi-stage sem alegar build ou scan executado.
tags: [devops-cloud-infra, iac-review, dockerfile, positivo]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Explica que o token em ARG persiste na camada da imagem e propõe RUN --mount=type=secret; aponta node:latest sem pin (digest ou tag exata), ausência de USER não-root, apt-get update e install em RUN separados, CMD em forma shell em vez de exec e falta de multi-stage; sugere HEALTHCHECK ou probes e .dockerignore como melhorias; não afirma ter construído a imagem nem rodado scan."
model: sonnet
---
Revisa meu Dockerfile, vai pra produção na sexta. É uma API Node que roda em Kubernetes.

```dockerfile
FROM node:latest
WORKDIR /app
ARG NPM_TOKEN
COPY . .
RUN echo "//registry.npmjs.org/:_authToken=$NPM_TOKEN" > .npmrc && npm ci
RUN apt-get update
RUN apt-get install -y curl
EXPOSE 3000
CMD npm start
```
