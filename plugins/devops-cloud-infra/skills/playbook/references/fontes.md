# Fontes, licenças e lacunas

Bibliografia validada que sustenta o plugin `devops-cloud-infra`. Todas as fontes web foram consultadas em **2026-10-10** pela cadeia de pesquisa do projeto (pesquisadores, validador e sintetizador, todos modelos Claude: a independência é parcial). As fontes do brain-of-agent (conteúdo do usuário, MIT) e do gstack (MIT, Garry Tan) foram lidas em **2026-10-09** a partir do snapshot local.

Como ler: **Classe** A = oficial/autoridade da tecnologia; B = especialista, repositório avaliado ou doc secundária; C = apenas sinal ou ideia. O número entre parênteses é a nota da rubrica de fontes (0 a 10). **Tratamento**: "destilado" = redação própria com atribuição (nenhum trecho literal); "literal" = texto de autoria da casa (MIT do repositório). Documentação oficial de sites teve **licença não verificada**: sempre destilada. Nenhum código de terceiros foi baixado ou executado. Comandos de exemplo vistos em páginas (`cosign sign`, `kubectl label`, `curl | bash` de READMEs) foram tratados como dado e não seguidos.

## Sumário

- [Fontes V-01 a V-29 (rodada 1)](#fontes-v-01-a-v-29-rodada-1)
- [Fontes V-30 a V-62 (rodada 2)](#fontes-v-30-a-v-62-rodada-2)
- [Brain-of-agent e gstack (conteúdo reaproveitado)](#brain-of-agent-e-gstack-conteúdo-reaproveitado)
- [Itens rejeitados e rebaixados](#itens-rejeitados-e-rebaixados)
- [Conflitos entre fontes e resolução (K1 a K15)](#conflitos-entre-fontes-e-resolução-k1-a-k15)
- [Artefatos da casa (P-01 a P-23)](#artefatos-da-casa-p-01-a-p-23)
- [Lacunas conhecidas](#lacunas-conhecidas)
- [Limitações das fontes](#limitações-das-fontes)

## Fontes V-01 a V-29 (rodada 1)

| ID | Título | URL | Classe | Licença | Tratamento |
| --- | --- | --- | --- | --- | --- |
| V-01 | GitHub, Security hardening for GitHub Actions (+ awesome-copilot, instruções de Actions) | https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions · https://github.com/github/awesome-copilot/blob/main/instructions/github-actions-ci-cd-best-practices.instructions.md | A (8) | docs GitHub: não verificada; awesome-copilot MIT | destilado |
| V-02 | Claude Code, Hooks | https://code.claude.com/docs/en/hooks | A (9) | docs Anthropic: não verificada | destilado |
| V-03 | Claude Code, Permissions | https://code.claude.com/docs/en/permissions | A (9) | idem | destilado |
| V-04 | Claude Code, Sandboxing | https://code.claude.com/docs/en/sandboxing | A (9) | idem | destilado |
| V-05 | Claude Code, Security | https://code.claude.com/docs/en/security | A (9) | idem | destilado |
| V-06 | Claude Code, Best practices | https://code.claude.com/docs/en/best-practices | A (9) | idem | destilado |
| V-07 | anthropics/claude-code-action (usage, solutions) | https://github.com/anthropics/claude-code-action | A (8) | MIT; 9,5 mil estrelas | destilado |
| V-08 | claude-code-action, docs/security.md | https://github.com/anthropics/claude-code-action/blob/main/docs/security.md | A (8) | MIT | destilado |
| V-09 | anthropics/claude-code-security-review | https://github.com/anthropics/claude-code-security-review | A (8) | MIT; 6,3 mil estrelas | destilado |
| V-10 | Anthropic, Building effective agents (19 dez 2024) | https://www.anthropic.com/engineering/building-effective-agents | A (9) | não verificada | destilado |
| V-11 | Claude Code, Skills; anthropics/skills | https://code.claude.com/docs/en/skills · https://github.com/anthropics/skills | A (8) | Apache-2.0 em muitas skills; 180,2 mil estrelas | destilado |
| V-12 | Claude Code, Sub-agents | https://code.claude.com/docs/en/sub-agents | A (8) | não verificada | destilado |
| V-13 | Thariq Shihipar, Lessons from building Claude Code: how we use skills (2026-06-03) | https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/ | B (7) | blog; domínio não confirmado como oficial além da autoria | destilado |
| V-14 | Claude Code power user tips; Common workflows | https://support.claude.com/en/articles/14554000-claude-code-power-user-tips · https://code.claude.com/docs/en/common-workflows | A (8) | não verificada | destilado |
| V-15 | Trail of Bits, claude-code-config | https://github.com/trailofbits/claude-code-config | B (5) | sem LICENSE visível; 2,1 mil estrelas | destilado (nunca copiar) |
| V-16 | Simon Willison, The lethal trifecta (2025-06-16) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | B (7) | blog | destilado |
| V-17 | HashiCorp, Terraform style guide | https://developer.hashicorp.com/terraform/language/style | A (9) | não verificada | destilado |
| V-18 | awesome-copilot, instruções de Terraform | https://github.com/github/awesome-copilot/blob/main/instructions/terraform.instructions.md | B (6) | MIT; 39,9 mil estrelas | destilado |
| V-19 | Docker, Building best practices | https://docs.docker.com/build/building/best-practices/ | A (9) | não verificada | destilado |
| V-20 | OWASP, Docker Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html | A (8) | não verificada | destilado |
| V-21 | Kubernetes, Pod Security Standards e Admission | https://kubernetes.io/docs/concepts/security/pod-security-standards/ · https://kubernetes.io/docs/concepts/security/pod-security-admission/ | A (9) | docs do projeto: não verificada | destilado |
| V-22 | Argo CD, Best practices | https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/ | A (8) | não verificada | destilado |
| V-23 | AWS Well-Architected Framework (introdução, 6 nov 2024) | https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html | B | não verificada | destilado |
| V-24 | gstack (Garry Tan), careful, freeze, guard | https://github.com/garrytan/gstack | B (7) | MIT; 135,7 mil estrelas | destilado |
| V-25 | LukasNiessen, kubernetes-skill | https://github.com/LukasNiessen/kubernetes-skill | B (5) | MIT; 446 estrelas | destilado (só o processo) |
| V-26 | Amplifying, What Claude Code picks (fev/2026) | https://amplifying.ai/research/claude-code-picks | B (6) | não verificada | destilado |
| V-27 | Hacker News, banco de produção apagado com Terraform | https://hn.algolia.com/api/v1/items/47278720 | C (5) | n/a | só sinal, nunca fato técnico |
| V-28 | Ask HN, acesso SSH/DB a LLMs | https://hn.algolia.com/api/v1/items/46620990 | B (5) | n/a | destilado |
| V-29 | Armin Ronacher, Agentic coding (2025-06-12) | https://lucumr.pocoo.org/2025/6/12/agentic-coding/ | C (4) | blog | só a ideia dos scripts; permissões desativadas: rejeitado |

## Fontes V-30 a V-62 (rodada 2)

| ID | Título | URL | Classe | Licença | Tratamento |
| --- | --- | --- | --- | --- | --- |
| V-30 | Helm, chart best practices (templates, values, rbac), `helm lint`, `helm template` | https://helm.sh/docs/chart_best_practices/templates/ · https://helm.sh/docs/helm/helm_lint/ · https://helm.sh/docs/helm/helm_template/ | A (8) | não verificada | destilado |
| V-31 | Argo CD, Automated sync | https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/ | A (8) | não verificada | destilado |
| V-32 | Argo CD, ApplicationSet | https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/ | A (8) | idem | destilado |
| V-33 | Flux, Concepts e Kustomization | https://fluxcd.io/flux/concepts/ · https://fluxcd.io/flux/components/kustomize/kustomizations/ | A (8) | idem | destilado |
| V-34 | Argo CD, Secret management | https://argo-cd.readthedocs.io/en/stable/operator-manual/secret-management/ | A (8) | idem | destilado |
| V-35 | Terraform, Remote state e State locking | https://developer.hashicorp.com/terraform/language/state/remote | A (9) | não verificada | destilado |
| V-36 | Terraform, Dependency lock file | https://developer.hashicorp.com/terraform/language/files/dependency-lock | A (9) | idem | destilado |
| V-37 | Terraform, Tests | https://developer.hashicorp.com/terraform/language/tests | A (8) | idem | destilado |
| V-38 | OpenTofu, Migration e State encryption | https://opentofu.org/docs/intro/migration/ · https://opentofu.org/docs/language/state/encryption/ | A (8) | licença do software não verificada | destilado |
| V-39 | Pulumi, State and backends; Secrets | https://www.pulumi.com/docs/iac/concepts/state-and-backends/ | A (8) | não verificada | destilado |
| V-40 | Well-Architected GCP, Azure e AWS (Security e Cost Optimization) | https://docs.cloud.google.com/architecture/framework · https://learn.microsoft.com/en-us/azure/well-architected/ · https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html | B (7) | não verificada | destilado |
| V-41 | AWS Secrets Manager, Best practices | https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html | A (9) | não verificada | destilado |
| V-42 | Kubernetes, Secrets; RBAC good practices | https://kubernetes.io/docs/concepts/configuration/secret/ · https://kubernetes.io/docs/concepts/security/rbac-good-practices/ | A (9) | não verificada | destilado |
| V-43 | External Secrets Operator; HashiCorp Vault | https://external-secrets.io/latest/introduction/overview/ · https://developer.hashicorp.com/vault/docs/what-is-vault | B (6) | não verificada | destilado |
| V-44 | Argo Rollouts, Concepts e Canary | https://argoproj.github.io/argo-rollouts/concepts/ · https://argo-rollouts.readthedocs.io/en/stable/features/canary/ | A (8) | não verificada | destilado |
| V-45 | Flagger, How it works | https://docs.flagger.app/usage/how-it-works | A (8) | não verificada | destilado |
| V-46 | Google SRE Workbook, Canarying releases | https://sre.google/workbook/canarying-releases/ | A (8) | © 2018, **CC BY-NC-ND 4.0** | só destilação |
| V-47 | OpenFeature, Introduction | https://openfeature.dev/docs/reference/intro/ | B (7) | não verificada | destilado |
| V-48 | AWS Lambda, Best practices | https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html | A (9) | não verificada | destilado |
| V-49 | Azure Functions, Best practices | https://learn.microsoft.com/en-us/azure/azure-functions/functions-best-practices | A (8) | não verificada | destilado |
| V-50 | Cloud Run, General development tips | https://docs.cloud.google.com/run/docs/tips/general | B (7) | não verificada | destilado |
| V-51 | CNCF TAG App Delivery, Platforms White Paper | https://tag-app-delivery.cncf.io/whitepapers/platforms/ | A (8) | não verificada | destilado |
| V-52 | Backstage, Software Templates | https://backstage.io/docs/features/software-templates/ | B (7) | não verificada | destilado |
| V-53 | Infracost, Docs | https://www.infracost.io/docs/ | B (7) | não verificada | destilado |
| V-54 | Google SRE book, Postmortem culture; Managing incidents | https://sre.google/sre-book/postmortem-culture/ · https://sre.google/sre-book/managing-incidents/ | A (8) | © 2017, **CC BY-NC-ND 4.0** | só destilação (insumo para `sre-observability`; não usado neste plugin) |
| V-55 | Docker, Build secrets; Dockerfile reference (HEALTHCHECK) | https://docs.docker.com/build/building/secrets/ · https://docs.docker.com/reference/dockerfile/ | A (9) | não verificada | destilado |
| V-56 | Kubernetes, Network Policies | https://kubernetes.io/docs/concepts/services-networking/network-policies/ | A (9) | não verificada | destilado |
| V-57 | Kubernetes, Enforce Pod Security Standards (namespace labels e admission controller) | https://kubernetes.io/docs/tasks/configure-pod-container/enforce-standards-namespace-labels/ | A (8) | não verificada | destilado |
| V-58 | Kubernetes, Probes; Resource management | https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ · https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ | A (8) | não verificada | destilado (leitura por resumo truncado) |
| V-59 | SLSA levels; Sigstore cosign (signing containers) | https://slsa.dev/spec/v1.0/levels (retirada; atual: https://slsa.dev/spec/v1.2/build-track-basics, conferida pelo validador de qualidade em 2026-10-10) · https://docs.sigstore.dev/cosign/signing/signing_with_containers/ | A (8) | não verificada | destilado |
| V-60 | Claude Code, Hooks (PermissionRequest, PostCompact, ConfigChange, Stop) | https://code.claude.com/docs/en/hooks | A (9) | não verificada | destilado |
| V-61 | HashiCorp, Automate Terraform with GitHub Actions (HCP Terraform) | https://developer.hashicorp.com/terraform/tutorials/automation/github-actions | B (7) | não verificada | destilado |
| V-62 | wshobson/agents (plugins DevOps; índice) | https://github.com/wshobson/agents | C (4) | MIT © Seth Hobson 2024; 40,3 mil estrelas | só contraexemplo e estrutura |

## Brain-of-agent e gstack (conteúdo reaproveitado)

| Origem | Arquivo (snapshot) | Licença | Uso neste plugin |
| --- | --- | --- | --- |
| brain-of-agent (francisco-efjr, commit 0d025fb) | `brains/fullstack/references/entrega-e-operacao.md` | MIT (do usuário) | Entrega no artefato, rollout e reversão, falhas frequentes, checklist |
| idem | `brains/qa/references/dados-ambientes-ci.md` | MIT | Gates honestos, manifesto de execução, ambiente efêmero, migração |
| idem | `brains/fullstack/references/protocolo-completo.md` | MIT | Modo DEVOPS-COMPLETO e matriz de aplicabilidade |
| idem | `brains/fullstack/assets/templates/{handoff-checkpoint,plano-incremento,adr}.md` | MIT | Templates adaptados |
| idem | `brains/qa/assets/templates/checklist-release.md` | MIT | Seções de dados, observabilidade e rollback do go/no-go |
| idem | `brains/fullstack/references/seguranca-e-privacidade.md` | MIT | Rotação de segredo exposto, fronteiras de confiança |
| gstack (Garry Tan) | `vendor/gstack/setup-deploy/SKILL.md` | MIT (Copyright 2026 Garry Tan) | Bloco `## Deploy Configuration` (redação própria) |
| gstack | `vendor/gstack/land-and-deploy/SKILL.md` | MIT | Vereditos e regras de verificação (redação própria; sem preâmbulo, telemetria ou binários `gstack-*`) |

Atribuição: "inspirado em gstack `setup-deploy` e `land-and-deploy` (MIT, Garry Tan)". Nada do gstack foi copiado em bloco.

## Itens rejeitados e rebaixados

| Item | Decisão | Motivo |
| --- | --- | --- |
| abdullahkhawer/devops-skills | Rejeitado | O conteúdo reportado não confere com o README atual |
| vercel-labs/agent-skills | Rebaixado a C | Específico da Vercel; fora do escopo genérico |
| wshobson/agents | C (V-62) | Existência confirmada; amostra de 2 skills com defeitos (PodSecurityPolicy como opção atual; DNS de egress só UDP) |
| devops-agentic-workflow-tf-aws | C, contraexemplo | Sem aprovação entre plan e apply; política admin |
| ykdojo/claude-code-tips | C | Recomenda `--dangerously-skip-permissions`; sem método de infra |
| aitmpl "secure git workflow" | C, ideia | Hooks só para `git commit`; instala por `npx` |
| awesome-claude-code | C, índice | Licença não identificada |
| blog "How Anthropic teams use Claude Code" | C, estudo de caso | Relato de fornecedor; sem Terraform |
| dev.to e HN (ApplicationSet) | Não aprovados | Sem técnica extraída |

## Conflitos entre fontes e resolução (K1 a K15)

Os códigos `K<n>` aparecem em outras partes do plugin. Regra geral: a documentação oficial atual prevalece sobre repositórios de instruções.

| # | Conflito | Resolução |
| --- | --- | --- |
| K1 | awesome-copilot recomenda "última versão estável" x HashiCorp manda fixar providers, módulos e `required_version` | Fixar; atualizar por PR dedicado (`init -upgrade`) |
| K2 | Hook ou skill de guarda como proteção x a própria fonte diz "advisory, não fronteira" | Hook é guardrail documentado e desativado; a camada real é IAM sem destroy, sandbox e permissões |
| K3 | ykdojo e Ronacher usam skip-permissions em container x docs mandam allowlist e sandbox | Rejeitar `--dangerously-skip-permissions` como padrão (risco, só em sandbox e repositório confiável) |
| K4 | `allowed-tools` de skill parece restringir x só pré-aprova | Tratar como pré-aprovação; limites reais vêm de `deny` e do sandbox |
| K5 | "CLAUDE.md não chega ao subagente" x chega (exceto Explore/Plan ou `omitClaudeMd`); o histórico não chega | O prompt de delegação cola o diff e repete as regras críticas |
| K6 | `sandbox.credentials` em settings de projeto x ignorado fora de user/managed | Proteção de credenciais documentada para settings do usuário |
| K7 | `plan` em `allow` por conveniência x `plan` assume credenciais e trava o state | `plan` em `ask` por padrão; `allow` só com credencial somente leitura |
| K8 | Argo Rollouts sugere blue-green primeiro x SRE Workbook e Flagger privilegiam canário com métricas | Blue-green se a troca é atômica ou a app não convive com duas versões; canário se convive e há métricas confiáveis |
| K9 | Argo CD "ligar sync automático, prune e self-heal sempre" x risco de apagar ou reverter em produção | Decisão por ambiente; rollback é commit; não citar "automático desligado por padrão" como literal |
| K10 | Flux: conceitos dizem `interval` padrão de 5 min x API diz obrigatório (mín. 60 s) sem default | Não citar default; exigir `interval` explícito |
| K11 | Stop hook como porteiro x após 8 continuações o bloqueio é ignorado | Stop só como lembrete; o gate real é skill, CI e revisor |
| K12 | SLSA v1.0 citada x página retirada, v1.2 atual | Citar v1.2; `cosign verify` pendente |
| K13 | kubernetes-skill "elimina alucinações" x sem métrica ou eval | Usar só o processo (diagnosticar, gerar, validar) |
| K14 | wshobson ensina PodSecurityPolicy e DNS de egress só UDP x PSS/PSA e UDP+TCP 53 | PSS/PSA; DNS em UDP e TCP 53 selecionando o namespace por `kubernetes.io/metadata.name` (Inferido) |
| K15 | Cache com `github.run_id` na chave x chave por `hashFiles(lockfile)` com `restore-keys` | Usar `hashFiles`; nunca `run_id` na chave primária |

## Artefatos da casa (P-01 a P-23)

Rascunhos escritos pelo validador (autoria da casa, MIT do repositório), **nunca testados em sessão real**. Notas são julgamento do validador (autoavaliação de modelo da mesma família, não validação externa). Onde ≥ 80 estão "aprovados"; 70 a 79 "com ressalvas" e foram reforçados no plugin com exemplos e critérios de saída.

| ID | Artefato | Nota | Onde entrou |
| --- | --- | --- | --- |
| P-01 | Subagente `infra-reviewer` | 82 | agente `infra-reviewer` |
| P-02 | Regra: gate antes de mutar infra | 80 | SN-02, `agente-seguro.md` |
| P-03 | Hook PreToolUse de exemplo | 80 | `ferramentas-e-mcp.md` (d) |
| P-04 | Template de permissões | 78 | `ferramentas-e-mcp.md` (b) |
| P-05 | Bloco CLAUDE.md "Infra" | 80 | `claude-md-snippets.md` |
| P-06 | Skill hub `iac-review` | 85 | skill `iac-review` |
| P-07 | Skill `deploy-infra` | 82 | skill `deploy-infra` |
| P-08 | Prompt de revisão de IaC em CI | 82 | `ferramentas-e-mcp.md` (e) |
| P-09 | Prompt de manutenção agendada | 77 | `agente-seguro.md`, biblioteca de prompts |
| P-10 | Esqueleto de Gotchas | 75 | seção Gotchas das skills |
| P-11 | Checklist agent-risk | 77 | `agente-seguro.md` |
| P-12 | Matriz de acesso do agente | 78 | `matriz-acesso-agente.md` |
| P-13 | Skill `helm-review` | 87 | `helm-gitops-review` |
| P-14 | Skill `gitops-review` | 83 | `helm-gitops-review` |
| P-15 | Referência `terraform-state-test.md` | 77 | `terraform-opentofu-pulumi.md` |
| P-16 | Skill `secrets-review` | 85 | `secrets-review` |
| P-17 | Skill `progressive-delivery` | 85 | `progressive-delivery` |
| P-18 | Skill `serverless-review` | 75 | `cloud-review` |
| P-19 | Referência `k8s-review.md` | 80 | `containers-k8s-helm.md` |
| P-20 | Skill `incident-postmortem` | 83 | fora do plugin (vai a `sre-observability`) |
| P-21 | Regras para exemplos de hook | 78 | `ferramentas-e-mcp.md` (d) |
| P-22 | Checklist de supply chain em CI | 70 | `cicd-e-supply-chain.md` (com `cosign verify` pendente) |
| P-23 | Checklist de PR de IaC | 75 | `checklist-pr-iac.md` |

## Lacunas conhecidas

1. **GitLab CI e Azure Pipelines** (citados no escopo do segmento): sem fonte validada; só princípios por analogia, marcados Inferido.
2. **Kustomize** além do glossário; `helm install --dry-run`; Helm `required`/`default`.
3. **FinOps Framework** (finops.org, 403); AWS Cost Optimization por pilar; subpáginas dos pilares do GCP e Azure; AWS Security pillar (princípios).
4. **Vault** (secrets engines, leases, TTL); External Secrets Operator (provedores e versão); SOPS fora do Flux.
5. **`cosign verify`** (issuer e identidade keyless), SLSA v1.2 e gerador de proveniência.
6. Ciclo de vida de feature flags; AnalysisTemplate do Argo Rollouts; Cloud Run (SIGTERM, segredos); runbooks e PagerDuty.
7. Plan em PR sem HCP Terraform (Atlantis etc.); Terragrunt; testes de módulos fora do `terraform test`.
8. CLAUDE.md, AGENTS.md e `.mdc` reais de repositórios de infra.
9. **Comunidade**: Reddit, X, YouTube, dev.to e newsletters não foram alcançados; só 2 threads do Hacker News.
10. **MCP servers de infraestrutura**: nenhum avaliado (Não verificável).
11. **Teste real** dos 23 artefatos e execução dos evals (`designed_not_executed`; a CLI local registrada na fundação é a 2.1.128, abaixo do mínimo 2.1.269 de `claude plugin eval`).
12. Ambientes reprodutíveis (devcontainer, compose local): sem fonte validada além do brain.

## Limitações das fontes

- Datas de último push e métricas do GitHub não foram verificadas (API com 403; `gh` não autenticado). Estrelas e licenças foram lidas nas páginas HTML. Popularidade não é qualidade.
- A leitura por WebFetch devolve resumo de modelo pequeno; páginas grandes (Kubernetes Secrets, RBAC, NetworkPolicy, probes, limits; hooks até ~200 mil de ~262 mil caracteres; Flux Kustomization) foram lidas só em parte.
- Licenças de docs oficiais não foram verificadas: tratamento é sempre destilação. SRE book e Workbook são CC BY-NC-ND 4.0: sem trecho literal.
- O fluxo "plan no PR, apply no merge" vem de um tutorial do HCP Terraform.
- A pesquisa Amplifying é resultado por versão de modelo, não dado de mercado.
- Conteúdo de terceiros contém texto dirigido a IA em alguns arquivos (ex.: awesome-copilot, dirigido ao Copilot): tratado como dado.
