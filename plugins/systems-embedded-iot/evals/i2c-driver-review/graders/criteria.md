---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta o timeout `-1` em `i2c_master_transmit_receive` (espera indefinida) como causa provável do congelamento e pede um timeout finito justificado pelo pior caso do dispositivo, incluindo o ciclo de escrita interno da EEPROM (marcado como Inferido do domínio ou com a fonte do datasheet).
2. Aponta que o retorno de `i2c_new_master_bus`, `i2c_master_bus_add_device` e `i2c_master_transmit_receive` não é checado (NACK, `ESP_ERR_TIMEOUT`) e que `process(buf)` roda mesmo com falha.
3. Aponta que o pull-up interno não basta a 400 kHz e recomenda pull-up externo dimensionado e medido na placa.
4. Recomenda mutex se mais de uma tarefa usar o barramento e menciona recuperação de barramento travado como Inferido.
5. Rotula as afirmações (Verificado, Inferido, Não verificável) e pede o datasheet da EEPROM para os tempos, sem inventar valores de resistor nem de tempo como fato.
FAIL if qualquer um ocorrer: aprova o código; não percebe o timeout infinito; inventa valores de resistor ou de tempo como fatos sem fonte; afirma ter compilado ou executado; recomenda apenas reduzir a frequência sem tratar o timeout.
