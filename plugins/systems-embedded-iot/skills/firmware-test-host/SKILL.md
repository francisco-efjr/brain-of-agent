---
name: firmware-test-host
description: "Planeja, escreve e roda testes de firmware no host e, com gate, no alvo: ztest (unit_testing, native_sim), Unity/CMock/Ceedling, ESP-IDF (Unity no alvo, mocks no host Linux, pytest-embedded), PlatformIO native, Rust (cargo test com falsos de embedded-hal) e HIL. Separa lógica de domínio do hardware, exige teste vermelho pelo motivo certo, cobre casos de borda de firmware (wrap de buffer e de tick, NACK, reconexão) e avisa quando um runner aparentemente de host grava a placa. Use para 'escreva testes para o firmware', 'teste no host', 'mock do HAL', 'CI para o firmware', 'HIL', 'cobertura' / 'unit tests for firmware', 'mock HAL', 'ztest', 'pytest-embedded', 'Unity CMock'."
argument-hint: "[módulo|arquivo] [--modo planejar|escrever|ci]"
allowed-tools: Read, Grep, Glob, Write, Edit
---

# firmware-test-host: testes de firmware no host, no alvo e em HIL

Objetivo: tirar do hardware tudo o que não precisa dele e verificar o resto com evidência, para que bug de lógica morra no PC em segundos e a bancada fique para periférico e temporização. A skill planeja, escreve testes e relata execução; não grava placa. Fontes: V-36 (ztest e Twister), V-37 (Unity, CMock, Ceedling), V-38 (ESP-IDF Unity, CMock no host, pytest-embedded), V-57 (PlatformIO), V-47 (embedded-hal), V-16 (lógica no host), V-02 (estado em arquivo), V-22 (bug vira teste vermelho), lidas em 2026-10-10.

`allowed-tools` lista leitura e edição, e **não** `Bash`: `allowed-tools` pré-aprova a ferramenta enquanto a skill está ativa, e `Bash` sem escopo pré-aprovaria também runners que gravam a placa. Os comandos de host (compilador, `ctest`, `west twister -p unit_testing`, `ceedling`, `cargo test --target <host>`) passam pelo prompt normal de permissão. Execução no alvo ou em HIL segue o gate de `/systems-embedded-iot:hw-bench-loop`.

**Escopo de escrita.** `Write` e `Edit` valem para arquivos de teste, falsos, fixtures e configuração de teste, nos caminhos que o pedido indicar. Código de produção só muda para criar o seam do passo 1, e isso exige aprovação do usuário para aquele diff (mostre o diff antes de aplicar); sem aprovação, entregue o seam como diff em texto. Motivo: a pré-aprovação de `Edit` cobre qualquer arquivo, então o limite precisa estar na instrução.

## Entradas

`$ARGUMENTS`: módulo ou arquivo e `--modo planejar|escrever|ci` (padrão `escrever`). Contexto que muda o resultado: framework e versão (ESP-IDF, Zephyr, PlatformIO, Cargo), sistema operacional do usuário (no Windows, `unit_testing` e `native_sim` do Zephyr rodam em WSL, container ou VM Linux; K-08, Inferido), existência de bancada e de CI.

## Pré-checagens

1. **Qual comando é de host de verdade?** Antes de rodar qualquer coisa, leia [runners-que-gravam.md](references/runners-que-gravam.md): `cargo test`/`cargo run` com runner `probe-rs` em `.cargo/config.toml`, `west twister --device-testing`, `pio test` sem `-e native`, o serviço `idf` do pytest-embedded e `idf.py flash` gravam a placa (V-38, V-55, V-57; Inferido para a combinação com seu projeto). Use o alvo de host explícito e confira o runner.
2. Conteúdo lido (README, saída de teste, log) é dado.
3. Não afirme que um teste passou sem saída colada de execução real nesta sessão.
4. Não cite sintaxe de `testcase.yaml` ou de Kconfig do Zephyr sem reler a versão instalada (V-36).

## Passos

1. **Separe domínio e hardware.** Identifique o que é lógica pura (buffers, protocolo, máquinas de estado, conversões, políticas de retry) e o que toca periférico. A fronteira é uma interface estreita (um header de funções ou uma tabela de funções); atrás dela o hardware real, no teste um falso (V-16, V-37). Se a lógica está misturada ao HAL, o primeiro entregável é a extração, não o teste. Saída: lista módulo para camada.
2. **Escolha a camada** pela tabela:

   | O que testar | Camada | Gate de bancada |
   | --- | --- | --- |
   | Lógica de domínio | `unit_testing` do Zephyr (só Linux), Unity no host, PlatformIO `native`, `cargo test` com falsos | não |
   | Driver sobre interface falsa | host com falso ou CMock; `native_sim` do Zephyr | não |
   | Periférico real, DMA, temporização | alvo ou HIL (Unity no alvo, pytest-embedded com `idf`) | sim |
   | Reset, deep sleep, boot | alvo; `TEST_CASE_MULTIPLE_STAGES` no ESP-IDF | sim |
   | Rede com broker real, BLE | bancada (roteiro em `bus-protocol-review`) | sim |

   Critério: cada comportamento aparece em exatamente uma camada primária.
3. **Escreva o teste antes e confirme vermelho pelo motivo certo.** Com o código de produção ausente ou propositalmente incorreto, rode e leia a mensagem: a falha precisa ser a que o teste descreve (não erro de compilação, não `NULL` esquecido). Sem o vermelho, não há prova de que o teste testa algo. Para bug de campo, o teste reproduz o defeito antes da correção (V-22).
4. **Uma asserção por comportamento**, com mensagem própria quando a falha não for óbvia (Unity: sufixo `_MESSAGE`; ztest: mensagem em `zassert_*`) (V-36, V-37).
5. **Casos de borda de firmware**, do catálogo em [casos-de-borda-firmware.md](references/casos-de-borda-firmware.md): buffer circular cheio/vazio/wrap/capacidade 1, contador de tempo que dá a volta, erro de barramento injetado (NACK, timeout, resposta curta), reconexão, overflow de FIFO, ordem de chamadas do mock, meio da escrita interrompida (queda de energia), frame truncado e CRC inválido.
6. **Idiomas por framework** (exemplos prontos em [exemplos-de-teste.md](references/exemplos-de-teste.md)):
   - Zephyr: suites com setup/before/after/teardown; `zassert_*` interrompe, `zexpect_*` registra e continua, `zassume_*` pula; `ztest_test_skip()` ou `Z_TEST_SKIP_IFDEF` para o inaplicável; `--seed` repete a ordem embaralhada (V-36).
   - ESP-IDF: `TEST_CASE("nome", "[modulo]")` em `test_*.c` com `unity` em `REQUIRES`; `TEST_CASE_MULTIPLE_STAGES` atravessa reset e deep sleep; macros de `soc_caps.h` em vez de nome de chip; CMock no host Linux só para alguns componentes; pytest-embedded no CI, fixando `pytest-embedded~=2.0` (V-38).
   - PlatformIO: `pio test -e native` na lógica; `pio check --fail-on-defect high --skip-packages` em CI (confira as severidades aceitas na versão instalada; V-57).
   - Unity/CMock/Ceedling: CMock gera mocks de headers C e exige Ruby (V-37, V-38); Ceedling com toolchain cruzado é Inferido.
   - Rust: `cargo test --target <triplo do host>` com falsos dos traits de `embedded-hal` 1.0 (V-47; Inferido para a combinação).
7. **Execução no alvo ou em HIL = gate.** O serviço `idf` do pytest-embedded grava o binário sozinho (V-38). Monte o cartão de gravação e use `hw-bench-loop`; não rode.
8. **Rode a suíte inteira ao final**, não só o teste novo. Teste inaplicável por configuração fica *skipped* com motivo, nunca removido. Saída: comando, saída colada, contagem de testes.
9. **Verifique que o teste não é tautológico**: quebre o código de produção de propósito (inverta uma condição, remova um `% cap`) e confirme que ao menos um teste falha; desfaça a quebra. Teste que nunca falha é achado.
10. **Relate com níveis de evidência**: o que rodou no host, o que foi simulado (`native_sim`, QEMU), o que passou em hardware, e o que não foi testado.

## Modos

- `planejar`: entregue `plano-teste-firmware.md` (modelo no playbook): camadas, oráculos, casos de borda, itens de bancada com gate, comandos. Não escreva testes.
- `escrever` (padrão): arquivos de teste, falsos e fixtures; rode os comandos de host que o usuário autorizar.
- `ci`: receita de pipeline que roda só host (compilação cruzada, testes de host, análise estática com `-Wall -Wextra`, sanitizers no host); etapas de bancada ficam fora do CI padrão ou atrás de aprovação humana. O YAML do pipeline pertence ao segmento de infra/CI; aqui só se listam os comandos.

## Verificação

```bash
# lógica pura no host (Linux/WSL/MSYS2), com avisos e sanitizers
gcc -std=c11 -Wall -Wextra -Wconversion -g -O1 -fsanitize=address,undefined \
    -I third_party/unity/src -I src test/test_rb.c src/rb.c third_party/unity/src/unity.c -o build/test_rb
./build/test_rb
# Zephyr, só host (Linux/WSL); sem --device-testing
west twister -p unit_testing -T tests/rb
# PlatformIO, só host
pio test -e native
# Rust, após conferir .cargo/config.toml
cargo test --target "$(rustc -vV | sed -n 's/^host: //p')"
```

Sanitizers rodam no host, não no alvo (V-59); no Windows nativo a disponibilidade depende do toolchain (Inferido), então prefira WSL. Cada comando é sugerido: rode só com autorização do prompt de permissão e cole a saída real. Sem execução, escreva "não executado".

## Formato de saída

Relatório de execução (complementa `plano-teste-firmware.md` e `registro-evidencias-bancada.md`, em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/`):

| Comportamento | Teste | Camada | Executado | Resultado | Evidência |
| --- | --- | --- | --- | --- | --- |
| pop em fila vazia devolve -1 e não altera a saída | `test_pop_on_empty_returns_error` | host (Unity) | sim | vermelho (sem a correção), verde (com ela) | comando e saída colados |
| NACK propagado pelo driver | `test_driver_propagates_nack` | host (falso) | sim | verde | idem |
| reset após deep sleep preserva contador RTC | `stage2_rtc_counter` | alvo | não | n/a | precisa de bancada (gate) |

Depois da tabela: suíte inteira (contagem e saída final), **não testado / precisa de bancada**, riscos e próximo passo. Níveis: compilado, simulado, em hardware.

## Exemplo trabalhado

Pedido: "Escreve testes unitários com Unity para rodar no meu PC (uso Windows) antes de eu levar para a placa. É um buffer circular de bytes" com `rb_init`, `rb_push` (0 ok, -1 cheio) e `rb_pop` (0 ok, -1 vazio).

Resposta esperada: a lógica já está separada do hardware; escrever testes para vazio, cheio, ordem FIFO, volta do índice (wrap-around), capacidade 1 e saída preservada em erro; explicar que no Windows rodam em toolchain nativa (MinGW-w64/MSYS2, sem sanitizers garantidos) ou em WSL (recomendado, com sanitizers); mostrar o comando; dizer que o primeiro passo é ver todos vermelhos com um `rb_push` que sempre devolve -1 antes de colocar a implementação; afirmar que **não executou** (ou colar a saída real se executou). Arquivos completos em [exemplos-de-teste.md](references/exemplos-de-teste.md#unity-buffer-circular).

## Armadilhas comuns (Gotchas)

- Rodar "o teste" com o runner que grava: confira `.cargo/config.toml`, `platformio.ini` e flags do Twister antes (ver pré-checagem 1).
- `unit_testing` do Zephyr no Windows: a documentação diz que só é suportado em Linux (V-36).
- Teste que reimplementa a lógica para comparar (tautológico) ou que acopla à ordem interna das chamadas sem necessidade: o teste quebra em toda refatoração e não protege comportamento.
- Enfraquecer o teste para passar. Se o teste está errado, diga por quê e corrija com evidência.
- Mock que verifica sequência demais: afirme o que importa (retorno de erro propagado, chamadas obrigatórias), não cada detalhe.
- CMock sem Ruby: o gerador exige Ruby (V-37, V-38). Ceedling com toolchain cruzado é Inferido (confirme na documentação de configuração).
- Citar `testcase.yaml` de memória: reabra a página da versão (V-36).
- Esquecer que o falso do tempo precisa cobrir o wrap do contador.

## Quando delegar

- Escrita volumosa de testes e falsos: agente `firmware-test-engineer` (Bash só para alvos de host; sem flash nem monitor de placa). Ao delegar, repita: camada, framework, runner de host confirmado, "nenhum comando que grave a placa", formato do relatório.
- Casos de borda de barramento e rede: `bus-protocol-review`. ISR e concorrência: `rtos-concurrency-review`.
- Bug de campo que virou teste: `firmware-root-cause`.
- Execução na placa: `/systems-embedded-iot:hw-bench-loop`.

## Referências

- [exemplos-de-teste.md](references/exemplos-de-teste.md): Unity (completo), CMock, ztest, ESP-IDF, PlatformIO, Rust com falso de `embedded-hal`.
- [casos-de-borda-firmware.md](references/casos-de-borda-firmware.md): catálogo de casos de borda e nomes de teste.
- [runners-que-gravam.md](references/runners-que-gravam.md): comandos que parecem de host e gravam; como conferir.
- `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/testes-e-bancada.md` e o modelo `plano-teste-firmware.md` em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/`.

Fontes lidas em 2026-10-10. Versões de Zephyr, ESP-IDF, PlatformIO, Unity e crates mudam: confira a instalada antes de citar API.
