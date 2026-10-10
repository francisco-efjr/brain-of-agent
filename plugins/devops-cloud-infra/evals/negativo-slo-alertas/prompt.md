---
name: negativo-slo-alertas
description: Caso negativo de quase-acerto que mede sobredisparo, verificando que um pedido de SLO e alertas de latência (domínio de observabilidade, não de infraestrutura) não aciona as skills de revisão, entrega ou diagnóstico de infra do plugin devops-cloud-infra.
tags: [devops-cloud-infra, negativo, sobredisparo, quase-acerto]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Responde com definição de SLI e SLO do checkout (indicador do usuário, janela, denominador), orçamento de erro e alertas baseados em consumo do orçamento, sem acionar skills de revisão de IaC, pipeline, Helm/GitOps, segredos, rollout, nuvem ou diagnóstico do plugin devops-cloud-infra, sem revisar Terraform, Kubernetes ou CI e sem ativar o modo completo."
model: sonnet
---
Preciso definir SLOs e alertas para o serviço de checkout. Hoje só temos um alerta de CPU alta. Temos Prometheus e Alertmanager, uns 400 pedidos por minuto no pico, e o time já viu cliente reclamar de lentidão sem nenhum alerta disparar. Como eu defino o SLI e o SLO de latência e de erro, e que alertas faz sentido criar?
