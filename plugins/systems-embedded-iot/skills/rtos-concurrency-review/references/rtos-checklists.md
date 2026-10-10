# Listas de verificação: FreeRTOS, Zephyr e bare metal

Uso: consulta da skill `rtos-concurrency-review`. Fontes: V-52 (FreeRTOS Kernel Book, capítulos 7, 12 e 13, CC BY-SA 4.0, apenas destilado aqui; `semphr.h` e `stack_macros.h` do kernel, MIT), V-15, V-49, V-50, V-51 (documentação do Zephyr), V-12, V-14. Lidas em 2026-10-10. Itens sem fonte lida vêm marcados Inferido (conhecimento estável do domínio) ou Não verificável; confira na versão instalada. As páginas `freertos.org` não puderam ser lidas (conteúdo renderizado no cliente), então nenhuma regra aqui se apoia nelas.

Sumário: [FreeRTOS](#freertos) · [FreeRTOS no ESP-IDF](#freertos-no-esp-idf) · [Zephyr](#zephyr) · [Bare metal](#bare-metal) · [Como relatar o que não dá para provar](#como-relatar-o-que-não-dá-para-provar)

## FreeRTOS

| # | Verificação | Motivo | Rótulo |
| --- | --- | --- | --- |
| R-01 | Dentro de ISR só funções `...FromISR`. | Variantes normais podem bloquear e usam seção crítica de tarefa. | Verificado (V-52, 7.2) |
| R-02 | `BaseType_t woken = pdFALSE;` no início da ISR, `&woken` em cada chamada `FromISR`, e `portYIELD_FROM_ISR(woken)` (ou `portEND_SWITCHING_ISR`) no fim. | O flag diz que uma tarefa de prioridade maior foi acordada; sem o yield ela espera o próximo tick. A macro é específica da porta e algumas só aceitam o uso no fim da ISR. | Verificado (V-15, V-52) |
| R-03 | Prioridade da ISR que chama API está dentro do limite `configMAX_SYSCALL_INTERRUPT_PRIORITY` (nome novo `configMAX_API_CALL_INTERRUPT_PRIORITY`); no Cortex-M valor numérico baixo é prioridade lógica alta; limite não pode ser 0; bits de prioridade alinhados à esquerda. | Acima do limite a ISR não pode chamar função do kernel; é a fonte mais comum de pedidos de suporte e `configASSERT()` costuma detectar. | Verificado (V-52, 7.8.1 e 13.2) |
| R-04 | No Cortex-M com STM32 HAL, o agrupamento de prioridades do NVIC usa todos os bits como preempção (sem sub-prioridade) quando o RTOS exige. Confira `NVIC_SetPriorityGrouping`/`HAL_NVIC_SetPriorityGrouping` e a doc da porta. | Sub-prioridades confundem a comparação com o limite de API. | Inferido |
| R-05 | `configASSERT()` definido em `FreeRTOSConfig.h` nas builds de desenvolvimento e de teste; política de produção escrita (registrar e reiniciar, por exemplo). | Custa tamanho e velocidade (12.2) e pega erro de prioridade e uso inválido da API. | Verificado (V-52) |
| R-06 | `configCHECK_FOR_STACK_OVERFLOW` ligado (1 ou 2); `vApplicationStackOverflowHook` só registra e para. | Métodos 1 e 2 não garantem detecção; o hook roda em contexto de interrupção; não há forma confiável de recuperar; portes com MPU pulam a checagem. | Verificado (V-52) |
| R-07 | `uxTaskGetStackHighWaterMark()` registrado por tarefa em build de teste, sob carga de pior caso. Unidade em palavras no kernel original (no ESP-IDF, bytes). | É a menor folga desde o início da tarefa. | Verificado (função); unidade Inferido |
| R-08 | Mutex para exclusão mútua entre tarefas; semáforo binário/notificação para sinalização ISR para tarefa. Mutex não é para ISR. | Mutex tem herança de prioridade; semáforo não. | Inferido |
| R-09 | Ordem de aquisição de mutex documentada e única; nunca esperar semáforo de sinalização segurando mutex. | Deadlock por ordem inversa. | Inferido |
| R-10 | Periódico com `xTaskDelayUntil` (ou `vTaskDelayUntil`), não `vTaskDelay` em laço. | `vTaskDelay` acumula o tempo do corpo e desliza o período. | Inferido |
| R-11 | Tarefa de prioridade alta não faz polling sem bloquear; toda tarefa tem ponto de bloqueio (fila, notificação, atraso). | Esfomeia tarefas de prioridade menor e o idle (que libera memória de tarefas apagadas). | Inferido |
| R-12 | Falha de `pvPortMalloc` tratada; `configUSE_MALLOC_FAILED_HOOK` avaliado; alocação fora de ISR e, em perfil sem heap, apenas na inicialização. | Heap esgotado em campo é falha silenciosa sem o hook. | Inferido |
| R-13 | Seção crítica de ISR usa a variante `taskENTER_CRITICAL_FROM_ISR` / `taskEXIT_CRITICAL_FROM_ISR` com o estado salvo. | A variante de tarefa não serve em ISR. | Inferido |

Padrão recomendado de processamento diferido: ISR lê o mínimo do periférico, enfileira ou notifica (`FromISR`), pede yield; tarefa "handler" bloqueia na fila/notificação e processa. Contabilize overrun: o retorno de `xQueueSendFromISR` diferente de `pdPASS` incrementa um contador que a tarefa reporta.

### Perguntas ao revisar prioridades de tarefas

1. Qual é o prazo (deadline) de cada tarefa e quem o mede?
2. Há dado ou periférico compartilhado entre tarefas de prioridades diferentes? Qual mecanismo?
3. Alguma tarefa de baixa prioridade segura um mutex de que uma de alta prioridade precisa? Há herança de prioridade?
4. O que acontece se a fila entre ISR e tarefa encher: descarta, bloqueia (proibido em ISR) ou conta?

## FreeRTOS no ESP-IDF

Inferido (conhecimento estável do ESP-IDF, não relido nesta rodada; confira a página do SoC e da versão):
- Seção crítica recebe um spinlock (`portMUX_TYPE`), por causa do modo SMP em chips de dois núcleos: `portENTER_CRITICAL(&mux)` em tarefa, `portENTER_CRITICAL_ISR(&mux)` em ISR. Seção crítica que desliga interrupções em um núcleo não protege o outro (V-12, regra geral).
- ISR registrada com `ESP_INTR_FLAG_IRAM` e o código que ela chama devem estar em IRAM (`IRAM_ATTR`), porque o cache de flash pode estar desabilitado durante escrita em flash (V-32 confirma a regra de IRAM para callbacks de SPI; a generalização é Inferido).
- Tamanho de pilha de tarefa em `xTaskCreate` é em bytes no ESP-IDF; no kernel original é em palavras.
- Mínimos de pilha como "2048/4096 bytes" vêm do autor de um workbench, não do ESP-IDF (V-25): não use como regra, meça.

## Zephyr

| # | Verificação | Motivo | Rótulo |
| --- | --- | --- | --- |
| Z-01 | Prioridade numérica menor tem precedência; cooperativas de `-CONFIG_NUM_COOP_PRIORITIES` a -1; preemptivas de 0 a `CONFIG_NUM_PREEMPT_PRIORITIES - 1`; meta-IRQ com `CONFIG_NUM_METAIRQ_PRIORITIES` no topo do espaço cooperativo. Cada prioridade tem justificativa escrita. | Thread cooperativa só cede voluntariamente; erro de faixa quebra a preempção esperada. | Verificado (V-49) |
| Z-02 | Pilha por thread com `K_THREAD_STACK_DEFINE`; uso medido com `k_thread_stack_space_get()` (exige `CONFIG_INIT_STACKS` e `CONFIG_THREAD_STACK_INFO`) em build de teste; limiar de alerta com `CONFIG_THREAD_RUNTIME_STACK_SAFETY`. | Estimativa estática é piso. | Verificado (V-49) |
| Z-03 | Padrões e faixas de prioridade conferidos no Kconfig da versão (a página de threads não traz os padrões). | Valores mudam entre versões. | Verificado (V-49: ausência na página) |
| Z-04 | ISR conectada com `IRQ_CONNECT` seguida de `irq_enable()`; código novo prefere `k_irq_enable()`/`k_irq_lock()`; `irq_connect_dynamic()` exige `CONFIG_DYNAMIC_INTERRUPTS`. | Nomes sem prefixo `k_` são "legacy" na página. | Verificado (V-50) |
| Z-05 | Dentro de ISR (ou com IRQ travado) só funções marcadas `isr-ok` na referência da versão. Lista não lida nesta rodada: `k_sem_give`, `k_msgq_put` com `K_NO_WAIT` e `k_work_submit` em ISR são Não verificável aqui; confira a marca na referência. | O contrato é por função e por versão. | Não verificável |
| Z-06 | Trabalho demorado vai para `k_work` ou thread; handler de work não bloqueia sem caminho de saída; `k_work_cancel()` é seguro em ISR; `k_work_schedule()`/`k_work_reschedule()` podem ser chamados de ISR; `k_work_flush()`, `k_work_cancel_sync()` e `k_work_queue_drain()` só em thread; checar o retorno e não "otimizar" com `k_work_is_pending()`. Item reenfileirado enquanto pendente executa uma vez. | A fila do sistema tem prioridade cooperativa mais baixa por padrão; handler bloqueante atrasa os demais itens. | Verificado (V-50) |
| Z-07 | ISR direta e zero-latency só com justificativa e medição de latência; dependem de `CONFIG_ARCH_HAS_DIRECT_INTERRUPTS` (o build falha onde não há suporte); zero-latency exige `CONFIG_ZERO_LATENCY_IRQS` e `IRQ_ZERO_LATENCY` e proíbe `ISR_DIRECT_PM`. | Zero-latency escapa do kernel: não pode chamar API do kernel. | Verificado (V-50); a última frase é Inferido |
| Z-08 | Após alterar `prj.conf`, abrir o `.config` final e conferir o símbolo: símbolo com dependência não satisfeita é ignorado sem erro. Pino e barramento fixos ficam no devicetree, não no Kconfig. | Configuração "aplicada" que não foi aplicada é a causa de muitos bugs de pilha e de sincronização. | Verificado (V-51: dicas de Kconfig) e Inferido (consequência) |
| Z-09 | `k_mutex` para exclusão entre threads (não em ISR); `k_sem`/`k_msgq`/`k_fifo` para sinalização. | Mesma lógica do FreeRTOS. | Inferido |
| Z-10 | `CONFIG_HW_STACK_PROTECTION` e `CONFIG_STACK_SENTINEL` avaliados em builds de teste. | Detectam estouro de pilha antes de corrupção silenciosa. | Inferido |

Observação de plataforma: o ciclo `west build`/`west flash` reconstrói por padrão; `west flash`, `west debug` e `--erase` gravam o dispositivo e exigem o gate de `hw-bench-loop` (V-51).

## Bare metal

1. **Super-loop mais ISR**: toda variável escrita na ISR e lida no laço principal é listada na tabela de dados compartilhados. Flag de um bit escrita só pela ISR e limpa só pelo laço pode ser aceitável; contador incrementado nos dois lados não é.
2. **Seção crítica por salvar e restaurar** o estado de máscara de interrupção (CMSIS: `__get_PRIMASK()` antes de `__disable_irq()` e restauração depois), nunca "habilitar incondicionalmente" ao sair; assim a seção é aninhável. Inferido.
3. **Leitura de dado multi-palavra** (por exemplo, `uint64_t` ou struct de timestamp) fora de seção crítica pode rasgar (torn read) em arquitetura de 32 bits. Use seção crítica, versão/sequence lock ou snapshot atômico.
4. **Cortex-M0/M0+**: só load/store atômicos; sem compare-and-swap; incremento atômico exige desabilitar interrupção (V-12). **M3 ou superior**: compare-and-swap disponível. `Relaxed` basta em núcleo único (V-12, texto Rust, vale como princípio).
5. **Inicialização**: inicialize o dado compartilhado antes de habilitar a interrupção que o toca (V-12).
6. **Pilha de ISR**: em bare metal a ISR usa a pilha principal; some o quadro de exceção por nível de aninhamento (Inferido).
7. **Prioridade de ISR**: documente a tabela de prioridades de NVIC e o motivo; ISR de alta prioridade que demora mais que a janela da ISR de baixa causa perda de evento.

## Como relatar o que não dá para provar

- Contexto de execução não visível no trecho (ISR registrada em outro arquivo): peça o arquivo ou rotule "Não verificável".
- Prioridade, pilha e latência: sem medição são Suposição; descreva o experimento (qual carga, qual pino de depuração para medir latência com osciloscópio ou analisador lógico, qual saída) e deixe a execução para o gate.
- Reproduzir condição de corrida: raramente é possível em teste; descreva o entrelaçamento exato em passos (ISR dispara entre a linha A e B) como "cenário", rotulado Inferido, e ofereça o teste de host que o simula com a interrupção chamada manualmente.
