# Cortex-M: decodificar uma falha e capturar o quadro empilhado

Uso: consulta da skill `firmware-root-cause`. Fonte: conhecimento estável da arquitetura Arm (ARMv7-M, ARMv8-M) e das convenções de compilador GCC; **não relido nesta rodada**, portanto tudo aqui é **Inferido**: confirme nomes, endereços e bits no manual da variante (Technical Reference Manual do núcleo e reference manual do fabricante) antes de afirmar em relatório. Relacionado, com fonte lida: V-52 (FreeRTOS: overflow e `configASSERT`), V-22 (método). Lidas em 2026-10-10.

Sumário: [Quando serve](#quando-serve) · [O quadro empilhado](#o-quadro-empilhado) · [Registradores de status de falha](#registradores-de-status-de-falha) · [Handler de exemplo](#handler-de-exemplo) · [Ler o resultado](#ler-o-resultado) · [Cortex-M0 e M0+](#cortex-m0-e-m0) · [Outras plataformas](#outras-plataformas)

## Quando serve

Cortex-M com HardFault, MemManage, BusFault ou UsageFault. Para ESP32, Zephyr e RTOS com tratador de pânico próprio, use o motivo de reset e o backtrace da plataforma ([catalogo-de-hipoteses.md](catalogo-de-hipoteses.md#motivo-de-reset-por-plataforma)).

## O quadro empilhado

Na entrada de uma exceção o hardware empilha oito palavras na pilha ativa, nesta ordem a partir do topo: R0, R1, R2, R3, R12, LR, PC, xPSR. O PC empilhado aponta para a instrução que falhava (em falha precisa) ou para uma próxima (em falha imprecisa). O valor de LR na entrada da exceção, `EXC_RETURN`, indica qual pilha estava ativa: o bit 2 igual a 1 indica a pilha de processo (PSP, tarefas de RTOS); igual a 0, a pilha principal (MSP). Com unidade de ponto flutuante e contexto ativo, o quadro é estendido (mais palavras); o layout das oito primeiras permanece (Inferido).

## Registradores de status de falha

Existem no ARMv7-M (Cortex-M3, M4, M7) e no ARMv8-M com extensão principal; não existem no ARMv6-M (M0, M0+). Estão no bloco de controle do sistema (SCB). Endereços do ARMv7-M, a confirmar no manual: CFSR em 0xE000ED28, HFSR em 0xE000ED2C, MMFAR em 0xE000ED34, BFAR em 0xE000ED38. Em CMSIS: `SCB->CFSR`, `SCB->HFSR`, `SCB->MMFAR`, `SCB->BFAR`.

O CFSR agrupa três campos: MMFSR (bits 7 a 0), BFSR (bits 15 a 8) e UFSR (bits 31 a 16).

| Bit (nome) | Significado | Leitura típica |
| --- | --- | --- |
| MMFSR.IACCVIOL (0) | busca de instrução em região proibida (MPU ou mapa) | salto para endereço inválido; ponteiro de função corrompido |
| MMFSR.DACCVIOL (1) | acesso a dados proibido | ponteiro nulo ou fora de região; veja MMFAR se o bit MMARVALID (7) estiver ligado |
| MMFSR.MSTKERR (4) / MUNSTKERR (3) | falha ao empilhar / desempilhar | pilha apontando para região inválida: estouro de pilha |
| BFSR.IBUSERR (8) | erro de barramento na busca de instrução | salto para região sem memória |
| BFSR.PRECISERR (9) | erro de barramento preciso em dados | endereço em BFAR (se BFARVALID, bit 15) aponta o acesso |
| BFSR.IMPRECISERR (10) | erro de barramento impreciso | escrita em buffer que falhou depois; PC não aponta o culpado |
| BFSR.STKERR (12) / UNSTKERR (11) | erro de barramento ao empilhar / desempilhar | pilha em região inválida; estouro de pilha |
| UFSR.UNDEFINSTR (16) | instrução indefinida | código corrompido, salto para dado, instrução não suportada pelo núcleo |
| UFSR.INVSTATE (17) | estado inválido de execução | salto para endereço com bit de Thumb zerado (ponteiro de função sem bit 0) |
| UFSR.INVPC (18) | PC inválido no retorno de exceção | pilha corrompida durante a exceção |
| UFSR.NOCP (19) | acesso a coprocessador ausente | uso de ponto flutuante com a FPU desligada |
| UFSR.UNALIGNED (24) | acesso desalinhado com trap habilitado | cast de ponteiro para tipo maior que o alinhamento |
| UFSR.DIVBYZERO (25) | divisão por zero com trap habilitado | validar divisor |

O HFSR indica que a falha foi escalada para HardFault (FORCED no bit 30 sinaliza falha configurável escalada; VECTTBL no bit 1, erro na leitura da tabela de vetores). Confirme tudo no manual da variante.

## Handler de exemplo

Padrão comum para GCC em Cortex-M3 ou superior. Escolhe a pilha correta, chama uma função C com o ponteiro do quadro e guarda o contexto em memória que sobrevive ao reset. Valide o assembler e as seções no toolchain do projeto antes de adotar (Inferido).

```c
#include <stdint.h>

typedef struct {
    uint32_t r0, r1, r2, r3, r12, lr, pc, xpsr;
    uint32_t cfsr, hfsr, mmfar, bfar;
    uint32_t magic;              /* marca de validade do registro */
} fault_record_t;

#define FAULT_MAGIC 0xFA17C0DEu

/* seção que o startup não zera; confirme o nome da seção no linker script do projeto */
__attribute__((section(".noinit"))) static volatile fault_record_t g_fault;

void hardfault_c(const uint32_t *sp)
{
    g_fault.r0 = sp[0]; g_fault.r1 = sp[1]; g_fault.r2 = sp[2]; g_fault.r3 = sp[3];
    g_fault.r12 = sp[4]; g_fault.lr = sp[5]; g_fault.pc = sp[6]; g_fault.xpsr = sp[7];
    g_fault.cfsr  = *(volatile uint32_t *)0xE000ED28u;   /* confirmar no manual */
    g_fault.hfsr  = *(volatile uint32_t *)0xE000ED2Cu;
    g_fault.mmfar = *(volatile uint32_t *)0xE000ED34u;
    g_fault.bfar  = *(volatile uint32_t *)0xE000ED38u;
    g_fault.magic = FAULT_MAGIC;
    /* política do produto: reset controlado (NVIC_SystemReset) ou parada para depuração */
    for (;;) { }
}

__attribute__((naked)) void HardFault_Handler(void)
{
    __asm volatile (
        "tst lr, #4        \n"
        "ite eq            \n"
        "mrseq r0, msp     \n"
        "mrsne r0, psp     \n"
        "b hardfault_c     \n"
    );
}
```

No boot seguinte: se `g_fault.magic == FAULT_MAGIC`, imprima o registro (inclua a versão do build), apague a marca e siga. Sem essa persistência o dado se perde no reset.

## Ler o resultado

1. **PC e LR para linha de código**: `arm-none-eabi-addr2line -e build/app.elf -f -p -C -i <PC>`; para LR (endereço de retorno com bit 0 ligado) remova o bit 0 antes. Confirme que o ELF é exatamente o que está no dispositivo (mesmo build); build diferente dá linha errada.
2. **Ver o código ao redor**: `arm-none-eabi-objdump -d -S build/app.elf | less` e localize o endereço.
3. **Tipo de falha**: cruze os bits do CFSR com a tabela acima. Exemplo de leitura (valores hipotéticos): DACCVIOL ligado com MMFAR perto de zero indica acesso de dados através de ponteiro nulo ou de índice negativo; STKERR ligado com SP fora da região da tarefa indica estouro de pilha.
4. **Contexto**: qual tarefa estava ativa (com RTOS, o ponteiro de tarefa corrente), qual ISR (campo de número de exceção no `IPSR` dentro do xPSR empilhado: bits 8 a 0, Inferido).
5. **Registre** o dado no relatório como Verificado se vier de saída real colada, e a interpretação como Inferido até confirmada pela correção e pelo teste.

## Cortex-M0 e M0+

ARMv6-M não tem CFSR, HFSR, MMFAR nem BFAR, não tem a instrução `ite` do assembler acima (o handler precisa de ramificação simples em vez de instrução condicional por IT) e tem apenas HardFault para todas as falhas. O quadro empilhado continua disponível; o diagnóstico depende de PC, LR, SP e de instrumentação do código (por exemplo, marcar etapas). Confirme no manual do núcleo (Inferido).

## Outras plataformas

- ESP32: motivo de reset por `esp_reset_reason()`, backtrace de pânico e core dump; decodificação com o ELF do build. Veja o catálogo.
- Zephyr: o log de erro fatal imprime registradores; o motivo de reset é obtido pela API de informação de hardware. Veja o catálogo.
- FreeRTOS: `configASSERT`, hook de overflow de pilha e hook de falha de `malloc` são os pontos de captura; o hook de overflow roda em contexto de interrupção e só deve registrar e parar (V-52).
