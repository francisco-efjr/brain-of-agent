# ADR [ID] — [decisão de pagamentos]

Adaptado do template `adr` do brain-of-agent (MIT). Use só para decisão material: modelo de ledger, política de idempotência, onde fica a máquina de estados, estratégia de conciliação, escolha de provedor, exceção a um invariante.

Estado: [proposta | aceita | substituída] · Data/revisão: [AAAA-MM-DD / commit] · Autor: [ ] · Revisor independente: [pessoa ou "não houve"]

## Contexto

Problema, restrições, volume, provedores, regulação aplicável, requisitos e evidências. Stack existente.

- Especificações e documentação lidas (**nome, versão, data de leitura**): [ex.: API do provedor X v2026-01, lida em 2026-10-11; Manual do Pix 2.10.0]
- O que é Verificado / Inferido / Suposição / Não verificável neste contexto: [lista curta]

## Opções (mínimo 2)

| Opção | Benefício | Custo/risco | Compatibilidade com o código atual | Evidência (fonte e rótulo) |
| --- | --- | --- | --- | --- |
| A — [ ] | [ ] | [ ] | [ ] | [V-nn / fonte; rótulo] |
| B — [ ] | [ ] | [ ] | [ ] | [ ] |

## Decisão

Opção escolhida e por quê. Hipóteses ainda não confirmadas (marcadas **Suposição**). Critérios do usuário que pesaram (volume, auditoria, equipe, prazo).

## Consequências

- Complexidade e operação: [ ]
- Dados e migração; limites de reversibilidade (não prometa rollback de dados perdidos só porque existe migração down): [ ]
- Segurança, privacidade (LGPD) e escopo PCI: [ ]
- Idempotência, ordem de eventos e conciliação afetadas: [ ]
- Testes necessários (com oráculo independente): [ ]

## Riscos e rótulos

| Risco | Probabilidade/impacto | Mitigação | Rótulo |
| --- | --- | --- | --- |
| [ ] | [ ] | [ ] | [Verificado / Inferido / Suposição] |

## Validação e revisão

- Critério observável que sustenta a escolha (teste, medição): [ ]
- Condição que exige reconsiderar a decisão: [ex.: contenção em conta quente acima de X; mudança de versão da spec]
- Perguntas abertas e **lista "Não verificado"**: [ ]
- Links para requisitos e artefatos: [ ]
