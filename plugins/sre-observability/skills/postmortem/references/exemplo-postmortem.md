# Exemplo: de notas com culpa a postmortem blameless

Cenário fictício. Rótulos: Verificado = tem fonte colada; Inferido = relato de memória; Suposição = estimativa sem medição.

## Notas recebidas

"Seg 03/08 ~22:10 BRT o João fez deploy da v3.2 sem rodar o teste de migração; a tabela `orders` travou; checkout fora ~47 min; 1.200 pedidos falharam (estimativa do Pedro); rollback às 22:57 pelo Carlos; ninguém avisou o suporte; soubemos pelo Twitter."

## Pontos a tratar antes de escrever

| Problema nas notas | Tratamento |
| --- | --- |
| Nomes como agentes da causa | Trocar por papéis: autor da mudança, plantonista, OL |
| "Sem rodar o teste de migração" como falha individual | Perguntar por que o pipeline permitia promover sem esse teste |
| "~22:10 BRT" e "Seg 03/08" | Pedir fuso e ano; se 2026 e BRT = UTC-3, 22:10 BRT = 01:10 UTC de 04/08 (Suposição de conversão, a confirmar) |
| "1.200 pedidos (estimativa)" | Manter como Suposição e anotar como medir (pedidos com erro nos logs do checkout) |
| "Soubemos pelo Twitter" | Falha de detecção: nenhum alerta cobriu a jornada de checkout |

## Rascunho (trecho)

```markdown
# Postmortem: checkout indisponível após migração da v3.2
Gatilho: indisponibilidade acima do limite e falha de monitoramento · Severidade: a definir (Suposição P1)
Autor do rascunho: IA (assistente), revisão humana pendente

## Impacto
- Duração: cerca de 47 min (fonte: notas do canal; cruzar com métrica de erro do checkout) (Inferido)
- Pedidos com falha: cerca de 1.200 (estimativa de um participante, sem medição) (Suposição)
- Dados perdidos: não informado (Não verificável)

## Linha do tempo (UTC, conversão a confirmar)
| Horário UTC | Evento | Fonte | Rótulo |
| --- | --- | --- | --- |
| ~01:10 | Deploy da v3.2 iniciado pelo autor da mudança | notas do canal | Inferido (memória) |
| ~01:10 a 01:57 | Tabela `orders` travada; checkout fora | notas do canal | Inferido |
| ? | Suporte e plantão percebem o problema pela rede social | notas do canal | Inferido, horário ausente |
| ~01:57 | Rollback concluído pelo OL | notas do canal | Inferido |

## Causas contribuintes (candidatas; confirmação humana pendente)
1. A migração chegou à produção sem a validação de bloqueio de tabela; o pipeline não exige o teste de migração antes da promoção.
2. Nenhum alerta cobria a jornada de checkout; a detecção veio de fora da empresa.
3. Sem canário: a mudança foi para 100% do tráfego de uma vez.

## O que funcionou / o que não funcionou
- Funcionou: rollback completo em cerca de 47 min.
- Não funcionou: detecção (fonte externa), comunicação com o suporte, ausência de aviso interno.

## Ações de acompanhamento (proposta; aprovação humana pendente)
| Ação | Dono | Prazo | Prioridade | Critério de conclusão |
| --- | --- | --- | --- | --- |
| Tornar o teste de migração obrigatório no pipeline | Equipe de plataforma | a definir | alta | Promoção bloqueada sem o teste (demonstrada) |
| Alerta de burn rate para `POST /pedidos` | Dono do serviço | a definir | alta | Disparo e reset provados em teste |
| Canal de aviso interno para o suporte em incidente | CL | a definir | média | Procedimento no runbook |

## Não sabemos ainda
- Hora exata do primeiro erro e do primeiro alerta (se houve).
- Quantos pedidos foram retomados pelos clientes.
- Por que o teste de migração não faz parte do pipeline.
```

## Lint do rascunho acima (resultado esperado)

- Culpa: zero termos da lista; "ninguém avisou" virou falha de detecção e de comunicação.
- Nomes próprios: zero; papéis em vez de pessoas.
- Horários: todos com fonte e rótulo; os ausentes aparecem como `?`.
- Causa raiz: apresentada como candidata; a decisão é dos humanos.
