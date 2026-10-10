# Alertas e sinais

Para revisar regras de alerta, converter alertas de recurso em alertas de SLO e auditar painéis. Consulta às fontes: 2026-10-10. Redação própria; os números de exemplo valem para o contexto citado e devem ser recalculados.

## Sumário

- [Sintoma antes de causa: os quatro sinais de ouro](#sintoma-antes-de-causa-os-quatro-sinais-de-ouro)
- [RED e USE](#red-e-use)
- [Burn rate multijanela](#burn-rate-multijanela)
- [Regras por tipo de alerta (conflito do `for:`)](#regras-por-tipo-de-alerta-conflito-do-for)
- [Rascunho de regra PromQL](#rascunho-de-regra-promql)
- [Notas de PromQL](#notas-de-promql)
- [Checklist de revisão de alerta](#checklist-de-revisão-de-alerta)
- [Roteamento: página, ticket, dashboard](#roteamento-página-ticket-dashboard)
- [Metamonitoramento e lotes](#metamonitoramento-e-lotes)
- [Checklist de painel](#checklist-de-painel)
- [Lacunas](#lacunas)

## Sintoma antes de causa: os quatro sinais de ouro

Fonte: V-04 (SRE Book "Monitoring Distributed Systems", Classe A). Regra central: **paginar por sintoma, depurar por causa**. O mesmo sinal pode ser sintoma para um observador e causa para outro (o disco cheio do banco é causa para a API e sintoma para quem opera o banco).

| Sinal | O que medir | Armadilha |
| --- | --- | --- |
| Latência | Duração de requisições com sucesso **separada** da duração de erros | Erro rápido (503) puxa a média para baixo e parece melhora |
| Tráfego | Demanda em métrica de domínio (req/s, pedidos/min, mensagens/s) | Olhar só bytes de rede |
| Erros | Explícitos (5xx), implícitos (200 com conteúdo errado) e por política (resposta acima de 1 s conta como erro) | Contar só 5xx |
| Saturação | Uso do recurso mais restrito, com meta de utilização (muitos sistemas degradam antes de 100%) | Alertar em 90% de CPU sem relação com o usuário |

## RED e USE

Fonte: V-06 (Brendan Gregg, USE method, Classe A; RED de Tom Wilkie via blog da Grafana, Classe B). Para cada **serviço**, RED: taxa (Rate), erros (Errors), duração (Duration). Para cada **recurso** (CPU, memória, disco, rede, pool, fila), USE: utilização, saturação, erros. RED mostra onde dói; USE, por quê. Observações verificadas: erros primeiro, por serem mais fáceis de interpretar; média de 5 min esconde rajadas de 100%; ~70% de utilização é regra de bolso, não lei, e vale mais para recursos não preemptáveis como disco.

## Burn rate multijanela

Fonte: V-03 (SRE Workbook "Alerting on SLOs", tabela 5-8, Classe A; aritmética conferida).

**Definição.** Burn rate = velocidade de consumo do budget relativa à velocidade que o esgotaria exatamente no fim da janela do SLO. Fórmula para escolher o limiar a partir do consumo desejado:

```
burn = consumo_do_budget × janela_do_SLO ÷ janela_do_alerta
limiar de taxa de erro = burn × (1 − meta)
tempo até esgotar o budget (ao ritmo burn) = janela_do_SLO ÷ burn
```

**Tabela para SLO 99,9% em 30 dias (720 h):**

| Severidade | Janela longa | Janela curta | Burn | Budget consumido ao disparar | Esgota em | Limiar de taxa de erro |
| --- | --- | --- | --- | --- | --- | --- |
| Página | 1 h | 5 min | 14,4 | 2% | 50 h | 1,44% |
| Página | 6 h | 30 min | 6 | 5% | 120 h (5 d) | 0,6% |
| Ticket | 3 d | 6 h | 1 | 10% | 30 d | 0,1% |

Conferência: 2% × 720 ÷ 1 = 14,4; 5% × 720 ÷ 6 = 6; 10% × 720 ÷ 72 = 1; 14,4 × 0,001 = 0,0144.

**Regras de construção** (todas Verificadas em V-03):
- Janela curta = janela longa ÷ 12 (1 h → 5 min; 6 h → 30 min; 3 d = 72 h → 6 h).
- A janela longa confirma queima **sustentada**; a curta confirma que **continua** agora e dá reset rápido quando o problema acaba.
- Condição em **AND**: dispara só quando as duas passam do limiar.
- Separe página (esgota em horas ou poucos dias) de ticket (queima lenta que merece atenção em horário comercial).
- Por que não um limiar único: no método 4 do Workbook (limiar único de burn rate), uma queima de 35× abaixo do limiar escolhido nunca alerta e esgota o budget em ≈ 20,5 h (720 ÷ 35); é o contra "baixo recall" da tabela de prós e contras.
- Teste cada par com falha sintética que prove **disparo e reset**; suprima duplicatas (um incidente, uma página).

**Recalcular para outro SLO (exemplo nosso, Inferido).** Meta 99,5% em 28 dias (672 h), budget 0,5%:

| Par | Cálculo do burn | Limiar de taxa de erro |
| --- | --- | --- |
| Página 2% em 1 h | 0,02 × 672 ÷ 1 = 13,44 | 13,44 × 0,005 = 6,72% |
| Página 5% em 6 h | 0,05 × 672 ÷ 6 = 5,6 | 5,6 × 0,005 = 2,8% |
| Ticket 10% em 3 d (72 h) | 0,10 × 672 ÷ 72 ≈ 0,933 | 0,933 × 0,005 ≈ 0,467% |

Mostre sempre a conta na saída; não reutilize 14,4/6/1 para outras metas ou janelas.

## Regras por tipo de alerta (conflito do `for:`)

Conflito K1 (V-03 × V-05): o Prometheus e o capítulo "Practical Alerting" recomendam duração mínima; o Workbook "Alerting on SLOs" desaconselha `for:` em alerta de SLO (nota de rodapé: pode filtrar ruído efêmero).

| Tipo | Condição | `for:` |
| --- | --- | --- |
| SLO / sintoma | burn rate multijanela em AND | Sem `for:` (as janelas já filtram o ruído) |
| Recurso / causa (disco enchendo, fila crescendo) | Limiar no recurso | `for:` ≥ 2 ciclos de avaliação (V-05) |
| Polling sintético de canário | Mesmo padrão em 2 checagens seguidas | Filtro próprio (não é `for:`); ver [resiliencia-canario-capacidade.md](resiliencia-canario-capacidade.md) |

## Rascunho de regra PromQL

**Rascunho gerado por este plugin, não executado, sintaxe Inferido.** O Workbook não traz exemplo PromQL na página lida e o skill `alerting-irm` da Grafana (V-27) cobre provisionamento, não foi validado como exemplo. Antes de aplicar: `promtool check rules arquivo.yml` e teste de unidade com `promtool test rules` (conhecimento estável; confira na versão instalada). Nada é aplicado ao Alertmanager nem silenciado pela skill.

```yaml
# SLO 99,9% / 30 d no serviço checkout; métrica http_requests_total{code}; scrape de 30 s.
groups:
- name: checkout-sli
  rules:
  - record: sli:http_errors:ratio_rate5m
    expr: sum(rate(http_requests_total{job="checkout",code=~"5.."}[5m])) / sum(rate(http_requests_total{job="checkout"}[5m]))
  - record: sli:http_errors:ratio_rate30m
    expr: sum(rate(http_requests_total{job="checkout",code=~"5.."}[30m])) / sum(rate(http_requests_total{job="checkout"}[30m]))
  - record: sli:http_errors:ratio_rate1h
    expr: sum(rate(http_requests_total{job="checkout",code=~"5.."}[1h])) / sum(rate(http_requests_total{job="checkout"}[1h]))
  - record: sli:http_errors:ratio_rate6h
    expr: sum(rate(http_requests_total{job="checkout",code=~"5.."}[6h])) / sum(rate(http_requests_total{job="checkout"}[6h]))
  - record: sli:http_errors:ratio_rate3d
    expr: sum(rate(http_requests_total{job="checkout",code=~"5.."}[3d])) / sum(rate(http_requests_total{job="checkout"}[3d]))
- name: checkout-burn
  rules:
  - alert: CheckoutBurnPageFast          # 2% do budget em 1 h
    expr: sli:http_errors:ratio_rate1h > (14.4 * 0.001) and sli:http_errors:ratio_rate5m > (14.4 * 0.001)
    labels: { severity: page }
  - alert: CheckoutBurnPageSlow          # 5% em 6 h
    expr: sli:http_errors:ratio_rate6h > (6 * 0.001) and sli:http_errors:ratio_rate30m > (6 * 0.001)
    labels: { severity: page }
  - alert: CheckoutBurnTicket            # 10% em 3 d
    expr: sli:http_errors:ratio_rate3d > (1 * 0.001) and sli:http_errors:ratio_rate6h > (1 * 0.001)
    labels: { severity: ticket }
```

Limitações do rascunho: o SLI é só de erro (some a latência com um segundo SLI); sem tráfego a razão não existe e o alerta não dispara (cubra com alerta de ausência de tráfego e teste de caixa-preta); anexe `runbook_url` por convenção (Suposição, ver abaixo).

## Notas de PromQL

Fonte: V-27 (grafana/skills `promql`, Apache-2.0, Classe B; atribuição: Grafana Labs).

- Janela de `rate()` com pelo menos 4× o intervalo de coleta (coleta de 30 s → ≥ 2 min).
- Agregue **depois** de `rate()`: `sum(rate(...))`, nunca `rate(sum(...))`.
- Em `histogram_quantile`, mantenha o rótulo `le` na agregação interna: `histogram_quantile(0.95, sum by (le) (rate(x_bucket[5m])))`.
- Proteja divisão por zero (denominador pode ser 0 em baixo tráfego).
- `rate()` só em contadores; em medidores use `deriv()` ou o valor direto (V-11).
- Não tire média de percentis entre instâncias: agregue buckets.

## Checklist de revisão de alerta

Fusão de V-03 e V-05 (Verificado). Ids completos em [checklist-completo.md](checklist-completo.md).

1. Alerta sobre objetivo de alto nível (sintoma do usuário), não sobre máquina isolada; combine caixa-branca e caixa-preta.
2. Cada página exige ação humana imediata e inteligente; sem ação vira ticket ou dashboard.
3. SLO ⇒ burn rate multijanela em AND, janela curta = longa ÷ 12; recurso ⇒ `for:` ≥ 2 ciclos.
4. Limiar relativo **mais** piso absoluto (exemplo do livro: razão de erros > 1% **e** > 1 erro/s por 2 min), para não acordar alguém por 1 erro em 3 requisições.
5. Contador em taxa, nunca medidor.
6. Roteamento explícito: página, ticket ou dashboard; um incidente gera uma página (supressão de duplicatas; inibição de alertas de causa quando o de sintoma já disparou).
7. Metas de alerta no plantão: tender a 1 alerta por incidente; mediana de páginas/dia próxima de 0 (V-24).
8. Teste de disparo e reset com falha sintética planejada; registro do resultado.

Nota sobre runbook: a página de práticas de alerta do Prometheus orienta apontar alertas para consoles (dashboards) e **não menciona runbook** (Verificado, V-05). Anotação `runbook_url` por regra é convenção de comunidade (Suposição). Um runbook por assinatura de falha: [incidentes-e-postmortem.md](incidentes-e-postmortem.md).

## Roteamento: página, ticket, dashboard

| Pergunta | Resposta | Destino |
| --- | --- | --- |
| Há impacto no usuário agora ou o budget esgota em horas? | Sim | Página |
| O budget esgota em dias, ou um recurso vai faltar em dias? | Sim | Ticket |
| É informação para diagnóstico? | Sim | Dashboard (console) |
| Ninguém age quando dispara? | Sim | Apague ou rebaixe |

Silêncios amplos escondem incidentes (risco registrado em V-27): silencie por matcher estreito, com dono e prazo.

## Metamonitoramento e lotes

- Teste de **caixa-preta** do caminho completo (sonda sintética do ponto de vista do usuário) vigia o próprio monitoramento: se o Prometheus ou o Alertmanager cair, algo externo precisa avisar (V-05).
- Jobs em lote: permita ao menos 2 execuções antes de alertar; meça o momento do último sucesso, não a duração de cada execução (V-05, V-11).

## Checklist de painel

Fonte: V-04.

- Latência de sucesso e de erro em séries separadas, em percentis (p50, p95, p99), nunca só média.
- Tráfego em unidade de domínio; erros explícitos e implícitos; saturação do recurso mais restrito com a meta de utilização desenhada.
- Linha do SLO e do budget restante visível; deploys marcados no eixo do tempo.
- RED por serviço e USE por recurso em seções distintas.
- Cada painel responde a uma pergunta ("o usuário está sofrendo?"); sem painel de 40 gráficos.

## Lacunas

- Nenhum exemplo PromQL oficial de burn rate foi lido (V-03, lacuna 3): trate as regras como rascunho e valide.
- Fonte oficial sobre estrutura de runbook inexistente (lacuna 2).
