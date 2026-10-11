from decimal import Decimal, ROUND_HALF_UP


def calcular_desconto(subtotal: Decimal, cliente_vip: bool = False) -> Decimal:
    """Calcula o desconto progressivo de um pedido.

    Regras (definidas pelo time de Produto):
    - subtotal abaixo de R$ 100,00: sem desconto
    - de R$ 100,00 até R$ 499,99: 5%
    - a partir de R$ 500,00: 10%
    - cliente VIP ganha +2 pontos percentuais em qualquer faixa com desconto
    - o desconto nunca passa de R$ 150,00
    - o valor é arredondado para centavos, meio para cima (half-up)
    - subtotal negativo é inválido (ValueError)
    """
    if subtotal < 0:
        raise ValueError("subtotal negativo")

    if subtotal >= Decimal("500"):
        percentual = Decimal("0.10")
    elif subtotal >= Decimal("100"):
        percentual = Decimal("0.05")
    else:
        percentual = Decimal("0")

    if cliente_vip and percentual > 0:
        percentual += Decimal("0.02")

    desconto = subtotal * percentual
    desconto = min(desconto, Decimal("150"))
    return desconto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
