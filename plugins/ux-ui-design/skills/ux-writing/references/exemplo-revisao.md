# Exemplo de revisão de microcopy

Caso sintético; produto e fatos são fictícios.

## Pedido

"Reescreve os textos da tela de pagamento recusado do app. Hoje aparece 'Erro 500: falha na transação' e um botão 'OK'. Quero tom caloroso mas direto. Limite do botão: 28 caracteres."

## Pré-checagens registradas

- Guia de voz: não encontrado no repositório informado; tom caloroso e direto vem do pedido (Suposição quanto ao registro exato, tratamento "você").
- Fatos disponíveis: o backend devolve apenas `status: declined`, sem motivo. Portanto o texto **não** pode afirmar a causa (saldo, limite, dados).
- Estado emocional provável: ansioso, no meio de uma compra.

## Saída

| Elemento | Atual | Recomendado | Alternativas | Justificativa | Nota de localização |
| --- | --- | --- | --- | --- | --- |
| Título | Erro 500: falha na transação | Pagamento não concluído | "Não conseguimos concluir o pagamento" (acolhedor, mais longo) | tira o código, diz o que aconteceu | título curto cabe em uma linha; "concluído" concorda com "pagamento" |
| Corpo | (ausente) | O cartão foi recusado e a compra não foi finalizada. Você pode tentar outra forma de pagamento ou falar com o suporte. | Neutro: "O pagamento não foi aprovado. Escolha outra forma de pagamento ou fale com o suporte." / Acolhedor: "Isso acontece. Tente outra forma de pagamento; se preferir, nosso suporte ajuda." | três partes sem inventar motivo; remédio prático | "forma de pagamento" é feminino; tradução deve manter a concordância |
| Botão primário | OK | Pagar de outra forma (20 car.) | "Usar outro cartão" (17 car.; direto, quando a causa provável é o cartão) / "Tentar de novo" (14 car.; neutro, se o erro for temporário) | verbo + objeto leva à próxima ação; cabe no limite | "outra forma" concorda com o feminino; em inglês, "Pay another way" |
| Botão secundário | (ausente) | Falar com o suporte (19 car.) | "Pedir ajuda" (11 car.) | saída para quem não resolve sozinho | |
| Status do pedido | (ausente) | Seu pedido continua salvo no carrinho. | — | só se o produto realmente mantém o carrinho | **Pendência de fato:** confirmar com o time |

Contagens de caracteres (com espaços) conferidas por script em 2026-10-10: todas as opções de botão ficam abaixo do limite de 28.

## Checagem das diretrizes de erro

| Diretriz | Nota | Observação |
| --- | --- | --- |
| 5 Linguagem simples, sem códigos | excelente | código removido |
| 6 Problema específico | bom | não há motivo conhecido; o texto é honesto sobre isso |
| 7 Remédio prático | excelente | dois caminhos claros |
| 8 Tom neutro, sem culpa | excelente | "o cartão foi recusado", não "você errou" |
| 10 Preservar o que foi digitado | não verificado | depende do produto manter os dados do cartão |
| 13 Falha total | não aplicável | falha pontual do pagamento |

## Pendências e suposições

- Fatos a confirmar: motivo real do erro quando o backend passar a retorná-lo; se o carrinho é preservado; canal e horário do suporte. Nenhum prazo de estorno ou reembolso foi mencionado, de propósito.
- Suposição: tratamento "você" e registro caloroso, sem guia de voz.
- Não testado com usuários; a clareza do texto só se confirma em teste.
