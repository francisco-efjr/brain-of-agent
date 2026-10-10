# Mapa de pinos - <placa / produto>

Alvo: <MCU exato + revisão do silício; módulo (ex.: com ou sem PSRAM)>. Fonte primária: <datasheet, seção; esquemático, revisão>. Cada linha precisa de fonte; sem fonte, a célula vai como "Não verificável". Não use rótulos de placa (D1, D2) como número de GPIO sem conferir o esquemático.

| GPIO / pino | Função | Componente | Direção | Pull (interno / externo) | Fonte (documento, seção) | Notas (boot, strapping, flash/PSRAM, só entrada) |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## Achados da auditoria (modo `pinos` de `datasheet-first`)

| ID | Gravidade | Achado | Pino(s) | Fonte | Rótulo |
| --- | --- | --- | --- | --- | --- |
| P-01 | | Pino ligado à flash/PSRAM do módulo em uso (ESP32 clássico: GPIO 6-11, e 16-17 com PSRAM, conforme doc ESP-IDF) | | | |
| P-02 | | Pino de strapping usado sem justificativa de boot (lista conforme datasheet da variante) | | | |
| P-03 | | Saída configurada em pino só de entrada (ESP32 clássico: GPIO 34-39) | | | |
| P-04 | | Mesmo pino em dois periféricos | | | |
| P-05 | | I2C só com pull-up interno | | | |
| P-06 | | Entrada flutuante | | | |
| P-07 | | ADC2 com Wi-Fi no ESP32 clássico (Inferido) | | | |
| P-08 | | Código diverge deste mapa | | | |

Vale para o ESP32 clássico; S2, S3, C3 e C6 têm mapas diferentes. Para outros MCUs, substitua os exemplos pelas restrições do datasheet da variante.
