---
name: lighthouse-inp-e-campo
description: "Mede performance web, verificando que o agente diz que o Lighthouse em modo de navegação não mede INP (usa TBT como proxy), pede dado de campo no p75 por dispositivo, cita as metas boas de LCP, INP e CLS, não atribui os limiares ruins a fonte inexistente, não inventa medições e indica a fronteira com o plugin web-frontend."
tags: [sre-observability, performance-engineering, web-vitals, campo]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Diz que o Lighthouse em modo de navegação não mede INP e que o TBT é indicador de laboratório (timespan só mede interações roteirizadas); pede dados de campo (RUM ou CrUX) no p75 separados por celular e desktop; cita metas boas LCP até 2,5 s, INP até 200 ms, CLS até 0,1; entrega plano de ações para LCP, INP e CLS com verificação em campo; cita limiares ruins, se citar, corretamente; não inventa medição nem promete ganho; aponta a fronteira com web-frontend."
model: sonnet
---
O Lighthouse deu 62 na nossa home, com o TBT alto. O time diz que o INP é 480 ms "segundo o Lighthouse" e que o LCP de laboratório é 3,1 s. Faz um plano de otimização pra gente.
