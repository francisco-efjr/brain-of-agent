# Auditoria de pinos: violações a procurar e tabela de saída

Uso: modo `pinos` da skill `datasheet-first`. Fontes lidas em 2026-10-10: V-26 (esp32_pin_audit do workbench, classe C, reescrito e corrigido contra a documentação do ESP-IDF), V-30 (pull-up de I2C), V-39 (isolamento de pinos antes do deep sleep), K-12 do design (conflito entre workbench e documentação, prevalece a documentação). Escopo de validade: **ESP32 clássico**. Para S2, S3, C3, C6 e outras variantes o mapa muda: use o datasheet da variante exata ou rotule Não verificável.

Sumário: [Coleta](#coleta) · [Violações](#violações) · [Tabela de saída](#tabela-de-saída) · [Exemplo](#exemplo) · [O que não entra](#o-que-não-entra)

## Coleta

Reúna as atribuições por `Grep` antes de ler documentação; cada linha encontrada vira uma linha da tabela.

| Plataforma | Onde procurar |
| --- | --- |
| ESP-IDF | `GPIO_NUM_[0-9]+`, `\.(sda\|scl\|mosi\|miso\|sclk\|tx\|rx)_io_num` (no comando real, `|` simples), `gpio_set_direction`, `gpio_config`, `CONFIG_.*GPIO` no `sdkconfig` e `Kconfig.projbuild` |
| Zephyr | `pinctrl-0`, `gpios = <&gpio`, arquivos `.overlay` e `.dts` da placa (devicetree não foi lido nesta rodada: leia o arquivo do projeto e não presuma o padrão da placa) |
| STM32 (CubeMX) | arquivo `.ioc` (linhas `PA5.Signal=...`, Inferido), `main.c` gerado, `MX_GPIO_Init` |
| Arduino/PlatformIO | `pinMode(`, `#define .*PIN`, `build_flags` com `-D` de pino, `variants/` da placa |

Pergunte pela placa/módulo exata (por exemplo, o módulo tem PSRAM?) e pelo esquemático: a mesma SoC tem pinos diferentes disponíveis conforme o módulo.

## Violações

Lista de verificação do ESP32 clássico. Severidade é o padrão; ajuste pelo cenário.

| # | Violação | Por que importa | Fonte e rótulo | Sev |
| --- | --- | --- | --- | --- |
| P-01 | Pino de flash ou PSRAM do módulo em uso: GPIO 6 a 11; também GPIO 16 e 17 em módulos com PSRAM. | O módulo usa esses pinos para a memória; usar como E/S trava o sistema ou corrompe o código. | Documentação do ESP-IDF (V-26, correção 4): "costumam estar ligados"; depende do módulo. Verificado | alta |
| P-02 | Pino de strapping usado sem justificativa de boot. A lista vem do datasheet da variante; no ESP32 clássico o datasheet lista GPIO 0, 2, 5, 12 e 15 (conhecimento estável, Inferido nesta rodada: confirme na revisão do datasheet do módulo). | Nível no pino durante o reset muda modo de boot ou tensão da flash; periférico externo pode forçar o nível errado. | Lista por variante: datasheet (Não verificável sem ele); lista do ESP32 clássico: Inferido | alta |
| P-03 | Saída configurada em pino só de entrada: GPIO 34 a 39 (sem pull interno). | O pino não dirige saída; entrada sem pull flutua. | Documentação do ESP-IDF. Verificado | alta |
| P-04 | O mesmo pino atribuído a dois periféricos ou a dois papéis. | Conflito silencioso; o último a configurar vence. | Leitura do código. Verificado | alta |
| P-05 | I2C apenas com pull-up interno. | A página do ESP-IDF diz que o pull-up interno é insuficiente para alta velocidade e indica pull-up externo (faixa 1 kΩ a 10 kΩ; valor da placa por medição e datasheet). | V-30. Verificado | alta |
| P-06 | Entrada flutuante (sem pull e sem driver externo). | Leituras aleatórias, consumo extra. | Prática; Inferido | média |
| P-07 | ADC2 usado com Wi-Fi ativo no ESP32 clássico. | O ADC2 é compartilhado com o rádio Wi-Fi nessa variante. | Inferido; não reconferido na documentação nesta rodada | média |
| P-08 | Pinos do console (GPIO 1 e 3 no UART0 padrão do ESP32 clássico) usados para outra função sem desligar o console. | Logs e bootloader escrevem no pino. | Inferido | média |
| P-09 | Código diverge do mapa de pinos do projeto. | A documentação engana quem monta a placa. | Leitura. Verificado | média |
| P-10 | Antes do deep sleep, pino com pull interno ligado a um nível que cria corrente; falta `rtc_gpio_isolate()` onde cabe. | Corrente de repouso acima do orçamento. | V-39. Verificado (função e propósito) | média |

Números de pilha, memória e pinos citados pelo workbench de terceiros (por exemplo "320 KB de SRAM", pilhas mínimas de 2048 e 4096 bytes) **não** entram: não aparecem na documentação do ESP-IDF consultada (V-26, V-25).

## Tabela de saída

Modelo `mapa-de-pinos.md` do playbook, com as colunas:

| GPIO | Função | Componente | Direção | Pull | Fonte (documento, seção) | Notas | Achados |
| --- | --- | --- | --- | --- | --- | --- | --- |

Depois da tabela, uma lista de achados com ID `P-nn` (use a numeração acima), arquivo:linha, severidade, confiança 1 a 10, correção e como verificar (esquemático, medição de nível no reset, teste de boot na bancada pelo gate de `hw-bench-loop`). Achados com confiança abaixo de 6 vão para "Não verificado".

## Exemplo

Código (trecho): `.sda_io_num = 21, .scl_io_num = 22, .flags.enable_internal_pullup = true` num módulo ESP32 clássico, e `gpio_set_direction(GPIO_NUM_35, GPIO_MODE_OUTPUT)` para um LED.

| GPIO | Função | Componente | Direção | Pull | Fonte | Notas | Achados |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 21 | I2C SDA | sensor externo | bidirecional | interno apenas | `i2c.c:12` | pino padrão de I2C no ESP32 clássico (Inferido) | P-05 |
| 22 | I2C SCL | sensor externo | saída | interno apenas | `i2c.c:12` | idem | P-05 |
| 35 | LED | LED da placa | saída (pedida) | sem pull interno | `led.c:8`; documentação ESP-IDF | GPIO 34 a 39 são só de entrada | P-03 |

Achados: P-03 (alta, confiança 9): GPIO 35 não pode ser saída; mover o LED para um pino de saída livre depois de conferir o esquemático. P-05 (alta, 8): confirmar pull-up externo no esquemático e medir tempo de subida; o valor do resistor vem do datasheet dos dispositivos. Não verificado: se o módulo usa PSRAM (afetaria GPIO 16 e 17), se algum pino listado é de strapping na variante (lista do datasheet).

## O que não entra

- Conclusões para S2, S3, C3, C6 sem o datasheet da variante.
- Valores de resistor, tensão ou corrente sem fonte da variante e da placa.
- Comandos que mudam estado do dispositivo (ler eFuse, forçar nível em pino real): qualquer teste físico passa pelo gate de `hw-bench-loop`.
