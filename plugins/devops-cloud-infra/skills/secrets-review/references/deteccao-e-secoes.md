# Detecção sem expor valores e seções por tipo de uso (SC-nn)

Base: V-17, V-34, V-38, V-39, V-41, V-42, V-43, V-55 e P-16 (nota 85); brain `seguranca-e-privacidade` ("segredo removido depois continua exposto"). Conferido em 2026-10-10. Destilação com redação própria. Os padrões de busca são conhecimento estável do domínio (Inferido): ajuste ao projeto.

## Sumário

- [Buscas](#buscas)
- [Mascaramento](#mascaramento)
- [Seções por tipo de uso](#seções-por-tipo-de-uso)
- [Exemplo anotado](#exemplo-anotado)
- [Padrões seguros de referência](#padrões-seguros-de-referência)
- [Texto de recomendação de rotação](#texto-de-recomendação-de-rotação)

## Buscas

Use sempre `output_mode: files_with_matches` (a ferramenta `Grep` em modo `content` imprime a linha inteira, valor incluso). Depois leia só o intervalo de linhas necessário. Nas tabelas, `\|` representa o `|` da alternância de regex.

| O que procurar | Padrão (regex, Grep) | Onde |
| --- | --- | --- |
| atribuição de credencial | `(?i)(password\|passwd\|secret\|token\|api[_-]?key\|private[_-]?key)\s*[:=]\s*["']?[^\s"'$\{<]{6,}` | `*.tf`, `*.tfvars`, `*.yaml`, `*.yml`, `*.env*`, `*.json`, `Dockerfile*` |
| chave de acesso AWS | `AKIA[0-9A-Z]{16}` | todo o repositório |
| token do GitHub | `gh[pousr]_[A-Za-z0-9]{36,}` | todo o repositório |
| chave privada | `-----BEGIN (RSA \|EC \|OPENSSH \|DSA \|)PRIVATE KEY-----` | todo o repositório |
| Secret do Kubernetes em claro | `kind:\s*Secret` (depois conferir `data:` ou `stringData:` com valor) | manifests, charts |
| segredo em build | `^\s*(ARG\|ENV)\s+\S*(TOKEN\|SECRET\|PASSWORD\|KEY)` | `Dockerfile*` |
| segredo ecoado em CI | `echo .*secrets\.` ou `secrets\.` em `with:` de action sem pin | `.github/workflows` |
| arquivos que não deveriam existir | `Glob`: `**/*.tfstate*`, `**/*.tfvars`, `**/.env*`, `**/*.pem`, `**/id_rsa*`, `**/credentials*.json` | todo o repositório |
| `.gitignore` cobre os acima | `Grep` por `tfstate`, `tfvars`, `.env` em `.gitignore` | raiz |

Histórico, só nomes de arquivo: `git log --all --diff-filter=A --name-only --pretty=format: -- "*.tfvars" ".env*" "*.pem" "*.tfstate*"`. Nunca `git log -p` nem `git show` sobre esses arquivos.

## Mascaramento

- Relate: tipo, nome da chave, `arquivo:linha`, "valor real, placeholder (`changeme`, `<...>`, `${VAR}`) ou referência a cofre".
- Não relate: valor, prefixo, sufixo, comprimento, hash.
- Se precisar mostrar contexto, substitua o valor por `<valor omitido>` no trecho.
- Se uma ferramenta imprimiu um valor na sua sessão, não o repita; diga ao usuário que o terminal ou log contém o segredo e que ele deve tratá-lo como exposto.

## Seções por tipo de uso

Severidade padrão entre parênteses; ajuste ao contexto.

### Nuvem: AWS Secrets Manager (V-41)

| ID | Verificar | Sev. |
| --- | --- | --- |
| SC-01 | chave KMS definida: `aws/secretsmanager` na maioria dos casos (sem custo); chave do cliente para acesso entre contas ou política de chave, com `kms:ViaService` e encryption context | Médio |
| SC-02 | rotação automática ligada (estratégias single user ou alternating users; intervalos a partir de 4 horas) | Alto |
| SC-03 | cache no cliente em vez de buscar a cada requisição (bibliotecas oficiais, extensão Lambda, EKS) | Baixo |
| SC-04 | quem pode `PutResourcePolicy` tem a condição `secretsmanager:BlockPublicPolicy: true`; mínimo privilégio por IAM, resource policy e ABAC | Alto |
| SC-05 | VPC endpoint de interface; CloudTrail, CloudWatch, Config e GuardDuty cobrindo acesso ao segredo | Médio |
| SC-06 | condições de IP em políticas quebram rotação por Lambda e chamadas feitas por serviços em nome do usuário; `aws:SourceVpc`/`SourceVpce` podem negar serviços fora da VPC: testar antes | Médio |
| SC-07 | comandos de CLI com segredo no argumento caem no histórico e nos logs do shell; usar arquivo, stdin ou variável lida do cofre | Médio |

A fonte diz tratar-se de considerações, não de prescrições (V-41). Equivalentes em GCP (Secret Manager) e Azure (Key Vault) não foram lidos nesta cadeia: marque Inferido ao aplicar por analogia.

### Kubernetes (V-42, V-43)

| ID | Verificar | Sev. |
| --- | --- | --- |
| SC-10 | `Secret` não vem cifrado no etcd por padrão: confirmar encryption at rest no provedor (**Não verificável** pelo repositório) | Alto |
| SC-11 | RBAC: `get`, `list` e `watch` em Secrets só para quem precisa (os três são equivalentes na prática); sem wildcard | Alto |
| SC-12 | quem cria Pod, ou Deployment, no namespace lê os Secrets dali: restringir criação de workloads e aplicar Pod Security Baseline ou Restricted onde não se confia em quem cria Pods | Alto |
| SC-13 | restringir o Secret a containers específicos (montar só onde precisa) em vez de `envFrom` amplo | Médio |
| SC-14 | provedor externo: External Secrets Operator (`SecretStore` por namespace, credencial mínima, admission control com OPA ou Kyverno porque o operador roda com privilégios elevados) ou Secrets Store CSI Driver. O valor final no ESO continua num Secret nativo | Médio |
| SC-15 | nenhum `Secret` com `data`/`stringData` versionado em claro | Crítico |

### GitOps (V-34, V-33)

| ID | Verificar | Sev. |
| --- | --- | --- |
| SC-20 | preferir criar o segredo no cluster de destino (Sealed Secrets, ESO, Secrets Store CSI Driver, Vault Secrets Operator) | Alto |
| SC-21 | injeção na geração de manifests (argocd-vault-plugin) deixa os manifests em texto plano no Redis: só com Redis e repo-server isolados por NetworkPolicy (e CNI que a aplique) | Alto |
| SC-22 | Flux: SOPS com `decryption.provider: sops`; a chave de decifragem existe só no cluster | Médio |

Detalhes de Application e Kustomization em `${CLAUDE_PLUGIN_ROOT}/skills/helm-gitops-review/references/gitops.md`.

### Docker e build (V-55)

| ID | Verificar | Sev. |
| --- | --- | --- |
| SC-30 | nenhum segredo em `ARG` ou `ENV` | Crítico |
| SC-31 | `RUN --mount=type=secret,id=<id>` (opções `id`, `target`, `env`; padrão `/run/secrets/<id>`) com `docker build --secret id=<id>,src=<arquivo>` ou `env=<VAR>` | Alto |
| SC-32 | `--ssh default` para repositório privado em vez de copiar a chave | Alto |
| SC-33 | `.dockerignore` exclui `.env`, `*.pem`, state | Alto |
| SC-34 | conferir `docker history --no-trunc` da imagem final (só com autorização; Inferido) | Alto |

### IaC: Terraform, OpenTofu, Pulumi (V-17, V-38, V-39)

| ID | Verificar | Sev. |
| --- | --- | --- |
| SC-40 | `sensitive = true` esconde o valor no `plan`, mas o state o guarda em texto puro: state remoto cifrado com acesso restrito | Alto |
| SC-41 | OpenTofu cifra o state (`key_provider` e `method`); chave fora do repositório; sem a chave o state é irrecuperável | Médio |
| SC-42 | nenhum `default` com valor secreto; `tfvars` com segredo fora do Git | Crítico |
| SC-43 | Pulumi: `--secret` em toda senha de config; provedor de chave (`awskms`, `azurekeyvault`, `gcpkms`, `hashivault`) por stack; ID físico em texto puro; `RandomPassword`, não `RandomString` | Alto |
| SC-44 | Terraform recente: valores efêmeros e argumentos somente-escrita evitam gravar o valor no state; suporte depende da versão do Terraform e do provider (Inferido, não está em V: confirme na documentação) | Informativo |
| SC-45 | ler segredo por `data` de cofre grava o valor lido no state: avaliar o item anterior | Médio |

### CI e shell

| ID | Verificar | Sev. |
| --- | --- | --- |
| SC-50 | segredos do GitHub só em `secrets.*`, no step que precisa; nunca em `echo`; valores derivados (base64, partes) não são mascarados no log (Inferido) | Alto |
| SC-51 | OIDC em vez de chave longa de nuvem (`gha-hardening-review`, GH-05) | Alto |
| SC-52 | segredo digitado em comando fica no histórico e em logs; usar leitura interativa ou arquivo com permissão restrita | Médio |

## Exemplo anotado

Entrada (valores omitidos aqui por regra):

```yaml
# k8s/db-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db
stringData:
  password: <valor omitido>
```

```hcl
# infra/vars.tfvars
db_password = "<valor omitido>"
```

| ID | Sev. | Tipo | Local | Risco | Correção | Rótulo |
| --- | --- | --- | --- | --- | --- | --- |
| SC-15 | Crítico | senha de banco | k8s/db-secret.yaml:7 | Secret em claro no repositório | substituir por `ExternalSecret` (ver abaixo); tratar a senha como exposta | Verificado (valor real: não confirmável sem comparar com o banco; presumir real) |
| SC-42 | Crítico | senha de banco | infra/vars.tfvars:1 | `tfvars` versionado | remover do Git, `.gitignore`, entregar via cofre ou `TF_VAR_` do pipeline | Verificado |
| SC-40 | Alto | state | (backend) | o valor também está no state em texto puro | backend remoto cifrado com acesso restrito | Inferido (backend não recebido) |
| SC-10 | Alto | etcd | (cluster) | sem confirmação de encryption at rest | verificar no provedor | Não verificável |

Rotação: recomendar. Histórico: confirmar com o comando de nomes acima; se o arquivo apareceu em commit anterior, a rotação é obrigatória mesmo depois da remoção.

## Padrões seguros de referência

ExternalSecret (ESO). A versão da API muda entre releases do operador: confirme com `kubectl api-resources | grep -i external-secrets` e use a que o cluster expõe (Inferido; V-43 não registra versão).

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: db
  namespace: pagamentos
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-sm
    kind: SecretStore            # por namespace; credencial mínima (V-43)
  target:
    name: db-credentials
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: pagamentos/prod/db
        property: password
```

Condição de política para quem pode definir resource policy no Secrets Manager (formato conforme a documentação do IAM; confira o nome da chave de condição antes de usar):

```json
{
  "Effect": "Allow",
  "Action": "secretsmanager:PutResourcePolicy",
  "Resource": "*",
  "Condition": { "Bool": { "secretsmanager:BlockPublicPolicy": "true" } }
}
```

## Texto de recomendação de rotação

"O segredo [tipo] de [local] esteve em [Git/imagem/log/state]. Remover o arquivo não o torna seguro, porque ele permanece no histórico e em clones. Recomendo: (1) gerar um novo valor no cofre; (2) atualizar quem o consome; (3) revogar o antigo; (4) conferir logs de acesso do período de exposição. Quem decide e executa é o titular do sistema; não rotacionei nada."
