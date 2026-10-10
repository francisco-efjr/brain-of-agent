---
name: plataforma-android-criterios
description: Mede se os critérios de aceite de uma história de app Android cobrem as particularidades da plataforma (permissão de localização, GPS, offline, app encerrado, fuso e hora do aparelho, dado pessoal), sem inventar limites e apontando o plugin de mobile para a profundidade.
tags: [product-discovery-specs, acceptance-criteria, android, platform-coverage]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Critérios declarativos com caminho feliz, permissão negada ou apenas aproximada, GPS desligado ou impreciso, sem conexão com sincronização posterior, app encerrado, hora do aparelho contra hora do servidor e dado pessoal, limites como pergunta ou Suposição, e indicação do plugin mobile-apps para o detalhe de plataforma."
model: sonnet
---
App Android de ponto eletrônico para uma rede de lojas. A história é: "Como funcionário, quero registrar meu ponto pelo celular para comprovar que estava no local de trabalho." O registro usa a localização do aparelho. Os funcionários usam celulares próprios, de modelos variados, e nem todas as lojas têm bom sinal de internet. Escreve os critérios de aceite.
