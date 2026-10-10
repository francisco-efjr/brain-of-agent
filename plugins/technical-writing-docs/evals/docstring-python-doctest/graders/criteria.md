---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final (ou no conteúdo de uma chamada Write):
1. A docstring usa aspas triplas, tem um resumo de uma linha com até 80 caracteres terminando em ponto, seguido de linha em branco e descrição curta; usa seções nomeadas no estilo Google (`Args`, `Returns`, `Raises`) e declara a escolha do estilo.
2. `Raises` documenta `ValueError` para texto vazio ou fora do formato (a exceção da interface); não documenta exceções de uso incorreto da API, como `AttributeError` ou `TypeError` para argumento que não é `str`.
3. Inclui exemplo no formato doctest (`>>> ` com a saída na linha seguinte) e as saídas estão corretas conforme o código: `parse_duration("1h30m")` resulta em `5400`, `"45s"` em `45`, `"2h"` em `7200`. Se mostrar o `ValueError` em doctest, a mensagem bate com o código (`duração inválida: 'abc'` para a entrada `"abc"`).
4. Não repete a assinatura (nome, tipos) como prosa redundante; a descrição diz o que a assinatura não diz (formatos aceitos h, m, s; partes opcionais; ordem).
5. Propõe o comando para rodar os exemplos (`python -m doctest -v` no arquivo, ou equivalente) e marca explicitamente que não foi executado, sem afirmar que os testes passaram.
FAIL if qualquer um ocorrer: saída de exemplo errada (por exemplo `5400` trocado, `"1h30m"` resultando em outro valor); afirma que o doctest passou ou que executou código; documenta exceção de uso incorreto; resumo com mais de 80 caracteres ou sem ponto; omite `Raises` do `ValueError`; altera o corpo da função.
