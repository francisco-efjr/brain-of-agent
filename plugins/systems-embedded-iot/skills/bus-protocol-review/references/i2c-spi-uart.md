# I2C, SPI e UART: listas de verificação por framework

Uso: consulta da skill `bus-protocol-review`. Fontes lidas em 2026-10-10: V-30 (Zephyr e ESP-IDF, I2C), V-32 (SPI/UART no ESP-IDF e no Zephyr), V-35 (checklist). Marcação: Verificado = visto na página citada; Inferido = conhecimento estável do domínio, não relido; Não verificável = sem fonte nesta rodada. Valores elétricos e de tempo vêm do datasheet do periférico e da medição na placa; as faixas abaixo são as que a documentação do framework cita.

Sumário: [I2C](#i2c) · [SPI](#spi) · [UART](#uart) · [Dimensionar buffer de RX](#dimensionar-buffer-de-rx) · [Teste de host com HAL falsa](#teste-de-host-com-hal-falsa)

## I2C

| # | Verificação | Motivo e fonte | Rótulo |
| --- | --- | --- | --- |
| I-01 | Todo retorno de transferência é checado; `-ETIMEDOUT` (Zephyr) e `ESP_ERR_TIMEOUT` (ESP-IDF) têm caminho de erro; NACK (`ESP_ERR_INVALID_RESPONSE`) e `ESP_ERR_NOT_FOUND` também. | Falha de periférico é rotina em campo. V-30. | Verificado |
| I-02 | Timeout finito que cobre o pior caso do dispositivo: ciclo de escrita interno de EEPROM, clock stretching do escravo, conversão de sensor. ESP-IDF: `xfer_timeout_ms = -1` espera indefinidamente e é desaconselhado. Zephyr: timeout por controlador em `zephyr,transfer-timeout-ms`, depois `CONFIG_I2C_TRANSFER_TIMEOUT_MS`, depois `K_FOREVER` se o valor for 0 (alguns drivers que gravam o timeout direto no hardware rejeitam 0 no build). | Espera infinita transforma falha transitória em travamento. V-30. | Verificado (valores numéricos do dispositivo: Não verificável sem datasheet) |
| I-03 | Para EEPROM do tipo 24xx, o dispositivo não responde ACK ao endereço durante o ciclo interno de escrita; o driver usa sondagem de ACK com limite de tentativas e tempo máximo do datasheet. | Padrão de projeto de EEPROM serial. | Inferido |
| I-04 | Pull-up externo dimensionado e medido. Página do ESP-IDF: 1 kΩ a 10 kΩ, 2 kΩ a 5 kΩ preferido, nunca abaixo de 1 kΩ; pull-up interno é insuficiente para alta velocidade; SCL de mestre até 400 kHz. | Borda lenta ou corrente excessiva. O valor final depende da capacitância do barramento e do número de dispositivos. V-30. | Verificado (faixa citada); valor da placa Não verificável sem medição |
| I-05 | Callbacks chamados em contexto de ISR não bloqueiam e usam apenas APIs `FromISR`. | V-30, V-52. | Verificado |
| I-06 | Criação do barramento e transferências do mestre são thread safe no ESP-IDF; as demais funções exigem mutex do chamador. Dono único do barramento por tarefa ou mutex explícito. | V-30. | Verificado |
| I-07 | Modo assíncrono do mestre no ESP-IDF é experimental e restringe a um dispositivo por barramento; a página mistura `on_recv_done` e `on_trans_done`: confira a estrutura de callbacks na versão instalada. | V-30, correção 4. | Verificado |
| I-08 | O controlador do ESP32 não faz clock stretching quando atua como escravo; `scl_wait_us` é a espera do mestre (0 usa o padrão do registrador); o "cerca de 12 ms" da página é dito como possível, não como limite. | V-30. | Verificado |
| I-09 | Recuperação de barramento travado (escravo segurando SDA baixo): reconfigurar SCL como GPIO, gerar até nove pulsos de clock até SDA liberar, emitir STOP, reinicializar o controlador; rodar em tarefa, com limite de tentativas e atraso. Nenhuma das duas páginas lidas trata de bus recovery. | Técnica descrita nas especificações I2C. | Inferido |
| I-10 | Endereço de 7 bits: o valor passado ao driver é o endereço de 7 bits (HAL do STM32 espera o endereço deslocado de 1 bit, `0x68 << 1`). | Fonte comum de "NACK sempre" ao portar. | Inferido |
| I-11 | Terminologia: API de controller estável e de target experimental no Zephyr; terminologia da especificação NXP I2C Rev 7.0 (controller/target). | V-30. | Verificado |

Correção típica (ESP-IDF, API de mestre nova): o timeout vira constante nomeada com a origem do número, o retorno é tratado e o erro sobe.

```c
/* origem do número: datasheet da EEPROM, tempo do ciclo de escrita e stretching (registre a seção) */
#define EEPROM_XFER_TIMEOUT_MS  20
esp_err_t err = i2c_master_transmit_receive(dev, &reg, 1, buf, sizeof buf, EEPROM_XFER_TIMEOUT_MS);
if (err != ESP_OK) {
    ESP_LOGW(TAG, "i2c read failed: %s", esp_err_to_name(err));
    return err;               /* quem chama decide: repetir, recuperar barramento ou reportar */
}
```

O valor 20 é um espaço reservado para o exemplo compilar, não um recomendado; o comentário exige a origem do número.

## SPI

| # | Verificação | Motivo e fonte | Rótulo |
| --- | --- | --- | --- |
| S-01 | ESP-IDF: buffers de DMA em memória interna compatível com DMA e alinhados a 32 bits (comprimento múltiplo de 4); buffer desalinhado força cópia temporária. | V-32. | Verificado |
| S-02 | `max_transfer_sz`: padrão 4092 com DMA e, sem DMA, o tamanho do FIFO (normalmente 64 bytes); transferência maior que o limite falha. | V-32. | Verificado |
| S-03 | Um só estilo de transação por dispositivo: polling termina antes e prende a CPU; por interrupção libera a CPU e demora mais. A página recomenda não misturar. | V-32. | Verificado |
| S-04 | Thread safety: cada dispositivo com uma tarefa dona; senão mutex. | V-32. | Verificado |
| S-05 | Só o ISR do driver fica em IRAM por padrão; callbacks quando se usa `ESP_INTR_FLAG_IRAM` precisam estar em IRAM. | V-32. | Verificado |
| S-06 | Limites típicos de clock no ESP32: 80 MHz (IO_MUX) e 26 MHz (GPIO matrix); o limite do dispositivo vem do datasheet dele. | V-32. | Verificado (ESP32 clássico) |
| S-07 | `cs_ena_pretrans` é incompatível com as fases de comando e endereço em full-duplex. | V-32. | Verificado |
| S-08 | Modo SPI (CPOL/CPHA), ordem de bits e polaridade de CS seguem o datasheet do dispositivo; erro aqui produz dados "quase certos". | Padrão do domínio. | Inferido |
| S-09 | Zephyr: terminologia controller/peripheral; nomes master/slave deprecados desde a v4.5, remoção prevista na v5.0. A API (`spi_config`, `spi_transceive`, retorno `-errno`) não foi lida: consulte a referência Doxygen da versão. | V-32. | Verificado (terminologia); API Não verificável |

## UART

| # | Verificação | Motivo e fonte | Rótulo |
| --- | --- | --- | --- |
| U-01 | ESP-IDF: buffer de RX do driver maior que o FIFO de hardware; eventos `UART_BUFFER_FULL`, `UART_FIFO_OVF`, `UART_FRAME_ERR`, `UART_PARITY_ERR` e `UART_BREAK` chegam pela fila de eventos e têm tratamento (contador, descarte controlado, resincronização de protocolo). | V-32. | Verificado |
| U-02 | Não passar `ESP_INTR_FLAG_IRAM` ao instalar o driver de UART. | V-32. | Verificado |
| U-03 | Controle de fluxo por hardware (RTS/CTS) ou software (XON 0x11, XOFF 0x13) escolhido quando a taxa do transmissor excede o consumo. | V-32. | Verificado |
| U-04 | A página do ESP-IDF não declara garantia geral de thread safety da UART: um dono por porta ou mutex. | V-32. | Verificado |
| U-05 | Zephyr: três APIs (polling, interrupt-driven, assíncrona com DMA); interrupt-driven e assíncrona não devem ser usadas ao mesmo tempo no mesmo periférico (`CONFIG_UART_EXCLUSIVE_API_CALLBACKS` ligado por padrão); `uart_poll_out()` bloqueia. | V-32. | Verificado |
| U-06 | Enquadramento de mensagem (delimitador, comprimento, CRC) tolera byte perdido e começa a ressincronizar após timeout de silêncio. | Padrão do domínio. | Inferido |
| U-07 | Taxa (baud) e erro de clock: a combinação baud/clock do SoC tem erro percentual aceitável; vem do manual de referência. | Padrão do domínio. | Não verificável sem manual |

## Dimensionar buffer de RX

Aritmética para o buffer da UART (8N1, ou seja, 10 bits por byte no fio): bytes por segundo = baud / 10. A 115200 baud são 11520 B/s, cerca de 11,5 B/ms. Buffer mínimo = taxa × pior latência do consumidor + tamanho da maior mensagem. Se a tarefa consumidora pode ficar 50 ms sem rodar (log síncrono, TLS, escrita em flash), o buffer precisa guardar 50 ms de dados mais a mensagem; a latência de pior caso é medida (Suposição até a medição). A política para `UART_BUFFER_FULL` (descartar o mais antigo, descartar o novo, parar o transmissor por fluxo) é decisão de projeto registrada.

## Teste de host com HAL falsa

Todo item acima que diz "tem caminho de erro" fica verificável com uma interface estreita para o barramento. Esqueleto em C (a interface é o que o driver enxerga; o hardware real a implementa e o teste injeta falhas):

```c
typedef enum { BUS_OK = 0, BUS_NACK, BUS_TIMEOUT, BUS_FAIL } bus_status_t;
typedef struct {
    bus_status_t (*write_read)(void *ctx, uint8_t addr7,
                               const uint8_t *w, size_t wl,
                               uint8_t *r, size_t rl, uint32_t timeout_ms);
    void *ctx;
} i2c_bus_t;
```

O teste cria um falso com uma fila de respostas (`BUS_OK` com bytes, `BUS_NACK`, `BUS_TIMEOUT`) e verifica que o driver propaga o erro, não usa o buffer de leitura quando houve falha, respeita o limite de tentativas e chama o falso com o timeout esperado. O roteiro completo está em `firmware-test-host`.
