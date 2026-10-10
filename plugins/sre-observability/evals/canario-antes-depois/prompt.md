---
name: canario-antes-depois
description: "Mede a validação de um plano de canário com comparação antes e depois, verificando recomendação de controle concorrente, poucas métricas ligadas aos SLIs sem CPU, séries separadas de canário e controle, baseline anterior e imutável, critérios de rollback prévios, alerta após duas checagens e decisão humana sobre rollback."
tags: [sre-observability, release-health, playbook, canario]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta que comparar hoje com ontem no mesmo horário confunde padrão de tráfego com efeito da versão; recomenda controle concorrente; poucas métricas (no máximo cerca de 12), de preferência SLIs, sem CPU como critério; separa canário e controle (20% de erro numa fatia de 5% aparece como cerca de 1% agregado); baseline capturado antes e não sobrescrito; critérios de rollback definidos antes; alerta só após 2 checagens seguidas; rollback é decisão humana; menciona o comando /sre-observability:release-health."
model: sonnet
---
Vou liberar a v5.1 do nosso serviço de busca para 5% do tráfego. Meu plano é comparar a taxa de erro e a CPU de hoje com as de ontem no mesmo horário; se piorar mais de 10%, eu reverto na hora. Valida esse plano e monta o checklist do canário.
