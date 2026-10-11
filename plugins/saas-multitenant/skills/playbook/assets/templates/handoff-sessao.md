# Handoff e checkpoint de sessão (SaaS multi-tenant)

> Adaptado do template `handoff-checkpoint.md` do brain-of-agent (conteúdo próprio do usuário, MIT). Gere antes de a janela de contexto encher, ao trocar de sessão ou ao fim de um marco. Após duas ou três correções falhas sobre o mesmo ponto, gere o handoff, limpe o contexto e reescreva o pedido com o que aprendeu (V-15, V-22).

Objetivo e escopo autorizado:
Revisão atual, ambiente e modelo de tenancy:
Estado do workspace e mudanças preservadas:
Leituras completas, parciais e ausentes (e retomada):
Fontes de verdade e decisões (ADR, spec, tabela status → acesso):

## Entregue

| Item | Estado | Alteração | Evidência (comando e saída) | Rótulo |
| --- | --- | --- | --- | --- |
| | | | | Verificado / Inferido / Suposição / Não verificável |

## Verificado e inferido

- Verificado (saída colada nesta sessão): [..]
- Inferido (leitura de código, conhecimento estável): [..]
- Suposições ativas: [..]
- Não verificável (sem acesso, ferramenta ou banco): [..]

## Isolamento e billing: estado

- Testes de dois tenants: [executados com a role da aplicação? resultado]
- Contexto por transação / pool de tamanho 1: [..]
- Webhooks: duplicado, fora de ordem, assinatura inválida: [..]
- Decisões de produto pendentes (`past_due`, `paused`, downgrade): [..]

## Pendências, riscos e impedimentos

[..]

## Checks invalidados por mudanças posteriores

[..]

## Dados, integrações e limpeza

Dados sintéticos usados: [..] · Credenciais de teste usadas (nomes, nunca valores): [..] · Limpeza necessária: [..]

## Próxima ação concreta

[..]

Ao retomar, confirme revisão e workspace antes de assumir que este estado continua válido. Não incluir segredos nem dados pessoais desnecessários.
