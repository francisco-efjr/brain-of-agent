# Revisão da história "Cancelar pedido"

**Veredito: não pronta para desenvolver.** Os três critérios não têm resultado que possa dar errado (nenhum teste falharia), e a história mexe com dinheiro: o defeito caro aqui é reembolso feito em dobro, não feito, ou pedido já enviado que é cancelado. Sugiro levar ao refinamento as perguntas 1 a 4 abaixo; sem elas não dá para escrever critério nem estimar.

Supondo que o contexto seja um e-commerce com pedido, pagamento online (cartão, Pix, boleto) e envio, e que "pedido" pode ter mais de um item. Se algo disso estiver errado, parte da revisão muda.

## O que encontrei, critério por critério

| Trecho | Problema | Pergunta que o substitui |
| --- | --- | --- |
| "o cliente pode cancelar o pedido" | Não diz **quando**. Um pedido passa por criado, aguardando pagamento, pago, em separação, enviado e entregue; cancelar em cada um tem custo e efeito diferentes. Também não diz quem, nem se cancela o pedido todo ou itens. | Em quais estados pode cancelar, e o que o sistema faz em cada um? |
| "o reembolso deve ser rápido" | Sem número, nenhum teste falha. Também não diz valor (frete? cupom? parcelas?), nem forma (mesmo cartão, Pix, boleto?). | Em quanto tempo, medido de onde até onde, e quanto volta, para onde? |
| "deve funcionar no app e no site" | "Funcionar" não é resultado esperado. Não diz versões do app, nem se as regras e mensagens são iguais nos dois canais. | Que versões do app entram? O resultado é idêntico nos dois canais? |

O que a história não diz, mas alguém vai decidir (melhor o PO, agora, do que o dev na véspera):

- **Pedido ainda não pago** (Pix gerado, boleto em aberto): cancelar não tem reembolso, mas o código de pagamento precisa deixar de valer e a reserva de estoque ser liberada. Foi isso que o autor imaginou?
- **Pedido já enviado ou entregue:** é cancelamento ou é devolução/arrependimento? São fluxos diferentes. Para compra fora da loja física o CDC (art. 49) tem regra própria de 7 dias a partir do recebimento; confirme com o jurídico se esta história cobre isso ou se fica de fora.
- **Cancelar na mesma hora em que o pedido é despachado ou o pagamento é confirmado:** quem ganha?
- **Falha no meio:** gateway fora do ar ou sem resposta ao pedir o estorno. O que o cliente vê? O pedido fica cancelado com reembolso pendente? Quem é avisado?
- **Repetição:** duplo clique, ou cancelar nos dois canais ao mesmo tempo, não pode gerar dois reembolsos.
- **Permissão:** só o titular do pedido? Cliente sem login? Atendimento? Hoje nada impede que alguém cancele pedido alheio se a regra ficar só na tela.
- **Efeitos em volta:** estoque devolvido, nota fiscal (cancelamento ou nota de devolução), cupom (volta ou queima?), e-mail ou push de confirmação, logística avisada, relatório financeiro.
- **Rastro:** quem cancelou, quando, por qual canal e com qual motivo? O motivo é obrigatório?
- **Confirmação:** é ação irreversível; há tela de "tem certeza?" com o valor que será devolvido?

## Perguntas para o refinamento (por ordem de quanto bloqueiam)

| # | Pergunta | Dono sugerido |
| --- | --- | --- |
| 1 | Em quais estados do pedido o cliente pode cancelar sozinho? E nos demais, o que ele vê e para onde é encaminhado? | PO + logística |
| 2 | Qual o prazo do reembolso, em número, e **de qual relógio**? (nosso pedido de estorno ao gateway é uma coisa; o dinheiro aparecer na fatura ou conta é outra e depende do emissor/banco.) | PO + financeiro |
| 3 | O que volta: produtos, frete, juros de parcelamento? E para onde: mesma forma de pagamento? Pix e boleto devolvem para qual conta? | PO + financeiro |
| 4 | Cancela só o pedido inteiro ou também itens? E pedido com entregas parciais? | PO |
| 5 | O que o cliente vê enquanto o reembolso está em andamento e se ele falhar? Quem age quando falha? | PO + dev + financeiro |
| 6 | Quem pode cancelar (titular logado, convidado, atendimento)? | PO + segurança |
| 7 | Versão mínima do app que precisa suportar? Quem tem versão antiga vê o quê? | PO + mobile |
| 8 | Pedido já entregue entra nesta história? | PO + jurídico |

## Proposta de critérios (hipóteses para o PO aceitar ou corrigir)

Os valores entre colchetes dependem das respostas acima; os demais são exemplos concretos para o time reagir, não requisitos decididos.

1. **Cancelamento só nos estados permitidos.** Ex.: pedido "pago" e "em separação" cancelam; pedido "enviado" não mostra o botão e, se a chamada vier direto pela API, é recusada com mensagem que explica o motivo e o caminho (devolução). Nada muda no pedido.
2. **Só o titular cancela.** Ex.: Bia tenta cancelar, pela API, o pedido da Ana: recusado; o pedido da Ana continua intacto.
3. **Cancelar é uma vez só.** Ex.: duplo clique ou duas requisições idênticas resultam em **um** cancelamento e **um** reembolso; a segunda chamada devolve o resultado da primeira.
4. **Reembolso com valor e destino definidos.** Ex.: pedido de R$ 300,00 (R$ 280,00 em produtos + R$ 20,00 de frete) pago em 3x no cartão e cancelado antes do envio: [R$ 300,00 / R$ 280,00, conforme a pergunta 3] estornados no mesmo cartão, e o total estornado nunca passa do valor pago.
5. **Reembolso com prazo mensurável.** Ex.: o estorno é solicitado ao gateway em até [5 minutos] e o cliente vê "Reembolso solicitado em 06/10/2026, previsão de [prazo informado pelo meio de pagamento]".
6. **Pedido não pago.** Ex.: pedido com Pix gerado e não pago, cancelado: nada é cobrado, o QR deixa de ser aceito (pagamento depois do cancelamento é recusado ou devolvido, regra a definir) e o estoque reservado volta.
7. **Falha no reembolso é visível e não duplica.** Ex.: gateway sem resposta em [10 s]: pedido fica "cancelado, reembolso pendente", o cliente vê "Estamos processando seu reembolso", há retentativa que confere o status antes de reenviar, e o financeiro é alertado se não resolver em [prazo].
8. **Paridade entre canais.** Ex.: o mesmo pedido, nas mesmas condições, tem a mesma opção, o mesmo valor e a mesma mensagem no app (versões ≥ [N]) e no site; cancelar em um canal aparece no outro em até [N segundos] sem recarregar manualmente.

Cada um precisa de ao menos um caminho negativo, e os de 1, 3 e 7 pedem teste na API, não só na tela.

## Riscos e onde testar

| Risco (por dano) | Como testar | Nível |
| --- | --- | --- |
| Reembolso duplicado ou acima do pago | requisição repetida e concorrente; conferir o número de estornos no gateway, não só a tela | API/integração |
| Reembolso que nunca acontece (falha silenciosa) | gateway simulado devolvendo erro e timeout; conferir estado, retentativa e alerta | integração com simulador de gateway |
| Cancelar o que já foi enviado | cancelar pela API em cada estado do pedido | API |
| Cancelar pedido alheio | duas contas, ID cruzado | API |
| Cancelamento × despacho ao mesmo tempo | duas ações simultâneas no mesmo pedido; só uma vence, e o estado final é coerente | integração |
| Valor devolvido errado (rateio de cupom, frete, parcelas) | cálculo independente em centavos, nunca o valor que a tela mostra | unitário |
| Canais divergentes | mesma matriz de estados no app (versão atual e a mais antiga suportada) e no site | E2E enxuto + API |
| Estoque, nota fiscal e e-mails | conferir cada efeito colateral após o cancelamento | integração |

Ficou de fora desta revisão: desempenho em dias de pico (cancelamentos pós-Black Friday), acessibilidade do fluxo e métricas em produção (taxa de cancelamento, tempo até o reembolso). Vale decidir se entram na história ou em outra; o risco que sobra se ninguém decidir é descobrir isso em produção.

## Tamanho e decisão

Do jeito que está, a história provavelmente não cabe numa sprint: cancelamento por estado, reembolso por forma de pagamento (cartão, Pix, boleto) e dois canais são pelo menos três pedaços. Sugestão de divisão para discutir: (a) cancelar pedido ainda não enviado, no site; (b) reembolso por forma de pagamento, com tratamento de falha; (c) mesmo fluxo no app; (d) pedidos já enviados ou entregues (provavelmente é devolução, outra história).

- [ ] Pronta para desenvolvimento
- [ ] Pronta com ressalvas
- [x] **Não pronta:** faltam respostas às perguntas 1 a 4 (PO, financeiro, logística) e a decisão sobre o escopo pós-envio (PO e jurídico). Se o PO não tiver as respostas até o refinamento, a saída é dividir a história e refinar só a parte (a).

Nota sobre o que isto é: revisão do texto da história, com base num modelo comum de e-commerce. Não verifiquei nenhum sistema, regra real de estados ou contrato com o gateway; os estados e os exemplos são hipóteses para vocês confirmarem. Regra legal (como o prazo de arrependimento) deve ser confirmada com o jurídico antes de virar critério.
