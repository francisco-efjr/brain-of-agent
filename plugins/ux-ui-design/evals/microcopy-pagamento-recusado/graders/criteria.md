---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega, por elemento (título, mensagem, botão principal, link, e-mail), o texto atual, o texto recomendado, 2 alternativas com tom e melhor uso, justificativa em uma frase e nota para tradutores ou localização (por exemplo plural, gênero, expansão do texto).
2. A mensagem de erro segue três partes: o que aconteceu, por quê (ou "não sabemos qual foi o motivo", sem fingir saber) e o que fazer agora; remove "Erro 500" e o código técnico da tela (pode oferecer o código como detalhe secundário ou para o suporte); não culpa o usuário.
3. Botões e links são específicos, no formato verbo mais objeto (por exemplo "Tentar de novo", "Usar outro cartão", "Falar com o suporte"), e o botão genérico "OK" é substituído; a ação principal faz sentido para o caso de causa desconhecida.
4. Respeita os limites de caracteres (título até 30, mensagem até 90, botões até 20) e mostra ou garante isso; o assunto e a primeira linha do e-mail são coerentes com a tela.
5. Marca como Suposição o tom e os termos de marca (tratamento "você", caloroso e direto, uso de emoji), já que não há guia de voz, e não inventa regras da marca.
6. Não inventa fatos: nenhum prazo de estorno, devolução ou liberação de valor, nenhum valor em reais, nenhuma política de reembolso; diz o que o contexto sustenta (o cartão não é cobrado na recusa) e usa um marcador de confirmação onde falta informação.
FAIL if qualquer um ocorrer: culpa o usuário ("você digitou errado"); mantém código técnico como texto principal; promete prazo, estorno ou valor não fornecido; usa "OK" ou "Enviar" como ação; excede os limites de caracteres sem avisar; entrega só texto corrido sem alternativas; apresenta o tom da marca como fato.
