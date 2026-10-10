# Terraform, OpenTofu e Pulumi: checklist de revisão e autoria

Conferido em 2026-10-10 contra as páginas oficiais citadas em V-17 e V-35 a V-39. As páginas marcam Terraform v1.16.x como versão mais recente na data da leitura; confirme a versão instalada com `terraform version` (ou `tofu version`, `pulumi version`). Destilação com redação própria; nenhuma passagem é cópia literal.

## Sumário

- [Checklist TF-nn](#checklist-tf-nn)
- [Leitura de um plan](#leitura-de-um-plan)
- [Exemplo anotado](#exemplo-anotado)
- [Esqueleto de autoria](#esqueleto-de-autoria)
- [terraform test](#terraform-test)
- [OpenTofu e Pulumi](#opentofu-e-pulumi)

## Checklist TF-nn

Severidade é o padrão; ajuste ao contexto e diga por quê. "Detectar" usa as ferramentas Grep/Read; em achados de segredo, use `files_with_matches` e mostre só tipo e `arquivo:linha`.

| ID | Verificar | Detectar | Sev. | Fonte |
| --- | --- | --- | --- | --- |
| TF-01 | `terraform fmt -check -recursive` e `validate` passam; 2 espaços; nomes em snake_case que não repetem o tipo (`aws_s3_bucket.logs`, não `aws_s3_bucket.logs_bucket`) | rodar | Baixo | V-17 |
| TF-02 | toda `variable` tem `type` e `description`; segredos com `sensitive = true` **e** state remoto cifrado de acesso restrito | `variable "` sem `type`; nomes com `password`, `token`, `secret` | Médio; Crítico se há valor `default` secreto | V-17 |
| TF-03 | `required_version` no bloco `terraform`; providers em `required_providers` com restrição; módulos com `version` exata | `required_providers`, `source =` de módulo sem `version` | Alto | V-17, V-36 |
| TF-04 | `.terraform.lock.hcl` versionado, com hashes de todas as plataformas do time (`terraform providers lock -platform=linux_amd64 -platform=darwin_arm64`); `init -upgrade` só em PR dedicado | `git ls-files .terraform.lock.hcl` | Alto | V-36 |
| TF-05 | backend remoto com lock; sem `-lock=false` em scripts e CI; `force-unlock` só com o lock próprio e o ID verificado | `-lock=false`, `force-unlock` em `Makefile`/workflows | Alto | V-35 |
| TF-06 | `*.tfstate`, `*.tfvars` com segredo e `.terraform/` fora do Git | `git ls-files '*.tfstate*' '*.tfvars'`, `.gitignore` | Crítico | V-17, V-35 |
| TF-07 | recurso com estado (banco, volume, bucket, fila) com proteção: `deletion_protection`/`prevent_destroy`, backup e snapshot final | `aws_db_instance`, `google_sql_database_instance`, `azurerm_*` sem proteção | Crítico se o `plan` destrói; Alto caso contrário | V-27; atributo varia por provider (Inferido) |
| TF-08 | IAM sem `*` em `Action` e `Resource`; funções com o mínimo necessário | `"\*"`, `actions = \["\*"\]`, `Resource.*\*` | Crítico | V-48, V-42 |
| TF-09 | regras de rede sem `0.0.0.0/0` ou `::/0` em portas administrativas (22, 3389) e de banco (3306, 5432, 6379, 27017) | `0\.0\.0\.0/0`, `::/0` | Crítico | V-09 (instrução de varredura), Inferido |
| TF-10 | credencial do pipeline sem permissão destrutiva; OIDC no lugar de chave longa | provider com `access_key`/`secret_key` | Alto | V-61 (Inferido), V-28 |
| TF-11 | tags de dono e ambiente nos recursos que geram custo | `tags` ausente; `default_tags` no provider | Médio | V-53 |
| TF-12 | testes `.tftest.hcl` com `command = plan` e mocks; `apply` só em conta descartável | `tests/*.tftest.hcl` | Médio | V-37 |
| TF-13 | pipeline `fmt` -> `validate` -> `tflint` -> scanner (trivy, tfsec ou checkov) no PR; plan especulativo comentado no PR | `.github/workflows` | Médio | V-18, V-61 |
| TF-14 | ordem dos argumentos: `count`/`for_each`, parâmetros, blocos, `lifecycle`, `depends_on` | leitura | Baixo | V-17 |

Conflito resolvido (K1): o arquivo de instruções do awesome-copilot recomenda "última versão estável"; a HashiCorp manda fixar. Siga a HashiCorp e atualize por PR dedicado.

Backend S3: versões recentes do Terraform oferecem lock nativo (`use_lockfile`) além do DynamoDB; confirme na documentação do backend e na sua versão (Inferido: não está em V).

## Leitura de um plan

Entrada: texto colado pelo usuário (`terraform plan -no-color`) ou `terraform show -json tfplan`. Você não gera o plan.

1. Resumo final: `Plan: A to add, B to change, C to destroy.` C maior que zero exige leitura linha a linha.
2. Marcadores por recurso: `+` cria, `~` altera, `-` destrói, `-/+` destrói e recria. `# X must be replaced` com `# forces replacement` nomeia o atributo que causa a troca.
3. Em JSON, `resource_changes[].change.actions` com `["delete","create"]` (ou `["create","delete"]`, com `create_before_destroy`) é substituição.
4. Para cada destruição ou troca, responda: tem estado? há `prevent_destroy`/proteção? existe backup restaurável? o dado é recriável?
5. `plan` limpo não prova ausência de efeito: drift e dependências externas ficam de fora (rótulo Inferido).

Resultado esperado no relatório: lista "recursos criados / alterados / destruídos / substituídos" e a pergunta de decisão ao humano quando houver destruição com estado.

## Exemplo anotado

Entrada (`infra/db.tf`, exemplo didático):

```hcl
variable "db_password" {
  default = "troque-me-123"
}

resource "aws_db_instance" "main" {
  identifier          = "pagamentos"
  engine              = "postgres"
  instance_class      = "db.t3.medium"
  username            = "app"
  password            = var.db_password
  publicly_accessible = true
  skip_final_snapshot = true
}

resource "aws_vpc_security_group_ingress_rule" "pg" {
  security_group_id = aws_security_group.db.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 5432
  to_port           = 5432
  ip_protocol       = "tcp"
}
```

Achados esperados:

| ID | Sev. | Local | Evidência | Correção | Rótulo |
| --- | --- | --- | --- | --- | --- |
| IAC-01 | Crítico | db.tf:1-3 | `default` com valor de senha numa variável sem `type`/`description`/`sensitive` | remover o `default`; `sensitive = true`; entregar o valor por secret manager; tratar como segredo exposto e recomendar rotação | Verificado |
| IAC-02 | Crítico | db.tf:11 | `publicly_accessible = true` | `false`, subnet privada | Verificado |
| IAC-03 | Crítico | db.tf:17 | porta 5432 aberta a `0.0.0.0/0` | CIDR da aplicação ou SG de origem | Verificado |
| IAC-04 | Alto | db.tf:12 | `skip_final_snapshot = true` e sem `deletion_protection` | `deletion_protection = true`, snapshot final, `backup_retention_period` > 0 | Verificado; nome do atributo por provider: Inferido |
| IAC-05 | Médio | db.tf:5 | sem `tags` de dono | `tags` ou `default_tags` | Verificado |
| IAC-06 | Alto | (módulo raiz) | não há `required_providers`/lockfile no trecho recebido | pedir os demais arquivos | Não verificável |

A senha no `default` vai parar no state em texto puro mesmo com `sensitive = true` (V-17): o achado IAC-01 pede state cifrado, não só a anotação.

## Esqueleto de autoria

Valores de versão são exemplos: confirme no registry e na sua política antes de fixar.

```hcl
terraform {
  required_version = ">= 1.7.0, < 2.0.0"   # 1.7+ para mocks em terraform test

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"                   # exemplo; confira a major vigente
    }
  }

  backend "s3" {}                          # parâmetros por -backend-config; sem credenciais no código
}

variable "senha_banco" {
  type        = string
  description = "Senha do usuário da aplicação. Vem do secret manager, nunca de default."
  sensitive   = true
}

resource "aws_db_instance" "principal" {
  count = var.criar_banco ? 1 : 0          # count/for_each primeiro (V-17)

  identifier              = "pagamentos"
  password                = var.senha_banco
  publicly_accessible     = false
  deletion_protection     = true
  backup_retention_period = 7
  skip_final_snapshot     = false

  lifecycle {
    prevent_destroy = true
  }
}
```

Depois de gerar: `terraform fmt -check`, `terraform validate` (se houver `.terraform/`), `tflint`. Entregue o que não rodou como "não executado".

## terraform test

Disponível desde a 1.6.0; mocks desde a 1.7.0 (V-37). `command = plan` não cria infraestrutura; o padrão é `apply`, que cria (GT-11).

```hcl
# tests/bucket.tftest.hcl
mock_provider "aws" {}

run "bucket_bloqueia_acesso_publico" {
  command = plan

  assert {
    condition     = aws_s3_bucket_public_access_block.this.block_public_acls == true
    error_message = "o bucket deve bloquear ACLs públicas"
  }
}
```

Adapte o endereço do recurso ao módulo testado. Para condições customizadas de falha esperada use `expect_failures` (vale só para a operação do `command`, e é recomendado com `plan`). Paralelismo exige `parallel = true`, runs sem referência a outputs uns dos outros e `state_key` distinto.

## OpenTofu e Pulumi

- OpenTofu: migração em 4 passos (backup, instalar, `init` e verificar, testar com mudança pequena), com cuidado extra em `terraform_remote_state` (V-38). Criptografia de state é recurso exclusivo do OpenTofu: `key_provider` (pbkdf2, aws_kms, gcp_kms, azure_vault, openbao, external), `method` (aes_gcm), `fallback` para rotação, `enforced` depois da migração, `TF_ENCRYPTION` que prevalece sobre o código. Antes de ativar: backup sem criptografia, chave fora do repositório, teste de leitura. Sem a chave, state e plan são irrecuperáveis.
- Pulumi: `pulumi preview` no PR; `pulumi refresh` quando houve mudança fora do Pulumi e antes de `destroy`; segredos com `--secret` na config; o ID físico do recurso fica em texto puro; `RandomPassword` e não `RandomString`; backend DIY (S3, Azure Blob, GCS) com versionamento e acesso restrito, sem as garantias transacionais do Pulumi Cloud; `pulumi stack migrate` exige CLI 3.254.0+ (V-39, correção 14).
