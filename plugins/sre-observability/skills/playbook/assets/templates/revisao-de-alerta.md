# Revisão de alertas — [SERVIÇO/ARQUIVO] — [data]

Template T-03. Molde PAD-15 (`ID · severidade · detecção · referência · correção`), itens SRE-nn do `checklist-completo.md`. As regras propostas são **rascunho não executado**: nada foi validado contra Prometheus nem aplicado ao Alertmanager, e nada foi silenciado.

**Escopo:** [arquivos de regras, rotas, painel] · **SLO considerado:** [meta e janela] · **Histórico de páginas:** [período, nº de páginas, % sem ação] · **Acesso:** [só colagem / leitura do repositório]

## 1. Classificação

| Alerta | Tipo (SLO/sintoma × recurso/causa) | Hoje | Proposta |
| --- | --- | --- | --- |
| [HighCPU] | recurso | página | ticket/dashboard |
| [HighErrors] | sintoma | página, limiar único | burn rate multijanela |

## 2. Achados

| ID | Severidade | Detecção (arquivo:linha) | Referência | Correção | Rótulo |
| --- | --- | --- | --- | --- | --- |
| SRE-20 | M | [rules.yml:12 `avg(rate(node_cpu...)) > 0.8`] | V-04, V-05 | [rebaixar a ticket] | Verificado (lido no arquivo) |
| SRE-21 | B | [rules.yml:30, limiar único 0,001] | V-03 | [pares multijanela em AND] | Verificado |

## 3. Conta do burn rate (mostrar sempre)

SLO [99,9]% em [30] dias ([720] h); budget [0,001].

| Par | Janela longa / curta | Consumo desejado | Burn = consumo × janela SLO ÷ janela alerta | Limiar de taxa de erro = burn × budget |
| --- | --- | --- | --- | --- |
| Página rápida | [1 h / 5 min] | [2%] | [0,02 × 720 ÷ 1 = 14,4] | [0,0144] |
| Página lenta | [6 h / 30 min] | [5%] | [0,05 × 720 ÷ 6 = 6] | [0,006] |
| Ticket | [3 d / 6 h] | [10%] | [0,10 × 720 ÷ 72 = 1] | [0,001] |

Regras: janela curta = longa ÷ 12; condição em AND; sem `for:` no alerta de SLO; `for:` ≥ 2 ciclos nos alertas de recurso. Os números acima valem para 99,9%/30 d; recalcule para outras metas.

## 4. Regra reescrita (rascunho)

```yaml
[regra proposta; ver exemplo em references/alertas-e-sinais.md; rótulo: rascunho, sintaxe Inferido]
```

## 5. Plano de teste

| Teste | Procedimento (falha sintética planejada, ambiente não produtivo) | Resultado esperado | Resultado obtido |
| --- | --- | --- | --- |
| Disparo | [injetar taxa de erro de [x]% por [y] min] | [alerta dispara em [z] min] | [não executado] |
| Reset | [remover a falha] | [alerta resolve em [w] min (janela curta)] | [não executado] |
| `promtool check rules` / `promtool test rules` | [comandos na versão instalada] | [sem erros] | [não executado] |

## 6. Perguntas em aberto e limitações

[ex.: histórico de páginas não fornecido, efeito no ruído estimado como Suposição; dashboards não vistos; `runbook_url` é convenção (Suposição).]
