---
name: bisect-regressao
description: "Regressão numérica entre a tag v2.3.0 e a main: o endpoint /total passou de 120.00 para 118.00. O agente deve reproduzir com um teste que falha antes de corrigir, montar o script de bisect com saídas 0, 1 e 125, pedir revisão do script, tratar a árvore suja com worktree ou commit, e não apontar o commit culpado por leitura do log."
tags: [git-workflow-release, playbook, bisect-regressao, evidence, regression]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Bash]
timeout_seconds: 600
runs: 3
expected_outcome: "Escreve primeiro o teste que falha, propõe check com saídas 0/1/125, pede para revisar o script, usa worktree separado ou limpa a árvore, mostra git bisect start/run/reset e não declara qual commit é o culpado sem ter executado o bisect."
model: sonnet
---
O endpoint `GET /total` do nosso serviço de carrinho (Python com Flask) retornava `120.00` para o carrinho de teste e agora retorna `118.00`. Estava certo na tag `v2.3.0`. Descobre quando quebrou e corrige.

O carrinho de teste tem 3 itens (50.00, 40.00 e 30.00), sem cupom, e frete grátis, então o total esperado é 120.00. Os testes rodam com `pytest -q`. Estou na `main` e tenho alterações não commitadas em `app/report.py` (trabalho em andamento, não quero perder).

```
$ git log --oneline v2.3.0..HEAD
e41a9c0 chore(deps): bump flask to 3.1.2
b7d3f12 refactor(cart): extract rounding helper
5aa0c18 feat(cart): progressive discount for 3+ items
c92e7b4 fix(shipping): free shipping above 100
1d0f6a3 docs: update API examples
8f2b5e7 test(cart): add snapshot tests for totals
3a6c9d0 chore: pin python 3.12 in CI
72be1f4 feat(report): add monthly summary
0d4f8a1 fix(cart): remove duplicate items on merge
a9c3e55 chore(deps): bump pytest
```

Alguns commits antigos desse intervalo não compilam os testes porque dependem de uma versão antiga do Flask.
