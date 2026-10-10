---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Conclui que há vazamento entre empresas nas duas views: `listar` devolve faturas de todas as empresas com aquele status (faturas/views.py:10, contando o comentário do topo; tolerância de 2 linhas) e `detalhe` busca por `pk` sem filtro de empresa (faturas/views.py:17), de modo que qualquer usuário autenticado lê a fatura de outra empresa.
2. Explica que `login_required` prova autenticação, não autorização, e descreve um cenário em passos (usuário da empresa A chama `/faturas/<id de B>` e recebe o dado).
3. Propõe a correção no servidor com o tenant derivado da sessão (por exemplo `Fatura.objects.filter(org_id=request.user.org_id, ...)` e `get(pk=pk, org_id=request.user.org_id)`), nunca de parâmetro enviado pelo cliente; menciona levar o filtro para uma camada central (manager ou queryset base) para não depender de cada view lembrar.
4. Propõe testes de negação entre tenants: usuário da empresa B tenta ler a fatura de A (espera 404 ou 403 consistente), e o teste relê o recurso ou confere o conteúdo da resposta, em vez de checar apenas o status 200.
5. Se classificar tenant como categoria de risco, rotula como Inferido (derivado de IDOR e controle por atributos) ou equivalente; não afirma ter executado nada.
FAIL if qualquer um ocorrer: diz que está seguro porque há login; sugere esconder o botão, ofuscar IDs ou usar UUID como correção; aceita receber o tenant do cliente; propõe teste que só verifica status 200; afirma ter rodado testes ou lido o repositório.
