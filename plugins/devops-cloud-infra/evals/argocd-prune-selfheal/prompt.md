---
name: argocd-prune-selfheal
description: Mede se a revisão de uma Application do Argo CD de produção discute prune e selfHeal por ambiente, rollback por commit, Secret em claro no repositório, config no mesmo repo do código e base de kustomize sem ref, sem executar sync nem inventar padrões do Flux ou do Argo.
tags: [devops-cloud-infra, helm-gitops-review, gitops, argocd, positivo]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Discute prune e selfHeal automáticos em produção (apaga e reverte sem clique, decidir por ambiente), diz que o rollback é novo commit e que com sync automático a UI bloqueia rollback, aponta o Secret com senha em claro no repositório (criar no cluster de destino com ESO, Sealed Secrets ou CSI; recomendar rotação), a config no mesmo repositório do código, targetRevision HEAD e a base de kustomize sem ?ref=; não manda sincronizar e não cita default do interval do Flux nem afirma que o sync automático é desligado por padrão como citação."
model: sonnet
---
Revisa essa Application do Argo CD de produção, por favor. Já está tudo no repositório da loja.

```yaml
# deploy/prod/application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: loja-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/acme/loja.git
    targetRevision: HEAD
    path: deploy/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: loja
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

```yaml
# deploy/prod/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: loja-db
type: Opaque
stringData:
  password: "troque-esta-senha-123"
```

```yaml
# deploy/prod/kustomization.yaml
resources:
  - github.com/acme/base-platform
  - secret.yaml
```

O repositório acme/loja.git é o mesmo onde fica o código da aplicação.
