# Relatório de EDA

Somente sobre o conjunto de **treino**; hold-out separado antes (por grupo ou tempo). Números só de código executado, com comando e saída; se não executou, escreva "a medir" e entregue o plano. Achados post hoc são **exploratórios** (V-15).

- **Dataset:** [caminho], versão/hash [..], período [..]; PII: [colunas] (não impressas)
- **Alvo:** [coluna]; **instante da decisão:** [..]
- **Comando/ambiente:** [comando, versões]

## 1. Forma e tipos
Linhas x colunas, dtype, memória, chave/grão. [..]

## 2. Ausentes e padrão de ausência
Percentual por coluna; separar **ausente**, **não detectado** e **zero verdadeiro**; ausência correlaciona com o alvo? [..]

## 3. Alvo e balanceamento
Distribuição, prevalência, evolução no tempo. [..]

## 4. Relação com o alvo
Média e DP junto de mediana e IQR; médias por grupo; informação mútua; `.corr()` só para numéricas lineares. [..]

## 5. Suspeitas de vazamento
| Coluna | Motivo | Frase de ordem temporal ou pergunta |
| --- | --- | --- |
| [coluna] | [ID / timestamp posterior / derivada do desfecho] | [..] |

## 6. Cardinalidade e outliers
Níveis por categórica; outliers listados (**nenhum removido ou imputado automaticamente**); decisão proposta: [..]

## 7. Features candidatas
[lista com disponibilidade na decisão, ver `tabela-disponibilidade-features.md`]

## 8. Premissas
[..]

## 9. O que não foi verificado
[..] (rótulos: Verificado / Inferido / Suposição / Não verificável)
