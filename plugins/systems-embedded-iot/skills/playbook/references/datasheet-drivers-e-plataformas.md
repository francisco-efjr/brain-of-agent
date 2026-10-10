# Datasheet primeiro, drivers e plataformas (STM32, ESP32, Arduino/PlatformIO)

Fontes lidas em 2026-10-10: V-16, V-23, V-25, V-26, V-28, V-47, V-48, V-57 (ver `fontes.md`). Regra central: **nome de registrador, campo, IRQ, função HAL, pino e número elétrico só entram com fonte da variante exata**. Sem fonte, a resposta é "Não verificável" e um pedido do documento, não um palpite.

Sumário: 1. Datasheet-first em 5 passos · 2. Tabela elemento -> fonte · 3. SVD, CMSIS-SVD e svd2rust · 4. Arquitetura em camadas e driver genérico · 5. STM32 HAL em 6 blocos · 6. ESP32: seis perguntas por contexto · 7. Auditoria de pinos · 8. Arduino e PlatformIO · 9. Gotchas.

## 1. Datasheet-first em 5 passos (V-23)

Origem: relatos de um thread do Hacker News (113 pontos, 52 comentários, 15/08/2025; alegações de privacidade do thread não são fato): agentes genéricos inventam registradores e chamadas HAL de outra família. Prática que mitiga:

1. Nomes de registrador e de função HAL vêm de **header, SVD ou datasheet citado com seção**.
2. Sem fonte, **pare e pergunte**.
3. Variante exata do chip e revisão do silício confirmadas (família não basta: `STM32G031` não é `STM32G0` genérico; ESP32 clássico não é S3).
4. Documento proprietário ou sob NDA não sai da máquina sem decisão do usuário (P-11).
5. Relate o que foi compilado, simulado e testado em hardware, separadamente.

Mensagem para pedir o que falta (modelo): "Para escrever o driver preciso de: (a) part number e revisão do silício; (b) datasheet ou reference manual (caminho do arquivo e seções do periférico); (c) errata; (d) SVD ou header da variante; (e) versão do framework. Enquanto isso, entrego a interface do driver e os testes de host com constantes marcadas como placeholders a confirmar."

## 2. Tabela elemento -> fonte (artefato obrigatório de driver)

| Elemento | Valor usado | Fonte (arquivo, seção/página, versão) | Rótulo |
| --- | --- | --- | --- |
| Endereço I2C | `<valor>` | `<datasheet, seção, rev.>` | Verificado se citado e conferido; senão Não verificável |
| Registrador `<NOME>` e campos | `<offset, bits>` | `<SVD ou RM, versão>` | idem |
| IRQ / vetor | `<nome>` | `<header da variante>` | idem |
| Tempo de conversão / timeout | `<ms>` | `<datasheet, tabela de características>` | idem |

Verificação por `grep`: cada nome citado existe no header/SVD fornecido (`grep -n "<NOME>" <arquivo>`). Divergência entre SVD e reference manual é **achado**, não decisão do modelo (V-48). Exemplo de uso honesto (eval E2): pedido do driver de um "TXS9000 igual ao TMP117" sem datasheet: não confirme a equivalência, declare endereço, registradores e conversões Não verificáveis, peça o documento e entregue interface I2C abstrata com placeholders.

## 3. SVD, CMSIS-SVD e svd2rust (V-48)

CMSIS-SVD formaliza registradores mapeados em memória, campos de bits e interrupções de dispositivos Arm Cortex; é mantido pelos fabricantes e distribuído em Device Family Packs; serve a visões de periférico no depurador e a headers CMSIS. svd2rust (Apache-2.0 e MIT, 860 estrelas na página) gera structs de mapa de registradores a partir do SVD. Registre **versão e origem do arquivo SVD**. A página do SVD não declara licença nem versão: não afirme.

## 4. Arquitetura em camadas e driver genérico (V-16, V-47)

- Camadas: BSP, drivers, middleware, aplicação, testes. Código gerado por ferramenta (CubeMX) fica separado do código à mão. Hardware atrás de interface estreita; init de periférico em **um** lugar; dono do periférico e do DMA documentado; clock, pinos e prioridades documentados.
- Em C: a interface do driver é um header (`sensor.h`, `hal_i2c.h`); o domínio chama a interface; teste de host usa mock (ver `testes-e-bancada.md`).
- Em Rust: driver genérico sobre os traits do `embedded-hal` 1.0 (`I2c`, `SpiDevice`, `OutputPin`, `DelayNs`), não sobre um HAL específico; registre a versão do crate (V-47).
- Erros e timeouts do barramento: ver `barramentos-e-protocolos.md`.

## 5. STM32 HAL em 6 blocos (V-16, redação própria; origem CC0)

Origem: `embedded-stm32-hal.mdc` (30 regras conferidas; repositório CC0-1.0). Reescrita em blocos com a razão de cada regra. Acrescenta a nuance que a fonte omite: **`volatile` não torna o acesso atômico nem ordena memória**.

**Antes de mexer em periférico:** leia o reference manual e a errata da variante; nomes de registrador e função HAL vêm de header ou datasheet citado.

| Bloco | Regras | Razão |
| --- | --- | --- |
| 1. Camadas | BSP/drivers/middleware/app/testes separados; código do CubeMX isolado; hardware atrás de interface estreita | Regenerar o projeto não pode apagar código à mão |
| 2. Periféricos e HAL | Documentar clock, pinos e dono de cada periférico; init em um lugar; **checar o retorno do HAL**; **timeout em toda espera** (nada de `HAL_MAX_DELAY` sem justificativa); DMA com dono e tempo de vida do buffer definidos | Retorno ignorado e espera infinita são as causas clássicas de travamento |
| 3. ISR e concorrência | ISR curta e sem alocação; seções críticas, atômicos ou filas para dado compartilhado; prioridades documentadas | RMW perdido e inversão |
| 4. Memória e tipos | Tabelas `const` em flash; inteiros de largura fixa; `volatile` só para ISR/registrador; pilhas de ISR e tarefas dimensionadas | Economiza RAM; evita surpresa de porte |
| 5. Robustez em campo | Watchdog desde o início; fault handler que registra motivo de reset, registradores de falha e versão do build | Falha de campo sem pista é irreproduzível |
| 6. Testes | Lógica no host; HIL para periférico | Ciclo rápido; realidade onde precisa |

Formato de saída de revisão: `achado · regra (bloco) · arquivo:linha · gravidade · como verificar`.

## 6. ESP32: seis perguntas por achado (V-28, redação própria)

Antes de qualquer achado em firmware ESP32: identifique chip, framework, versão e configuração (`sdkconfig`). Julgue pelo comportamento em campo (semanas de uptime, OTA, reconexão, baixa tensão). Para cada achado responda:

1. **Contexto de execução:** tarefa, ISR, timer ou event loop? (limita as operações).
2. **Limite:** pilha, fila, retries, espera e alocação têm teto explícito?
3. **Dono do dado:** quem escreve e lê; há troca de mensagem em vez de estado compartilhado?
4. **Região de memória:** a escolha é deliberada (IRAM, DRAM, PSRAM, flash)?
5. **Classe de falha:** transitória, de configuração ou de hardware? (watchdog é último recurso, não correção).
6. **Consequência em campo:** o que o usuário vê após semanas ou numa queda de energia?

Rótulo de evidência: compilado, simulado, em hardware (separados). Política de memória (K-01): ESP-IDF usa heap por padrão; a regra do workbench "heap para buffers acima de 512 bytes e evitar buffers grandes na pilha" é regra de pilha x heap, não conflito com a regra "sem heap" do STM32 bare metal (V-25). Os mínimos de pilha 2048/4096 bytes do workbench são números do autor: **não entram**.

## 7. Auditoria de pinos (modo `pinos` de `datasheet-first`; V-26 corrigido pela doc ESP-IDF)

Saída: tabela `assets/templates/mapa-de-pinos.md` (GPIO, função, componente, direção, pull, fonte, notas) e lista de achados com gravidade.

| Violação a procurar | Fonte / rótulo |
| --- | --- |
| Pino de flash ou PSRAM do módulo em uso: no ESP32 clássico, GPIO 6-11 e também 16-17 em módulos com PSRAM costumam estar ligados à flash/PSRAM | Doc ESP-IDF, Verificado |
| Pino de strapping usado sem justificativa de boot (a lista vem do datasheet da variante; no ESP32 clássico inclui GPIO 5 e 12) | Datasheet da variante; GPIO 5 e 12: Inferido |
| Saída configurada em pino só de entrada (GPIO 34-39 no clássico, sem pull interno) | Doc ESP-IDF, Verificado |
| Mesmo pino em dois periféricos | Revisão do código e do mapa |
| I2C só com pull-up interno | Ver `barramentos-e-protocolos.md` |
| Entrada flutuante | Revisão |
| ADC2 com Wi-Fi no ESP32 clássico | Inferido; não reconferido na doc |
| Código divergente do mapa de pinos documentado | Revisão com grep |

Vale só para o ESP32 **clássico**; S2, S3, C3 e C6 têm mapas diferentes e exigem o datasheet da variante (K-12). Pinos, cores e mínimos de pilha do workbench (V-25) não entram sem conferência.

## 8. Arduino e PlatformIO (lacuna parcial, V-57)

- PlatformIO: testes `native` no host, na placa ou em ambos; `pio check` com Cppcheck; ver `testes-e-bancada.md`. `platformio.ini` é a fonte do alvo (`board`, `framework`, `platform`, versões fixadas).
- Arduino: o guia de estilo oficial não trouxe conteúdo na pesquisa; sem fonte validada. Regras de Arduino neste plugin são as gerais de firmware (timeouts, retorno checado, sem alocação em ISR) e `Serial.println` em ISR é achado (Inferido).
- Pergunta pontual ("como pisco um LED no Arduino Uno?") recebe resposta curta e direta, sem referências (proporcionalidade).

## 9. Gotchas

- Rótulo de pino de placa de desenvolvimento (D1, D2) não é número de GPIO: confira o esquemático da placa (Inferido).
- Header gerado por CubeMX muda com a versão do pacote: registre versão do HAL/CMSIS.
- Errata pode invalidar o comportamento documentado do periférico: sempre consulte a errata da revisão do silício.
- `esp32-expert` e `esp32-firmware-engineer-skill` de terceiros: só destilação, não instalar (V-18, V-28).
