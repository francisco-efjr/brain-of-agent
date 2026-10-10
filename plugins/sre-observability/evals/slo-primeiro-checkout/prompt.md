---
name: slo-primeiro-checkout
description: "Mede o primeiro SLO de uma jornada de checkout, verificando recusa de 100 por cento e de tempo médio, SLIs em linguagem de usuário, linha de base dos logs do nginx em janela fixa, consequência SLO versus SLA, conta do error budget e metas sem dados marcadas como Suposição."
tags: [sre-observability, slo-design, slo]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Recusa com motivo a meta de 100 por cento e o tempo médio como SLI; propõe no máximo 5 SLIs em linguagem de usuário com percentis e dois limiares de latência; manda medir a linha de base nos logs do nginx numa janela fixa e arredondar para baixo, sem inventar valores medidos; declara consequência (SLO ou SLA); mostra a conta do budget (99,9 por cento em 30 dias = 43,2 min); entrega política com dono, aprovadores e escalonamento; rotula metas sem dados como Suposição."
model: sonnet
---
Somos uma loja virtual pequena. A jornada mais importante é criar pedido: `POST /pedidos` (API em Node atrás de um nginx). Nunca tivemos SLO. Tenho os logs de acesso do nginx do último mês, com o campo `request_time` em cada linha, mas eles não estão nesta máquina agora. O pessoal de produto quer "disponibilidade de 100%" e "tempo médio de resposta abaixo de 200 ms". Me ajuda a definir o primeiro SLO e a política de error budget? Quem decide é produto, junto com o dev líder e a pessoa de infra.
