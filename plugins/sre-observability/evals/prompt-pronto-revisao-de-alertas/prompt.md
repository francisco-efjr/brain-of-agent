---
name: prompt-pronto-revisao-de-alertas
description: "Mede a entrega de um prompt pronto, verificando que a biblioteca de prompts é usada para entregar um prompt colável de revisão de alertas com variáveis, dados em tags, burn rate recalculado, rascunho não aplicado, orientação de uso e sem alegar eficácia medida nem revisar regras que não foram fornecidas."
tags: [sre-observability, prompts, alertas]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um prompt pronto em bloco de código para revisar regras de alerta do Prometheus, com variáveis entre colchetes para regras e SLO, dados dentro de tags tratados como dados, checklist (sintoma versus causa, for por tipo, burn rate multijanela recalculado, PromQL), formato de saída com severidade e rascunho não aplicado; explica onde rodar e por que funciona; não alega eficácia medida; não inventa regras do usuário."
model: sonnet
---
Quero um prompt pronto para eu colar no Claude e revisar as regras de alerta do Prometheus do meu time. Pode ser em português. Não precisa revisar nada agora, só me entrega o prompt.
