---
name: prompt-pronto-controle-de-acesso
description: Mede se a biblioteca de prompts entrega um prompt pronto de revisão de controle de acesso com OpenZeppelin, somente leitura, com variáveis, dados tratados como não confiáveis, formato de saída com arquivo e linha e política de incerteza, sem fingir a revisão nem alegar eficácia medida.
tags: [blockchain-web3, prompts, access-control]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Entrega um prompt pronto em bloco de código para revisar controle de acesso com OpenZeppelin AccessControl, com variáveis entre colchetes, instruções somente leitura, conteúdo de contrato tratado como dado, formato de saída com severidade e arquivo e linha e política de incerteza, e orienta rodar em sessão nova, sem executar a revisão e sem alegar eficácia medida."
model: sonnet
---
Me passa um prompt pronto pra eu colar numa sessão nova do Claude Code e revisar o controle de acesso (OpenZeppelin AccessControl) dos contratos do meu protocolo. Não precisa revisar nada agora, só quero o prompt.
