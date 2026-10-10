---
name: i2c-driver-review
description: "Mede o disparo de bus-protocol-review e a revisão técnica de uso de I2C no ESP-IDF com timeout infinito, retorno não checado, pull-up interno a 400 kHz e possível acesso concorrente."
tags: [systems-embedded-iot, i2c, esp-idf, bus-protocol-review]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta o timeout -1 (espera indefinida) como causa provável do congelamento e pede timeout finito baseado no pior caso (incluindo o ciclo de escrita interno da EEPROM), o retorno não checado (NACK e timeout), o pull-up interno insuficiente a 400 kHz com pull-up externo dimensionado e medido e mutex se várias tarefas usam o barramento, rotula cada afirmação e pede o datasheet da EEPROM para os tempos."
model: sonnet
---
Revisa o uso de I2C neste firmware ESP-IDF que lê uma EEPROM (o sistema às vezes congela):

```c
i2c_master_bus_config_t bus_cfg = {
    .i2c_port = I2C_NUM_0, .sda_io_num = 21, .scl_io_num = 22,
    .clk_source = I2C_CLK_SRC_DEFAULT, .flags.enable_internal_pullup = true };
i2c_new_master_bus(&bus_cfg, &bus);
i2c_device_config_t dev_cfg = { .dev_addr_length = I2C_ADDR_BIT_LEN_7,
    .device_address = 0x50, .scl_speed_hz = 400000 };
i2c_master_bus_add_device(bus, &dev_cfg, &dev);
uint8_t reg = 0x00, buf[16];
i2c_master_transmit_receive(dev, &reg, 1, buf, 16, -1);
process(buf);
```
