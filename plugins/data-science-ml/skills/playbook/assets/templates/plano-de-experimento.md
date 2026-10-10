# Plano de experimento

Preencha antes de treinar. Campos entre `[COLCHETES]` são variáveis. Rotule cada afirmação: Verificado, Inferido, Suposição, Não verificável. Fontes: V-01, V-09, V-31 (`references/fontes.md`).

## 1. Decisão
- **Pergunta / decisão que o resultado alimenta:** [por exemplo, "quais clientes recebem oferta de retenção"]
- **Instante da decisão (quando o modelo é consultado):** [por exemplo, "1º dia do mês, com dados até o dia anterior"]
- **Instante em que o rótulo fica conhecido:** [por exemplo, "60 dias depois"]
- **Custo do erro:** falso positivo = [custo]; falso negativo = [custo]

## 2. Critério de sucesso (até 3)
| Métrica | Meta | Origem da meta (benchmark, experimento anterior, especialista) |
| --- | --- | --- |
| [métrica] | [valor] | [origem] |

## 3. Baseline
- Heurística ou `Dummy*`: [descrição]; métrica nas mesmas dobras: [a medir]
- Modelo atual em produção (se houver): [versão e métrica]

## 4. Dados
- Fonte e período: [..]; hash/versão: [sha256 ou versão do snapshot]; PII: [sim/não; colunas]
- Grão: uma linha por [X] por [Y]

## 5. Split e validação
- Tipo: [hold-out temporal | GroupKFold por [entidade] | StratifiedKFold | TimeSeriesSplit com horizonte [h]]
- Justificativa (estrutura dos dados): [..]
- Hold-out final tocado **uma vez**, ao fim: [sim]

## 6. Features e modelo
- Features candidatas e disponibilidade na decisão: ver `tabela-disponibilidade-features.md`
- Modelos: [..]; tudo que aprende dentro de `Pipeline`: [sim]
- Tuning: [grid | random | Optuna], parâmetros [3 a 5], `n_trials` [..], `timeout` [..]

## 7. Reprodutibilidade
- Seed: [valor em `config.py`]; tolerância de reexecução: [por exemplo, |Δ AUC| ≤ 0,005 em 3 reexecuções]
- Lockfile: [arquivo]; commit: [sha] (diretório sujo: [sim/não])

## 8. Critério de aceite (numérico)
[por exemplo, "PR-AUC de validação ≥ baseline.json + 0,01, mesma CV, sem alterar o split"]

## 9. Verificação
- Comando: [comando que reproduz]; evidência a anexar: [saída]

## 10. O que não será feito
[escopo excluído, para evitar deriva]
