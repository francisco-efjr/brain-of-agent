# Template: referência (quadrante: informação)

Fontes: V-11, GS-gen Step 3 (processo adaptado de garrytan/gstack, MIT). Neutra, completa e derivada do código: cada afirmação é rastreável a um arquivo lido. Espelha a estrutura do produto. Cobre 100% da superfície pública. **Sem "por quê" e sem passo a passo** (links para explicação e how-to). Exemplos ilustram, não instruem.

````markdown
# [NOME DA ENTIDADE]

[Um parágrafo: o que é, o que faz e quando se usa.]

## Interface

[Lista completa da superfície pública: funções, comandos, parâmetros. Inclua tipos, padrões e restrições.]

| Nome | Tipo | Padrão | Restrições | Descrição |
| --- | --- | --- | --- | --- |
| `[NOME]` | `[TIPO]` | `[PADRÃO]` | [ex.: até 256 caracteres, `^[a-z-]+$`] | [O QUE FAZ] |

"Aceita uma string" é insuficiente; "aceita uma string de até 256 caracteres que casa com `^[a-z-]+$`" é nível de referência.

## Opções e configuração

[Cada opção com tipo, padrão e efeito. Omita a seção se não houver.]

## Erros e códigos de saída

[Mensagens ou códigos, quando existirem, e o que significam.]

## Exemplos

[2 a 3 exemplos que funcionariam se copiados. Marque executado ou "não executado".]

## Relacionados

- How-to: [LINK] · Explicação: [LINK] · Tutorial: [LINK]
````

## Revisão

- [ ] Item por item: assinatura, tipos e padrões conferidos contra o código (Grep).
- [ ] Nenhum item da superfície pública ficou de fora (lista de exports comparada).
- [ ] Nenhuma recomendação nem opinião no texto.
- [ ] Termos iguais aos do código.
