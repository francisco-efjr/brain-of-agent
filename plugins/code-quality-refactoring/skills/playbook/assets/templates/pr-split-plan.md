# Plano de divisão de mudança grande

Mudança: [descrição]  ·  Tamanho atual: [N linhas, M arquivos]  ·  Limiar do projeto: [~400 linhas / 10 arquivos, Suposição ajustável]

Princípios: refatoração pura separada de mudança de comportamento; cada commit autocontido, com testes e suíte verde; PRs empilhados quando um depende do outro. Orientação do Google: cerca de 100 linhas costuma ser razoável, cerca de 1000 é grande demais, a critério do revisor.

| # | Commit/PR | Tipo (refatoração pura / comportamento / testes / migração) | Arquivos | Linhas | Depende de | Verificação (comando) | Revisor sugerido |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [ex.: extrair `_tarifa_base`] | refatoração pura | | | nenhum | [suíte antes = depois] | |
| 2 | [ex.: nova regra X] | comportamento | | | 1 | [teste novo + suíte] | |

Ordem de merge: [1 -> 2 -> ...]. Riscos: [conflitos, flags, migrações].
Commit, push e abertura de PR só com pedido explícito do usuário; estratégia de branches e merge é de `git-workflow-release`.
