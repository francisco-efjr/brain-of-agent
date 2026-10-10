# Comandos que parecem de host e gravam a placa

Uso: pré-checagem da skill `firmware-test-host` e do agente `firmware-test-engineer`. Fontes lidas em 2026-10-10: V-38 (o serviço `idf` do pytest-embedded grava o binário automaticamente), V-51 (`west flash`, `west debug` e `--erase` gravam), V-55 (probe-rs: `download`, `flash`, `erase`, `reset` e escrita de memória escrevem; `run` grava antes de abrir o RTT; `cargo-flash` e `cargo-embed`), V-57 (PlatformIO: testes no host `native`, na placa ou nos dois), V-62 e V-21 (classificação de risco: gravar, apagar, resetar e escrever memória são de alto risco). A combinação de cada um com o **seu** projeto (runner configurado, ambientes) é Inferido: confira no repositório. Esta tabela mantém a regra do plugin: gravar, apagar, resetar, escrever memória e acionar atuador exigem confirmação explícita no chat.

Sumário: [Tabela](#tabela) · [Como conferir antes de rodar](#como-conferir-antes-de-rodar) · [Alternativas seguras](#alternativas-seguras) · [Se o comando gravaria](#se-o-comando-gravaria)

## Tabela

| Comando | Por que pode gravar | Como saber no projeto | Alternativa só de host |
| --- | --- | --- | --- |
| `cargo test`, `cargo run` | Se `.cargo/config.toml` define `runner = "probe-rs run ..."` ou o `target` padrão é cruzado, o executável é enviado ao chip (V-55, Inferido) | ler `.cargo/config.toml` (e `~/.cargo/config.toml`): chaves `[build] target`, `[target.*] runner` | `cargo test --target <triplo do host>` (`rustc -vV` mostra `host:`); falsos de `embedded-hal` |
| `cargo flash`, `cargo embed` | grava por definição (V-55) | n/a | não usar em teste de host |
| `probe-rs run`, `probe-rs download`, `erase`, `reset`, escrita de memória | gravam ou alteram o alvo; `run` grava antes de abrir o RTT (V-55) | n/a | ler símbolos e logs offline |
| `west twister --device-testing` | executa teste em placa conectada, com gravação | flags do comando e `--device-serial`/mapa de hardware | `west twister -p unit_testing` ou `native_sim` em Linux (V-36) |
| `west flash`, `west debug`, `--erase` | gravam; `--erase` apaga a flash antes (V-51) | n/a | `west build` apenas compila |
| `pio test` (sem `-e`) | roda em todos os ambientes do `platformio.ini`, inclusive placas, com upload (Inferido) | ambientes definidos em `platformio.ini` e `test_*` | `pio test -e native` (V-57) |
| `pio run -t upload`, `-t uploadfs`, `-t erase` | gravam | n/a | `pio run` sem alvo apenas compila |
| `idf.py flash`, `app-flash`, `erase-flash`, `erase-otadata` | gravam e apagam | n/a | `idf.py build`, `idf.py size` |
| `pytest ... --embedded-services idf` / serviço `idf` do pytest-embedded | grava o binário automaticamente (V-38) | opções de linha de comando, `pytest.ini`, `conftest.py` | `--embedded-services` com `qemu` ou `wokwi` sem placa física (Inferido, confirme na documentação) ou teste de host |
| `idf.py monitor`, monitor serial genérico | abrir a porta pode resetar o alvo via DTR/RTS (Inferido) | opções do monitor (`--help`) | ler log já capturado |
| `esptool`, `openocd ... program`, `JLinkExe`, `st-flash`, `nrfjprog`, `avrdude`, `dfu-util`, `mcumgr` | gravam, apagam ou enviam imagem | n/a | não usar |
| `ceedling test:all`, `ctest`, `make test` | normalmente host; um Makefile ou configuração personalizada pode chamar gravador | ler o alvo `test` do Makefile/`CMakeLists.txt`/`project.yml` | rodar só se a leitura confirmar host |

## Como conferir antes de rodar

1. `grep -n "runner\|target" .cargo/config.toml` (e o arquivo do usuário no diretório home, se existir). Se aparecer `probe-rs`, `cargo-embed` ou um alvo cruzado como padrão, o `cargo test` simples grava.
2. `grep -n "^\[env" platformio.ini` e `grep -n "test_\|upload" platformio.ini`: veja que ambientes existem e que `-e native` existe.
3. `grep -rn "device-testing\|embedded-services\|flash" .github tests Makefile CMakeLists.txt 2>/dev/null` para achar chamadas de gravação escondidas em CI ou em scripts de teste.
4. Leia o alvo de teste em `Makefile`/`CMakeLists.txt`/`project.yml` (Ceedling) antes de executar.
5. Confirme o **alvo de host explícito** na linha que vai rodar; nunca confie no padrão.
6. Em dúvida, trate como Gate: peça confirmação no chat com o comando exato e diga o que ele grava.

## Alternativas seguras

- Compilar sem gravar: `cmake --build`, `ninja`, `make`, `idf.py build`, `west build`, `pio run` (sem alvo), `cargo build`.
- Testar lógica no host: Unity/CMock/Ceedling, `unit_testing` e `native_sim` do Zephyr (Linux), PlatformIO `native`, `cargo test --target <host>`.
- Verificar sem rodar: `size`, `.map`, `-fstack-usage`, `clang-tidy`, `cppcheck`.
- Emulação: QEMU/Wokwi quando o framework a suporta (serviços do pytest-embedded; V-38); é "simulado", nível de evidência diferente de "em hardware".

## Se o comando gravaria

Pare, devolva ao agente principal (ou ao usuário) o comando exato e o que ele grava, e use `/systems-embedded-iot:hw-bench-loop`: cartão de gravação, confirmação, registro. No agente `firmware-test-engineer`: "se um comando gravar, apagar, resetar ou escrever memória do dispositivo, ou acionar atuador, pare e devolva o pedido ao agente principal com o comando exato; não execute".
