---
name: workflow-ou-agente
description: "Mede se o plugin aplica a decisão workflow ou agente a um processo previsível (nota fiscal por e-mail para planilha), com idempotência, fila de erro e reprocesso, sem inventar cobertura de Zapier/Make."
tags: [automation-integrations, designing-workflow-automations, workflow, agente, idempotencia, positivo]
runs: 3
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
expected_outcome: "Recomenda workflow com extração por LLM em um passo, idempotência pelo ID da nota, fila de erro com reprocesso, faz no máximo uma pergunta por vez e declara lacunas de ferramenta."
---
Quero um agente que, quando chegar uma nota fiscal por e-mail, extraia o valor e lance na planilha do financeiro (Google Sheets). Chegam uns 40 e-mails por mês, a maioria com a nota em PDF anexo, de uns 15 fornecedores fixos; às vezes o fornecedor reenvia o mesmo e-mail. Hoje a Marina digita tudo à mão. Devo usar um agente com ferramentas? Já uso Make para outras coisas e tenho um Zapier parado, não tenho preferência. Se der erro no meio (PDF ilegível, planilha fora do ar), ninguém pode descobrir só no fim do mês.
