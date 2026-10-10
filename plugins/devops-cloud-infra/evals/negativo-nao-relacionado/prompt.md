---
name: negativo-nao-relacionado
description: Caso negativo que mede sobredisparo, verificando que um pedido sem relação com infraestrutura (função Python de validação de CPF com testes) não aciona nenhuma skill do plugin devops-cloud-infra nem produz conversa de Terraform, Kubernetes ou deploy.
tags: [devops-cloud-infra, negativo, sobredisparo]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega a função de validação de CPF em Python com testes (dígitos verificadores, rejeição de sequências repetidas, formatação com e sem pontuação) sem acionar skills do plugin devops-cloud-infra e sem mencionar Terraform, Kubernetes, CI ou deploy."
model: sonnet
---
Escreve uma função em Python que valida um CPF, com testes. Pode usar pytest.
