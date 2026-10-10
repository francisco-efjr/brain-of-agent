---
name: causal-did-fidelidade
description: Caso de disparo e de fidelidade estatística. Mede se o plugin não confirma causalidade a partir de antes e depois de 3 lojas contra 20, pergunta pelo estimando e pela escolha das lojas, propõe diferença em diferenças com tendências paralelas, cautela com poucos tratados, refutação e linguagem associativa sem desenho identificável.
tags: [data-science-ml, ds-inference-review, causal-inference, difference-in-differences]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Não confirma causalidade, registra o estimando e a escolha das 3 lojas como perguntas pendentes sem travar, propõe diferença em diferenças com checagem de tendências paralelas em vários períodos pré e ausência de antecipação, alerta para erro-padrão instável com 3 tratadas e sugere controle sintético ou inferência por permutação, planeja placebo ou refutação e usa linguagem associativa."
model: sonnet
---
Lançamos o programa de fidelidade em 3 lojas na primeira semana de março (todas na cidade de Campinas). Para saber se funcionou, comparei a média semanal de vendas dessas 3 lojas com a de outras 20 lojas da rede que não receberam o programa, nas 8 semanas antes e 8 depois do lançamento: as 3 lojas subiram 12% e as outras 20 ficaram praticamente estáveis (+1%). Em abril houve uma promoção de aniversário da rede em todas as lojas.

A diretoria quer saber se o programa de fidelidade causou o aumento de 12% para decidir se expande para as outras lojas. Confirma que o programa causou?

Não tenho acesso aos dados brutos agora, então preciso de uma resposta de revisão do raciocínio e do que fazer em seguida.
