---
name: debt-triage-hotspots
description: "Mede a priorização de dívida técnica por frequência de mudança vezes dor, não por feiura: estável e feio vai para o fim, dívida deliberada exige dono e prazo, números citam a fonte e nada é corrigido."
tags: [code-quality-refactoring, tech-debt-triage, prioritization]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Ordena por frequência de mudança vezes dor com os dados colados, põe os módulos estáveis e feios no fim, classifica quadrantes, exige dono e prazo para a dívida deliberada, cita a origem dos números e não altera código."
model: sonnet
---
Preciso decidir o que atacar de dívida técnica no próximo trimestre. Tenho 2 devs por 6 semanas. Segue o que levantei no repositório do backend de faturamento.

Commits por arquivo nos últimos 6 meses (`git log --since="6 months ago" --name-only`):

```text
48 src/billing/invoice.py
36 src/orders/pricing.py
31 src/billing/tax.py
27 src/auth/session.py
22 src/api/handlers.py
14 src/utils/dates.py
 2 src/legacy/report_v1.py
 1 src/legacy/xml_export.py
 0 src/core/old_scheduler.py
```

Minhas anotações sobre os que acho feios:
- `invoice.py`: função gigante de 600 linhas; 9 bugs de produção ligados a ela nesses 6 meses.
- `pricing.py`: lógica duplicada com `tax.py`; 4 bugs no período.
- `session.py`: 14 TODO/FIXME e um workaround com o comentário "por ora, depois a gente arruma" que ninguém assumiu; 2 incidentes.
- `report_v1.py`: 2.000 linhas de código horrível, mas só mexemos duas vezes e nunca deu bug.
- `xml_export.py`: feio, estável, 1 commit.
- `old_scheduler.py`: obsoleto, ninguém mexe, funciona.

Me ajuda a priorizar. Não precisa mexer em código agora.
