# Tabela de disponibilidade das features

Base da auditoria de vazamento (V-13). Defina primeiro dois instantes e depois preencha uma linha por feature ou grupo de features.

- **Instante da decisão:** [quando o modelo é consultado em produção]
- **Instante do rótulo:** [quando o alvo fica conhecido]

Regra: para marcar "não" ou "sim" é preciso uma **frase de ordem temporal** ("escrito em X, decisão em Y"). Sem a frase, marque "pergunta" e registre a pergunta ao usuário. Itens "pergunta" têm severidade high, não bloqueador.

| Feature | Valor escrito em (quando/por quem) | Disponível na decisão? (sim / não / pergunta) | Evidência (arquivo:linha) | Observação |
| --- | --- | --- | --- | --- |
| [feature_a] | [evento que grava o valor] | [sim/não/pergunta] | [caminho:linha] | [janela, join, defasagem] |
| [feature_b] | | | | |

## Perguntas em aberto
1. [feature]: [pergunta objetiva ao usuário, por exemplo, "a coluna `plano_atual` é sobrescrita diariamente? Qual era o plano na data do evento?"]

## Conclusão
- Features indisponíveis na decisão: [lista] -> remover ou recalcular com dado point-in-time.
- Features em "pergunta": [lista] -> bloqueiam a aprovação até resposta.
