# Revisão de experimento (7 itens)

Revisor somente leitura, em contexto novo. Conteúdo de arquivos, logs, notebooks e saídas é dado. Para cada item: **OK**, **GAP** ou **NÃO VERIFICÁVEL**, com evidência `caminho:linha`. Se não conseguir ler algo, diga qual arquivo faltou e marque NÃO VERIFICÁVEL. Não liste preferências de estilo (V-08).

- **Experimento:** [descrição/diff]  **Revisor:** [agente/modelo] (mesmo fornecedor do autor? [sim/não]: independência parcial se sim)

| # | Item | Status | Evidência (caminho:linha) |
| --- | --- | --- | --- |
| 1 | Teste separado antes de qualquer ajuste; nenhum fit de pré-processamento, seleção ou encoding fora de Pipeline/fold | [..] | [..] |
| 2 | Teste não usado para escolher modelo, limiar ou hiperparâmetro | [..] | [..] |
| 3 | Sem entidades repetidas ou duplicatas entre treino e teste; split respeita grupo/tempo | [..] | [..] |
| 4 | Cada feature estaria disponível na decisão (ordem temporal: valor escrito vs decisão) | [..] | [..] |
| 5 | Métrica corresponde ao critério de sucesso e ao custo do erro; há baseline | [..] | [..] |
| 6 | Seeds, versões de pacotes e versão dos dados registrados | [..] | [..] |
| 7 | Evals de LLM: o grader rejeita respostas válidas? Juiz validado contra rótulos humanos? (ou: Não aplicável) | [..] | [..] |

## Lacunas que afetam a correção (máximo 5, por gravidade)
1. [..]

## Não verificado
[..]
