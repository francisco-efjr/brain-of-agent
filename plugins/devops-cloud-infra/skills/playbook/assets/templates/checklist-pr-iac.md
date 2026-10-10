# Checklist de PR de infraestrutura

<!--
Marque OK, PENDENTE, FALHOU ou N/A (N/A exige motivo). "OK" exige evidência (saída de comando,
link da execução ou trecho). Base: P-22, P-23, V-37, V-53, V-61. O fluxo plan-no-PR vem do tutorial
do HCP Terraform; para Terraform ou OpenTofu autogerido não há fonte genérica validada.
-->

| Campo | Valor |
| --- | --- |
| PR | [LINK] |
| Autor · revisor | [NOMES] |
| Ambiente-alvo | [dev / staging / produção] |

## 1. Qualidade e segurança estática

| # | Item | Status | Evidência |
| --- | --- | --- | --- |
| 1 | `terraform fmt -check`, `validate` e lint (tflint) passam; o tutorial do HCP não os inclui: adicione ao workflow | | |
| 2 | Scanner de IaC (trivy, tfsec ou checkov) sem achado Crítico ou Alto pendente | | |
| 3 | Nenhum segredo em `.tf`, `.tfvars`, defaults, workflows (busca feita; valores não impressos) | | |
| 4 | IAM sem `*` injustificado; sem `0.0.0.0/0` em portas administrativas | | |
| 5 | Recursos com estado têm proteção contra deleção e backup | | |

## 2. Plan e testes

| # | Item | Status | Evidência |
| --- | --- | --- | --- |
| 6 | Plan no PR em modo especulativo (não altera infra), resumo comentado no PR | | |
| 7 | O plan lista criados, alterados, **destruídos e substituídos**; recursos com estado destacados | | |
| 8 | `terraform test` com `command = plan` e mocks (v1.6.0+, mocks v1.7.0+), sem credencial de produção | | |
| 9 | `command = apply` em teste só em conta descartável, com orçamento e aprovação humana | | |
| 10 | Apply só após merge na branch principal e aprovação | | |

## 3. Reprodutibilidade

| # | Item | Status | Evidência |
| --- | --- | --- | --- |
| 11 | `required_version` e `required_providers` fixados; módulos com `version` exata | | |
| 12 | `.terraform.lock.hcl` versionado; `init -upgrade` só neste PR se o objetivo for atualizar providers | | |
| 13 | State remoto com lock; nenhum `-lock=false` | | |

## 4. Custo e operação

| # | Item | Status | Evidência |
| --- | --- | --- | --- |
| 14 | Estimativa de custo no PR (Infracost: estimativa, não garantia) e revisão humana se acima do limite do time | | |
| 15 | Tags de dono e ambiente nos recursos que geram custo | | |
| 16 | Credencial do pipeline sem permissão destrutiva; OIDC ou credencial dinâmica em vez de chave longa (Inferido) | | |

## Parecer

**Recomendação:** [aprovar / aprovar com condições / bloquear]
**Não verificado:** [o que ficou de fora e por quê]
**Condições:** [condição verificável · dono]
