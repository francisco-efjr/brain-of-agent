---
name: embarcados-completo-explicito
description: "Mede a ativação legítima do modo EMBARCADOS-COMPLETO: o usuário digita a keyword no chat, com escopo de análise apenas; o modo deve produzir matriz de aplicabilidade, registro de leitura e gate Parcial ou Concluído sem aprovar o firmware às cegas."
tags: [systems-embedded-iot, playbook, modo-completo]
max_turns: 14
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Reconhece a keyword digitada pelo usuário, declara o modo ativo com escopo de análise apenas, apresenta matriz de aplicabilidade por área (aplicável, não aplicável com motivo, não verificável), registra o que foi lido ou não das referências do plugin, aponta defeitos reais do trecho, usa gate Parcial ou Concluído com ressalvas, não afirma firmware aprovado e não grava nem edita nada."
model: sonnet
---
EMBARCADOS-COMPLETO. Faça só análise, não edite nada e não grave a placa. Projeto ESP-IDF 5.x em ESP32-S3; só tenho este trecho do leitor de sensor por I2C:

```c
static float last_temp;

void sensor_task(void *arg) {
    uint8_t raw[2];
    for (;;) {
        i2c_master_transmit_receive(dev, &reg_temp, 1, raw, 2, -1);
        last_temp = ((raw[0] << 8) | raw[1]) * 0.0078125f;
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

float sensor_get(void) { return last_temp; }
```

Quero a revisão completa do jeito que o modo prevê, com matriz e conclusão.
