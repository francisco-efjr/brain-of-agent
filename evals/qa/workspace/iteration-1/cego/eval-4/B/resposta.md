Segue o bug pronto pra colar. Onde está **[preencher]** é algo que eu não tinha; vale completar antes de mandar, principalmente valores e evidência, que é o que mais ajuda o dev.

---

**Título**
[Android] Cupom BLACK10 some da tela ao trocar o CEP do endereço, mas o total mantém o desconto e o pagamento cobra sem desconto

**Ambiente**
- App Android 3.4.1
- Samsung Galaxy A54, Android [versão]
- Ambiente: [produção / homologação]
- Usuário/conta: [id ou e-mail]
- iPhone: não reproduz ([modelo, versão do app, nº de tentativas])

**Passos para reproduzir**
1. Carrinho com [itens] e endereço de entrega com CEP [A]
2. Aplicar o cupom BLACK10. O desconto aparece normalmente
3. Trocar o endereço de entrega para um com outro CEP [B]
4. Olhar o resumo do pedido
5. Ir para o pagamento e finalizar

**Resultado atual**
- Depois do passo 3, a linha de desconto do BLACK10 some do resumo, mas o **total continua com o desconto aplicado**. Ou seja, a tela se contradiz.
- No pagamento, foi cobrado o **valor cheio, sem desconto**.
- Pedido 88123: total na tela R$ [x], cobrado R$ [y].

**Resultado esperado**
Tela e cobrança coerentes entre si. Ou o BLACK10 continua valendo (linha de desconto, total e cobrança com desconto), ou, se o cupom não vale para o novo CEP, o desconto some do total também e o cliente é avisado antes de pagar. O que a tela mostra como total tem que ser o que é cobrado.

**Frequência**
Intermitente: 2 de 5 tentativas no A54. [O que foi diferente nas 3 vezes que não aconteceu?]

**Severidade**
Alta. O cliente vê um total e é cobrado um valor maior.

**Evidências**
- Pedido 88123 (cobrança sem desconto)
- [print/vídeo do resumo com desconto sumido e total descontado]
- [print da tela de pagamento ou comprovante com o valor cobrado]
- [horário aproximado das 2 ocorrências, para o dev buscar nos logs]

---

**Antes de enviar, 5 coisas que só você sabe:**

1. **Valores do 88123.** O total que apareceu e o que foi cobrado. Sem isso o dev não mede o tamanho do problema.
2. **O que mudou nas 3 vezes que deu certo.** Pode ser o CEP escolhido, a velocidade da troca, se esperou o resumo recalcular, a rede. Se você lembrar de qualquer diferença, é a pista mais útil de um bug intermitente.
3. **Quantas vezes testou no iPhone.** Se foi 1 ou 2, escreva "não reproduzi em N tentativas" em vez de "não acontece", porque com 2 em 5 isso não prova nada. Se tiver outro Android à mão, vale testar também: não dá para afirmar que é só do A54.
4. **Os passos.** Eu montei os passos 1, 4 e 5 por dedução (a ordem carrinho, cupom, endereço, pagamento). Corrija se o fluxo real for outro, por exemplo se a troca de endereço acontece dentro do checkout.
5. **O 88123 foi teste ou cliente real?** Se foi cliente real, a cobrança a mais precisa ser tratada à parte do bug (estorno ou ajuste), então vale avisar o suporte ou o financeiro agora.

Não coloquei hipótese de causa no texto porque ninguém confirmou nenhuma. O único fato que já aponta para algo é que tela e cobrança divergem, e isso já está no relato.
