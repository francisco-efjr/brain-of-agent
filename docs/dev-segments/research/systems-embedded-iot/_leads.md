# systems-embedded-iot — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Cobertura do atlas é fraca; poucas pistas, mas há dois itens específicos. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| Embedded STM32 HAL .mdc (CT-10) | https://github.com/PatrickJS/awesome-cursorrules | B (6) | ISR curtas e determinísticas; checar retorno do HAL; `volatile` só para ISR/registradores; sem heap; tabelas `const` em flash; timeouts; watchdog; DMA/CPU sem sincronização é proibido; lógica pura testada no host. CC0; literais Verificados. |
| C++ programming guidelines .mdc (CT-10) | https://github.com/PatrickJS/awesome-cursorrules | B (5) | RAII, Rule of Zero/Five, `std::optional/expected`. CC0. |
| Bitcraze, loop com hardware real (CP-27) | https://www.bitcraze.io/?p=14780 | B (5) | Daemon local para link stateful + comandos one-shot (`flash`, `reset`, `console --since`, `log`, `param`) com saída curta e exit code; skill do ciclo build → flash → observar → corrigir; nunca flashar fora da bancada sem autorização; exigir header/datasheet. Experimento único, não reverificado. |
| claude-plugins-official, LSPs (AO-30) | https://github.com/anthropics/claude-plugins-official | A | 12 plugins LSP em `plugins/` (podem incluir clangd/rust-analyzer: Não verificado). Apache-2.0. |
| Trail of Bits config e skills (EC-12) | https://github.com/trailofbits/claude-code-config | B | Padrões de sandbox e deny rules úteis para firmware com segredos; `building-secure-contracts` não se aplica. |
| Ronacher (CP-12) | https://lucumr.pocoo.org/2025/6/12/agentic-coding/ | B | Ferramenta pronta para agente: rápida, saída curta, timeout, logs fixos. |
| Compilador C (AO-31) | https://www.anthropic.com/engineering/building-c-compiler | A | Projeto de baixo nível; saída de teste desenhada para o modelo (relato da Anthropic). |
| Harnesses (AO-20) | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | A | Estado em arquivo para tarefas longas. |
| awesome-copilot (CT-14) | https://github.com/github/awesome-copilot | A | Atlas diz que cobre 24 de 25 segmentos; embarcados não detalhado: abrir `instructions/`. |
| Ask HN (CP-21) | https://news.ycombinator.com/item?id=46691243 | B | Escopo e stack importam. |
| gstack `/investigate` (BR-17) | https://github.com/garrytan/gstack | B | Causa raiz antes de corrigir; vale em bugs de hardware com instrumentação. |

## 2. Repositórios e arquivos a abrir
- `PatrickJS/awesome-cursorrules/rules/embedded-stm32-hal.mdc` e `cpp-programming-guidelines-cursorrules-prompt-file.mdc`.
- Página Bitcraze citada (blog) e o repositório de skills associado: não localizado no atlas (Não verificável).
- `anthropics/claude-plugins-official/plugins/` (LSPs).
- Zephyr/FreeRTOS docs, Rust Embedded Book, MISRA, datasheets, ESP-IDF não estão no atlas: lente authoritative.

## 3. Materiais oficiais Anthropic pertinentes
AO-30 (LSPs), AO-20, AO-31, AO-06 (verificação por comando), AO-23 (escopo de autorização).

## 4. Padrões da comunidade
- CLI curto com exit code e logs em caminho fixo para o ciclo com hardware (CP-27, CP-12).
- Não inferir registradores; exigir header ou datasheet (CP-27).
- Nunca flashar sem autorização (CP-27, BR-26).
- Lógica pura testada no host (CT-10).

## 5. O que o brain-of-agent já oferece
- `brain_refs` vazio: sem brain específico (BR transversais: embarcados praticamente nulo).
- Transversais: BR-04 (rótulos), BR-26 (modelo de segurança de automação: agir só em recursos próprios, credenciais não passam pelo agente), BR-06/07 (templates).
- BR-03: modo `EMBARCADOS-COMPLETO`.

## 6. Lacunas e cuidados
- Faltam MISRA, sanitizers, clang-tidy, CI, protocolos (I2C, SPI, UART, CAN, MQTT, BLE), OTA, energia, segurança embarcada.
- O próprio atlas diz que o plugin deve acrescentar MISRA/sanitizers/CI.
- Regras de hardware exigem autorização física; plugin nunca deve flashar nem acionar dispositivos por conta própria.
