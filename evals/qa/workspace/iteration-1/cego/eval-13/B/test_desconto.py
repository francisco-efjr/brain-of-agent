"""Testes unitários de calcular_desconto.

Os testes seguem a REGRA DE NEGÓCIO descrita na docstring da função, não o
comportamento atual do código. Quando um teste falha, o suspeito é o código.
"""
from decimal import Decimal

import pytest

from desconto import calcular_desconto

D = Decimal


# ---------------------------------------------------------------------------
# Faixas e limites (cliente comum)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "subtotal",
    ["0", "0.01", "50.00", "99.98", "99.99"],
)
def test_abaixo_de_100_nao_tem_desconto(subtotal):
    assert calcular_desconto(D(subtotal)) == D("0.00")


@pytest.mark.parametrize(
    "subtotal, esperado",
    [
        ("100.00", "5.00"),    # limite inferior da faixa de 5% (inclusivo)
        ("100.01", "5.00"),    # 5.0005 -> 5.00
        ("250.00", "12.50"),   # meio da faixa
        ("499.98", "25.00"),   # 24.999  -> 25.00
        ("499.99", "25.00"),   # limite superior da faixa de 5% (24.9995 -> 25.00)
    ],
)
def test_faixa_de_5_por_cento(subtotal, esperado):
    assert calcular_desconto(D(subtotal)) == D(esperado)


@pytest.mark.parametrize(
    "subtotal, esperado",
    [
        ("500.00", "50.00"),    # "a partir de R$ 500,00": limite inclusivo
        ("500.01", "50.00"),    # 50.001 -> 50.00
        ("501.00", "50.10"),
        ("1000.00", "100.00"),
    ],
)
def test_faixa_de_10_por_cento(subtotal, esperado):
    assert calcular_desconto(D(subtotal)) == D(esperado)


def test_salto_entre_faixas_no_limite_de_500():
    """499,99 cai nos 5% e 500,00 nos 10%: o desconto tem que subir no limite."""
    assert calcular_desconto(D("500.00")) > calcular_desconto(D("499.99"))


# ---------------------------------------------------------------------------
# Cliente VIP (+2 pontos percentuais, só em faixa que já tem desconto)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("subtotal", ["0", "0.01", "50.00", "99.99"])
def test_vip_abaixo_de_100_continua_sem_desconto(subtotal):
    # "+2 pontos em qualquer faixa COM desconto": a faixa sem desconto não ganha nada
    assert calcular_desconto(D(subtotal), cliente_vip=True) == D("0.00")


@pytest.mark.parametrize(
    "subtotal, esperado",
    [
        ("100.00", "7.00"),    # 5% + 2 = 7%
        ("200.00", "14.00"),
        ("499.99", "35.00"),   # limite superior da faixa: 34.9993 -> 35.00
    ],
)
def test_vip_faixa_de_5_por_cento_vira_7(subtotal, esperado):
    assert calcular_desconto(D(subtotal), cliente_vip=True) == D(esperado)


@pytest.mark.parametrize(
    "subtotal, esperado",
    [
        ("500.00", "60.00"),    # 10% + 2 = 12%, limite inclusivo
        ("500.01", "60.00"),    # 60.0012 -> 60.00
        ("1000.00", "120.00"),
    ],
)
def test_vip_faixa_de_10_por_cento_vira_12(subtotal, esperado):
    assert calcular_desconto(D(subtotal), cliente_vip=True) == D(esperado)


def test_vip_sempre_recebe_pelo_menos_o_mesmo_desconto_do_cliente_comum():
    for subtotal in ["0", "99.99", "100.00", "499.99", "500.00", "5000.00"]:
        s = D(subtotal)
        assert calcular_desconto(s, cliente_vip=True) >= calcular_desconto(s)


def test_cliente_vip_e_false_por_padrao():
    s = D("200.00")
    assert calcular_desconto(s) == calcular_desconto(s, cliente_vip=False)
    assert calcular_desconto(s) == D("10.00")


def test_cliente_vip_aceita_argumento_posicional():
    assert calcular_desconto(D("200.00"), True) == D("14.00")


# ---------------------------------------------------------------------------
# Teto de R$ 150,00
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "subtotal, vip, esperado",
    [
        ("1499.00", False, "149.90"),    # logo abaixo do teto
        ("1500.00", False, "150.00"),    # 10% = 150 exato (limite do teto)
        ("1500.01", False, "150.00"),    # 150.001 -> continua 150.00
        ("10000.00", False, "150.00"),   # bem acima: 1000 sem teto
        ("1200.00", True, "144.00"),     # 12% = 144, abaixo do teto
        ("1250.00", True, "150.00"),     # 12% = 150 exato
        ("1250.01", True, "150.00"),     # 150.0012 -> 150.00
        ("100000.00", True, "150.00"),
    ],
)
def test_teto_de_150_reais(subtotal, vip, esperado):
    assert calcular_desconto(D(subtotal), cliente_vip=vip) == D(esperado)


@pytest.mark.parametrize("vip", [False, True])
def test_desconto_nunca_passa_de_150(vip):
    for subtotal in ["500.00", "1500.00", "1500.01", "99999.99", "1000000"]:
        assert calcular_desconto(D(subtotal), cliente_vip=vip) <= D("150.00")


# ---------------------------------------------------------------------------
# Arredondamento half-up para centavos
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "subtotal, esperado",
    [
        ("100.10", "5.01"),   # 5.005  -> 5.01 (half-even daria 5.00)
        ("100.30", "5.02"),   # 5.015  -> 5.02
        ("100.50", "5.03"),   # 5.025  -> 5.03 (half-even daria 5.02)
        ("100.09", "5.00"),   # 5.0045 -> 5.00 (abaixo da metade: para baixo)
        ("100.11", "5.01"),   # 5.0055 -> 5.01 (acima da metade: para cima)
    ],
)
def test_arredondamento_half_up_faixa_5(subtotal, esperado):
    assert calcular_desconto(D(subtotal)) == D(esperado)


@pytest.mark.parametrize(
    "subtotal, vip, esperado",
    [
        ("500.05", False, "50.01"),   # 50.005 -> 50.01
        ("500.04", False, "50.00"),   # 50.004 -> 50.00
        ("125.25", True, "8.77"),     # 8.7675 -> 8.77
        ("100.25", True, "7.02"),     # 7.0175 -> 7.02
        ("100.07", True, "7.00"),     # 7.0049 -> 7.00
    ],
)
def test_arredondamento_half_up_outros_casos(subtotal, vip, esperado):
    assert calcular_desconto(D(subtotal), cliente_vip=vip) == D(esperado)


def test_arredondamento_ocorre_antes_do_teto_nao_estoura_150():
    # 12% de 1249,99 = 149.9988 -> 150.00 (arredonda para o teto, não passa dele)
    assert calcular_desconto(D("1249.99"), cliente_vip=True) == D("150.00")


# ---------------------------------------------------------------------------
# Formato do resultado
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "subtotal, vip",
    [("0", False), ("99.99", True), ("100", False), ("333.33", True), ("20000", True)],
)
def test_resultado_e_decimal_com_duas_casas(subtotal, vip):
    resultado = calcular_desconto(D(subtotal), cliente_vip=vip)
    assert isinstance(resultado, Decimal)
    assert resultado.as_tuple().exponent == -2


# ---------------------------------------------------------------------------
# Entrada inválida
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("subtotal", ["-0.01", "-1", "-100.00", "-99999"])
@pytest.mark.parametrize("vip", [False, True])
def test_subtotal_negativo_levanta_value_error(subtotal, vip):
    with pytest.raises(ValueError, match="negativo"):
        calcular_desconto(D(subtotal), cliente_vip=vip)


def test_subtotal_zero_e_valido():
    assert calcular_desconto(D("0")) == D("0.00")
    assert calcular_desconto(D("0"), cliente_vip=True) == D("0.00")
