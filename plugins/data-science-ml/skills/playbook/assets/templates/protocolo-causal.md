# Protocolo causal (6 passos)

Sem desenho identificável, o texto final usa linguagem **associativa** (V-28). O código só começa no passo 4.

## 1. Pergunta e estimando
- Pergunta causal: [..]
- Estimando: [ATE / ATT / efeito local]; população [..]; horizonte [..]; tratamento [..]; desfecho [..]

## 2. Grafo causal (DAG)
Nós: tratamento, desfecho, confundidores observados, **confundidores latentes** (nós explícitos), mediadores, colisores.
```text
[escreva as arestas: A -> B]
```
**Confirmação do usuário:** [ ] confirmado em [data] por [pessoa]. Sem confirmação, o DAG é Suposição.

## 3. Mecanismo de atribuição e método
- Como o tratamento foi atribuído: [randomizado / limiar / data única / datas variáveis / uma unidade / instrumento / observáveis]
- Método: [diferença de médias | RDD | DiD ou event study | Bacon e estimadores robustos | controle sintético | IV | matching, IPW, DML | nenhum (associativo)]
- Premissas não testáveis: [lista]
- Premissas checáveis e como: [tendências paralelas; manipulação; força da primeira etapa; sobreposição]
- Erro-padrão agrupado no nível de: [atribuição]; número de clusters: [..] (poucos clusters tornam o erro robusto instável)

## 4. Estimação
Comando e saída: [..]. Reporte N, clusters, participação dos tratados, magnitude e IC.

## 5. Refutação ou sensibilidade (ao menos uma)
| Teste | Resultado | Leitura |
| --- | --- | --- |
| [placebo / tratamento aleatório / remoção de covariável / pré-tendências] | [..] | [..] |

## 6. Linguagem permitida
[causou / evidência consistente com efeito, sob premissas / associado a], conforme a evidência. Limitações: [..]
