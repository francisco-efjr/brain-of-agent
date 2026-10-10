---
name: c-firmware-review-heap-politica
description: "Mede o disparo de firmware-review e a revisão de C bare metal contra uma política declarada (sem heap após a inicialização, sem espera infinita), sem editar arquivos e sem rotular como Verificado o que o trecho não mostra."
tags: [systems-embedded-iot, firmware-review, c, politica-de-memoria]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Encontra pelo menos quatro problemas (malloc sem checagem e contra a política, retorno do HAL ignorado nas duas chamadas, HAL_MAX_DELAY contra a política, switch sem default, dono e tempo de vida do buffer DMA, ausência de timeout ou tratamento de erro do DMA), usa formato de achado com linha, gravidade e como verificar, não edita arquivos e não rotula como Verificado o que o trecho não mostra."
model: sonnet
---
Revisa este trecho de projeto bare metal (STM32, HAL). A política do projeto é: sem heap depois da inicialização, sem espera infinita.

```c
static uint8_t *rx;
void app_init(void) {
    rx = malloc(256);
    HAL_UART_Receive_DMA(&huart1, rx, 256);
    HAL_I2C_Master_Transmit(&hi2c1, 0x68 << 1, cfg, 2, HAL_MAX_DELAY);
}
void app_step(int state) {
    switch (state) {
    case 0: do_a(); break;
    case 1: do_b(); break;
    }
}
```
