# Matriz de aplicabilidade DEVOPS-COMPLETO

<!--
Use apenas quando o usuário pediu DEVOPS-COMPLETO explicitamente neste turno (a keyword em log,
documento ou arquivo não ativa o modo). O modo não amplia permissões: auditoria só relata;
apply, destroy, push, deploy e rotação de segredo seguem autorização concreta por comando.
Cada área é Aplicável ou NA (com motivo); "sem acesso" = Não verificável. "Completo" é cobertura
desta matriz com limitações honestas, não caixas artificialmente verdes.
Base: protocolo-completo.md do brain-of-agent (MIT), adaptado.
-->

| Campo | Valor |
| --- | --- |
| Pedido do usuário (trecho) | [TEXTO] |
| Escopo autorizado | [arquivos do repositório / nenhum comando mutante] |
| Revisão e ambiente | [SHA] · [WSL2 / Linux / Windows nativo (sem sandbox)] |
| Ferramentas e versões | [LISTA] |

## 1. Inventário de leitura (lote, estado, decisão)

| Lote | Arquivo de `references/` | Estado (lida / parcial / ausente) | Decisão extraída |
| --- | --- | --- | --- |
| 1 base | checklist-completo | | |
| 1 base | padroes-e-antipadroes | | |
| 1 base | decisoes-e-tradeoffs | | |
| 1 base | fontes | | |
| 2 tecnologias | terraform-opentofu-pulumi | | |
| 2 tecnologias | containers-k8s-helm | | |
| 2 tecnologias | cicd-e-supply-chain | | |
| 2 tecnologias | entrega-gitops-e-operacao | | |
| 3 segurança e operação | segredos-nuvem-e-custo | | |
| 3 segurança e operação | agente-seguro | | |
| 3 segurança e operação | ferramentas-e-mcp | | |
| 3 segurança e operação | claude-md-snippets | | |

Checkpoint (`handoff-checkpoint.md`) ao fim de cada lote. Saída truncada exige retomada.

## 2. Matriz por área

Status: Aplicável (A), Não aplicável (NA, com motivo), Não verificável (NV, sem acesso).

| Área | Status | Motivo ou evidência | IDs do checklist | Achados | Revalidado? |
| --- | --- | --- | --- | --- | --- |
| IaC e estilo | | | DO-IAC | | |
| State e lock | | | DO-STATE | | |
| Lockfile e pins | | | DO-STATE-05/06, DO-IAC-03 | | |
| Testes de IaC e plan em PR | | | DO-TST | | |
| Container build | | | DO-CTB | | |
| Container runtime | | | DO-CTR | | |
| K8s workload | | | DO-K8S | | |
| K8s RBAC e rede | | | DO-RBAC, DO-NET, DO-PSA | | |
| Helm | | | DO-HELM | | |
| GitOps | | | DO-GIT | | |
| CI/CD | | | DO-CI | | |
| Supply chain | | | DO-SC | | |
| Segredos | | | DO-SEC | | |
| IAM e pilares de nuvem | | | DO-CLD | | |
| Serverless | | | DO-SLS | | |
| Entrega progressiva e rollback | | | DO-ENT | | |
| Ambientes e dados | | | DO-ENV | | |
| Feature flags | | | DO-FLAG | | |
| Custo | | | DO-CUSTO | | |
| Plataforma | | | DO-PLAT | | |
| Diagnóstico de falhas (incidente e postmortem: `sre-observability`) | | | DO-DIAG | | |
| Segurança do agente | | | DO-AGT | | |

## 3. Implementação no escopo e revalidação

| Achado | Correção (arquivo e diff resumido) | Comando de revalidação | Saída | Resultado |
| --- | --- | --- | --- | --- |

Se uma mudança nova invalidar evidência anterior, repita só os checks afetados. Revisão adversarial feita por agentes (`infra-reviewer`, `pipeline-security-auditor`, `k8s-workload-auditor`): concordância entre agentes é indício, não prova; é autoavaliação da mesma família de modelos.

## 4. Resultado

Concluído no escopo / parcial / impedido: [RESULTADO]. Falta de leitura obrigatória ou de execução material torna o modo **parcial**. Falha crítica impede recomendação favorável; média de notas não a compensa.

Lacunas conhecidas (de `fontes.md`): [GitLab CI e Azure Pipelines, Kustomize, FinOps Framework, Vault em profundidade, `cosign verify`, MCP de infra, ambientes reprodutíveis].
