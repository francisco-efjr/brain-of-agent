# Containers em tempo de execução e manifests Kubernetes: checklist rápido

Conferido em 2026-10-10 (V-20 OWASP Docker, V-21 Pod Security Standards, V-42 RBAC e Secrets, V-56 NetworkPolicy, V-57 adoção do PSA, V-58 probes e limits). O guia completo de Kubernetes, Helm e RBAC está em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/containers-k8s-helm.md`; este arquivo traz o específico para revisão de arquivo. Para auditoria detalhada de workloads delegue ao agente `k8s-workload-auditor`.

## docker run e docker-compose (CT-nn)

| ID | Verificar | Detectar | Sev. | Fonte |
| --- | --- | --- | --- | --- |
| CT-01 | sem `privileged: true` / `--privileged` | Grep | Crítico | V-20 |
| CT-02 | sem montar `/var/run/docker.sock`, nem somente leitura (dá controle do host) | `docker.sock` | Crítico | V-20 |
| CT-03 | usuário não-root (`user:`) | ausência de `user` e de `USER` na imagem | Alto | V-20 |
| CT-04 | sistema de arquivos somente leitura + `tmpfs` onde precisar escrever | `read_only`, `tmpfs` | Médio | V-20 |
| CT-05 | `cap_drop: [ALL]` e `cap_add` pontual | `cap_drop`, `cap_add` | Alto | V-20 |
| CT-06 | `security_opt: ["no-new-privileges:true"]` | Grep | Médio | V-20 |
| CT-07 | limites de memória, CPU e processos | `mem_limit`, `cpus`, `pids_limit` | Médio | V-20 |
| CT-08 | portas publicadas só no necessário e em `127.0.0.1` quando for local | `ports:` com `0.0.0.0` ou sem host | Médio | Inferido |
| CT-09 | segredos por Docker/Compose secrets ou ambiente injetado, não por valor em `environment:` do arquivo versionado | `environment:` com `PASSWORD=` | Crítico | V-20 (regra 12), V-55 |
| CT-10 | scanner de imagem no CI (Trivy, Grype ou Clair citados pela OWASP) | workflows | Médio | V-20 |

Exemplo conforme (Compose):

```yaml
services:
  api:
    image: registry.example.com/api@sha256:<digest-real>
    user: "10001:10001"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    mem_limit: 512m
    pids_limit: 200
    ports:
      - "127.0.0.1:8080:8080"
    secrets:
      - db_password
secrets:
  db_password:
    file: ./secrets/db_password.txt   # fora do Git (.gitignore); em produção, secret manager
```

## Manifests Kubernetes puros (K8-nn)

| ID | Verificar | Sev. | Fonte |
| --- | --- | --- | --- |
| K8-01 | Restricted: `allowPrivilegeEscalation: false`, `runAsNonRoot: true`, `runAsUser` diferente de 0, `seccompProfile.type: RuntimeDefault` (ou `Localhost`), `capabilities.drop` com `ALL` (e `add` só `NET_BIND_SERVICE`) | Alto | V-21 (tabela lida) |
| K8-02 | sem `privileged`, `hostPath`, `hostNetwork`, `hostPID`, `hostIPC` | Crítico | V-21 |
| K8-03 | `requests` e `limits` de CPU e memória; limite de CPU causa throttling, limite de memória pode causar OOM kill; `limit` sem `request` copia o limit como request | Médio | V-58 |
| K8-04 | `livenessProbe` simples e local ao processo; dependências (banco) só na `readinessProbe`; `startupProbe` para app lento (tempo máximo = `failureThreshold` x `periodSeconds`) | Médio | V-58 |
| K8-05 | imagem por tag fixa ou digest, nunca `latest` | Alto | V-19 |
| K8-06 | `automountServiceAccountToken: false` quando o Pod não usa a API (o valor do Pod prevalece sobre o da ServiceAccount) | Médio | V-42 |
| K8-07 | RBAC: `RoleBinding` em vez de `ClusterRoleBinding`; sem wildcard em `verbs`/`resources`; sem `cluster-admin` no uso diário; ninguém em `system:masters` | Crítico se wildcard em produção | V-42 |
| K8-08 | nenhum `Secret` em claro no repositório (`kind: Secret` com `data`/`stringData`); `get/list/watch` em Secrets só a quem precisa | Crítico | V-42 |
| K8-09 | `NetworkPolicy` default deny por namespace e CNI que a implemente (sem controller, a policy não tem efeito) | Médio | V-56 |
| K8-10 | labels de Pod Security no namespace (`pod-security.kubernetes.io/enforce`, `audit`, `warn`) | Médio | V-21, V-57 |

Container conforme ao nível Restricted:

```yaml
spec:
  automountServiceAccountToken: false
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: api
      image: registry.example.com/api@sha256:<digest-real>
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop: ["ALL"]
        readOnlyRootFilesystem: true   # boa prática; o Restricted não exige (Inferido)
      resources:
        requests: { cpu: 100m, memory: 128Mi }
        limits: { memory: 256Mi }
      readinessProbe:
        httpGet: { path: /ready, port: 8080 }
      livenessProbe:
        httpGet: { path: /healthz, port: 8080 }   # só o processo, sem banco
```

Omitir `limits.cpu` é escolha comum para evitar throttling (Inferido); decida com a equipe e registre.

## Adoção do Pod Security Admission em cluster existente

Ordem (V-57; a sequência vem das seções da página, a espera pelos avisos antes de impor é Inferido): `kubectl version` (PSA `v1` exige Kubernetes 1.25 ou superior), `kubectl label --dry-run=server --overwrite ns --all pod-security.kubernetes.io/enforce=<nível>` para ver o impacto sem alterar, `audit` e `warn` em todos os namespaces, `kubectl get namespaces --selector='!pod-security.kubernetes.io/enforce'` para os que faltam, e `enforce` com `enforce-version` um namespace por vez. Você propõe; quem rotula é o usuário (altera o cluster).

## NetworkPolicy: default deny sem quebrar DNS

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes: ["Ingress", "Egress"]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
spec:
  podSelector: {}
  policyTypes: ["Egress"]
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
      ports:
        - { protocol: UDP, port: 53 }
        - { protocol: TCP, port: 53 }
```

DNS em UDP **e** TCP 53 e seletor por `kubernetes.io/metadata.name` (K14; Inferido: a página lida não cobre a regra de DNS). Itens separados em `from`/`to` somam (união); a semântica E de `namespaceSelector` com `podSelector` no mesmo item não foi verificada na fonte lida: teste num namespace não produtivo.

## Armadilhas

- `kubectl get *` em `allow` deixa passar `kubectl get secret -o yaml`; peça `deny` explícito (GT-07).
- Defaults de `periodSeconds` (10), `timeoutSeconds` (1) e `failureThreshold` (3) vieram de conhecimento geral por truncamento da leitura: confira no cluster (GT-12).
- PodSecurityPolicy não existe a partir do Kubernetes 1.25; conteúdo que a recomenda está desatualizado (V-62).
