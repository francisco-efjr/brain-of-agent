# Barramentos e protocolos: I2C, SPI, UART, CAN, MQTT, BLE

Fontes lidas em 2026-10-10: V-30 a V-35, V-61 (ver `fontes.md`). Documentação oficial dos projetos (Zephyr, ESP-IDF) e padrões OASIS; nada foi executado. **Valores elétricos (pull-up, terminação, taxa, tempos) vêm do datasheet do periférico e da medição na placa**; sem datasheet, pare e pergunte. Rótulos: Verificado (lido na fonte), Inferido, Não verificável.

Sumário: 1. Checklist unificado · 2. I2C · 3. SPI e UART · 4. CAN (TWAI) · 5. MQTT · 6. BLE · 7. Teste em bancada de MQTT e BLE · 8. Gotchas.

## 1. Checklist unificado de barramento e rede (V-35)

Responda cada item com Verificado, Inferido ou Não verificável e cite a fonte:

1. Todo erro (timeout, NACK, bus-off, FIFO overflow, desconexão) tem caminho explícito e teste.
2. Timeouts cobrem o pior caso do periférico.
3. Elétrica (pull-up, terminação, transceiver) vem do datasheet e foi medida.
4. Recuperação de bus-off e de barramento travado roda em task, com limite de tentativas e atraso (I2C: Inferido).
5. Callbacks de ISR não bloqueiam.
6. DMA com buffer alinhado e em RAM válida.
7. Acesso concorrente tem dono único ou mutex.
8. Protocolos de rede têm keep alive, will, sessão e reconexão justificados.
9. O caminho de erro é exercitado em teste de host com HAL falsa ou em bancada.

Saída: tabela `achado · item · arquivo:linha · gravidade · como verificar`.

## 2. I2C (V-30)

Zephyr (hardware/peripherals/i2c) e ESP-IDF (api-reference/peripherals/i2c), páginas lidas por inteiro.

| Tema | Regra | Rótulo |
| --- | --- | --- |
| Timeout (Zephyr) | `zephyr,transfer-timeout-ms` por controlador, depois `CONFIG_I2C_TRANSFER_TIMEOUT_MS`, depois `K_FOREVER` se 0 (alguns drivers que gravam o timeout no hardware rejeitam 0 no build); erro `-ETIMEDOUT` | Verificado |
| Timeout (ESP-IDF) | `xfer_timeout_ms` de -1 espera indefinidamente (desaconselhado no probe); erros `ESP_ERR_INVALID_RESPONSE` (NACK), `ESP_ERR_TIMEOUT`, `ESP_ERR_NOT_FOUND` | Verificado |
| Cobertura do timeout | Deve cobrir o ciclo de escrita interno de EEPROM e clock stretching do escravo; valor vem do datasheet | Inferido |
| Pull-up | Externo de 1 kΩ a 10 kΩ (2 kΩ a 5 kΩ preferido, não abaixo de 1 kΩ); interno insuficiente para alta velocidade; SCL de mestre até 400 kHz; dimensionar e **medir** na placa | Verificado (doc ESP-IDF) |
| Callbacks de ISR | Sem bloqueio; APIs `FromISR` | Verificado |
| Thread safety (ESP-IDF) | Criação de barramento e transferências do mestre são thread safe; demais funções exigem mutex | Verificado |
| Modo assíncrono | Experimental (a transação assíncrona do mestre, não o driver todo); só um dispositivo por barramento; a página cita `on_recv_done` no texto e `on_trans_done` na estrutura | Verificado |
| Clock stretching | O controlador do ESP32 não faz stretching como escravo; `scl_wait_us` é espera do mestre (0 usa o padrão de registrador); "cerca de 12 ms" é dito como possível, não como limite | Verificado |
| Recuperação de barramento travado | Nenhuma das páginas trata; pulsar SCL até liberar SDA e emitir STOP é prática conhecida | Inferido |
| Zephyr | API de controller estável e de target experimental; terminologia NXP I2C Rev 7.0 | Verificado |

Exemplo de achado (cópia reduzida do caso de eval E5): `i2c_master_transmit_receive(dev, &reg, 1, buf, 16, -1);` em EEPROM com `enable_internal_pullup = true` a 400 kHz: timeout -1 é a causa provável de congelamento (severidade alta); retorno ignorado (NACK/timeout) (alta); pull-up interno a 400 kHz (média; exige pull-up externo medido); sem mutex se houver mais de uma tarefa (média). Tempos reais: Não verificável sem datasheet da EEPROM.

## 3. SPI e UART (V-32)

**SPI mestre no ESP-IDF** (página lida):

- Buffers em memória interna compatível com DMA e alinhados a 32 bits (comprimento múltiplo de 4); buffer desalinhado força cópia temporária.
- `max_transfer_sz` padrão 4092 com DMA; sem DMA, o tamanho do FIFO (normalmente 64 bytes).
- Transação por polling termina antes e prende a CPU; por interrupção libera a CPU e demora mais; a página recomenda **um só tipo por dispositivo**.
- Thread safe só se cada dispositivo tem uma task; senão, mutex.
- Só o ISR fica em IRAM por padrão; callbacks com `ESP_INTR_FLAG_IRAM` precisam estar em IRAM.
- Limites típicos de clock no ESP32: 80 MHz (IO_MUX) e 26 MHz (GPIO matrix). `cs_ena_pretrans` é incompatível com as fases de comando e endereço em full-duplex.

**UART no ESP-IDF:** buffer RX maior que o FIFO de hardware; `UART_BUFFER_FULL`, `UART_FIFO_OVF`, `UART_FRAME_ERR`, `UART_PARITY_ERR` e `UART_BREAK` chegam como eventos na fila e precisam de política (contar, descartar, sinalizar); não passe `ESP_INTR_FLAG_IRAM` ao instalar o driver; fluxo de controle por hardware (RTS/CTS) ou software (XON 0x11, XOFF 0x13). A página não declara garantia geral de thread safety: use dono único ou mutex.

**UART no Zephyr:** três APIs (polling, interrupt-driven, assíncrona com DMA). Interrupt-driven e assíncrona **não** devem ser usadas ao mesmo tempo no mesmo periférico (`CONFIG_UART_EXCLUSIVE_API_CALLBACKS` ligado por padrão). `uart_poll_out()` bloqueia.

**SPI no Zephyr:** a página lida só traz terminologia (controller/peripheral; nomes master/slave deprecados desde a v4.5, remoção prevista na v5.0). A API (`spi_config`, `spi_transceive`, retorno `-errno`) fica no Doxygen e não foi lida: Não verificável.

Checklist: erro de FIFO, quadro e paridade tratados; buffers DMA alinhados e em RAM interna; um estilo de transação por dispositivo; dono único ou mutex; ISR/callbacks sem bloqueio e em IRAM se o flash puder ser escrito durante a operação; RX dimensionado para a taxa e política para `BUFFER_FULL`.

## 4. CAN no ESP-IDF (TWAI) (V-31)

| Tema | Regra | Rótulo |
| --- | --- | --- |
| Estados de erro | Error Active (contadores < 96), Error Warning (96 a 127), Error Passive (>= 128), Bus Off (TEC >= 256; só o TEC define bus-off) | Verificado |
| Recuperação | `twai_node_recover()` só de task; não é imediata e termina em `on_state_change`; devolve `ESP_ERR_INVALID_STATE` se o nó não está em bus-off; o número exato "129 bits recessivos" é ambíguo: use a regra operacional | Verificado / Não verificável (número) |
| Transmissão | `twai_node_transmit()` devolve `ESP_ERR_INVALID_STATE` em bus-off; buffer de TX assíncrono válido até `on_tx_done` | Verificado |
| Filtro | Um filtro de máscara no ESP32 (bit 1 deve coincidir, 0 ignorado; ID e máscara 0 aceita tudo); modo dual com dois filtros de 16 bits (em ID de 29 bits só os 16 altos); `twai_node_config_mask_filter()` com o nó desabilitado | Verificado |
| Hardware | Transceiver externo obrigatório (exemplo TJA105x), salvo teste de nó único com TX e RX em curto; taxa de bits e terminação de 120 ohm vêm do datasheet do transceiver e do barramento | Verificado (transceiver) / Não verificável (terminação e taxa nesta fonte) |
| FD | A página documenta API de FD, mas o controlador do ESP32 interpreta frames FD como erro: não generalize para outras variantes | Verificado |

Regra: todo nó CAN registra `on_state_change`, trata Bus Off e agenda a recuperação em task com limite de tentativas e atraso; o filtro é configurado com o nó desabilitado e testado com IDs dentro e fora da máscara.

## 5. MQTT 3.1.1 e 5.0 (V-33)

Números entre colchetes são identificadores de conformidade do OASIS 3.1.1 (lidos); **o MQTT 5.0 foi lido só até a metade** (as seções de QoS e reenvio do 5.0 não foram lidas: as regras de QoS abaixo são do 3.1.1).

| Tema | Regra | Origem |
| --- | --- | --- |
| Keep Alive | Cliente envia PINGREQ se não há outro pacote [MQTT-3.1.2-23]; servidor desconecta após 1,5 vez o intervalo [MQTT-3.1.2-24]; zero desliga o mecanismo | 3.1.1 |
| Will | Publicado em desconexão anormal e descartado após DISCONNECT; QoS 0 quando will flag é 0 [MQTT-3.1.2-13] | 3.1.1 |
| Sessão | CleanSession 1 descarta sessão [MQTT-3.1.2-6]; 0 retoma ou cria sessão [MQTT-3.1.2-4]. Mensagens QoS 1 e 2 só persistem com sessão | 3.1.1 |
| Packet Identifier | Não zero em SUBSCRIBE, UNSUBSCRIBE e PUBLISH com QoS > 0 [MQTT-2.3.1-1]; mesmo identificador no reenvio; DUP em 1 no reenvio [MQTT-3.3.1-1] | 3.1.1 |
| QoS 1 / QoS 2 | PUBACK com o mesmo identificador [MQTT-4.3.2-2]; QoS 2: PUBLISH, PUBREC, PUBREL, PUBCOMP, sem reenviar o PUBLISH depois do PUBREL [MQTT-4.3.3-1] | 3.1.1 |
| Reenvio | Obrigatório só ao reconectar com CleanSession 0 [MQTT-4.4.0-1]; a 3.1.1 não proíbe reenvio fora da reconexão | 3.1.1 |
| Curingas | Só em filtros; `#` por último e sozinho; `+` ocupa um nível inteiro; filtros com curinga não casam tópico começado por `$` | 3.1.1 |
| Violação | Fecha a conexão [MQTT-4.8.0-1] | 3.1.1 |
| Segurança | Capítulo 5, não normativo: TLS, porta 8883, evitar cifra NULL, autenticação e autorização no servidor | 3.1.1 |
| 5.0 | Server Keep Alive no CONNACK substitui o do cliente [MQTT-3.1.2-21]; Will Delay Interval: se a sessão reconecta antes do atraso, o will não sai [MQTT-3.1.3-9]; Clean Start 1 descarta sessão; Session Expiry Interval `0xFFFFFFFF` = sem expirar; Topic Alias Maximum 0 ou ausente proíbe alias; pacote acima de Maximum Packet Size é Protocol Error (DISCONNECT 0x95) | 5.0 |

Checklist de cliente MQTT de dispositivo:

1. Versão do protocolo registrada (3.1.1 ou 5.0).
2. Keep alive justificado pela rede e pela bateria; PINGREQ tratado.
3. Will com tópico de status e política de retain definida.
4. Sessão (CleanSession ou Clean Start e Session Expiry) escolhida de forma consciente.
5. QoS 1 pode duplicar: consumidor idempotente.
6. Reconexão com backoff e jitter (nunca laço fixo apertado).
7. TLS na porta 8883 com validação de certificado; credenciais fora do firmware versionado.
8. Buffer de recepção dimensionado para o Maximum Packet Size (Inferido).

Exemplo de achado (caso reserva `mqtt-client-review`): cliente com QoS 1 sem will, `clean_session=true`, laço de reconexão com `delay(1000)` fixo, porta 1883 e senha em literal no código. Achados: perda de mensagens QoS 1 na queda (sessão descartada), sem sinal de morte do dispositivo (sem will), reconexão sincronizada de frota derruba o broker (sem backoff/jitter), tráfego sem TLS e credencial no repositório (crítico). Fonte: V-33.

## 6. BLE (V-34): só decisão de pilha

As fontes lidas são índices. Registre **decisão**, não regra: qual pilha (Zephyr tem pilha BLE completa "from application to radio hardware" com LE Host, LE Audio, LE Controller; NimBLE no ESP-IDF é host configurável e qualificável pelo Bluetooth SIG, portado ao FreeRTOS, com controller acessado por VHCI e thread do host em `nimble_port_freertos_init`), qual papel, qual controller e qual versão. **Nenhuma regra de MTU, parâmetros de conexão, pareamento/segurança ou GATT tem fonte validada:** responda "Não verificável" e peça a documentação do host usado (Zephyr LE Host; NimBLE).

## 7. Teste em bancada de MQTT e BLE (V-61, só destilado)

As skills `testbench-mqtt`/`testbench-ble` do repositório Embedded-AI-Harness (MIT) dependem de uma bancada específica (API HTTP sem autenticação, broker aberto, `sudo`); **não instale nem copie**. Padrões úteis, em redação própria:

- Teste de reconexão com regra de firewall por dispositivo em vez de parar um broker compartilhado.
- O will de "morte" se observa pelo tópico de status; semeie um valor retido sentinela antes de testar o will.
- Valor retido durante a queda é obsoleto: exija pelo menos duas chegadas ao vivo antes de ler contadores.
- BLE: uma conexão por vez, dados em hex, desconecte antes de reconectar.
- Qualquer execução em bancada passa pelo gate de hardware.

## 8. Gotchas

- Modo assíncrono do I2C do ESP-IDF é experimental; páginas multi-alvo: confirme a variante.
- "129 bits" do TWAI ambíguo; número exato é Não verificável.
- Zephyr SPI: não cite campos da API sem ler o Doxygen da versão.
- Pull-up de linha CAN e terminação: sem fonte; datasheet do transceiver.
