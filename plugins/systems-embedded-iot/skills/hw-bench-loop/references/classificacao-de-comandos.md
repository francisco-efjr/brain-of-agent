# Classificação de comandos de bancada: leitura, gate leve, gate e recusar

Uso: skill `hw-bench-loop`, agentes com `Bash` e a pré-checagem de `firmware-test-host`. Fontes lidas em 2026-10-10: V-62 (probe-rs na skill de terceiros: flash, erase, reset e write-mem são risco alto; list, info, read-mem, rtt baixo; `.bin` exige endereço; chip nunca adivinhado), V-21 (flash, write-mem e reset classificados como alto risco; ambiguidade lista candidatos), V-51 (`west flash`, `west debug` e `--erase` gravam; `west flash -H` lista opções do runner), V-55 (probe-rs: `download`, `flash`, `erase`, `reset`, escrita de memória; `run` grava antes de abrir o RTT; `cargo-flash`, `cargo-embed`), V-38 (o serviço `idf` do pytest-embedded grava automaticamente), V-57 (PlatformIO). Classes do plugin: leitura (livre no host, ainda sujeita ao prompt de permissão), gate leve (pergunte; muda o estado do alvo sem gravar), gate (cartão e confirmação) e recusar. A sintaxe exata e o efeito de cada opção variam por versão: confirme com `--help`. Só as entradas atribuídas a um item V-nn foram lidas nas fontes; as demais linhas são conhecimento estável do domínio (Inferido) e devem ser conferidas com `--help`.

Sumário: [Regra de classificação](#regra-de-classificação) · [Tabela por ferramenta](#tabela-por-ferramenta) · [Descoberta de alvos](#descoberta-de-alvos) · [Quando houver dúvida](#quando-houver-dúvida)

## Regra de classificação

1. Se o comando pode alterar flash, RAM, registrador, configuração de proteção ou o estado de execução do alvo (reset, parada), não é leitura.
2. Se pode escrever ou apagar: **gate** (cartão de gravação, "confirmo gravar").
3. Se só conecta, para o núcleo ou abre uma porta que pode resetar o alvo: **gate leve** (pergunte, mostre o efeito).
4. Se opera sobre eFuse, OTP, chaves de secure boot, criptografia de flash, proteção permanente de leitura ou anti-rollback: **recusar** e encaminhar a `ota-security-review`.
5. Comando desconhecido: gate até ler o `--help` e reclassificar.

## Tabela por ferramenta

| Ferramenta | Leitura | Gate leve | Gate | Recusar |
| --- | --- | --- | --- | --- |
| `idf.py` | `build`, `size`, `size-components`, `size-files`, `menuconfig` (edita config local) | `monitor` (pode resetar o alvo por DTR/RTS: Inferido), `-p <porta> ...` que só abre a porta | `flash`, `app-flash`, `erase-flash`, `erase-otadata`, `partition-table-flash` | comandos de eFuse e de chaves de secure boot (`espefuse`, `espsecure` de produção) |
| `esptool` | `version`; ler documentação | `chip_id`, `flash_id`, `read_mac`, `read_flash` (conectam e podem reiniciar o chip em modo bootloader: Inferido) | `write_flash`, `erase_flash`, `erase_region`, `write_mem`, `load_ram` | operações de eFuse |
| `west` (Zephyr) | `build`, `boards`, `twister -p unit_testing`, `flash -H` (ajuda do runner, V-51) | nenhum comando fixo (conectar sem gravar depende do runner; `west debug` está em Gate) | `flash`, `debug`, qualquer `--erase`, `twister --device-testing` | `mcumgr` com `confirm`/`test` de produção sem plano; chaves de assinatura de produção |
| `probe-rs` | `list`, `info`, leitura de memória, `rtt` de um alvo já em execução (V-62) | `attach` (Inferido: conecta sem gravar), `gdb` como servidor | `download`, `flash`, `erase`, `reset`, `write` de memória, `run` (grava antes do RTT, V-55), `cargo flash`, `cargo embed` | proteção de leitura permanente |
| OpenOCD | `-c "init; ...; shutdown"` só com comandos de leitura (`mdw`, `reg` com o alvo parado pelo usuário: ver gate leve) | `halt`, `resume` | `program`, `flash write_image`, `erase`, `reset`, `mww` | `flash protect` permanente |
| J-Link (`JLinkExe`, `JFlash`) | listar emuladores | conectar e parar o núcleo | `loadfile`, `erase`, `w4`/`w1` de escrita, `r` de reset | bits de proteção/readout |
| PlatformIO | `pio run`, `pio check`, `pio test -e native`, `pio device list` | `pio device monitor` (abrir porta; pode resetar) | `pio run -t upload`, `-t uploadfs`, `-t erase`, `pio test` sem `-e native` | n/a |
| STM32 (`st-flash`, `STM32_Programmer_CLI`) | listar probes (`st-info --probe`, Inferido) | conectar | `write`, `erase`, `-w` | opção de byte de proteção de leitura (RDP nível 2 é permanente: Inferido) |
| Nordic (`nrfjprog`), AVR (`avrdude`), DFU (`dfu-util`) | listar | conectar | `--program`, `-U write`, `--erase`, `-D` | `--rbp ALL`/proteção de leitura, fuses de AVR (Inferido) |
| `mcumgr`/`imgtool` | `image list`, ler estado | `echo`/status | `image upload`, `image test`, `reset` | assinatura com chave de produção |
| `pytest` com pytest-embedded | coleta (`--collect-only`), serviços `qemu`/`wokwi` sem placa (Inferido) | serviço `serial` apenas lendo | serviço `idf` (grava o binário sozinho, V-38) | n/a |
| `cargo` | `build`, `test --target <host>` com runner de host conferido | n/a | `cargo run`/`test` com runner de gravação, `flash`, `embed` | n/a |
| Scripts do projeto | ler o script antes | se abre a porta | se chama um dos acima | se chama eFuse/chave |

## Descoberta de alvos

Para listar candidatos sem alterar nada (host): portas seriais do sistema (Windows: gerenciador de dispositivos ou `Get-CimInstance Win32_SerialPort`; Linux: `ls /dev/ttyUSB* /dev/ttyACM*`; macOS: `ls /dev/cu.*`), `probe-rs list`, `west flash -H`. Duas ou mais opções que servem: lista e pergunta (V-21). Número de série do probe ou caminho de porta vai para o cartão. Não escolha por "a primeira da lista".

## Quando houver dúvida

- Ferramenta nova ou opção desconhecida: `--help`, e enquanto isso trate como gate.
- Wrapper do projeto (`make flash`, `./scripts/deploy.sh`): leia o corpo; classifique pela pior operação que ele chama.
- Comando composto (`&&`, `;`, `|`): classifique cada parte; a pior define a classe. Build encadeado com flash sem parada é antipadrão (V-21): separe em dois comandos.
- Agente ou hook: o gate no plugin é regra do texto; o hook documentado em `ferramentas-e-mcp.md` é uma camada extra e um comando alternativo escapa dele (V-05, V-63).
