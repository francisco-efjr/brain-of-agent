Escrevi os testes (`test_desconto.py`, 53 casos parametrizados) e eles já acharam **dois defeitos na própria função**: com a `desconto.py` atual, 5 dos 53 casos falham. Isso é esperado: o teste segue a regra escrita na docstring, e o código não segue.

## Defeitos encontrados

| # | O que a regra diz | O que o código faz | Exemplo | Esperado | Obtido |
| --- | --- | --- | --- | --- | --- |
| 1 | "a partir de R$ 500,00: 10%" | usa `subtotal > 500` em vez de `>= 500` | subtotal R$ 500,00, não VIP | R$ 50,00 | R$ 25,00 |
| 1 | idem (VIP) | idem | subtotal R$ 500,00, VIP | R$ 60,00 | R$ 35,00 |
| 2 | VIP ganha +2 pontos "em qualquer faixa **com desconto**" | soma os 2 pontos até na faixa abaixo de R$ 100 (0% + 2%) | subtotal R$ 99,99, VIP | R$ 0,00 | R$ 2,00 |
| 2 | idem | idem | subtotal R$ 50,00, VIP | R$ 0,00 | R$ 1,00 |

O defeito 1 é o clássico `>` no lugar de `>=` e dá prejuízo direto: quem compra exatamente R$ 500,00 perde metade do desconto. O defeito 2 dá desconto que ninguém prometeu.

**Preciso da sua confirmação no defeito 2.** Li "faixa com desconto" como "a faixa abaixo de R$ 100 não conta, então VIP ali continua sem nada". Se o Produto quis dizer outra coisa (VIP sempre ganha 2%, mesmo em pedido pequeno), é a docstring que está errada, e esses testes (`test_vip_abaixo_de_100_continua_sem_desconto` e a varredura no fim) mudam de expectativa. O defeito 1 não tem essa dúvida: o texto é explícito.

Correção mínima (duas linhas), que deixa os 53 casos verdes:

```diff
@@ -16,14 +16,14 @@
     if subtotal < 0:
         raise ValueError("subtotal negativo")
 
-    if subtotal > Decimal("500"):
+    if subtotal >= Decimal("500"):
         percentual = Decimal("0.10")
     elif subtotal >= Decimal("100"):
         percentual = Decimal("0.05")
     else:
         percentual = Decimal("0")
 
-    if cliente_vip:
+    if cliente_vip and percentual > 0:
         percentual += Decimal("0.02")
 
     desconto = subtotal * percentual
```

## Como rodar

Salve como `test_desconto.py` na mesma pasta de `desconto.py` e rode:

```
pytest -v test_desconto.py
```

## O que os testes cobrem

- **Faixas e limites** (R$ 0,00, 0,01, 99,99 / 100,00, 100,01, 499,99 / 500,00, 500,01), com e sem VIP. Os limites das faixas são os de maior risco, e o defeito 1 estava exatamente num deles.
- **VIP**: +2 pontos nas faixas com desconto; nenhum desconto abaixo de R$ 100.
- **Teto de R$ 150,00**: abaixo, exatamente no teto e acima, para VIP e não VIP. Os valores "acima" foram escolhidos para o desconto sem teto dar bem mais que R$ 150 (R$ 1.600 daria R$ 160); em R$ 1.500,01 o teto e o arredondamento dão o mesmo resultado, então ali o teste não pegaria um teto removido.
- **Arredondamento half-up**: casos que caem exatamente em meio centavo (R$ 100,10 gera 5,005 e deve virar 5,01; o `ROUND_HALF_EVEN` do Decimal daria 5,00). Também há casos que arredondam para baixo, para pegar arredondamento "sempre para cima".
- **Tipo do retorno**: `Decimal` com 2 casas. `Decimal("5.0") == Decimal("5.00")` é verdadeiro, então só comparar o valor não pega um `quantize` removido.
- **Subtotal negativo**: `ValueError`, com e sem VIP. Zero é válido e não lança.
- **Varredura de invariantes** (R$ 0 a R$ 3.000, passo de R$ 0,50): desconto sempre entre 0 e 150, VIP nunca recebe menos que não VIP, e nenhum dos dois recebe desconto abaixo de R$ 100. Serve de rede para pontos que escolhi à mão.

Os valores esperados são **calculados à mão a partir da docstring**, com a conta no comentário. Nenhum chama `calcular_desconto` para montar o esperado, porque isso copiaria os defeitos para dentro do teste (você veria tudo verde com o bug 1 e o bug 2 presentes). Os `Decimal` são sempre criados de string, nunca de float.

## O que foi verificado

- **Executei**, mas não com o pytest real: ele não está instalado aqui e não instalei pacotes. Rodei o arquivo com um runner mínimo meu que imita só `parametrize`, `param` e `raises`. Resultado: com a `desconto.py` atual, 48 passam e 5 falham (os casos da tabela acima mais a varredura); com a correção, 53 passam. Rode uma vez com o pytest de verdade antes de confiar. Não espero diferença, mas não pude confirmar.
- **Mutação manual**: apliquei 13 alterações plausíveis na versão corrigida (trocar `>=` por `>` nos dois limites, mudar cada percentual, remover ou mudar o teto, trocar half-up por half-even e por truncamento, aceitar subtotal zero como inválido, inverter o padrão de `cliente_vip`, entre outras). Os testes pegaram as 13.

## Fica de fora (risco que sobra)

- **Subtotal que não seja `Decimal`**: com `float`, a função lança `TypeError` ao multiplicar. A regra só fala de dinheiro, não de tipo aceito. Se a chamada vem de fora (API, planilha), vale decidir o contrato e testar.
- **Subtotal com mais de 2 casas** (ex.: R$ 499,995): a regra não diz em que faixa cai. Hoje cai nos 5%. Pergunta para o Produto, sem teste por enquanto.
- **`cliente_vip` que não seja bool** (`None`, `"false"`): tratado como verdadeiro/falso pelo Python. Não testei.
- Teste de integração com o carrinho, o frete ou o cupom: a função só calcula; quem a chama não foi coberto.

## Código completo

```python
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
```
