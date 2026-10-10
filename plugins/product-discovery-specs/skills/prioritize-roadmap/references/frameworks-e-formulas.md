# Frameworks de priorização: escalas, fórmulas e exemplo

Fontes: V-21 (RICE, Intercom, Sean McBride, 2018-01-05), V-22 (Kano, Wikipedia), V-23 (MoSCoW, Wikipedia), V-24 (phuryn/pm-skills `prioritization-frameworks`, MIT), V-32 (Opportunity Score). Tudo destilado com redação própria. Registre sempre a versão da escala usada.

## Sumário

- [Árvore de decisão](#árvore-de-decisão)
- [RICE](#rice)
- [Exemplo RICE resolvido](#exemplo-rice-resolvido)
- [ICE](#ice)
- [Opportunity Score](#opportunity-score)
- [MoSCoW](#moscow)
- [Kano](#kano)
- [Lacunas de evidência](#lacunas-de-evidência)

## Árvore de decisão

```text
O que estou priorizando?
|- problemas de cliente, com dado de importância e satisfação -> Opportunity Score
|- ideias ou iniciativas
|    |- tenho dado de alcance? -> RICE
|    '- só julgamento rápido?  -> ICE (e diga que é julgamento)
|- requisitos de uma entrega com capacidade fixa -> MoSCoW
'- expectativas de recurso (o que o cliente espera, encanta, ignora) -> Kano (classifica; depois priorize com outro framework)
```

Antes de pontuar: existe um resultado alvo? Qual a fonte de cada número? Quem vai revisar os scores que pareçam errados?

## RICE

Fórmula: **(Alcance x Impacto x Confiança) / Esforço**. O artigo do Intercom traz a fórmula como imagem; a mesma fórmula aparece na skill do phuryn (MIT), que corrobora (V-21).

| Fator | Definição | Escala (Intercom 2018) |
| --- | --- | --- |
| Alcance | pessoas ou eventos afetados em um período declarado | número real; declare o período (ex.: por trimestre) |
| Impacto | efeito em cada pessoa alcançada | 3 massivo, 2 alto, 1 médio, 0,5 baixo, 0,25 mínimo |
| Confiança | quanto os dados sustentam as estimativas | 100% alta, 80% média, 50% baixa; abaixo disso, "moonshot" |
| Esforço | trabalho total | pessoa-mês; 0,5 para menos de um mês |

Notas:

- Algumas fontes secundárias citam confiança de até 20%: por isso a versão é registrada (V-21).
- "Sem dado de alcance, confiança 50%" é Inferido, não está no artigo.
- "Não comparar RICE entre objetivos diferentes" não foi confirmado na fonte; trate como cautela razoável, não como regra.
- O artigo diz que RICE não é regra absoluta: revise scores que pareçam errados.

## Exemplo RICE resolvido

Enunciado: priorizar com RICE (trimestre) quatro itens. Dados fornecidos pelo usuário (nada foi acrescentado):

| Item | Alcance | Impacto | Confiança | Esforço (pessoa-mês) | Score = R x I x C / E |
| --- | --- | --- | --- | --- | --- |
| A | 2000 | 2 | 80% | 2 | 2000 x 2 x 0,8 / 2 = **1600** |
| B | 500 | 3 | 100% | 1 | 500 x 3 x 1 / 1 = **1500** |
| C | 8000 | 1 | 50% | 4 | 8000 x 1 x 0,5 / 4 = **1000** |
| D | 300 | 0,5 | 100% | 0,5 | 300 x 0,5 x 1 / 0,5 = **300** |

Ordem: A > B > C > D. Versão da escala: Intercom 2018 (impacto 3/2/1/0,5/0,25; confiança 100/80/50%; esforço em pessoa-mês). Origem dos números: informados pelo usuário (não verificados por mim; não sei se são dado ou estimativa).

Conferência:

```bash
python -c "print(2000*2*0.8/2, 500*3*1/1, 8000*1*0.5/4, 300*0.5*1/0.5)"
# 1600.0 1500.0 1000.0 300.0
```

Sensibilidade (mudanças plausíveis, calculadas):

| Cenário | Efeito |
| --- | --- |
| A tem confiança 50% em vez de 80% | A = 1000, empata com C e cai abaixo de B (1500) |
| B tem impacto 2 em vez de 3 | B = 1000, empata com C |
| A com esforço 3 em vez de 2 | A = 1066,7; cai abaixo de B |
| C com confiança 80% em vez de 50% | C = 1600, empata com A no topo |

Leitura: A e B estão a 6% um do outro; qualquer revisão pequena de confiança inverte a ordem. Trate A e B como empate técnico (limiar de 15% é Suposição de calibração). D está claramente atrás. O ranking apoia a conversa; a decisão é do humano. Pergunta útil: o que daria mais certeza sobre a confiança de A e de B?

## ICE

**Impacto x Confiança x Facilidade** (V-24). A fonte não fixa a escala; defina e registre (por exemplo 1 a 10 para cada fator, Suposição), e lembre que Facilidade é o inverso de esforço (maior = mais fácil). ICE é julgamento rápido: diga isso. Para ordenar poucos itens com pouco dado, é suficiente; para decisões caras, prefira RICE ou evidência.

## Opportunity Score

**Importância x (1 - Satisfação)**, com ambos normalizados de 0 a 1 (V-24, V-32). Requer dado de pesquisa: alto score = muito importante e mal atendido. Sem dado de importância e satisfação fornecido pelo usuário, não calcule.

## MoSCoW

Origem: Dai Clegg (1994, RAD), usado em DSDM (V-23).

| Categoria | Significado | Regra de corte |
| --- | --- | --- |
| Must | sem isso a entrega falha ou não faz sentido | a soma dos Must cabe na capacidade; se não cabe, a classificação falhou ou o escopo está grande |
| Should | importante, mas há contorno | entra se sobrar capacidade |
| Could | desejável, baixo custo de ficar de fora | primeiro a sair |
| Won't | **nesta entrega** | registre "não nesta entrega" e o campo "reavaliar em" |

Críticas conhecidas (V-23): a ambiguidade do Won't (parece "nunca") e a falta de ordem dentro de cada categoria. Mitigue com o rótulo e ordenando os Must por dependência ou valor.

## Kano

Classifica expectativas; não prioriza (V-22). Categorias: *must-be*, *one-dimensional*, *attractive*, *indifferent*, *reverse* (a página usa esses nomes; "basic" e "performance" aparecem como sinônimos em outra seção).

Pergunta em par para cada recurso, respondendo com uma de cinco opções (gosto, espero, neutro, tolero, desgosto):

- Funcional: "Se o produto tiver `<recurso>`, como você se sente?"
- Disfuncional: "Se o produto não tiver `<recurso>`, como você se sente?"

Tabela de avaliação mais citada (conhecimento estável, **Inferido**: a página da Wikipedia tem uma tabela de avaliação, mas confira o original antes de usar como regra, V-22). Linhas = resposta funcional; colunas = resposta disfuncional. A = attractive, O = one-dimensional, M = must-be, I = indifferent, R = reverse, Q = questionable (resposta contraditória).

| Funcional \ Disfuncional | gosto | espero | neutro | tolero | desgosto |
| --- | --- | --- | --- | --- | --- |
| gosto | Q | A | A | A | O |
| espero | R | I | I | I | M |
| neutro | R | I | I | I | M |
| tolero | R | I | I | I | M |
| desgosto | R | R | R | R | Q |

Exige pesquisa com usuários reais. Sem respostas, diga "não é possível classificar" em vez de supor categorias.

## Lacunas de evidência

WSJF e Kano em fonte primária, e ICE na fonte original (Sean Ellis), não foram lidos no atlas (VALIDATED, lacuna 7). Por isso este plugin trata ICE e Kano como instrumentos de apoio e não como práticas validadas em fonte primária.
