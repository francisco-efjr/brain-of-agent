# Orçamentos de pilha, memória e energia - <produto / versão do firmware>

Alvo: <MCU + revisão> · Firmware: <commit / versão> · Data: <...>. Cada número tem método de medição e rótulo: Verificado (medido, com instrumento/comando e data), Inferido (estimativa do compilador ou cálculo) ou Suposição. Margem declarada é decisão do projeto.

## 1. Pilha por contexto

| Contexto (tarefa / thread / ISR) | Estimativa estática (`-fstack-usage`, caminho mais profundo, qualificadores) | Medição em runtime (high-water, carga usada) | Tamanho configurado | Margem | Rótulo |
| --- | --- | --- | --- | --- | --- |

Notas: `dynamic` sem `bounded` é piso, não teto. Medição: `uxTaskGetStackHighWaterMark()` (FreeRTOS) ou `k_thread_stack_space_get()` com `CONFIG_INIT_STACKS` e `CONFIG_THREAD_STACK_INFO` (Zephyr). Meça no pior caso (rede, log, TLS).

## 2. Flash e RAM (do `.map`)

| Região | Tamanho disponível | Usado | Maiores símbolos / seções | Margem | Comando de origem |
| --- | --- | --- | --- | --- | --- |
| Flash | | | | | `size -A` / `nm --size-sort -S` / saída do build |
| RAM (.data + .bss + heap/pilhas) | | | | | |

## 3. Energia (medida na própria placa, com o firmware real)

| Estado (ativo / modem sleep / light sleep / deep sleep) | Corrente média | Instrumento e método | Condições (rádio, temperatura, tensão) | Tempo de wake-up | Data / firmware |
| --- | --- | --- | --- | --- | --- |

A documentação do ESP-IDF não traz valores de corrente: nenhum número entra sem medição. Antes de medir deep sleep: rádio parado, pinos isolados, wake-up configurado.

## 4. Latência / temporização

| Caminho crítico | Meta | Medido (método) | Rótulo |
| --- | --- | --- | --- |

## 5. Decisões e pendências

<itens acima da meta, ações, o que depende de bancada>
