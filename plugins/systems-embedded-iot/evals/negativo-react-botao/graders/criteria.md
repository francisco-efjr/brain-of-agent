---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega um componente React de botão primário com Tailwind e um estado de loading (por exemplo, `isLoading`, `disabled` e `aria-busy` durante o carregamento).
2. Entrega testes com Testing Library que cobrem pelo menos o estado normal e o estado de loading.
3. A resposta não menciona firmware, microcontrolador, gravação em placa, ISR nem o modo EMBARCADOS-COMPLETO, e não produz relatório, matriz ou checklist de embarcados.
FAIL if qualquer um ocorrer: ignora o pedido; produz conteúdo de firmware ou IoT; anuncia modo completo; entrega apenas texto genérico sem código.
