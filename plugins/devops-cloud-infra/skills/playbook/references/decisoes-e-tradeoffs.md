# Decisões e trade-offs de infraestrutura

Cada decisão tem critério de escolha, trade-off e o que registrar. O plugin não impõe ferramenta: a stack do projeto prevalece. Para registrar uma decisão material use `assets/templates/adr-infra.md`. Topologia de negócio, limites de serviço e multi-região são de `architecture-design`.

Rótulos: Verificado (fonte lida), Inferido, Suposição. Versões e flags: conferir na instalada.

## Sumário

- [Terraform x OpenTofu x Pulumi](#terraform-x-opentofu-x-pulumi)
- [Blue-green x canary](#blue-green-x-canary)
- [Sync automático por ambiente (Argo CD) e Argo x Flux](#sync-automático-por-ambiente-argo-cd-e-argo-x-flux)
- [Segredos: ESO x CSI x Sealed Secrets x injeção na geração](#segredos-eso-x-csi-x-sealed-secrets-x-injeção-na-geração)
- [Chave KMS gerenciada x do cliente](#chave-kms-gerenciada-x-do-cliente)
- [Plano de hospedagem serverless](#plano-de-hospedagem-serverless)
- [Cobrança por requisição x por instância (Cloud Run)](#cobrança-por-requisição-x-por-instância-cloud-run)
- [Pin x "última versão estável"](#pin-x-última-versão-estável)
- [Repositório de config: mono x separado](#repositório-de-config-mono-x-separado)
- [Quanta autonomia dar ao agente](#quanta-autonomia-dar-ao-agente)
- [Revisão por agente x scanner determinístico](#revisão-por-agente-x-scanner-determinístico)
- [Rollback x correção para frente](#rollback-x-correção-para-frente)

## Terraform x OpenTofu x Pulumi

| Critério | Terraform | OpenTofu | Pulumi |
| --- | --- | --- | --- |
| Linguagem | HCL | HCL (migração em 4 passos: backup, instalar, `init` e verificar, testar com mudança pequena) | Linguagens de programação gerais |
| Criptografia de state | Não é recurso do Terraform (state em texto puro; `sensitive` só oculta saída) | Recurso exclusivo: `key_provider` (pbkdf2, aws_kms, gcp_kms, azure_vault, openbao, external), `method` (aes_gcm, external, unencrypted), `fallback`, `enforced`, `TF_ENCRYPTION` | Secrets cifrados onde ficam (provedores `awskms`, `azurekeyvault`, `gcpkms`, `hashivault`); ID físico do recurso fica em texto puro |
| Testes | `terraform test` (v1.6.0+; mocks v1.7.0+) | Consulte a doc da versão (não lida) | Testes na linguagem escolhida (não lido) |
| State | Remoto com lock, se o backend suportar | Idem; atenção a `terraform_remote_state` na migração | Pulumi Cloud por padrão; DIY em S3, Azure Blob, GCS, PostgreSQL ou arquivo; `PULUMI_BACKEND_URL` |

Quando escolher (Inferido, a partir das capacidades verificadas): fique no que o repositório já usa; migre só por motivo concreto. OpenTofu quando a criptografia nativa de state é requisito, lembrando que sem a chave o state e o plan são irrecuperáveis. Pulumi quando a equipe quer lógica em linguagem geral e aceita o modelo de backend e secrets. Terraform quando o ecossistema, o HCP Terraform ou o fluxo `plan` no PR do tutorial HashiCorp (V-61) já são a base. Registrar: versão exata da ferramenta, backend, quem tem acesso ao state e à chave. Fontes: V-17, V-35 a V-39.

## Blue-green x canary

| Condição | Escolha | Observação |
| --- | --- | --- |
| A troca precisa ser atômica, ou a aplicação não convive com duas versões | Blue-green | A versão nova só recebe tráfego depois do teste |
| A aplicação convive com duas versões e há métricas confiáveis | Canary | Divisão por cabeçalho HTTP exige traffic manager (ingress ou service mesh) |
| Equipe começando, métricas imaturas | Blue-green e migrar para canary conforme cresce a confiança | Sugestão da doc do Argo Rollouts (V-44) |

Antes de qualquer um, preencha as cinco linhas de `assets/templates/plano-rollout-rollback.md` (métricas poucas e percebidas pelo usuário; controle em paralelo mais SLO; duração e tamanho representativos incluindo pico; gatilhos automático e humano; rollback e o que não reverte). Flagger e Argo Rollouts são compatíveis nesse ponto quando a condição é explícita (K8, em `fontes.md`). A migração de schema que impede a versão anterior de ler os dados (por exemplo, coluna NOT NULL) quebra o rollback: use expandir, migrar, contrair (`database-data-modeling`). Fontes: V-44, V-45, V-46.

## Sync automático por ambiente (Argo CD) e Argo x Flux

Decida por ambiente, não globalmente:

| Ambiente | Sync automático | Prune | Self-heal |
| --- | --- | --- | --- |
| Dev, staging | Aceitável | Aceitável, revisado | Aceitável |
| Produção | Só se deploy sem clique for aceito pela organização | Explícito e revisado (por padrão não apaga) | Decisão consciente: reverte mudança manual após o timeout (5 s) |

Rollback em GitOps é novo commit; com sync automático, o rollback pela UI do Argo CD fica bloqueado (V-31). Argo CD e Flux resolvem o mesmo problema com modelos diferentes: Argo traz UI e `ApplicationSet`; Flux é um conjunto de controllers (fontes `GitRepository`, `OCIRepository`, `HelmRepository`, `Bucket`; `Kustomization`), com SOPS nativo via `decryption.provider: sops` (V-33). Escolha pelo que a equipe já opera e por como lida com segredos (Argo não cita SOPS na página de segredos, V-34). Não cite o default de `interval` do Flux: as páginas divergem (K10). Registrar: política por ambiente, quem pode editar a config, como mudança manual é tratada.

## Segredos: ESO x CSI x Sealed Secrets x injeção na geração

| Opção | Ideia | Cuidado |
| --- | --- | --- |
| External Secrets Operator | `SecretStore` (por namespace) e `ExternalSecret`; mantém o Secret nativo atualizado | O valor final vira Secret nativo; o ciclo de vida do segredo está fora do escopo; o operador roda com privilégios elevados: credencial mínima e admission control (OPA ou Kyverno) (V-43) |
| Secrets Store CSI Driver | Monta o segredo no Pod | Confira rotação e versão do driver na doc (não lida em profundidade) |
| Sealed Secrets | Segredo cifrado no Git, decifrado no cluster | Chave do controller vira ativo crítico de backup (Inferido) |
| Vault Secrets Operator | Segredos do Vault no cluster | A página do Vault lida não trata de secrets engines, leases e TTL (lacuna) |
| Injeção na geração de manifests (argocd-vault-plugin) | Segredo entra ao gerar o manifest | Desencorajado: manifest com segredo fica em texto plano no Redis do Argo (V-34) |

Regra: preferir criar o segredo no cluster de destino (V-34 recomenda fortemente). Fontes: V-34, V-42, V-43.

## Chave KMS gerenciada x do cliente

`aws/secretsmanager` (gerenciada) na maioria dos casos, sem custo; chave do cliente quando há acesso entre contas ou necessidade de política de chave própria, com `kms:ViaService` e encryption context (V-41). A fonte descreve considerações, não prescrições: registre a razão da escolha.

## Plano de hospedagem serverless

| Plataforma | Decisão que pesa | Fonte |
| --- | --- | --- |
| Azure Functions | O plano é escolhido no início (troca limitada, sobretudo entre Consumption e Elastic Premium); Flex Consumption quando possível; cold start tratado por plano (always ready no Flex, warmup trigger no Premium, duas instâncias e Health Check no Dedicated) | V-49 |
| Lambda | Reserved concurrency (0 para parar recursão), provisioned concurrency com custo, memória por teste (AWS Lambda Power Tuning) | V-48 |
| Cloud Run | Concorrência (padrão 80), startup CPU boost, instâncias mínimas | V-50 |

Quotas e limites por plano: Não verificado até conferir na doc atual do provedor.

## Cobrança por requisição x por instância (Cloud Run)

No modo por requisição, a CPU fora da resposta é limitada: trabalho em background pede cobrança por instância (V-50). Registrar: padrão de uso (picos, trabalho pós-resposta) e custo estimado com a calculadora do provedor (Não verificado aqui).

## Pin x "última versão estável"

Fixe. O repositório de instruções do awesome-copilot sugere "última versão estável" para Terraform; o guia da HashiCorp manda fixar providers, módulos e `required_version`. A fonte oficial prevalece (K1). Atualize por PR dedicado (`init -upgrade`), com lockfile versionado. Fontes: V-17, V-18, V-36.

## Repositório de config: mono x separado

Separado do código da aplicação: CI sem loops, auditoria limpa, acessos distintos (V-22). Mono-repo é aceitável quando o time é único e a pipeline evita laços (Inferido); registre o motivo. Bases remotas de kustomize sempre por `?ref=`.

## Quanta autonomia dar ao agente

| Nível | Quando | Garantia necessária |
| --- | --- | --- |
| Somente leitura (get, describe, plan, diff) | Revisão e diagnóstico | Credencial somente leitura (IAM), `deny` de Secrets |
| Escrita em repositório, sem tocar ambiente | Modo autoria | Revisão do diff, checks existentes, sem `apply` |
| Staging com "sim" por comando | Validação de mudança | Gate, credencial limitada, alvo confirmado |
| Produção | Somente via pipeline humano | IAM sem escrita para o agente |

Detalhes em `agente-seguro.md`. Autonomia irrestrita (`--dangerously-skip-permissions`) não é opção padrão: risco, só em sandbox e repositório confiável (V-29, K3).

## Revisão por agente x scanner determinístico

O agente cobre contexto e intenção (requisito não implementado, IAM largo para o propósito); scanners (`tflint`, trivy, tfsec, checkov, `hadolint`, `kubeconform`) cobrem regras fixas de forma repetível. Use ambos e diga qual rodou. Um revisor do mesmo modelo não é validação externa (V-06). Fontes: V-18, V-20.

## Rollback x correção para frente

Rollback quando a versão anterior é compatível com o schema e com os dados gravados; correção para frente quando reverter não é seguro, com decisão explícita do responsável (brain `entrega-e-operacao`). Em GitOps, ambos são commits. Registrar no plano o que não reverte.
