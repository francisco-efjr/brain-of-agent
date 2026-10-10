# Tarefas: [NOME DA FEATURE]

**Spec:** [caminho] (aprovada em [data]) · **Gate G2:** [aprovação do plano, data]

Formato, inspirado no template de tarefas do spec-kit (GitHub, MIT): `T001 [P] [US1] descrição com caminho/exato/do/arquivo`. `[P]` só com arquivo distinto e sem dependência de tarefa incompleta. Substitua os itens de exemplo; nenhum deve sobrar. Testes vêm primeiro apenas se a spec pedir.

## Fase 1: Setup

- [ ] T001 [descrição, `caminho/arquivo`]
- [ ] T002 [P] [descrição, `caminho/outro-arquivo`]

## Fase 2: Fundação *(bloqueia todas as histórias)*

- [ ] T003 [descrição, `caminho/arquivo`] · cobre FR-[n]

**Checkpoint da fundação:** [comando ou evidência que prova que está pronta].

## Fase 3: História 1 (P1): [título]

- [ ] T004 [US1] [descrição, `caminho/arquivo`] · cobre FR-[n]
- [ ] T005 [P] [US1] [descrição, `caminho/outro-arquivo`] · cobre FR-[n]

**Checkpoint da história 1:** [teste independente da spec, executável].

## Fase 4: História 2 (P2): [título]

- [ ] T006 [US2] [descrição, `caminho/arquivo`] · cobre FR-[n]

**Checkpoint da história 2:** [teste independente].

## Fase N: Polish

- [ ] T0NN [descrição: documentação, limpeza, verificação final de SC]

## Dependências

[T003 bloqueia T004 e T006; T005 independe de T004.] *(sem ciclos)*

## Cobertura

| FR | Tarefas | Check |
| --- | --- | --- |
| FR-001 | T004 | [comando ou teste] |
