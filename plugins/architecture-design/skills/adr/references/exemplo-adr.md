# Exemplo de ADR e checklist aplicado

Sumário: 1. Pedido de exemplo · 2. Saída esperada da skill · 3. Checklist aplicado · 4. Como o exemplo erraria

Exemplo ilustrativo e fictício: nomes, números e decisores são inventados para mostrar o formato; os números estão rotulados Suposição de propósito. Base: V-12, V-13, V-14.

## 1. Pedido de exemplo

> "Decidimos usar PostgreSQL em vez de DynamoDB para o serviço de pedidos. Time de 4 pessoas, consultas relacionais, ~200 req/s de pico (estimativa nossa). Também vamos renomear `tmp` para `orderDraft`. Registre as decisões. Quem decidiu foi a Marina (tech lead)."

## 2. Saída esperada da skill

```markdown
Gatekeeper
- Banco do serviço de pedidos: aceito (estrutural, cara de reverter: migração de dados).
- Renomear `tmp` para `orderDraft`: rejeitado (estágio 1; detalhe de implementação) -> nenhum registro.
Relacionados: nenhum ADR encontrado em docs/adr/ (pasta inexistente).

# ADR-0001: PostgreSQL como banco do serviço de pedidos
Status: proposto · Data: 2026-10-10 · Decidido por: Marina (tech lead), informado pelo usuário · Confiança: média

## Contexto
O serviço de pedidos precisa de consultas relacionais (pedido, itens, cliente, filtros por status e período) e transações entre pedido e itens. O time tem 4 pessoas e experiência prévia com SQL. Pico estimado: ~200 req/s (Suposição: estimativa do time, não medida). Não há requisito de multirregião ativo-ativo declarado.

## Decisão
Vamos usar PostgreSQL gerenciado como banco principal do serviço de pedidos.

## Alternativas
| Opção | Prós | Contras | Motivo da rejeição |
| --- | --- | --- | --- |
| Não mudar nada (manter pedidos no banco do monólito) | Zero migração; uma única transação com cadastro | Acopla o esquema de pedidos ao do monólito; deploys conjuntos | Não resolve a necessidade de isolar o serviço (Suposição: motivo informado pelo usuário, confirmar) |
| DynamoDB | Escala horizontal gerenciada; sem servidor de banco para operar | Consultas relacionais exigem desenho de acesso prévio e índices secundários; curva de aprendizado para o time | Consultas ad hoc por status e período são o caso de uso central |
| PostgreSQL gerenciado | Transações, SQL, experiência do time | Escala de escrita vertical primeiro; operação de réplicas e backups | Escolhida |

## Consequências
- Positivas: transações entre pedido e itens; consultas flexíveis; menor curva de aprendizado.
- Negativas: limite de escala de escrita de um único primário; custo de operar réplicas, backups e upgrades; migração futura para particionamento exige trabalho.
- Neutras: o contrato HTTP do serviço não muda.
- Reversibilidade: trocar de banco depois exige migração de dados e reescrita de acesso; não é uma decisão de um commit.

## Gatilhos de reavaliação
- Pico de escrita sustentado acima de ~1.000 req/s por 7 dias (Suposição: limiar a confirmar com benchmark do time).
- Requisito de multirregião ativo-ativo.
- Time maior que 10 pessoas com ciclos de entrega independentes por módulo.

## Links
- Pendências: [NEEDS CLARIFICATION] quem aprova a mudança de status para `aceito`?; [NEEDS CLARIFICATION] por que o banco do monólito não serve (motivo de isolamento).
```

## 3. Checklist aplicado

| Item | Resultado |
| --- | --- |
| Nome `adr-0001-postgresql-banco-pedidos.md`, data ISO | Sim |
| >= 2 alternativas, uma "não mudar nada", com motivo | Sim (3 linhas) |
| >= 1 positiva e >= 1 negativa | Sim |
| Confiança declarada | Média (decisão baseada em experiência do time e estimativa não medida) |
| Números medidos ou rotulados | 200 req/s e 1.000 req/s rotulados Suposição |
| Decisor humano nomeado | Marina, conforme o usuário; não inventado |
| Nenhuma promessa de rollback de dados | Sim |

## 4. Como o exemplo erraria

- Criar ADR para a renomeação de `tmp`: viola o gatekeeper.
- Escrever "decidido por: equipe" sem nome: decisão sem dono.
- Omitir "não mudar nada" ou deixar a lista de contras do PostgreSQL vazia: ADR vira propaganda.
- Gravar `docs/adr/adr-0001-...md` sem mostrar o rascunho e pedir aprovação: papel da skill `adr-write`, com aprovação explícita.
