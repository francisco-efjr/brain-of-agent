---
name: direcao-landing-clinica-vet
description: Mede se, ao pedirem a direção visual de uma landing antes de codar, o plugin entrega brief de uma linha, plano compacto com cores em hex e tipografia, revisão contra escolhas genéricas e piso de qualidade, sem escrever código final nem afirmar que renderizou ou testou no celular.
tags: [ux-ui-design, design-brief, direcao-visual]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega brief de uma linha, plano com 4 a 6 cores nomeadas com hex e papel, 1 ou 2 famílias tipográficas, esboço de layout e 2 ou 3 princípios; lista escolhas genéricas trocadas ou justificadas; cita estados, foco visível, prefers-reduced-motion e 320 px; declara que nada foi renderizado; não escreve código final nem arquivos antes do aceite."
model: sonnet
---
Antes de eu codar, define a direção visual da landing da Clínica Vet Bairro Novo. É uma clínica veterinária de bairro em Fortaleza, atende cães e gatos, o agendamento é por WhatsApp. Os tutores têm de 25 a 55 anos e acessam quase só pelo celular. Ainda não temos marca: só o nome e um logo que ainda vai ser feito. O site vai ser implementado depois, por outra pessoa, em Next.js.

Quero cores, fontes e layout, e que não pareça feito por IA. Ainda não escreve código; me mostra o plano para eu aprovar.
