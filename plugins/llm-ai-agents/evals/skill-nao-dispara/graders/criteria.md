---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Reescreve a `description` dizendo o que a skill faz (extrair tabelas, preencher formulários, juntar PDFs), quando usar (com gatilhos concretos como «extrair tabelas de PDF», «preencher formulário PDF», «juntar PDFs», extract tables, merge PDFs), em português e em inglês, e quando NÃO usar (por exemplo, outros formatos de documento ou OCR de imagem), com no máximo 1024 caracteres e o caso de uso no início.
2. Explica por que «Helps with PDFs» não dispara (é vaga; não diz quando usar) e que a description é o que decide o acionamento automático.
3. Monta ou descreve um conjunto de teste de disparo com cerca de 20 consultas, metade positivas e metade quase-acertos negativos (parecem do domínio mas não devem disparar), com divisão aproximadamente 60/40 entre treino e teste e cada consulta executada mais de uma vez.
4. Mantém tom calmo: nenhuma ênfase em CAPS nem «ALWAYS USE THIS SKILL»; «insistente» significa gatilhos e exclusões concretos.
5. Aponta ajustes secundários úteis (corpo abaixo de 500 linhas, detalhes em references, efeito colateral com `disable-model-invocation`, seção de armadilhas) sem reescrever a skill inteira.
6. Diz que não executou o teste de disparo e que o resultado é hipótese até rodar (por exemplo com `claude -p` ou `claude plugin eval`).
FAIL if qualquer um ocorrer: declara que testou ou que a skill agora dispara; sugere CAPS, «ALWAYS USE» ou ameaça na description; não inclui consultas negativas; não menciona divisão treino e teste; deixa a description sem gatilhos em português ou inglês.
