# Tabela de estados do pagamento

Base: V-12 (máquina de estados de pagamento; precedência de evidências definida pelo plugin, **Inferido**). Uma linha por estado. A coluna "Evidência de entrada" diz **qual fato** autoriza entrar no estado, e de qual fonte na precedência: (1) extrato de liquidação · (2) consulta autenticada ao provedor · (3) evento de webhook verificado · (4) resposta síncrona ou redirecionamento · (5) comando. Estados da linha abaixo são um exemplo de cartão com captura; adapte a Pix e boleto (sem autorização e captura separadas).

## Entidades (separadas, cada uma com seu próprio estado)

pedido · intenção de pagamento · tentativa · autorização · captura · liquidação · estorno · disputa · lançamento no ledger · entrega. Valores **autorizado**, **capturado** e **estornado** ficam em colunas próprias, fora do status.

## Estados e transições

| Estado | Evidência de entrada (fonte 1 a 5) | Estados anteriores permitidos | Comandos aceitos | Timeout e ação | Efeito no ledger | Compensação se a evidência chegar tarde |
| --- | --- | --- | --- | --- | --- | --- |
| `pending` | intenção persistida com chave de idempotência (5) | — | chamar o provedor | [prazo do projeto]; consultar o provedor, **nunca** reenviar com chave nova | nenhum | — |
| `requires_action` | resposta do provedor pedindo 3DS/ação (4) + consulta (2) | `pending` | confirmar | [≥ 5 min no SDK de 3DS (V-39)]; abandono → `failed` | nenhum | — |
| `authorized` | consulta (2) ou evento verificado (3) | `pending`, `requires_action` | capturar, anular | janela de captura do provedor [conferir]; expira → `void` | reserva (`pending` do ledger) | anulação |
| `captured` | consulta (2) ou evento verificado (3) | `authorized` | estornar | — | `post` da reserva | estorno ligado |
| `settled` | linha do extrato (1) | `captured` | — | — | movimento para saldo disponível | ajuste classificado e aprovado |
| `refunded_partial` / `refunded` | evento verificado (3) + consulta (2) | `captured`, `settled` | estornar mais (≤ saldo estornável) | [prazo de estorno do provedor] | estorno ligado ao original | — |
| `failed` | recusa definitiva (2 ou 3) | `pending`, `requires_action`, `authorized` | nova tentativa = nova intenção e nova chave | — | `void` se havia reserva | — |
| `disputed` | evento de disputa (3) + consulta (2) | `captured`, `settled` | responder, aceitar | prazo da bandeira [conferir] | débito da disputa registrado | resultado `won`/`lost` no ledger |
| `indeterminate` | timeout/resposta perdida | qualquer estado de chamada externa | consultar o provedor | [prazo do projeto] | nenhum até resolver | resolver por referência/`txid`/`EndToEndId` |

## Regras de transição

- Transição por `UPDATE ... WHERE state = <anterior permitido>` com chave de idempotência, origem e tempo observado; `rowcount` 0 = transição inválida ou obsoleta → **fila de conciliação**, nunca descartar nem forçar.
- Evento fora de ordem **converge**: releia o recurso; não ordene por `created`.
- Sucesso tardio depois de retry é evidência nova: registrar compensação no ledger.
- Redirecionamento do cliente (4) **nunca** libera produto sozinho; boleto e Pix só entregam após (2) ou (3).
- Transição entre `captured` e `settled` só pelo extrato (1) ou por consulta que o confirme.

## Verificação

- Teste por transição válida e por transição inválida (matriz estado × comando).
- Teste de timeout em cada chamada externa e de evento duplicado e fora de ordem.
- Auditoria: nenhum pagamento em `captured` sem lançamento correspondente; nenhum lançamento sem pagamento.
- Rótulo: precedência de evidências = **Inferido**; estados de provedor = conforme a documentação da versão lida ([versão, data]).
