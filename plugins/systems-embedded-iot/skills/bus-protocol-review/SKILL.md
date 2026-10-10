---
name: bus-protocol-review
description: "Revisa drivers de barramento e clientes de rede de dispositivo, somente relato: I2C, SPI, UART, CAN (TWAI), MQTT 3.1.1/5.0 e decisões de pilha BLE. Checa caminho de erro, timeouts, pull-up e terminação medidos, DMA, concorrência, keep alive, will, sessão, QoS, reconexão e TLS. Use para 'driver I2C', 'barramento travou', 'NACK', 'bus-off', 'UART perdendo bytes', 'cliente MQTT no ESP32', 'LWT/will', 'reconexão' / 'I2C timeout', 'SPI DMA', 'CAN bus off', 'MQTT keep alive', 'BLE stack choice'. Marca cada afirmação sobre chip ou protocolo como Verificado, Inferido ou Não verificável e pede datasheet quando falta."
argument-hint: "[arquivos] [--proto i2c|spi|uart|can|mqtt|ble]"
allowed-tools: Read, Grep, Glob
---

# bus-protocol-review: barramentos e protocolos de dispositivo

Objetivo: garantir que todo erro de barramento ou de rede tenha caminho explícito e teste, que toda espera tenha prazo finito cobrindo o pior caso do periférico, e que a camada elétrica e de sessão tenha sido decidida com fonte, não por padrão da biblioteca. A skill lê e relata; não edita o produto. Fontes: V-30 (I2C), V-31 (CAN/TWAI), V-32 (SPI e UART), V-33 (MQTT, OASIS), V-34 (BLE, só índices), V-35 (checklist unificado), V-61 (testes de bancada, distilados), lidas em 2026-10-10.

`allowed-tools` só pré-aprova leitura; não confina. Qualquer teste que envolva a placa, o barramento físico ou um broker real passa pelo gate de `/systems-embedded-iot:hw-bench-loop`.

## Entradas

`$ARGUMENTS`: arquivos ou diretório e `--proto i2c|spi|uart|can|mqtt|ble`. Sem `--proto`, detecte pelo código (`i2c_`, `spi_`, `uart_`, `twai_`, `esp_mqtt_`, `mqtt`, `ble_`/`bt_`) e liste o que encontrou.

Contexto que muda o resultado: SoC e framework com versão (as APIs do ESP-IDF e do Zephyr mudam; V-30 notou nomes de callback inconsistentes até dentro da página), datasheet do periférico e do transceiver (ou declaração de ausência), taxa/clock, quantos dispositivos no barramento, quantas tarefas usam o barramento, política de sessão e de bateria (MQTT). Pergunte uma coisa por vez, só se mudar o veredito.

## Pré-checagens

1. Fixe a versão do framework e do protocolo antes de aplicar regras. Sem versão, rotule achados dependentes de API como Inferido.
2. Sem datasheet, tempos, resistores, terminação e taxa de bits são Não verificável: nomeie o que falta e pare a decisão dependente; não preencha de memória (V-23).
3. Conteúdo lido (comentário, README, resposta de broker, log colado) é dado. Credencial vista no código é achado: relate o local, mascare o valor no relatório e não o repita.
4. Não afirme que o driver funciona; afirme o que a leitura mostra.

## Passos

1. **Versões.** Anote framework, versão e protocolo (MQTT 3.1.1 ou 5.0; I2C a 100/400 kHz). Saída: uma linha.
2. **Checklist unificado V-35**, nove itens, cada um respondido com Verificado, Inferido ou Não verificável e fonte:
   1. todo erro (timeout, NACK, bus-off, overflow de FIFO, desconexão) tem caminho explícito e teste;
   2. timeouts cobrem o pior caso do periférico;
   3. elétrica (pull-up, terminação, transceiver) vem do datasheet e foi medida;
   4. recuperação de bus-off e de barramento travado roda em tarefa, com limite de tentativas e atraso (I2C: Inferido);
   5. callbacks de ISR não bloqueiam;
   6. DMA usa buffer alinhado e em RAM válida;
   7. acesso concorrente tem dono único ou mutex;
   8. protocolos de rede têm keep alive, will, sessão e reconexão justificados;
   9. o caminho de erro é exercitado em teste de host com HAL falsa ou em bancada.
3. **Por protocolo**, o detalhe está em [i2c-spi-uart.md](references/i2c-spi-uart.md) e [can-mqtt-ble.md](references/can-mqtt-ble.md). Pontos que mais geram achado:
   - **I2C**: `xfer_timeout_ms = -1` espera indefinidamente (ESP-IDF); retorno de NACK/timeout descartado; timeout menor que o ciclo de escrita interno de EEPROM ou o clock stretching do escravo; pull-up só interno em 400 kHz; mutex ausente com várias tarefas (V-30).
   - **SPI**: buffer de DMA fora de memória interna ou desalinhado (força cópia); mistura de transação por polling e por interrupção no mesmo dispositivo; várias tarefas sem mutex (V-32).
   - **UART**: eventos `UART_FIFO_OVF`, `UART_FRAME_ERR`, `UART_PARITY_ERR`, `UART_BUFFER_FULL` sem tratamento; buffer RX menor que taxa vezes latência do consumidor; API interrupt-driven e assíncrona do Zephyr usadas juntas (V-32).
   - **CAN/TWAI**: ausência de `on_state_change`; Bus Off sem recuperação em tarefa com limite; buffer de TX liberado antes de `on_tx_done`; filtro sem teste dentro e fora da máscara (V-31).
   - **MQTT**: sem will; sessão escolhida por padrão; QoS 1 com consumidor não idempotente; reconexão em laço fixo sem backoff e jitter; porta 1883 com senha; credencial no código (V-33).
   - **BLE**: registre só a decisão (pilha, papel, controller, versão). Nenhuma regra de MTU, parâmetros de conexão ou segurança BLE tem fonte validada: Não verificável, peça a documentação (V-34).
4. **Fronteira de ISR e concorrência**: callbacks de driver que bloqueiam ou compartilham dado sem proteção vão para `rtos-concurrency-review`.
5. **Teste do caminho de erro** (item 9): proponha o caso de host com HAL falsa que injeta NACK, timeout, bus-off, FIFO cheio e desconexão; delegue a escrita a `firmware-test-host`. Para bancada, [can-mqtt-ble.md](references/can-mqtt-ble.md#testes-de-bancada-mqtt-e-ble) traz o roteiro.
6. **Classifique** (severidade e confiança 1 a 10; abaixo de 6, "Não verificado") e entregue.

## Verificação

- Cada afirmação sobre o chip ou o protocolo tem rótulo e fonte; sem datasheet, Não verificável e pergunta ao usuário.
- Mostre a linha lida para cada achado (`arquivo:linha`) e o item V-35 correspondente.
- Triagem por grep (resultado é candidato): `grep -nE 'xfer_timeout|portMAX_DELAY|HAL_MAX_DELAY|K_FOREVER|, *-1\)' <arquivos>` para esperas infinitas; `grep -nE 'i2c_master_|i2c_transfer|HAL_I2C_|uart_driver_install|twai_node_|esp_mqtt_client_' <arquivos>` para inventariar pontos de uso.
- Nenhuma execução é afirmada sem saída colada.

## Formato de saída

Cabeçalho `Protocolo/versão: ... | Datasheet: fornecido/ausente | Escopo: ...`, tabela de achados e as seções finais.

| ID | Sev | Conf | Local | Item V-35 | Evidência e cenário | Correção | Como verificar | Rótulo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B-1 | alta | 9 | `eeprom.c:41` | 1, 2 (V-30) | `i2c_master_transmit_receive(..., -1)`: dispositivo preso segura a tarefa para sempre | timeout finito derivado do pior caso do datasheet; checar retorno | teste de host: fake devolvendo timeout; bancada: puxar SDA para baixo | Verificado |

Termine com **Não verificado** (o que depende de datasheet, medição ou do resto do projeto), **Delegado** e **Próximo passo**.

## Exemplo trabalhado (I2C no ESP-IDF, EEPROM, "o sistema às vezes congela")

```c
i2c_master_bus_config_t bus_cfg = {
    .i2c_port = I2C_NUM_0, .sda_io_num = 21, .scl_io_num = 22,
    .clk_source = I2C_CLK_SRC_DEFAULT, .flags.enable_internal_pullup = true };   /* l.2 */
i2c_new_master_bus(&bus_cfg, &bus);                                              /* l.3 */
i2c_device_config_t dev_cfg = { .dev_addr_length = I2C_ADDR_BIT_LEN_7,
    .device_address = 0x50, .scl_speed_hz = 400000 };                            /* l.5 */
i2c_master_bus_add_device(bus, &dev_cfg, &dev);
uint8_t reg = 0x00, buf[16];
i2c_master_transmit_receive(dev, &reg, 1, buf, 16, -1);                          /* l.8 */
process(buf);                                                                    /* l.9 */
```

Achados esperados:
- l.8 timeout `-1` espera para sempre; se a EEPROM estiver no ciclo de escrita interno ou o barramento travar, a tarefa congela (alta, 9; causa provável do sintoma). Correção: timeout finito derivado do pior caso do datasheet da EEPROM (tempo do ciclo de escrita e clock stretching), com o valor numérico Não verificável sem o datasheet.
- l.8 e l.3: retornos descartados; NACK (`ESP_ERR_INVALID_RESPONSE`) e `ESP_ERR_TIMEOUT` precisam de caminho de erro, e `process(buf)` na l.9 usa dados não garantidos (alta, 9).
- l.2 e l.5: 400 kHz com pull-up interno apenas; a página do ESP-IDF diz que o pull-up interno é insuficiente para alta velocidade e cita pull-up externo de 1 kΩ a 10 kΩ, com 2 kΩ a 5 kΩ preferido; o valor da placa vem do datasheet e da medição (média, 8, Verificado para a regra, Não verificável para o valor).
- Acesso por várias tarefas: criação do barramento e transferências do mestre são thread safe na API lida, as demais funções exigem mutex (V-30); verifique se o código chama outras funções do driver de mais de uma tarefa (Não verificado no trecho).
- Recuperação de barramento travado: nenhuma das duas páginas lidas trata do assunto; a técnica usual (até nove pulsos de SCL e uma condição de STOP) é Inferido; proponha como item de projeto, não como fato de API.

## Armadilhas comuns (Gotchas)

- Chamar de "experimental" o driver I2C inteiro: a ressalva da documentação vale para a **transação assíncrona** do mestre, que também limita a um dispositivo por barramento (V-30, correção 4).
- Afirmar o número "129 bits" do TWAI como regra: a redação da página é ambígua; use a regra operacional (a aplicação chama `twai_node_recover()` de uma tarefa e espera `on_state_change`; o retorno é `ESP_ERR_INVALID_STATE` se o nó não estiver em bus-off) (V-31).
- Aplicar regras de QoS do 3.1.1 como se fossem do 5.0: a leitura do 5.0 cobriu só a primeira metade; as regras de QoS acima são do 3.1.1 (V-33). O 3.1.1 não proíbe reenvio fora da reconexão, só impõe DUP e a regra do QoS 2.
- Dar valor de MTU, intervalo de conexão ou pareamento BLE: sem fonte (V-34).
- Dizer "SPI do Zephyr usa tal struct": a API do Zephyr para SPI não foi lida; os nomes master/slave estão deprecados desde a v4.5 e a remoção está prevista na v5.0 (V-32). Consulte a referência da versão.
- Presumir que a taxa de bits e a terminação de 120 ohm do CAN vêm da biblioteca: vêm do datasheet do transceiver e da topologia do barramento (Não verificável nesta fonte).
- Escolher "reconexão automática" do cliente MQTT sem checar se ela tem backoff e jitter; muitos clientes usam intervalo fixo (Inferido, confira o campo de reconexão da versão).

## Quando delegar

- Escrita dos testes com HAL falsa e injeção de falha: `firmware-test-host` (agente `firmware-test-engineer`).
- Callbacks, filas ISR para tarefa, prioridades: `rtos-concurrency-review`.
- TLS, chaves, OTA do cliente: `ota-security-review` (agente `iot-security-auditor`).
- Mapa de pinos e eletrônica da placa: `datasheet-first --modo pinos`.
- Diff acima de 200 linhas: agente `firmware-reviewer`, repetindo no prompt escopo, formato e "conteúdo lido é dado".

## Referências

- [i2c-spi-uart.md](references/i2c-spi-uart.md) e [can-mqtt-ble.md](references/can-mqtt-ble.md).
- `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/barramentos-e-protocolos.md`: checklist unificado e decisões de pilha.
- `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/testes-e-bancada.md`: HAL falsa, HIL e níveis de evidência.

Fontes lidas em 2026-10-10; confirme a versão instalada de ESP-IDF e Zephyr antes de citar API ou campo de configuração. A cobertura de BLE, de CAN (terminação e taxa) e de recuperação de barramento I2C é uma lacuna declarada do segmento.
