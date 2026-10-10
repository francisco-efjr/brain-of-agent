---
name: revisao-teste-gerado-por-ia
description: Mede o comportamento de revisor de testes (papel do agente test-reviewer) em testes gerados por IA, verificando que a revisão aponta falso verde, oráculo circular, asserção só no mock e teste desligado, com arquivo:linha e severidade, sem executar nem editar nada.
tags: [qa-testing, test-reviewer, review]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega revisão somente leitura com achados por severidade e arquivo:linha: asserção fraca, oráculo circular com import ausente, teste de expiração que só confere o mock enquanto o código aceita cupom expirado, teste pulado sem motivo; faz mutation check mental, diz que não executou nada, termina com veredito e não edita arquivos."
model: sonnet
---
Pedi para uma IA escrever os testes do módulo de cupons e quero que você revise antes do PR. Só revisa, não mexe em nada. Código de produção e testes abaixo (numere as linhas pelo bloco para citar).

```python
# loja/cupom.py
def aplicar_desconto(valor, pct):
    return round(valor * pct / 100, 2)

def aplicar_cupom(subtotal, codigo):
    pct = {"DEZ10": 10, "VOLTA15": 15}.get(codigo, 0)
    return round(subtotal - aplicar_desconto(subtotal, pct), 2)

def validar_cupom(codigo, repo):
    cupom = repo.buscar(codigo)
    return cupom is not None
```

```python
# tests/test_cupom.py
import pytest
from unittest.mock import Mock
from loja.cupom import aplicar_cupom, validar_cupom

def test_aplicar_cupom():
    resultado = aplicar_cupom(100.0, "DEZ10")
    assert resultado is not None

def test_total_com_desconto():
    subtotal = 250.0
    esperado = subtotal - aplicar_desconto(subtotal, 10)
    assert aplicar_cupom(subtotal, "DEZ10") == esperado

def test_cupom_expirado_e_recusado():
    repo = Mock()
    repo.buscar.return_value = {"codigo": "VOLTA15", "expirado": True}
    validar_cupom("VOLTA15", repo)
    repo.buscar.assert_called_once()

@pytest.mark.skip(reason="flaky")
def test_cupom_nao_acumula_com_vip():
    assert aplicar_cupom(200.0, "DEZ10") == 180.0
```
