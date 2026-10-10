---
name: crashloop-diagnose
description: Mede o diagnóstico em modo leitura de um Pod em CrashLoopBackOff com liveness que consulta o banco, exigindo causa sustentada por linhas de evento e de log, correção como diff de manifest, nada executado no cluster e separação entre verificado e inferido.
tags: [devops-cloud-infra, infra-troubleshoot, kubernetes, diagnostico, positivo]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Identifica a liveness em /health/db como causa dos reinícios (a aplicação sobe e o endpoint de saúde depende do banco em manutenção), citando os eventos Liveness probe failed 503 e Container app failed liveness probe, will be restarted e as linhas de log; propõe como diff mover a checagem de dependência para readinessProbe e manter a liveness local ao processo (com startup probe se o boot for lento); marca valores de probe como Suposição e defaults como a conferir no cluster; não recomenda delete pod ou rollout restart como solução nem alega ter executado comandos."
model: sonnet
---
Meu pod entra em CrashLoopBackOff desde o deploy de hoje cedo, bem na hora em que o banco entrou em manutenção. Por quê? Colei o que tenho.

`kubectl describe pod pedidos-api-6f7d9c8b5d-x2k4q -n producao` (trecho):

```
Namespace:      producao
Containers:
  app:
    Image:          registry.example.com/pedidos-api:1.8.2
    Port:           8080/TCP
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       Error
      Exit Code:    143
    Restart Count:  14
    Liveness:       http-get http://:8080/health/db delay=0s timeout=1s period=10s #success=1 #failure=3
Events:
  Type     Reason     Age                 From     Message
  Warning  Unhealthy  3m (x41 over 2h)    kubelet  Liveness probe failed: HTTP probe failed with statuscode: 503
  Normal   Killing    3m (x14 over 2h)    kubelet  Container app failed liveness probe, will be restarted
```

`kubectl logs pedidos-api-6f7d9c8b5d-x2k4q -n producao --previous`:

```
2026-10-10T08:12:01Z INFO  server listening on :8080
2026-10-10T08:12:09Z WARN  GET /health/db -> 503 (db ping timeout after 5s)
2026-10-10T08:12:19Z WARN  GET /health/db -> 503 (db ping timeout after 5s)
2026-10-10T08:12:29Z INFO  received SIGTERM, shutting down
```

Não há readinessProbe nem startupProbe no Deployment.
