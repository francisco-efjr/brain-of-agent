# Modelo de PRD enxuto e exemplo

Estrutura destilada de V-34 (limites mensuráveis, `TBD`, non-goals) e V-35 (até 3 perguntas, 600 a 1.000 palavras, premissas explícitas), com redação própria. Os fluxos de origem são MIT (awesome-copilot, phuryn/pm-skills).

## Sumário

- [Modelo das 10 seções](#modelo-das-10-seções)
- [Tabela de métrica com definição operacional](#tabela-de-métrica-com-definição-operacional)
- [Matriz dos quatro riscos](#matriz-dos-quatro-riscos)
- [Exemplo: resposta quando faltam dados](#exemplo-resposta-quando-faltam-dados)
- [Exemplo: trecho de PRD com lacunas honestas](#exemplo-trecho-de-prd-com-lacunas-honestas)

## Modelo das 10 seções

Orçamento de palavras sugerido (soma 600 a 1.000; é Suposição de calibração, ajuste ao caso):

| # | Seção | Palavras | Conteúdo mínimo |
| --- | --- | --- | --- |
| 1 | Resumo | 50 a 80 | problema, para quem, resultado esperado, em 3 a 4 frases |
| 2 | Problema e contexto | 80 a 150 | situação atual, evidência (com origem) e o que acontece se nada for feito |
| 3 | Objetivos e métricas | 80 a 150 | 3 a 5 objetivos, cada um com métrica de definição operacional |
| 4 | Usuários e segmentos | 50 a 100 | quem usa, quem decide, quem é afetado |
| 5 | Não-objetivos | 40 a 80 | pelo menos 2; o que alguém poderia esperar e não entra |
| 6 | Solução | 100 a 200 | comportamento e experiência, sem tecnologia; fluxo principal e bordas relevantes |
| 7 | Requisitos de alto nível | 60 a 150 | `FR-01`... "o sistema deve..." um por linha; detalhe vai para a spec da feature |
| 8 | Riscos | 60 a 120 | matriz dos quatro riscos, com dono |
| 9 | Premissas e perguntas abertas | 50 a 100 | Suposições, `TBD`, perguntas com dono |
| 10 | Faseamento | 40 a 80 | MVP, v1.1, v2.0 como fatias que entregam valor; critério para avançar |

Requisitos de IA (só se o produto usa IA): comportamento esperado, limites, como avaliar. Entram como seção 7b.

## Tabela de métrica com definição operacional

Conhecimento estável do domínio (Inferido): uma métrica sem fórmula, fonte e janela não pode ser medida por duas pessoas do mesmo jeito.

| Campo | Exemplo (ilustrativo, números não são recomendação) |
| --- | --- |
| Nome | Taxa de cadastro concluído |
| Fórmula | cadastros concluídos / cadastros iniciados |
| Fonte do dado | `TBD` (qual evento ou tabela registra início e conclusão?) |
| Janela | por semana, coorte da semana de início |
| Baseline | `TBD` (medir antes de prometer meta) |
| Meta | `TBD` até existir baseline; depois "+X pontos percentuais em Y semanas" |
| Origem da meta | Suposição / estimativa / dado |

Regra: meta sem baseline é Suposição. Escreva isso.

## Matriz dos quatro riscos

Fonte: V-25 (Marty Cagan, SVPG, 2017-12-04). Donos sugeridos pela fonte: produto para valor e negócio, design para usabilidade, engenharia para viabilidade.

| Risco | Pergunta de teste | Dono | Evidência que resolve | Status |
| --- | --- | --- | --- | --- |
| Valor | As pessoas vão querer isto? | produto | entrevistas sobre comportamento passado, teste de fumaça | aberto |
| Usabilidade | Conseguirão usar? | design | teste de usabilidade (vá a `ux-ui-design`) | aberto |
| Viabilidade | Conseguimos construir com o que temos? | engenharia | `feasibility-scout`, protótipo descartável | aberto |
| Negócio | Funciona para o negócio (custo, jurídico, canais)? | produto | análise de custo, parecer do jurídico | aberto |

## Exemplo: resposta quando faltam dados

Pedido: "Escreve um PRD para um app de delivery de marmitas fit."

Faltam problema, usuário e métrica. Resposta correta, sem PRD:

```text
Para o PRD não sair com palpites, preciso de três respostas que só você tem:
1. Que problema concreto você quer resolver, e para quem? (ex.: quem pede marmita hoje, onde, e o que
   falha na opção atual)
2. Quem é o primeiro usuário que você quer atender (perfil, cidade, canal por onde chega)?
3. Como você vai saber que funcionou nos primeiros 3 meses? (um número ou fato observável; se ainda
   não sabe, eu registro como lacuna)
Não vou incluir tamanho de mercado, concorrentes nem metas que você não me der. Quando responder,
escrevo o PRD em até 1.000 palavras, com o que continuar desconhecido em "Premissas e perguntas abertas".
```

## Exemplo: trecho de PRD com lacunas honestas

Cenário: usuário respondeu só o problema ("meus clientes esquecem de repetir o pedido semanal").

```markdown
## 3. Objetivos e métricas
| Objetivo | Métrica (nome, fórmula) | Fonte | Janela | Baseline | Meta |
| --- | --- | --- | --- | --- | --- |
| Reduzir pedidos semanais esquecidos | pedidos recorrentes concluídos / clientes com pedido na semana anterior | TBD | semana | TBD | TBD (Suposição: definir após medir 4 semanas) |

## 9. Premissas e perguntas abertas
- Suposição: o esquecimento é a causa principal da queda de pedidos. Evidência atual: relato do solicitante, sem dados.
  Se estiver errada: o lembrete não move a métrica.
- [NEEDS CLARIFICATION: existe cadastro com histórico de pedidos por cliente? | dono: operação]
- TBD: meta de recorrência (depende do baseline).
```

O que mostra: tudo que não foi dado vira Suposição ou `TBD` com dono; o PRD não afirma mercado, preço nem concorrente.
