# ADR-[NNN]: Modelo de tenancy de [PRODUTO]

Status: [proposto | aceito | substituído por ADR-NNN] · Data: [AAAA-MM-DD] · Decisores: [nomes] · Rótulos: Verificado, Inferido, Suposição, Não verificável.

Preencha com dados do projeto. Pergunte ao usuário só o que muda a decisão, uma pergunta por vez; o que faltar vira Suposição declarada. Fontes: `V-07`, `V-33`, `V-44` em `references/fontes.md`.

## 1. Contexto

- Produto e quem paga: [..]
- Definição de tenant: [empresa | organização | família/grupo | outro]. Um cliente pode ter vários tenants? [sim/não]
- Stack: [linguagem, framework, ORM, Postgres e versão, pooler, auth/IdP, billing e versão da API]
- Restrições: [compliance, residência de dados, prazo, equipe]

## 2. As 6 perguntas (V-07)

| # | Pergunta | Resposta | Rótulo |
| --- | --- | --- | --- |
| 1 | Quem é o tenant e um cliente pode ter vários? | | |
| 2 | Há exigência regulatória ou contratual de separação física? | | |
| 3 | Quantos tenants em 3 anos e qual o maior? | | |
| 4 | Isolamento é vendido como plano (enterprise)? | | |
| 5 | O que pode ser compartilhado por camada (UI, aplicação, dados)? | | |
| 6 | Como mapear requisição → tenant → deployment? | | |

## 3. Opções por camada

| Camada | Opção A | Opção B | Opção C |
| --- | --- | --- | --- |
| UI | | | |
| Aplicação | | | |
| Dados | pool + RLS | schema por tenant (**relato de praticante**, V-44) | banco/instância por tenant (silo) |
| Prós | | | |
| Contras | | | |
| Custo e operação | | | |

Padrão se o usuário não decidir: pool + RLS para planos comuns; silo para chave própria, residência de dados ou isolamento físico; **nunca** tabela ou coluna por tenant; migração de schema automatizada com versão por tenant (V-33).

## 4. Decisão

[Modelo por camada, em uma frase cada.] Mapa tenant → deployment: [tabela ou serviço de diretório]. Mapeamento da requisição: [claim | subdomínio | outro] com validação de audience e scope (V-32).

## 5. Consequências e riscos

| Risco | Probabilidade/impacto | Mitigação | Teste que prova |
| --- | --- | --- | --- |
| Vazamento entre tenants por filtro esquecido | | RLS + `FORCE` + role sem `BYPASSRLS` | suíte de dois tenants |
| Noisy neighbor | | limites por tenant (V-09) | teste de carga em ambiente descartável |
| Complexidade de migração | | automação e versão por tenant | migração em N tenants com falha isolada |

## 6. Critérios de mudança de modelo

[Gatilhos: chave própria, residência, tenant que degrada os demais, RTO/RPO diferenciado. Valores são Suposição até o produto definir.] Plano de migração entre modelos: [cópia por tenant, reconciliação por partição, janela, reversão].

## 7. Ligações

Ciclo de vida do tenant (V-30): [link]. Billing (um Customer por tenant, V-39): [decisão]. Noisy neighbor: [link]. Auditoria: [link].

## 8. Pendências e Suposições

- [..]
