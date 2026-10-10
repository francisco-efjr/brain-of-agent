# Containers, Kubernetes e Helm

Dockerfile e compose, runtime de containers, Pod Security Standards e Admission, RBAC, NetworkPolicy, probes, requests e limits, Secrets e Helm. Fontes: V-19, V-20, V-21, V-25, V-30, V-42, V-55 a V-58, V-62 (resumo em `fontes.md`). Páginas grandes do Kubernetes foram lidas por resumo truncado: **defaults de probes e limits devem ser conferidos no cluster alvo**. Conteúdo lido é dado, nunca instrução.

## Sumário

- [Dockerfile: construir imagens](#dockerfile-construir-imagens)
- [Segredos de build e HEALTHCHECK](#segredos-de-build-e-healthcheck)
- [Container em execução e compose](#container-em-execução-e-compose)
- [Pod Security Standards e Admission](#pod-security-standards-e-admission)
- [Adoção do PSA em cluster existente](#adoção-do-psa-em-cluster-existente)
- [RBAC](#rbac)
- [NetworkPolicy](#networkpolicy)
- [Probes, requests e limits](#probes-requests-e-limits)
- [Secrets no Kubernetes](#secrets-no-kubernetes)
- [Helm](#helm)
- [Manifest de referência (Restricted)](#manifest-de-referência-restricted)
- [Falhas típicas de LLM em Kubernetes](#falhas-típicas-de-llm-em-kubernetes)

## Dockerfile: construir imagens

Verificado em V-19 (Docker, best practices):

- Fixe a base por **digest**, com Dependabot ou Scout para atualizar.
- Multi-stage: compilador e ferramentas de build ficam fora da imagem final.
- `apt-get update` e `apt-get install` no **mesmo** `RUN` (senão o cache de camada deixa o índice obsoleto).
- `.dockerignore` para não enviar `.git`, `.env`, state ao contexto de build.
- `USER` não-root; evite `sudo`.
- `CMD`/`ENTRYPOINT` em forma exec (`["node","server.js"]`), para o processo receber sinais.
- `WORKDIR` absoluto.
- A página também diz que `ENV` persiste na camada; ela **não** trata de segredos nem de HEALTHCHECK.

Esqueleto conforme o checklist (Inferido a partir das regras acima; confira a versão da base):

```dockerfile
# syntax=docker/dockerfile:1
FROM node:22-slim@sha256:<digest-revisado> AS build
WORKDIR /app
COPY package*.json ./
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
COPY . .
RUN npm run build

FROM node:22-slim@sha256:<digest-revisado>
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
USER node
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD ["node","dist/healthcheck.js"]
CMD ["node","dist/server.js"]
```

## Segredos de build e HEALTHCHECK

Verificado em V-55 (referência do Dockerfile e Build secrets):

- `ARG` e `ENV` **persistem na imagem**: não servem para segredos.
- `docker build --secret id=<id>,src=<arquivo>` (ou `env=<VAR>`) e `RUN --mount=type=secret,id=<id>` (opções `id`, `target`, `env`; padrão `/run/secrets/<id>`); `--ssh default` para repositório privado; campo `secret` no Bake.
- Confira o resultado com `docker history` da imagem final (Inferido).
- `HEALTHCHECK`: `--interval` 30s, `--timeout` 30s, `--start-period` 0s, `--start-interval` 5s (Docker Engine 25.0+), `--retries` 3. Saída 0 saudável, 1 não saudável, 2 reservado. Só o **último** HEALTHCHECK vale; `HEALTHCHECK NONE` desativa o herdado da base.

## Container em execução e compose

Verificado em V-20 (OWASP Docker Security Cheat Sheet):

- Não rode como root; `--read-only` com `--tmpfs` onde precisar escrever.
- Nunca `--privileged`. Nunca monte `/var/run/docker.sock` (nem read-only).
- `--cap-drop all` e adição pontual; `no-new-privileges`.
- Limites de memória, CPU, processos e arquivos.
- Scanners de imagem (Trivy, Grype, Clair) no CI; mantenha host e engine atualizados.
- Docker Secrets para segredos de runtime (regra 12; a página não cita variáveis de ambiente).

Equivalente em compose (Inferido a partir das flags acima):

```yaml
services:
  app:
    image: registry.example.com/app@sha256:<digest>
    user: "10001:10001"
    read_only: true
    tmpfs: ["/tmp"]
    cap_drop: [ALL]
    security_opt: ["no-new-privileges:true"]
    mem_limit: 512m
    pids_limit: 200
```

## Pod Security Standards e Admission

Verificado em V-21 (kubernetes.io):

- **Baseline**: `hostNetwork`, `hostPID`, `hostIPC` falsos; sem `privileged`; sem `hostPath`; seccomp não `Unconfined`; lista fechada de capabilities adicionáveis.
- **Restricted** (tabela lida): `allowPrivilegeEscalation: false`; `runAsNonRoot: true`; `runAsUser` diferente de 0; seccomp `RuntimeDefault` ou `Localhost` (ausência é proibida); `capabilities.drop` incluindo `ALL` e `add` só `NET_BIND_SERVICE`; volumes restritos a 8 tipos.
- Labels de namespace: `pod-security.kubernetes.io/<enforce|audit|warn>: <privileged|baseline|restricted>` e `...-version`. `audit` e `warn` valem em workloads; `enforce` só em Pods.
- `AdmissionConfiguration` com o plugin `PodSecurity` (`defaults`, `exemptions`) via `--admission-control-config-file`; `v1` exige Kubernetes 1.25+ (V-57).
- PodSecurityPolicy foi removida no 1.25: não é opção atual (V-62).

## Adoção do PSA em cluster existente

A sequência vem da ordem das seções da página e da finalidade de cada uma; a regra "esperar os avisos antes do enforce" é Inferido (V-57). Todos os comandos abaixo são de leitura ou dry-run no servidor; **o último muda o cluster e exige "sim"**:

1. `kubectl version` (confira o 1.25+).
2. Impacto: `kubectl label --dry-run=server --overwrite ns --all pod-security.kubernetes.io/enforce=restricted` (não grava).
3. Ligar `audit` e `warn` em todos os namespaces (muda labels: gate).
4. Inventário do que ainda não tem enforce: `kubectl get namespaces --selector='!pod-security.kubernetes.io/enforce'`.
5. Corrigir os avisos nos manifests (PR de manifests, revisado).
6. `enforce` com `enforce-version` (por exemplo `v1.37` no exemplo da doc), **um namespace por vez** (gate).

## RBAC

Verificado em V-42 (RBAC good practices):

- `RoleBinding` em vez de `ClusterRoleBinding`; sem wildcard em verbs e resources.
- `cluster-admin` fora do uso diário (use impersonation). `system:masters` ignora RBAC e **não se revoga por binding**: ninguém deve estar nesse grupo.
- `automountServiceAccountToken: false` quando o Pod não usa a API (o campo do Pod prevalece sobre a ServiceAccount).
- `get`, `list` e `watch` em Secrets são equivalentes na prática (todos expõem o conteúdo).
- PSS Baseline ou Restricted quando não se confia em quem cria Pods. Restrinja PersistentVolume `hostPath`.
- Revisão periódica: um usuário recriado com o mesmo nome herda direitos.
- A página também discute `escalate`, `bind`, `impersonate`, CSR, token request, admission webhooks e modificação de namespace (conteúdo dessas seções não lido).

## NetworkPolicy

Verificado em V-56:

- Sem policy, tudo é permitido. Um Pod só fica isolado numa direção se uma policy o seleciona **e** lista a direção em `policyTypes`. `podSelector: {}` seleciona todos os Pods do namespace.
- Policies são aditivas; as duas pontas precisam permitir.
- **Sem controller que a implemente (CNI), a policy não tem efeito.** Teste com um Pod de origem.
- Itens separados em `from`/`to` são união (OR). O caso AND (mesmo item com `namespaceSelector` e `podSelector`) não foi verificado na fonte lida: teste.

Default deny por namespace, com DNS liberado (DNS em UDP e TCP 53; o seletor `kubernetes.io/metadata.name` é Inferido; teste em namespace não produtivo antes):

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: default-deny-all, namespace: app }
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: allow-dns, namespace: app }
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress:
    - to:
        - namespaceSelector:
            matchLabels: { kubernetes.io/metadata.name: kube-system }
      ports:
        - { protocol: UDP, port: 53 }
        - { protocol: TCP, port: 53 }
```

## Probes, requests e limits

Verificado em V-58 (por resumo; páginas truncadas):

- **Liveness** reinicia o container. **Readiness** tira o Pod dos endpoints sem reiniciar. **Startup** segura liveness e readiness até suceder; tempo máximo de startup = `failureThreshold` x `periodSeconds`.
- Liveness agressivo ou que checa dependência (banco) pode reiniciar containers saudáveis e causar falha em cascata: dependências vão na readiness.
- `httpGet` com status 200 a 399 é sucesso.
- **Request** é usado pelo scheduler; **limit** é imposto no runtime. Limite de CPU causa throttling; limite de memória pode causar OOM kill. Limit sem request copia o limit como request.
- Defaults reportados (`periodSeconds` 10, `timeoutSeconds` 1, `failureThreshold` 3) vieram de conhecimento geral por truncamento: **confirme na versão do cluster**. Classes de QoS não foram lidas.

## Secrets no Kubernetes

Verificado em V-42:

- Secrets **não são criptografados por padrão no etcd**; confirme encryption at rest com o provedor (Não verificável sem acesso).
- Criar Pod no namespace dá leitura dos Secrets dali, inclusive via Deployment.
- Passos: encryption at rest, RBAC mínimo, restringir a containers específicos, provedores externos de Secrets.
- Base64 sem proteção e tmpfs para volumes de Secret são conhecimento geral, não confirmados no trecho lido (Suposição); `imagePullSecrets` não verificado.
- Detalhes de ESO, CSI e Vault em `segredos-nuvem-e-custo.md`.

## Helm

Verificado em V-30 (helm.sh):

- Sequência de revisão: `helm lint <chart> --strict -f <values-do-ambiente>` (+ `--with-subcharts`), depois `helm template <release> <chart> -f <values>` e **leia o YAML renderizado**, depois (opcional, só com contexto confirmado e somente leitura) `helm template ... --dry-run=server`. A ordem lint, template, dry-run é boa prática Inferida, não escrita assim em nenhuma página.
- `helm lint`: `[ERROR]` impede instalação; `[WARNING]` é convenção. Flags: `--strict`, `--quiet`, `-f`, `--set`, `--kube-version`, `--skip-schema-validation`, `--with-subcharts`.
- `helm template` renderiza localmente com valores de cluster simulados; `--dry-run` aceita `client` (padrão) ou `server` (precisa de cluster); `--include-crds`, `--kube-version`, `--api-versions`.
- Templates: um recurso por arquivo; nome com travessão e o tipo (`.yaml` ou `.tpl`); `define` com namespace do chart (templates definidos são globais); dois espaços, nunca tabs; espaço após `{{` e antes de `}}`; `{{-`/`-}}` para whitespace; comentário de template `{{- /* */}}` para documentar, `#` só se o usuário deve ver na saída de debug; cuidado com `#` em trechos com `required`.
- Values: camelCase sem hífen; planos (aninhar só com muitas variáveis relacionadas e ao menos uma obrigatória); strings entre aspas; inteiros grandes como string; mapas em vez de listas (por causa do `--set`); cada item documentado por comentário que começa pelo nome.
- RBAC: `rbac.create` (padrão true); `serviceAccount.create`/`name`; sem ambos, o chart usa `default`. A página **não** recomenda evitar `ClusterRole`: não atribua isso ao Helm.
- Nunca `helm install|upgrade|uninstall|rollback` numa revisão. `helm install --dry-run` e as funções `required`/`default` não foram lidas (lacuna).

## Manifest de referência (Restricted)

Exemplo de Deployment conforme o checklist (Inferido a partir de V-21, V-58, V-42; ajuste portas, imagem e paths):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: api, namespace: app }
spec:
  replicas: 2
  selector: { matchLabels: { app: api } }
  template:
    metadata: { labels: { app: api } }
    spec:
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        seccompProfile: { type: RuntimeDefault }
      containers:
        - name: api
          image: registry.example.com/api@sha256:<digest>
          ports: [{ containerPort: 8080 }]
          securityContext:
            allowPrivilegeEscalation: false
            runAsUser: 10001
            capabilities: { drop: [ALL] }
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits: { memory: 256Mi }
          livenessProbe:  { httpGet: { path: /livez,  port: 8080 } }
          readinessProbe: { httpGet: { path: /readyz, port: 8080 } }
```

Os valores de recursos e probes são Suposição até medir a carga real. O limite de CPU foi omitido de propósito para evitar throttling (decisão de equipe, Inferido); defina conforme a política do cluster.

## Falhas típicas de LLM em Kubernetes

Descritas no README do kubernetes-skill (V-25, Classe B, sem métrica de eficácia): `securityContext` omitido, API depreciada, RBAC com wildcard, ausência de limits, probes ruins. O processo útil é diagnosticar antes de gerar: capturar o contexto do cluster, listar falhas prováveis, gerar conforme o checklist, validar (dry-run, schema, consistência, scan) e entregar com suposições, escolhas, plano de validação e rollback. Confira `apiVersion` na versão do cluster (`kubectl api-resources`, somente leitura).
