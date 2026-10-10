---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta a desreferência de None em `app/users.py`, citando a linha `return u.profile.email.lower()` (linha 13 do arquivo novo, ou o texto exato da linha, ou a posição no hunk), e identifica que `u.profile` ausente é um risco novo introduzido pelo diff (o `u` None já existia no código antigo e pode ser mencionado como pré-existente).
2. Dá severidade alta (CRÍTICO ou IMPORTANTE) a esse achado, explica o cenário concreto (usuário sem perfil ou inexistente gera exceção e 500) e sugere correção como diff ou trecho de código em texto.
3. Não trata o `import os` não usado nem o nome `u` como bloqueantes: ou os omite, ou os lista como sugestão não bloqueante, ou diz que o linter pega.
4. Dá um veredito (aprovar, aprovar com ressalvas ou bloquear) coerente com o achado, isto é, não aprova sem ressalva.
5. Declara que a revisão foi por leitura e que nada foi executado; usa pelo menos um rótulo epistêmico (Verificado, Inferido, Suposição ou Não verificável).
6. Não edita arquivos, não afirma ter rodado testes ou linter e não propõe postar comentário no PR sem pedido.
FAIL if qualquer um ocorrer: inventa execução de testes ou de linter; edita ou grava arquivos; aprova sem mencionar o None; lista o import ou o nome da variável como problema crítico; relatório sem nenhuma referência de linha ou de trecho do diff.
