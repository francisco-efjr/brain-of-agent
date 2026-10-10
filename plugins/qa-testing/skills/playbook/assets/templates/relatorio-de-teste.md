# Relatório de teste: <sistema, build e data>

Como usar: o relatório apoia uma decisão (quase sempre "liberar ou não"). Ordem em que o gestor lê: recomendação, riscos, escopo, números, tendência, condições, decisões pedidas. Escreva em linguagem de negócio; troque "92% passaram" por quais fluxos passaram e quais falhas restam. Nunca misture verificado com inferido. Adaptado do brain-of-agent (MIT).

**Recomendação em uma linha:** <liberar / liberar com ressalvas / não liberar, e por quê>
**Pergunta ou decisão que esta execução informa:** <...>
**Ambiente e condições:** <versão, configuração, massa, janela; ambiente fora do ar ou dados faltando são risco>
**Critérios acordados antes de executar:** <fontes e limites>

## Riscos abertos (3 a 5, em linguagem de negócio)

| Risco | Efeito para o negócio | Decisão que pede | Dono e data |
| --- | --- | --- | --- |
| <clientes com cupom e frete grátis pagam até 10% a mais> | <campanha de 10/10 depende dessa combinação> | <corrigir antes da campanha> | <PO, 08/10> |

## Escopo

**Testado:** <fluxos e plataformas>
**NÃO testado e o risco que isso deixa:** <ex.: app iOS (8 casos; dispositivo indisponível): falha no checkout atingiria clientes iOS>

## Números (com denominadores)

| Planejados | Executados | Aprovados | Com falha | Bloqueados | Não executados |
| --- | --- | --- | --- | --- | --- |
| <n> | <n> | <n> | <n> | <n> | <n> |

Defeitos abertos por severidade: <bloqueador / crítica / alta / média / baixa, com IDs>. Tendência no ciclo: <abertos × fechados; estabilizando?>

## Achados relevantes

| ID | Impacto | Reprodução (resumo) | Estado |
| --- | --- | --- | --- |

## Rótulos e limitações

**Verificado** (executado, com evidência em `evidencia-de-teste.md`): <...> · **Inferido:** <...> · **Suposição:** <...> · **Não verificável:** <...>

## Decisões pedidas e próximos passos

| Decisão ou ação | Dono | Data |
| --- | --- | --- |

Versão curta para mensagem: "Release <v>, recomendação: <...>. Ressalva: <...>. Testado: <...> (<executados> de <planejados>, <aprovados> aprovados, <falhas> com falha). Não testado: <...>. Risco: <...>; mitigação: <...>. Defeitos abertos: <contagem por severidade>. Decisão pedida (<quem>, até <data>): <...>"
