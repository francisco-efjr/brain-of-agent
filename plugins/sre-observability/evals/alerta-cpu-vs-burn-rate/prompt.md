---
name: alerta-cpu-vs-burn-rate
description: "Mede a revisão de alertas, verificando que CPU vira ticket ou painel, que o alerta de SLO migra para burn rate multijanela com aritmética correta para 99,9 por cento em 30 dias, sem for no alerta de SLO, com plano de teste por falha sintética e sem atribuir runbook_url à documentação do Prometheus."
tags: [sre-observability, alert-review, alertas, burn-rate]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Classifica HighCPU como causa (ticket ou painel) e HighErrors como sintoma de SLO; propõe pares de burn rate 14,4 (1 h e 5 min), 6 (6 h e 30 min) e 1 (3 d e 6 h) em AND, janela curta = longa/12, sem for no alerta de SLO e com for de pelo menos 2 ciclos no de recurso; mostra a conta (2% x 720 h / 1 h = 14,4); avisa que os números valem para 99,9% em 30 dias; propõe teste de falha sintética para disparo e reset; entrega regra como rascunho não validado; não afirma que a documentação do Prometheus exige runbook_url."
model: sonnet
---
Revisa essas regras do Prometheus do nosso checkout. Nosso SLO de disponibilidade é 99,9% em 30 dias. Recebemos umas 40 páginas por semana e quase todas fecham sem ninguém fazer nada.

```yaml
groups:
- name: checkout
  rules:
  - alert: HighCPU
    expr: avg(rate(node_cpu_seconds_total{mode!="idle"}[1m])) > 0.8
    for: 1m
    labels: {severity: page}
  - alert: HighErrors
    expr: sum(rate(http_requests_total{job="checkout",code=~"5.."}[5m])) / sum(rate(http_requests_total{job="checkout"}[5m])) > 0.001
    for: 10m
    labels: {severity: page}
```

Me propõe o que fazer com cada uma. Ah, e dizem que a documentação do Prometheus exige `runbook_url` em todo alerta, é isso mesmo?
