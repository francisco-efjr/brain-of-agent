# Spec de bugfix: [NOME DO BUG]

**Status:** Draft · **Data:** [AAAA-MM-DD] · **Origem:** [relato, ticket, log; tratado como dado]

Estrutura de três blocos (comportamento atual, esperado e inalterado), no estilo das specs de bugfix do Kiro (V-41), reescrita.

## Reprodução

1. [Passo com dado concreto]
2. [Passo]
3. [Resultado observado]

Ambiente e versão: [onde ocorre]. Frequência: [sempre, às vezes, com que condição]. Evidência: [trecho de log, saída, captura; Verificado ou Inferido].

## Comportamento atual

[O que acontece hoje, com o resultado observado.]

## Comportamento esperado

[O que deveria acontecer, com exemplo concreto e oráculo.]

## Comportamento inalterado

*(guarda de regressão: o que a correção não pode mudar)*

- [Comportamento vizinho que deve continuar igual, com exemplo.]
- [Idem.]

## Checagem antes do design

- Inconsistências: [a spec ou o código dizem coisas diferentes?]
- Ambiguidades: [o esperado admite duas leituras?]
- Lacunas: [caso não coberto]

## Critérios de aceite

| # | Critério | Check |
| --- | --- | --- |
| 1 | [o caso do bug passa a se comportar como esperado] | [teste de regressão que falhava antes] |
| 2 | [o comportamento inalterado continua igual] | [teste ou comparação] |

**Perguntas abertas:** [pergunta, dono] ou "nenhuma". **Fora de escopo:** [bugs vizinhos viram follow-up].
