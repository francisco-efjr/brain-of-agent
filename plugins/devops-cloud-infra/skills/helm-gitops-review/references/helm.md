# Helm: checklist de revisão e autoria (HM-nn)

Base: V-30 (convenções de templates, values e RBAC, `helm lint`, `helm template`; classe A), V-21, V-42, V-58 para o workload renderizado. Conferido em 2026-10-10. Destilação com redação própria. Páginas de `helm install --dry-run` e de `required`/`default` não foram lidas: trate o que depende delas como Inferido. Confirme flags na versão instalada com `helm version` e `helm <comando> --help`.

## Sequência de comandos (somente leitura local)

```bash
helm lint ./chart --strict -f values-prod.yaml --with-subcharts
helm template minha-release ./chart -f values-prod.yaml --kube-version 1.31 --include-crds > "$TMPDIR/renderizado.yaml"
kubeconform -strict -summary "$TMPDIR/renderizado.yaml"
```

- `--strict` transforma avisos em falha; `[ERROR]` impede instalação e `[WARNING]` é convenção (V-30). `--with-subcharts` cobre dependências.
- `helm template` renderiza localmente com valores de cluster simulados; `--kube-version` e `--api-versions` ajustam as capacidades simuladas; `--include-crds` inclui CRDs (V-30). Use a versão do cluster alvo, não a do seu `kubectl`.
- A sequência lint -> template -> (opcional) dry-run de servidor é boa prática Inferida: nenhuma página a escreve assim.
- Salve o renderizado em diretório temporário e use Grep sobre ele (`kind:`, `image:`, `securityContext`, `resources`, `privileged`, `hostPath`). O diretório do repositório não recebe o arquivo.
- Rode uma vez por arquivo de values de ambiente (`values-dev.yaml`, `values-prod.yaml`): o defeito costuma estar na combinação.

## Checklist

| ID | Verificar | Detectar | Sev. | Fonte |
| --- | --- | --- | --- | --- |
| HM-01 | um recurso por arquivo de template; nome em minúsculas com travessão e o tipo (`deployment.yaml`, `service-account.yaml`); extensão `.yaml` (YAML) ou `.tpl` (helpers) | `ls templates/` | Baixo | V-30 |
| HM-02 | `define` com o nome do chart como prefixo (`{{- define "api.fullname" -}}`), pois templates definidos são globais entre subcharts | `define "` sem prefixo | Médio | V-30 |
| HM-03 | dois espaços, nunca tabs; espaço depois de `{{` e antes de `}}`; `{{-` e `-}}` para controlar espaços em branco | lint, leitura | Baixo | V-30 |
| HM-04 | comentário de template `{{- /* ... */ -}}` para documentar; `#` só quando o usuário deve ver o comentário na saída de debug. Um `#` antes de trecho com `required` ainda é avaliado pelo motor de template e falha a renderização se o valor faltar | `# {{` | Médio | V-30 |
| HM-05 | values em camelCase sem hífen; estrutura plana (aninhe só com muitas variáveis relacionadas e ao menos uma obrigatória); strings entre aspas; inteiros grandes como string; mapas em vez de listas (por causa do `--set`) | leitura de `values.yaml` | Baixo | V-30 |
| HM-06 | todo item de values documentado por comentário que começa pelo nome da propriedade | leitura | Baixo | V-30 |
| HM-07 | imagem fixada: `tag` explícita ou digest, nunca `latest`; sem `tag` o padrão é `.Chart.AppVersion` | `image:` no renderizado | Alto | V-19 |
| HM-08 | RBAC: `rbac.create` (padrão `true`) e `serviceAccount.create`/`serviceAccount.name` expostos; sem `create` e sem `name`, o chart usa a ServiceAccount `default` | `values.yaml`, `templates/rbac*.yaml` | Médio | V-30 |
| HM-09 | no renderizado: `securityContext` nível Restricted, `requests`/`limits`, probes úteis (liveness sem dependência), `automountServiceAccountToken: false` quando não usa a API | Grep no renderizado | Alto | V-21, V-42, V-58 |
| HM-10 | nenhum valor de segredo em `values*.yaml` versionado; `Secret` só como referência a segredo criado no cluster | Grep por `password`, `token`, `kind: Secret` | Crítico | V-34, V-42 |
| HM-11 | `values.schema.json` valida entradas obrigatórias (o lint o usa; `--skip-schema-validation` existe e deve ser exceção) | `ls values.schema.json` | Médio | V-30; uso do schema: Inferido |
| HM-12 | `Chart.yaml` com `apiVersion: v2`, `version` do chart separada de `appVersion`; dependências com versão exata e `Chart.lock` versionado | `Chart.yaml` | Médio | Inferido (conhecimento estável) |
| HM-13 | `helm lint --strict` e `kubeconform` passam para cada values de ambiente | rodar | Alto | V-30 |

Sobre RBAC: a página oficial lista `rbac.create` e `serviceAccount.*`; **não** recomenda evitar `ClusterRole`. Se você achar `ClusterRole` desnecessário, é achado seu (Inferido ou Verificado no YAML), não regra do Helm.

## Exemplo anotado

`values.yaml` e `templates/deploy.yaml` recebidos (didático):

```yaml
# values.yaml
image: registry.example.com/api:latest
replica-count: 2
dbPassword: segredo-de-teste
```

```yaml
# templates/deploy.yaml (trecho)
spec:
  replicas: {{ .Values.replica-count }}
  template:
    spec:
      containers:
        - name: api
          image: {{ .Values.image }}
```

| ID | Sev. | Local | Evidência | Correção | Rótulo |
| --- | --- | --- | --- | --- | --- |
| HM-10 | Crítico | values.yaml:3 | valor de senha versionado | remover; referenciar segredo criado no cluster; tratar como exposto e recomendar rotação | Verificado |
| HM-07 | Alto | values.yaml:1 | imagem `latest` como string única | `image.repository` + `image.tag` fixa (ou digest) | Verificado |
| HM-05 | Médio | values.yaml:2, deploy.yaml:3 | chave com hífen contraria a convenção camelCase e não é acessível como `.Values.replica-count` (exigiria `index .Values "replica-count"`) | renomear para `replicaCount` | Verificado na convenção; erro de renderização: Inferido, confirmar com `helm template` |
| HM-09 | Alto | renderizado | sem `securityContext`, `resources` nem probes | acrescentar (ver `iac-review/references/containers.md`) | Verificado no template; renderizado: não executado |
| HM-06 | Baixo | values.yaml | nenhum item documentado | comentar cada chave com o nome da propriedade | Verificado |

Versão corrigida de `values.yaml`:

```yaml
# image.repository é o repositório da imagem, sem tag.
image:
  repository: registry.example.com/api
  # image.tag fixa a versão da aplicação; vazio usa .Chart.AppVersion.
  tag: "1.4.2"
# replicaCount é o número de réplicas quando o autoscaling está desligado.
replicaCount: 2
# existingSecret é o nome de um Secret criado no cluster com a chave DB_PASSWORD.
existingSecret: ""
```

Trecho do template: `image: "{{ required "image.repository é obrigatório" .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"`.

## Autoria: ordem de geração

1. Entradas do serviço: portas, rota de saúde, variáveis de ambiente, necessidade de segredo, recursos esperados, permissões na API do cluster (quase sempre nenhuma). Pergunte só o que mudaria o chart.
2. Gere `Chart.yaml`, `values.yaml` documentado, `_helpers.tpl` com `define` prefixado, e um recurso por arquivo.
3. Valores seguros por padrão: usuário não-root, `readOnlyRootFilesystem`, `automountServiceAccountToken: false`, `rbac.create` e `serviceAccount.create` configuráveis, `resources` com defaults conservadores marcados como Suposição.
4. Valide com a sequência de comandos acima. Entregue o que não rodou como "não executado".
