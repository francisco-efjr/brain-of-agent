# ADR [ID] — [decisão]

Adaptado do template `adr.md` do brain-of-agent (MIT). Use para decisão material: padrão de proxy ou contrato imutável, fonte de preço, mitigação de inflação em cofre, escolha de L2, modelo de administração. Não crie ADR para cada linha.

Estado: [proposta | aceita | substituída] · Data/revisão (commit): [ ]

## Contexto

Problema, restrições, requisitos, evidências, stack e versões (compilador, OpenZeppelin, Foundry), cadeia alvo, valor em risco estimado e quem é afetado.

## Opções

| Opção | Benefício | Custo/risco | Compatibilidade | Evidência |
| --- | --- | --- | --- | --- |
| [A: ex. imutável] | | | | [fonte V-… ou teste] |
| [B: ex. UUPS com timelock] | | | | |

## Decisão

Opção escolhida e por quê. Hipóteses ainda não confirmadas (rotule Suposição). Quem tem poder privilegiado após a decisão (admin, atualizador, pausa) e como é controlado.

## Consequências

- Segurança: [superfície nova, quem pode o quê]
- Operação: [monitoramento, rotação de chaves, resposta a incidente]
- Dados e migração: [layout de storage; upgrade é irreversível em estado, não prometa rollback de dados perdidos]
- Testes afetados: [invariantes, replay, upgrade em fork local]
- Custo: [gás, capital preso]

## Validação e revisão

Critérios observáveis (teste Foundry, comando e saída esperados). Condição que exige reconsiderar a decisão (nova versão maior do OpenZeppelin, mudança de rede, incidente). Links para a especificação de invariantes e o relatório de achados.
