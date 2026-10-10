---
name: pinos-esp32-auditoria
description: "Mede o disparo de datasheet-first no modo pinos e a auditoria de GPIO de um ESP32 clássico: saída em pino só de entrada, pino de flash, strapping, dois periféricos no mesmo pino e I2C só com pull-up interno."
tags: [systems-embedded-iot, datasheet-first, pinos, esp32]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Monta a tabela GPIO, função, direção e pull; aponta GPIO 35 como saída (pino só de entrada), GPIO 6 em uso (pino de flash do módulo), GPIO 12 de strapping sem justificativa, GPIO 21 usado por I2C e por um relé, e I2C apenas com pull-up interno; pede o esquemático e o módulo exato; marca como Não verificável o que depende do datasheet do módulo; não afirma que o hardware foi testado."
model: sonnet
---
Antes de mandar fazer a PCB, audita a pinagem deste projeto ESP32 (módulo WROOM-32, o clássico):

```c
#define PIN_LED      GPIO_NUM_35   // LED de status
#define PIN_RELE     GPIO_NUM_21   // aciona o relé da bomba
#define PIN_BOTAO    GPIO_NUM_6    // botão de manual
#define PIN_ENABLE   GPIO_NUM_12   // habilita o driver do motor

i2c_master_bus_config_t bus = { .sda_io_num = GPIO_NUM_21, .scl_io_num = GPIO_NUM_22,
                                .flags.enable_internal_pullup = true };  // sensor a 400 kHz
gpio_set_direction(PIN_LED, GPIO_MODE_OUTPUT);
gpio_set_direction(PIN_ENABLE, GPIO_MODE_OUTPUT);
```
