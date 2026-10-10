# ADR [ID] — [decisão de infraestrutura]

<!--
Use só para decisão material (ferramenta, backend de state, estratégia de rollout, modelo de segredos,
plataforma). Não crie ADR para cada linha de configuração. Base: adr.md do brain-of-agent (MIT),
adaptado com campos de custo, operação, reversibilidade e state. Sem segredos.
-->

Estado: [proposta / aceita / substituída por ADR-xxx] · Data e revisão do código: [DATA] · [SHA]

## Contexto

Problema, restrições, requisitos, evidências e stack existente: [TEXTO]. Ambiente(s): [dev / staging / produção]. Fontes (com rótulo): [V-nn, docs oficiais, medições].

## Opções

| Opção | Benefício | Custo e risco | Operação (quem opera, on-call) | Reversibilidade e state | Evidência |
| --- | --- | --- | --- | --- | --- |
| A. [ex.: Terraform com state em S3 e lock] | | | | | |
| B. [ex.: OpenTofu com criptografia de state] | | | | | |
| C. Não mudar | | | | | |

## Decisão

Opção escolhida e por quê: [TEXTO]. Hipóteses ainda não confirmadas (Suposição): [LISTA].

## Consequências

- Complexidade e operação: [TEXTO]
- Custo (estimativa; Infracost ou calculadora do provedor, Suposição até medir): [VALOR]
- Segurança (superfície nova, permissões, segredos): [TEXTO]
- State e dados: [onde ficam, quem acessa, backup e restauração]
- Migração: [passos, janela, compatibilidade entre versões]
- Limites de reversibilidade: [o que não volta; não prometa rollback de dados perdidos só porque existe um passo "down"]

## Validação e revisão

- Critérios observáveis (comando ou métrica) que sustentam a escolha: [LISTA]
- Teste ou experimento: [DESCRIÇÃO]
- Condição que exige reconsiderar: [GATILHO]
- Links: requisito, plano de mudança (`plano-mudanca-infra.md`), PR.
