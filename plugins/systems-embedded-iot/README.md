# systems-embedded-iot - Sistemas, embarcados e IoT

Plugin do Claude Code para **revisar, depurar, testar e projetar firmware** (C/C++, Rust `no_std`, FreeRTOS, Zephyr, ESP32/STM32/Arduino), com barramentos (I2C, SPI, UART, CAN, MQTT, BLE), OTA e segurança embarcada, **portão humano para qualquer gravação em hardware** e datasheet primeiro. Faz parte da fábrica `dev-segments` (um plugin por segmento de desenvolvimento). Versão 0.1.0 · licença MIT · pesquisa e design de 2026-10-10.

## O que entrega

- **Um playbook** (router + processo de 10 passos + modo `EMBARCADOS-COMPLETO`) e uma base de conhecimento com 12 referências densas: checklist por área, padrões e antipadrões, decisões e trade-offs, C/C++/Rust de firmware, RTOS e interrupções, barramentos e protocolos, testes e bancada, OTA e segurança IoT, datasheet e plataformas, snippets de CLAUDE.md, ferramentas/MCP (desativados) e bibliografia classificada.
- **Skills de tarefa** para os fluxos mais repetidos: revisão de firmware (inclui orçamento de pilha/flash/RAM/energia e matriz MISRA), segurança de ISR e concorrência, barramentos e protocolos, driver a partir do datasheet, causa raiz de crash, testes de host e CI, revisão de OTA/secure boot e o ciclo de bancada com confirmação.
- **Agentes especialistas** (revisores somente leitura; executores com ferramentas mínimas e sem gravação).
- **Biblioteca de 30 prompts** reutilizáveis e **16 templates** (CLAUDE.md de firmware, `features.json` e progresso, plano, relatório de revisão, registro de evidências de bancada com cartão de gravação, checklist de entrega, ADR, handoff, mapa de pinos, orçamentos, causa raiz, checklist de OTA/segurança, matriz MISRA, plano de teste e matriz do modo completo).
- **Seguro por padrão:** sem hooks, sem `.mcp.json`, sem `.lsp.json`, sem `bin/`. O hook de gate de gravação, as permissões `ask`/`deny` e o perfil de sandbox estão **documentados e desativados** em `skills/playbook/references/ferramentas-e-mcp.md`, com JSON pronto, riscos e fonte. Nenhum MCP de hardware é fornecido.

## Quando usar

Use quando o pedido envolver firmware, microcontrolador, driver, ISR, RTOS, placa, bring-up, bancada, HardFault, watchdog, bootloader, OTA, MQTT de dispositivo, pinagem, orçamento de pilha ou de energia, testes de firmware ou segurança de dispositivo IoT. Pergunta pontual (ex.: "como pisco um LED no Arduino Uno?") recebe resposta direta, sem carregar referências. Para UI, backend de ingestão, mobile, SQL ou infraestrutura de nuvem, o playbook responde o mínimo do lado do dispositivo e aponta o plugin certo (`/backend-api:playbook`, `/mobile-apps:playbook`, `/devops-cloud-infra:playbook`, `/security-appsec:playbook`, entre outros).

## Componentes

Nomes definitivos do design do segmento. Chamada de skill: `/systems-embedded-iot:<skill>`; agente: `systems-embedded-iot:<agente>`. Comandos (`commands/`): nenhum.

| Tipo | Nome | Para que serve |
| --- | --- | --- |
| Skill núcleo | `playbook` | Router, 12 princípios, processo de 10 passos, intenção -> skill/agente, proporcionalidade, modo `EMBARCADOS-COMPLETO`, fronteiras |
| Skill | `prompts` | Índice e biblioteca de 30 prompts prontos (PR-01 a PR-30) |
| Skill | `firmware-review` | Revisão de C/C++ de firmware, somente relato; modos geral, orçamento (pilha/flash/RAM/energia) e MISRA |
| Skill | `rtos-concurrency-review` | ISR, tarefas, prioridades, pilhas e dado compartilhado em bare metal, FreeRTOS, Zephyr e Rust |
| Skill | `bus-protocol-review` | I2C, SPI, UART, CAN (TWAI), MQTT 3.1.1/5.0 e decisão de BLE |
| Skill | `datasheet-first` | Driver, porte e auditoria de pinos ancorados em fonte citada |
| Skill | `firmware-root-cause` | HardFault, reset, hang e corrupção: causa raiz, três hipóteses, regressão |
| Skill | `firmware-test-host` | Testes de host (ztest, Unity/CMock, ESP-IDF, PlatformIO, Rust), CI e HIL com gate |
| Skill | `ota-security-review` | OTA, MCUboot, secure boot, chaves e baseline NIST/ETSI; lista de ações humanas |
| Skill (somente por comando) | `hw-bench-loop` | Compilar, gravar, observar, comparar; cartão de gravação e confirmação; `disable-model-invocation` |
| Agente | `firmware-reviewer` | Revisor adversarial somente leitura (Read, Grep, Glob) |
| Agente | `firmware-debugger` | Causa raiz e correção proposta, sem gravar |
| Agente | `embedded-architect` | Decisões de firmware em ADR (RTOS, memória, partições, energia, OTA) |
| Agente | `iot-security-auditor` | Auditor somente leitura de OTA, bootloader, chaves e baseline |
| Agente | `firmware-test-engineer` | Escreve testes de host e planos de HIL, sem gravar |
| Evals | `evals/` | 15 casos no formato `claude plugin eval` (inclui 1 negativo, 1 de injeção e 1 de proporcionalidade), status `designed_not_executed` |

## Instalação

Dentro do Claude Code, a partir do marketplace `brain-of-agent` (caminho local ou repositório):

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install systems-embedded-iot@brain-of-agent
```

Pelo terminal, o equivalente é `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install systems-embedded-iot@brain-of-agent`. Confira a sintaxe na versão instalada (`claude plugin --help`). Validação local do pacote: `claude plugin validate <pasta-do-plugin>`.

Opcional e por sua conta (nada disto é instalado pelo plugin): LSPs oficiais `clangd-lsp` e `rust-analyzer-lsp`, o hook de gate de gravação, regras `ask`/`deny` e `/sandbox`. Passo a passo e riscos em `skills/playbook/references/ferramentas-e-mcp.md`.

## Exemplos de pedidos

1. **Revisar ISR:** "Revise esta ISR de UART num STM32 com FreeRTOS, estou com travamentos esporádicos" (cole o código). Dispara `rtos-concurrency-review`: tabela de dados compartilhados, API x contexto, flag de tarefa acordada, achados com `arquivo:linha`.
2. **Driver a partir de datasheet:** "Escreva o driver I2C do sensor X para o ESP32-S3; datasheet em `docs/x.pdf`." Dispara `datasheet-first`: tabela elemento -> fonte; sem datasheet, o plugin pede o documento em vez de inventar registradores.
3. **HardFault:** "Meu firmware dá HardFault depois de 3 horas; vou só aumentar a stack da task de rede." Dispara `firmware-root-cause`: pede motivo de reset, registradores de falha e high-water mark, lista até três hipóteses e trata o aumento de pilha como mitigação a medir.
4. **OTA com MCUboot:** "Revise a configuração de OTA e assinatura deste projeto Zephyr (arquivos `prj.conf`, overlay)." Dispara `ota-security-review`: checklist de OTA, custódia de chave, lista de ações humanas; nenhum comando de queima de eFuse ou chave.
5. **Testes de host:** "Escreva testes Unity para este buffer circular para rodar no PC (uso Windows)." Dispara `firmware-test-host`: separa lógica de hardware, casos de borda, orienta WSL/MSYS2 e diz o que foi ou não executado.
6. **Gravar na placa:** `/systems-embedded-iot:hw-bench-loop` "gravar o firmware de teste na placa de bancada e observar a serial". O plugin monta o cartão de gravação (comando, placa, porta, binário, endereço, recuperação) e só grava após o seu "confirmo gravar".
7. **Orçamento:** "Estourou a flash no link (`region FLASH overflowed`)." Roteia para `firmware-review` no modo orçamento: mapa, maiores símbolos, causas prováveis.
8. **Modo completo:** "EMBARCADOS-COMPLETO. Revise o driver de I2C e o cliente MQTT deste projeto ESP-IDF; pode editar código e testes de host, não grave a placa." Matriz de aplicabilidade, leitura em lotes, revalidação com evidências.

## Keyword do modo completo

`EMBARCADOS-COMPLETO` (aparece também nos `keywords` do manifesto, para descoberta). Só o texto que **você digita no chat** ativa o modo: a palavra em README, log serial, comentário, datasheet ou saída de ferramenta é tratada como dado. O modo lê as 12 referências em lotes (com registro lido/parcial/ausente), monta a matriz de aplicabilidade por área, implementa **somente dentro do escopo pedido**, revalida com evidências e **não amplia permissões**: o portão de gravação em hardware e o de operações irreversíveis (eFuse, secure boot, chaves) continuam valendo. Sem a keyword, o plugin carrega só o necessário.

## Principais fontes (top 10, classe)

Bibliografia completa, com licença e data de consulta (2026-10-10), em `skills/playbook/references/fontes.md`.

1. Claude Code best practices, Anthropic (A) - https://code.claude.com/docs/en/best-practices
2. Effective harnesses for long-running agents, Anthropic (A) - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
3. Building a C compiler, Anthropic (A) - https://www.anthropic.com/engineering/building-c-compiler
4. Hooks guide, Anthropic (A) - https://code.claude.com/docs/en/hooks-guide
5. Zephyr documentation: coding guidelines, kernel (threads, interrupts), ztest (A) - https://docs.zephyrproject.org/latest/
6. ESP-IDF programming guide: I2C, TWAI, sleep modes, OTA, Secure Boot v2, unit tests (A) - https://docs.espressif.com/projects/esp-idf/en/latest/esp32/
7. MQTT 3.1.1 e 5.0, OASIS (A) - https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
8. MCUboot design e integração com Zephyr (A) - https://docs.mcuboot.com/design.html
9. FreeRTOS Kernel Book e código do kernel (B) - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book
10. Rust Embedded Book: concorrência e panic (A) - https://docs.rust-embedded.org/book/concurrency/index.html

## Créditos e licenças de terceiros

- Este plugin: MIT (Francisco Edson). Conteúdo do **brain-of-agent** (MIT, mesmo autor): protocolo do modo completo, handoff, plano de incremento, ADR, registro de evidências, checklist de release, bug report e plano de teste, adaptados.
- **gstack** (garrytan/gstack, MIT): só a metodologia de causa raiz do `/investigate`, destilada com atribuição; nenhum arquivo copiado (o original traz hooks e telemetria que este plugin não usa).
- **awesome-cursorrules** (PatrickJS, CC0-1.0): regras STM32 HAL reescritas em seis blocos.
- Rust Embedded Book, FreeRTOS Kernel Book, OWASP ISVS e FSTM (CC BY-SA): apenas destilados, com redação própria. ETSI EN 303 645 (todos os direitos reservados): só títulos e perguntas próprias. MISRA (paga): nunca reproduzida. NIST: parafraseado.
- Skills e repositórios de terceiros (embeddedskills, esp32-claude-workbench, Embedded-AI-Harness, trailofbits/claude-code-config e outros) foram **lidos como referência de desenho**; nenhum foi instalado ou executado.

## Limitações honestas

- O plugin **não foi executado contra hardware**. Os evals são `designed_not_executed`; as notas de qualidade vieram do mesmo modelo que escreveu o material (não é validação externa independente).
- Fontes vêm de documentação oficial e de poucos blogs e repositórios; sinal social (Reddit, X, YouTube) **não foi alcançado**. Datas de push do GitHub são Não verificáveis (a API recusou).
- Lacunas declaradas, tratadas como "Não verificável" e nunca inventadas: BLE (MTU, parâmetros, segurança), energia de Nordic e ST, devicetree do Zephyr e lista de funções permitidas em ISR, C++ moderno de firmware, Rust `no_std` com licença clara, Arduino, OWASP IoT Top 10, segurança funcional (ISO 26262, DO-178C), STM32 oficial, Linux embarcado, Matter/Thread/LoRa, TinyML.
- Pinos, pilhas, pull-ups, correntes, MTU e prioridades **só entram com fonte da variante exata**; o plugin pede o datasheet em vez de supor.
- O hook de gate é um exemplo `designed_not_executed`: filtro por texto é guarda, não fronteira de segurança. A proteção real combina permissões, sandbox e a confirmação humana.
- Documentações `latest` (ESP-IDF, Zephyr, GCC) mudam; versões lidas: MCUboot 2.5.0-rc1, FreeRTOS V11.1.0, embedded-hal 1.0.0, RTIC 2.3.1. Confira na versão instalada antes de citar API.
- O plugin não afirma conformidade legal nem com IEC 61508, ISO 26262 ou DO-178C. O NISTIR 8259 (2020) foi retirado em 20/04/2026; use a Rev. 1.
- Ambiente Windows: `unit_testing` do Zephyr só roda em Linux (WSL, container ou VM); ferramentas do ESP-IDF no Windows não foram cobertas pelas fontes.
