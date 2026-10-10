# Depuração com probe: parar, ler, liberar, com os limites do gate

Uso: consulta da skill `firmware-root-cause` (e do agente `firmware-debugger`, que **não** executa nada daqui). Fecha a pendência do crítico: fluxo de depuração com GDB/OpenOCD/probe-rs com leitura de registradores de falha com o alvo parado, mantendo o gate de hardware. Fontes lidas em 2026-10-10: V-55 (probe-rs e defmt: gravam e depuram ARM e RISC-V por SWD/JTAG, memória, run/halt, breakpoints, reset, RTT; ferramentas `probe-rs`, `cargo-flash`, `cargo-embed`), V-62 (probe-rs na skill de terceiros: escrita é alto risco, leitura baixo; chip e endereço nunca são adivinhados), V-21 (ambiguidade para o fluxo e lista candidatos), V-51 (`west flash`, `west debug`, `--erase` gravam), V-27 (portão), V-19 (humano no circuito). Sintaxe exata de cada ferramenta varia por versão: confira `--help` antes de qualquer comando; os comandos abaixo ilustram a classe da operação, não são receita.

Sumário: [Classes de operação](#classes-de-operação) · [Antes de conectar](#antes-de-conectar) · [Roteiro parar-ler-liberar](#roteiro-parar-ler-liberar) · [Comandos de leitura que ilustram o roteiro](#comandos-de-leitura-que-ilustram-o-roteiro) · [Cartão do gate leve](#cartão-do-gate-leve) · [O que nunca entra aqui](#o-que-nunca-entra-aqui)

## Classes de operação

| Classe | Operações | Regra |
| --- | --- | --- |
| Livre (host) | listar probes e portas; abrir ELF e `.map`; `addr2line`/`objdump` sobre o ELF; decodificar core dump salvo; ler logs já gravados | Sem efeito no alvo. Passa pelo prompt normal de permissão do Bash quando é comando |
| Gate leve | conectar a um alvo em execução; parar o núcleo; ler registradores do núcleo, SCB, RAM e pilha; retomar a execução sem alterar estado | Pergunte antes e mostre o cartão abaixo: parar o núcleo tem efeito físico indireto |
| Gate | gravar, apagar, resetar, escrever memória ou registrador, alterar breakpoints em flash que reprogramem, `probe-rs run`/`download`/`erase`/`reset`, `cargo flash`/`embed`, `west flash`/`debug`/`--erase`, `idf.py flash`, `openocd ... program`, monitor serial que reseta | Exige o ciclo completo de `hw-bench-loop`: cartão de gravação, confirmação explícita no chat, registro de evidência |
| Recusar | eFuse/OTP, chaves de secure boot, criptografia de flash, proteção permanente de leitura, anti-rollback | Encaminhe a `ota-security-review`; sem comando copiável |

Observação de V-55: `probe-rs run` grava antes de abrir o RTT; ele pertence ao Gate, mesmo parecendo "só observar".

## Antes de conectar

1. **Alvo e probe inequívocos.** Se houver mais de um probe ou porta, liste os candidatos e pare (V-21). Chip informado pelo usuário, nunca adivinhado (V-62).
2. **Estado seguro dos atuadores.** Parar o núcleo mantém saídas no último estado; periféricos como temporizadores de PWM podem continuar rodando. Peça confirmação de que a carga está desligada ou em estado seguro.
3. **Watchdog.** O watchdog independente pode reiniciar o alvo enquanto o núcleo está parado, a menos que o fabricante o congele em depuração. Sem saber, o usuário precisa aceitar que o alvo pode resetar e apagar o estado que se queria ver.
4. **Sessões concorrentes.** Pare outras sessões de depuração antes (V-61: parar sessões de depuração antes de gravar); duas ferramentas no mesmo probe se atrapalham.
5. **Windows e drivers.** Trocar o driver do J-Link para WinUSB pode quebrar as ferramentas da SEGGER (V-21). Não altere drivers por conta própria; é configuração do sistema, decisão do usuário.
6. **Símbolos.** Tenha o ELF exato do firmware em execução; build diferente dá linhas erradas.

## Roteiro parar-ler-liberar

1. **Conectar sem reset e sem gravação** (opção de "attach" da ferramenta, conferida no `--help`). Nunca use modo que programa a flash na conexão.
2. **Parar** o núcleo. Anote o horário e o estado de watchdog observado.
3. **Ler** o mínimo necessário:
   - registradores do núcleo (PC, LR, SP, xPSR) e, em Cortex-M3 ou superior, os registradores de status de falha (CFSR e relacionados, [cortex-m-faults.md](cortex-m-faults.md));
   - a região da pilha da tarefa ativa e o valor do SP;
   - variáveis globais relevantes por símbolo (contadores, estado de máquina).
   Evite ler registradores de dados de periféricos (UART, ADC, SPI): ler pode limpar flags ou esvaziar FIFO (Inferido).
4. **Liberar**: retomar a execução. Se a retomada exigir reset, é Gate.
5. **Registrar** os valores lidos e a interpretação no relatório de causa raiz: dado lido é Verificado; interpretação é Inferido até a correção provar.

## Comandos de leitura que ilustram o roteiro

Ilustrações de sintaxe estável de GDB (conectado a um servidor de depuração já iniciado pelo usuário). Não são pré-aprovados: cada comando de Bash passa pelo prompt de permissão, e a conexão passa pelo gate leve.

```text
(gdb) info registers                 # núcleo: r0-r12, sp, lr, pc, xpsr
(gdb) x/16xw $sp                     # 16 palavras a partir do topo da pilha
(gdb) p/x *(unsigned int *)0xE000ED28   # CFSR no ARMv7-M; confirmar no manual
(gdb) bt                             # pilha de chamadas, se o SP e o ELF forem consistentes
(gdb) info threads                   # com RTOS aware, tarefas e estados
```

Em OpenOCD, `mdw <endereço> <n>` lê palavras de memória e `reg` mostra registradores do núcleo; `halt`, `resume` e `reset` alteram o estado de execução (`reset` e `program` são Gate). Em probe-rs, listar probes e informações do alvo é leitura; `read`/`write` de memória e `reset` seguem a classificação da tabela (escrita e reset são Gate). Em todos os casos, confira o `--help` da versão (V-55, V-62).

Quando o firmware tem RTT com `defmt` (probe-rs), o log estruturado chega ao host sem parar o núcleo; abrir RTT por ferramenta que também grava é Gate (V-55).

## Cartão do gate leve

Mostre antes de conectar e espere um "confirmo" no chat:

```text
Gate leve: parar o núcleo para leitura
Alvo: <placa e part number>        Probe/porta: <id>      ELF: <caminho, hash curto>
Operações: conectar sem reset e sem gravação; parar; ler núcleo, SCB, RAM, pilha; retomar
Riscos: atuadores mantêm o último estado; watchdog pode resetar; temporização do produto muda
Estado seguro confirmado pelo usuário: <sim/não>      Duração prevista: <segundos>
Fora de escopo: gravar, apagar, resetar, escrever memória ou registrador
```

## O que nunca entra aqui

- Agente `firmware-debugger`: lê, analisa e propõe; sem probe, sem flash, sem monitor de placa. Se a investigação exigir probe, ele devolve ao agente principal o pedido com o comando exato.
- Comando de eFuse, de chave ou de proteção permanente.
- Alterar drivers USB, regras de sistema ou configuração do probe sem decisão do usuário.
- API HTTP de bancada sem autenticação e MCP de hardware ativo (V-29, V-61): não usar nem instalar a partir deste plugin.
