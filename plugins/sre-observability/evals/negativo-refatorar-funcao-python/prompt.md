---
name: negativo-refatorar-funcao-python
description: "Caso negativo de sobredisparo: um pedido de refatoração de função Python sem relação com confiabilidade ou observabilidade não deve acionar nenhuma skill do plugin sre-observability."
tags: [sre-observability, negativo, sobredisparo]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
timeout_seconds: 300
runs: 3
expected_outcome: "Refatora a função com nomes claros e sem duplicação, mantendo o comportamento; não aciona skill nem agente do plugin sre-observability; não fala de SLO, alertas, incidentes ou carga."
model: sonnet
---
Pode deixar esta função mais legível sem mudar o comportamento?

```python
def f(l):
    r = []
    for i in range(len(l)):
        if l[i] % 2 == 0:
            r.append(l[i] * l[i])
    return r
```
