# Esqueletos de driver: interface em C, driver genérico em Rust, constantes pendentes

Uso: consulta da skill `datasheet-first`. São moldes de estrutura, não drivers de componente real: nenhum endereço, registrador ou fórmula aqui pertence a um dispositivo concreto, e os valores de exemplo são espaços reservados que o build recusa até serem preenchidos com fonte. Fontes de desenho: V-16 (hardware atrás de interface estreita), V-47 (embedded-hal 1.0), V-37 (HAL falsa no host), lidas em 2026-10-10.

Sumário: [Camadas](#camadas) · [Interface de barramento em C](#interface-de-barramento-em-c) · [Constantes pendentes](#constantes-pendentes) · [Driver genérico em Rust](#driver-genérico-em-rust) · [Teste do driver com falso](#teste-do-driver-com-falso)

## Camadas

```text
app/        regra de negócio; só conhece a API do driver (testável no host)
drivers/    protocolo do componente (registradores, conversões); só conhece a interface de barramento
bsp/        liga a interface de barramento ao periférico real (HAL, ESP-IDF, Zephyr); pinos e clock aqui
generated/  código do gerador do fabricante (CubeMX etc.); não editar à mão
```

Regras (V-16): inicialização de cada periférico em um único lugar; dono do periférico e do DMA documentado; clock, pinos e prioridades de interrupção documentados no BSP; o driver nunca inclui o header do HAL.

## Interface de barramento em C

```c
/* drivers/bus.h: o driver depende disto, não do HAL */
#include <stddef.h>
#include <stdint.h>

typedef enum { BUS_OK = 0, BUS_NACK, BUS_TIMEOUT, BUS_FAIL } bus_status_t;

typedef struct {
    bus_status_t (*write_read)(void *ctx, uint8_t addr7,
                               const uint8_t *tx, size_t tx_len,
                               uint8_t *rx, size_t rx_len,
                               uint32_t timeout_ms);
    void *ctx;                       /* handle do periférico real, ou do falso no teste */
} i2c_bus_t;
```

```c
/* drivers/sensor_x.c */
#include "bus.h"
#include "sensor_x_regs.h"           /* constantes com fonte; ver "Constantes pendentes" */

typedef struct { const i2c_bus_t *bus; uint8_t addr7; } sensor_x_t;

int sensor_x_read_raw(const sensor_x_t *s, int16_t *out)
{
    uint8_t reg = SENSOR_X_REG_RESULT;      /* fonte: <datasheet §seção> */
    uint8_t buf[2];
    bus_status_t st = s->bus->write_read(s->bus->ctx, s->addr7, &reg, 1, buf, 2,
                                         SENSOR_X_XFER_TIMEOUT_MS);   /* fonte: <tabela de tempos> */
    if (st != BUS_OK) { return -(int)st; }  /* não toca *out em erro */
    *out = (int16_t)(((uint16_t)buf[0] << 8) | buf[1]);   /* ordem dos bytes: fonte <§> */
    return 0;
}
```

Pontos do molde: o driver não conhece o HAL; o retorno de erro é explícito e `*out` não muda em falha; o tempo limite e a ordem dos bytes são constantes com fonte; o BSP implementa `write_read` para o periférico real (por exemplo, chamando `i2c_master_transmit_receive` do ESP-IDF com o timeout recebido) e o teste de host implementa um falso.

## Constantes pendentes

Quando o datasheet ainda não foi fornecido, o cabeçalho de constantes existe, mas o build falha até alguém preencher cada valor com fonte. Assim nenhum valor chutado chega à placa.

```c
/* drivers/sensor_x_regs.h */
#pragma once

#ifndef SENSOR_X_DATASHEET_CONFIRMED
#error "sensor_x_regs.h: constantes PENDENTES. Preencher a partir do datasheet (endereço, registradores, tempos) e definir SENSOR_X_DATASHEET_CONFIRMED."
#endif

/* Depois de confirmar, cada linha leva a fonte: */
/* #define SENSOR_X_ADDR7            0x??   fonte: datasheet <doc> §<seção>, pino ADDR no esquemático <folha> */
/* #define SENSOR_X_REG_RESULT       0x??   fonte: datasheet <doc> §<seção> */
/* #define SENSOR_X_XFER_TIMEOUT_MS  ??     fonte: datasheet <doc> tabela de tempos; inclui conversão e stretching */
```

Para o teste de host, o falso pode definir a macro de confirmação e as constantes do **teste** (marcadas como valores do falso), mantendo o `#error` ativo no build de produto.

## Driver genérico em Rust

`embedded-hal` 1.0.0 (lido em 2026-10-10; confira `latest`) traz os módulos `delay`, `digital`, `i2c`, `pwm` e `spi` bloqueantes, mais `embedded-hal-async` e `embedded-hal-nb` (V-47). Regra: o driver é genérico sobre os traits, não sobre o tipo de um HAL.

```rust
#![no_std]
use embedded_hal::i2c::I2c;

// Constantes com fonte; enquanto pendentes, o crate não compila de propósito.
mod regs {
    // PENDENTE: preencher a partir do datasheet e remover o compile_error!
    compile_error!("sensor_x::regs pendente: endereço e registradores sem fonte");
    pub const ADDR: u8 = 0; // fonte: <datasheet §seção>
    pub const RESULT: u8 = 0; // fonte: <datasheet §seção>
}

pub struct SensorX<I2C> {
    i2c: I2C,
    addr: u8,
}

impl<I2C: I2c> SensorX<I2C> {
    pub fn new(i2c: I2C) -> Self {
        Self { i2c, addr: regs::ADDR }
    }

    /// Lê o registrador de resultado; propaga o erro do barramento sem tocar o valor.
    pub fn read_raw(&mut self) -> Result<i16, I2C::Error> {
        let mut buf = [0u8; 2];
        self.i2c.write_read(self.addr, &[regs::RESULT], &mut buf)?;
        Ok(i16::from_be_bytes(buf)) // ordem dos bytes: fonte <§>
    }

    pub fn release(self) -> I2C {
        self.i2c
    }
}
```

`I2c::write_read(address, write, read)` é o método do trait na série 1.0 (Inferido, conferir na documentação do crate na versão fixada). Timeout e política de repetição ficam no HAL concreto ou em um wrapper; o trait não define timeout. Teste de host: implemente um tipo falso com `impl embedded_hal::i2c::ErrorType` e `impl I2c` que devolve bytes ou um erro injetado (o crate `embedded-hal-mock` oferece falsos prontos; licença e versão a conferir antes de adotar, Não verificável aqui).

Revisão de driver Rust (V-47, V-12): `unsafe` justificado por invariante escrita; nenhum `static mut` tocado por interrupção; versão dos crates registrada; um único `#[panic_handler]` no binário final (não no crate de biblioteca).

## Teste do driver com falso

Com a interface de barramento, o teste de host cobre o que a placa só mostra tarde: NACK, timeout, resposta curta, ordem dos bytes. Exemplo de falso mínimo em C:

```c
typedef struct { bus_status_t status; uint8_t rx[4]; size_t rx_len; uint32_t last_timeout; } fake_t;

static bus_status_t fake_write_read(void *ctx, uint8_t a, const uint8_t *tx, size_t txl,
                                    uint8_t *rx, size_t rxl, uint32_t timeout_ms)
{
    fake_t *f = ctx; (void)a; (void)tx; (void)txl;
    f->last_timeout = timeout_ms;
    if (f->status != BUS_OK) { return f->status; }
    for (size_t i = 0; i < rxl && i < f->rx_len; i++) { rx[i] = f->rx[i]; }
    return BUS_OK;
}
```

O teste afirma que `sensor_x_read_raw` devolve erro negativo e preserva `*out` quando `status = BUS_NACK`, e que o `last_timeout` recebido é o da constante com fonte. Escrita completa e execução: `firmware-test-host`.
