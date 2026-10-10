# As 13 diretrizes de mensagens de erro (NN/g), em quatro dimensões

Fonte: Tim Neusesser e Evan Sunwall, "Error Message Guidelines", NN/g, 2023-05-14 (https://www.nngroup.com/articles/error-message-guidelines/). Conteúdo © NN/g: abaixo só há destilação com redação própria e exemplos do plugin (V-12; Verificado: 13 diretrizes em 4 dimensões, não 12 em 3). Os exemplos da fonte são de 2023; confira a página antes de citar.

## Como pontuar

Para cada mensagem, avalie cada diretriz aplicável com ruim (0), regular (1), bom (2) ou excelente (3), e registre a média e a nota mais baixa. A nota mais baixa orienta a correção; a média sozinha esconde o problema. Diretriz não aplicável ao contexto fica de fora da média, com o motivo.

## Visibilidade (4)

| # | Diretriz | Pergunta de teste | Exemplo ruim → melhor |
| --- | --- | --- | --- |
| 1 | Mostrar perto da origem | O erro aparece junto ao campo ou elemento que o causou? | banner no topo da página → texto abaixo do campo "CPF" |
| 2 | Cues redundantes, não só cor | Há texto, ícone ou padrão além da cor? | borda vermelha só → ícone + texto "Informe o CPF" |
| 3 | Destaque proporcional à gravidade | Modal só para erro que bloqueia? | modal para "Cupom expirado" → mensagem inline ao lado do cupom |
| 4 | Não acusar cedo demais | O erro aparece só depois de a pessoa terminar de digitar? | "E-mail inválido" ao digitar a primeira letra → validar ao sair do campo ou ao enviar |

## Comunicação (4)

| # | Diretriz | Pergunta de teste | Exemplo ruim → melhor |
| --- | --- | --- | --- |
| 5 | Linguagem simples, sem códigos | Uma pessoa leiga entende sem pesquisar? | "Erro 403 Forbidden" → "Você não tem permissão para ver esta página. Peça acesso a quem administra a conta." |
| 6 | Problema específico | Diz exatamente o que falhou? | "Dados inválidos" → "A senha precisa ter pelo menos 8 caracteres." |
| 7 | Remédio prático | Diz o que fazer agora? | "Falha no envio" → "Não conseguimos enviar. Confira sua conexão e tente de novo." |
| 8 | Tom neutro, sem culpa | Evita "você errou", humor e exclamação? | "Você digitou errado!" → "Esse e-mail não parece completo. Exemplo: nome@exemplo.com." |

## Eficiência (4)

| # | Diretriz | Pergunta de teste | Exemplo ruim → melhor |
| --- | --- | --- | --- |
| 9 | Prevenir erros prováveis | O design evita o erro antes (máscara, seletor, restrição, aviso)? | campo livre de data → seletor de data com formato visível |
| 10 | Preservar o que foi digitado | O formulário mantém os dados depois do erro? | limpar tudo ao falhar → manter os campos e marcar só o inválido |
| 11 | Sugerir correções prováveis | Oferece a correção quando é conhecida? | "E-mail inválido" → "Você quis dizer nome@gmail.com?" (só se a sugestão for confiável) |
| 12 | Explicar brevemente, com link para detalhe | Mensagem curta e acesso ao detalhe opcional? | parágrafo longo → frase curta + "Saiba por que isso acontece" |

## Falha total (1)

| # | Diretriz | Pergunta de teste |
| --- | --- | --- |
| 13 | Mitigar a falha total do serviço | Se o serviço inteiro falha, a pessoa sabe o que acontecerá com o que fazia, se algo foi perdido e onde buscar ajuda ou alternativa? |

Aplicação restrita (V-12): a diretriz 13 só se aplica a indisponibilidade ampla. O enunciado das perguntas acima é do plugin (Inferido); consulte a fonte para o texto original.

## Modelo de mensagem em três partes

```text
O que aconteceu + por quê (se o sistema sabe) + o que fazer agora

Pagamento não concluído. O cartão foi recusado pelo emissor.
Escolha outra forma de pagamento ou confirme os dados do cartão.
```

Sem o motivo conhecido, omita o "por quê" em vez de inventá-lo: "Não conseguimos concluir o pagamento. Tente outra forma de pagamento ou fale com o suporte."
