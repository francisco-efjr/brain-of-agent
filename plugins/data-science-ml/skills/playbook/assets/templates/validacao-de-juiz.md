# Validação de juiz LLM

Antes de confiar no juiz (V-04, V-06). Concordância bruta não valida: com 95% de saídas boas, um juiz que sempre aprova concorda 95%.

- **Critério avaliado (um por modo de falha):** [..]
- **Especialista (normalmente um, talvez dois):** [nome/função]
- **Juiz:** [modelo e versão]; **gerador:** [modelo]; mesmo modelo? [sim/não] (se sim, **não é independente**: declarar)
- **Data da validação:** [aaaa-mm-dd]

## Dados
- Erros óbvios dos dados corrigidos antes: [sim/não]
- Casos diversos por funcionalidade, cenário e persona: [descrição]
- Rótulos: binário (aprova/reprova) com **crítica escrita** pelo especialista.
- Divisão: treino (10–20%, exemplos no prompt) [n] · dev (40–45%) [n] · teste (40–45%) [n]; 30 a 50 de cada rótulo em dev e teste quando possível. dev e teste não entram no prompt.

## Resultados
| Conjunto | n (aprova/reprova) | TPR | TNR | Kappa de Cohen | Concordância bruta (só para referência) |
| --- | --- | --- | --- | --- | --- |
| dev | [..] | [..] | [..] | [..] | [..] |
| teste (rodado **uma vez**, prompt congelado) | [..] | [..] | [..] | [..] | [..] |

## Vieses (4 passos)
1. Ordem invertida em comparações par a par: inconsistência [..]
2. Nota vs comprimento da resposta: [..]
3. Instrução reformulada: variação [..]
4. Kappa reportado: [..]

## Criteria drift
Critérios revisados após a 1ª rodada de rotulagem? [sim/não]; mudanças com data: [..]

## Congelamento e revalidação
Prompt do juiz congelado em [hash/versão]. Revalidar ao trocar modelo, prompt ou distribuição. Próxima revisão: [data].

## Decisão
[usar o juiz | usar com ressalvas | não usar]; justificativa baseada em TPR e TNR, não em concordância bruta.
