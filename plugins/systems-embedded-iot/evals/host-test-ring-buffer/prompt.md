---
name: host-test-ring-buffer
description: "Mede o disparo de firmware-test-host e a qualidade de testes Unity para um buffer circular, em Windows, sem depender de placa e sem afirmar execução."
tags: [systems-embedded-iot, testes, unity, host, firmware-test-host]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega testes Unity que cobrem vazio, cheio, wrap-around, ordem FIFO, capacidade 1 e ponteiro nulo ou comportamento documentado, sem depender de placa, orienta rodar no Windows via toolchain nativa, MSYS2 ou WSL, diz como executar e que não executou (ou cola saída real), e menciona vermelho antes de verde."
model: sonnet
---
Escreve testes unitários com Unity para rodar no meu PC (uso Windows) antes de eu levar para a placa. É um buffer circular de bytes:

```c
typedef struct { uint8_t *buf; size_t cap, head, tail, len; } rb_t;
void rb_init(rb_t *r, uint8_t *storage, size_t cap);
int  rb_push(rb_t *r, uint8_t b);   /* 0 ok, -1 cheio */
int  rb_pop(rb_t *r, uint8_t *out); /* 0 ok, -1 vazio */
```

Mostra os testes aqui na resposta.
