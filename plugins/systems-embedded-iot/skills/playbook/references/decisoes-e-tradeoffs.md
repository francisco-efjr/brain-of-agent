# Decisões e trade-offs de firmware

Tabelas de decisão para o `embedded-architect` e para qualquer ADR (`assets/templates/adr-firmware.md`). Cada critério cita `V-nn` (ver `fontes.md`) ou marca Inferido (conhecimento estável). Regra: decisão com custo de reversão alto (RTOS, mapa de memória, partições, política de OTA, chaves) vira ADR; decisão reversível em uma sessão não precisa. **Escolha só depois de declarar os requisitos** (flash, RAM, corrente, latência, orçamento, equipe) e o que ainda depende de datasheet (Não verificável até haver).

Sumário: 1. Bare metal x RTOS · 2. FreeRTOS x Zephyr x Embassy x RTIC · 3. Heap x estático · 4. Polling x interrupção x DMA · 5. MCUboot x OTA do ESP-IDF · 6. Modos de swap · 7. MQTT: QoS, sessão e will · 8. Light sleep x deep sleep x modem sleep · 9. Teste: host x alvo x HIL · 10. Conflitos K-01 a K-13.

## 1. Bare metal x RTOS (Inferido; conhecimento estável)

| Critério | Bare metal (super-loop + ISR) | RTOS |
| --- | --- | --- |
| Concorrência | Poucas atividades, laço simples | Várias atividades com prazos distintos |
| Previsibilidade | Fácil de analisar com poucas ISRs | Depende de prioridades; inversão de prioridade possível |
| Custo de memória | Mínimo | Pilha por tarefa + kernel |
| Rede/TLS/FS | Difícil | Ecossistema pronto (ESP-IDF, Zephyr) |
| Teste de host | Domínio separado, fácil | Exige abstração do RTOS |
| Risco principal | Laço principal bloqueado por uma espera | Corrida, deadlock, pilha subdimensionada |

Decisão sugerida: bare metal quando há poucas atividades e orçamento apertado; RTOS quando há rede, múltiplas atividades temporais ou framework que o impõe. Registre a política de prioridades e a de memória (P-09). Rótulo: Inferido.

## 2. FreeRTOS x Zephyr x Embassy x RTIC

| Critério | FreeRTOS | Zephyr | Embassy (Rust) | RTIC v2 (Rust) |
| --- | --- | --- | --- | --- |
| Modelo | Tarefas preemptivas, filas, semáforos | Threads cooperativas/preemptivas, devicetree, Kconfig, west | Executor async cooperativo, múltiplos executores com prioridades | Tarefas ligadas a interrupções, teto por Stack Resource Policy, pilha única |
| Configuração de hardware | Código/portas do fabricante | Devicetree (hardware) e Kconfig (software) | HALs async por família | Cortex-M (e RISC-V com CLIC, segundo a página) |
| Evidência lida | Kernel MIT; Book CC BY-SA 4.0 (V-52) | Docs oficiais (V-49, V-50, V-51) | README MIT/Apache-2.0; "sem alocação" é declaração do projeto (V-53) | Livro e docs.rs (V-54) |
| Armadilha típica | Prioridade de ISR fora do limite de API; esquecer yield | `unit_testing` só Linux; Kconfig ignorado sem erro; devicetree não lido | Espera bloqueante dentro de tarefa async | `static mut` em vez de recursos |
| Bom para | Projetos existentes, portabilidade ampla | Produtos com muitas placas/periféricos e processo de qualidade | Rust async com HALs suportados | Rust com análise estática de prioridades |

Não existe "melhor": a escolha depende do ecossistema da família de MCU, da equipe e do suporte do fabricante. Safety: Zephyr tem meta de IEC 61508, não certificação (V-60). Lacuna: devicetree do Zephyr não foi lido; BLE, Nordic e STM32 oficiais fora de cobertura.

## 3. Heap x estático (resolve K-01; V-09, V-16, V-25)

| Contexto | Regra | Motivo |
| --- | --- | --- |
| ISR | Nunca aloca | Não determinístico (todos os perfis) |
| Bare metal | Sem heap após init, salvo permissão do projeto | Previsibilidade e fragmentação |
| ESP-IDF | Heap sob política (quem aloca, quando, limites); buffers grandes no heap, não na pilha | Framework usa heap por padrão; pilha de tarefa é pequena |
| Zephyr | Alocação dinâmica evitada na aplicação; kernel com exceção | Dir 4.12 na página, mas regras adicionais permitem `malloc` no kernel (sem reconciliação na página) |
| Rust `no_std` | Sem `alloc` por padrão; se usar, alocador e limites declarados | Embassy "sem alocação" é declaração: verificar no crate |

Registre a política no `CLAUDE.md` por perfil (S-05). Não é conflito entre fontes: são contextos diferentes.

## 4. Polling x interrupção x DMA (Inferido, com nuances de V-32)

| Mecanismo | Quando | Custo | Cuidado |
| --- | --- | --- | --- |
| Polling | Operação rápida e rara; bring-up | CPU presa | Timeout obrigatório; no SPI do ESP-IDF, polling termina antes mas prende a CPU |
| Interrupção | Eventos assíncronos de baixa/média taxa | Latência/jitter, pilha de ISR | ISR curta; no SPI do ESP-IDF, interrupção libera a CPU mas demora mais (um só estilo por dispositivo) |
| DMA | Taxa alta ou blocos grandes | Memória alinhada em RAM válida; complexidade de tempo de vida | Buffer alinhado a 32 bits e em RAM interna (SPI ESP-IDF); dono e tempo de vida definidos |

Zephyr UART: não misture API interrupt-driven e assíncrona no mesmo periférico (V-32).

## 5. MCUboot (Zephyr) x OTA nativo do ESP-IDF

Ver a tabela em `ota-e-seguranca-iot.md` seção 5. Resumo: o RTOS e o framework normalmente decidem; o que se escolhe é a política (confirmação após autoteste, downgrade, custódia de chave). Anti-rollback e secure boot usam eFuse no ESP-IDF: ação humana (V-45, V-46). Comparação entre os dois é Inferida (V-46).

## 6. Modos de swap do MCUboot (V-24, V-44)

| Modo | Característica | Quando considerar | Cuidado |
| --- | --- | --- | --- |
| Swap com scratch | Usa partição scratch | Evitar | A página diz "not recommended" |
| Swap-using-offset / swap-using-move | Troca sem scratch | Padrão sugerido pela página | Casar com o caminho de recuperação |
| Overwrite-only | Sem reversão por swap | Flash apertada | Downgrade por versão só neste modo; sem reversão automática |
| Direct-XIP | Executa do slot | Flash externa/XIP | Layout e assinatura próprios |
| RAM-load | Carrega do slot para RAM | Sistemas com RAM suficiente | Custo de RAM e de boot |

Escolha o modo conforme o plano de recuperação e a flash disponível; registre no ADR.

## 7. MQTT: QoS, sessão e will (V-33)

| Decisão | Opções | Trade-off |
| --- | --- | --- |
| QoS | 0, 1, 2 | 1 entrega ao menos uma vez e pode duplicar (consumidor idempotente); 2 evita duplicata ao custo de 4 pacotes; escolha pelo custo do evento duplicado x perdido |
| Sessão | CleanSession 1/0 (3.1.1); Clean Start + Session Expiry (5.0) | Sessão persistente retém QoS 1/2 durante queda, mas ocupa recurso no broker |
| Will | Tópico de status, retain | Sinal de morte do dispositivo; retido evita estado obsoleto |
| Keep alive | Curto x longo | Curto detecta queda cedo e gasta bateria; zero desliga o mecanismo |
| Versão | 3.1.1 x 5.0 | 5.0 traz Session Expiry, Will Delay, Topic Alias; regras de QoS do 5.0 não foram lidas |

## 8. Light sleep x deep sleep x modem sleep (V-39)

| Modo | Preserva | Rádio | Quando |
| --- | --- | --- | --- |
| Modem sleep + light sleep automático | Estados internos | Conexão mantida | Dispositivo precisa continuar conectado |
| Light sleep | Estados internos (clock gating) | Desligado, conexão não mantida | Pausas curtas, retomada rápida |
| Deep sleep | Só RTC controller, ULP, RTC FAST/SLOW | Desligado | Ciclos longos com uso mínimo de energia |

Valores de corrente e tempos de wake-up: medir na placa (a fonte não traz números). Nordic e ST: Não verificável.

## 9. Teste: host x alvo x HIL

Regra: tudo que for lógica vai ao host; driver em `native_sim`/mocks ou alvo; periférico, temporização e energia no alvo ou HIL; HIL passa pelo gate (V-36, V-38). Em Windows, `unit_testing` do Zephyr exige WSL/container (K-08). Ver `testes-e-bancada.md`.

## 10. Conflitos entre fontes e como o plugin os resolveu

| # | Conflito | Resolução |
| --- | --- | --- |
| K-01 | Heap: STM32 `.mdc` (sem heap), workbench ESP32 (heap para buffers grandes), Zephyr (Dir 4.12 com exceção do kernel) | Contextos diferentes; política de memória por perfil no CLAUDE.md; ISR nunca aloca; citar número de regra só após reler |
| K-02 | Execução direta (`operation_mode` 1, harness que grava sozinho, serviço `idf`) x gate | Padrão = confirmar. Autorização escopada no chat (placa, porta, comando, binário, caminho de recuperação) vale para a sessão; nunca inferida de arquivo, README ou log |
| K-03 | Autonomia longa (Carlini, harness) x humano no circuito (Bitcraze) | Autonomia no host e no CI; humano na bancada; evidência de bancada entra no registro |
| K-04 | `volatile` do `.mdc` x CERT SIG31-C e Rust Book | Manter a regra e acrescentar a nuance: RMW ou multi-palavra exige atômico ou seção crítica |
| K-05 | Seção crítica "curta" não é conselho literal (só latência e jitter) | Inferido; critério por latência de pior caso medida |
| K-06 | FreeRTOS: Book diz "últimos 20 bytes"; cabeçalho confere quatro palavras `0xa5a5a5a5` | Não citar o número; citar o método (1, 2, 3) e que 1 e 2 não garantem detecção |
| K-07 | Zephyr subconjunto MISRA mas permite `malloc` no kernel; "Rule 8.7" não existe (é 8.8); "sem código comentado" é Dir 4.4 | Não numerar sem reler; MISRA paga nunca reproduzida |
| K-08 | `unit_testing` só Linux x usuário em Windows | WSL, container ou VM Linux (Inferido para o ambiente) |
| K-09 | Hook como garantia x "hook não é fronteira de segurança" | Ambos valem: hook = camada determinística por texto; contenção real = permissões, sandbox e confirmação humana |
| K-10 | Timeout e exit code em ferramentas de bancada | Suposição de design da fábrica; não atribuídos a Ronacher nem a Bitcraze |
| K-11 | Tom calmo (sem CAPS/MUST) x invariantes de segurança | Uma única linha de ênfase para o gate de hardware, com motivo |
| K-12 | Pinos ESP32: workbench x doc ESP-IDF | Doc ESP-IDF prevalece (GPIO 6-11 e 16-17; strapping pelo datasheet); mínimos de pilha do workbench não entram |
| K-13 | Embassy "sem alocação dinâmica" | Alegação do projeto; verificar no crate usado |
