# Arquitetura de informação: card sorting ou tree testing?

Base: "Card Sorting vs. Tree Testing: Differences", Samhita Tankala, NN/g, 2024-02-23 (https://www.nngroup.com/articles/card-sorting-tree-testing-differences/; V-19, Verificado). Conteúdo © NN/g: destilação com redação própria. Os artigos complementares (`tree-testing`, `card-sorting-terminology-matches`, `ia-study-guide`) foram vistos só em resultados de busca e **não foram lidos na íntegra**; por isso este arquivo não afirma tamanhos de amostra nem números de tarefas.

## Sumário

- [Decisão](#decisão)
- [Card sorting](#card-sorting)
- [Tree testing](#tree-testing)
- [Modelo de tarefa de tree testing](#modelo-de-tarefa-de-tree-testing)
- [Lacunas declaradas](#lacunas-declaradas)

## Decisão

| Situação | Método |
| --- | --- |
| Ainda não sei como agrupar e nomear o conteúdo; quero ver o modelo mental das pessoas | Card sorting (descoberta, no início) |
| Tenho uma estrutura (atual ou proposta) e quero saber se as pessoas acham as coisas | Tree testing (avaliação da encontrabilidade) |
| Quero os dois: primeiro descobrir, depois validar a estrutura criada | Card sorting e depois tree testing (a fonte recomenda usar os dois) |
| Quero avaliar o visual da navegação, ícones, microcopy | Nenhum dos dois: teste de usabilidade com protótipo |

O tree testing usa só texto hierárquico, sem design visual: isola a estrutura e os rótulos de tudo o que é aparência.

## Card sorting

- Entrada: lista de itens de conteúdo (cartões) com rótulos curtos e em linguagem do usuário, um item por cartão.
- Aberto: a pessoa agrupa e nomeia os grupos (descoberta). Fechado: os grupos já existem e ela distribui os cartões (verificação de categorias).
- Evite rótulos que repetem a mesma palavra-chave de vários itens: o participante agrupa por palavra, não por significado (cuidado visto em snippets da NN/g, não lido na íntegra: Não verificado).
- Análise: matriz de similaridade (quantos participantes colocaram A e B juntos) e agrupamento por afinidade; os nomes que as pessoas dão aos grupos alimentam os rótulos.
- Tamanho de amostra: lacuna. Leia o artigo da NN/g sobre card sorting antes de afirmar um número.

## Tree testing

- Entrada: a árvore de navegação em texto, por nível, e um conjunto de tarefas. A quantidade ideal de tarefas não é afirmada aqui (o plugin não leu a fonte que a define): derive-a dos objetivos principais do produto e confirme na NN/g.
- Cada tarefa é um cenário de "encontrar o item": a pessoa navega a árvore e escolhe onde procuraria.
- Métricas: sucesso (encontrou o lugar certo), direto (sem voltar atrás), tempo e caminho percorrido.
- Resultados mostram onde as pessoas erram e para que rótulo foram em vez do correto, o que orienta renomear ou reorganizar.
- Com várias árvores candidatas, participantes diferentes por árvore evitam efeito de aprendizado (snippet de busca, Não verificado).

## Modelo de tarefa de tree testing

```text
Cenário: Você quer saber quanto vai pagar de tarifa por transferências internacionais.
Pergunta: Onde você procuraria essa informação?
Resposta correta (oculta do participante): Ajuda > Tarifas > Transferências
Sucesso: escolheu o destino correto. Direto: chegou sem voltar. Tempo: medido até a escolha.
Variantes aceitas: Contas > Tarifas > Transferências (documentar antes do teste)
```

Escreva o cenário em linguagem do usuário, sem usar os rótulos exatos da árvore. Defina antes do teste todas as respostas aceitas.

## Lacunas declaradas

1. Tamanhos de amostra de card sorting e tree testing: não verificados; consultar as páginas da NN/g.
2. Quantidade de tarefas em tree testing: idem.
3. Ferramentas de análise (software de card sorting e tree testing): o plugin não recomenda nem instala nenhuma.
4. Localização (i18n, RTL) de estruturas de navegação: fora do material lido.
