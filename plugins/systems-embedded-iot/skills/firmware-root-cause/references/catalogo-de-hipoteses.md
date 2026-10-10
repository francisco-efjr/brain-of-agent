# Catálogo de hipóteses por sintoma e motivo de reset por plataforma

Uso: consulta da skill `firmware-root-cause`, passo 3. Sintoma para hipóteses plausíveis, com a **observação que as distingue**. Fontes com leitura direta: V-22 (método), V-52 (FreeRTOS: pilha, `configASSERT`, hooks), V-49 e V-50 (Zephyr), V-12 (corrida com interrupção), V-30 e V-31 (barramentos), V-39 (energia), V-28 (princípios de campo). O restante é conhecimento estável do domínio, marcado Inferido; confirme na documentação da versão instalada. Lidas em 2026-10-10.

Sumário: [Como usar](#como-usar) · [Catálogo](#catálogo) · [Motivo de reset por plataforma](#motivo-de-reset-por-plataforma) · [Observar sem perturbar](#observar-sem-perturbar)

## Como usar

1. Escolha a linha pelo sintoma; leve no máximo três hipóteses para o relatório (a skill para depois da terceira falha).
2. Para cada hipótese, a coluna "distingue" é o experimento mais barato que a confirma ou refuta.
3. Dado ausente: peça a instrumentação da coluna "dado necessário" em vez de supor.
4. Toda linha é ponto de partida: o relatório só diz "confirmada" com evidência colada.

## Catálogo

| Sintoma | Hipótese | Distingue (observação) | Dado necessário | Rótulo |
| --- | --- | --- | --- | --- |
| HardFault depois de horas | Estouro de pilha de uma tarefa | marca d'água de pilha próxima de zero; falha ao empilhar (STKERR/MSTKERR) ou SP fora da região da tarefa | `uxTaskGetStackHighWaterMark` / `k_thread_stack_space_get`, registradores de falha | Verificado (métodos de medição, V-52, V-49); associação a falha Inferido |
| HardFault depois de horas | Ponteiro nulo ou inválido num caminho raro | endereço de falha perto de zero; PC dentro da função que usa o ponteiro | endereço de falha e PC mapeados com `addr2line` | Inferido |
| HardFault depois de horas | Heap esgotado ou fragmentado, `malloc` devolveu NULL | falha de alocação registrada; hook de falha de `malloc` do FreeRTOS acionado | contador de falhas de alocação, tamanho do heap livre mínimo | Inferido |
| HardFault depois de horas | Corrupção por DMA ou ISR (buffer na pilha, escrita fora do limite) | variável vizinha muda sem escrita da tarefa; dono do buffer DMA é pilha local | mapa de memória (`.map`), endereços das variáveis, código de DMA | Inferido (V-16 trata dono do DMA) |
| Reinicia sozinho | Watchdog de tarefa ou de interrupção | motivo de reset indica watchdog; uma tarefa bloqueada ou laço sem ponto de bloqueio | motivo de reset; qual tarefa deixou de alimentar | Verificado (ESP-IDF tem códigos separados para watchdog de tarefa e de interrupção: Inferido, conferir) |
| Reinicia sozinho | Brownout (queda de tensão na transmissão de rádio ou ligação de carga) | motivo de reset de brownout; ocorre junto de picos de corrente | motivo de reset; forma de onda da alimentação com osciloscópio | Inferido |
| Reinicia sozinho | `configASSERT`/`assert` disparou e reiniciou | linha do assert no log; reset por software ou pânico | log do pânico | Verificado (V-52 sobre `configASSERT`) |
| Trava sem reiniciar | Deadlock de mutex (ordem de aquisição invertida) | duas tarefas bloqueadas, cada uma segurando o mutex da outra | lista de tarefas e estados no momento do travamento | Inferido |
| Trava sem reiniciar | Espera infinita em barramento ou rede | tarefa bloqueada em `i2c`/`spi`/`recv` com timeout infinito | pilha de chamadas da tarefa; grep de esperas infinitas (V-30) | Verificado (regra), Inferido (causa) |
| Trava sem reiniciar | Tempestade de interrupções (fonte não limpa) | CPU quase 100% em ISR; as tarefas não rodam | contador de entradas da ISR; flag de pendência | Inferido |
| Trava sem reiniciar | Inversão de prioridade | tarefa de alta prioridade bloqueada atrás de uma de baixa prioridade que segura recurso, com uma de média prioridade rodando | prioridades e quem segura o recurso | Inferido |
| Funciona no host, falha no alvo | Largura de inteiro, alinhamento ou endianness | resultado difere com o mesmo estímulo; acesso desalinhado | tipos nos pontos de divergência; teste de host com `-m32` ou com tipos de largura fixa | Inferido |
| Funciona no host, falha no alvo | Memória não inicializada (pilha, heap) | comportamento muda entre execuções; sanitizer de host acusa uso de valor não inicializado | AddressSanitizer/UBSan no host; `-Wuninitialized` | Verificado (opções GCC, V-59) |
| Funciona no host, falha no alvo | Temporização (host é mais rápido e sem preempção) | falha some com atraso adicionado; depende de carga | medição de tempo com pino de depuração | Inferido |
| Funciona em debug, falha em release | Comportamento indefinido exposto por otimização; falta de `volatile` em registrador | muda com `-O0` contra `-Os`; sanitizer acusa | compilar o mesmo código em -O0 e -Os no host com UBSan | Inferido |
| Falha só com Wi-Fi/BLE ativo | Pico de corrente, tarefa do rádio com prioridade alta, ISR em flash com cache desligado | falha correlaciona com transmissão; ISR fora de IRAM durante escrita em flash | tempo de falha vs. atividade de rádio; localização do código da ISR | Inferido (IRAM: V-32 para callbacks de SPI) |
| Corrupção de fila ou de pacote | Corrida entre ISR e tarefa | contagem de elementos inconsistente; contador RMW perde atualização | tabela de dados compartilhados (`rtos-concurrency-review`) | Verificado (V-12) |
| Falha após OTA | Imagem nova não confirmada, rollback ou partição incorreta | estado da imagem (pendente de verificação) e motivo de reversão | log do bootloader; tabela de partições | Verificado (estados do ESP-IDF, V-46) |
| Falha após deep sleep | Estado perdido (RAM desligada), pinos não isolados, wake-up mal configurado | motivo de reset de deep sleep; dado não preservado | motivo de reset e dados em memória RTC | Verificado (V-39) |

## Motivo de reset por plataforma

Registre o motivo no boot, em todo build. Os nomes abaixo são Inferido (conhecimento estável, não relido nesta rodada): confirme na versão instalada.

| Plataforma | Como obter | Observação |
| --- | --- | --- |
| ESP-IDF | `esp_reset_reason()` devolve um `esp_reset_reason_t` com motivos como power-on, software, pânico, watchdog de tarefa, watchdog de interrupção, outros watchdogs, deep sleep e brownout | O monitor decodifica o backtrace de pânico com o ELF do build; core dump em flash e comandos `idf.py coredump-info`/`coredump-debug` existem (Inferido; confirme a versão) |
| Zephyr | `hwinfo_get_reset_cause()` (exige `CONFIG_HWINFO` e suporte do SoC) devolve máscara de causas; o log de erro fatal mostra registradores | Coredump via `CONFIG_DEBUG_COREDUMP` (Inferido); `k_sys_fatal_error_handler` permite política própria |
| STM32 | Flags de reset no registrador de controle e status do RCC (nomes e macros variam por família, por exemplo `__HAL_RCC_GET_FLAG(RCC_FLAG_IWDGRST)`); limpar depois de ler | Confirme macros e bits no reference manual e no HAL da família |
| FreeRTOS genérico | `vApplicationStackOverflowHook`, hook de falha de `malloc` (`configUSE_MALLOC_FAILED_HOOK`), `configASSERT` | Hook de overflow roda em contexto de interrupção: registrar e parar (V-52) |
| Outro MCU | Registrador de causa de reset do fabricante | Pergunte o part number; sem manual, Não verificável |

## Observar sem perturbar

- Abrir monitor serial pode resetar o alvo (DTR/RTS em placas USB-serial; Inferido). Opções para evitar reset existem em algumas ferramentas; confirme `--help` da versão. Se o reset for aceitável, avise o usuário antes: ele pode apagar o estado que se queria observar.
- `printf` e log síncrono mudam tempo e uso de pilha; um bug de corrida pode desaparecer com log. Prefira contadores, buffers circulares em RAM e pino de depuração.
- Ler registrador de periférico pode limpar flag ou esvaziar FIFO (Inferido); em falha, leia só o bloco de controle do sistema, RAM e pilha.
- Parar o núcleo com depurador pode disparar watchdog e deixar saídas/atuadores em último estado; combine com o usuário antes (veja [depuracao-com-probe.md](depuracao-com-probe.md)).
