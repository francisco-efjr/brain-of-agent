# Catálogo de hipóteses e sinais de leitura

Uso: depois de coletar a evidência do passo 2 da skill, escolha as linhas do sintoma, ordene por probabilidade x custo de checar e teste a mais barata primeiro. Todos os sinais abaixo são **de leitura**.

Rótulos: as linhas com fonte V-nn foram verificadas nas páginas oficiais citadas (V-31, V-33, V-35, V-36, V-37, V-58, V-56, V-21, V-42 e o brain `dados-ambientes-ci`). As demais são conhecimento estável do domínio e estão marcadas **Inferido**: confirme a sintaxe e as mensagens na versão instalada, porque o texto exato de mensagens muda entre versões. Conferido em 2026-10-10. A pendência "fonte A para diagnóstico" (páginas oficiais de depuração de Pods e `helm status`/`history`) segue aberta.

## Sumário

- [Kubernetes](#kubernetes)
- [Helm](#helm)
- [Argo CD e Flux](#argo-cd-e-flux)
- [Terraform e OpenTofu](#terraform-e-opentofu)
- [CI/CD](#cicd)
- [Exemplo guiado](#exemplo-guiado)

## Kubernetes

Como ler `kubectl describe pod`: veja `State` e `Last State` (campos `Reason` e `Exit Code`), `Restart Count` e, no fim, `Events`. Códigos de saída comuns: 137 (SIGKILL: costuma ser OOM kill ou morte por probe), 143 (SIGTERM), 1 (erro da aplicação) (Inferido).

| Sintoma | Hipótese | Sinal que confirma | Sinal que refuta | Fonte |
| --- | --- | --- | --- | --- |
| `CrashLoopBackOff` | a aplicação falha ao iniciar (config, dependência, permissão) | `logs --previous` com erro e exit code diferente de 0 | `Reason: OOMKilled`; eventos de probe | Inferido |
| `CrashLoopBackOff`, `Exit Code: 137` | limite de memória excedido (OOM kill) | `Last State: Terminated, Reason: OOMKilled` e `limits.memory` baixo no spec | `Reason: Error` com stack trace | V-58 (limite de memória pode causar OOM kill) |
| reinícios periódicos sem erro de aplicação | liveness agressivo ou que consulta dependência | Events com falha de liveness seguida de reinício; probe aponta para rota que chama o banco | probe local ao processo e estável | V-58 |
| `Running` mas `0/1 Ready` | readiness falhando (rota, porta, dependência) | Events "Readiness probe failed" com status HTTP ou connection refused | readiness passa e o Service continua sem endpoints (seletor de labels) | V-58; seletor: Inferido |
| `ImagePullBackOff`, `ErrImagePull` | tag ou digest inexistente; credencial de registry; limite de pull | Events "Failed to pull image" com `not found`, `unauthorized` ou `rate limit` | imagem puxada com sucesso em outro nó | Inferido |
| `Pending` | sem recurso, afinidade, taint ou PVC pendente | Events `FailedScheduling` com `Insufficient cpu/memory`, `untolerated taint` ou `unbound PersistentVolumeClaim` | Pod agendado em um nó | Inferido |
| `CreateContainerConfigError` | `Secret` ou `ConfigMap` referenciado não existe, chave ausente | Events citando o objeto ou a chave | objetos existem no namespace (`kubectl get secret <nome> -n <ns>` sem `-o yaml`) | Inferido |
| Pods não são criados após ativar PSA | admissão rejeitou o Pod (Pod Security) | Events do ReplicaSet/Deployment com `violates PodSecurity` e o controle que falhou | namespace sem labels `pod-security.kubernetes.io/*` | V-21, V-57; texto da mensagem: Inferido |
| `forbidden` em logs da aplicação | RBAC insuficiente na ServiceAccount | mensagem `cannot <verbo> <recurso>` | erro de rede, não de autorização | V-42; texto: Inferido |
| "could not resolve host" depois de NetworkPolicy | egress default deny sem liberar DNS (UDP e TCP 53) | policy `Egress` sem regra para o DNS do cluster | resolução funciona e falha só um destino | V-56 (policy), DNS: Inferido |
| policy "não faz efeito" | o CNI não implementa NetworkPolicy | cluster sem controller que a aplique | tráfego bloqueado como esperado | V-56 |
| latência alta sob carga sem erro | throttling por limite de CPU | métrica de throttling do container no sistema de métricas do cluster | CPU abaixo do limite | V-58 |
| `rollout status` não termina | novos Pods não ficam Ready; prazo de progresso excedido | Pods do novo ReplicaSet com probe falhando ou `Pending` | todos os Pods Ready e o rollout aguardando outra condição | Inferido |

## Helm

| Sintoma | Hipótese | Sinal que confirma | Fonte |
| --- | --- | --- | --- |
| "another operation (install/upgrade/rollback) is in progress" | release presa em estado pendente por execução anterior interrompida | `helm status` e `helm history` mostram revisão `pending-*` | Inferido |
| `UPGRADE FAILED` com "timed out waiting for the condition" | Pods não ficaram Ready no prazo | `kubectl get pods`, `describe` (veja tabela de Kubernetes) | Inferido |
| "has no deployed releases" | a primeira instalação falhou | `helm history` com revisão `failed` | Inferido |
| erro de renderização | valor obrigatório ausente (`required`), YAML inválido, `#` antes de `required` | `helm template ... -f <values>` local reproduz o erro | V-30 (comportamento de `#` com `required`) |
| diferença entre ambientes | values do ambiente sobrescrevem o padrão de forma inesperada | `helm template` com cada `values-*.yaml` e comparação do renderizado | V-30 |

Propostas (não execute): `helm rollback`, novo `helm upgrade` com correção. Ambas mudam o cluster e vão para `deploy-infra`.

## Argo CD e Flux

| Sintoma | Hipótese | Sinal que confirma | Fonte |
| --- | --- | --- | --- |
| `OutOfSync` permanente | controller altera campo (ex.: `replicas` com HPA) ou Git diverge do vivo | diff do `Application`; campo mutado por controller | V-22, V-31 |
| mudança manual "voltou sozinha" | self-heal (Argo CD) ou reconciliação (Flux) | `selfHeal` ligado; Flux reverte `kubectl edit/patch/delete` | V-31, V-33 |
| sync automático falhou e não repete | uma tentativa por SHA e conjunto de parâmetros | `retry` ausente; condição de falha do `Application` | V-31 |
| `Degraded` | um recurso filho não está saudável | status do recurso filho (veja Kubernetes) | V-31; leitura: Inferido |
| não consigo fazer rollback pela UI | sync automático ativo | `syncPolicy.automated` presente | V-31 |
| recurso apagado inesperadamente | `prune` ligado e o manifest saiu do Git | `prune: true`; commit que removeu o arquivo | V-31, V-33 |
| `Kustomization` não fica `Ready` | espera a dependência (`dependsOn` exige `Ready`), health check ou fonte falhando | condições da `Kustomization` e do `GitRepository`; ciclo em `dependsOn` | V-33 |
| falha de decifragem | segredo SOPS ausente no cluster ou `decryption.provider` incorreto | mensagem da condição citando decryption | V-33; texto: Inferido |
| `wait: true` não respeita `healthChecks` | `wait: true` ignora `healthChecks` | ambos presentes no spec | V-33 |

## Terraform e OpenTofu

| Sintoma | Hipótese | Sinal que confirma | Fonte |
| --- | --- | --- | --- |
| "Error acquiring the state lock" | outro run ativo, ou run morto que deixou lock | a mensagem traz ID, operador e hora do lock; confira se há run ativo no CI | V-35 |
| checksum ou hash do provider diverge | `.terraform.lock.hcl` sem hash da plataforma de quem roda | erro de checksum no `init`; lockfile só com `h1:` de uma plataforma | V-36 |
| "Backend initialization required" | mudou backend ou módulos | mensagem pede `init` | Inferido |
| `plan` com troca inesperada | atributo que força substituição, ou drift | `forces replacement` no atributo; compare com o state | Inferido |
| erro de credencial | token expirado, role OIDC com condição de repositório/branch não atendida | mensagem do provider; claims do job | Inferido |
| `terraform test` criou recursos | `command = apply` (padrão) | bloco `run` sem `command = plan` | V-37 |

Propostas (não execute): `terraform force-unlock <ID>` só se o destravamento automático falhou **e** o lock é do próprio usuário (V-35); `terraform providers lock -platform=...` em PR dedicado (V-36); `init -upgrade` em PR próprio.

## CI/CD

| Sintoma | Hipótese | Sinal que confirma | Fonte |
| --- | --- | --- | --- |
| job vermelho | o primeiro step que falhou é a causa; os seguintes são consequência | log do primeiro step vermelho e o exit code | brain `dados-ambientes-ci` |
| pipeline verde, mas nada foi testado | `\|\| true`, zero testes coletados, shard ausente, `continue-on-error`, job cancelado tratado como sucesso | contagem de testes executados; `\|\| true` no YAML | brain |
| falha oculta em pipe | `cmd \| tee` sem `pipefail` devolve o exit code do último comando | script sem `set -o pipefail` | Inferido |
| 403 do `GITHUB_TOKEN` | `permissions` insuficientes para o job | `permissions: contents: read` e o job tenta escrever | V-01 |
| segredo vazio em PR de fork | PRs de fork não recebem segredos no gatilho `pull_request` | evento do run e origem do PR | Inferido |
| cache nunca reaproveitado | chave primária com `github.run_id` | `key:` contém `run_id` | V-01 |
| deploy publicou versão antiga | recompilou em vez de promover o artefato testado | job de deploy com novo `build`; digests diferentes | brain |

## Exemplo guiado

Entrada colada pelo usuário (fictícia): `kubectl get pods -n pagamentos` mostra `api-7d9f-xk2 0/1 ImagePullBackOff`; `describe pod` traz em Events: `Failed to pull image "registry.example.com/api@sha256:...": not found`.

1. Alvo: contexto confirmado como `staging-1`, namespace `pagamentos` (Verificado pelo `kubectl config current-context`). Mudança recente: commit `a1b2c3` alterou o digest da imagem em `k8s/api/deployment.yaml`.
2. Hipóteses: (a) digest inexistente no registry; (b) credencial de pull ausente; (c) limite de taxa do registry. Sinal de (a): mensagem `not found`; (b) produziria `unauthorized`; (c) produziria `rate limit`.
3. O evento diz `not found` → (a) confirmada; (b) e (c) descartadas pela mensagem. Rótulo: Verificado (evento) com Inferido sobre o texto de cada erro.
4. Correção proposta: o digest foi digitado errado ou o push da imagem não terminou. Diff: restaurar o digest do build aprovado em `deployment.yaml`; check: `docker buildx imagetools inspect registry.example.com/api@sha256:<digest>` retorna o manifest (leitura no registry, a cargo do usuário); depois `kubectl rollout status`.
5. Ação no ambiente: nenhuma executada; a aplicação do diff vai para `deploy-infra`.
6. Prevenção: CI que valida a existência do digest antes de abrir o PR de deploy.
