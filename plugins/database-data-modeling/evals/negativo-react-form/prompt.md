---
name: negativo-react-form
description: "Caso negativo: pedido de componente React de login, sem relação com banco de dados. Mede se nenhuma skill do plugin é acionada e se a resposta é sobre React."
tags: [database-data-modeling, negative]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Escreve um componente React de formulário de login com validação de e-mail e senha sem acionar nenhuma skill do plugin de banco de dados."
model: sonnet
---
Escreve pra mim um componente React de formulário de login com validação de e-mail e senha. Pode usar hooks e TypeScript, sem biblioteca de formulários.
