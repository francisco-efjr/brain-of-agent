---
name: postmortem-notas-com-culpa
description: "Mede a redação de um postmortem blameless a partir de notas que nomeiam pessoas e misturam estimativas, verificando papéis em vez de nomes, linha do tempo com fonte, horários de memória como Inferido, números rotulados, falha de detecção como contribuinte, ações com dono e prazo a definir, causa raiz como hipótese e seção Não sabemos ainda."
tags: [sre-observability, postmortem, blameless]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um postmortem completo sem nomes de pessoas como causa (usa papéis), com linha do tempo em que cada evento tem fonte e rótulo, horários aproximados como Inferido e fuso e ano a confirmar, 1.200 pedidos como estimativa, detecção por cliente sem alerta como causa contribuinte de sistema, ações com dono e prazo a definir para aprovação humana, causa raiz como hipótese, seção Não sabemos ainda, status Rascunho; não inventa horários nem números."
model: sonnet
---
Preciso do postmortem do incidente de segunda. Estas são as notas que juntei do canal #incidentes e do que o pessoal lembra:

- Seg 03/08, ~22:10 BRT: o João fez o deploy da v3.2 sem rodar o teste de migração
- Logo depois a tabela orders travou (a migração segurou um lock longo); checkout fora ~47 min
- ~1.200 pedidos falharam (estimativa do Pedro, não conferimos no banco)
- 22:57 BRT: o Carlos fez o rollback e o checkout voltou
- Ninguém avisou o suporte; ficamos sabendo pelo Twitter
- Nenhum alerta disparou

Escreve o postmortem completo.
