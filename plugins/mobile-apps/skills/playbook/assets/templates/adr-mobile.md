# ADR [ID]: [decisão]

Adaptado do template `adr` do brain-of-agent (MIT, Francisco Edson). Use só para decisão material com alternativas reais (framework, arquitetura de UI, estratégia offline, pipeline). Salve em `docs/adr/`. Referencie o ADR de sistema de `/architecture-design:playbook` quando houver.

Estado: [proposta / aceita / substituída] · Data: [AAAA-MM-DD] · Dono humano da decisão: [nome]
Plataformas e versões lidas: [ex.: Android AGP 8.x, Kotlin 2.x, minSdk 26] (verificado em [data])

## Contexto

Problema, restrições, requisitos e evidências. Stack e arquitetura existentes (arquivos). Ambiente do time (SO, macOS disponível?). Fatos voláteis envolvidos (target API, regras de loja) com data de verificação.

## Opções

| Opção | Benefício | Custo e risco | Compatibilidade com o repositório | Evidência (V-nn ou medição) |
| --- | --- | --- | --- | --- |
| Não mudar nada | [ex.: zero risco imediato] | [ex.: bug recorrente continua] | Total | [ex.: 3 incidentes] |
| [Opção A] | | | | |
| [Opção B] | | | | |

## Decisão

Opção escolhida e por quê. Hipóteses ainda não confirmadas (rotule Suposição). Quem decidiu.

## Consequências

Complexidade, operação, dados, migração local, segurança, testes e loja afetados. Limites de reversibilidade e de recuperação: não prometa rollback de dados perdidos só porque existe migração. Para OTA, registre que a fonte não descreve rollback e aponte a documentação.

## Validação e revisão

Critérios observáveis (comando, métrica, teste) que sustentam a escolha. Condição que exige reconsiderar a decisão (ex.: SDK major novo, mudança de regra de loja). Links para requisito e artefatos.
