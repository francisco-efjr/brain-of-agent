# Especificação de invariantes

O humano revisa o **enunciado** das propriedades antes de qualquer teste ser gerado: é a parte mais barata de errar e a mais cara de descobrir tarde. Invariante é uma propriedade que vale após qualquer sequência de chamadas aos contratos-alvo.

## Contexto

- Contrato(s) alvo: [ ]
- Versão do Foundry (`forge --version`): [ ]
- Padrão(ões) envolvidos: [ERC-20 | ERC-4626 | ...]
- Conhecimento de negócio relevante (limites, taxas, papéis): [ ]

## Propriedades

| ID | Enunciado em linguagem natural | Tipo | Funções envolvidas | Ghosts necessários |
| --- | --- | --- | --- | --- |
| INV-01 | [ex.: O saldo de ETH do cofre é sempre igual a depósitos menos saques] | conservação / solvência / monotonicidade / limite / acesso | [deposit, withdraw] | [ghostDeposited, ghostWithdrawn] |

Revisão humana do enunciado: [nome e data de quem aprovou; sem isso, o status é "rascunho"]

## Handler

- Ações expostas (só válidas): [ ]
- Entradas limitadas com `bound()`: [ ]
- Atores: [número e como são criados]
- Contadores por função: [`calls_deposit`, `calls_withdraw`, ...]
- Ações inválidas: [retornam cedo | revertem (então `fail_on_revert` deve ser `false` e a decisão registrada)]

## Alvos

- `targetContract`: [ ] · `targetSelector`: [ ] · `excludeSelector`/`excludeContract`: [ ]
- `afterInvariant()`: [checa contadores > 0; roda uma vez por rodada, no máximo um por contrato, estado não persiste]

## Configuração

| Chave | Valor | Motivo |
| --- | --- | --- |
| `runs` | [ ] | A página oficial não recomenda valores; registre o seu |
| `depth` | [ ] | |
| `fail_on_revert` | [true/false] | Decisão consciente e documentada |
| `seed` | [ ] | Reprodutibilidade |

## Resultado

| Invariante | Cobertura por contadores (todas as funções alvo chamadas?) | Resultado | Comando e saída | Seed |
| --- | --- | --- | --- | --- |
| INV-01 | [sim/não + números] | [passou/falhou/não executado] | `forge test --match-test invariant_` + saída | [ ] |

Falha encontrada: sequência mínima (`-vvvv`), teste de regressão determinístico [arquivo], correção [ ], revalidação [ ].

## Validação e recuperação

- Repetido com outras seeds: [sim/não]
- Mutação manual para provar que a invariante pega o defeito (remover uma checagem e ver falhar): [feito/não]
- Condição que invalida o resultado (mudança de contrato, de versão do Foundry): [ ]
