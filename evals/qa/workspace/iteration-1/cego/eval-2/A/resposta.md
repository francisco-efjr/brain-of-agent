**Veredito:** do jeito que está, a história ainda não está pronta para ser estimada. A intenção é clara e a necessidade é real, mas os três critérios de aceite não dão para testar (ninguém consegue dizer "passou" ou "falhou") e faltam as regras que definem o tamanho do trabalho. Eu levaria para amanhã como uma conversa para fechar essas lacunas e sairia do refinamento com a história dividida.

## O que está bom

- Persona, ação e valor estão claros. O "para não pagar por algo que não quero mais" mostra que o foco é o dinheiro voltar, e não só o pedido mudar de status. Esse foco deve guiar as decisões de escopo.

## Problemas nos critérios de aceite

**1. "o cliente pode cancelar o pedido"**
Só repete a história e não diz quando. Um pedido pago, em separação, enviado ou entregue tem tratamentos bem diferentes. Falta definir:
- em quais status o cancelamento é permitido;
- se cancela o pedido inteiro ou só alguns itens;
- se há confirmação e se o motivo é obrigatório;
- o que o cliente vê depois de cancelar.

**2. "o reembolso deve ser rápido"**
Não é verificável. Para o cliente, "rápido" pode ser minutos (Pix) ou até duas faturas (cartão), e parte desse prazo é do banco ou do gateway, fora do nosso controle. Vale separar o que prometemos do que depende de terceiros, por exemplo: "solicitamos o estorno em até [X] após o cancelamento e mostramos ao cliente o prazo estimado para cada meio de pagamento". Também falta definir:
- quais meios de pagamento entram (cartão, Pix, boleto, saldo, pagamento dividido);
- o que é devolvido (frete, cupom, cashback);
- o que acontece quando o estorno falha.

**3. "deve funcionar no app e no site"**
É um requisito de paridade, não um critério. Falta dizer:
- quais plataformas e versões mínimas (iOS, Android, versões antigas do app que o cliente não atualizou, navegadores);
- se a regra fica em um só lugar, no backend. Se ficar, a parte de cada canal é só tela, e é pequena. Se não, a história praticamente dobra de tamanho.

## Lacunas que a história não menciona

- **Pedido já despachado ou entregue:** vira recusa na entrega ou devolução? Em compra online no Brasil existe o direito de arrependimento de 7 dias (CDC, art. 49). Vale confirmar com jurídico/produto se isso entra aqui ou em outra história.
- **Efeitos colaterais:** liberar estoque, devolver cupom/cashback/pontos, cancelar nota fiscal (se já emitida), avisar logística ou vendedor (se houver marketplace).
- **Pedido com vários itens, entregas ou vendedores:** existe cancelamento parcial?
- **Concorrência e repetição:** o pedido é despachado no mesmo instante em que o cliente confirma o cancelamento; duplo clique; cancelar no app e no site ao mesmo tempo. O cancelamento precisa gerar um único estorno.
- **Falha no estorno:** gateway fora do ar ou estorno recusado. Precisa de nova tentativa automática, alerta e tratamento pelo atendimento.
- **Comunicação:** confirmação na tela, e-mail ou push, com valor e prazo.
- **Autorização e auditoria:** só o dono do pedido cancela; registrar quem cancelou, quando e por qual canal.
- **Atendimento:** o SAC pode cancelar em nome do cliente? Se sim, é outra história.
- **Métricas:** taxa de cancelamento, tempo até o estorno concluir, contatos ao SAC sobre reembolso.

## Perguntas para levar ao refinamento

| Pergunta | Quem responde |
|---|---|
| Em quais status o pedido pode ser cancelado pelo próprio cliente? | PO / operação |
| Cancelamento é sempre total ou também parcial? | PO |
| Quais meios de pagamento existem hoje e quais entram nesta entrega? | PO / pagamentos |
| Qual o prazo real de estorno por meio de pagamento e o que podemos prometer? | Pagamentos / financeiro |
| Frete, cupom e cashback voltam? | PO / financeiro |
| O que acontece com pedido já despachado? | PO / jurídico |
| Já existe API ou regra de cancelamento no backend, ou é do zero? | Time de desenvolvimento |
| Há integração fiscal, de estoque e de logística a avisar? | Dev / fiscal / logística |
| O app tem versões antigas em uso que precisam ser suportadas? | Mobile |

## Sugestão de divisão

A ideia é fatiar na vertical, para que cada pedaço já entregue valor ao cliente. Cancelar sem devolver o dinheiro não resolve a dor da história.

1. **Fatia fina:** cancelar pedido inteiro ainda não despachado, com estorno automático no mesmo meio de pagamento (comece pelo mais usado), pelo site, com e-mail de confirmação.
2. **Mesmo fluxo no app** (se o backend já estiver pronto na fatia 1, é só interface).
3. **Demais meios de pagamento** (boleto, saldo, pagamento dividido).
4. **Acompanhamento do reembolso** (status e prazo na tela do pedido).
5. **Fora de escopo por enquanto:** cancelamento parcial, pedido já despachado ou devolução, cancelamento pelo atendimento.

## Proposta de reescrita (para discutir)

Os valores entre [colchetes] precisam ser definidos por vocês. Não coloquei números porque não tenho como saber os prazos reais.

**História:** Como cliente com um pedido pago que ainda não saiu para entrega, quero cancelá-lo direto no app ou no site, para receber meu dinheiro de volta sem precisar falar com o atendimento.

**Critérios de aceite:**
1. Dado um pedido meu em status [pago / em separação], quando escolho "Cancelar pedido" e confirmo, então o pedido passa a "Cancelado" e vejo a confirmação com o valor e o prazo estimado do reembolso.
2. Dado um pedido já despachado ou em status posterior, então a opção de cancelar não aparece e vejo uma mensagem explicando o que fazer [devolução / atendimento].
3. Dado que o cancelamento foi confirmado, então o estorno de [valor total pago, incluindo frete? sim/não] é solicitado ao gateway no mesmo meio de pagamento em até [X minutos], e o prazo mostrado ao cliente é [Pix: ...; cartão: ...].
4. Dado que o estorno falha, então o pedido continua cancelado, o estorno é reprocessado automaticamente [N vezes] e, se persistir, gera alerta para o atendimento e aviso ao cliente.
5. Dado que o pedido foi despachado entre eu abrir a tela e confirmar, então o cancelamento é recusado com mensagem clara e nenhum estorno é gerado.
6. Dado um duplo clique ou uma segunda tentativa de cancelar o mesmo pedido, então existe um único cancelamento e um único estorno.
7. Dado o cancelamento, então estoque é liberado e cupom/cashback são [devolvidos / não devolvidos].
8. Recebo [e-mail / push] com a confirmação, o valor e o prazo.
9. O comportamento e os textos são os mesmos no site ([navegadores]) e no app ([iOS/Android, versão mínima]), com a regra única no backend.
10. Só o dono do pedido consegue cancelar, e o cancelamento fica registrado (quem, quando, canal).

Se quiser, transformo isso em cartões já divididos nas fatias acima, com os critérios de cada um.
