---
name: isr-freertos-review
description: "Mede o disparo de rtos-concurrency-review e a qualidade técnica da revisão de uma ISR de UART com FreeRTOS que usa API de tarefa, aloca, loga e incrementa contador compartilhado."
tags: [systems-embedded-iot, rtos, isr, freertos]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta pelo menos três problemas reais (xQueueSend com portMAX_DELAY na ISR em vez de FromISR, falta do flag de tarefa acordada repassado ao yield, alocação e snprintf e log na ISR, rxCount++ como leitura-modificação-escrita sem proteção com volatile não dando atomicidade), cita a linha do trecho, recomenda conferir a prioridade da ISR contra o limite de API da porta, propõe mover o trabalho para uma tarefa, usa rótulos Verificado ou Inferido e não afirma ter compilado nem executado."
model: sonnet
---
Pode revisar esta ISR de UART num STM32 com FreeRTOS? Estou com travamentos esporádicos.

```c
QueueHandle_t rxQueue;
volatile uint32_t rxCount;

void USART2_IRQHandler(void) {
    if (USART2->ISR & USART_ISR_RXNE) {
        uint8_t b = USART2->RDR;
        xQueueSend(rxQueue, &b, portMAX_DELAY);
        char *msg = pvPortMalloc(32);
        snprintf(msg, 32, "rx %u", rxCount++);
        log_write(msg);
    }
}
```
