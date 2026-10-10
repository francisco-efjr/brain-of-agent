---
name: docstring-python-doctest
description: Mede se a docstring da função parse_duration segue o estilo Google com resumo curto, Args, Returns e só o Raises da interface, traz exemplo doctest com saída correta e marca a execução como não realizada.
tags: [technical-writing-docs, docstrings, documentar-codigo]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega docstring com resumo de uma linha até 80 caracteres, Args, Returns e Raises ValueError, doctest com 5400 para 1h30m e demais saídas corretas, sem repetir a assinatura nem documentar exceções de uso incorreto, e propõe python -m doctest marcando como não executado."
model: sonnet
---
Adicione docstring a esta função. O projeto não tem guia de estilo escrito e a gente quer que os exemplos virem teste.

```python
import re

_PADRAO = re.compile(r"^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$")


def parse_duration(texto: str) -> int:
    m = _PADRAO.match(texto.strip())
    if not texto.strip() or not m:
        raise ValueError(f"duração inválida: {texto!r}")
    horas, minutos, segundos = (int(g) if g else 0 for g in m.groups())
    return horas * 3600 + minutos * 60 + segundos
```

Ela converte textos como "1h30m", "45s" ou "2h" em segundos. Texto vazio ou fora desse formato levanta `ValueError`.
