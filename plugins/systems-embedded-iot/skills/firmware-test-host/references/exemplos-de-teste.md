# Exemplos de teste de firmware: Unity, CMock, ztest, ESP-IDF, PlatformIO e Rust

Uso: consulta da skill `firmware-test-host`. Código original deste plugin (MIT do plugin), sem trechos de terceiros. Fontes de API lidas em 2026-10-10: V-36 (ztest), V-37 (Unity, CMock, Ceedling), V-38 (ESP-IDF e pytest-embedded), V-57 (PlatformIO), V-47 (embedded-hal). Nenhum exemplo foi **executado** nesta rodada de construção: antes de apresentar como funcional, compile e rode (a skill exige saída colada). Nomes de macros e opções variam por versão: confira a instalada.

Sumário: [Unity: buffer circular](#unity-buffer-circular) · [CMock](#cmock) · [ztest](#ztest) · [ESP-IDF](#esp-idf) · [PlatformIO](#platformio) · [Rust com falso de embedded-hal](#rust-com-falso-de-embedded-hal) · [Falso de driver em C com injeção de erro](#falso-de-driver-em-c-com-injeção-de-erro)

## Unity: buffer circular

Contrato: `rb_push` devolve 0 se coube e -1 se cheio; `rb_pop` devolve 0 e escreve a saída, ou -1 se vazio, sem alterar a saída.

`src/rb.h`

```c
#pragma once
#include <stddef.h>
#include <stdint.h>

typedef struct { uint8_t *buf; size_t cap, head, tail, len; } rb_t;

void rb_init(rb_t *r, uint8_t *storage, size_t cap);
int  rb_push(rb_t *r, uint8_t b);    /* 0 ok, -1 cheio */
int  rb_pop(rb_t *r, uint8_t *out);  /* 0 ok, -1 vazio */
```

**Passo vermelho**: comece com `src/rb.c` que apenas devolve -1 nas duas funções e confirme que os testes abaixo falham pelo motivo certo (valores diferentes do esperado), não por erro de compilação. Depois troque pela implementação.

`src/rb.c`

```c
#include "rb.h"

void rb_init(rb_t *r, uint8_t *storage, size_t cap)
{
    r->buf = storage; r->cap = cap;
    r->head = 0; r->tail = 0; r->len = 0;
}

int rb_push(rb_t *r, uint8_t b)
{
    if (r->len == r->cap) { return -1; }      /* cobre cap == 0 sem dividir por zero */
    r->buf[r->head] = b;
    r->head = (r->head + 1) % r->cap;
    r->len++;
    return 0;
}

int rb_pop(rb_t *r, uint8_t *out)
{
    if (r->len == 0) { return -1; }
    *out = r->buf[r->tail];
    r->tail = (r->tail + 1) % r->cap;
    r->len--;
    return 0;
}
```

`test/test_rb.c`

```c
#include "unity.h"
#include "rb.h"

static rb_t r;
static uint8_t store[4];

void setUp(void)    { rb_init(&r, store, sizeof store); }
void tearDown(void) { }

void test_pop_on_empty_fails_and_keeps_output(void)
{
    uint8_t v = 0xAA;
    TEST_ASSERT_EQUAL_INT(-1, rb_pop(&r, &v));
    TEST_ASSERT_EQUAL_UINT8_MESSAGE(0xAA, v, "saida nao pode mudar em erro");
}

void test_push_then_pop_returns_same_byte(void)
{
    uint8_t v = 0;
    TEST_ASSERT_EQUAL_INT(0, rb_push(&r, 0x5A));
    TEST_ASSERT_EQUAL_INT(0, rb_pop(&r, &v));
    TEST_ASSERT_EQUAL_UINT8(0x5A, v);
}

void test_push_on_full_fails_and_keeps_data(void)
{
    uint8_t v = 0;
    for (uint8_t i = 0; i < 4; i++) { TEST_ASSERT_EQUAL_INT(0, rb_push(&r, i)); }
    TEST_ASSERT_EQUAL_INT(-1, rb_push(&r, 99));
    TEST_ASSERT_EQUAL_INT(0, rb_pop(&r, &v));
    TEST_ASSERT_EQUAL_UINT8(0, v);               /* o 99 nao entrou */
}

void test_fifo_order_survives_index_wraparound(void)
{
    uint8_t v = 0;
    const uint8_t expect[] = { 2, 3, 4, 5 };
    for (uint8_t i = 0; i < 3; i++) { TEST_ASSERT_EQUAL_INT(0, rb_push(&r, i)); }   /* 0 1 2 */
    TEST_ASSERT_EQUAL_INT(0, rb_pop(&r, &v));                                       /* sai 0 */
    TEST_ASSERT_EQUAL_INT(0, rb_pop(&r, &v));                                       /* sai 1 */
    for (uint8_t i = 3; i < 6; i++) { TEST_ASSERT_EQUAL_INT(0, rb_push(&r, i)); }   /* head dá a volta */
    for (size_t k = 0; k < sizeof expect; k++) {
        TEST_ASSERT_EQUAL_INT(0, rb_pop(&r, &v));
        TEST_ASSERT_EQUAL_UINT8(expect[k], v);
    }
}

void test_capacity_one(void)
{
    rb_t one; uint8_t s[1]; uint8_t v = 0;
    rb_init(&one, s, sizeof s);
    TEST_ASSERT_EQUAL_INT(0, rb_push(&one, 7));
    TEST_ASSERT_EQUAL_INT(-1, rb_push(&one, 8));
    TEST_ASSERT_EQUAL_INT(0, rb_pop(&one, &v));
    TEST_ASSERT_EQUAL_UINT8(7, v);
    TEST_ASSERT_EQUAL_INT(-1, rb_pop(&one, &v));
}

void test_capacity_zero_never_accepts(void)
{
    rb_t zero; uint8_t v = 0;
    rb_init(&zero, NULL, 0);
    TEST_ASSERT_EQUAL_INT(-1, rb_push(&zero, 1));
    TEST_ASSERT_EQUAL_INT(-1, rb_pop(&zero, &v));
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_pop_on_empty_fails_and_keeps_output);
    RUN_TEST(test_push_then_pop_returns_same_byte);
    RUN_TEST(test_push_on_full_fails_and_keeps_data);
    RUN_TEST(test_fifo_order_survives_index_wraparound);
    RUN_TEST(test_capacity_one);
    RUN_TEST(test_capacity_zero_never_accepts);
    return UNITY_END();
}
```

Notas: `setUp`/`tearDown` são chamados por Unity antes e depois de cada `RUN_TEST`. Ponteiro `NULL` em `rb_push`/`rb_pop` não tem teste porque o contrato acima não o define; se o projeto decidir que `NULL` é erro (-1) ou asserção, a decisão entra no contrato e depois no teste. Com Ceedling, o `main` e a lista de `RUN_TEST` são gerados e basta a função `test_*`.

Verificação de qualidade: introduza uma quebra deliberada (por exemplo, remova `% r->cap` do `rb_push`) e confirme que `test_fifo_order_survives_index_wraparound` falha; desfaça. Rode também sob `-fsanitize=address,undefined` no host (V-59).

## CMock

CMock gera mocks de headers C e funciona com Unity; Ceedling reúne Unity, CMock e CException e copia as dependências para `vendor/` com `ceedling new --local`; CMock exige Ruby (V-37, V-38). O gerador cria, por função do header, funções de expectativa; abaixo, o padrão de uso para um driver que depende de `i2c_bus.h` (nomes gerados e plugins dependem da configuração do projeto; Inferido, confirme na documentação do CMock instalado):

```c
#include "unity.h"
#include "mock_i2c_bus.h"          /* gerado a partir de i2c_bus.h */
#include "sensor_x.h"

void test_sensor_returns_error_when_bus_nacks(void)
{
    int16_t out = 1234;
    /* espera uma chamada de write_read e a faz devolver NACK */
    i2c_bus_write_read_ExpectAnyArgsAndReturn(BUS_NACK);
    TEST_ASSERT_LESS_THAN_INT(0, sensor_x_read_raw(&sensor, &out));
    TEST_ASSERT_EQUAL_INT16(1234, out);          /* saida preservada */
}
```

Regra de uso: mock para verificar o que importa (erro propagado, chamadas obrigatórias); para muitas chamadas com dados, um falso escrito à mão (abaixo) é mais legível que dezenas de `Expect`.

## ztest

Zephyr (`unit_testing` constrói só o código testado e o Ztest e funciona apenas em Linux; `native_sim` constrói o sistema completo para o host) (V-36). Cabeçalho `<zephyr/ztest.h>` nas versões atuais; versões antigas usavam `<ztest.h>`: confirme.

```c
#include <zephyr/ztest.h>
#include "rb.h"

static rb_t r;
static uint8_t store[4];

static void before(void *fixture)
{
    ARG_UNUSED(fixture);
    rb_init(&r, store, sizeof store);
}

ZTEST_SUITE(rb_suite, NULL, NULL, before, NULL, NULL);   /* predicate, setup, before, after, teardown */

ZTEST(rb_suite, test_pop_on_empty)
{
    uint8_t v = 0xAA;
    zassert_equal(-1, rb_pop(&r, &v), "pop em vazio deve falhar");
    zassert_equal(0xAA, v, "saida nao pode mudar");
}
```

`zassert_*` interrompe o teste, `zexpect_*` registra e continua, `zassume_*` pula o teste quando a premissa não vale; `ZTEST_F` usa fixture; `ZTEST_P` é parametrizado (V-36). Teste inaplicável: `ztest_test_skip()` ou `Z_TEST_SKIP_IFDEF`. Execução só de host: `west twister -p unit_testing -T <pasta do teste>`; `--seed` reproduz a ordem embaralhada; `--device-testing` grava placa e é Gate. O `testcase.yaml` com `type: unit` define a categoria; releia a página da versão antes de escrever o arquivo (V-36).

## ESP-IDF

Teste em alvo com Unity (V-38): arquivo `test_*.c` no componente de teste, `unity` em `REQUIRES`.

```c
#include "unity.h"
#include "rb.h"

TEST_CASE("rb pop on empty fails", "[rb]")
{
    rb_t r; uint8_t store[4], v = 0xAA;
    rb_init(&r, store, sizeof store);
    TEST_ASSERT_EQUAL_INT(-1, rb_pop(&r, &v));
    TEST_ASSERT_EQUAL_UINT8(0xAA, v);
}
```

Pontos (V-38): testes em host Linux usam mocks (CMock) e só alguns componentes suportam; `TEST_CASE_MULTIPLE_DEVICES` (até cinco DUTs) e `TEST_CASE_MULTIPLE_STAGES` (etapas que atravessam reset, por exemplo o motivo do reset após deep sleep); prefira macros de capacidade de `soc_caps.h` a nomes de chip; para CI a página recomenda pytest-embedded 2.x com serviços `serial`, `esp`, `idf`, `qemu` e `wokwi`, fixture `dut` com `expect`; fixe `pytest-embedded~=2.0`. O serviço `idf` **grava o binário na placa** automaticamente: Gate. Os serviços `qemu` e `wokwi` rodam em emulação sem gravar placa física (Inferido; confirme na documentação). Se a lógica é pura, prefira o caso de host: mais rápido e sem gate.

## PlatformIO

`platformio.ini` com ambiente de host (V-57: testes rodam no host `native`, na placa ou nos dois; frameworks Doctest, GoogleTest, Unity e Custom):

```ini
[env:native]
platform = native
test_framework = unity

[env:board]
platform = <plataforma da placa>
board = <placa>
framework = <framework>
```

Comandos: `pio test -e native` (só host). Sem `-e native`, `pio test` roda também em ambientes de placa e pode gravar (Gate). Análise: `pio check --fail-on-defect high --skip-packages` (Cppcheck é a ferramenta padrão; por padrão só `src_dir` e `include_dir` são checados; confira as severidades aceitas na versão instalada, Inferido).

## Rust com falso de embedded-hal

Driver genérico sobre `embedded_hal::i2c::I2c` (1.0.0 na leitura de 2026-10-10; V-47) testa-se no host com um tipo que implementa o trait. Requer `cargo test --target <triplo do host>` com `.cargo/config.toml` sem runner `probe-rs` (ver [runners-que-gravam.md](runners-que-gravam.md)). Inferido: confirme a API do crate na versão fixada.

```rust
use embedded_hal::i2c::{ErrorKind, ErrorType, I2c, NoAcknowledgeSource, Operation};

struct FakeI2c { fail: Option<ErrorKind>, reply: [u8; 2], last_addr: u8 }

impl ErrorType for FakeI2c { type Error = ErrorKind; }

impl I2c for FakeI2c {
    fn transaction(&mut self, address: u8, ops: &mut [Operation<'_>]) -> Result<(), Self::Error> {
        self.last_addr = address;
        if let Some(e) = self.fail { return Err(e); }
        for op in ops.iter_mut() {
            if let Operation::Read(buf) = op {
                let n = buf.len().min(2);
                buf[..n].copy_from_slice(&self.reply[..n]);
            }
        }
        Ok(())
    }
}

#[test]
fn nack_is_propagated_and_value_untouched() {
    let i2c = FakeI2c { fail: Some(ErrorKind::NoAcknowledge(NoAcknowledgeSource::Address)),
                        reply: [0, 0], last_addr: 0 };
    let mut dev = SensorX::new(i2c);
    assert!(dev.read_raw().is_err());
}
```

O crate `embedded-hal-mock` oferece falsos prontos; licença e versão a conferir antes de adotar (Não verificável nesta rodada).

## Falso de driver em C com injeção de erro

Interface `i2c_bus_t` de `datasheet-first`; o falso tem uma fila de respostas e registra o que foi pedido.

```c
typedef struct {
    bus_status_t status[8];  size_t n_status;   size_t i;       /* resposta por chamada */
    uint8_t      rx[8][4];   uint8_t rx_len[8];                  /* bytes devolvidos */
    uint32_t     seen_timeout[8];  uint8_t seen_addr[8];  size_t calls;
} fake_bus_t;

static bus_status_t fake_write_read(void *ctx, uint8_t a, const uint8_t *tx, size_t txl,
                                    uint8_t *rx, size_t rxl, uint32_t timeout_ms)
{
    fake_bus_t *f = ctx;  (void)tx;  (void)txl;
    size_t k = f->i < f->n_status ? f->i : f->n_status - 1;     /* repete a última resposta */
    f->seen_timeout[f->calls % 8] = timeout_ms;  f->seen_addr[f->calls % 8] = a;  f->calls++;  f->i++;
    if (f->status[k] != BUS_OK) { return f->status[k]; }
    for (size_t j = 0; j < rxl && j < f->rx_len[k]; j++) { rx[j] = f->rx[k][j]; }
    return BUS_OK;
}
```

Testes que ela habilita: erro propagado sem tocar a saída; limite de tentativas (`calls` não passa do máximo); timeout recebido igual à constante com fonte; recuperação depois de um NACK seguido de sucesso.
