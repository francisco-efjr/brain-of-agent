# Plano de entrega: [iniciativa]

Adaptado de `plano-incremento.md` do brain-of-agent (MIT, Francisco Edson), sem campos de dados e UI específicos. Cada fase entrega algo utilizável e verificável (fatia vertical). Para tarefas em nível de arquivo, use `tasks.md` e `plano-implementacao.md`.

## Objetivo e baseline

- **Problema, usuário e comportamento atual:** [texto]
- **Critério de sucesso e fonte:** [métrica e origem]
- **Estado observado e reprodução:** [Verificado ou Inferido]
- **Escopo, exclusões e autorização:** [o que pode mudar, o que não, quem aprova]
- **Stack, revisão e ambiente (se já fixados pela spec):** [texto]

## Fatia vertical

Entrada do usuário, regra e resultado observável; descreva cada fronteira e sua falha ou recuperação.

| Requisito | Alteração de comportamento | Invariante | Compatibilidade ou contrato | Verificação (oráculo) |
| --- | --- | --- | --- | --- |
| FR-001 | | | | |

## Fases e riscos

| Fase | Artefato utilizável | Risco | Mitigação | Critério de saída |
| --- | --- | --- | --- | --- |
| 1 | [o que o usuário já consegue fazer] | | | [verificável por comando ou evidência] |

- **Dependências e decisões materiais:** [lista, com dono]
- **Duplicação, concorrência, timeout e autorização:** [como cada regra se comporta]
- **Estados de interface, acessibilidade e plataforma:** [critérios, se aplicável]

## Validação

- Checks existentes a executar: [lista]
- Regressões necessárias e por quê: [lista]
- Roteiro manual e efeitos persistidos: [lista]
- Não executável e risco restante: [lista]

## Entrega

- **Como executar, configurar e observar:** [passos]
- **Publicação e reversão:** somente dentro da autorização do usuário; ação externa pede confirmação.
- **Evidências, pendências e próximo passo:** [lista]
