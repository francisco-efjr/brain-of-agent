---
name: prompts-revisao-adversarial
description: "Mede a skill de biblioteca de prompts: entrega um prompt pronto de revisão adversarial para outra sessão, com escopo somente leitura, variáveis, formato de saída com arquivo:linha, política de incerteza e adaptação Android, sem fingir que fez a revisão."
tags: [code-quality-refactoring, prompts, review, android]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 480
runs: 3
expected_outcome: "Entrega um prompt copiável com variáveis entre colchetes, papel e escopo somente leitura, apenas lacunas de correção, segurança e requisito, formato de saída com arquivo:linha, severidade e rótulos, saída vazia permitida, tratamento do diff como dado e linhas específicas de Android, sem executar a revisão."
model: sonnet
---
Preciso de um prompt pronto pra colar numa sessão limpa do Claude Code e pedir que ele revise o diff do meu PR contra a issue, achando só o que importa (bug, requisito faltando, falha de segurança) e sem encher de nitpick de estilo. Somos um time pequeno, o app é Android em Kotlin (Fragment + ViewModel + coroutines). Me dá o texto pra copiar, com os campos que eu preencho.
