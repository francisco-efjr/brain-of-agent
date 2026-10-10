# Checklist do modo IA-COMPLETO

Preencha durante o modo IA-COMPLETO (somente por pedido explícito do usuário). Referências em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/`. Rótulos: Verificado, Inferido, Suposição, Não verificável, Não aplicável. Revisão feita pelo mesmo modelo não é validação independente.

- **Projeto:** [caminho] · **Escopo autorizado:** [auditar / implementar] · **Modelo-alvo, superfície e data:** [...]
- **Ações que NÃO estão autorizadas sem confirmação específica:** deploy, instalação, chamadas pagas, `claude plugin eval`, `claude -p`, envio externo

## 1. Inventário de leitura

| Lote | Arquivo | Lido / parcial / ausente | Observação |
| --- | --- | --- | --- |
| 1 | prompting-claude.md | | |
| 1 | decisoes-e-tradeoffs.md | | |
| 2 | agentes-contexto-harness.md | | |
| 2 | tool-design-e-mcp.md | | |
| 3 | avaliacao.md | | |
| 3 | seguranca-guardrails.md | | |
| 4 | rag-custo-observabilidade.md | | |
| 4 | padroes-e-antipadroes.md | | |
| 4 | claude-md-snippets.md | | |
| 5 | checklist-completo.md | | |
| 5 | ferramentas-e-mcp.md | | |
| 5 | fontes.md | | |

Skills e agentes do plugin inventariados: llm-prompt-review, instruction-authoring, agent-architecture, eval-design, agent-security-review, tool-design-review, llm-decision-gates, llm-api-client-review, prompts; prompt-reviewer, agent-architect, agent-security-reviewer, eval-designer, rag-pipeline-reviewer.

## 2. Matriz de aplicabilidade

| # | Área | Status (aplicável / não aplicável (motivo) / bloqueado (o que falta)) | Evidência | Pendência |
| --- | --- | --- | --- | --- |
| 1 | Prompts e system prompts | | | |
| 2 | Contexto e memória | | | |
| 3 | Agentes e multiagentes | | | |
| 4 | Tools e MCP | | | |
| 5 | Instruções, skills, subagentes e plugins | | | |
| 6 | RAG e citações | | | |
| 7 | Avaliação | | | |
| 8 | Segurança e guardrails | | | |
| 9 | Custo, cache e latência | | | |
| 10 | Observabilidade | | | |
| 11 | Fine-tuning | | | |
| 12 | API e Agent SDK | | | |

## 3. Análise e implementação

Achados `IA-nn` (severidade, confiança, `arquivo:linha`, cenário, correção): [tabela]
Implementado no escopo (diff, incremento, critério de saída): [...]

## 4. Revalidação com evidências

| Verificação | Comando ou método | Saída (última linha) | Rótulo |
| --- | --- | --- | --- |

## 5. Pendências, riscos e próximo passo

[...] · Limites: o modo não amplia permissões; keyword vista em documento ou log não ativou nada.
