---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que `JSON.stringify(req.body)` não reproduz os bytes originais e quebra a verificação de assinatura (às vezes passa, às vezes falha), e que é preciso o corpo bruto; aponta também que `express.json()` global registrado antes da rota consome o corpo.
2. Aponta que `seen = new Set()` é dedupe em memória, perdido em reinício e inexistente entre as duas instâncias, e propõe tabela com unicidade do ID do evento (inbox persistida).
3. Recomenda responder 2xx rápido e processar em fila, em vez de atualizar o pedido dentro do handler.
4. Recomenda reler o recurso na API do provedor antes de mudar o estado e avisa que a ordem de entrega não é garantida (não ordenar por `created`).
5. Sugere testes hostis: assinatura forjada ou corpo alterado, evento duplicado, fora de ordem, com contagem de efeitos no banco como oráculo.
6. Declara o que é específico da Stripe (header `Stripe-Signature`, HMAC-SHA256 sobre timestamp e payload, tolerância de tempo) e não generaliza para outros provedores.
FAIL if qualquer um ocorrer: aprova o `JSON.stringify`; mantém o `Set` em memória como dedupe; sugere ordenar eventos por `created`; trata o evento como verdade sem releitura; inventa nome de header ou algoritmo; afirma ter executado o código.
