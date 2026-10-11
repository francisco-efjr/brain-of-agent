Montei o bug report com o que você me passou. Não reproduzi nada, então tudo abaixo vem do seu relato. O que eu não sei está marcado com **[preencher]**. Esses pontos são os que mais pesam para o dev conseguir agir sem te perguntar nada, então vale preencher antes de enviar (no fim tem uma lista curta do que coletar, por ordem de importância).

---

## Título

**Checkout Android: após trocar o CEP com BLACK10 aplicado, a tela mostra o total com desconto e o pagamento cobra sem desconto**

## Resumo

No app Android, ao aplicar o cupom BLACK10 e depois trocar o endereço de entrega para outro CEP, a linha de desconto some do resumo, mas o total continua com o desconto. No pagamento, o cliente é cobrado sem desconto, ou seja, paga mais do que a tela mostrava. Ocorreu 2 vezes em 5 tentativas; no iPhone não ocorreu.

## Ambiente

| Campo | Valor |
| --- | --- |
| Ambiente | **[preencher: produção ou homologação]** |
| App | Android 3.4.1 (build **[preencher]**) |
| Aparelho | Samsung Galaxy A54, Android **[preencher a versão, em Configurações > Sobre o telefone]** |
| Conta | **[preencher: conta de teste ou cliente real]** |
| Pedido afetado | 88123 |
| Data e hora (com fuso) | **[preencher, de cada uma das 2 ocorrências]** |

## Pré-condições

- Carrinho com **[preencher: itens e subtotal]**.
- Cupom BLACK10 válido (tipo e regra: **[preencher: percentual ou valor fixo? tem restrição de região ou frete?]**).
- Duas opções de endereço: CEP A **[preencher]** e CEP B **[preencher]**.

## Passos para reproduzir

1. Abrir o app Android 3.4.1 e entrar com a conta de teste.
2. Com o carrinho montado, ir ao checkout com o endereço do CEP A.
3. Aplicar o cupom BLACK10. Conferir que aparece a linha de desconto e que o total é **R$ [preencher]**.
4. Trocar o endereço de entrega para o CEP B.
5. Observar o resumo do pedido.
6. Seguir para o pagamento e confirmar com **[preencher: cartão, PIX...]**.

## Resultado esperado

O valor cobrado é igual ao total que a pessoa viu na confirmação, e o resumo é coerente consigo mesmo.

- Se BLACK10 continua válido para o CEP B: a linha de desconto permanece e o total e a cobrança têm desconto.
- Se BLACK10 não vale para o CEP B: o desconto sai da linha e do total, o app avisa a pessoa antes do pagamento, e a cobrança é igual ao total mostrado.

A regra de negócio de qual dos dois casos vale **[confirmar com dev/PO]**. Nos dois casos, tela e cobrança não podem divergir.

## Resultado obtido

- Após trocar o CEP, a linha de desconto some do resumo.
- O total continua com desconto: **R$ [preencher o total exibido]**.
- No pagamento do pedido 88123 foi cobrado **R$ [preencher o valor cobrado]**, sem desconto. Diferença: **R$ [preencher]**.

## Frequência

- Android 3.4.1, Samsung A54: **2 de 5** tentativas.
- iPhone: não ocorreu em **[preencher: quantas tentativas e qual versão do app iOS]**.
- Ainda não sei o que diferencia as 2 que falharam das 3 que não falharam: **[preencher: CEPs usados, tempo entre aplicar o cupom e trocar o CEP, rede]**.

## Evidências

- Pedido 88123: valor cobrado (extrato do pagamento ou tela do pedido).
- **[anexar]** Vídeo de tela de uma ocorrência, mostrando a troca do CEP e o resumo antes e depois, com o horário visível.
- **[anexar]** Print do resumo com o total exibido e o print/extrato com o valor cobrado.
- **[preencher]** Request id ou horário exato (com fuso) das 2 ocorrências, para o dev achar nos logs.
- Mascare nome, CPF, endereço completo e dados de cartão em prints e vídeos.

## Impacto

O cliente é cobrado por um valor diferente do que viu ao confirmar, e a diferença é o valor do desconto do BLACK10. O erro não aparece na tela, então a pessoa só percebe depois, no extrato. Isso gera chamado de suporte, pedido de estorno e possível contestação no cartão. Não há contorno para o cliente. Quantos clientes foram afetados: **ainda desconhecido** (o dev pode consultar pedidos do app Android 3.4.1 com BLACK10 e cobrança sem desconto).

Se o pedido 88123 for de cliente real, a correção do valor cobrado dele é uma ação à parte deste bug (suporte/financeiro).

## Classificação sugerida

| Eixo | Valor | Justificativa |
| --- | --- | --- |
| Severidade | Crítica | valor cobrado errado, sem contorno para o cliente |
| Prioridade | P1 se o BLACK10 estiver ativo para clientes reais; P2 caso contrário | cada pedido Android com troca de CEP pode ser afetado. Quem decide é o PO. Uma opção para ele é desligar o BLACK10 no Android ou bloquear a troca de CEP depois do cupom enquanto não houver correção |

## Hipóteses (não confirmadas, para o dev avaliar)

- A troca de CEP dispara um recálculo (frete e total) no servidor que descarta o cupom, e o app Android não atualiza o total exibido (estado local desatualizado). O iOS trataria essa resposta diferente.
- Corrida entre respostas: as 2 de 5 sugerem que o resultado depende de qual resposta chega por último (recálculo do frete e revalidação do cupom). Seria coerente com o defeito aparecer só às vezes.
- Sugestão para o dev: comparar a requisição e a resposta do recálculo logo após a troca de CEP em uma ocorrência com defeito e em uma sem.

---

## O que coletar antes de enviar (por ordem de importância)

1. **Valores do pedido 88123**: subtotal, frete, desconto, total exibido na tela e total cobrado. É o que prova o defeito em reais.
2. **Refazer o cenário mais 5 vezes no Android gravando a tela**, anotando em cada uma: CEP A e B, se o frete mudou de valor, se trocou o CEP logo depois de aplicar o cupom ou esperou, Wi-Fi ou 4G. Se as falhas tiverem algo em comum (por exemplo, só quando o frete muda), esse é o dado mais útil que você pode entregar ao dev.
3. **Horário (com fuso) e request id das 2 ocorrências.**
4. **Ambiente e conta**: produção ou homologação, cliente real ou conta de teste.
5. **Iphone com mais tentativas.** "Não acontece no iPhone" só sustenta uma conclusão se tiver tentativas suficientes: se a taxa fosse a mesma do Android (2 em 5, ou 40%), 0 falhas em 3 tentativas ocorre por acaso cerca de 22% das vezes, e em 5 tentativas cerca de 8%. Com poucas tentativas, escreva "não reproduzi no iOS em N tentativas" em vez de "só acontece no Android".
6. Se der, testar a versão anterior do app (3.4.0 ou a que estiver disponível) para saber se é regressão.

Fora deste bug, fica sem teste: outros cupons, outros fluxos de pagamento e outros aparelhos Android. Isso só vale investigar depois que o dev identificar a causa.
