---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica que `crypto.randomUUID()` dentro do laço gera chave nova a cada tentativa e que isso anula a idempotência (o timeout após o gateway aceitar vira segunda cobrança).
2. Propõe gerar a chave uma vez por intenção de negócio (por exemplo derivada do pedido ou persistida na criação) e persisti-la antes da chamada externa; o retry reusa a mesma chave e o mesmo corpo.
3. Trata timeout como estado desconhecido: reusa a chave e/ou consulta o estado no provedor antes de reenviar, sem gerar chave nova para a mesma operação.
4. Menciona uma barreira no banco (constraint de unicidade ou reserva atômica) e que a mesma chave com corpo diferente deve ser erro.
5. Propõe teste que conta linhas no banco (duplo clique e timeout seguido de retry) como oráculo, não apenas a resposta da API.
6. Trata o cliente Android: o app deve reusar a mesma chave (gerada e guardada antes do envio) ou o servidor deriva a chave do pedido, para o reenvio do app não criar nova cobrança.
7. Usa rótulos ou ressalvas (Verificado, Inferido, Suposição, Não verificado) para o que depende do provedor (retenção da chave, comportamento com corpo diferente) e não afirma ter executado testes.
FAIL if qualquer um ocorrer: mantém uma chave nova por tentativa; propõe apenas cache em memória ou lock distribuído como proteção; promete exactly-once; afirma execução ou resultado de teste que não ocorreu; usa float para valor monetário na solução proposta.
