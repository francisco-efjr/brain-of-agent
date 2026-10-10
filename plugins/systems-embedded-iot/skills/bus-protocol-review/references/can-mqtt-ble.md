# CAN (TWAI), MQTT e BLE: listas de verificação e roteiro de bancada

Uso: consulta da skill `bus-protocol-review`. Fontes lidas em 2026-10-10: V-31 (TWAI no ESP-IDF), V-33 (MQTT 3.1.1 e 5.0, OASIS), V-34 (BLE, só índices), V-61 (skills de bancada do SensorsIot, destiladas; MIT, nada copiado), V-35. Os números de regra `[MQTT-x.y.z-n]` vêm dos padrões OASIS. Rótulos: Verificado (lido na fonte), Inferido (conhecimento estável do domínio), Não verificável (sem fonte nesta rodada).

Sumário: [CAN (TWAI)](#can-twai) · [MQTT](#mqtt) · [BLE](#ble) · [Testes de bancada MQTT e BLE](#testes-de-bancada-mqtt-e-ble)

## CAN (TWAI)

Fonte: página TWAI do ESP-IDF (V-31). A página é multi-alvo e documenta API de FD, embora diga que o controlador do ESP32 interpreta frames FD como erro: não generalize para outras variantes.

| # | Verificação | Motivo e fonte | Rótulo |
| --- | --- | --- | --- |
| C-01 | O nó registra `on_state_change` e trata os estados: Error Active (contadores abaixo de 96), Error Warning (96 a 127), Error Passive (128 ou mais), Bus Off (TEC de 256 ou mais; só o TEC define bus-off). | Reação a degradação antes do bus-off. V-31. | Verificado |
| C-02 | Recuperação de Bus Off: `twai_node_recover()` só de tarefa (não de ISR), não é imediata e termina em `on_state_change`; limite de tentativas e atraso entre elas; `twai_node_transmit()` devolve `ESP_ERR_INVALID_STATE` em bus-off; `twai_node_recover()` devolve `ESP_ERR_INVALID_STATE` se o nó não está em bus-off. | Evita laço de recuperação que ocupa o barramento. V-31. | Verificado |
| C-03 | O buffer de transmissão assíncrona fica válido até `on_tx_done`. | Reutilizar o buffer antes corrompe o quadro. V-31. | Verificado |
| C-04 | Filtro de máscara: bit 1 deve coincidir, bit 0 é ignorado; ID e máscara 0 aceita tudo; modo dual com dois filtros de 16 bits (em ID de 29 bits só os 16 bits altos são filtrados). Configurar com o nó desabilitado (`twai_node_config_mask_filter()`) e testar IDs dentro e fora da máscara. | Filtro mal configurado perde mensagens ou entrega ruído. V-31. | Verificado |
| C-05 | Transceiver externo obrigatório (a página cita o TJA105x como exemplo), salvo teste de nó único com TX e RX em curto. | V-31. | Verificado |
| C-06 | Taxa de bits, terminação de 120 ohm e topologia vêm do datasheet do transceiver e do projeto do barramento. | Sem fonte nesta rodada. | Não verificável |
| C-07 | O número exato de bits recessivos para sair de bus-off ("129 consecutive recessive bits (11 bits each)") é ambíguo na página; use a regra operacional de C-02. | V-31, correção 5. | Verificado (ambiguidade) |

## MQTT

Fontes: OASIS MQTT 3.1.1 (29/10/2014) e 5.0 (07/03/2019). A leitura do 5.0 cobriu só a primeira metade (as seções de QoS e de reenvio do 5.0 não foram lidas); as regras de QoS abaixo são do 3.1.1.

| # | Verificação | Regra (fonte) | Rótulo |
| --- | --- | --- | --- |
| M-01 | Versão do protocolo registrada (3.1.1 ou 5.0). Muda o vocabulário (CleanSession contra Clean Start e Session Expiry) e os recursos. | V-33 | Verificado |
| M-02 | Keep alive justificado por rede e bateria. O cliente envia PINGREQ se não houve outro pacote [MQTT-3.1.2-23]; o servidor desconecta após 1,5 vez o intervalo [MQTT-3.1.2-24]; zero desliga o mecanismo. No 5.0 o Server Keep Alive do CONNACK substitui o do cliente [MQTT-3.1.2-21]. | V-33 | Verificado |
| M-03 | Will com tópico de status e retain definidos; publicado em desconexão anormal e descartado após DISCONNECT; Will QoS 0 quando o will flag é 0 [MQTT-3.1.2-13]. No 5.0, se a sessão reconecta antes do Will Delay Interval o will não sai [MQTT-3.1.3-9]. Padrão de projeto: publicar "online" (retain) após conectar e deixar o will publicar "offline" (retain) no mesmo tópico. | V-33 | Verificado (regras); padrão online/offline é Inferido |
| M-04 | Sessão escolhida de forma consciente: CleanSession 1 descarta a sessão [MQTT-3.1.2-6]; 0 retoma ou cria [MQTT-3.1.2-4]; mensagens de QoS 1 e 2 só persistem com sessão. No 5.0: Clean Start 1 descarta; Session Expiry Interval 0xFFFFFFFF significa sem expirar. | V-33 | Verificado |
| M-05 | QoS 1 pode duplicar: o consumidor é idempotente (PUBACK com o mesmo Packet Identifier [MQTT-4.3.2-2]; reenvio com o mesmo identificador e DUP em 1 [MQTT-3.3.1-1]). QoS 2 usa PUBLISH, PUBREC, PUBREL, PUBCOMP e não reenvia o PUBLISH depois do PUBREL [MQTT-4.3.3-1]. Reenvio obrigatório só ao reconectar com CleanSession 0 [MQTT-4.4.0-1]; o padrão não proíbe reenvio em outros momentos. Packet Identifier nunca é zero em SUBSCRIBE, UNSUBSCRIBE e PUBLISH com QoS maior que 0 [MQTT-2.3.1-1]. | V-33 | Verificado (3.1.1) |
| M-06 | Reconexão com backoff exponencial e jitter, com teto; sem laço fixo de poucos segundos que sobrecarrega o broker após queda da rede. Em muitos clientes embarcados o intervalo de reconexão é fixo: backoff exige desligar a reconexão automática e controlar na aplicação. | Prática de rede; detalhe do cliente varia | Inferido |
| M-07 | TLS na porta 8883 com validação de certificado; evitar cifra NULL; autenticação e autorização no servidor (capítulo 5 do padrão, não normativo). Credenciais fora do firmware versionado (provisionamento, NVS cifrada ou elemento seguro, conforme a plataforma). | V-33 | Verificado (TLS e cifra); provisionamento é Inferido |
| M-08 | Tópicos: curingas só em filtros de inscrição, `#` por último e sozinho no nível, `+` ocupa um nível inteiro, filtros com curinga não casam tópico que começa com `$` [MQTT-4.7.x]. Nunca publicar em tópico com curinga. | V-33 | Verificado |
| M-09 | Buffer de recepção do cliente dimensionado para o maior pacote esperado; no 5.0, pacote acima do Maximum Packet Size é Protocol Error com DISCONNECT 0x95. Violação de protocolo fecha a conexão [MQTT-4.8.0-1]. | V-33 (buffer: Inferido) | Verificado/Inferido |
| M-10 | Topic Alias Maximum zero ou ausente proíbe alias (5.0). | V-33 | Verificado |

Campos de configuração a procurar no esp-mqtt (nomes do ESP-IDF 5.x, Inferido: confira a estrutura `esp_mqtt_client_config_t` na versão instalada): `broker.address.uri` (esquema `mqtts://` para TLS), `broker.verification.*` (certificado ou bundle de autoridades), `credentials.*`, `session.keepalive`, `session.last_will.*` (tópico, mensagem, QoS, retain), `session.disable_clean_session`, `network.disable_auto_reconnect` e `network.reconnect_timeout_ms`. Em Zephyr o cliente MQTT tem estrutura própria e não foi lido nesta rodada (Não verificável).

Achados típicos em código real: QoS 1 sem will, `clean_session = true` com expectativa de mensagens retidas na sessão, laço de reconexão com `vTaskDelay(1000)` fixo, URI `mqtt://...:1883` com usuário e senha no código, tópico de comando assinado com curinga amplo (`#`) sem autorização no servidor, handler de mensagem que processa o payload dentro do callback do cliente (bloqueia o laço de rede).

## BLE

Fontes: índices do Zephyr (Bluetooth: Supported features, Qualification, Stack Architecture, LE Host, LE Audio, LE Controller, API, Tools, Shell) e da pilha NimBLE do ESP-IDF (host portado ao FreeRTOS, controller acessado por VHCI com `esp_nimble_hci_init()`, thread do host criada em `nimble_port_freertos_init` e substituível; V-34, classe B de 5, referência e não fonte de regra).

O que a skill faz com BLE: registrar a **decisão** (qual pilha, qual papel central/periférico, qual controller, qual versão) e perguntar o que falta. Nenhuma regra de MTU, parâmetros de conexão, segurança ou pareamento BLE tem fonte validada nesta rodada: qualquer valor desses é Não verificável e a resposta correta é pedir a documentação da pilha (subpáginas LE Host do Zephyr ou do NimBLE) ou o datasheet do SoC. Não cite valores de memória, de latência ou de consumo BLE sem a fonte.

## Testes de bancada MQTT e BLE

Destilado de V-61 (não copiado; a fonte depende de uma bancada específica com API HTTP sem autenticação, broker aberto e descoberta com `sudo`: não reproduza esse desenho). Este roteiro vale para qualquer bancada que o usuário já tenha. Cada passo que interage com a placa ou com o broker real passa pelo gate de `hw-bench-loop`.

MQTT:
1. **Will de morte**: observe pelo tópico de status que o firmware usa e não por um tópico de will separado. Antes do teste, publique um valor retido sentinela no tópico de status, para provar que o will o sobrescreve.
2. **Reconexão**: provoque a queda por regra de firewall por dispositivo, e não parando um broker compartilhado (outros dispositivos dependem dele).
3. **Retido obsoleto**: durante a queda o valor retido fica velho; exija pelo menos duas chegadas ao vivo (não retidas) antes de ler contadores e concluir que a telemetria voltou.
4. Registre a versão do firmware, o broker (versão e configuração de QoS/sessão), o relógio e o log do cliente; o resultado entra no registro de evidências com nível "em hardware".

BLE:
1. Uma conexão por vez; dados trafegados em hexadecimal; desconectar antes de reconectar; tratar "já conectado" como estado, não como falha aleatória.
2. Registre o dispositivo, a pilha e a versão; qualquer afirmação sobre MTU ou parâmetros de conexão negociados vem da captura real (log do host ou sniffer), nunca de memória.
