---
name: prompts
description: Biblioteca de 32 prompts curados de DevOps, cloud e infraestrutura, prontos para colar, com variáveis, motivo e fontes. Cobre gate antes de mutar infra, plano de mudança, delegação de revisão, revisão de Terraform/OpenTofu, Dockerfile, compose, Kubernetes, Helm, GitOps, GitHub Actions e segredos, rollout e rollback, diagnóstico de pod e CI, serverless, custo, supply chain, segurança do agente, prompt de sistema e mensagem inicial. Use quando pedirem 'um prompt para', 'prompt pronto de DevOps', 'template de pedido para revisar terraform/k8s/pipeline', 'ready-made prompt for infra review', 'prompt for canary plan'. Indica qual prompt usar; não executa a tarefa do prompt.
---

# Prompts de DevOps, cloud e infraestrutura

Esta skill entrega o texto de um prompt pronto e diz como usá-lo. Ela não executa a tarefa do prompt: quando a pessoa quer que o Claude faça o trabalho agora, a coluna "Para fazer agora" da tabela aponta a skill ou o agente do plugin que já faz isso.

## Como entregar um prompt

1. Escolha na tabela abaixo o prompt que cobre a situação (um, no máximo dois). Se nenhum cobrir, adapte o mais próximo e diga qual adaptou.
2. Abra só a seção do prompt no arquivo indicado (cada arquivo tem sumário). Não leia a biblioteca inteira.
3. Preencha as variáveis `[EM_COLCHETES]` com o que a pessoa já disse. Deixe as demais entre colchetes; não invente conta, cluster, versão, comando nem número.
4. Entregue o prompt num bloco de código, seguido de 2 a 4 linhas: onde rodar (sessão nova para prompts de revisão, para o revisor não herdar o contexto do autor), que ferramentas exige (somente leitura ou também execução), quais variáveis faltam e por que ele é estruturado assim.
5. Se a pessoa colar o material (diff, `plan`, log, YAML), ofereça executar o prompt; não revise material que não foi dado.
6. Não afirme que o prompt tem eficácia medida. Nenhum foi testado em sessão real; os casos de `evals/` estão `designed_not_executed`.
7. Nenhum prompt desta biblioteca autoriza `apply`, `destroy`, `helm upgrade`, `kubectl apply`, `git push` nem deploy. Quem entrega o prompt também não executa esses comandos: o gate (alvo confirmado, efeito, rollback e "sim" explícito) vem antes. Quando a pessoa pedir para rodar a mudança, aponte o comando explícito `/devops-cloud-infra:deploy-infra`.
8. Em execução sem interação (subagente, lote, CI, `claude -p`), os prompts com pergunta ou gate mandam registrar as dúvidas em "Decisões pendentes do humano" e seguir como rascunho. Preservar essa linha ao adaptar.

Plataforma: infraestrutura de servidor é o núcleo. Para mobile (assinatura, lojas, builds nativos) aponte `/mobile-apps:playbook`; para empacotamento e auto-update de desktop, o plugin `cli-desktop-tooling`; para web, a plataforma de deploy fixada no projeto (PR-31) e, para performance de frontend, `web-frontend`. Detalhes na tabela "Plataformas" de [prompt-library.md](references/prompt-library.md#plataformas-o-que-muda).

## Situação → prompt

Arquivo A = [prompt-library.md](references/prompt-library.md) (PR-01 a PR-14, PR-17, PR-19, PR-26, PR-27, PR-29 a PR-32). Arquivo B = [prompts-entrega-supply-chain-custo.md](references/prompts-entrega-supply-chain-custo.md) (PR-15, PR-16, PR-18, PR-20 a PR-25, PR-28).

| ID | Prompt | Use quando | Arq. | Para fazer agora |
| --- | --- | --- | --- | --- |
| PR-01 | Delegar revisão de IaC ao `infra-reviewer` | editou IaC e vai abrir PR; diff mexe em IAM, rede ou state | A | agente `infra-reviewer` |
| PR-02 | Gate antes de mutar infra | alguém pede `apply`, `kubectl apply`, `helm upgrade`, `git push` | A | skill `playbook` (mostra o gate); execução só por `/devops-cloud-infra:deploy-infra` |
| PR-03 | Plano de mudança com alvo, efeito e rollback | antes de `apply` ou deploy | A | comando `/devops-cloud-infra:plan-infra` ou agente `rollout-planner` |
| PR-04 | Revisão de IaC em CI (`prompt:` do claude-code-action) | workflow de PR que revisa infra | A | skill `gha-hardening-review` |
| PR-05 | Manutenção agendada somente leitura | rotina semanal via `/loop`, Routines ou cron | A | skill `playbook` |
| PR-06 | Auditar workflow do GitHub Actions | PR em `.github/workflows` | A | skill `gha-hardening-review` ou agente `pipeline-security-auditor` |
| PR-07 | Revisar Dockerfile | Dockerfile novo ou alterado | A | skill `iac-review` |
| PR-08 | Endurecer container e compose | compose, `docker run`, runtime | A | skill `iac-review` |
| PR-09 | Revisar manifests Kubernetes | PR de Deployment, StatefulSet, Job | A | skill `iac-review` ou agente `k8s-workload-auditor` |
| PR-10 | Plano de adoção do Pod Security Admission | cluster existente, ativar `enforce` | A | agente `k8s-workload-auditor` |
| PR-11 | Auditar RBAC e ServiceAccounts | revisão periódica de permissões | A | agente `k8s-workload-auditor` |
| PR-12 | NetworkPolicy default deny sem quebrar DNS | novo namespace | A | agente `k8s-workload-auditor` |
| PR-13 | Revisar Helm chart | mudança em chart | A | skill `helm-gitops-review` |
| PR-14 | Revisar configuração GitOps | PR em repositório de config (Argo CD, Flux) | A | skill `helm-gitops-review` |
| PR-15 | Plano de rollout canário ou blue-green | nova release com Rollouts ou Flagger | B | skill `progressive-delivery` ou agente `rollout-planner` |
| PR-16 | Critérios de rollback antes do deploy | qualquer release | B | skill `progressive-delivery` |
| PR-17 | Caça a segredos sem imprimir valores | auditoria de repositório | A | skill `secrets-review` |
| PR-18 | Migrar segredos para o cluster de destino | tirar segredo do Git ou da geração de manifests | B | skill `secrets-review` |
| PR-19 | Revisar state, lock, lockfile e testes do Terraform | repositório Terraform, OpenTofu ou Pulumi | A | skill `iac-review` |
| PR-20 | Plano de migração Terraform para OpenTofu | decisão de migrar | B | skill `iac-review` |
| PR-21 | Migração em lote de módulos em worktrees | mesma mudança em muitos módulos | B | skill `playbook` |
| PR-22 | Checklist de PR de IaC: plan, teste e custo | revisar ou montar o pipeline do PR de IaC | B | skill `iac-review` |
| PR-23 | Revisão serverless | Lambda, Azure Functions, Cloud Run | B | skill `cloud-review` |
| PR-24 | Pilares Well-Architected como perguntas | revisão de arquitetura na nuvem | B | skill `cloud-review` |
| PR-25 | Estimativa e governança de custo | PR de IaC que cria recurso pago, FinOps | B | skill `cloud-review` |
| PR-26 | Diagnosticar workload Kubernetes que não sobe | CrashLoopBackOff, Pending, OOMKilled, OutOfSync | A | skill `infra-troubleshoot` |
| PR-27 | Diagnosticar job de CI que falhou ou passou por engano | pipeline vermelho ou verde suspeito | A | skill `infra-troubleshoot` |
| PR-28 | Proveniência e assinatura de imagens | pipeline de release de contêineres | B | skill `gha-hardening-review` ou agente `pipeline-security-auditor` |
| PR-29 | Agent-risk e matriz de acesso | antes de dar acesso a infra ao agente | A | skill `playbook` (`agente-seguro.md`) |
| PR-30 | Registrar um Gotcha depois de falha real | erro observado numa skill ou agente | A | skill `playbook` |
| PR-31 | Prompt de sistema para projetos de infra | `CLAUDE.md` ou instruções de projeto, ou outra IA | A | skill `playbook` (`claude-md-snippets.md`) |
| PR-32 | Mensagem inicial sugerida | abrir uma sessão de infra com contexto completo | A | skill `playbook` |

Se o pedido é sobre o projeto de infraestrutura inteiro, sobre o modo `DEVOPS-COMPLETO` ou sobre qual skill usar, use a skill `playbook`. Incidente em produção com impacto em usuário (papéis, comunicação, postmortem), SLO e alertas pertencem ao plugin `sre-observability`; aqui só o diagnóstico técnico da falha de infraestrutura.

## Os dois prompts de projeto

- **PR-31, prompt de sistema:** cola no `CLAUDE.md` do repositório de infra (ou em outra IA). Fixa a plataforma de deploy do projeto, o gate, o tratamento de conteúdo externo como dado, a regra de credenciais e a escalada em três falhas. Mantenha o `CLAUDE.md` curto (menos de 200 linhas) e use só o que o agente não descobre lendo o repositório.
- **PR-32, mensagem inicial sugerida:** abre uma sessão com os campos que mais faltam em pedidos de infraestrutura (ambientes e contas, ambiente do agente e sandbox, critério de aceite em comandos). Campos ausentes não são preenchidos como fatos.

## Licença e origem

Os prompts são texto da casa (MIT) ou redação própria a partir de fontes oficiais e de terceiros, com atribuição por prompt. Conteúdo do brain-of-agent (MIT, Francisco Edson) entra adaptado; vereditos de deploy foram inspirados em gstack `land-and-deploy` (MIT, Garry Tan) com redação própria. Fontes com licença restritiva (Google SRE book e Workbook, CC BY-NC-ND 4.0) só foram destiladas.

## Gotchas

- Um prompt com `[VARIAVEL]` não preenchida chega ao modelo como texto literal e ele pode inventar o valor: confira os colchetes antes de enviar.
- Prompts de revisão rodam melhor em sessão ou subagente novo; no mesmo contexto do autor, o revisor tende a concordar com o autor.
- Prompt não é controle de acesso: o limite real de um agente com acesso a infraestrutura é IAM, sandbox e permissões, não o texto do prompt.
- Cole o `plan` ou a saída do lint junto: sem eles o prompt devolve "não executado", não uma aprovação.

Validado em: 2026-10-10 · modelo-alvo: Claude Sonnet 5.5 · rascunhos não testados em sessão real.
