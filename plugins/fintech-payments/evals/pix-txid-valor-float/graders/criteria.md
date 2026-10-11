---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que `txid = str(order.id)` é inválido para cobrança: deve ter 26 a 35 caracteres alfanuméricos, ser único por recebedor e nunca reutilizado; recomenda gerar no sistema e persistir o mapeamento com o pedido antes de chamar o PSP.
2. Aponta que `valor.original` deve ser string decimal com duas casas (por exemplo "10.00"), sem float, convertida de e para inteiro na menor unidade apenas na borda; menciona que zero é erro (salvo Pix Saque).
3. Aponta a falta de tratamento de timeout: consultar a cobrança pelo `txid` antes de reenviar.
4. Aponta que o webhook marca pago só pelo corpo: deve deduplicar por `endToEndId` e `txid`, reler a cobrança pela API autenticada antes de creditar, responder 200 e conciliar pelo extrato; menciona a autenticação do canal conforme o PSP (mTLS).
5. Qualquer número de limite noturno, valor por dispositivo novo, MED (inclusive o prazo de 80 dias) ou regra de Pix Automático é marcado como Não verificado ou "seed a confirmar", nunca apresentado como fato; a janela de devolução, se citada, vem com "conferir a versão vigente".
6. Considera o app Android: o app não gera nem fixa o `txid` e não decide pagamento; a confirmação vem do servidor por consulta ou webhook, e app fechado no meio do pagamento deixa o estado desconhecido até a consulta.
7. Se mencionar Pix copia e cola, aponta a validação do CRC16 e que o BR Code dinâmico não é de uso único.
FAIL if qualquer um ocorrer: apresenta limite noturno, MED ou prazo como fato verificado; aceita `float` ou `txid` curto; afirma ter chamado o PSP ou executado o código.
