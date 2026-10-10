# Fontes e bibliografia - Sistemas, embarcados e IoT

Todas as consultas foram feitas em 2026-10-10 pela fábrica dev-segments (leitura por ferramenta de busca e fetch; nada baixado nem executado). Classe: A = documentação oficial, norma ou engenharia do mantenedor; B = repositório, blog ou autor reconhecido; C = sinal de comunidade ou repositório pequeno (auto-declarado). Nota entre parênteses = nota 0-10 da rubrica de fontes. "Destilar" = o plugin usa redação própria, sem texto literal. Itens `V-nn` remetem ao consolidado de pesquisa da fábrica; as ressalvas de cada item foram levadas ao arquivo temático indicado.

Sumário: 1. Top 20 · 2. Demais fontes por tema · 3. Rejeitados e rebaixados · 4. Licenças e atribuições · 5. Lacunas · 6. Como conferir versões.

## 1. Top 20 (por utilidade direta e estabilidade)

| # | Título (V-) | URL | Classe | Licença | Por que importa |
| --- | --- | --- | --- | --- | --- |
| 1 | Claude Code best practices (V-01) | https://code.claude.com/docs/en/best-practices | A | n/a (destilar) | CLAUDE.md curto, verificação com evidência, revisão adversarial |
| 2 | Effective harnesses for long-running agents (V-02) | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | A | n/a (destilar) | `features.json` + progresso + git para bring-up e portes |
| 3 | Building a C compiler (V-03) | https://www.anthropic.com/engineering/building-c-compiler | A | n/a (destilar) | Verificador quase perfeito; saída curta de ferramenta |
| 4 | Hooks guide (V-05) | https://code.claude.com/docs/en/hooks-guide | A | n/a (destilar) | Gate de gravação (`PreToolUse`); deny vence em bypass |
| 5 | awesome-cursorrules `embedded-stm32-hal.mdc` (V-16) | https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/embedded-stm32-hal.mdc | B (6) | CC0-1.0 (repositório) | 30 regras de firmware STM32 HAL; usado como destilação reescrita |
| 6 | Zephyr coding guidelines (V-09) | https://docs.zephyrproject.org/latest/contribute/coding_guidelines/index.html | A | n/a (destilar); projeto Apache-2.0 (Inferido) | Checklist de C embarcado sem copiar MISRA |
| 7 | Rust Embedded Book: concorrência e panic (V-12, V-11) | https://docs.rust-embedded.org/book/concurrency/index.html e https://docs.rust-embedded.org/book/start/panicking.html | A | texto CC-BY-SA (Inferido); destilar | Dado compartilhado com interrupção; panic handler |
| 8 | FreeRTOS Kernel Book e `semphr.h`/`stack_macros.h` (V-52, V-15) | https://github.com/FreeRTOS/FreeRTOS-Kernel-Book e https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/semphr.h | B (7) | Book CC BY-SA 4.0 (destilar); kernel MIT | `FromISR`, yield, prioridade máxima de API, overflow de pilha |
| 9 | Zephyr kernel: threads e interrupções (V-49, V-50) | https://docs.zephyrproject.org/latest/kernel/services/threads/index.html e https://docs.zephyrproject.org/latest/kernel/services/interrupts.html | A | n/a (destilar) | Prioridades, pilha medida, ISR x work item |
| 10 | I2C: Zephyr e ESP-IDF (V-30) | https://docs.zephyrproject.org/latest/hardware/peripherals/i2c.html e https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/i2c.html | A | n/a (destilar) | Timeout, NACK, pull-up, ISR, thread safety |
| 11 | CAN no ESP-IDF (TWAI) (V-31) | https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/twai.html | A | n/a (destilar) | Estados de erro, bus-off, filtros |
| 12 | MQTT 3.1.1 e 5.0 (OASIS) (V-33) | https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html e https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html | A | n/a (destilar; padrão OASIS) | Keep alive, will, sessão, QoS, curingas, TLS |
| 13 | MCUboot design e Zephyr (V-24, V-44) | https://docs.mcuboot.com/design.html e https://docs.mcuboot.com/readme-zephyr.html | A | Apache-2.0 (repositório) | Slots, swap, assinatura, custódia de chave, downgrade |
| 14 | ESP-IDF Secure Boot v2 e OTA (V-45, V-46) | https://docs.espressif.com/projects/esp-idf/en/latest/esp32/security/secure-boot-v2.html e https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/ota.html | A | n/a (destilar) | Portão de produção, rollback, anti-rollback |
| 15 | GCC: `-fstack-usage`, `-fanalyzer`, sanitizers (V-59) | https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html , https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html , https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html | A | n/a (destilar) | Orçamento de pilha e análise estática em host |
| 16 | ztest e ESP-IDF unit tests + pytest-embedded (V-36, V-38) | https://docs.zephyrproject.org/latest/develop/test/ztest.html e https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/unit-tests.html | A | n/a (destilar) | `unit_testing` só Linux, `native_sim`, multi-estágio, CI |
| 17 | embeddedskills e embedded-systems-architect (V-21, V-62, V-27) | https://github.com/zhinkgit/embeddedskills e https://github.com/Zachariah9420/embedded-systems-architect | B (6) / C (5) | MIT (ambos) | Gate `operation_mode`, `.bin` exige endereço, níveis de evidência |
| 18 | Beningo: Claude Code para firmware (V-17) | https://www.beningo.com/why-claude-code-for-firmware-development-matters/ | B (6) | não declarada (destilar) | 13 seções de CLAUDE.md de firmware; começar com cerca de 20 linhas |
| 19 | NIST IR 8259A e Rev. 1; ETSI EN 303 645 (V-42, V-43) | https://csrc.nist.gov/pubs/ir/8259/a/final e https://www.etsi.org/deliver/etsi_en/303600_303699/303645/02.01.01_60/en_303645v020101p.pdf | A | NIST: domínio público (Inferido); ETSI: direitos reservados (só título e paráfrase) | Baseline de produto IoT sem copiar norma |
| 20 | gstack `/investigate` (V-22) | https://raw.githubusercontent.com/garrytan/gstack/main/investigate/SKILL.md | B (6) | MIT | Metodologia de causa raiz; não copiar o arquivo (hooks e telemetria) |

## 2. Demais fontes por tema

| V- | Tema | Fonte (URL) | Classe | Licença / observação |
| --- | --- | --- | --- | --- |
| V-04 | Autoria de skills | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md | A | repositório sem licença na API: destilar |
| V-06 | Plugins, manifesto, LSP | https://code.claude.com/docs/en/plugins-reference e https://code.claude.com/docs/en/plugins/code-intelligence | A | destilar; a URL sem `/plugins/` em code-intelligence é 404 |
| V-07 | Marketplace oficial | https://github.com/anthropics/claude-plugins-official | A | Apache-2.0 (página); push Não verificável |
| V-08 | Sandbox | https://www.anthropic.com/engineering/claude-code-sandboxing | A | destilar |
| V-10 | ESP-IDF Style Guide | https://docs.espressif.com/projects/esp-idf/en/latest/esp32/contribute/style-guide.html | A | destilar |
| V-13 | clang-tidy | https://clang.llvm.org/extra/clang-tidy/ | A | destilar |
| V-14 | CERT SIG31-C e MISRA C:2023 (matriz) | https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/signals-sig/sig31-c e https://www.mathworks.com/help/bugfinder/misra-c-2023-reference.html | B (7) | MISRA é paga: nunca reproduzida |
| V-18 | Vetar skills de terceiros | https://snyk.io/articles/claude-skills-embedded-systems-engineers/ | B (5) | blog de vendor; estatísticas (36%, 13%) são da própria Snyk, sem metodologia na página |
| V-19 | Loop de hardware (Bitcraze) | https://www.bitcraze.io/?p=14780 | B (6) | destilar; sintaxe de CLI e exit codes são Suposição da fábrica |
| V-20 | Princípios de ferramenta (Ronacher) | https://lucumr.pocoo.org/2025/6/12/agentic-coding/ | B (6) | destilar; o texto não fala de timeout nem exit code |
| V-23 | Datasheet primeiro (thread HN) | https://news.ycombinator.com/item?id=44915206 | B (5) | relatos; alegações de privacidade do thread não são fato |
| V-25 | Regras operacionais ESP32 | https://github.com/agodianel/esp32-claude-workbench | C (4) | MIT; 79 estrelas; números de pilha/pino não entram |
| V-26 | Auditoria de pinos ESP32 | https://raw.githubusercontent.com/agodianel/esp32-claude-workbench/main/.claude/skills/esp32_pin_audit/SKILL.md | C (4) | destilar com correções da doc ESP-IDF |
| V-28 | ESP32 por contexto de execução | https://raw.githubusercontent.com/johnkozaris/jko-claude-plugins/main/plugins/esp32-cpp/skills/esp32-expert/SKILL.md | C (4) | MIT (11 estrelas); destilar |
| V-29 | Harness com hardware real | https://github.com/SensorsIot/Embedded-AI-Harness | C (4) | MIT; API da bancada sem autenticação; só referência de desenho |
| V-32 | SPI e UART | https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/spi_master.html , .../uart.html , https://docs.zephyrproject.org/latest/hardware/peripherals/uart.html , .../spi.html | A | destilar; API do SPI do Zephyr não lida |
| V-34 | BLE (índices) | https://docs.zephyrproject.org/latest/services/connectivity/bluetooth/index.html e https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/bluetooth/nimble/index.html | B (5) | só decisão de pilha; nenhuma regra de MTU ou segurança |
| V-37 | Unity, CMock, Ceedling | https://github.com/ThrowTheSwitch/Unity , https://github.com/ThrowTheSwitch/CMock , https://github.com/throwtheswitch/ceedling | B (7) | MIT; datas de commit Não verificáveis |
| V-38 | pytest-embedded | https://docs.espressif.com/projects/pytest-embedded/en/latest/ | A | licença não declarada na página |
| V-39 | Sleep modes ESP-IDF | https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/sleep_modes.html | A | destilar |
| V-40 | Power management Zephyr | https://docs.zephyrproject.org/latest/services/pm/index.html | B (5) | "Last source update" abr/2022: referência, não regra |
| V-41 | OWASP IoT, ISVS, FSTM | https://owasp.org/www-project-internet-of-things/ , https://github.com/OWASP/IoT-Security-Verification-Standard-ISVS , https://github.com/scriptingxss/owasp-fstm | B (6) | CC BY-SA 4.0: destilar; ISVS em RC; Top 10 2018 não lido |
| V-47 | embedded-hal 1.0 | https://docs.rs/embedded-hal/latest/embedded_hal/ | A | MIT ou Apache-2.0 |
| V-48 | SVD e svd2rust | https://github.com/rust-embedded/svd2rust e https://open-cmsis-pack.github.io/svd-spec/main/index.html | B (7) | svd2rust Apache-2.0/MIT; página SVD sem licença |
| V-51 | Kconfig e west | https://docs.zephyrproject.org/latest/build/kconfig/tips.html , .../kconfig/index.html , https://docs.zephyrproject.org/latest/develop/west/index.html , .../west/build-flash-debug.html | A | destilar |
| V-53 | Embassy | https://github.com/embassy-rs/embassy e https://embassy.dev/ | B (7) | MIT ou Apache-2.0; docs CC-BY-SA |
| V-54 | RTIC v2 | https://rtic.rs/2/book/en/ e https://docs.rs/rtic/latest/rtic/ | B (7) | licença do livro não declarada |
| V-55 | probe-rs e defmt | https://probe.rs/docs/ e https://defmt.ferrous-systems.com/ | B (7) | licença não declarada nas páginas |
| V-56 | Embedonomicon | https://docs.rust-embedded.org/embedonomicon/ | B (6) | referência de linker/arranque |
| V-57 | PlatformIO | https://docs.platformio.org/en/latest/advanced/unit-testing/index.html e https://docs.platformio.org/en/latest/core/userguide/cmd_check.html | B (7) | destilar |
| V-58 | cppcheck e MISRA | https://cppcheck.sourceforge.io/misra.php | A | destilar |
| V-60 | Safety do Zephyr | https://docs.zephyrproject.org/latest/safety/index.html e .../safety/safety_overview.html | B (6) | IEC 61508 é meta, não certificação |
| V-61 | Skills de bancada SensorsIot | https://github.com/SensorsIot/Embedded-AI-Harness/tree/main/.claude/skills | C (4) | MIT; `sudo`, broker aberto: só destilar |
| V-63 | Config segura para Claude Code | https://github.com/trailofbits/claude-code-config | B (5) | licença não exibida: destilar |
| V-35 | Checklist de barramento e protocolo | síntese própria da fábrica sobre V-30 a V-33 | B (6) | autoria da fábrica |

## 3. Rejeitados e rebaixados (não usar como fonte de regra)

| Item | Decisão | Motivo |
| --- | --- | --- |
| BARR-C:2018 | referência de consulta | licença proíbe postar o PDF; só estrutura de capítulos, sem texto |
| C++ do awesome-cursorrules | rebaixado a sinal (C) | é C++ de desktop (SOLID, `std::filesystem`, exceções); nada de firmware |
| CISA Secure by Design | referência de política | três princípios gerais; não trata de IoT; PDF não lido |
| automotive-claude-code-agents (199 estrelas, MIT) | C (3) | contagens grandes sem resultados de teste (sinal de conteúdo em massa) |
| embedded-ai-workspace | C (3) | auto-declarado sem logs ou métricas |
| esp32-firmware-engineer-skill | só destilação | sem licença; 12 estrelas |
| stm32-mcp | referência de segurança | MIT, 25 estrelas; útil só pela nota "não é sandbox; pode gravar e sobrescrever memória" |
| Ask HN (461 pontos) | C (3) | relatos gerais, não de embarcados |
| awesome-copilot agent-safety | rebaixado | não menciona hardware |
| cpp-language-service-tools, cmake-vcpkg, dev.to ESP32-S3 | rejeitados | dependem de ferramentas específicas, foco em desktop ou sem regra reaproveitável |

## 4. Licenças e atribuições

- brain-of-agent (francisco-efjr, MIT): protocolo do modo completo, handoff, plano de incremento, ADR, registro de evidências, checklist de release, bug report e plano de teste, adaptados em `assets/templates/` e na seção do modo EMBARCADOS-COMPLETO.
- gstack (garrytan, MIT): apenas a metodologia de causa raiz (V-22), destilada com atribuição. Nenhum arquivo copiado; o frontmatter do original traz hooks e telemetria que este plugin não usa.
- awesome-cursorrules (PatrickJS, CC0-1.0): regras STM32 HAL reescritas em seis blocos (V-16). Nenhum trecho literal.
- CC BY-SA (Rust Embedded Book, FreeRTOS Kernel Book, ISVS, FSTM): exigem atribuição e mesma licença para derivados; por isso só destilação com redação própria.
- ETSI EN 303 645: todos os direitos reservados; o plugin usa os títulos das 13 provisões e perguntas próprias. MISRA: paga; nunca reproduzida. NIST: documentos públicos, ainda assim parafraseados.
- Nenhuma fonte de terceiros foi instalada ou executada. Estrelas e licenças vêm de páginas HTML (a API do GitHub recusou, 403); datas de push são Não verificáveis.

## 5. Lacunas conhecidas (declare "Não verificável" em vez de inventar)

1. BLE: MTU, parâmetros de conexão, segurança/pareamento e GATT sem fonte validada (V-34).
2. Energia: guias da Nordic e da ST; Zephyr PM de 2022; "medir corrente como critério de pronto" é prática derivada do ESP-IDF (V-39, V-40).
3. Devicetree do Zephyr; lista de funções "isr-ok"; análise de pilha do Zephyr; API do SPI do Zephyr (Doxygen).
4. C++ moderno de firmware (sem exceções/RTTI, `constexpr`, `std::optional` em freestanding): sem fonte; o plugin só dá orientação Inferida a conferir na documentação da toolchain.
5. Rust `no_std`: nenhum AGENTS.md ou skill com licença clara; `DEFMT_LOG` e `embedded-hal-async` não lidos.
6. Arduino (guia de estilo vazio) e `pio test`.
7. Segurança funcional (ISO 26262, DO-178C, IEC 61508 além da meta do Zephyr) e OWASP IoT Top 10 (PDF com link 404).
8. Comunidade social (Reddit, X, YouTube) não alcançada; "padrões de comunidade" vêm de blogs, HN e GitHub.
9. Fora de cobertura: STM32 oficial (além do `.mdc` CC0), Nordic/nRF, RP2040, bootloaders STM32, NVS/flash e desgaste, USB, displays, Matter/Thread/LoRa/Zigbee, TinyML, Linux embarcado (Yocto/Buildroot), provisionamento, conformidade de rádio.
10. CAN: pull-up, terminação e taxa de bits sem fonte; I2C: recuperação de barramento e clock stretching Inferidos; MQTT 5.0 lido só até a metade.
11. clang-tidy com toolchain cruzado (`--target`, `--sysroot`) não verificado.
12. Prompt-scores dos itens da pesquisa são do mesmo modelo que validou: não são validação externa independente. O plugin não foi executado contra hardware.

## 6. Como conferir versões antes de citar API

| Item | Onde conferir |
| --- | --- |
| ESP-IDF | `idf.py --version`; doc com seletor de versão em docs.espressif.com (a URL `latest` muda) |
| Zephyr | `west --version` e `VERSION` na árvore; doc `latest` x `v<versão>` |
| FreeRTOS | `tasks.h` (`tskKERNEL_VERSION_NUMBER`); README do kernel cita V11.1.0 (LTS 202406.00) na leitura de 2026-10-10 |
| MCUboot | README do repositório cita 2.5.0-rc1 na leitura; confira a versão do módulo no `west.yml` |
| embedded-hal, RTIC, Embassy | `cargo tree -p <crate>`; embedded-hal 1.0.0 e RTIC 2.3.1 na leitura |
| GCC, clang-tidy, cppcheck | `<ferramenta> --version`; flags mudam entre versões |
| NIST 8259 | NISTIR 8259 (2020) foi retirado em 20/04/2026; use a Rev. 1 |
