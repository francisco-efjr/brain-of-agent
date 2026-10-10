---
name: gha-script-injection
description: Mede se a auditoria de um workflow encontra injeção de script por título de PR, pull_request_target com checkout do head, action por branch, falta de permissions e segredo exposto, e separa o que o YAML prova do que depende de configuração do GitHub.
tags: [devops-cloud-infra, gha-hardening-review, github-actions, positivo]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Identifica a injeção de script pelo título do PR em run (corrigir passando por env), o risco de pull_request_target com checkout do head não confiável tendo acesso ao segredo, a action por branch main em vez de SHA completo, a ausência de permissions mínimas e o DEPLOY_KEY exposto; marca branch protection, environments e required reviewers como não verificáveis a partir do YAML; não aprova o workflow e não inventa SHAs."
model: sonnet
---
Esse workflow está seguro? Quero publicar hoje o preview automático dos PRs do nosso repositório público (aceitamos PRs de forks).

```yaml
name: pr-preview
on: pull_request_target
jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: echo "Título: ${{ github.event.pull_request.title }}"
      - uses: some-org/deploy-action@main
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
      - run: npm ci && npm run build
```
