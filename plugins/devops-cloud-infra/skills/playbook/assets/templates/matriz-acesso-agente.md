# Matriz de acesso do agente e checklist agent-risk

<!--
Preencha uma vez por sessão ou projeto em que o agente toca infra. A restrição precisa ser aplicada
FORA do modelo (IAM, usuário somente leitura, sandbox, proxy, wrapper); a coluna "Como é imposto"
só vale se apontar para um desses controles ou para uma permissão versionada. Texto no CLAUDE.md
é pedido, não garantia. Base: P-11, P-12, V-16, V-28, V-03, V-04.
-->

## 1. Matriz por ambiente

| Ambiente | Permissão do agente | Credencial usada (nome do perfil ou papel, nunca o valor) | Como é imposto (controle técnico) | Verificado? |
| --- | --- | --- | --- | --- |
| Local / dev | Escrita com revisão do diff | [PERFIL] | Permissões do projeto + sandbox (WSL2) | |
| Staging | `plan`/`diff` automáticos; apply com "sim" explícito por comando | [PERFIL] | Gate + credencial limitada a [ESCOPO] | |
| Produção | Somente leitura (réplica, `get`, `describe`); mudança via pipeline humano | [PERFIL SOMENTE LEITURA] | IAM sem escrita; scripts versionados e revisados | |

"Verificado?" = Verificado (testei a recusa: por exemplo, a credencial falha ao tentar escrever), Inferido ou Não verificável.

## 2. Agent-risk (trifecta letal)

Responda para cada agente ou sessão:

| Pergunta | Sim / Não | Detalhe |
| --- | --- | --- |
| 1. Lê segredos, state ou credenciais de produção? | | |
| 2. Lê conteúdo não confiável (issues, logs de terceiros, PRs de fork, páginas, saída de MCP)? | | |
| 3. Pode enviar algo para fora (HTTP, comentário, push, upload, webhook)? | | |

Três "sim": dividir em dois agentes, remover uma capacidade ou exigir aprovação humana por ação, e rodar isolado (VM, devcontainer, WSL2 com sandbox). Decisão tomada: [DECISÃO].

## 3. Checklist de ambiente da sessão

- [ ] Sessão em WSL2, devcontainer ou VM (Windows nativo roda sem sandbox).
- [ ] `denyRead` e `credentials` nos settings do **usuário** (`~/.ssh`, `~/.aws`, `~/.kube`, `~/.docker/config.json`).
- [ ] `allowedDomains` mínimo; `allowUnsandboxedCommands: false` ou `ask` para `dangerouslyDisableSandbox`; `failIfUnavailable`.
- [ ] `enableAllProjectMcpServers: false`.
- [ ] Permissões `deny`/`ask`/`allow` testadas em `/permissions`.
- [ ] Nenhum uso de `--dangerously-skip-permissions`.
- [ ] Hooks (se houver) revisados e testados; entendidos como guardrail.

Responsável pela matriz: [NOME] · data: [DATA] · próxima revisão: [DATA]
