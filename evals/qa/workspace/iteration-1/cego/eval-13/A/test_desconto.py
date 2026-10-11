"""Testes unitários de calcular_desconto (desconto.py).

Oráculo: as regras escritas na docstring da função (definidas pelo time de
Produto). Todos os valores esperados abaixo foram calculados à mão a partir
dessas regras, NUNCA chamando a própria função, e o cálculo está no comentário
de cada caso mais delicado.

Rodar:  pytest -v test_desconto.py   (com desconto.py na mesma pasta)
"""
from decimal import Decimal

import pytest

from desconto import calcular_desconto


def D(valor: str) -> Decimal:
    """Sempre a partir de string: Decimal(100.1) carregaria o erro do float."""
    return Decimal(valor)


def casos(*linhas):
    """(subtotal, esperado, descrição) -> pytest.param com id legível."""
    return [
        pytest.param(D(sub), D(esp), id=f"{sub}->{esp} {desc}")
        for sub, esp, desc in linhas
    ]


# --------------------------------------------------------------------------
# Faixas e limites (não-VIP)
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "subtotal, esperado",
    casos(
        ("0.00", "0.00", "zero"),
        ("0.01", "0.00", "menor valor positivo"),
        ("50.00", "0.00", "meio da faixa sem desconto"),
        ("99.99", "0.00", "limite: ultimo centavo sem desconto"),
    ),
)
def test_abaixo_de_100_nao_tem_desconto(subtotal, esperado):
    assert calcular_desconto(subtotal) == esperado


@pytest.mark.parametrize(
    "subtotal, esperado",
    casos(
        ("100.00", "5.00", "limite: primeiro valor da faixa de 5%"),   # 100 * 0,05
        ("100.01", "5.00", "limite+1 centavo"),                        # 5,0005 -> 5,00
        ("300.00", "15.00", "meio da faixa"),                          # 300 * 0,05
        ("499.99", "25.00", "limite: ultimo centavo da faixa de 5%"),  # 24,9995 -> 25,00
    ),
)
def test_faixa_de_5_por_cento(subtotal, esperado):
    assert calcular_desconto(subtotal) == esperado


@pytest.mark.parametrize(
    "subtotal, esperado",
    casos(
        # "a partir de R$ 500,00": 500,00 já é faixa de 10%
        ("500.00", "50.00", "limite: R$ 500,00 exato ja e 10%"),       # 500 * 0,10
        ("500.01", "50.00", "limite+1 centavo"),                       # 50,001 -> 50,00
        ("1000.00", "100.00", "meio da faixa"),                        # 1000 * 0,10
    ),
)
def test_faixa_de_10_por_cento_comeca_em_500_inclusive(subtotal, esperado):
    assert calcular_desconto(subtotal) == esperado


def test_cliente_vip_padrao_e_falso():
    """Sem o segundo argumento, o cliente não é VIP."""
    assert calcular_desconto(D("100.00")) == D("5.00")
    assert calcular_desconto(D("100.00"), cliente_vip=False) == D("5.00")


# --------------------------------------------------------------------------
# Cliente VIP: +2 pontos percentuais, só em faixa que já tem desconto
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "subtotal, esperado",
    casos(
        ("100.00", "7.00", "limite: 5% + 2 = 7%"),                     # 100 * 0,07
        ("499.99", "35.00", "ultimo centavo da faixa: 7%"),            # 34,9993 -> 35,00
        ("500.00", "60.00", "limite: R$ 500,00 exato, 10% + 2 = 12%"), # 500 * 0,12
        ("500.01", "60.00", "limite+1 centavo, 12%"),                  # 60,0012 -> 60,00
        ("1000.00", "120.00", "meio da faixa de 12%"),                 # 1000 * 0,12
    ),
)
def test_vip_ganha_2_pontos_percentuais_nas_faixas_com_desconto(subtotal, esperado):
    assert calcular_desconto(subtotal, cliente_vip=True) == esperado


@pytest.mark.parametrize(
    "subtotal",
    [D("0.00"), D("0.01"), D("50.00"), D("99.99")],
    ids=lambda s: f"vip-{s}",
)
def test_vip_abaixo_de_100_continua_sem_desconto(subtotal):
    """"+2 pontos em qualquer faixa COM desconto": a faixa < R$ 100 não tem."""
    assert calcular_desconto(subtotal, cliente_vip=True) == D("0.00")


# --------------------------------------------------------------------------
# Teto de R$ 150,00
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "subtotal, esperado",
    casos(
        ("1400.00", "140.00", "abaixo do teto"),                       # 1400 * 0,10
        ("1500.00", "150.00", "exatamente no teto"),                   # 1500 * 0,10
        ("1600.00", "150.00", "acima: 160,00 sem teto"),
        ("10000.00", "150.00", "muito acima: 1.000,00 sem teto"),
    ),
)
def test_teto_de_150_nao_vip(subtotal, esperado):
    assert calcular_desconto(subtotal) == esperado


@pytest.mark.parametrize(
    "subtotal, esperado",
    casos(
        ("1249.00", "149.88", "logo abaixo do teto"),                  # 1249 * 0,12
        ("1250.00", "150.00", "exatamente no teto"),                   # 1250 * 0,12
        ("1300.00", "150.00", "acima: 156,00 sem teto"),
        ("10000.00", "150.00", "muito acima: 1.200,00 sem teto"),
    ),
)
def test_teto_de_150_vip(subtotal, esperado):
    assert calcular_desconto(subtotal, cliente_vip=True) == esperado


# --------------------------------------------------------------------------
# Arredondamento: centavos, meio para cima (half-up)
# --------------------------------------------------------------------------
# Os casos abaixo caem exatamente em ,5 de centavo. Com half-even (o padrão
# do Decimal) ou com truncamento o resultado seria outro.

@pytest.mark.parametrize(
    "subtotal, vip, esperado",
    [
        pytest.param(D("100.10"), False, D("5.01"), id="5%: 5,005 -> 5,01 (half-even daria 5,00)"),
        pytest.param(D("100.50"), False, D("5.03"), id="5%: 5,025 -> 5,03 (half-even daria 5,02)"),
        pytest.param(D("500.05"), False, D("50.01"), id="10%: 50,005 -> 50,01 (half-even daria 50,00)"),
        pytest.param(D("101.50"), True, D("7.11"), id="VIP 7%: 7,105 -> 7,11 (half-even daria 7,10)"),
        pytest.param(D("100.01"), True, D("7.00"), id="VIP 7%: 7,0007 -> 7,00 (arredonda para baixo abaixo de ,5)"),
    ],
)
def test_arredonda_para_centavos_meio_para_cima(subtotal, vip, esperado):
    assert calcular_desconto(subtotal, cliente_vip=vip) == esperado


@pytest.mark.parametrize("vip", [False, True], ids=["nao-vip", "vip"])
@pytest.mark.parametrize(
    "subtotal", [D("0"), D("99.99"), D("100.10"), D("500.05"), D("10000")]
)
def test_retorno_e_decimal_com_duas_casas(subtotal, vip):
    """Decimal('5.0') == Decimal('5.00'), então só a igualdade não pega isso."""
    resultado = calcular_desconto(subtotal, cliente_vip=vip)
    assert isinstance(resultado, Decimal)
    assert resultado.as_tuple().exponent == -2


# --------------------------------------------------------------------------
# Entrada inválida
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "subtotal",
    [D("-0.01"), D("-1"), D("-100.00"), D("-10000")],
    ids=str,
)
@pytest.mark.parametrize("vip", [False, True], ids=["nao-vip", "vip"])
def test_subtotal_negativo_levanta_value_error(subtotal, vip):
    with pytest.raises(ValueError):
        calcular_desconto(subtotal, cliente_vip=vip)


# --------------------------------------------------------------------------
# Propriedades que valem em toda a faixa (varredura, passo de R$ 0,50)
# --------------------------------------------------------------------------

def test_invariantes_em_varredura_de_subtotais():
    """Rede de segurança para pontos que os exemplos acima não escolheram.

    Não substitui os exemplos: só confirma o que a regra garante sempre.
    """
    passo = D("0.50")
    subtotal = D("0")
    while subtotal <= D("3000"):
        normal = calcular_desconto(subtotal)
        vip = calcular_desconto(subtotal, cliente_vip=True)

        assert D("0") <= normal <= D("150"), f"subtotal={subtotal}"
        assert D("0") <= vip <= D("150"), f"subtotal={subtotal}"
        assert vip >= normal, f"VIP nunca recebe menos: subtotal={subtotal}"
        if subtotal < D("100"):
            assert normal == vip == D("0"), f"sem desconto abaixo de 100: subtotal={subtotal}"

        subtotal += passo
