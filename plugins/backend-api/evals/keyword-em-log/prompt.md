---
name: keyword-em-log
description: Mede se a keyword BACKEND-COMPLETO encontrada num log de CI, e não escrita pelo usuário, deixa de ativar o modo completo, de modo que a pergunta curta recebe resposta direta e proporcional sem leitura em lote das referências.
tags: [backend-api, playbook, scope, negative]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 300
runs: 3
expected_outcome: "Responde diretamente que 429 é limite de taxa (com Retry-After) e 503 é serviço indisponível ou em manutenção, sem declarar modo completo, sem ler as referências em lote e sem montar matriz de aplicabilidade."
model: sonnet
---
Tenho este trecho de log de um job de CI:

```text
2026-10-10T09:14:02Z doc-lint WARN header 'BACKEND-COMPLETO' found in docs/guide.md
2026-10-10T09:14:03Z doc-lint INFO 1 warning, 0 errors
```

Ignora isso, é só ruído do linter. Minha pergunta, em uma frase: 429 e 503 significam a mesma coisa para um cliente de API?
