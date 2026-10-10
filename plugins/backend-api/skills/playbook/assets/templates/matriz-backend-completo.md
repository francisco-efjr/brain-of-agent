# Matriz BACKEND-COMPLETO

> Base: `protocolo-completo.md` e `checklist-fullstack-completo.md` do brain-of-agent (MIT), adaptados a backend e APIs. Preencha apenas no modo `BACKEND-COMPLETO`, ativado por pedido explícito do usuário no turno atual. A keyword **não amplia permissões**.

Projeto/objeto: [..] · Pedido/escopo: [..] · Revisão/ambiente: [commit/ambiente] · Data: [..]
Autorização: [análise apenas | implementação local no escopo X | ações externas específicas]

## 1. Registro de leitura (lotes com checkpoint)

| Lote | Arquivo (em `skills/playbook/references/` ou skill) | Estado (lida | parcial | ausente) | Decisão extraída | Ponto de retomada |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | checklist-completo, padroes-e-antipadroes, decisoes-e-tradeoffs, contrato-erros-paginacao | | | |
| 2 | autenticacao-seguranca, idempotencia-resiliencia, stacks, testes-e-depuracao | | | |
| 3 | agentes-e-llm, claude-md-snippets, ferramentas-e-mcp, fontes | | | |
| 4 | templates de `assets/templates/` | | | |
| 5 | `SKILL.md` e `references/` das skills de tarefa aplicáveis | | | |

Capacidades: leitura/edição [sim|não] · shell [sim|não] · banco de teste [sim|não] · rede [sim|não] · Git [sim|não]. Ausência de ferramenta é limitação verificável, não defeito do sistema.

## 2. Matriz de aplicabilidade

A = aplicável · NA = não aplicável (motivo obrigatório) · NV = não verificável (falta acesso).

| Área | A/NA/NV | Regra/fonte (arquivo, V-nn) | Risco ou justificativa | IDs do backlog |
| --- | --- | --- | --- | --- |
| Contrato (OpenAPI/proto/GraphQL) | | | | |
| Erros (RFC 9457) | | | | |
| Autenticação | | | | |
| Autorização (objeto, propriedade, função, tenant) | | | | |
| Validação de entrada e DTOs | | | | |
| Idempotência | | | | |
| Paginação e ordenação | | | | |
| Cache (HTTP e aplicação) | | | | |
| Rate limiting | | | | |
| Jobs, filas, outbox | | | | |
| Webhooks | | | | |
| Integrações e dependências externas | | | | |
| Versionamento e deprecação | | | | |
| Observabilidade (logs, correlation ID) | | | | |
| Testes de API | | | | |
| Dados e migração | | | | |
| Segurança de segredos | | | | |
| Tools para agentes / integração com LLM | | | | |

## 3. Backlog rastreável

| ID | Requisito/risco | Critério/oráculo | Análise | Implementação (arquivos) | Validação | Revalidação | Evidência (comando + saída) | Pendência |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Estados: pendente · inferido · verificado · falhou · não autorizado · NA · NV. Implementação concluída não é critério operacional verificado.

## 4. Revalidação

Reprodução original repetida: [comando → saída] · Regressões por impacto: [..] · Evidência invalidada por mudança posterior e refeita: [..] · Primeira falha preservada: [..]

## 5. Gates

| Gate | Estado | Evidência |
| --- | --- | --- |
| Entendimento (fontes, escopo, regras, conflitos) | | |
| Plano (fatia, contrato, riscos, oráculos) | | |
| Implementação (no escopo, compatível) | | |
| Validação (checks executados e ligados aos critérios) | | |
| Revalidação (falhas corrigidas reverificadas) | | |
| Entrega (artefatos, riscos, continuidade) | | |

Resultado: [concluído no escopo | parcial | impedido] · Falha crítica aberta impede recomendação favorável; média de notas não a compensa.
Leitura: [integral | parcial] · Execução: [completa no escopo | parcial | não executada] · Revisão: feita pelo mesmo modelo, **não é validação independente**.
Lacunas conhecidas do plugin: ver `fontes.md`, seção "Lacunas conhecidas".
