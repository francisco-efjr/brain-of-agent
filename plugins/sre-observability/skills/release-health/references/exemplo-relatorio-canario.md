# Exemplo: relatório de canário do serviço de busca (v5.1)

Cenário fictício, dados ilustrativos. Plano do usuário: liberar a v5.1 para 5% do tráfego, comparando erro e CPU de hoje com ontem no mesmo horário e revertendo se piorar mais de 10%.

## Revisão do plano (o que corrigir antes de começar)

| Plano do usuário | Problema | Ajuste |
| --- | --- | --- |
| Comparar hoje com ontem no mesmo horário | Padrão de tráfego muda; confunde regressão com demanda | Comparar com o **controle concorrente** (os 95% na v5.0) no mesmo período |
| Métrica de CPU | Ruidosa, não é SLI | Erro e latência p95 do endpoint de busca (SLIs) |
| "Reverte se piorar mais de 10%" | Sem baseline, sem n mínimo, sem decisão nomeada | Baseline capturado antes; limiar relativo calibrado (Suposição); aprovador do rollback por papel |
| Métricas agregadas | 20% de erro no canário com 5% do tráfego aparece como cerca de 1% agregado | Séries separadas de canário e controle |

## Critérios escritos antes do deploy

- Interromper se, em 2 checagens seguidas: taxa de erro do canário acima do triplo do controle **e** acima de 0,5% absoluto (Suposição; calibrar com a variância do baseline), ou p95 do canário 50% acima do controle (Suposição).
- Aprovador do rollback: IC (papel). Efeitos irreversíveis: nenhum e-mail ou cobrança no fluxo de busca; migração de schema: nenhuma (T-15).

## Relatório (T-11)

```text
Serviço: search          Estado: DEGRADED
Janela: 14:00 a 14:20 UTC   Checagens: 20 (a cada 60 s; cadência real: 60 a 64 s)
Baseline: capturado 13:45 UTC (antes do deploy), não sobrescrito

| Métrica                 | Baseline | Controle (v5.0, n=95.400) | Canário (v5.1, n=5.020) |
| ----------------------- | -------- | ------------------------- | ----------------------- |
| erro 5xx (razão)        | 0,12%    | 0,13%                     | 0,41%  (checagens 6 a 20) |
| latência p95 /search    | 210 ms   | 215 ms                    | 330 ms (checagens 8 a 20) |
| latência p99 /search    | 480 ms   | 490 ms                    | 520 ms |

Alertas confirmados:
- ALTA  p95 do canário 53% acima do controle  first_seen 14:08  confirmed_at 14:09  evidência: consulta [link], janela 14:05 a 14:09  resolved: não
Observações transitórias (1 checagem apenas, não são alertas):
- erro 5xx do canário 0,9% na checagem 5, voltou a 0,4% na checagem 6

Veredito: a v5.1 degrada p95 em relação ao controle. Decisão humana pendente: investigar, manter observando, reverter ou ignorar.
Próximo passo sugerido: investigar com root-cause-investigation (diff da v5.1 e spans); rollback só se o IC aprovar (proposta de comando não incluída: depende da ferramenta de deploy do time).
```

## JSON equivalente (campos destilados do gstack canary, MIT, Garry Tan)

```json
{
  "service": "search",
  "started_at": "2026-10-10T14:00:00Z",
  "ended_at": "2026-10-10T14:20:00Z",
  "status": "DEGRADED",
  "metrics": [
    { "name": "latency_p95_ms", "baseline": 210, "control": 215, "canary": 330, "n_control": 95400, "n_canary": 5020 }
  ],
  "alerts": [
    { "severity": "high", "first_seen": "2026-10-10T14:08:00Z", "confirmed_at": "2026-10-10T14:09:00Z",
      "evidence": "consulta de p95 por versão, 14:05 a 14:09 UTC", "resolved": false }
  ],
  "observations": [
    { "at": "2026-10-10T14:05:00Z", "note": "erro 5xx do canário 0,9% em uma checagem; voltou a 0,4%" }
  ]
}
```

Regra de estado: BROKEN se algum alerta crítico foi confirmado; senão DEGRADED se qualquer alerta foi confirmado; senão HEALTHY. Transitórios ficam em `observations`.

## O que a skill não fez

Não executou rollback, não consultou sistemas por conta própria e não alterou o baseline. Os números desta página são ilustrativos; não os use como limiares.
