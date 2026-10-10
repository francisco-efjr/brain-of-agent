# ADR [ID]: [decisão de dados]

Estado: [proposta | aceita | substituída por [ID]] · Data/revisão: [AAAA-MM-DD, identificação]
Adaptado do template de ADR do Brain of Agent (MIT, © 2026 Brain of Agent contributors).

## Contexto

Problema, requisitos, restrições, volume, evidências (planos, medições) e stack existente: [engine e versão, ORM, tenancy atual].

## Opções

| Opção | Benefício | Custo/risco | Compatibilidade | Evidência (rótulo) |
| --- | --- | --- | --- | --- |
| [ex.: banco compartilhado com RLS] | | | | |
| [ex.: banco por tenant] | | | | |

## Decisão

[Opção escolhida e por quê. Hipóteses ainda não confirmadas marcadas como Suposição.]
Áreas cobertas: [tenancy | particionamento | isolamento | engine | outra].

## Consequências

Complexidade, operação, migração, segurança, testes e custo. Reversibilidade: o que reverte com código, o que exige restauração de backup. Não prometa rollback de dados perdidos só porque existe migração "down".

## Validação e revisão

Critérios observáveis (testes, medições, ensaio em cópia). Gatilho de revisão: [ex.: mais de 500 tenants; p95 acima de X; mudança de versão do SGBD]. Links: [requisito, ADR de arquitetura, plano de migração].
