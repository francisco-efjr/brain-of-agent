# RTOS, interrupções e recursos (pilha, memória, energia)

Fontes lidas em 2026-10-10: V-15, V-39, V-40, V-49, V-50, V-51, V-52, V-59 (ver `fontes.md`). Onde a regra depende de porta, arquitetura ou versão, o texto diz "conferir na versão instalada". Rótulos: Verificado (lido na fonte), Inferido (conhecimento estável ou análise), Não verificável.

Sumário: 1. Contextos de execução · 2. FreeRTOS · 3. Zephyr · 4. Dado compartilhado · 5. Orçamento de pilha · 6. Energia e sleep · 7. Revisão em 12 perguntas · 8. Gotchas.

## 1. Contextos de execução e o que cada um pode fazer

Revisar firmware começa por inventariar os contextos: ISR, tarefa/thread, timer (callback no daemon ou em ISR), workqueue, event loop do framework. O contexto limita as operações (V-28).

| Operação | ISR | Tarefa / thread | Observação |
| --- | --- | --- | --- |
| Bloquear (semáforo com espera, `vTaskDelay`, `k_sleep`, mutex com espera) | não | sim | Em ISR a espera trava o sistema ou é erro de API (V-15, V-52) |
| Alocar/liberar (`malloc`, `pvPortMalloc`, `k_malloc`) | não | sob política (P-09) | Tempo não determinístico e fragmentação (Inferido) |
| `printf`, log síncrono, I/O de arquivo | não | sim, com custo | Log em ISR: só buffer circular preenchido por ISR e drenado por tarefa |
| API do kernel | só variante de ISR (`...FromISR` no FreeRTOS; funções marcadas isr-ok no Zephyr) | normal | Lista isr-ok do Zephyr não lida: Não verificável (V-50) |
| Seção crítica | curta e medida | curta | Não protege entre núcleos (V-12) |

Regra de projeto: ISR copia o dado mínimo, limpa a causa da interrupção e sinaliza; a tarefa processa. Prioridade de ISR e de tarefa são espaços diferentes: toda ISR de hardware ganha de toda tarefa.

## 2. FreeRTOS

Fontes: Kernel Book (cap. 7, 12, 13; CC BY-SA 4.0, destilado), `semphr.h` e `stack_macros.h` (MIT) (V-15, V-52). As páginas freertos.org não puderam ser lidas.

1. **Só `...FromISR` dentro de ISR** (`xQueueSendFromISR`, `xSemaphoreGiveFromISR`, `xTaskNotifyFromISR`, `xEventGroupSetBitsFromISR`). A variante normal pode bloquear ou usar seção crítica que não vale em ISR.
2. **Flag de tarefa acordada.** `BaseType_t xHigherPriorityTaskWoken = pdFALSE;` é passado à API; se acordar tarefa de prioridade maior, vira `pdTRUE`. No fim da ISR, repasse o flag a `portYIELD_FROM_ISR(x)` ou `portEND_SWITCHING_ISR(x)`. A macro é específica da porta e alguns portes só aceitam no fim da ISR (V-52).
3. **Limite de prioridade da API.** `configMAX_SYSCALL_INTERRUPT_PRIORITY` (nome novo: `configMAX_API_CALL_INTERRUPT_PRIORITY`) é a maior prioridade de interrupção que pode chamar a API; acima dele a ISR não pode chamar nenhuma função do FreeRTOS. No Cortex-M, valor numérico baixo é prioridade lógica alta, os bits de prioridade são alinhados à esquerda e o limite não pode ser 0. O Book diz que prioridade de interrupção é a fonte mais comum de pedidos de suporte e que `configASSERT()` costuma detectá-la (V-52). Confira o `FreeRTOSConfig.h` e a doc da porta.
4. **`configASSERT` definido** nas builds de desenvolvimento e de teste, com custo de tamanho e velocidade (V-52).
5. **Pilha.** `uxTaskGetStackHighWaterMark()` devolve a menor folga desde o início da tarefa. `configCHECK_FOR_STACK_OVERFLOW` métodos 1 e 2 **não garantem** detecção; o método 3 existe só em alguns portes; portes com MPU pulam a checagem. O hook de overflow roda em contexto de interrupção e não há como recuperar com segurança: registre e pare (V-52). Não cite o número de bytes da checagem (o Book e o cabeçalho divergem).
6. **Prioridades de tarefa** justificadas por escrito (quem pode preemptar quem, o que acontece com inversão de prioridade: mutex com herança em vez de semáforo binário para exclusão, Inferido).

Exemplo de ISR correta (ilustrativo; nomes de registrador são de uma família STM32 e devem ser conferidos no header da variante):

```c
static volatile uint32_t s_rx_dropped;            /* único escritor: esta ISR */

void USART2_IRQHandler(void)
{
    BaseType_t woken = pdFALSE;
    if (USART2->ISR & USART_ISR_RXNE) {
        uint8_t b = (uint8_t)USART2->RDR;          /* ler limpa a causa */
        if (xQueueSendFromISR(g_rx_queue, &b, &woken) != pdPASS) {
            s_rx_dropped++;                         /* contador lido pela tarefa */
        }
    }
    portYIELD_FROM_ISR(woken);
}
```

Por que assim: a fila é a fronteira ISR para tarefa; não há espera, alocação nem `printf`; a perda é contada, não silenciosa. Ressalva: `s_rx_dropped++` só é seguro com um único escritor e leitura de 32 bits atômica na arquitetura (Inferido); para vários escritores use atômico (V-12).

## 3. Zephyr

Fontes: V-49 (threads), V-50 (interrupções e workqueue), V-51 (Kconfig e west). Conferir os padrões do Kconfig na versão instalada (a página não traz os valores).

- **Prioridades.** Valor numérico menor tem precedência. Cooperativas vão de `-CONFIG_NUM_COOP_PRIORITIES` a -1; preemptivas de 0 a `CONFIG_NUM_PREEMPT_PRIORITIES - 1`; meta-IRQ via `CONFIG_NUM_METAIRQ_PRIORITIES` na ponta mais alta do espaço cooperativo. Justifique cada prioridade por escrito (V-49).
- **Pilha.** `K_THREAD_STACK_DEFINE`; `k_thread_stack_space_get()` exige `CONFIG_INIT_STACKS` e `CONFIG_THREAD_STACK_INFO`; `CONFIG_THREAD_RUNTIME_STACK_SAFETY` liga limiar por thread com handler. Meça o pior caso em build de teste (V-49).
- **ISR.** `IRQ_CONNECT` seguido de `irq_enable()` (nomes `k_irq_*` preferidos em código novo). `irq_connect_dynamic()` exige `CONFIG_DYNAMIC_INTERRUPTS`. ISR direta e zero-latency dependem de suporte da arquitetura: `CONFIG_ARCH_HAS_DIRECT_INTERRUPTS` (o build falha onde não há), `CONFIG_ZERO_LATENCY_IRQS` e `IRQ_ZERO_LATENCY`, e proíbem `ISR_DIRECT_PM`. A página diz que o zero-latency está implementado no Cortex-M, sem dizer "somente" (V-50). Use ISR direta só com justificativa e latência medida.
- **Trabalho demorado** vai para thread ou work item. Workqueue: item reenfileirado enquanto pendente roda uma vez; a fila do sistema tem prioridade cooperativa a mais baixa por padrão e **um handler que bloqueia atrasa os demais**; `k_work_cancel()` é seguro em ISR; `k_work_schedule()` e `k_work_reschedule()` podem ser chamados de ISR; `k_work_flush()`, `k_work_cancel_sync()` e `k_work_queue_drain()` só em thread; confira o retorno e não "otimize" com `k_work_is_pending()` (V-50).
- **Kconfig.** Use `depends on`; `select` só para símbolos auxiliares sem dependências; `imply` para padrão desabilitável; pino, nome de dispositivo e barramento fixo ficam no **devicetree**, não no Kconfig; atribuição a símbolo sem prompt é ignorada; após mudar `prj.conf`, confira o `.config` final (V-51). `scripts/kconfig/lint.py` acha símbolos inalcançáveis.
- **west.** `west build -b <BOARD>` (`-p` para pristine). **`west flash` e `west debug` gravam/abrem sessão** e reconstroem por padrão; `--erase` apaga a flash antes e a página não traz aviso de perda de dados; `west flash -H` lista runners. Tudo isso é gravação e entra no gate (V-51).

## 4. Dado compartilhado com interrupção

Checklist (V-12, V-14, V-16): cada dado compartilhado tem **dono** e **mecanismo** registrados; protegido por seção crítica, atômico ou fila; inicializado **antes** de habilitar a interrupção; `volatile` só para registrador/flag de ISR e nunca como atomicidade (CERT SIG31-C, analogia ISR x handler de sinal: Inferido); dado multi-palavra (struct, contador de 64 bits em MCU de 32 bits) exige seção crítica; Cortex-M0/M0+ só tem load/store atômicos, M3+ tem CAS (V-12); seção crítica não protege entre núcleos (ESP32 de dois núcleos: use spinlock/mutex do framework, Inferido). Duração "curta" da seção crítica não vem da fonte (só latência e jitter): defina pelo pior caso de latência medido, não por um número fixo (K-05).

| Dado | Escritores | Leitores | Proteção | Inicializado antes de habilitar IRQ? |
| --- | --- | --- | --- | --- |
| `g_rx_queue` | ISR UART | tarefa de protocolo | fila do RTOS | sim, em `app_init()` |
| `s_rx_dropped` | ISR UART | tarefa de telemetria | escritor único, leitura de 32 bits | n/a |

## 5. Orçamento de pilha (procedimento)

Fonte: V-59 (GCC), V-49, V-52. Resultado alimenta `assets/templates/orcamentos.md`.

1. Compile com `-fstack-usage`: cada unidade gera `.su` com função, bytes e qualificadores `static`, `dynamic`, `bounded`.
2. Some o caminho de chamada mais profundo por tarefa/contexto (inclua a pilha própria da ISR, quando houver, e o quadro de contexto salvo na exceção, Inferido). Ferramentas de grafo de chamada (ex.: `cflow`, `-fcallgraph-info`) ajudam; confira na versão do GCC.
3. Trate `dynamic` **sem** `bounded` como **piso**, não teto. Chamada por ponteiro de função, recursão e `alloca`/VLA quebram o cálculo estático; sem recursão, VLA e `alloca` fica auditável (V-09).
4. Confirme em runtime: `uxTaskGetStackHighWaterMark()` (FreeRTOS) ou `k_thread_stack_space_get()` (Zephyr), em build de teste, com o pior caso de carga (rede, log, TLS).
5. Margem declarada no orçamento (ex.: 25%) é decisão do projeto, não regra da fonte (Suposição).
6. Estimativa do compilador não é medição de pior caso: o valor entra como "Inferido"; só a medição vira "Verificado" (V-59).

Estouro de flash/RAM no link (`region 'FLASH' overflowed by N bytes`): gere o mapa (`-Wl,-Map=build/app.map`), liste os maiores símbolos (`nm --size-sort -S` ou `size -A`), procure `printf` com ponto flutuante, bibliotecas inteiras puxadas por um símbolo, tabelas sem `const` indo para RAM, `-Os` ausente, `-ffunction-sections -fdata-sections -Wl,--gc-sections` ausentes (Inferido; conhecimento estável de binutils/GCC, confira os nomes na toolchain).

## 6. Energia e sleep

Fontes: V-39 (ESP-IDF, boa), V-40 (Zephyr PM, índice de 2022: referência). Nordic e ST: Não verificável (lacuna).

- **Light-sleep:** periféricos digitais e CPUs com clock gating e tensão reduzida; estados internos preservados. **Deep-sleep:** CPUs, maior parte da RAM e periféricos digitais desligados; ficam RTC controller, ULP e RTC FAST/SLOW. **O rádio (Wi-Fi/BT) fica desligado nos dois**, e a conexão não é mantida mesmo sem chamar stop/deinit; para manter conexão use modem-sleep com light-sleep automático (V-39).
- Fontes de wake-up no ESP-IDF: timer, touchpad, ext0, ext1, ULP, GPIO, UART (só light-sleep). `rtc_gpio_isolate()` antes de `esp_deep_sleep_start()` evita corrente por pull interno.
- O pulso de wake-up de 3 ciclos do RTC slow clock é detalhe de uma função específica e depende de `CONFIG_RTC_CLK_SRC` (V-39, correção 1): não generalize.
- **Critério de pronto de energia:** tabela ativo/light/deep com corrente **medida na própria placa**, com o firmware real e instrumento adequado (multímetro de precisão ou analisador de consumo), data e versão do firmware. A página do ESP-IDF não traz valores de corrente nem tempos de wake-up: nenhum número entra sem medição. "Medir corrente como critério de pronto" é prática derivada, sem fonte própria (V-40, Inferido).
- Antes do deep-sleep: rádio parado, pinos isolados, dados que sobrevivem em RTC memory marcados, wake-up configurado. Teste o caminho de acordar e o motivo do reset (caso multi-estágio no ESP-IDF, ver `testes-e-bancada.md`).
- Zephyr PM: camadas System PM, Device PM, Device Runtime PM, Power Domain; decida qual camada controla cada periférico e quem precisa de wakeup (V-40). Sem guia de medição na fonte.

## 7. Revisão de ISR e concorrência em 12 perguntas

1. Quais contextos existem e qual é a prioridade de cada um? 2. Há tabela de dados compartilhados com dono e proteção? 3. Só APIs de ISR em ISR? 4. O flag de tarefa acordada chega ao yield? 5. A prioridade da ISR respeita o limite de API da porta? 6. A ISR bloqueia, aloca ou chama `printf`? 7. O trabalho pesado está em tarefa ou work item? 8. A pilha de cada tarefa foi medida (high-water) e há detecção de overflow? 9. `configASSERT`/asserts de dev estão ligados? 10. Dado multi-palavra ou RMW tem atômico ou seção crítica? 11. A inicialização ocorre antes de habilitar a interrupção? 12. Em dois núcleos, a proteção vale entre núcleos? Cada resposta com rótulo e `arquivo:linha`.

## 8. Gotchas

- `k_sem_give` em ISR e a lista isr-ok do Zephyr não foram confirmados (Não verificável).
- Handler de overflow de pilha não recupera; watchdog é último recurso, não correção (V-28).
- `static mut` (Rust) tocado por interrupção é achado; ver `c-cpp-rust-firmware.md`.
- Medir altera o sistema: log em ISR para medir latência perturba o resultado; use pino de GPIO + analisador lógico quando a latência importa (Inferido).
