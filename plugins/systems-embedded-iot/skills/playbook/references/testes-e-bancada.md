# Testes de firmware e bancada

Fontes lidas em 2026-10-10: V-02, V-03, V-19, V-20, V-21, V-27, V-29, V-36, V-37, V-38, V-57, V-62 (ver `fontes.md`). A pesquisa não executou nenhum desses frameworks; sintaxes de arquivos de configuração (por exemplo `testcase.yaml`) devem ser relidas na versão instalada. Rótulos: Verificado, Inferido, Suposição, Não verificável.

Sumário: 1. Camadas de teste · 2. Zephyr (ztest, Twister) · 3. Unity, CMock, Ceedling · 4. ESP-IDF e pytest-embedded · 5. PlatformIO · 6. Rust · 7. HIL e runners que gravam · 8. Casos de borda de firmware · 9. Sessões longas e `features.json` · 10. Ferramenta de bancada para agente · 11. Loop de bancada com gate · 12. Níveis de evidência.

## 1. Camadas de teste (qual camada para qual risco)

| Camada | Roda onde | Serve para | Não prova |
| --- | --- | --- | --- |
| Domínio puro (parser, máquina de estados, buffer circular, CRC) | host (`unit_testing`, Unity, PlatformIO `native`, `cargo test` no host) | Lógica e casos de borda, rápido e determinístico | Temporização, periférico, interrupção real |
| Driver com HAL falsa | host (mock/stub) ou `native_sim` | Sequência de chamadas, tratamento de erro injetado (NACK, timeout) | Comportamento elétrico do sensor |
| Periférico, tempo, DMA, energia | alvo ou HIL | Comportamento real | Cobertura ampla (lento, exige bancada) |

Princípio P-03: separe o domínio do hardware atrás de uma interface (um header), para que a camada barata cubra a maior parte da lógica (V-16, V-36, V-37).

## 2. Zephyr: ztest e Twister (V-36)

- `ZTEST_SUITE` com predicate, setup, before, after e teardown; `ZTEST`, `ZTEST_F` (fixture), `ZTEST_P` (parametrizado), `ZTEST_USER`.
- `zassert_*` interrompe o teste; `zexpect_*` registra e continua; `zassume_*` pula.
- `native_sim` constrói o SO completo para o host; `unit_testing` constrói só o código testado e o Ztest (`type: unit`) e funciona **só em Linux** ("Running unit tests is therefore only supported for Linux"). Em Windows ou macOS, rode em WSL, container ou VM Linux (K-08, Inferido para o ambiente).
- Twister com `--seed` reproduz a ordem embaralhada (o embaralhamento imprime a seed; a página não diz que `--seed` exige `CONFIG_ZTEST_SHUFFLE`).
- Teste inaplicável usa `ztest_test_skip()` ou `Z_TEST_SKIP_IFDEF`: **skipped, não omitido**.
- **`west twister --device-testing` grava a placa**: gate.
- Não cite a sintaxe do `testcase.yaml` sem reler a versão.

## 3. Unity, CMock, Ceedling (V-37, MIT)

- Unity: asserções de inteiros de largura fixa, hex, arrays, floats, strings, ponteiros, memória e variantes `_MESSAGE`.
- CMock gera mocks de headers C e funciona com Unity; **exige Ruby** (confirmado pela página de unit tests do ESP-IDF). O zip do CMock exige Unity e CException.
- Ceedling une Unity e CMock; `ceedling new --local` copia Unity, CMock e CException em `vendor/`; README cita 1.1.10 (sem data). Ceedling com toolchain cruzado: Inferido, confira a documentação de configuração.

Padrão "HAL falsa no host": a interface do driver é um header (`hal_i2c.h`); o CMock gera `mock_hal_i2c.c`; o teste verifica a sequência de chamadas e injeta retornos de erro. Exemplo (Unity + CMock, ilustrativo; nomes de função gerados dependem da configuração do CMock):

```c
void test_sensor_read_returns_error_on_nack(void)
{
    hal_i2c_write_read_ExpectAndReturn(0x48, reg_temp, 1, NULL, 2, HAL_ERR_NACK);
    hal_i2c_write_read_IgnoreArg_rx();

    TEST_ASSERT_EQUAL_INT(SENSOR_ERR_BUS, sensor_read_temp(&dev, &out));
    TEST_ASSERT_FALSE_MESSAGE(dev.valid, "leitura invalida nao pode ficar marcada como valida");
}
```

Regra: uma asserção por comportamento, com mensagem própria quando o caso não é óbvio. Endereço `0x48` e o nome `reg_temp` aqui são placeholders do exemplo, não fatos de um sensor (P-02).

## 4. ESP-IDF e pytest-embedded (V-38)

- Testes em alvo usam Unity: `TEST_CASE("nome", "[modulo]")` em arquivos `test_*.c`, com `unity` em `REQUIRES`.
- Testes no host Linux usam mocks (CMock); só alguns componentes suportam.
- `TEST_CASE_MULTIPLE_DEVICES` (até cinco DUTs) e `TEST_CASE_MULTIPLE_STAGES` (etapas que atravessam reset, como motivo do reset após deep sleep).
- Prefira macros de capacidade de `soc_caps.h` a nomes de chip.
- A página recomenda **pytest-embedded** para CI. Versão 2.x: serviços `serial`, `esp`, `idf` (**grava o binário automaticamente**), `qemu` e `wokwi`; fixture `dut` com `expect`; fixe `pytest-embedded~=2.0`. A página não declara licença nem usa o termo HIL; HIL é o uso com o serviço `idf` e placa real (Inferido).
- Definição de pronto de teste ESP-IDF: caso de host (mock) para a lógica; caso em alvo para periférico; caso multi-estágio para sleep e reset; CI com pytest-embedded; **rodar em placa exige confirmação**.

## 5. PlatformIO (V-57)

- Testes rodam no host (`native`), na placa ou nos dois; frameworks: Doctest, GoogleTest, Unity, Custom. **`pio test` sem `-e native` pode gravar na placa** (Inferido; `pio test` não foi lido).
- `pio check`: Cppcheck é a ferramenta padrão; opções `-e`, `-f/--src-filters`, `--flags`, `--severity`, `--json-output`, `--fail-on-defect`, `--skip-packages`, `-s`, `-v`; por padrão só `src_dir` e `include_dir`; sem `--fail-on-defect` o código de saída é o da ferramenta. Em CI: `pio check --fail-on-defect high --skip-packages` (confira as severidades aceitas na versão instalada: Inferido).
- `pio run -t upload` e `-t uploadfs` gravam: gate.

## 6. Rust (Inferido, sem fonte própria)

`cargo test --target <triplo do host>` com fakes dos traits do `embedded-hal` (V-47). Antes de rodar, confira `.cargo/config.toml`: um `runner` de `probe-rs` ou `target` cruzado padrão faz o teste gravar a placa (V-55). Testes em alvo com `probe-rs` seguem o gate.

## 7. HIL e runners que gravam

| Runner | Grava? | Fonte |
| --- | --- | --- |
| `west flash`, `west debug`, `west twister --device-testing` | sim | V-51, V-36 |
| `idf.py flash`, serviço `idf` do pytest-embedded | sim | V-38 |
| `pio run -t upload`, `pio test` sem `-e native` | sim (Inferido para `pio test`) | V-57 |
| `probe-rs download/flash/erase/reset/write-mem/run`, `cargo flash/embed` | sim | V-55 |
| `cargo run/test` com `runner = probe-rs ...` | sim, não detectável por texto | Inferido |
| `probe-rs list/info/read-mem/rtt` | não (leitura) | V-55 |

Antes de rodar qualquer coisa que pareça de host, leia o runner e use o alvo de host explícito. Cartão de gravação e confirmação no chat para as linhas "sim".

## 8. Casos de borda de firmware (peça-os em todo plano)

Overflow e underflow de buffer circular; wrap de contador de tempo (`uint32_t` de milissegundos dá a volta em cerca de 49,7 dias, aritmética estável de 32 bits) comparando diferenças e não valores absolutos; erro de barramento injetado (NACK, timeout) e recuperação; reconexão de rede e backoff; ordem de chamadas do mock; ponteiro nulo ou comportamento documentado; valores-limite de inteiros de largura fixa; reset no meio de uma gravação de configuração (consistência da NVS, Inferido); acordar do deep sleep com o motivo de reset correto (caso multi-estágio).

## 9. Sessões longas: `features.json` e progresso (V-02)

- Dois papéis: inicializador (cria ambiente, `init.sh`, lista de funcionalidades, primeiro commit) e codificação (uma funcionalidade por sessão).
- Lista de funcionalidades em **JSON** em que o agente só altera o campo `passes` (o modelo altera menos JSON do que Markdown). Template: `assets/templates/features.json` e `assets/templates/progresso.md`.
- Regra do plugin (Suposição de design): `passes` só vira `true` com saída de teste de host ou log de bancada anexado em `evidencia`; sessão começa com orientação (git log, progresso), build e smoke test; termina em estado limpo e commitado.
- Ressalva da fonte: o exemplo original é web; a Anthropic lista como questão aberta se o padrão generaliza. Em firmware, o teste de ponta a ponta exige bancada e autorização.

## 10. Ferramenta de bancada para agente: checklist (V-03, V-20, V-19)

Antes de entregar a um agente um script de build, gravação, log ou teste:

1. A saída padrão é curta? (a fonte diz "poucas linhas"; 20 linhas é Suposição da fábrica).
2. Erro tem prefixo fixo e motivo **na mesma linha** (`ERROR <motivo>`)?
3. O log completo vai para um caminho fixo?
4. Existe modo rápido determinístico (amostra fixa por seed)?
5. Existe oráculo de referência (por exemplo, build de host x build de alvo, delta debugging)?
6. Rápida e silenciosa por padrão, com botão de verbosidade; pidfile contra segunda instância (V-20).
7. Timeout em toda espera e exit code não zero em falha: **Suposição de design da fábrica** (as fontes não tratam de timeout nem exit code; não as atribua a Ronacher nem a Bitcraze).
8. Operação que escreve no dispositivo classificada como alto risco e atrás de confirmação; `.bin` exige endereço; ambiguidade de projeto/probe/porta lista candidatos e para (V-21).
9. Resultado por estágio em JSON (`stage`, `ok`, `backend`, `error`, `next_commands`): campos são Suposição da fábrica.

Contexto: Carlini (V-03) relata cerca de 2.000 sessões e US$ 20 mil com 16 agentes num compilador, e alerta que passar nos testes raramente prova que acabou e que software autônomo sem verificação humana traz riscos reais. Para hardware, isso reforça o gate e o "humano no circuito" (Bitcraze, V-19).

## 11. Loop de bancada com gate (resumo; fluxo completo na skill `hw-bench-loop`)

Compilar (livre) -> cartão de gravação -> confirmação no chat -> gravar -> observar (console, log, RTT) -> comparar -> corrigir, com registro em `assets/templates/registro-evidencias-bancada.md`. Regras: alvo e probe/porta inequívocos; chip informado (nunca adivinhar); `.bin` com endereço; caminho de recuperação confirmado; leitura de verificação quando houver; irreversíveis são recusados e encaminhados a `ota-security-review`; pare após três ciclos sem progresso; ao final, liste o que ficou gravado na placa (V-21, V-27, V-62).

Observar também pode alterar a placa: abrir um monitor serial pode resetar o alvo (DTR/RTS; Inferido) e `probe-rs run` grava antes do RTT (V-55). Pare sessões de depuração antes de gravar; nunca `uhubctl` na porta raiz do uplink, nunca `gh auth login` (V-61). A API HTTP da bancada do SensorsIot não tem autenticação (V-29): só em rede confiável.

## 12. Níveis de evidência

| Nível | Significa | Pode afirmar |
| --- | --- | --- |
| Compilado | Build/cross-build passou | "compila com <toolchain e versão>" |
| Analisado | clang-tidy, cppcheck, sanitizers no host | "sem achados da ferramenta X em Y" |
| Testado no host | Unity/ztest/`native` rodou | "domínio passa N casos" |
| Simulado | QEMU, `native_sim`, Wokwi | "comportamento em simulador" |
| Em hardware | Rodou na placa X revisão Y, com saída colada | "funciona na bancada nas condições Z" |

Mapa para rótulos da casa (V-27): confirmado = Verificado; inferência de engenharia = Inferido; estimativa e a verificar = Suposição; dados insuficientes = Não verificável. Resultado negativo também é registrado, com versão da ferramenta, comando e log. Especificação citada pelo usuário vale "a verificar".
