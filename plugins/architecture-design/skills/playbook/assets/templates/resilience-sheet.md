<!-- Folha de resiliência e consistência. Responda sim, não ou N.A. (com motivo). Leia "quando NÃO usar" em resiliencia-e-consistencia.md antes. -->
# Folha de resiliência: [fluxo ou integração]

Data: [AAAA-MM-DD] · Falha parcial concreta analisada: [qual efeito já aconteceu, qual processo morre, o que o chamador sabe]

## Retry
| Item | Resp. | Nota |
| --- | --- | --- |
| Falha transitória? | | |
| Operação idempotente ou com chave? | | |
| SDK ou cliente já repete? | | |
| Limite de tentativas e orçamento de tempo | | |
| Atraso exponencial com jitter | | |
| Só uma camada repete | | |
| Logs: tentativas como info, última como erro | | |

## Circuit breaker
| Item | Resp. | Nota |
| --- | --- | --- |
| Limiar e janela | | |
| Tempo aberto e crescimento | | |
| Chamadas de teste no meio-aberto | | |
| Fallback definido | | |
| Evento e alerta por transição | | |
| Um breaker por dependência ou shard | | |
| Timeout do chamador curto | | |
| A plataforma (DLQ, mesh) já cobre? | | |

## Bulkhead
| Item | Resp. | Nota |
| --- | --- | --- |
| Dependências que podem esgotar recurso compartilhado | | |
| Pool ou fila separada, tamanho medido | | |
| Limite da plataforma já disponível | | |
| Alerta por pool; custo de menor utilização aceito | | |

## Consumidor idempotente
| Item | Resp. | Nota |
| --- | --- | --- |
| Chave estável (não CorrelationId) | | |
| Operação naturalmente idempotente? | | |
| Marcador e efeito na mesma transação | | |
| Unicidade no banco | | |
| Em andamento / concluído para efeito externo | | |
| Retenção maior que redelivery e DLQ | | |
| Métrica de duplicatas; chave nos logs | | |
| Ordem tratada (sessão, partição, versão) | | |

## Outbox
| Item | Resp. | Nota |
| --- | --- | --- |
| Estado e evento na mesma transação | | |
| ID estável do evento | | |
| Publicador assíncrono com retomada | | |
| Ordem por agregado | | |
| Retenção com margem de dias | | |
| Consumidor idempotente | | |
| Biblioteca pronta avaliada | | |

## Saga
| Item | Resp. | Nota |
| --- | --- | --- |
| Compensação por passo | | |
| Pivô marcado; passos pós-pivô idempotentes | | |
| Coreografia só com poucos serviços | | |
| Bloqueio semântico em registros em edição | | |
| Monitoramento do estado da saga | | |
| Plano para compensação que falha | | |

## CQRS e event sourcing (só se propostos)
Cinco perguntas de CQRS respondidas? [sim/não] · O benefício de event sourcing justifica o custo? [..] · Estratégia de versionamento de eventos definida antes do primeiro evento? [..]

## Testes que provam
| Propriedade | Teste | Existe? |
| --- | --- | --- |
| Duplicata inofensiva | mensagem enviada 2x, 1 efeito | |
| Crash após commit | publicador retoma do outbox | |
| Timeout com aceitação desconhecida | estado pendente, não falha | |
| Compensação que falha | alerta e novo ciclo | |
| Retry único | contagem de tentativas = limite de uma camada | |

## Não verificado
[..]
