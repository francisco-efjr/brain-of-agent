# Relatório de auditoria de custo Apify

Formato de saída fixo do agente `apify-cost-auditor` (modos plano e execução) e da skill `auditoria-de-custo`. A auditoria é **somente leitura**: não executa Actors, não altera arquivos, não pede token e não relata o valor de segredos (cita a chave e o local). Achado sem evidência é descartado. Custo desconhecido é "Não verificável", **não** conformidade. Regras R1 a R12 em `references/checklist-completo.md` (seção "Auditoria de custo").

## Cabeçalho

- **Escopo auditado:** [sessão / pesquisa / período]
- **Modo:** [plano (pré-voo) | execução (pós)]
- **Orçamento aprovado:** US$ [total] (por [quem], em [mensagem/data]) · por run US$ [x]
- **Fontes lidas:** [planos, `registro-de-custo.md`, arquivos de pesquisa com "Obtido via", `args.apify` se houver]
- **Independência:** a auditoria é do mesmo modelo de quem planejou ou executou: não é revisão independente.

## Veredito

- **Modo execução:** `conforme` | `conforme com ressalvas` | `não conforme`
- **Modo plano:** `aprovar plano` | `corrigir` | `bloquear`
- Resumo em 1 a 3 linhas.

## Modo plano: checklist de pré-voo

| # | Item | Resultado (ok / falha / NA com motivo / NV) | Evidência |
| --- | --- | --- | --- |
| 1 | Orçamento do usuário presente e em US$ | | |
| 2 | Actor na lista permitida ou escolhido por `escolher-actor` | | |
| 3 | Preço do dia datado | | |
| 4 | `input` com limite de volume (não o default) | | |
| 5 | Limites em `callOptions`, não no `input` | | |
| 6 | `callOptions.timeout` definido (≠ 0) | | |
| 7 | `maxTotalChargeUsd` ≥ mínimo do Actor e ≤ teto por run (PPE) | | |
| 8 | Usage-based marcado "sem teto USD", com estimativa | | |
| 9 | Rota gratuita avaliada | | |
| 10 | `waitSecs` ≤ 30 | | |
| 11 | Uma run por plano | | |
| 12 | Plano de leitura (`limit` ≤ 20, `fields`) | | |
| 13 | Riscos (PII, termos) e critério de parada | | |

## Achados

| ID | Severidade | Evidência (arquivo:linha ou campo) | Regra | Recomendação | Rótulo |
| --- | --- | --- | --- | --- | --- |
| A-01 | alta / média / baixa | | R1–R12 | | Verificado / Inferido / Não verificável |

Severidade: **alta** = gasto acima do orçamento, re-run sem aprovação, tool de escrita usada, segredo exposto. **Média** = teto ausente em PPE, Actor fora da lista, custo real desconhecido com orçamento acima de US$ 1. **Baixa** = registro incompleto, PII sem plano de exclusão.

## Tabela de runs reconstruída

| # | Actor | runId | Teto US$ | Estimativa US$ | Custo real US$ | Status | Plano | Observação |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Saldo do orçamento

- Teto comprometido (soma): US$ [x] · saldo pelo teto: US$ [orçamento − x]
- Custo real conhecido: US$ [y] de [n] runs (as demais: não verificável) · saldo real (só com custo conhecido): US$ [orçamento − y]

## Não verificado

Liste o que não foi possível conferir (custo real ausente, `nextStep` seguido ou não, runs fora do registro, comportamento do teto em runtime) e **o que o usuário deve ler no Console** (Billing/Usage, lista de Runs).

## Recomendações (sem executar nada)

Inclua sempre que cabível: ligar o limite da conta em Billing › Limits (overage desligado), apagar datasets com PII, revogar ou rotacionar token exposto, novo plano para qualquer coleta adicional.

## Exemplo de achados (cenário fictício: orçamento US$ 0,50; runs #1 e #2 iguais de `trudax/reddit-scraper-lite`, teto 0,10 e custo real 0,09 cada; #3 `apidojo/tweet-scraper`, fora da lista, sem teto, custo real 0,50)

| ID | Severidade | Evidência | Regra | Recomendação | Rótulo |
| --- | --- | --- | --- | --- | --- |
| A-01 | alta | soma real 0,09 + 0,09 + 0,50 = 0,68 > 0,50 | R2 | Revisar o orçamento antes de qualquer nova run; ligar limite da conta | Verificado (custos informados) |
| A-02 | alta | run #2 com mesmo Actor e input da #1, sem novo plano | R3 | Registrar o desvio; nova coleta só com novo plano | Verificado |
| A-03 | média | `apidojo/tweet-scraper` fora da lista permitida | R4 | Remover ou aprovar explicitamente | Verificado |
| A-04 | média | #3 sem teto e sem limite de volume (`maxItems`) | R5, R6 | Definir `maxItems` e `maxTotalChargeUsd` no plano | Verificado |

Veredito do exemplo: `não conforme`.
