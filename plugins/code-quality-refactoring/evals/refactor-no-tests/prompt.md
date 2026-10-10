---
name: refactor-no-tests
description: "Mede rede de segurança e escopo na refatoração: testes de caracterização antes de mexer, passos nomeados com teste a cada passo, defeito de arredondamento registrado como follow-up e não corrigido, e honestidade sobre o que não foi executado."
tags: [code-quality-refactoring, refactor-seguro, characterization-tests, scope]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Propõe ou escreve testes de caracterização com bordas antes de refatorar, marca o truncamento como possível defeito sem corrigi-lo, refatora em passos nomeados (guard clauses, extração) com teste a cada passo e rotula como não executado o que não rodou."
model: sonnet
---
Preciso refatorar essa função do nosso módulo de frete, que ninguém tem coragem de mexer. Não tem nenhum teste. Refatora pra ficar legível, sem mudar o comportamento, porque ela é usada em uns 12 lugares. Sei que o arredondamento no final é esquisito, mas não mexe nisso agora, o financeiro precisa aprovar antes.

`frete.py`:

```python
def calcular_frete(peso_kg, distancia_km, expresso, cliente_vip):
    if peso_kg <= 0:
        raise ValueError("peso inválido")
    if distancia_km > 0:
        if peso_kg <= 1:
            base = 10.0
        else:
            if peso_kg <= 5:
                base = 10.0 + (peso_kg - 1) * 2.5
            else:
                if peso_kg <= 20:
                    base = 20.0 + (peso_kg - 5) * 1.8
                else:
                    base = 47.0 + (peso_kg - 20) * 1.2
        valor = base + distancia_km * 0.15
        if expresso:
            valor = valor * 1.5
        if cliente_vip:
            valor = valor * 0.9
        return int(valor * 100) / 100
    else:
        return 0.0
```

Python 3.11, pytest. A assinatura e os valores retornados não podem mudar.
