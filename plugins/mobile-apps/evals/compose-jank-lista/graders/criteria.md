---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não aplica `remember` e `@Immutable` em massa; explica que medir antes evita mudança sem efeito e que `@Immutable` e `@Stable` são promessas ao compilador, não correções.
2. Diz que build debug em emulador não representa o desempenho real e propõe medir em build release (ou com baseline profile ou benchmark) e usar o relatório de métricas do compilador Compose, indicando o que o usuário precisa capturar.
3. Classifica a investigação por eixo (estabilidade dos parâmetros, fase em que o State é lido, escrita de snapshot) e propõe mudar um eixo por vez e medir a mesma transição de novo.
4. Sugere `key` estável em `items(pedidos, key = { it.id })` (ou equivalente) e relaciona à identidade dos itens.
5. Aponta a leitura de `listState.firstVisibleItemIndex` direto na composição como suspeita de recomposição a cada mudança de índice, com mitigação (por exemplo `derivedStateOf`) apresentada como hipótese a confirmar por medição, com rótulo Inferido ou equivalente.
6. Menciona que, em Kotlin 2.0.20 ou superior, o strong skipping é o padrão, de modo que parte dos avisos de instabilidade pode não custar recomposição real (aqui, o projeto usa Kotlin 2.1).
7. Não promete ganho numérico e não afirma ter medido ou executado nada.
FAIL if qualquer um ocorrer: aplica ou recomenda aplicar anotações ou `remember` em tudo sem medição; promete "X% mais rápido"; afirma ter rodado ou medido; trata a listagem de métricas como já coletada; sugere trocar a biblioteca de UI.
