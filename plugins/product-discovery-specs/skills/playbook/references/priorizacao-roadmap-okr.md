# Priorização, roadmap e OKR

Como escolher o framework certo, pontuar com origem declarada e montar roadmap, OKRs e pitches sem falsa precisão. Leia ao usar `prioritize-roadmap` ou `write-prd`. Fontes: V-21, V-22, V-23, V-24, V-26, V-43, V-45 (destiladas; classes em [fontes.md](fontes.md)).

## Sumário

- [1. Árvore de decisão do framework](#1-árvore-de-decisão-do-framework)
- [2. RICE](#2-rice)
- [3. ICE e Opportunity Score](#3-ice-e-opportunity-score)
- [4. MoSCoW](#4-moscow)
- [5. Kano](#5-kano)
- [6. Sensibilidade e revisão humana](#6-sensibilidade-e-revisão-humana)
- [7. Roadmap Now-Next-Later](#7-roadmap-now-next-later)
- [8. OKR](#8-okr)
- [9. Definição operacional de métrica](#9-definição-operacional-de-métrica)
- [10. Pitch com apetite](#10-pitch-com-apetite)

## 1. Árvore de decisão do framework

Escolha pelo **objeto** que está sendo ordenado (V-24, skill de priorização do phuryn/pm-skills, MIT; "priorize problemas, não funcionalidades"):

| O que você ordena | Framework | Fórmula ou saída |
| --- | --- | --- |
| Problemas de cliente (com pesquisa de importância e satisfação) | Opportunity Score | Importância x (1 - Satisfação), ambas normalizadas de 0 a 1 |
| Ideias ou iniciativas, com pouco dado | ICE | Impacto x Confiança x Facilidade |
| Ideias ou iniciativas, com estimativa de alcance e esforço | RICE | (Alcance x Impacto x Confiança) / Esforço |
| Requisitos dentro de um escopo de entrega | MoSCoW | Must, Should, Could, "não nesta entrega" |
| Expectativas de funcionalidades | Kano | Classifica o tipo de atributo; **não ordena** |
| Várias dimensões sem dados | Matriz ponderada (pesos declarados) | Soma ponderada; os pesos são Suposição |

Perguntas antes de pontuar: qual é o resultado alvo do trimestre? Quem decide? Que dado existe (analytics, pesquisa, suporte)? Sem dado, o número é Suposição e o framework é só uma forma de organizar a conversa.

## 2. RICE

Fonte: Sean McBride, Intercom, 2018-01-05 (V-21, classe B). A fórmula aparece como imagem no artigo e é corroborada pela skill do phuryn (MIT): **(Alcance x Impacto x Confiança) / Esforço**.

| Fator | Definição | Escala (versão Intercom) |
| --- | --- | --- |
| Alcance (R) | quantas pessoas ou eventos por período | número, com período declarado (ex.: usuários por trimestre) |
| Impacto (I) | efeito por pessoa alcançada | 3 massivo, 2 alto, 1 médio, 0,5 baixo, 0,25 mínimo |
| Confiança (C) | quanto se confia nas estimativas | 100% alta, 80% média, 50% baixa; abaixo disso é "moonshot" |
| Esforço (E) | pessoa-mês, total do time | número; 0,5 para menos de um mês |

Regras:

1. **Registre a versão da escala** na planilha (resumos secundários citam outras, como 20% para confiança mínima). Padrão deste plugin: Intercom.
2. Cada número tem **origem**: dado (com fonte), estimativa (de quem) ou Suposição. "Sem dado de alcance, confiança 50%" é Inferido, regra deste plugin.
3. Não misture escalas de impacto entre listas; não compare RICE entre objetivos diferentes sem normalizar (Inferido; a fonte só diz que o RICE não é regra absoluta).
4. Recalcule a aritmética; uma conta errada num ranking é falsa precisão.

Exemplo (trimestre; dados fornecidos pelo usuário, sem acréscimos nossos):

| Item | Alcance | Impacto | Confiança | Esforço (pessoa-mês) | RICE |
| --- | --- | --- | --- | --- | --- |
| A | 2.000 | 2 | 80% | 2 | 2.000 x 2 x 0,8 / 2 = **1.600** |
| B | 500 | 3 | 100% | 1 | 500 x 3 x 1 / 1 = **1.500** |
| C | 8.000 | 1 | 50% | 4 | 8.000 x 1 x 0,5 / 4 = **1.000** |
| D | 300 | 0,5 | 100% | 0,5 | 300 x 0,5 x 1 / 0,5 = **300** |

Ordem: A, B, C, D. Sensibilidade: A e B estão a 6% de distância (1.600 contra 1.500); se a confiança de A cair de 80% para 50%, A vai a 1.000 e perde para B. Diga isso e deixe a decisão com o humano.

## 3. ICE e Opportunity Score

- **ICE** = Impacto x Confiança x Facilidade, cada fator em escala de 1 a 10 declarada (V-24; a origem em Sean Ellis é lacuna, ver [fontes.md](fontes.md)). Mais rápido que o RICE; pior para comparar iniciativas de tamanhos diferentes, porque "facilidade" esconde o esforço absoluto.
- **Opportunity Score** = Importância x (1 - Satisfação), com ambas de 0 a 1 vindas de pesquisa real. Sem pesquisa, não calcule: gere perguntas de pesquisa.

## 4. MoSCoW

Dai Clegg, 1994 (RAD), usado com DSDM (V-23, Wikipedia, classe B).

| Categoria | Regra de corte | Campo extra |
| --- | --- | --- |
| Must | sem isso a entrega falha ou é ilegal/insegura | motivo |
| Should | importante, mas há contorno temporário | contorno |
| Could | desejável; entra se sobrar capacidade | |
| **Não nesta entrega** (Won't) | decidido fora **desta** entrega | **reavaliar em:** data ou evento |

Críticas conhecidas (V-23): "Won't" é ambíguo (parece "nunca"), e não há ordem dentro da categoria. Por isso o rótulo "não nesta entrega" e o campo "reavaliar em". Limite de bolso para Musts é Suposição: se mais da metade do escopo é Must, o corte não aconteceu.

## 5. Kano

Noriaki Kano, anos 1980 (V-22, Wikipedia, classe B; seções sem fonte no artigo, **conferir o original antes de tratar a tabela como regra**). Categorias: must-be, one-dimensional, attractive, indifferent, reverse.

Pergunta em **pares** para cada funcionalidade, com cinco respostas possíveis (gosto, espero, neutro, tolero, desgosto):

- Funcional: "Se o produto **tiver** [funcionalidade], como você se sente?"
- Disfuncional: "Se o produto **não tiver** [funcionalidade], como você se sente?"

Leitura simplificada (Inferido; conhecimento estável do método, não verificado nesta consulta): funcional "gosto" + disfuncional "desgosto" indica one-dimensional; "gosto" + qualquer resposta intermediária indica attractive; resposta intermediária + "desgosto" indica must-be; "neutro" nos dois lados indica indifferent; combinações incoerentes indicam resposta duvidosa ou reverse.

Usar para **classificar** expectativas, nunca para ordenar. Exige pesquisa com usuários reais; sem ela, não preencha a matriz.

## 6. Sensibilidade e revisão humana

1. Mostre o que muda o ranking: varie 1 fator por vez nos itens vizinhos (como no exemplo A e B).
2. Peça ao usuário para revisar scores que pareçam errados (recomendação do artigo original do RICE).
3. Destaque empates técnicos (diferença menor que a incerteza das estimativas) e use critério de desempate declarado (risco, dependência, aprendizado).
4. A decisão final é humana; o entregável termina com "decisão a cargo de [dono]".

## 7. Roadmap Now-Next-Later

ProdPad (V-45, classe B com nota 5: fonte comercial e autoatribuída; Janna Bastow reivindica a invenção). Colunas:

- **Now:** em andamento e bem definido.
- **Next:** fila depois do Now, menos detalhe.
- **Later:** problemas maiores e vagos, ainda não decompostos.

Justificativa: roadmap por data força prazos e reduz flexibilidade. Campos por item: **problema**, **resultado esperado**, **grau de certeza** (alto, médio, baixo; Suposição declarada), objetivo de negócio ligado. Datas são opcionais; se existirem, são estimativas rotuladas. Template: [roadmap-nnl.md](../assets/templates/roadmap-nnl.md). Lacuna: não há segunda fonte nem fonte para roadmap por resultado (Pichler, Perri, SVPG); trate como prática difundida, não como método validado.

Publicar o roadmap (wiki, Slack, ferramenta de tracker) é ação externa: só com confirmação do texto exato.

## 8. OKR

Guia Google re:Work (V-43, classe B): um objetivo qualitativo por bloco; **cerca de três** key results mensuráveis por objetivo; 3 a 5 objetivos por equipe; nota de 0,0 a 1,0; sucesso é cerca de 0,7 e o "ponto ideal" é 0,6 a 0,7; nota baixa é dado para calibrar o próximo ciclo; **OKR não é avaliação de desempenho**; as notas não são ciência. A página não usa a dicotomia "comprometido e aspiracional" (resumos de terceiros usam; não a trate como regra do Google).

Regras do plugin:

1. Objetivo: qualitativo, inspirador, sem número.
2. Key result: mede resultado, não atividade ("reduzir o tempo de primeira resposta de 6 h para 2 h", e não "lançar chatbot").
3. Cada KR com **definição operacional** (próxima seção) e baseline; sem baseline, `TBD`.
4. Nota 0 a 1 no fim do ciclo, para calibração; nunca para ranquear pessoas. Se o usuário pedir "use o OKR para avaliar o time", explique a ressalva da fonte e ofereça outro instrumento.

Template: [okr.md](../assets/templates/okr.md). Sem evidência de eficácia na fonte.

## 9. Definição operacional de métrica

Vale para KRs e para as métricas de sucesso do PRD (conhecimento estável do domínio; Inferido, sem fonte A no atlas). Toda métrica traz:

| Campo | Exemplo |
| --- | --- |
| Nome | Taxa de ativação em 7 dias |
| Fórmula | usuários que concluíram [evento X] em até 7 dias após o cadastro / usuários cadastrados no mesmo dia |
| Fonte do dado | tabela ou evento de analytics, com responsável |
| Janela e frequência | coorte semanal; leitura toda segunda |
| Baseline | valor atual com data, ou `TBD` |
| Meta | valor e prazo, com a origem da meta (dado, estimativa, Suposição) |
| Guarda | métrica que não pode piorar (ex.: tickets de suporte por usuário) |

North Star, HEART e AARRR são citados na literatura de produto, mas **não têm fonte validada neste atlas**: não os apresente como boa prática comprovada; se o usuário os trouxer, use-os como vocabulário dele.

## 10. Pitch com apetite

Shape Up (Ryan Singer, Basecamp/37signals; V-26; texto protegido, © 37signals: **apenas destilar, nunca reproduzir**). Estrutura do pitch: **problema** (com um caso real), **apetite** (quanto tempo vale a pena gastar, definido antes da solução e inverso de estimativa), **solução de baixa fidelidade** (elementos e fluxo, sem pixel), **limites** (o que fica de fora), **rabbit holes** (riscos técnicos ou de produto a resolver antes), **no-gos** (decisões deliberadas de não fazer) e **riscos de premissa**. O ciclo de seis semanas e a betting table são contexto do autor; adapte ao seu ritmo. Template: [pitch.md](../assets/templates/pitch.md).
