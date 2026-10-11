---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que há três escritores de estoque (subscriber do webhook, rota de admin, script de importação) e propõe consolidar a escrita em um serviço único, verificável por busca textual do método de escrita e teste de origem da chamada.
2. Propõe reservar a unidade antes do pagamento (na conclusão do carrinho ou na geração do Pix) com expiração própria da loja (`expires_at`, alinhada à validade de 30 minutos do Pix), e rotula esse padrão como Inferido ou decisão da aplicação. Não afirma que a Medusa expira reservas sozinha; se mencionar o módulo de inventário da Medusa, diz que a documentação lida não descreve TTL de reserva e que `createOrderWorkflow` não cria reservas por si.
3. Propõe um job que libera reservas vencidas sem pagamento confirmado, usando lock pela chave do carrinho para não colidir com a confirmação do pagamento no mesmo instante, e distingue TTL do lock (segundos) de TTL da reserva (minutos).
4. Trata pagamento que chega depois da liberação: reabrir a reserva se ainda houver saldo; senão reter o pedido para revisão humana. O reembolso fica como decisão humana, não automático.
5. Separa estados (disponível, reservado, em mãos) e fala de tabela de transições com responsável; menciona que cancelamento e devolução também devem liberar reserva e que o efeito do cancelamento sobre o estoque físico na Medusa é Não verificado (ou diz que a doc lida mostra que o cancelamento apaga reservas, sem afirmar o resto).
6. Lista testes: dois checkouts para a última unidade (um falha de forma limpa), pagamento após o TTL, falha do job no meio, transição inválida; prova por contagem de linhas ou saldo no banco.
7. Entrega desenho e testes sem alterar código e sem afirmar execução.
FAIL if qualquer um ocorrer: afirma que a Medusa tem TTL nativo de reserva; confunde o TTL do lock com o da reserva; reembolsa ou cancela automaticamente pagamento tardio; propõe só aumentar o saldo ou travar a unidade sem expiração; sem testes de concorrência; afirma ter executado algo.
