# GitOps: Argo CD e Flux (GO-nn)

Base: V-22 (boas práticas do Argo CD), V-31 (sync automático), V-32 (ApplicationSets), V-33 (Flux), V-34 (segredos no Argo CD), P-14 (nota 83). Conferido em 2026-10-10. Destilação com redação própria. O que **não** citar: default do `interval` do Flux (as páginas oficiais divergem, K10), a frase "sync automático desligado por padrão" do Argo CD (a página só o implica, K9), gerador `merge` e progressive sync do ApplicationSet (não confirmados, V-32).

## Fatos de referência (Verificado)

| Tema | Fato | Fonte |
| --- | --- | --- |
| Argo CD prune e self-heal | desligados por padrão; self-heal timeout de 5 s; reconciliação de 120 s com jitter de 60 s (no máximo cerca de 3 min) | V-31 |
| Argo CD retry | `retry.limit` com `-1` é ilimitado; com sync automático há uma tentativa por SHA e conjunto de parâmetros | V-31 |
| Argo CD rollback | com sync automático não é possível pela UI; o caminho é um novo commit | V-31 |
| ApplicationSet | geradores citados: List, Cluster, Git, Matrix; controlador incluso desde o Argo CD v2.3; alerta de segurança com página própria | V-32 |
| Argo CD segredos | preferir criar no cluster de destino; injeção na geração de manifests deixa os manifests em texto plano no cache Redis | V-34 |
| Argo CD boas práticas | repositório de config separado do código; campos geridos por controllers (ex.: `replicas` com HPA) fora do Git; bases remotas de kustomize por tag ou SHA (`?ref=`) | V-22 |
| Flux fontes | GitRepository, OCIRepository, HelmRepository, Bucket | V-33 |
| Flux Kustomization | `interval` obrigatório (mínimo 60 s); `prune` obrigatório; `deletionPolicy` padrão `MirrorPrune`; `dependsOn` espera `Ready`; `wait: true` ignora `healthChecks`; `decryption.provider: sops`; `retryInterval` padrão igual a `interval` | V-33 |
| Flux reversão | mudanças manuais (`kubectl edit/patch/delete`) são revertidas, salvo suspender a reconciliação ou commitar | V-33 |

## Checklist

| ID | Verificar | Sev. | Fonte |
| --- | --- | --- | --- |
| GO-01 | `syncPolicy.automated` só onde deploy sem clique é aceito (decisão por ambiente) | Alto em produção | V-31, K9 |
| GO-02 | `prune: true` explícito e revisado; por padrão o Argo CD não apaga | Alto | V-31 |
| GO-03 | `selfHeal` decidido por ambiente: reverte mudança manual após o timeout; em produção, avalie o efeito em correções emergenciais manuais | Médio | V-31 |
| GO-04 | `retry` com backoff e limite; `limit: -1` só com motivo | Médio | V-31 |
| GO-05 | `allowEmpty` só com motivo (permite sincronizar sem recursos) | Médio | Inferido (campo do Argo CD) |
| GO-06 | rollback documentado como novo commit; ninguém depende do rollback da UI com sync automático | Médio | V-31 |
| GO-07 | `targetRevision` de produção: branch móvel é decisão consciente (todo merge implanta); preferir tag ou SHA onde o processo de promoção for por PR | Médio | Inferido |
| GO-08 | ApplicationSet: quem cria ou edita gera Applications com destino amplo; `AppProject` restringe destinos e repositórios; template testado com um cluster antes de escalar | Alto | V-32; AppProject: Inferido |
| GO-09 | Flux: `prune` explícito; `kustomize.toolkit.fluxcd.io/prune: disabled` só onde proposital | Alto | V-33 |
| GO-10 | `dependsOn` sem ciclo e com health checks quando a ordem depende de CRDs ou controllers; lembrar que `wait: true` ignora `healthChecks` | Médio | V-33 |
| GO-11 | `interval` explícito (mínimo 60 s) e coerente com a carga; `retryInterval` definido | Baixo | V-33 |
| GO-12 | nenhum `Secret` em claro no repositório; segredo criado no cluster de destino (Sealed Secrets, ESO, Secrets Store CSI Driver, Vault Secrets Operator); Flux com SOPS via `decryption.provider: sops` | Crítico | V-34, V-33 |
| GO-13 | plugin que injeta segredo na geração de manifests (argocd-vault-plugin): só com Redis e repo-server isolados por NetworkPolicy (e CNI que a aplique) e, de preferência, cluster dedicado | Alto | V-34 |
| GO-14 | repositório de config separado do código (CI sem loop, auditoria limpa, acesso separado); campos geridos por controllers fora do Git ou em `ignoreDifferences` | Médio | V-22 |
| GO-15 | bases remotas de kustomize fixadas por tag ou SHA, nunca por HEAD | Alto | V-22 |
| GO-16 | sem `kubectl` manual em produção como processo normal (Inferido): mudança durável é commit | Médio | V-33; Inferido |

## Exemplo Argo CD: Application de staging

Autoria da casa; ajuste nomes e repositórios.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: pagamentos-staging
  namespace: argocd
spec:
  project: pagamentos              # AppProject que limita destinos e repositórios
  source:
    repoURL: https://git.example.com/plataforma/config.git
    targetRevision: main
    path: apps/pagamentos/overlays/staging
  destination:
    server: https://kubernetes.default.svc
    namespace: pagamentos
  syncPolicy:
    automated:
      prune: true                  # staging: revisado; em produção, decisão explícita
      selfHeal: true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas           # gerido pelo HPA
```

Para produção, a variação típica é remover `automated` (sync manual, aprovado) ou mantê-lo com `prune: false` e revisar remoções por PR. A escolha é da equipe: registre-a como decisão (ADR de infra).

## Exemplo ApplicationSet (gerador List)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: pagamentos
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - ambiente: staging
            url: https://kubernetes.default.svc
  template:
    metadata:
      name: "pagamentos-{{ambiente}}"
    spec:
      project: pagamentos
      source:
        repoURL: https://git.example.com/plataforma/config.git
        targetRevision: main
        path: "apps/pagamentos/overlays/{{ambiente}}"
      destination:
        server: "{{url}}"
        namespace: pagamentos
```

Revise: um elemento novo na lista cria uma Application com destino novo. Quem aprova o PR no repositório de config controla onde isso implanta; por isso o `AppProject` e o CODEOWNERS contam.

## Exemplo Flux: Kustomization com dependência e SOPS

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: pagamentos
  namespace: flux-system
spec:
  interval: 10m
  retryInterval: 2m
  timeout: 5m
  path: ./apps/pagamentos/staging
  prune: true
  sourceRef:
    kind: GitRepository
    name: config
  dependsOn:
    - name: infra-controllers
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: api
      namespace: pagamentos
  decryption:
    provider: sops
    secretRef:
      name: sops-age
```

Revise: sem `wait: true` (que ignoraria `healthChecks`), a ordem depende do `Ready` de `infra-controllers`; `prune: true` apaga o que sair do Git; o Secret `sops-age` (chave de decifragem) existe só no cluster e nunca no repositório.

## Verificação no cluster (somente leitura)

Com contexto confirmado: `kubectl diff -f <renderizado>` mostra o que mudaria (saída 0 sem diferenças, 1 com diferenças, maior que 1 em erro; Inferido). Sem acesso: "não verificado no cluster". Nunca `argocd app sync`, `flux reconcile` nem `kubectl apply`.
