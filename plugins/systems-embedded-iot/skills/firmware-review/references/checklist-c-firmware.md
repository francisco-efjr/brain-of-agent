# Checklist de C/C++ de firmware: 16 regras com motivo, detecção e fonte

Uso: consulta da skill `firmware-review`. Redação própria; nenhum texto de MISRA, CERT ou do guia do Zephyr é reproduzido. Fontes: V-09 (Zephyr coding guidelines), V-10 (ESP-IDF Style Guide), V-14 (CERT SIG31-C e matriz MISRA), V-16 (regras STM32 HAL, CC0 do repositório awesome-cursorrules, reescritas), V-13 (clang-tidy), V-59 (GCC). Lidas em 2026-10-10.

Sumário: [A erro e retorno](#a-erro-e-retorno) · [B recursos](#b-recursos) · [C tipos e atomicidade](#c-tipos-e-atomicidade) · [D fluxo e estilo defensivo](#d-fluxo-e-estilo-defensivo) · [E robustez de campo](#e-robustez-de-campo) · [Como usar a coluna Detecção](#como-usar-a-coluna-detecção)

Coluna **Detecção**: padrão de `grep -nE` ou opção de compilador/clang-tidy para localizar candidatos. É triagem: cada candidato precisa de leitura para virar achado. Nomes de checks do clang-tidy e flags do GCC são conhecimento estável (Inferido); confirme com `clang-tidy -list-checks` e `gcc --help=warnings` na versão instalada.

## A erro e retorno

| ID | Regra | Motivo | Detecção |
| --- | --- | --- | --- |
| C-01 | Toda chamada que devolve status (HAL, driver, `esp_err_t`, `errno`, `k_*`) tem o retorno checado; descarte intencional usa `(void)` com comentário. | Falha de periférico ignorada vira dado lixo ou travamento adiante, longe da causa. | `grep -nE '^\s*(HAL_\|esp_\|i2c_\|spi_\|uart_)\w+\(' src/` e confira linhas sem `if`/`=`/`ESP_ERROR_CHECK`; `-Wunused-result` com `__attribute__((warn_unused_result))` nas funções próprias. |
| C-02 | Erro recuperável retorna código; `assert`/`ESP_ERROR_CHECK` ficam para erro interno irrecuperável, na inicialização fatal (V-10). | Abortar em campo por falha transitória (NACK, perda de link) derruba o produto. | `grep -nE 'assert\(\|ESP_ERROR_CHECK\(\|configASSERT\('` e leia se estão em caminho de runtime recuperável. |
| C-03 | Expressão dentro de `assert` não tem efeito colateral. | Em build com `NDEBUG` o efeito some e o comportamento muda entre debug e release. | `grep -nE 'assert\([^)]*(\+\+\|--\|=[^=]\|\w+\()'` e leia os candidatos. |
| C-04 | Dois estilos de erro não se misturam no mesmo módulo (retorno negativo, `bool`, `esp_err_t`, `errno`). | O chamador precisa saber como testar; mistura gera `if (ret)` com sentido invertido. | Leitura: tabela "função → convenção de erro" do módulo. |

## B recursos

| ID | Regra | Motivo | Detecção |
| --- | --- | --- | --- |
| C-05 | Todo recurso adquirido (memória, mutex, handle, DMA, fd) é liberado em todos os caminhos de saída, inclusive os de erro. | Vazamento só aparece depois de dias de uptime. | Leitura de cada `return` entre aquisição e liberação; `clang-tidy -checks='clang-analyzer-*'` (Inferido). |
| C-06 | Buffer de DMA tem dono único, tempo de vida maior que a transferência, alinhamento e região de memória válidos para o periférico. | DMA escreve depois de a função retornar; pilha local ou memória desalinhada corrompe dados (V-16, V-32 para ESP-IDF). | `grep -nE 'HAL_.*DMA\|spi_.*trans\|uart_.*dma'` e confira de onde vem o buffer (pilha local é achado). |
| C-07 | Sem recursão. | Pilha limitada; o `.su` do GCC não limita recursão (V-09, V-59). | `clang-tidy -checks='misc-no-recursion'` (Inferido); `-fstack-usage` mostrando `dynamic`. |
| C-08 | Tabelas e constantes `const` ficam em flash; `static` em escopo de arquivo para o que não é API. | RAM é escassa; símbolo global sem necessidade vira acoplamento e colisão de nomes (V-09 trata `static` para linkage interno). | `-Wmissing-prototypes -Wmissing-variable-declarations` (clang) e `size -A`. |

## C tipos e atomicidade

| ID | Regra | Motivo | Detecção |
| --- | --- | --- | --- |
| C-09 | Inteiros de largura fixa (`uint8_t`, `int32_t`) em registradores, protocolos e estruturas compartilhadas; `size_t` para tamanhos. | `int` e `long` mudam de largura entre alvos (8, 16, 32 e 64 bits); layout de pacote muda junto. | `grep -nE '\b(int\|unsigned\|long\|short)\b' src/` ; `-Wconversion -Wsign-conversion`. |
| C-10 | `volatile` só para registrador mapeado e flag escrita em ISR. Ele não dá atomicidade nem ordem de memória. Leitura-modificação-escrita (`cnt++`) ou dado multi-palavra compartilhado exige atômico, seção crítica ou fila. | A fonte STM32 usa `volatile` para ISR/registrador; CERT SIG31-C e o Rust Book mostram que isso não basta (V-14, V-12, K-04). | `grep -nE 'volatile'` e, para cada variável, liste escritores e leitores; vá a `rtos-concurrency-review`. |
| C-11 | Nenhum cast remove `const` ou `volatile`. | Escreve em flash/ROM ou deixa o compilador otimizar acesso a registrador (V-09). | `-Wcast-qual`. |
| C-12 | Aritmética de tempo usa subtração com sinal sobre contadores que dão a volta: `(int32_t)(agora - prazo) >= 0`. | Comparar `agora >= prazo` quebra no wrap do tick (32 bits de milissegundos dão a volta em cerca de 49,7 dias). O período é aritmética; a técnica é idiomática (Inferido). | `grep -nE 'tick\|millis\|HAL_GetTick\|k_uptime\|xTaskGetTickCount'` e leia comparações `<`/`>=`. |

## D fluxo e estilo defensivo

| ID | Regra | Motivo | Detecção |
| --- | --- | --- | --- |
| C-13 | `switch` tem `default`; cadeia `if/else if` termina em `else` quando o conjunto de casos é fechado; fallthrough é explícito. | Valor inesperado (estado corrompido) cai em silêncio (V-09). | `-Wswitch-default -Wimplicit-fallthrough`. |
| C-14 | Macros com parênteses em parâmetros e no corpo; função `static inline` quando possível; include guard ou `#pragma once` consistente com o projeto (V-10 usa `#pragma once`). | Precedência de operadores em macro gera bug que só aparece com certos argumentos. | `clang-tidy -checks='bugprone-macro-parentheses'` (Inferido); `grep -nE '#define\s+\w+\(' src/`. |
| C-15 | Sem código comentado nem inalcançável; código desativado só com comentário que explica o porquê (V-10). | Código morto engana quem lê e apodrece. | `-Wunreachable-code` (clang); `grep -nE '^\s*//\s*(if\|for\|HAL_\|return)'`. |

## E robustez de campo

| ID | Regra | Motivo | Detecção |
| --- | --- | --- | --- |
| C-16 | Watchdog ligado desde a inicialização; fault handler registra motivo de reset, registradores de falha e versão do build em memória que sobrevive ao reset; toda espera (semáforo, fila, barramento, DMA) tem timeout finito justificado pelo pior caso do periférico. Watchdog é último recurso, não correção (V-28). | Falha em campo sem registro não é depurável; espera infinita transforma falha transitória em travamento permanente (V-16, V-30). | `grep -nE 'portMAX_DELAY\|HAL_MAX_DELAY\|K_FOREVER\|WAIT_FOREVER\|osWaitForever\|, *-1\)'`; procurar `HardFault_Handler`, `esp_reset_reason`, `hwinfo_get_reset_cause`. |

## Como usar a coluna Detecção

0. Nas tabelas acima, `\|` é o escape de barra vertical do Markdown: no comando real use `|` simples (alternância do `grep -E`).
1. Rode o grep sobre o escopo da revisão e leia cada ocorrência; o grep acha candidatos, não defeitos.
2. Espera infinita só é aceitável com justificativa por escrito (por exemplo, tarefa que dorme até evento, sem recurso preso). Registre a justificativa ou o achado.
3. Quando o repositório define wrappers (`MY_CHECK(x)`), troque o padrão do grep pelo nome do wrapper e leia a definição uma vez.
4. Regra do projeto vence regra deste arquivo se estiver escrita (CLAUDE.md, guia de estilo). Cite a regra do projeto como fonte do achado.
5. Para cada regra violada, o campo "Verificar" do achado deve nomear um teste de host com HAL falsa, uma opção de compilador ou uma medição; veja `firmware-test-host`.
