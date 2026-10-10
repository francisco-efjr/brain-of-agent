# Pré-análise de experimento A/B

Preencha e congele **antes** de ver resultados. Leitura posterior segue a ordem: SRM, guardrails, primária, secundárias (V-26). Números de poder são cálculo do desenho, não fato observado.

- **Hipótese e decisão:** [o que será lançado/abandonado conforme o resultado]
- **Período e exposição:** [início, fim; quem entra na análise e quando (definição de exposição)]

| Item | Preenchimento |
| --- | --- |
| Métrica primária (definição exata, janela) | [..] |
| Guardrails e limiares | [métrica: limiar] |
| Unidade de randomização | [usuário/sessão/loja] |
| Unidade de análise (deve ser igual à de randomização) | [..] |
| Razão planejada entre braços | [por exemplo, 50/50] |
| Teste de SRM | qui-quadrado nas contagens; p < 0,001 como convenção para investigar |
| n por braço planejado | [..] |
| MDE do desenho vs menor efeito que vale lançar | [MDE] vs [efeito mínimo de interesse] |
| Clusters (se houver) | m médio [..]; ICC [..]; DEFF = 1 + (m − 1)·ICC = [..] |
| CUPED | [sim: covariável [..] medida antes da exposição / não] |
| Regra de parada | [duração fixa / sequencial: método] |
| Teste e correção das secundárias | [Holm ou Bonferroni (confirmatórias) / BH (triagem exploratória)] |
| Família de testes | métricas [a] x variantes [b] x segmentos [c] x olhadas [d] = [total] |
| Subgrupos pré-registrados | [lista; os demais são exploratórios] |

## Premissas e riscos
[contaminação entre braços, efeito de novidade, sazonalidade, poucos clusters, outras]

## Relatório pós-teste
Use `relatorio-estatistico.md`. Desvios do plano ficam registrados com data.
