# Rust `no_std`: concorrência com interrupção, panic handler, RTIC e Embassy

Uso: consulta da skill `rtos-concurrency-review` quando o código é Rust embarcado. Fontes: V-11 (panic handler), V-12 (concorrência), V-53 (Embassy), V-54 (RTIC v2), V-47 (embedded-hal), lidas em 2026-10-10. O Rust Book embarcado é CC BY-SA: o texto abaixo é redação própria; os exemplos de código são originais deste plugin. Versões de crates mudam: registre a versão no relatório e confira o `latest` antes de recomendar API. Não existe, nas fontes lidas, AGENTS.md ou skill de Rust `no_std` com licença clara (lacuna 5 do design): o que está aqui vem da documentação.

Sumário: [Achados típicos](#achados-típicos) · [Padrão com seção crítica](#padrão-com-seção-crítica) · [Atômicos](#atômicos) · [Panic handler](#panic-handler) · [RTIC](#rtic) · [Embassy](#embassy) · [Perguntas de revisão](#perguntas-de-revisão)

## Achados típicos

| Padrão | Por que é achado | Severidade usual | Fonte |
| --- | --- | --- | --- |
| `static mut` tocado por handler de interrupção e por `main` | Leitura-modificação-escrita perde atualização quando a interrupção ocorre entre leitura e escrita; o compilador pode otimizar acessos | alta | V-12 |
| `unsafe { COUNTER += 1 }` em handler sem seção crítica nem atômico | Idem; `unsafe` aqui afirma uma garantia que o código não dá | alta | V-12 |
| Estado inicializado depois de habilitar a interrupção | Handler vê valor não inicializado | alta | V-12 |
| Handler que espera um lock detido pela thread principal | A thread principal não roda enquanto o handler espera: travamento | alta | V-12 |
| Seção crítica usada como proteção entre dois núcleos | Seção crítica desabilita interrupções do núcleo local; não exclui o outro núcleo | alta | V-12 |
| Dois `#[panic_handler]` (ou nenhum) no grafo de dependências | Erro de link: o handler deve existir exatamente uma vez | média | V-11 |
| Espera bloqueante (laço ocupado, `delay` síncrono longo) dentro de tarefa Embassy | Impede o executor de rodar as outras tarefas | alta | V-53 |
| Recurso compartilhado entre tarefas RTIC de prioridades diferentes por `static mut` | Contorna a política de teto de recurso que evita corrida e deadlock | alta | V-54 |
| Driver amarrado ao tipo de um HAL específico em vez dos traits | Impede teste no host e reuso (ver `datasheet-first`) | baixa | V-47 |

## Padrão com seção crítica

Contador tocado por uma interrupção e lido em `main`. Ruim:

```rust
static mut TICKS: u32 = 0;

#[interrupt]
fn TIM2() {
    unsafe { TICKS += 1; }          // RMW sem proteção
}
```

Preferível, com `cortex-m` (a API `cortex_m::interrupt::Mutex` exige o token da seção crítica para acessar o dado; verifique a versão do crate e, se o projeto usa `critical-section`, o equivalente `critical_section::Mutex`):

```rust
use core::cell::RefCell;
use cortex_m::interrupt::{self, Mutex};

static TICKS: Mutex<RefCell<u32>> = Mutex::new(RefCell::new(0));

#[interrupt]
fn TIM2() {
    interrupt::free(|cs| {
        *TICKS.borrow(cs).borrow_mut() += 1;
    });
}

fn ticks_now() -> u32 {
    interrupt::free(|cs| *TICKS.borrow(cs).borrow())
}
```

Pontos de revisão (V-12): o acesso só existe dentro da seção crítica; o dado é inicializado antes de a interrupção ser habilitada (`unmask`); a seção é curta no sentido mensurável (latência máxima de interrupção), não em número de linhas; em dois núcleos a seção crítica local não basta (use a primitiva da plataforma).

Para tipos que não cabem em um atômico (por exemplo, `Option<Buffer>` entregue da interrupção para `main`), o padrão do livro é `Mutex<RefCell<Option<T>>>`: a interrupção faz `replace(Some(...))`, o laço principal faz `take()` dentro de `interrupt::free`. Uma fila SPSC sem espera (crates como `heapless` oferecem; confira a versão e a licença) é a alternativa quando há fluxo contínuo.

## Atômicos

- Cortex-M0 e M0+ só têm load e store atômicos: `fetch_add` e `compare_exchange` não existem em hardware; crates como `portable-atomic` emulam com seção crítica (Inferido; confira a documentação). Cortex-M3 ou superior tem compare-and-swap (V-12).
- `Ordering::Relaxed` basta quando só um núcleo acessa e o que importa é a atomicidade de uma variável isolada (V-12). Para publicar dados por flag entre contextos (escrever buffer, depois sinalizar), use `Release` na escrita do flag e `Acquire` na leitura (Inferido, modelo de memória do Rust).
- Atômico protege uma variável; invariantes entre duas variáveis ainda pedem seção crítica.

## Panic handler

Regras (V-11): `#[panic_handler]` com assinatura `fn(&PanicInfo) -> !`, exatamente uma vez no grafo de dependências; crates comuns: `panic-halt`, `panic-abort`, `panic-itm`, `panic-semihosting`, usados com `use panic_halt as _;`; a escolha pode variar por perfil com `cfg(debug_assertions)`; para depurar, ponha breakpoint em `rust_begin_unwind`. `extern crate` é estilo anterior à edição 2018.

Revisão: o que o produto faz ao entrar em pânico em campo? Halt sem reset deixa o dispositivo mudo; combine com watchdog ou reset controlado e registro do motivo (ver `firmware-root-cause`). `panic-semihosting` pode parar o alvo se não houver depurador conectado (Inferido): não usar em produção.

## RTIC

RTIC v2 (V-54): tarefas de hardware ligadas a interrupções (o NVIC escolhe pela prioridade) e tarefas de software em executores async, um por prioridade; Stack Resource Policy com teto calculado em compilação; execução até o fim em uma pilha única, sem deadlock por construção; arquitetura explícita Cortex-M (RISC-V com CLIC mencionado). Revisão:
1. Recurso compartilhado entre prioridades diferentes passa pelo mecanismo de recursos (`#[shared]` com `lock`), nunca por `static mut`.
2. Prioridades justificadas por escrito, como em qualquer RTOS.
3. Versão do crate registrada (a documentação do livro v2 pode divergir de v1).

## Embassy

Embassy (V-53): framework "Rust e async"; executor que suspende o núcleo quando não há trabalho; múltiplos executores com prioridades; módulo de tempo; HALs async para STM32, nRF, RP e outros. Licença MIT ou Apache-2.0 à escolha, documentação CC-BY-SA. Revisão:
1. Nenhuma espera bloqueante dentro de tarefa: use `Timer::after(...).await`, canais e sinais do Embassy.
2. Executor e prioridades documentados; tarefa de interrupção de alta prioridade em executor próprio.
3. A afirmação "sem alocação dinâmica" é declaração do projeto (K-13): confirme no crate que o produto usa antes de repetir.
4. Versão do crate registrada.

## Perguntas de revisão

1. Quais variáveis `static` existem e qual contexto escreve cada uma?
2. Há `unsafe`? Para cada bloco, que invariante o autor afirma e quem a garante?
3. A interrupção é habilitada (unmask) depois da inicialização de todos os dados que ela toca?
4. O alvo tem um ou dois núcleos? A proteção usada vale para isso?
5. Existe exatamente um panic handler e o comportamento em produção está definido?
6. O driver é genérico sobre `embedded-hal` 1.0 e testável no host com implementação falsa? (versão 1.0.0 na leitura de 2026-10-10; confira `latest`)

Rótulos: tudo que veio de V-11, V-12, V-53 e V-54 e foi lido é Verificado; comportamentos de `portable-atomic`, `heapless`, `panic-semihosting` e modelo `Acquire/Release` são Inferido até conferência na versão do projeto.
