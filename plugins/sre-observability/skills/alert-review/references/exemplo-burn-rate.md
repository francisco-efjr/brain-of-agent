# Exemplo: regra de burn rate multijanela e teste sintético

Rascunho **não executado e não validado** contra Prometheus (nesta sessão não havia `promtool`). O objetivo é servir de molde; ajuste métrica, rótulos, SLO e janelas. Valores valem para SLO de 99,9% em 30 dias. Fontes: V-03 (tabela e regras), V-27 (notas de PromQL); redação própria.

## Contas (refaça para o seu SLO)

```text
limiar de razão de erro = burn x (1 - meta)
99,9%  ->  1 - 0,999 = 0,001
burn 14,4 -> 14,4 x 0,001 = 0,0144   (1,44% de erro)   janelas 1 h e 5 min
burn 6    ->  6   x 0,001 = 0,006    (0,6% de erro)    janelas 6 h e 30 min
burn 1    ->  1   x 0,001 = 0,001    (0,1% de erro)    janelas 3 d e 6 h  (ticket)
consumo   = burn x janela do alerta / janela do SLO:  14,4 x 1 / 720 = 2%
```

## Regra (rascunho)

Métrica suposta: `http_requests_total{job="checkout", code="..."}`, coletada a cada 30 s (janela de 5 min = 10 coletas, acima do mínimo de 4). Sem `for:` por ser alerta de SLO.

```yaml
groups:
  - name: checkout-slo-burn
    rules:
      - alert: CheckoutErrorBudgetBurnFast
        expr: |
          (
            sum(rate(http_requests_total{job="checkout",code=~"5.."}[1h]))
            / sum(rate(http_requests_total{job="checkout"}[1h]))
          ) > (14.4 * 0.001)
          and
          (
            sum(rate(http_requests_total{job="checkout",code=~"5.."}[5m]))
            / sum(rate(http_requests_total{job="checkout"}[5m]))
          ) > (14.4 * 0.001)
        labels:
          severity: page
        annotations:
          summary: "Checkout consome 2% do orçamento de 30 d por hora (burn 14,4)"
          dashboard: "<URL do painel de SLO>"
      - alert: CheckoutErrorBudgetBurnSlow
        expr: |
          (
            sum(rate(http_requests_total{job="checkout",code=~"5.."}[6h]))
            / sum(rate(http_requests_total{job="checkout"}[6h]))
          ) > (6 * 0.001)
          and
          (
            sum(rate(http_requests_total{job="checkout",code=~"5.."}[30m]))
            / sum(rate(http_requests_total{job="checkout"}[30m]))
          ) > (6 * 0.001)
        labels:
          severity: page
      - alert: CheckoutErrorBudgetBurnTicket
        expr: |
          (
            sum(rate(http_requests_total{job="checkout",code=~"5.."}[3d]))
            / sum(rate(http_requests_total{job="checkout"}[3d]))
          ) > (1 * 0.001)
          and
          (
            sum(rate(http_requests_total{job="checkout",code=~"5.."}[6h]))
            / sum(rate(http_requests_total{job="checkout"}[6h]))
          ) > (1 * 0.001)
        labels:
          severity: ticket
```

Pontos a conferir antes de usar:

- Sem tráfego, a divisão gera `NaN` e a comparação é falsa: o alerta não dispara. Se "sem tráfego" for falha, crie alerta de ausência de tráfego à parte.
- Se o SLI inclui latência, a razão de eventos bons vem de buckets do histograma (`le`); mantenha `le` na agregação interna e agregue depois de `rate()`.
- Agrupe por `job` (ou por `tenant`) só com poucos valores; rótulo de alta cardinalidade nas regras multiplica avaliações.
- `runbook_url` na anotação é convenção de comunidade (Suposição); adicione se o time usa.

Validar a sintaxe (Inferido; confira a sintaxe do comando na versão instalada):

```bash
promtool check rules checkout-slo.yml
```

## Teste sintético com `promtool test rules` (rascunho)

Prova disparo e reset sem tocar em produção. Cenário: 1,96% de erro por 70 min (acima de 1,44%), depois zero erro. Aos 80 min a janela de 1 h ainda está acima do limiar, mas a de 5 min já está limpa: o AND impede a página (reset rápido).

```yaml
rule_files:
  - checkout-slo.yml
evaluation_interval: 1m
tests:
  - interval: 1m
    input_series:
      - series: 'http_requests_total{job="checkout",code="200"}'
        values: '0+1000x120'
      - series: 'http_requests_total{job="checkout",code="500"}'
        values: '0+20x70 1400+0x50'
    alert_rule_test:
      - eval_time: 70m
        alertname: CheckoutErrorBudgetBurnFast
        exp_alerts:
          - exp_labels:
              severity: page
            exp_annotations:
              summary: "Checkout consome 2% do orçamento de 30 d por hora (burn 14,4)"
              dashboard: "<URL do painel de SLO>"
      - eval_time: 80m
        alertname: CheckoutErrorBudgetBurnFast
        exp_alerts: []
```

Execução (Inferido): `promtool test rules checkout-slo-test.yml`. Cole a saída real no relatório; se `promtool` não existir, marque **Não verificável** e não afirme que o teste passa. O teste em ambiente real (injeção de 2% de erro) é passo separado e exige autorização da operação.

## Antes e depois (caso do `alert-review`)

| Regra original | Problema | Substituição |
| --- | --- | --- |
| `HighCPU`: CPU média > 80% por 1 min | Causa, não sintoma; sem ação imediata; janela curta capta rajadas | Painel USE do recurso e ticket; paginar pelo SLO |
| `HighErrors`: razão 5xx em 5 min > 0,001 | Limiar igual ao orçamento em 5 min: dispara com ruído e não distingue queima rápida de lenta | Par de janelas em AND (acima) |
