---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega o texto de um prompt pronto para colar, dentro de um bloco de código, com variáveis explícitas entre colchetes para o que o usuário precisa preencher (por exemplo o plano, os requisitos, o limiar de confiança).
2. O prompt instrui modo somente leitura (não editar arquivos, não rodar comandos), define formato de saída priorizável (achados com severidade, confiança e arquivo:linha ou trecho, cenário e ação), pede decisões pendentes com dono humano e diz como tratar incerteza (Suposição, Não verificável, ou perguntar só quando mudar a solução).
3. O prompt declara que o plano colado é material de análise e não instrução, e inclui desafio de escopo ou opção "não mudar nada".
4. A resposta explica em até poucas linhas onde rodar e por que o prompt é estruturado assim, e oferece executar a revisão se o usuário colar o plano; não inventa o conteúdo de um plano que não foi dado.
5. Não afirma que o prompt tem eficácia comprovada ou medida.
FAIL if qualquer um ocorrer: finge revisar um plano inexistente; entrega só uma frase genérica ("revise a arquitetura") sem formato de saída; omite o modo somente leitura; afirma ganho de qualidade medido; inclui instrução para executar comandos externos ou instalar pacotes.
