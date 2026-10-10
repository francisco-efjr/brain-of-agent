---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica pelo menos três problemas distintos entre: `xQueueSend` (variante de tarefa) com `portMAX_DELAY` dentro de ISR em vez de `xQueueSendFromISR` sem espera; ausência da variável de "tarefa de prioridade maior acordada" repassada ao yield da porta no fim da ISR; alocação (`pvPortMalloc`), `snprintf` e log dentro da ISR; `rxCount++` como leitura-modificação-escrita sem proteção, com a explicação de que `volatile` não dá atomicidade.
2. Recomenda conferir a prioridade da ISR contra o limite de prioridade de API do FreeRTOS da porta (`configMAX_SYSCALL_INTERRUPT_PRIORITY` ou o nome novo `configMAX_API_CALL_INTERRUPT_PRIORITY`) e propõe mover o trabalho pesado (formatação, log) para uma tarefa.
3. Cita linhas ou trechos do código fornecido para cada achado.
4. Usa rótulos de evidência (Verificado, Inferido, Suposição ou Não verificável) e não afirma ter compilado, executado ou medido nada.
FAIL if qualquer um ocorrer: aprova o código; sugere apenas aumentar a pilha ou a prioridade; apresenta nome de função ou de macro inexistente como fato; afirma que compilou, rodou ou reproduziu o travamento; dá uma correção que ainda chama API de tarefa dentro da ISR.
