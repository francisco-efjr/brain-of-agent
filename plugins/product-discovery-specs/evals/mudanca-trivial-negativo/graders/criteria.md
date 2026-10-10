---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Faz a troca pedida: `bg-[#1d4ed8]` passa a `bg-[#2563eb]` na variante primary, e mostra o diff ou o trecho alterado.
2. Não altera o que não foi pedido (a cor de hover, a variante secondary, a estrutura do componente). Pode mencionar em uma frase que o hover continua com `#1e40af` e perguntar se quer ajustá-lo, sem mudar por conta própria.
3. Responde de forma direta e curta, sem entrevista de requisitos, sem pedir critérios de aceite, sem criar spec, PRD, histórias ou plano e sem pedir aprovação de documento.
FAIL if qualquer um ocorrer: faz perguntas de requisitos antes de trocar a cor; produz spec, PRD, critérios de aceite ou tarefas; altera outras partes do arquivo; aciona skill ou agente do plugin product-discovery-specs.
