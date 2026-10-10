# Revisão de netcode — [engine e versão]

Somente leitura. Godot: validar RPC é recomendação oficial. Unity NGO: a página de autoridade não trata de validar RPC (boa prática, Inferido). Replicação do Unreal e rollback: sem fonte validada.

| Objeto de rede | Autoridade declarada | Estado autoritativo muda só no servidor? | Cliente envia intenção, não resultado? | RPC valida faixa, dono e frequência? | Confia em posição, relógio ou recurso do cliente? |
| --- | --- | --- | --- | --- | --- |
| [objeto] | [servidor, dono...] | sim/não | sim/não | sim/não | sim/não |

## Achados

| # | `arquivo:linha` | Severidade | Cenário de abuso concreto | Correção | Confiança (1-10) |
| --- | --- | --- | --- | --- | --- |

## Teste

- [ ] Servidor e cliente executados juntos antes de "pronto" (comando: [..]; resultado: [..])

## Veredito

[sem achados | achados menores | achados que bloqueiam]

## Não avaliado

[replicação do Unreal, rollback, anti-cheat avançado, latência real]
