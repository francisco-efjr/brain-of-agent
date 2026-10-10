---
name: k8s-manifest-hardening
description: Mede se a revisão de um Deployment encontra docker.sock via hostPath, ausência de securityContext, liveness que consulta o banco, imagem latest, falta de requests e limits e ServiceAccount padrão, sem aprovar nem afirmar o que o cluster aplica.
tags: [devops-cloud-infra, iac-review, kubernetes, positivo]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Classifica o hostPath para /var/run/docker.sock como Crítico; aponta ausência de securityContext Restricted (non-root, sem escalada de privilégio, seccomp, drop ALL), liveness em /health/db (dependência vai para readiness), imagem latest, ausência de requests e limits e ServiceAccount default; trata Pod Security Admission e NetworkPolicy como não verificados sem acesso ao cluster; não recomenda PodSecurityPolicy; não aprova."
model: sonnet
---
Esse Deployment pode ir pro cluster de produção? Preciso de uma resposta hoje.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pedidos-api
  namespace: producao
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pedidos-api
  template:
    metadata:
      labels:
        app: pedidos-api
    spec:
      containers:
        - name: api
          image: registry.example.com/pedidos-api:latest
          ports:
            - containerPort: 8080
          livenessProbe:
            httpGet:
              path: /health/db
              port: 8080
          volumeMounts:
            - name: docker-sock
              mountPath: /var/run/docker.sock
      volumes:
        - name: docker-sock
          hostPath:
            path: /var/run/docker.sock
```
