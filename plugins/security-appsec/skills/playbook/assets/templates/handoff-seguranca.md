# Handoff de segurança

Checkpoint de continuidade (inspirado no `handoff-checkpoint.md` do brain fullstack, MIT do usuário). Gere ao fim de uma revisão ou de cada lote do modo SEGURANCA-COMPLETO, e antes de a janela de contexto encher. Quem retomar lê só este arquivo e abre os artefatos citados.

## Entregue

- Pedido original e escopo: <...>
- Status: <completo | parcial | não avaliado>
- Artefatos: <relatório, patch, matriz, caminhos>

## Verificado, Inferido, Suposição, Não verificável

- Verificado (com comando ou `arquivo:linha`): <...>
- Inferido: <...>
- Suposição: <...>
- Não verificável: <...>

## Achados em aberto

| ID | Severidade | Estado (Mantido, VERIFY, corrigido, refutado) | Local | Próxima ação |
| --- | --- | --- | --- | --- |
| <VULN-001> | <...> | <...> | <arquivo:linha> | <...> |

## Registro de leitura (modo SEGURANCA-COMPLETO)

| Arquivo | lido, parcial ou ausente | Decisão extraída |
| --- | --- | --- |
| <caminho> | <...> | <...> |

## Pendências e decisões humanas

- <ex.: rotacionar a credencial X (ação humana); autorizar teste em homologação; decidir sobre reescrever o histórico>

## Riscos e limitações

- <lacunas: LGPD, JWT, SAST/DAST, cloud/IaC>; revisão por modelo é uma camada; revisor e autor são o mesmo modelo? <sim/não>

## Próximo passo

<uma ação concreta>

## Retomar

Comece lendo: <arquivos>. Não repita: <o que já foi verificado>. Comandos úteis: <...>. Não execute nada que exija autorização que ainda não foi dada: <lista>.
