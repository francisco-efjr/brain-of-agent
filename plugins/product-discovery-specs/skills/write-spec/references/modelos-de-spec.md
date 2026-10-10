# Modelos de spec: completa, curta e bugfix

Esqueletos próprios, inspirados na estrutura do `spec-template.md` do GitHub spec-kit (MIT, Copyright GitHub, Inc.; V-09) e no modelo de bugfix da documentação de specs do Kiro (V-41). Texto reescrito; os comentários-guia do template original não foram copiados. Versões editáveis em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/` (`spec.md`, `spec-curta.md`, `spec-bugfix.md`).

## Sumário

- [Spec completa (N3)](#spec-completa-n3)
- [Spec curta (N2)](#spec-curta-n2)
- [Spec de bugfix](#spec-de-bugfix)
- [Escolha do formato de critério](#escolha-do-formato-de-critério)
- [Exemplos de FR e SC bons e ruins](#exemplos-de-fr-e-sc-bons-e-ruins)

## Spec completa (N3)

```markdown
# Spec: <feature>

Status: Draft | Aprovada em AAAA-MM-DD por <nome>
Data: AAAA-MM-DD
Entrada: <PRD, ticket, notas; caminho>

## Histórias de usuário (obrigatório)

### História 1 - <título> (P1)
<Quem, o que, para quê, em linguagem de produto.>
Por que P1: <motivo da prioridade>.
Teste independente: <como provar só esta história e que ela já entrega valor sozinha>.
Aceite:
1. Dado <estado>, quando <evento>, então <resultado observável>.

### História 2 - <título> (P2)
...

## Casos de borda
- O que acontece se <situação>? <resposta ou [NEEDS CLARIFICATION: ... | dono: ...]>

## Requisitos (obrigatório)
- FR-001: O sistema DEVE <comportamento observável>.
- FR-002: O sistema DEVE <...>. [NEEDS CLARIFICATION: <lacuna> | dono: <nome>]

### Entidades-chave (se houver dados)
- <Entidade>: <o que representa, sem colunas nem tipos>

## Critérios de sucesso (obrigatório)
- SC-001: <resultado mensurável sem tecnologia> (origem do número: dado / estimativa / Suposição)

## Fora de escopo
- <item>

## Premissas
- <Suposição e o que muda se estiver errada>

## Perguntas abertas
(lista de todos os [NEEDS CLARIFICATION], com dono)

## Histórico
- AAAA-MM-DD: criação. AAAA-MM-DD: <mudança e motivo>
```

Regras: cada história é um MVP que entrega valor sozinha (P1 sozinha já é um produto útil); nenhum nome de framework, tabela ou biblioteca em `FR`/`SC`; toda lacuna vira marcador e aparece na lista final.

## Spec curta (N2)

Até 1 página. Use quando a mudança toca uma tela, endpoint ou regra simples.

```markdown
# Spec curta: <mudança>

Problema: <1 a 2 frases>
Comportamento esperado: <3 a 6 linhas, incluindo a falha principal>
Fora de escopo: <1 a 3 itens>
Critérios (cada um com check):
- C1: <regra + exemplo concreto> | Check: <comando ou verificação> | Oráculo: <resultado exato>
- C2 (negativo): ...
Perguntas abertas: <marcador + dono, ou "nenhuma">
```

Se a spec curta passar de uma página, o nível provavelmente é N3 (limiar Inferido).

## Spec de bugfix

```markdown
# Bugfix: <resumo>

## Comportamento atual
<o que acontece hoje, com passos de reprodução e dado concreto>
Reprodução: <passos ou comando>

## Comportamento esperado
<o que deveria acontecer, observável>

## Comportamento inalterado (guarda de regressão)
- <o que não pode mudar com a correção>   (peça pelo menos dois)

## Análise antes do design
- Inconsistências entre os três blocos: <lista ou "nenhuma">
- Lacunas: <caso de borda sem resposta> -> [NEEDS CLARIFICATION: ...]

## Critérios
| # | Critério | Check | Oráculo |
| --- | --- | --- | --- |
| B1 | atual -> esperado | reprodução do bug; deve falhar antes e passar depois | <resultado> |
| B2 | inalterado | <teste de regressão existente ou novo> | <resultado> |
```

## Escolha do formato de critério

Um padrão principal por spec (V-20). Não misture na mesma spec sem motivo.

| Formato | Use quando | Cuidado |
| --- | --- | --- |
| Regra + exemplo | padrão para quase tudo | todo exemplo com dado concreto |
| Given/When/Then | negócio lê, há contexto e estados | declarativo; um comportamento por cenário (V-17) |
| EARS | comportamento de sistema, regulado, embarcado | mais de 3 pré-condições fica pesado; requisito sem condição encaixa mal (V-20) |
| Checklist | itens independentes (campos, textos) | cada item verificável sozinho |

## Exemplos de FR e SC bons e ruins

| Ruim | Problema | Bom |
| --- | --- | --- |
| FR: "O sistema DEVE usar Redis para cachear a busca" | tecnologia no requisito | FR: "O sistema DEVE devolver o resultado da busca repetida em até X ms" (X a definir: `TBD`) |
| SC: "A API responde rápido" | sem número, sem oráculo | SC: "p95 da busca abaixo de `TBD` ms com `TBD` usuários simultâneos (origem: Suposição até medir)" |
| FR: "O sistema DEVE tratar erros de pagamento" | não diz qual erro nem o resultado | FR: "Se o gateway não responder em `TBD` s, o pedido DEVE ficar como 'aguardando pagamento' e a pessoa DEVE ver a mensagem X" |
| História: "Criar tabela de pedidos" | fatia horizontal, sem valor visível | História: "Como cliente, quero finalizar um pedido para receber em casa" |
| SC: "Aumentar a satisfação" | não mensurável | SC: "Nota média da pergunta X no pós-compra subir de `TBD` (baseline) para `TBD` em `TBD` semanas" |
