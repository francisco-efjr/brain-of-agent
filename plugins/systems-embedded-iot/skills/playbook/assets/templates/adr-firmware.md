# ADR [ID] - [decisão de firmware]

Adaptado de `adr.md` do brain-of-agent (MIT, Francisco Edson). Use para decisão com custo de reversão alto: RTOS, política de memória, mapa de memória e partições, modo de swap/OTA, estados de energia, topologia de barramentos, chaves.

Estado: [proposta / aceita / substituída] · Data / revisão: [identificação] · Autor: [papel]

## Contexto

Problema, requisitos e restrições com números e fonte: flash, RAM, corrente média, latência, temperatura, volume, equipe. Alvo (MCU + revisão), framework e versão. O que depende de datasheet e ainda é Não verificável: [lista].

## Opções

| Opção | Benefício | Custo / risco | Compatibilidade (alvo, toolchain, bootloader) | Evidência (V-nn, medição, datasheet) |
| --- | --- | --- | --- | --- |

## Decisão

Opção escolhida e por quê. Hipóteses ainda não confirmadas: [...].

## Política de memória e orçamentos iniciais

Política (bare metal / ESP-IDF / Zephyr / Rust): [...]. Orçamento de flash, RAM e pilha com método de medição: [...].

## Consequências

Complexidade, operação, teste (host x alvo), segurança, OTA e energia afetados. Reversibilidade: o que não volta (eFuse, partições gravadas em campo, chave publicada). Plano de recuperação: [...].

## Decisões que exigem humano

[chaves, eFuse, secure boot, proteção de leitura, anti-rollback, gravação em bancada]

## Validação e revisão

Critérios observáveis, experimento ou teste que sustenta a escolha; condição que exige reconsiderar; links para requisito e artefatos.
