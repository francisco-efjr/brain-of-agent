# Orçamentos de firmware: pilha, flash/RAM, energia e matriz MISRA

Uso: modo `orcamento` e modo `misra` da skill `firmware-review`. Fontes: V-59 (GCC), V-49 (Zephyr threads), V-52 (FreeRTOS), V-39 (sleep modes do ESP-IDF), V-58 (cppcheck), V-14 (CERT e MISRA), lidas em 2026-10-10. O que não vem dessas fontes vem marcado Inferido (conhecimento estável do domínio; confirme na versão instalada). Nenhum valor numérico de projeto de terceiros é usado.

Sumário: [Pilha](#pilha) · [Flash e RAM](#flash-e-ram) · [Energia](#energia) · [Matriz MISRA](#matriz-misra) · [Tabela de resultado](#tabela-de-resultado)

Regra geral: estimativa do compilador não é pior caso. Número só entra como Verificado quando existe comando e saída colada; sem medição é Suposição. Medição que exige rodar o firmware na placa passa pelo gate de `hw-bench-loop`.

## Pilha

1. **Gerar** o `.su`: compile com `-fstack-usage` (CMake: `-DCMAKE_C_FLAGS="-fstack-usage"`; PlatformIO: `build_flags = -fstack-usage`). Cada objeto gera um `.su` com linhas `arquivo.c:linha:coluna:funcao<TAB>bytes<TAB>qualificador`; o qualificador é `static`, `dynamic` ou `dynamic,bounded` (V-59).
2. **Ler o qualificador**: `static` é o consumo fixo do quadro; `dynamic` significa que a função ajusta a pilha no corpo (VLA, `alloca`); sem `bounded` o número cobre só a parte estaticamente limitada, ou seja, é piso, não teto (V-59). Função com `dynamic` sem `bounded` no caminho crítico é achado.
3. **Montar o caminho mais fundo por contexto**. O GCC não imprime o grafo de chamadas no `.su`; opções: `-fcallgraph-info=su` (GCC 10 ou superior, Inferido) ou rastreio manual a partir do ponto de entrada, incluindo chamadas por ponteiro de função (liste os destinos possíveis; ponteiro sem lista é Não verificável). Some: quadros da cadeia + custo de entrada de exceção + chamadas de biblioteca (`printf`, `snprintf`, TLS, parsers) que não têm `.su` no seu build.
4. **Custo de exceção no Cortex-M** (Inferido, confira o manual da variante): o hardware empilha 8 palavras (32 bytes) na entrada de uma exceção; com contexto de ponto flutuante ativo o quadro estendido é maior. ISR usa a pilha corrente (MSP em bare metal; com FreeRTOS no Cortex-M a ISR usa MSP e as tarefas usam PSP, Inferido). Interrupções aninhadas somam quadros.
5. **Confirmar no alvo** com marca d'água, em build de teste e sob a carga do pior caso (mensagem máxima, caminho de erro, log ligado, reconexão):
   - FreeRTOS: `uxTaskGetStackHighWaterMark()` devolve a menor folga desde o início (V-52). Atenção à unidade: no kernel original é em palavras de pilha (`StackType_t`); no FreeRTOS do ESP-IDF a pilha é dada em bytes (Inferido; confira na porta). Ligue `configCHECK_FOR_STACK_OVERFLOW` (métodos 1 e 2 não garantem detecção; o hook roda em contexto de interrupção e só deve registrar e parar; V-52).
   - Zephyr: `k_thread_stack_space_get()` exige `CONFIG_INIT_STACKS` e `CONFIG_THREAD_STACK_INFO`; `CONFIG_THREAD_RUNTIME_STACK_SAFETY` adiciona limiar por thread com handler (V-49). `CONFIG_THREAD_ANALYZER` imprime uso periódico (Inferido).
6. **Registrar** em `orcamentos.md`: por contexto, estimativa estática, medida, carga usada, folga e quem aprovou a margem. A política de margem (por exemplo, "medido + 25%") é decisão do projeto: Suposição até estar no CLAUDE.md.

Exemplo de cálculo (valores hipotéticos para mostrar o método, não são de nenhum projeto):

| Contexto | Cadeia mais funda | Estático (bytes) | Medido (bytes) | Obs |
| --- | --- | --- | --- | --- |
| tarefa `net` | `net_task` > `mqtt_poll` > `tls_read` > `snprintf` | 640 (sem `snprintf`, que não tem `.su`) | Não medido | `snprintf` de newlib com ponto flutuante pesa; medir |
| ISR UART | `USART2_IRQHandler` > `rb_push` | 48 + quadro de exceção | Não medido | `rb_push` sem `dynamic` |

Leitura do exemplo: a estimativa estática é piso; a linha só vira "Verificado" quando a coluna Medido tem valor e há comando e saída anexos.

## Flash e RAM

Comandos de medição (todos de host; nenhum grava a placa):

```bash
arm-none-eabi-size -A -d build/app.elf                         # seções em formato sysv
arm-none-eabi-nm -S --size-sort -C build/app.elf | tail -n 25  # 25 maiores símbolos
# link com mapa e uso por região (GNU ld):
#   -Wl,-Map=build/app.map -Wl,--print-memory-usage -ffunction-sections -fdata-sections -Wl,--gc-sections
idf.py size ; idf.py size-components ; idf.py size-files       # ESP-IDF (builds sem gravar)
west build -t rom_report ; west build -t ram_report            # Zephyr
```

Os alvos `rom_report`/`ram_report` do Zephyr e `size-components` do ESP-IDF são conhecimento estável, não relidos nesta rodada (Inferido). `pio run` sem `-t upload` apenas compila.

Quando o link falha com `region 'FLASH' overflowed by N bytes` ou `section '.bss' will not fit in region 'RAM'`:
1. Confirme que os tamanhos de região no linker script batem com o datasheet da variante exata; sem o datasheet, o tamanho real é Não verificável (use `datasheet-first`).
2. Gere o mapa e a lista dos maiores símbolos antes de cortar qualquer coisa.
3. Candidatos frequentes (Inferido): suporte a `printf` com ponto flutuante na libc (`-u _printf_float` em newlib-nano), strings de log, tabelas grandes que não estão em `const`, bibliotecas inteiras ligadas por um único uso, símbolos do Kconfig/`sdkconfig` ligados sem necessidade, build de debug sem `-Os`, exceções e RTTI de C++ (`-fno-exceptions -fno-rtti`), reserva de heap e pilha no linker script (por exemplo `_Min_Heap_Size` e `_Min_Stack_Size` nos scripts gerados pelo CubeMX), que contam como RAM mesmo sem uso.
4. Corte uma coisa por vez e remeça o `size`. Reporte o antes e o depois em bytes, não em porcentagem solta.

## Energia

Fonte principal: sleep modes do ESP-IDF (V-39). Guias da Nordic e da ST e a página de power management do Zephyr (última atualização da fonte em abril de 2022, V-40) estão fora de cobertura: para esses alvos, diga "Não verificável" e peça a documentação do fabricante.

1. **Fases**: ativo (CPU e rádio), modem-sleep, light-sleep, deep-sleep, e o pico de transmissão. Light-sleep mantém estados internos com clock gating e tensão reduzida; deep-sleep desliga CPUs, quase toda a RAM e periféricos digitais, mantendo RTC controller, ULP e RTC FAST/SLOW; o rádio (Wi-Fi/BT) fica desligado em ambos, e para manter conexão a fonte indica modem-sleep com light-sleep automático (V-39).
2. **Corrente é medida na própria placa**, com o firmware real, instrumento adequado (multímetro de precisão ou analisador de consumo; picos curtos exigem amostragem rápida: Inferido), registrando versão do build, tensão de alimentação e data. Placas de desenvolvimento incluem LEDs, regulador e ponte USB-serial que consomem corrente; meça no módulo ou descreva o que ficou ligado (Inferido).
3. **Antes de entrar em deep-sleep** (checklist da fonte V-39 e derivados): rádio parado, `rtc_gpio_isolate()` nos pinos que não devem puxar corrente por pull interno, dados que sobrevivem marcados em memória RTC, fontes de wake-up configuradas (timer, touchpad, ext0, ext1, ULP, GPIO; UART só em light-sleep).
4. **Média ponderada** (aritmética, vale com valores medidos): `I_med = soma(I_i * t_i) / T` sobre um ciclo completo; autonomia ideal = capacidade / `I_med`. Capacidade útil real depende de temperatura, autodescarga e corte de tensão da célula, que vêm da folha da bateria (Suposição até citar).
5. **Definição de pronto**: tabela com corrente por fase, método, instrumento, build e data. Valor de datasheet ou de blog não substitui medição na sua placa.

## Matriz MISRA

Objetivo: documentar a política de análise estática, não repetir a norma. O texto oficial é pago e não entra no plugin (V-14, V-58).

1. **Edição e categorias**: C:2012 ou C:2023 (a de 2023 consolida a de 2012 com corrigenda 1 e 2 e emendas 1 a 4; V-14); categorias mandatory, required, advisory; diretrizes (Dir) e regras (Rule) em listas separadas.
2. **Cobertura por ferramenta**: o addon MISRA do cppcheck cobre quase todas as regras de C:2012 com emendas; as regras 1.1 e 1.2 não são tratadas e devem ser verificadas pelos compiladores (V-58). O comando do addon e o arquivo de textos de regras não estão na página lida; o uso usual é `cppcheck --addon=misra.json` com o caminho do arquivo de textos fornecido pelo detentor da licença (Inferido; confira a documentação do cppcheck instalado). C:2023 não está na página lida (Não verificável para o cppcheck).
3. **Preencher**: uma linha por regra adotada, com cobertura (cppcheck, compilador, revisão manual, não coberta), status atual e desvio com razão e aprovador. Use os identificadores da cópia licenciada do projeto; não cole o texto das regras.
4. **Rastrear regra do Zephyr**: a página de diretrizes se descreve como subconjunto de MISRA-C 2012 e ao mesmo tempo permite alocação no kernel; a numeração citada por terceiros já divergiu (V-09). Releia a versão em uso antes de citar um número.
5. **Analogia CERT**: SIG31-C trata handler de sinal (só `volatile sig_atomic_t` e atômicos lock-free; handler que apenas marca flag e retorna); para ISR é analogia (Inferido, V-14).

Modelo pronto: `matriz-misra.md` em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/`.

## Tabela de resultado

| Orçamento | Método e comando | Resultado | Folga | Rótulo |
| --- | --- | --- | --- | --- |
| Pilha por contexto | `-fstack-usage` + marca d'água sob carga | por contexto | por contexto | Verificado se houver saída; senão Suposição |
| Flash e RAM | `size -A` + mapa | por região | bytes livres | Verificado se houver saída |
| Energia | instrumento + build + data | por fase | autonomia calculada | Verificado só com medição na placa |
