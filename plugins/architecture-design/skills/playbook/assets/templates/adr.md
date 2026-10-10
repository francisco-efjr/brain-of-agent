<!--
Template de ADR consolidado. Base: assets/templates/adr.md do brain-of-agent (MIT, Francisco Edson),
fundido com a forma de Nygard e Fowler (V-13) e a governança do Azure Well-Architected (V-12).
Uso: preencha no chat, mostre ao usuário e só grave em docs/adr/adr-NNNN-slug.md após aprovação explícita (nome padrão: adote a convenção do projeto ou do pedido quando houver, por exemplo ADR-001-slug.md).
Não edite um ADR aceito: crie um novo que o substitui. Pontos sem resposta: [NEEDS CLARIFICATION: ...]. Sem humano para entrevistar (execução em lote), as perguntas viram esses marcadores e uma seção "Pendências".
-->
# ADR-[NNNN]: [título nominal, ex.: "PostgreSQL como banco do serviço de pedidos"]

Status: [proposto | aceito | substituído por NNNN | descontinuado]
Data: [AAAA-MM-DD] · Decidido por: [nome(s) humano(s)] · Confiança: [alta | média | baixa]
Revisar em: [data, obrigatório se confiança baixa]

## Contexto

[Problema, forças em tensão, restrições, requisitos e evidências, stack existente. Neutro: não defenda a decisão aqui. Afirmações sobre código com arquivo:linha; premissas sem evidência marcadas como Suposição.]

## Opções

Uma só tabela para todas as opções, as escolhidas e as rejeitadas (não repita a lista em outra seção).

| Opção | Benefício | Custo/risco | Compatibilidade | Evidência | Escolhida? Se não, motivo da rejeição |
| --- | --- | --- | --- | --- | --- |
| Não mudar nada | | | | | |
| [Opção B] | | | | | |
| [Opção C] | | | | | |

## Decisão

Vamos [ação em voz ativa]. [Por que esta opção, em duas ou três frases. Hipóteses ainda não confirmadas listadas.]

Se o status é `proposto` e o decisor está pendente, escreva em vez disso: "Decisão proposta (aguarda [nome ou papel do decisor]): vamos [ação em voz ativa]." A frase não registra uma decisão tomada; só o decisor a converte em "Vamos...". Não invente o decisor.

## Consequências

- Positivas: [ao menos uma]
- Negativas: [ao menos uma]
- Neutras: [ex.: tarefas novas, treinamento]
- Complexidade, operação, dados, migração, segurança e testes afetados: [lista]
- Reversibilidade: [limites e custo de desfazer; não prometa rollback de dados perdidos só porque existe migração down]

## Validação e gatilhos de reavaliação

- Critério observável que sustenta a escolha (teste, experimento, métrica): [ex.: p95 < 400 ms com carga X]
- Gatilho que reabre a decisão: [evidência concreta, ex.: "contenção de deploy entre equipes por 30 dias"]

## Links

[Requisitos, issues, ADRs relacionados (substitui / substituído por), diagramas]
