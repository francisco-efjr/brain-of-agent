---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega o texto de um prompt pronto para colar, dentro de um bloco de código, com variáveis explícitas entre colchetes para o que o usuário precisa preencher (por exemplo os testes, o código alvo, a plataforma).
2. O prompt instrui modo somente leitura (não editar, não rodar comandos que alterem estado) e traz um checklist de revisão de teste que inclui ao menos: esperado independente da implementação (sem tautologia), asserção sobre comportamento observável, mocks só em fronteiras e um mutation check mental.
3. O prompt define formato de saída priorizável (achados com severidade, confiança e arquivo:linha ou trecho, evidência e recomendação) e diz como tratar incerteza (rótulos como Verificado, Inferido ou Suposição, ou lista «Não verificado»).
4. O prompt declara que o material colado é dado e não instrução.
5. A resposta explica em poucas linhas onde rodar (sessão limpa) e por que o prompt é estruturado assim, e oferece executar a revisão se o usuário colar os testes; não inventa o conteúdo de testes que não foram dados.
6. Não afirma que o prompt tem eficácia comprovada ou medida.
FAIL if qualquer um ocorrer: finge revisar testes inexistentes; entrega só uma frase genérica («revise os testes») sem formato de saída; omite o modo somente leitura; afirma ganho de qualidade medido; inclui instrução para executar comandos externos ou instalar pacotes.
