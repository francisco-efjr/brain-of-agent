# Plano de implementação: [NOME DA FEATURE]

**Spec:** [caminho] · **Status:** Draft · **Data:** [AAAA-MM-DD]

Oito seções e IDs estáveis (`REQ-`, `TASK-`, `TEST-`, `RISK-`, `ASSUMPTION-`, `ALT-`, `FILE-`, `DEP-`), no estilo do agente de plano do awesome-copilot (MIT), reescrito. O campo "Critério de conclusão" por fase é construção deste plugin. Nenhuma tarefa exige decisão humana nem deixa placeholder; se exigir, volta à spec como pergunta aberta.

## 1. Requisitos e restrições

- REQ-001: [requisito da spec, com referência FR-nnn]
- CON-001: [restrição: prazo, compatibilidade, legado]

## 2. Passos

### Fase 1: [nome]

**Objetivo:** [resultado da fase].

| Tarefa | Descrição | Arquivos |
| --- | --- | --- |
| TASK-001 | [ação concreta] | FILE-001 |

**Critério de conclusão (mensurável, verificável por comando):** [ex.: a suíte do módulo X passa; a chamada Y retorna o corpo do exemplo da spec].

## 3. Alternativas

- ALT-001: [alternativa considerada] · descartada porque [motivo].

## 4. Dependências

- DEP-001: [serviço, biblioteca ou equipe, com versão ou contrato].

## 5. Arquivos

- FILE-001: `[caminho]` · [existente ou novo] · [o que muda]

## 6. Testes

| ID | Cobre | Descrição | Comando |
| --- | --- | --- | --- |
| TEST-001 | REQ-001 | [o que prova] | [comando exato] |

## 7. Riscos e premissas

- RISK-001: [risco] · mitigação: [ação] · dono: [nome]
- ASSUMPTION-001: [Suposição] · confirmar com: [dono]

## 8. Especificações relacionadas

[Links para spec, PRD, decisões de produto e ADRs.]

## Rastreabilidade

Cada REQ liga a pelo menos uma TASK e um TEST: [tabela REQ, TASK, TEST].
