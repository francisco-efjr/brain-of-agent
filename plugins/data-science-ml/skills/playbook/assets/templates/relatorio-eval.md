# Relatório de eval de componente LLM

Status: [projetado, não executado | executado em [data]]. Sem execução, não preencha números: descreva o plano e o custo. Percentuais sempre com denominador e método (V-02, V-03, brain-of-agent).

- **Componente e critérios de sucesso (métrica + meta + origem da meta):** [..]
- **Congelado antes da rodada:** conjunto [versão/hash], rubrica [versão], modelo e configuração [..], ferramentas [..], limites de tempo/custo [..], regra de parada [..]
- **Juiz:** [código | LLM [modelo] | humano]; ≠ gerador? [sim/não]; validação: ver `validacao-de-juiz.md`

## Resultados por tag
| Tag | Casos únicos | Tentativas | Sucesso por tentativa | IC 95% (Wilson) | pass@k | pass^k |
| --- | --- | --- | --- | --- | --- | --- |
| [tag] | [n] | [n x k] | [s/n] | [a, b] | [..] | [..] |

Dez reexecuções do mesmo caso não equivalem a dez casos independentes: o denominador de casos únicos manda.

## Falhas críticas (fora da média)
| Tipo | Casos | Contagem | Exemplos (id) |
| --- | --- | --- | --- |
| [inventar valor / citar fonte inexistente / ação fora de autorização] | [..] | [..] | [..] |

## Erros para leitura humana
Lista dos casos errados com saída, referência e decisão: erro do modelo ou do grader? [..]

## Latência e custo
p50/p95 [..]; custo por tarefa concluída, incluindo retries [..]

## Validade e limites
[independência do juiz, vazamento entre partições, amostra, mudanças de distribuição]

## Decisão
[aprovar / ajustar / rejeitar] + próxima rodada. Rótulo: avaliação por IA vs rótulo humano: [..]
