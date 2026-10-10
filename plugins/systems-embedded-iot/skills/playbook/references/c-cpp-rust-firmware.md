# C, C++ e Rust no firmware

Fontes: V-09, V-10, V-11, V-12, V-13, V-14, V-16, V-47, V-48, V-53, V-54, V-55, V-56, V-58, V-59 (ver `fontes.md`). Regra do plugin: nenhum texto de MISRA, CERT ou do Rust Book é reproduzido; os checklists abaixo são redação própria. Antes de citar número de regra, releia a versão atual da fonte.

Sumário: 1. C embarcado em 15 itens · 2. ESP-IDF style · 3. Análise estática: clang-tidy, cppcheck, MISRA · 4. Analyzer e sanitizers · 5. C++ de firmware (lacuna) · 6. Rust no_std · 7. Formato de achado.

## 1. C embarcado: checklist de revisão em 15 itens (V-09, V-10, V-14, V-16)

Cada item tem a razão em uma frase e a opção "rastrear regra": leia a página atual do Zephyr (`/contribute/coding_guidelines/`) antes de citar número. A página se descreve como subconjunto de MISRA-C 2012.

| # | Item | Razão | Como verificar |
| --- | --- | --- | --- |
| 1 | Toda chamada que devolve status é checada; ignorar de propósito usa `(void)` | Erro silencioso vira falha tardia e sem pista | `-Wunused-result`, clang-tidy `bugprone-unused-return-value`, revisão |
| 2 | Erro recuperável retorna código; `assert` só para erro interno irrecuperável e sem efeito colateral na expressão | `assert` some em build de release; efeito colateral some junto | grep `assert(` com chamada dentro |
| 3 | Recursos adquiridos são liberados em todos os caminhos de erro | Vazamento em campo derruba o produto em semanas | revisão por caminho; `-fanalyzer` em C como complemento |
| 4 | Sem alocação dinâmica após init, salvo política do projeto (P-09); ISR nunca aloca | Fragmentação e tempo não determinístico | grep `malloc|calloc|realloc|new` e política no CLAUDE.md |
| 5 | Sem recursão; sem VLA/`alloca` | Pilha limitada e não analisável | `-Wvla`, grafo de chamadas |
| 6 | Não remover `const` ou `volatile` por cast | Quebra a garantia do tipo e o acesso a registrador | `-Wcast-qual` |
| 7 | `static` para linkage interno; tabelas imutáveis `const` (ficam em flash) | Reduz RAM e superfície de colisão | `nm`/`.map` mostra `.data` indevido |
| 8 | Inteiros de largura fixa (`uint32_t`) e conversões explícitas | `int` muda entre portes | `-Wconversion`, clang-tidy |
| 9 | `volatile` só para registrador e flag de ISR; não é atomicidade nem ordem | RMW perdido; multi-palavra rasga | ver `rtos-interrupcoes-e-recursos.md` seção 4 |
| 10 | `switch` com `default`; cadeia `if/else if` termina em `else` | Estado novo não pode passar despercebido | `-Wswitch-default` |
| 11 | Macros com parênteses em parâmetros e no corpo; preferir `static inline` e `enum` | Precedência e dupla avaliação | clang-tidy `bugprone-macro-parentheses` |
| 12 | Sem código comentado nem inalcançável; código desativado só com comentário que explica o motivo | Ruído que apodrece | revisão |
| 13 | Include guard (`#pragma once` ou `#ifndef`) em todo header; protótipos visíveis | Dupla definição e chamada sem protótipo | build limpo com `-Wmissing-prototypes` |
| 14 | Watchdog desde o início; fault handler registra motivo de reset, registradores de falha e versão do build | Campo sem pista é bug eterno | revisão do handler |
| 15 | Toda espera tem timeout finito justificado pelo pior caso do periférico | Travar é pior que falhar | grep `HAL_MAX_DELAY|portMAX_DELAY|K_FOREVER|-1` e justificativa |

Notas de fidelidade (V-09): a página do Zephyr tem Dir 4.12 (sem alocação dinâmica) mas regras adicionais permitem `malloc` e correlatos no kernel, sem reconciliar (K-07); "Rule 8.7" não existe na página (é 8.8) e "sem código comentado" é Dir 4.4. Por isso o plugin não numera.

## 2. ESP-IDF style (V-10, conferido na versão `latest`)

Erro recuperável retorna código; `assert` só para erro interno irrecuperável e sem efeito colateral; `ESP_ERROR_CHECK` para `esp_err_t` irrecuperável (e só em inicialização fatal, nunca em caminho de campo recuperável: prática do plugin, Inferido); `(void)` para variável não usada; `#pragma once`; 4 espaços, 120 colunas, astyle; sem código comentado; prefixo `s_` em estáticas. O guia **não cobre ISR/IRAM**: em callbacks de ISR use o checklist de `rtos-interrupcoes-e-recursos.md`; funções chamadas com flash desabilitado precisam estar em IRAM (Inferido; confira o atributo `IRAM_ATTR` e as flags na doc da versão).

## 3. Análise estática (V-13, V-14, V-58)

**clang-tidy** (V-13). Pré-requisito: `compile_commands.json` (`-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`). Comandos sugeridos, não executados sem pedido:

```text
clang-tidy -p build -checks='-*,bugprone-*,cert-*,misc-*' -warnings-as-errors='*' src/driver.c
clang-tidy -list-checks -checks='cert-*'
```

`-checks=` aceita globs e prefixo `-`; famílias `bugprone-`, `cert-`, `misc-`, `cppcoreguidelines-`, `readability-`; `NOLINT` precisa de motivo; `--fix` só com diff revisado. **Com toolchain cruzado** (`--target`, `--sysroot`, headers do `arm-none-eabi`) o comportamento não foi verificado: Não verificável até testar no projeto. Pistas comuns: `-- --target=arm-none-eabi --sysroot=<caminho>` após `--`, ou ajuste no `compile_commands.json` (Inferido).

**cppcheck + MISRA** (V-58). O addon cobre quase todas as regras do MISRA C:2012 incluindo as emendas; as regras 1.1 e 1.2 não são tratadas e devem ser verificadas pelos compiladores. A página não traz o comando do addon, a licença do texto das regras nem MISRA C:2023: confira na documentação instalada. **O texto da MISRA é pago e não entra no plugin.**

**Matriz MISRA** (use `assets/templates/matriz-misra.md`): qual edição (C:2012 ou C:2023, que consolida a 2012 com corrigenda 1 e 2 e emendas 1 a 4), quais categorias (mandatory, required, advisory), quais regras o cppcheck cobre, quais só o compilador, quais o time desvia e **por quê** (V-14). O plugin nunca afirma conformidade; Zephyr declara IEC 61508 como meta, não certificação (V-60).

## 4. `-fanalyzer`, `-fstack-usage` e sanitizers (V-59)

- `-fanalyzer`: execução simbólica interprocedural, "neither sound nor complete", mais cara que os outros avisos e **"only suitable for use on C code in this release"**. Avisos `-Wanalyzer-*` (null-dereference, use-after-free, double-free, malloc-leak, out-of-bounds, fd-leak, valor não inicializado). Complemento, nunca prova.
- Sanitizers **no host** (lógica de domínio compilada para PC): `-fsanitize=address,undefined` (ou `thread`; ASan e TSan não combinam), com `-g` e `-O0/-O1/-Og`; não combine `-Werror` com sanitizers. No alvo embarcado, sanitizers raramente cabem: Inferido.
- `-fstack-usage`: ver `rtos-interrupcoes-e-recursos.md` seção 5. `-Wstack-usage=` pode estar em Warning Options (não lida): confira.
- `-fstack-protector` e variantes existem; custo e suporte dependem da toolchain (Inferido).

## 5. C++ de firmware (lacuna: sem fonte validada)

A única regra de C++ encontrada na pesquisa era de C++ de desktop (SOLID, `std::filesystem`, exceções) e foi rebaixada. O que segue é orientação **Inferida** (conhecimento estável de toolchains GCC/Clang), a conferir na documentação da sua toolchain e do seu framework:

| Tema | Orientação | Rótulo |
| --- | --- | --- |
| Exceções e RTTI | Muitos projetos desligam (`-fno-exceptions -fno-rtti`) por tamanho e previsibilidade; ESP-IDF e Zephyr têm opções de Kconfig/sdkconfig próprias: conferir | Inferido |
| Alocação | `new`/`delete` e contêineres da STL alocam: aplique a política P-09; prefira buffers estáticos, `std::array` e tipos de capacidade fixa | Inferido |
| `constexpr` e tabelas | Tabelas calculadas em compilação ficam em flash; confirme no `.map` | Inferido |
| Inicialização estática | Ordem de construtores globais entre unidades é indefinida; evite dependência de hardware em construtores globais | Inferido |
| Biblioteca padrão | Ambiente "freestanding" oferece subconjunto; `std::optional`/`std::expected` dependem da versão do padrão e da libstdc++ da toolchain | Não verificável sem a toolchain |
| ISR e C++ | Callbacks de ISR com assinatura C (`extern "C"`) e sem alocação, como em C | Inferido |

## 6. Rust `no_std`

Fontes: V-11, V-12, V-47, V-48, V-53, V-54, V-55, V-56. Livros em CC-BY-SA: só destilação. Registre a versão de cada crate (`cargo tree`).

- **Panic handler (V-11).** Exatamente um `#[panic_handler]` com `fn(&PanicInfo) -> !` no grafo de dependências. Crates `panic-halt`, `panic-abort`, `panic-itm`, `panic-semihosting`; `use panic_halt as _;`; escolha por perfil com `cfg(debug_assertions)`; breakpoint em `rust_begin_unwind` ao depurar. Em campo, o handler deveria registrar o motivo e reiniciar de forma controlada (Inferido, decisão de produto).
- **Concorrência com interrupção (V-12).** `static mut` tocado por interrupção perde atualização em leitura-modificação-escrita e é um achado de revisão. Use `Mutex<RefCell<Option<T>>>` com token de critical section, atômicos (Cortex-M0/M0+ só load/store; M3+ com CAS; `Relaxed` basta em núcleo único) ou filas. Inicialize antes de habilitar a interrupção. Handler que espera lock da thread principal pode travar. Critical section não protege entre núcleos. Nas edições recentes do Rust, referências a `static mut` são avisadas ou negadas por lint (`static_mut_refs`): Inferido, confira a edição do projeto.
- **embedded-hal 1.0 (V-47).** Driver genérico sobre os traits (`I2c`, `SpiDevice`, `OutputPin`, `DelayNs`), não sobre o tipo de um HAL; testes usam implementação falsa dos traits (ver `testes-e-bancada.md`); módulos bloqueantes em `embedded-hal`, `embedded-hal-async` para async e `embedded-hal-nb` para polling (não lidos em detalhe). Versão lida: 1.0.0, MIT ou Apache-2.0; confira `latest`.
- **SVD e svd2rust (V-48).** svd2rust gera structs de mapa de registradores a partir de SVD. Nome de registrador, campo e interrupção vem do SVD da **variante exata**, com versão e origem registradas; divergência entre SVD e manual de referência é achado, não decisão do modelo.
- **Embassy (V-53).** Framework async com executor que suspende o núcleo sem trabalho e múltiplos executores com prioridades. Sem espera bloqueante dentro de tarefa. "Sem alocação dinâmica" é declaração do projeto: verifique no crate usado (K-13).
- **RTIC v2 (V-54).** Tarefas de hardware ligadas a interrupções (NVIC escolhe pela prioridade), tarefas de software em executores async, teto por Stack Resource Policy calculado em compilação, execução até o fim em pilha única, sem deadlock. Recurso entre prioridades passa pelo mecanismo de recursos do RTIC, não por `static mut`.
- **probe-rs e defmt (V-55).** probe-rs grava e depura ARM/RISC-V por SWD/JTAG, com RTT para logs; `cargo-flash`/`cargo-embed` gravam. **`download`, `flash`, `erase`, `reset`, `write-mem` e `run` são escrita (gate); `list`, `info`, `read-mem` e `rtt` são leitura.** `probe-rs run` grava antes de abrir o RTT. defmt: strings internadas, níveis `error/warn/info/debug/trace`, transportes `defmt-rtt`, `defmt-itm`, `defmt-semihosting`; `DEFMT_LOG` não lido.
- **Embedonomicon (V-56).** Referência para arranque e linker script (`cortex-m-rt` etc.), não receita de produção.
- **Runner perigoso.** `.cargo/config.toml` com `runner = "probe-rs run ..."` faz `cargo run`/`cargo test` gravarem a placa (Inferido). Para teste de host use `--target <triplo do host>` após conferir o arquivo.
- Lacuna: nenhum AGENTS.md ou skill de Rust `no_std` com licença clara; `embedded-hal-async` e `DEFMT_LOG` não lidos.

Exemplo de achado (Rust):

```rust
static mut TICKS: u32 = 0;                      // lido na main, escrito na interrupção
#[interrupt] fn TIM2() { unsafe { TICKS += 1; } } // RMW sem proteção
```

Correção sugerida: `AtomicU32` com `fetch_add(1, Ordering::Relaxed)` em núcleo único (V-12) ou `Mutex<Cell<u32>>` com critical section. Rótulo: Verificado (visível no trecho) para o padrão; Inferido para o impacto em campo.

## 7. Formato de achado de revisão de código

`ID · severidade (crítica/alta/média/baixa) · confiança 1-10 · arquivo:linha · regra/fonte V-nn · evidência (trecho) · cenário concreto · correção · como verificar · rótulo`. Em dúvida abaixo de confiança 6, não reporte como achado: mova para "Não verificado".
