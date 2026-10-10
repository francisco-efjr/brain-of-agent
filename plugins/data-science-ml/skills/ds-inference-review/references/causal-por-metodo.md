# Causal por método: perguntas, diagnósticos e refutações

Validado em 2026-10-10. Estrutura do protocolo e da árvore por mecanismo: V-28 (Jill0099 `causal-inference-mixtape`, classe C, 17 estrelas; abstract do DoWhy, arXiv 2011.04216: Model, Identify, Estimate, Refute). Conteúdo redigido pelo plugin; os diagnósticos de cada método são conhecimento estável de econometria e inferência causal (Inferido). Fontes primárias (Hernán e Robins, documentação do DoWhy e EconML) **não foram lidas** (lacuna 6): trate como roteiro de revisão, não como norma. Nada aqui manda instalar pacote: se o usuário usar uma biblioteca, ele a instala; confira a API na versão dele.

## Sumário
1. Perguntas antes do método
2. DiD e event study
3. RDD
4. Controle sintético
5. IV
6. Matching, IPW, DML
7. Refutação e sensibilidade
8. Exemplo: programa de fidelidade em 3 lojas
9. Linguagem permitida

## 1. Perguntas antes do método

1. Qual é o **estimando**? (efeito médio em quem, comparado a qual alternativa, em que horizonte)
2. **Como o tratamento foi atribuído?** (sorteio, regra de corte, escolha do gestor, adoção escalonada, auto-seleção)
3. Quem decidiu e com que informação? (a resposta aponta os confundidores)
4. Há interferência entre unidades (spillover, canibalização, efeitos de rede)?
5. Quais dados existem antes do tratamento?
6. O DAG: variáveis que causam tratamento e desfecho (confundidores), mediadores, colisores. O usuário confirma o grafo antes do código.

## 2. DiD e event study

- Premissas: tendências paralelas na ausência do tratamento; sem antecipação (comportamento não muda antes da data); sem spillover entre tratados e controles; composição estável.
- Diagnósticos: gráfico de médias pré-tratamento; **event study** com coeficientes de "leads" (devem ser indistinguíveis de zero); sensibilidade à escolha do grupo controle; placebo em datas pré-tratamento falsas.
- Erro-padrão agrupado no nível da atribuição (loja, região). Com poucos clusters tratados ou totais, o erro robusto é instável: use inferência por permutação/placebo e comunique cautela.
- Adoção em datas diferentes: o DiD de dois fatores (TWFE) pode enviesar quando os efeitos variam no tempo ou entre coortes; use estimadores robustos (Callaway-Sant'Anna, Sun-Abraham) e a decomposição de Bacon para diagnosticar (V-28).

## 3. RDD

- Premissas: a variável de corrida não é manipulada na vizinhança do corte; as demais variáveis são contínuas no corte; o efeito é **local** (vale perto do corte).
- Diagnósticos: **teste de manipulação** (densidade da variável de corrida) antes de estimar; continuidade de covariáveis; sensibilidade a largura de banda e à ordem do polinômio; placebo em cortes falsos.

## 4. Controle sintético

- Quando: uma (ou poucas) unidade tratada e muitas candidatas a controle com longa série pré-tratamento.
- Premissas: o sintético reproduz a unidade tratada **antes** do tratamento; sem choques específicos coincidentes; sem spillover.
- Diagnósticos: qualidade do ajuste pré-tratamento (se ruim, o método não se aplica); **inferência por permutação** (rodar o mesmo procedimento em unidades de controle e comparar o efeito); remover doadores um a um.

## 5. IV

- Premissas: relevância (o instrumento move o tratamento: reporte a estatística da primeira etapa; F > 10 é regra de bolso, Inferido), exclusão (o instrumento só afeta o desfecho via tratamento; **não testável**: argumente), monotonicidade. Estima efeito local (LATE), não o efeito médio da população.
- Diagnósticos: primeira etapa reportada; resultados com erro-padrão correto; discussão explícita da exclusão.

## 6. Matching, IPW, DML

- Premissas: sem confundidor não medido (não testável); **sobreposição** (cada perfil tem chance de ser tratado e não tratado).
- Diagnósticos: balanceamento de covariáveis depois do ajuste (diferença padronizada; < 0,1 é regra de bolso), distribuição de escores de propensão, pesos extremos.
- Não controle colisores nem mediadores quando o estimando é o efeito total.
- Sensibilidade a confundidor não observado (por exemplo, E-value ou análise de Rosenbaum; Inferido): quão forte um confundidor precisaria ser para anular o resultado?

## 7. Refutação e sensibilidade

Exija ao menos uma; reporte o resultado, mesmo quando desconfortável.
- **Placebo no tempo**: tratar uma data pré-tratamento; efeito deve ser ~0.
- **Placebo na unidade ou no desfecho**: desfecho que o tratamento não deveria afetar.
- **Confundidor aleatório**: adicionar um confundidor aleatório; a estimativa não deve mudar.
- **Subconjunto**: reestimar em subamostras; deve ser estável.
- **Sensibilidade**: o tamanho de um confundidor não medido que anularia o efeito.
Bibliotecas como DoWhy empacotam refutadores desse tipo (nomes e assinaturas: confira na documentação da versão instalada; a documentação não foi lida neste plugin).

## 8. Exemplo: programa de fidelidade em 3 lojas (caso de eval E-08)

Pedido: "lançamos fidelidade em 3 lojas em março; comparei vendas dessas 3 com 20 outras antes e depois: +12%. Confirma que o programa causou?"

Resposta esperada, em ordem:
1. Perguntar o estimando e **como as 3 lojas foram escolhidas** (gestores escolheram as melhores? as de maior crescimento? sorteio?).
2. Reconhecer o desenho: antes/depois com controles → DiD. Premissas: tendências paralelas pré-março, nada mudou só nas 3 lojas em março (campanha local, reforma), sem canibalização entre lojas próximas.
3. Pedir série mensal por loja, ao menos 12 meses antes; checar tendências pré e fazer event study com leads.
4. Agrupar o erro-padrão por loja; **com 3 tratadas** a inferência é frágil: sugerir controle sintético/permutação como complemento e declarar a limitação.
5. Refutação: placebo em uma data anterior (por exemplo, novembro); desfecho placebo (categoria não afetada pelo programa).
6. Linguagem: sem identificação, "as 3 lojas tiveram vendas 12% maiores que as outras 20 depois de março; isso é compatível com um efeito do programa, mas não o distingue de seleção das lojas ou de choques locais".

## 9. Linguagem permitida

| Situação | Pode escrever | Não escreva |
| --- | --- | --- |
| Experimento randomizado íntegro (SRM ok) | "A variante aumentou X em Y (IC 95% ...)" | "para todos os usuários, sempre" sem discutir validade externa |
| Observacional com desenho identificável e refutações passadas | "estimamos que o tratamento aumentou X em Y sob as premissas P1..Pn" | "provamos" |
| Observacional sem desenho | "X está associado a Y; não identificamos efeito causal" | "causou", "gerou", "impactou" |
