# Cenário de eval para skills e prompts de dados: [NOME DO CENÁRIO]

Uso: medir se uma skill, prompt ou CLAUDE.md melhora o resultado. Base: V-06 (Hamel Husain e Shreya Shankar; harness do `dbt-agent-skills`, Apache-2.0; rmoff). Status dos evals: `designed_not_executed` até rodar. `claude plugin eval` exige Claude Code 2.1.269 ou superior.
Regra central: a rubrica (`criterios.md`) não pode estar no disco nem no contexto do agente que gera a saída.

## Estrutura
Este template descreve um cenário de medição manual (rubrica fora do ambiente do executor). Para rodar com `claude plugin eval`, use o formato oficial: `evals/<caso>/prompt.md` (frontmatter `description`, `tags`, `max_turns`, `allowed_tools`, `runs`; o corpo é o pedido, com todo o contexto dentro dele) e `evals/<caso>/graders/*.md` (`type: llm`, `tool_used`, `regex`...). Exemplos reais em `evals/` deste plugin. `allowed_tools` só concede ferramentas de leitura: `Bash`, `Write` e `Edit` exigem `--allow-tools` na linha de comando.
```text
evals/[CENÁRIO]/
├── prompt.txt        ← pedido como o usuário escreveria; não cita o nome da skill
├── criterios.md      ← rubrica; fora do ambiente do agente executor
└── contexto/         ← cópia descartável de arquivos de entrada (YAML, SQL, logs)
```

## Matriz (opcional)
| Prompt \ Skills | Nenhuma | Uma skill | Plugin completo |
| --- | --- | --- | --- |
| Rico (stack, escopo, aceite) | [RESULTADO] | [RESULTADO] | [RESULTADO] |
| Mínimo (uma frase) | [RESULTADO] | [RESULTADO] | [RESULTADO] |
Rode cada célula ao menos 3 vezes. pass@k mede "alguma vez acerta"; pass^k mede consistência. Uma execução não prova nada. Não presuma ganho: há relato de skills que ajudaram menos que o esperado.

## Camadas
1. Determinística: arquivo existe, teste existe, contagem confere, comando citado.
2. Juiz binário por modo de falha: uma pergunta por chamada, `{"falha": true|false, "evidencia": "<trecho literal curto>"}`; agente `eval-judge`; modelo de família diferente do gerador quando possível; sem nota 1 a 5 como porta de aprovação.
3. Revisão humana de amostra; calibrar o juiz contra rótulos humanos (divisão dev/teste). 100% de aprovação é sinal de rubrica frouxa.

## Modos de falha (derivados de 20 a 50 saídas reais, não inventados)
| ID | Modo de falha | Pergunta binária ao juiz | Exemplo de saída que falha |
| --- | --- | --- | --- |
| F1 | [MODO] | [A saída ... ?] | [TRECHO] |

## Critérios do caso (`criterios.md`)
PASS se [COMPORTAMENTOS OBSERVÁVEIS: ex.: lista os dois consumidores; propõe modelo versionado; pede o target de dev; rotula a execução como não verificada].
FAIL se [FALHAS CRÍTICAS: ex.: renomeia no lugar; afirma ter rodado `dbt build`; sugere `--full-refresh`; remove testes].

## Registro de execução
| Execução | Data | Modelo | Skills ativas | Resultado por modo de falha | Custo/tokens/tempo |
| --- | --- | --- | --- | --- | --- |
| 1 | [DATA] | [MODELO] | [SKILLS] | [F1: ok/falha] | [VALORES] |
Custos citados em posts são de uma execução, não média.
