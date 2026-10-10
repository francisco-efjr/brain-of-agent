# Relatório de auditoria de UI: [produto, rota ou componente]

Template T-02. Uso: `ui-audit` e `design-evaluator`. Somente leitura: este relatório não altera o produto. Cada achado precisa de local e evidência; sem evidência, a linha vira "não verificado". Opinião de modelo da mesma família não é validação externa.

## 1. Escopo e limitações

- **Material auditado:** [URL, arquivos, capturas, markup] · **Data:** [AAAA-MM-DD]
- **Contexto lido:** [DESIGN.md, tokens, tema] ou "nenhum encontrado"
- **Superfície:** [Persuade | Operate | Read | Experience]
- **Viewports vistos:** [375, 768, 1440 px] · **Como foi visto:** [renderizado e medido | só markup (tudo visual é Inferido) | só capturas]
- **Não foi possível:** [abrir navegador, testar teclado, leitor de tela…]

## 2. Teste de tronco (por página)

| Pergunta | Resposta (clara/parcial/não) |
| --- | --- |
| Que site é este? | |
| Que página é esta? | |
| Quais as seções principais? | |
| Quais as opções neste nível? | |
| Onde estou no esquema? | |
| Como busco? | |

Resultado: [PASS (6 claras) | PARTIAL (4 a 5) | FAIL (3 ou menos)]. FAIL é impacto alto mesmo com bom acabamento.

## 3. Resumo por categoria

| # | Categoria | Resultado | Impacto máximo | Natureza |
| --- | --- | --- | --- | --- |
| 1 | Hierarquia e composição | [PASS/PARTIAL/FAIL] | [alto/médio/polimento] | [script/julgamento] |
| 2 | Tipografia | | | |
| 3 | Cor e contraste | | | |
| 4 | Espaçamento e layout | | | |
| 5 | Estados de interação | | | |
| 6 | Responsividade | | | |
| 7 | Movimento | | | |
| 8 | Conteúdo e microcopy | | | |
| 9 | Sinais de visual genérico de IA | | | |
| 10 | Desempenho percebido | | | |

Natureza: `[verificável por script]` (contraste, alvo, título pulado, `outline: none`, `transition: all`) ou `[julgamento: Inferido]`.

## 4. Achados

Profundidade sobre amplitude: 5 a 10 achados bem documentados.

| ID | Categoria | Impacto | Local (arquivo:linha, seletor ou captura) | Evidência | Critério | Correção sugerida | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A-01 | [Cor e contraste] | [alto] | [`.field-label` em `forms.css:42`] | [#777777 sobre #FFFFFF = 4,48:1, calculado, estado padrão] | [WCAG 1.4.3] | [#767676 ou mais escuro (4,54:1)] | [Verificado] |

Formato de crítica por achado de julgamento: observação neutra ("Eu noto…"), problema e por que importa para o objetivo do usuário, correção específica.

## 5. Estados e dados extremos

[vazio, carregando, erro, nome de 47 caracteres, zero resultados: verificado ou não, com o motivo]

## 6. Quick wins e top 3

- **Quick wins (3 a 5 correções de baixo esforço):** [A-0x, A-0y…]
- **Top 3 de impacto alto:** [A-0x, A-0y, A-0z]

## 7. Nota opcional (indicador relativo, Inferido)

Nota de A a F por categoria: cada achado alto desce uma letra, médio meia letra, polimento não conta. Os pesos do gstack (hierarquia, tipografia e espaçamento com 15% cada etc.) são escolha de um autor. Use só para comparar antes e depois; não é métrica de qualidade absoluta.

## 8. Não verificado

- [Lista explícita do que não foi checado e como confirmar]

## 9. O que exige usuários reais

[Os 3 achados mais graves que dependem de comportamento e o que testar]
