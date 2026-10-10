# Parecer de prontidão: <release ou funcionalidade, data>

Como usar: comece pela recomendação; separe o que foi verificado (com evidência) do que não foi. Cada risco residual vem na forma "se… então…", com probabilidade, detecção, contorno e quem aceita. "GO com condições" exige condições verificáveis e um dono para cada uma. O parecer é informação para decisão, não garantia de ausência de defeitos; recomendar rollback ou deploy não executa nenhum dos dois. Critérios: `references/estrategia-e-risco.md` e `references/checklist-completo.md`. Adaptado do brain-of-agent (MIT).

**Recomendação:** <GO / GO com condições / NO-GO>
**Resumo (2 ou 3 linhas para quem não vai ler o resto):** <...>
**Tipo de liberação:** <completa / gradual (canary) / atrás de flag, com etapas>

**Verificado** (comando, versão e ambiente de cada evidência): <suítes, ambientes, plataformas, números>
**Não verificado** (e por quê): <...>

| Critério de prontidão | Estado | Evidência |
| --- | --- | --- |
| Zero crítico aberto no escopo; altos com contorno e aceite | <OK / PENDENTE / FALHOU> | <link ou ID> |
| Smoke e regressão crítica verdes em pré-produção equivalente à produção | | |
| Riscos altos mitigados ou aceitos formalmente | | |
| Desempenho e segurança verificados, ou risco declarado | | |
| Migração e rollback (ou roll-forward) ensaiados, com tempo medido | | |
| Painel e alertas para o comportamento novo; plantão sabe o que olhar | | |
| Flag ou kill switch, quando aplicável | | |
| Suporte e áreas afetadas informados | | |

**Riscos residuais aceitos:**

| Risco (se… então…) | Probabilidade | Como detectamos | Contorno | Aceito por | Data |
| --- | --- | --- | --- | --- | --- |
| <se a transportadora B falhar, clientes do Norte veem "frete indisponível" e não compram> | <baixa: por quê> | <alerta de erro de cotação em minutos> | <flag volta à tabela antiga em menos de 5 min> | <PO> | <data> |

**Condições para GO** (verificável + dono): <...>
**Plano pós-release:** <o que monitorar, por quanto tempo, checkpoints, critério objetivo de rollback e quem decide>
**Decisão:** <decisor · papel · decisão · data e hora>
