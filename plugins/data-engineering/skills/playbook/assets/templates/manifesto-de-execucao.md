# Manifesto de execução: [PIPELINE/VERIFICAÇÃO]

Uso: colar em relatórios de aceitação, causa raiz e migração para que o resultado seja interpretável. Adaptado do "manifesto de execução" de `brains/qa/references/dados-ambientes-ci.md` (brain-of-agent, MIT, do autor): os sete campos originais foram mantidos e foram acrescentados adapter/warehouse e data de corte, que importam em dados.
Falha de setup (ambiente indisponível, permissão ausente) é bloqueio ou erro de infraestrutura, não aprovação nem defeito automático do produto.

```text
Artefato/commit: [IDENTIFICADOR IMUTÁVEL: hash do commit, tag ou imagem]
Configuração: [REVISÃO + FLAGS RELEVANTES, sem segredos; ex.: target de dev, --select, --state]
Dados/schema: [VERSÃO DAS MIGRAÇÕES + MASSA/SEED/NAMESPACE]; data de corte dos dados: [DATA]
Dependências: [REAIS|SANDBOX|SIMULADAS] + versões conhecidas (dbt [V], adapter [V], Airflow [V], Spark/Flink [V])
Execução: [COMANDO LITERAL, PARÂMETROS, RUNNER, INÍCIO/FIM, FUSO]
Plataforma: [WAREHOUSE/ENGINE E VERSÃO; adapter; região; SO/runtime quando relevante]
Limites conhecidos: [DIFERENÇAS QUE PODEM MUDAR O COMPORTAMENTO: dado sintético, volume menor, role diferente]
```

## Preflight (antes de executar)
| Verificação | Resultado |
| --- | --- |
| Identidade do ambiente confirmada como desenvolvimento | [SIM/NÃO/DESCONHECIDO: parar se não for SIM] |
| Versão implantada/instalada | [VERSÃO] |
| Dependências necessárias disponíveis | [SIM/NÃO] |
| Relógio e fuso | [FUSO] |
| Permissões (leitura/escrita só em dev) | [OK/PROBLEMA] |

## Fidelidade por risco
Cálculo puro não precisa de cluster de produção. Concorrência de banco pode depender do isolamento real. Desempenho depende de topologia, dados e capacidade: um ambiente menor valida regressão relativa, não capacidade absoluta de produção.
