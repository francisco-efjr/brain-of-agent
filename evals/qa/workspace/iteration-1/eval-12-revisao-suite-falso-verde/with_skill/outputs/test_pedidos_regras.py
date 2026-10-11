"""Regras de pedido (cálculo de total, cupom, estoque): sem rede, sem ordem, sem estado.

Rodar:  pytest test_pedidos_regras.py -q

Substitui test_total_com_desconto, test_total_varios_itens e test_pedido_sem_estoque.
Pontos marcados com AJUSTE dependem de uma decisão de negócio ou de um nome que o
arquivo original não revela: confirme antes de confiar no resultado.
"""
import pytest

from loja.pedidos import calcular_total, criar_pedido

# AJUSTE: troque pela exceção de domínio real (ex.: EstoqueInsuficiente).
# Com Exception genérica o teste ainda falha se NADA for lançado, mas aceita
# qualquer erro (TypeError por assinatura mudada, por exemplo).
ErroSemEstoque = Exception
ErroQuantidadeInvalida = Exception  # AJUSTE: idem (ex.: ValueError)


def item(preco, qtd=1):
    return {"preco": preco, "qtd": qtd}


def assert_valor(total, esperado):
    """Dinheiro: não tolera 1 centavo de erro e exige no máximo 2 casas."""
    assert total == pytest.approx(esperado, abs=0.005)
    # AJUSTE: premissa de que o total sai arredondado em centavos. Se o projeto
    # usa Decimal/centavos inteiros, adapte (e prefira isso a float).
    assert round(total, 2) == total, f"total com mais de 2 casas decimais: {total!r}"


def test_total_soma_preco_vezes_quantidade_de_varios_itens():
    # Oráculo calculado à mão, independente do código: 10,10 x 3 = 30,30; + 0,20 = 30,50
    assert_valor(calcular_total([item(10.10, 3), item(0.20)]), 30.50)


@pytest.mark.parametrize(
    "itens, esperado",
    [
        ([item(100.0)], 90.0),           # exemplo do teste original
        ([item(50.0, 3)], 135.0),        # 150,00 - 10%: o desconto vale sobre o total, não só o 1º item
        ([item(33.33, 3)], 89.99),       # 99,99 - 10% = 89,991 -> arredonda para 89,99
        ([item(60.0), item(40.0)], 90.0),  # vários itens: desconto sobre a soma (100,00)
    ],
)
def test_cupom_dez_aplica_10_por_cento_sobre_o_total(itens, esperado):
    assert_valor(calcular_total(itens, cupom="DEZ"), esperado)


def test_sem_cupom_o_total_nao_tem_desconto():
    assert_valor(calcular_total([item(100.0)]), 100.0)


@pytest.mark.parametrize("qtd", [0, -1])
def test_quantidade_zero_ou_negativa_e_recusada(qtd):
    # AJUSTE: premissa de que quantidade <= 0 é erro (negativa geraria total negativo).
    with pytest.raises(ErroQuantidadeInvalida):
        calcular_total([item(10.0, qtd)])


def test_pedido_sem_estoque_e_recusado():
    # pytest.raises falha se NADA for lançado (o try/except original nunca falhava).
    with pytest.raises(ErroSemEstoque):
        criar_pedido([{"sku": "SEM-ESTOQUE", "qtd": 1}])
    # AJUSTE: acrescente a verificação do efeito (nenhum pedido criado e estoque
    # inalterado), usando a consulta de estoque/pedidos que o projeto já tem.
