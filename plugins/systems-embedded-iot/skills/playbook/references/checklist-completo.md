# Checklist completo e matriz de aplicabilidade

Usado no modo `EMBARCADOS-COMPLETO` e como lista de pronto em qualquer entrega maior. Cada item tem um critério verificável e uma fonte `V-nn` (ver `fontes.md`) ou "conhecimento estável" (Inferido). Formato de matriz: `assets/templates/matriz-embarcados-completo.md`.

Sumário: 1. Como usar a matriz · 2. Áreas A a N · 3. Gates · 4. Registro de leitura · 5. Resultado.

## 1. Como usar a matriz

Para cada área, marque um estado: **Aplicável** (itens avaliados), **NA** (não se aplica, com motivo: por exemplo "projeto sem rede"), **NV** (aplicável, mas sem acesso a datasheet, placa, repositório ou ferramenta: Não verificável). "Completo" é cobertura honesta da matriz, não caixas artificialmente verdes (protocolo do brain-of-agent, adaptado). Cada item aplicável recebe: `OK` (com evidência), `FALHA` (achado com `arquivo:linha`), `PENDENTE` ou `NV`. Item bloqueante é marcado com (*): `FALHA` ou `PENDENTE` em item (*) impede recomendação favorável, salvo aceite formal de quem decide, registrado.

Evidência aceita: saída de comando colada, trecho de código com linha, diff, log de bancada com data e revisão, link para artefato de CI. "Testado" sem evidência conta como PENDENTE. Leitura de código é Inferido, não Verificado.

## 2. Áreas

### A. Alvo e escopo

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| A-01 (*) | MCU/variante exata e revisão do silício identificados | ficha do alvo no `CLAUDE.md`/plano | V-28, V-62 |
| A-02 (*) | Framework e versão (ESP-IDF, Zephyr, FreeRTOS, Arduino/PlatformIO, Cargo) conferidos nos manifestos | `sdkconfig`, `prj.conf`, `platformio.ini`, `Cargo.toml`, `CMakeLists.txt` | V-28 |
| A-03 | Fontes de verdade listadas (datasheet, RM, errata, SVD, headers) ou ausência declarada | tabela elemento -> fonte | V-23, V-48 |
| A-04 | Escopo, exclusões e autorização do pedido registrados | plano de uma página | house-style |
| A-05 | Política de memória do perfil declarada | S-05 | V-09, V-16, V-25 |
| A-06 | Estado do workspace preservado (mudanças do usuário intactas) | `git status` antes e depois | brain |

### B. C/C++/Rust

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| B-01 (*) | Toda chamada com status é checada; ignorar de propósito usa `(void)` | grep + clang-tidy `bugprone-unused-return-value` | V-09, V-10 |
| B-02 | Sem recursão, VLA e `alloca` | `-Wvla`, grafo de chamadas | V-09 |
| B-03 | `switch` com `default`; `else` final | `-Wswitch-default` | V-09 |
| B-04 | Sem remover `const`/`volatile` por cast | `-Wcast-qual` | V-09 |
| B-05 | Inteiros de largura fixa; conversões explícitas | `-Wconversion` | V-16 |
| B-06 | Build com `-Wall -Wextra` sem avisos novos | saída do build | conhecimento estável |
| B-07 | clang-tidy/cppcheck rodados no escopo, resultados tratados (toolchain cruzado: NV) | saída colada | V-13, V-58 |
| B-08 | Rust: um `#[panic_handler]`; sem `static mut` com interrupção; versões de crates registradas | `cargo tree`, grep | V-11, V-12, V-47 |
| B-09 | Matriz MISRA preenchida se houver política (edição, categorias, desvios) | `matriz-misra.md` | V-14, V-58 |
| B-10 | C++: política sobre exceções/RTTI/alocação declarada (Inferido) | CLAUDE.md | lacuna |

### C. Memória

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| C-01 (*) | Sem alocação em ISR; heap conforme a política | grep `malloc|new|pvPortMalloc|k_malloc` por contexto | V-16, V-25 |
| C-02 | Tabelas `const` em flash (não em `.data`) | `.map`, `nm`/`size -A` | V-16 |
| C-03 | Orçamento flash/RAM do `.map` com margem declarada | `orcamentos.md` | V-59 |
| C-04 (*) | Pilha por contexto: estimativa (`.su`) e medição (high-water) | `orcamentos.md` | V-59, V-49, V-52 |
| C-05 | Buffers DMA em RAM válida e alinhados; dono e tempo de vida definidos | revisão | V-32, V-16 |
| C-06 | Erro de link `region overflowed` tratado pela análise do mapa | mapa e símbolos maiores | estável (Inferido) |

### D. ISR e concorrência

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| D-01 (*) | ISR curta, sem bloqueio nem `printf` | revisão por ISR | V-16, V-15 |
| D-02 (*) | Tabela de dados compartilhados com dono e proteção | tabela anexa | V-12 |
| D-03 | `volatile` não usado como atomicidade; multi-palavra protegido | revisão | V-14, V-12 |
| D-04 | Inicialização antes de habilitar a interrupção | ordem em `app_init()` | V-12 |
| D-05 | Seção crítica com latência de pior caso medida | medição ou NV | V-12 (K-05) |
| D-06 | Dois núcleos: proteção vale entre núcleos | revisão | V-12 |

### E. RTOS

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| E-01 (*) | FreeRTOS: só `FromISR`; flag de tarefa acordada repassado ao yield | revisão | V-52, V-15 |
| E-02 | Prioridade de ISR dentro do limite de API da porta; `configASSERT` ligado em dev | `FreeRTOSConfig.h` | V-52 |
| E-03 | Overflow de pilha: `configCHECK_FOR_STACK_OVERFLOW` ligado e high-water registrado | config + log | V-52 |
| E-04 | Zephyr: prioridades justificadas; pilha medida com `k_thread_stack_space_get()` | `prj.conf`, log | V-49 |
| E-05 | Trabalho demorado fora da ISR e fora do handler que bloqueia a fila do sistema | revisão | V-50 |
| E-06 | Kconfig: `.config` final conferido; hardware fixo no devicetree | `.config` | V-51 |

### F. Barramentos

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| F-01 (*) | Todo erro de barramento tem caminho e teste; sem espera infinita injustificada | grep `-1|K_FOREVER|HAL_MAX_DELAY` | V-30, V-35 |
| F-02 | Timeout cobre o pior caso do periférico (datasheet) | tabela de timeouts | V-30 |
| F-03 | Elétrica (pull-up, terminação, transceiver) do datasheet e medida | datasheet + medição ou NV | V-30, V-31 |
| F-04 | I2C/SPI/UART: dono único ou mutex; callbacks sem bloqueio; DMA alinhado | revisão | V-30, V-32 |
| F-05 | CAN: `on_state_change`, bus-off com recuperação limitada, filtro testado | revisão e teste | V-31 |
| F-06 | UART: eventos de overflow/frame/paridade tratados; RX dimensionado | revisão | V-32 |

### G. Rede (MQTT/BLE/Wi-Fi)

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| G-01 | Versão MQTT, keep alive, will, sessão e QoS justificados | config do cliente | V-33 |
| G-02 | Reconexão com backoff e jitter | código | V-33 |
| G-03 (*) | TLS com validação de certificado; credenciais fora do repositório | grep de segredos | V-33, V-44 |
| G-04 | Consumidor idempotente para QoS 1 | contrato com o backend | V-33 |
| G-05 | BLE: decisão de pilha registrada; regras de MTU/segurança NV | ficha | V-34 |
| G-06 | Buffer de RX vs Maximum Packet Size | revisão (Inferido) | V-33 |

### H. Energia

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| H-01 | Corrente medida na placa por estado (ativo/light/deep) com instrumento e firmware real | `orcamentos.md` | V-39 |
| H-02 | Antes do deep sleep: rádio parado, pinos isolados, RTC memory marcada, wake-up configurado | revisão e teste | V-39 |
| H-03 | Conexão que precisa persistir usa modem-sleep, não deep sleep | decisão registrada | V-39 |
| H-04 | Fabricantes sem fonte (Nordic, ST) marcados NV | nota | lacuna |

### I. Testes

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| I-01 (*) | Lógica de domínio testada no host; teste vermelho confirmado pelo motivo certo | saída colada | V-36, V-37 |
| I-02 | Casos de borda de firmware (wrap, overflow, erro injetado, reconexão) | plano de teste | `testes-e-bancada.md` |
| I-03 | Teste inaplicável é skipped, não removido | runner | V-36 |
| I-04 | Suíte inteira ao final; runner conferido (não grava sem gate) | saída + config | V-55, V-57 |
| I-05 | Sanitizers no host em CI | CI | V-59 |
| I-06 | CI com `pytest-embedded` fixado `~=2.0` quando ESP-IDF | `requirements` | V-38 |

### J. Bancada e gate

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| J-01 (*) | Nenhuma gravação sem confirmação explícita; cartão de gravação apresentado | transcrição | V-21, V-27, V-62 |
| J-02 (*) | Alvo/probe/porta inequívocos; chip informado; `.bin` com endereço | cartão | V-21, V-62 |
| J-03 | Caminho de recuperação confirmado | registro | V-27 |
| J-04 | Evidência de bancada com placa, revisão, comando, saída e data | `registro-evidencias-bancada.md` | V-27 |
| J-05 | O que ficou gravado na placa foi listado ao final | handoff | V-21 |
| J-06 | Ferramenta de bancada com saída curta e erro com motivo | checklist da seção 10 de `testes-e-bancada.md` | V-03, V-20 |

### K. OTA e segurança

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| K-01 (*) | Imagem assinada e verificada antes do boot; chave de exemplo fora de produção | config + build de produção | V-44, V-45 |
| K-02 (*) | Confirmação após autoteste, rollback testado, partição de fábrica mantida | teste de bancada | V-46 |
| K-03 | Política de downgrade/anti-rollback decidida por humano | ADR | V-46 |
| K-04 (*) | Irreversíveis (eFuse, secure boot, flash encryption, RDP) apenas listados como ação humana | checklist de OTA | V-27, V-45 |
| K-05 | Segredos fora do repositório, `prj.conf`, `sdkconfig`, logs | varredura | V-44 |
| K-06 | Baseline de produto (13 perguntas ETSI; capacidades NIST) respondido | `checklist-ota-seguranca.md` | V-42, V-43 |
| K-07 | JTAG e download por UART: estado declarado | config | V-45 |

### L. Build e CI

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| L-01 | Build reprodutível: toolchain e versões fixadas; versão do firmware embutida | comando de build e `--version` | estável |
| L-02 | CI roda build cruzado, testes de host, análise e gera artefato assinado (assinatura = ação humana ou HSM) | pipeline (`/devops-cloud-infra:playbook`) | V-44 |
| L-03 | Proveniência do binário gravado (hash do artefato do CI) | hash no cartão de gravação | V-29 |
| L-04 | Release de firmware: matriz de hardware, versão, rollback; publicar tag é ato humano | `checklist-entrega-firmware.md` | V-29 |

### M. Documentação

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| M-01 | Mapa de pinos com fonte por linha | `mapa-de-pinos.md` | V-26 |
| M-02 | Orçamentos e mapa de memória com método de medição | `orcamentos.md` | V-59 |
| M-03 | ADR para decisão material (RTOS, partições, OTA, energia) | `adr-firmware.md` | brain |
| M-04 | Runbook de bancada (comandos, recuperação, o que nunca fazer) | doc | V-61 |
| M-05 | `CLAUDE.md` do firmware curto e sem segredo | contagem de linhas | V-01, V-17 |

### N. Entrega

| ID | Item | Como verificar | Fonte |
| --- | --- | --- | --- |
| N-01 (*) | Resultado separa compilado/simulado/em hardware e Verificado/Inferido/Suposição/NV | relatório | V-27 |
| N-02 | Limitações e riscos residuais em linguagem de decisão | relatório | brain |
| N-03 | Revisão independente declarada como parcial se for do mesmo modelo | nota | house-style |
| N-04 | Handoff com próxima ação e estado da placa | `handoff-checkpoint-firmware.md` | brain |

## 3. Gates do modo completo

| Gate | Saída necessária |
| --- | --- |
| Entendimento | Alvo, fontes de verdade, escopo e conflitos identificados (A) |
| Plano | Contrato (escopo, riscos, testes, reversão), oráculos e dependências de datasheet |
| Implementação | Mudança no escopo; erro, ISR e memória tratados |
| Validação | Checks executados e ligados aos critérios; níveis de evidência |
| Revalidação | Falhas corrigidas verificadas de novo; evidência invalidada refeita |
| Entrega | Artefatos, riscos, estado da placa, lacunas, próximo passo |

## 4. Registro de leitura (modo completo)

Para cada arquivo de referência: caminho, revisão (versão do plugin), `lido` / `parcial` / `ausente`, decisão extraída. Leitura truncada é `parcial` e exige retomada. Lote persistido com checkpoint; leitura em lotes não significa todo o texto no contexto ao mesmo tempo.

## 5. Resultado

**Concluído** (escopo feito, itens aplicáveis verificados, exclusões justificadas, risco residual explícito), **Parcial** (falta leitura, acesso, execução ou revalidação material) ou **Impedido** (condição e próximo passo). Falha crítica aberta impede recomendação favorável; média de notas não a compensa. Nunca declare "firmware aprovado" com leitura ou execução parcial, nem funcionamento em hardware sem log de bancada.
