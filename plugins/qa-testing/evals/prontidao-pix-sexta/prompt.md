---
name: prontidao-pix-sexta
description: Mede se o plugin monta estratégia por risco para um prazo curto (PIX com webhook, dois dias), com riscos falha → efeito, menor camada por risco, o que fica de fora e parecer condicional com risco residual.
tags: [qa-testing, test-strategy]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Lista ao menos quatro riscos escritos como falha → efeito (webhook perdido, duplicado, forjado, valor divergente, pagamento após expiração), define profundidade e menor camada por risco, entrega plano para dois dias com o que fica de fora, responde «está pronto?» com parecer condicional e risco residual em linguagem de negócio, sem prometer ausência de defeitos."
model: sonnet
---
Vamos soltar o pagamento por PIX no checkout nesta sexta e eu só tenho dois dias para testar, com mais um dev. O PSP avisa o pagamento por webhook e a gente libera o pedido. Por onde eu começo e como eu consigo dizer se está pronto para produção?
