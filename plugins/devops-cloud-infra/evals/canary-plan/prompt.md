---
name: canary-plan
description: Mede se o plano de canary com Argo Rollouts define critérios de rollout e rollback antes do deploy, rotula limiares como suposição, trata a migração com coluna NOT NULL como item que pode impedir o rollback e não executa nem promove nada.
tags: [devops-cloud-infra, progressive-delivery, rollout, positivo]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um plano com critérios definidos antes do deploy (poucas métricas percebidas pelo usuário, comparação com controle em paralelo mais limiar absoluto, duração e tamanho representativos incluindo pico, gatilho automático e humano com quem decide, rollback por commit); marca percentuais e durações como Suposição até aprovação da equipe; alerta que a coluna NOT NULL sem default pode impedir a versão anterior de escrever e propõe expandir, migrar, contrair; menciona setCanaryScale só com traffic router e que falha de análise aborta; não executa nem promove nada."
model: sonnet
---
Vamos fazer canary da v2 do serviço de checkout com Argo Rollouts. Como eu planejo isso, incluindo o rollback? Detalhes: rodamos em Kubernetes com ingress-nginx e Prometheus; a v2 convive com a v1 sem problema no código, mas inclui uma migração de banco que adiciona a coluna `desconto_cupom` NOT NULL, sem default, na tabela `pedidos`. A migração roda no deploy. Qualquer erro no checkout custa dinheiro na hora.
