---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Explica que ênfase em CAPS, «CRITICAL» e «IMPORTANT!!!» tende a causar excesso de uso de ferramenta ou de rigidez em modelos atuais e a substitui por motivo e linguagem calma (a ênfase restante, se houver, fica em uma ou duas linhas).
2. Dá o motivo da regra sobre concorrentes e uma alternativa positiva (por exemplo, o que fazer quando o cliente citar um concorrente), em vez de manter a proibição seca.
3. Troca «se em dúvida use a ferramenta» por um critério de quando buscar o pedido (por exemplo, só quando houver número do pedido ou e-mail do cliente) e explica que o uso indiscriminado custa latência e chamadas.
4. Aponta que prefill (preencher a resposta do assistente com «{») não é mais suportado a partir da família Claude 4.6 e sugere saída estruturada (JSON schema) ou instrução de formato no lugar, avisando que o schema é validado por código.
5. Trata «pense passo a passo» como muleta de geração antiga em modelo com raciocínio e pede verificação ou ajuste de effort no lugar, ou explica que não é necessário.
6. Inclui um plano de teste (por exemplo, 3 tarefas reais com e sem a mudança, critério por tarefa) e diz que não executou o prompt.
FAIL if qualquer um ocorrer: aumenta a ênfase ou acrescenta mais CAPS; mantém o prefill como solução; reescreve sem explicar o motivo das mudanças; afirma que o prompt reescrito foi testado ou validado; inventa parâmetros de API.
