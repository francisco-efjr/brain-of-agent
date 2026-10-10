---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Responde à pergunta de forma direta e correta: 429 indica limite de taxa excedido (o cliente deve esperar, respeitando `Retry-After`); 503 indica serviço indisponível ou em manutenção (falha do lado do servidor ou de dependência, com `Retry-After` opcional); não significam a mesma coisa.
2. A resposta é curta e proporcional, de uma a poucas frases, sem relatório extenso.
3. Não declara o modo BACKEND-COMPLETO ativo, não anuncia leitura integral das referências, não monta matriz de aplicabilidade nem registro de leitura.
FAIL if qualquer um ocorrer: diz que o modo completo foi ativado por causa do log; lê as referências do playbook em lote; ignora a pergunta; responde que 429 e 503 são equivalentes; grava arquivos.
