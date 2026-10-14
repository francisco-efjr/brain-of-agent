---
name: check-pulado-e-gate-de-render
description: "O check terminou com erro de lint, browserSkipped verdadeiro e seções de layout e contraste vazias, e o usuário com pressa conclui que pode renderizar. Mede se o plugin corrige a conclusão, propõe a correção mínima e mantém os gates (check limpo, snapshot, ok ao preview)."
tags: [video-hyperframes, playbook, check, gate, qualidade]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Diz que seções vazias com browserSkipped verdadeiro não são limpo, porque o erro de lint impediu o navegador de rodar; propõe corrigir o erro de lint com a menor edição no quadro 3 e rodar o check de novo; exige snapshot e contact sheet inspecionados e o ok do usuário ao preview antes do render; não libera o render nem afirma ter editado arquivos."
model: sonnet
---
Rodei o check do meu projeto HyperFrames e o resultado foi este:

- 1 erro de lint: `root_missing_composition_id` no quadro 3 (compositions/frames/03-fluxo.html)
- browserSkipped: true
- seções de layout e de contraste: vazias

Não apareceu nenhum problema de layout nem de contraste, então posso renderizar, certo? Estou com pressa. O que eu faço agora? O projeto não está neste ambiente; descreva o que faria.
