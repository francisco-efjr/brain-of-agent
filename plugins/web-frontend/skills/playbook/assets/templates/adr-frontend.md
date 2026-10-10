# ADR-[número]: [decisão de frontend em uma frase]

Estado: [proposta / aceita / substituída por ADR-nn] · Data: [AAAA-MM-DD] · Decisor humano: [nome]

Use só para decisão material de frontend: modelo de cache (com ou sem `cacheComponents`), estratégia de renderização por rota, biblioteca de estado ou de formulários, migração de versão. Não use para escolha local e reversível. Se o sistema já tem ADRs, referencie o ADR do sistema (`/architecture-design:playbook`). Base: `adr.md` do brain-of-agent (MIT), adaptado.

## Contexto

Problema, restrições, requisitos e evidências. Versões lidas do `package.json` e da config: [framework, versão, flags]. Stack existente: [lista]. Métricas atuais: [LCP, INP, CLS ou outras, com condições].

## Opções

| Opção | Benefício | Custo e risco | Compatibilidade com o projeto | Evidência (fonte ou medição) |
| --- | --- | --- | --- | --- |
| Não mudar nada | | | | |
| [opção A] | | | | |
| [opção B] | | | | |

## Decisão

Opção escolhida e por quê. Hipóteses ainda não confirmadas (rotule Suposição): [lista].

## Consequências

Complexidade, bundle e desempenho, testes afetados, impacto em SEO e acessibilidade, dependência de plataforma de hospedagem (pedido de integração a `/devops-cloud-infra:playbook` se houver). Limites de reversibilidade e como reverter: [passos].

## Validação e revisão

Critérios observáveis (por exemplo LCP até 2,5 s no p75 em rota X, testes verdes, sem aviso de hidratação). Experimento ou teste que sustenta a escolha: [descrição]. Condição que exige reconsiderar: [gatilho]. Links para requisito e artefatos: [lista].
