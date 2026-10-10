---
name: rust-static-mut-isr
description: "Mede o disparo de rtos-concurrency-review em Rust no_std: static mut tocado por uma interrupção de timer e pelo laço principal, com leitura-modificação-escrita e zeragem concorrentes."
tags: [systems-embedded-iot, rust, no_std, isr, rtos-concurrency-review]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Identifica static mut tocado pela interrupção e pelo main como corrida (a zeragem em main e o incremento na ISR perdem atualização), explica a intercalação concreta, propõe Mutex<Cell<u32>> com seção crítica (critical-section) ou atômico com a ressalva de que Cortex-M0 e M0+ só têm load e store, pergunta ou registra a arquitetura, menciona inicializar antes de habilitar a interrupção e não afirma ter compilado."
model: sonnet
---
Estou aprendendo Rust embarcado. Este firmware pisca um LED a cada 1000 ticks de um timer, mas às vezes o LED pisca fora de hora. O que pode estar errado?

```rust
#![no_std]
#![no_main]

use panic_halt as _;
use cortex_m_rt::entry;
use hal::pac::interrupt;

static mut TICKS: u32 = 0;

#[interrupt]
fn TIM2() {
    unsafe { TICKS += 1; }
}

#[entry]
fn main() -> ! {
    let mut led = setup_led();
    setup_timer_tim2();
    loop {
        unsafe {
            if TICKS >= 1000 {
                TICKS = 0;
                led.toggle();
            }
        }
    }
}
```
