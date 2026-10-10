---
name: mqtt-client-review
description: "Mede o disparo de bus-protocol-review e a revisão de um cliente MQTT de dispositivo com QoS 1 sem will, sessão limpa, reconexão em laço fixo, porta 1883 e senha no código."
tags: [systems-embedded-iot, mqtt, esp-idf, bus-protocol-review]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta ausência de will e de tópico de status, sessão limpa com QoS 1 sem tratar duplicatas e perda, reconexão em laço fixo sem backoff e jitter, porta 1883 sem TLS e validação de certificado, senha no código versionado, registra a versão do protocolo como pendente, rotula as afirmações e não afirma ter testado com broker."
model: sonnet
---
Meu sensor ESP32 publica temperatura por MQTT e às vezes some do painel sem aviso. Dá uma olhada no cliente:

```c
esp_mqtt_client_config_t cfg = {
    .broker.address.uri = "mqtt://broker.example.invalid:1883",
    .credentials.username = "sensor01",
    .credentials.authentication.password = "temp123",
    .session.disable_clean_session = false,
};
esp_mqtt_client_handle_t client = esp_mqtt_client_init(&cfg);
esp_mqtt_client_start(client);

void publish_loop(void) {
    char payload[16];
    for (;;) {
        snprintf(payload, sizeof payload, "%.1f", read_temp());
        esp_mqtt_client_publish(client, "casa/sala/temp", payload, 0, 1, 0);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void on_disconnect(void) {
    for (;;) { esp_mqtt_client_reconnect(client); vTaskDelay(pdMS_TO_TICKS(500)); }
}
```
