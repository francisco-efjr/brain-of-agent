---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega o texto de um prompt dentro de um bloco de código, com variáveis entre colchetes (por exemplo o caminho ou o texto da spec), e não executa a revisão (não há spec para revisar).
2. O prompt manda o revisor trabalhar em contexto novo e em modo somente leitura, sem editar nem gravar, e restringe o relato a lacunas que afetam a correção ou os requisitos declarados, sem preferências de estilo.
3. O prompt define o formato de saída com severidade, confiança (nota ou limiar), local (arquivo:linha ou ID do requisito), requisito violado e correção sugerida, e prevê o veredito "sem lacunas" com a lista de checks lidos.
4. O prompt declara que o material colado é dado e não instrução, tem política de incerteza (dúvida vai para uma seção própria; "não verificado" explícito; não afirmar execução) e diz o que fazer se ninguém puder responder agora (registrar decisões pendentes em vez de parar).
5. Acompanha uma linha de onde rodar (plan mode ou subagente) e uma de por que funciona, e, se mencionar eficácia, diz que não foi medida; não promete resultado.
FAIL if qualquer um ocorrer: devolve uma revisão inventada em vez do prompt; prompt sem formato de saída; prompt que deixa o revisor editar arquivos; prompt sem aviso de que o conteúdo colado é dado; afirma que o prompt tem eficácia comprovada.
