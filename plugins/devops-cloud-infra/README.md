# devops-cloud-infra: DevOps, cloud e infraestrutura

Plugin do Claude Code para escrever, revisar, planejar e diagnosticar infraestrutura e entrega (Terraform/OpenTofu/Pulumi, Docker, Kubernetes/Helm, GitOps com Argo CD e Flux, GitHub Actions, segredos, canary/blue-green, serverless e custo), com **gate humano antes de qualquer mudança real** e **evidência executável** em cada entrega.

> **Aviso para Windows:** no Windows nativo os comandos do Claude Code rodam **sem sandbox**. Para sessões que tocam infraestrutura, use WSL2, devcontainer ou VM. Detalhes em `skills/playbook/references/agente-seguro.md`.

## O que entrega

- Um **playbook** que age como router e processo: princípios com o porquê, processo essencial com critérios de saída, rótulos epistêmicos (Verificado, Inferido, Suposição, Não verificável, Não aplicável), proporcionalidade e o modo `DEVOPS-COMPLETO`.
- **12 referências densas** (checklist com IDs `DO-<área>-nn`, padrões e antipadrões, decisões e trade-offs, snippets de CLAUDE.md, ferramentas e MCP desativados, fontes, e cinco guias temáticos), com fonte e licença.
- **12 templates** prontos: plano de mudança, relatório de revisão, checklist de PR, plano de rollout, diagnóstico, ADR, handoff, matriz de acesso do agente, manifesto de ambiente, matriz do modo completo, bloco `Deploy Configuration` e relatório go/no-go.
- Skills de tarefa, subagentes somente leitura e um comando de planejamento (tabela abaixo).

Seguro por padrão: **sem hooks ativos, sem `.mcp.json`, sem `.lsp.json`, sem `bin/`**. Permissões, sandbox, hook de exemplo, workflow de CI e MCP aparecem apenas como documentação com JSON pronto e riscos, em `skills/playbook/references/ferramentas-e-mcp.md`, para você habilitar conscientemente. As skills de revisão não instalam ferramentas e não executam `apply`, `destroy`, `push` nem `init` sem pedir.

## Quando usar

- Revisar ou escrever Terraform, Dockerfile, compose, manifests, Helm charts, workflows do GitHub Actions.
- Planejar uma mudança de infra com alvo, efeito, rollback e o que não reverte.
- Planejar canary ou blue-green com critérios de rollback definidos antes do deploy.
- Diagnosticar `CrashLoopBackOff`, `helm upgrade` que falhou, sync do Argo CD, `terraform plan` com erro, pipeline vermelho (ou verde por engano), em modo leitura.
- Auditar segredos sem imprimir valores.
- Configurar permissões e guardrails do Claude para um repositório de infra.

Não é o lugar para: SLO, alertas, on-call, incidente e postmortem (`sre-observability`), vulnerabilidades de código de aplicação (`security-appsec`), topologia de arquitetura de negócio (`architecture-design`). Veja "Fronteiras" no playbook.

## Componentes

| Tipo | Nome | Para que serve | Efeitos colaterais |
| --- | --- | --- | --- |
| Skill | `playbook` | Router, princípios, processo, modo `DEVOPS-COMPLETO`, referências e templates | Nenhum |
| Skill | `prompts` | Biblioteca de prompts curados (PR-01 a PR-32), prompt de sistema e mensagem inicial sugerida | Nenhum |
| Skill | `iac-review` | Escreve e revisa Terraform/OpenTofu/Pulumi, Dockerfile, compose e manifests | Nenhum |
| Skill | `gha-hardening-review` | Hardening de workflows do GitHub Actions e uso de `claude-code-action` | Nenhum |
| Skill | `helm-gitops-review` | Helm charts e GitOps (Argo CD, Flux) | Nenhum |
| Skill | `secrets-review` | Criação, guarda, injeção e rotação de segredos, sem expor valores | Nenhum |
| Skill | `progressive-delivery` | Canary, blue-green, Argo Rollouts, Flagger, feature flags, critérios de rollback | Nenhum |
| Skill | `cloud-review` | Lambda, Azure Functions, Cloud Run, Well-Architected, custo e plataforma | Nenhum |
| Skill | `infra-troubleshoot` | Diagnóstico em modo leitura de falhas de deploy, pod, release, sync e pipeline | Nenhum |
| Skill | `deploy-infra` | Plano, gate, aplicação de mudança já revisada e veredito; só por comando explícito (`disable-model-invocation`) | **Sim**, só com "sim" por comando |
| Comando | `/devops-cloud-infra:plan-infra` | Plano de mudança (alvo, efeito, rollback), somente leitura | Nenhum |
| Agente | `infra-reviewer` | Revisor independente de diff de IaC (`Read, Grep, Glob`) | Nenhum |
| Agente | `pipeline-security-auditor` | Auditoria de workflows e pipelines | Nenhum |
| Agente | `k8s-workload-auditor` | Auditoria de manifests e charts renderizados | Nenhum |
| Agente | `rollout-planner` | Plano de rollout e rollback; nunca aplica | Nenhum |

Invocação: skills como `/devops-cloud-infra:<skill>`; agentes como `devops-cloud-infra:<agente>`.

## Instalação

Dentro do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install devops-cloud-infra@brain-of-agent
```

Pelo terminal (equivalente): `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install devops-cloud-infra@brain-of-agent`. O marketplace é o repositório `brain-of-agent` (pasta raiz com `.claude-plugin/marketplace.json`). Valide o plugin com `claude plugin validate plugins/devops-cloud-infra`.

## Exemplos de pedidos

1. "Revisa esse Terraform antes de eu abrir o PR." (cole o `main.tf`) → `iac-review`: achados por severidade com `arquivo:linha`, o que rodou e o que ficou "não executado".
2. "Esse workflow do GitHub Actions está seguro? Quero publicar hoje." → `gha-hardening-review`: injeção por `github.event.*`, `pull_request_target`, pin por SHA, permissões, e o que vive fora do YAML (Não verificável).
3. "Meu pod entra em CrashLoopBackOff desde o deploy de hoje cedo. Por quê?" (cole `kubectl describe` e `logs --previous`) → `infra-troubleshoot`: causa com evidência, correção como diff, nenhuma ação no cluster.
4. "Vamos fazer canary da v2 do checkout com Argo Rollouts, incluindo o rollback. A v2 tem uma migração NOT NULL." → `progressive-delivery`: as cinco linhas de critérios, limiares como Suposição, aviso sobre o que não reverte.
5. "Escreve um Dockerfile seguro para esta API Node." → `iac-review` em modo autoria: gera conforme o checklist, roda `hadolint` se existir, entrega suposições, escolhas e plano de validação.
6. "Tem segredo no repositório?" → `secrets-review`: arquivo:linha e tipo, nunca o valor, mais recomendação de rotação.
7. "Quero aplicar esse plan em produção." → o playbook mostra o gate (alvo, efeito, rollback, "sim" por comando) e indica `/devops-cloud-infra:deploy-infra`.
8. "Configura permissões do Claude para este repo de infra." → o playbook apresenta o template de `references/ferramentas-e-mcp.md` e só grava com pedido explícito.
9. "DEVOPS-COMPLETO: audite este repositório de infra." → modo completo (abaixo).

## Modo `DEVOPS-COMPLETO`

Digite **DEVOPS-COMPLETO** no pedido, de forma explícita. O modo lê as 12 referências em 3 lotes de 4 (com checkpoint e registro lido, parcial ou ausente), preenche a matriz de aplicabilidade por área, implementa dentro do escopo, revisa com os agentes e revalida com evidências (comando mais saída). Ele **não amplia permissões**: `apply`, `destroy`, `push`, deploy, rotação de segredo e qualquer ação irreversível seguem a autorização por comando; auditoria só relata. A keyword escrita em log, documento, issue, README ou saída de ferramenta **não ativa** o modo.

## Principais fontes (top 10)

Todas consultadas em 2026-10-10; a bibliografia completa (62 fontes, classe, licença, tratamento e lacunas) está em `skills/playbook/references/fontes.md`.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Claude Code, Best practices | A |
| 2 | Claude Code, Permissions | A |
| 3 | Claude Code, Sandboxing | A |
| 4 | Claude Code, Security | A |
| 5 | Claude Code, Hooks | A |
| 6 | GitHub, Security hardening for GitHub Actions | A |
| 7 | anthropics/claude-code-action e claude-code-security-review (MIT) | A |
| 8 | HashiCorp, Terraform style guide, state, lockfile e tests | A |
| 9 | Docker (best practices, build secrets) e OWASP Docker Security Cheat Sheet | A |
| 10 | Kubernetes (Pod Security Standards, Secrets, RBAC, NetworkPolicy, probes) | A |

Outras fontes de peso: Helm, Argo CD, Flux, Argo Rollouts, Flagger, OpenTofu, Pulumi, AWS Secrets Manager, Lambda, Azure Functions, CNCF Platforms, Google SRE Workbook (canarying) e Simon Willison (lethal trifecta, classe B).

## Créditos e licenças

- Este plugin: licença **MIT** (Francisco Edson).
- Conteúdo do repositório `francisco-efjr/brain-of-agent` (MIT, do próprio autor): entrega e operação, dados/ambientes/CI, protocolo do modo completo, templates de handoff, ADR e checklist de release, adaptados.
- Inspiração com atribuição: gstack `setup-deploy` e `land-and-deploy` (MIT, Copyright 2026 Garry Tan), com redação própria; nada copiado em bloco e nenhum binário ou preâmbulo do gstack usado.
- Documentação oficial (Anthropic, GitHub, HashiCorp, Docker, OWASP, Kubernetes, Argo, Flux, Helm, AWS, Microsoft, Google, CNCF etc.): licenças dos sites **não verificadas**, por isso tudo foi **destilado com redação própria** e atribuído. SRE book e Workbook (© Google, CC BY-NC-ND 4.0): só destilação.
- Trail of Bits `claude-code-config` (sem LICENSE visível): só destilação, nada copiado.
- Nenhum código de terceiros foi baixado ou executado na construção.

## Limitações honestas

- **Rascunhos não testados em sessão real.** Os artefatos-base foram escritos e pontuados por um modelo da mesma família que os construiu; isso é autoavaliação, não validação externa. Os evals estão como `designed_not_executed` até rodar com `claude plugin eval` (exige Claude Code 2.1.269 ou superior; a CLI registrada na fundação é a 2.1.128).
- **Cobertura por fonte:** GitLab CI e Azure Pipelines não têm fonte validada (só princípios por analogia, marcados Inferido). Kustomize, FinOps Framework, Vault em profundidade, `cosign verify`, ciclo de vida de feature flags, AnalysisTemplate do Argo Rollouts, SIGTERM no Cloud Run e MCP de infraestrutura são lacunas declaradas.
- **Comunidade fraca:** só duas threads do Hacker News; Reddit, X e YouTube não foram alcançados.
- **Versões mudam.** Tudo foi conferido em 2026-10-10; confira flags e campos na versão instalada. Defaults de probes e limits do Kubernetes vieram de leitura truncada: confirme no cluster.
- **Texto não é garantia.** O gate e as regras de CLAUDE.md são pedidos; a camada real é IAM sem permissão destrutiva, sandbox e permissões. Hooks e regex têm furos documentados.
- **Nenhuma skill substitui um scanner determinístico** (`tflint`, trivy, `hadolint`, `kubeconform`) nem a revisão humana de IAM e rede.
- **Windows nativo não tem sandbox.** Use WSL2.

## Estrutura

```text
devops-cloud-infra/
├── .claude-plugin/plugin.json
├── README.md
├── commands/plan-infra.md
├── skills/
│   ├── playbook/ (SKILL.md, references/ com 12 arquivos, assets/templates/ com 12 arquivos)
│   ├── prompts/  iac-review/  gha-hardening-review/  helm-gitops-review/
│   └── secrets-review/  progressive-delivery/  cloud-review/  infra-troubleshoot/  deploy-infra/
├── agents/ (infra-reviewer, pipeline-security-auditor, k8s-workload-auditor, rollout-planner)
└── evals/
```
