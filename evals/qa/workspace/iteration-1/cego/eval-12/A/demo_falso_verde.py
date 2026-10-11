"""Prova local (sem rede, sem pytest) de que a suite original nao pega bugs.

Carrega o test_pedidos.py ORIGINAL (somente leitura), troca `requests` e
`loja.pedidos` por stubs em memoria, injeta bugs no stub e roda as funcoes de teste.
`loja.pedidos` aqui e uma implementacao FICTICIA minha, so para simular defeitos.
"""
import importlib.util
import sys
import types
from decimal import Decimal

ORIGINAL = "/Users/francisco.junior/novo projeto/brain-of-agent/evals/qa/files/test_pedidos.py"


class EstoqueInsuficiente(Exception):
    pass


def make_loja(bug=None):
    def calcular_total(itens, cupom=None):
        total = 0.0
        for i in itens:
            qtd = 1 if bug == "ignora_qtd" else i["qtd"]
            total += i["preco"] * qtd
        if cupom == "DEZ" and bug != "ignora_cupom":
            total *= 0.9
        return total

    def criar_pedido(itens):
        if bug == "sem_checagem_estoque":
            return {"id": 1}
        if bug == "quebrado":
            raise TypeError("criar_pedido() missing 1 required positional argument")
        for i in itens:
            if i["sku"] == "SEM-ESTOQUE":
                raise EstoqueInsuficiente(i["sku"])
        return {"id": 1}

    loja = types.ModuleType("loja")
    pedidos = types.ModuleType("loja.pedidos")
    pedidos.calcular_total = calcular_total
    pedidos.criar_pedido = criar_pedido
    loja.pedidos = pedidos
    return loja, pedidos


class FakeResp:
    def __init__(self, status=200, body=None):
        self.status_code = status
        self._body = body if body is not None else {"id": "p-1"}

    def json(self):
        return self._body


def load_original(bug=None, fake_requests=None):
    loja, pedidos = make_loja(bug)
    sys.modules["loja"], sys.modules["loja.pedidos"] = loja, pedidos
    sys.modules["requests"] = fake_requests or types.ModuleType("requests")
    spec = importlib.util.spec_from_file_location("test_pedidos_orig", ORIGINAL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(fn):
    try:
        fn()
        return "VERDE"
    except BaseException as e:  # noqa
        return f"VERMELHO ({type(e).__name__})"


print("== 1) Bugs injetados em loja.pedidos x testes offline da suite original ==")
print(f"{'bug injetado':<24}{'total_com_desconto':<28}{'sem_estoque':<28}{'total_varios_itens'}")
for bug in [None, "ignora_cupom", "ignora_qtd", "sem_checagem_estoque", "quebrado"]:
    m = load_original(bug)
    r = [run(m.test_total_com_desconto), run(m.test_pedido_sem_estoque), run(m.test_total_varios_itens)]
    print(f"{str(bug or '(sem bug)'):<24}{r[0]:<28}{r[1]:<28}{r[2]}")

print("\n== 2) `patch` em loja.pedidos.calcular_total tem efeito no teste? ==")
m = load_original(None)
import loja.pedidos as lp
print("nome usado pelo teste e o mesmo objeto de loja.pedidos?", m.calcular_total is lp.calcular_total)
from unittest.mock import patch
with patch("loja.pedidos.calcular_total", return_value=90.0):
    print("durante o patch, o teste ainda aponta para o original?", m.calcular_total is not lp.calcular_total)

print("\n== 3) Float em dinheiro ==")
print("10.1*3 + 0.2 =", 10.1 * 3 + 0.2, "| Decimal =", Decimal("10.1") * 3 + Decimal("0.2"))

print("\n== 4) Dependencia de ordem / ausencia de assercao (requests falso) ==")
calls = []


class FakeRequests(types.ModuleType):
    def __init__(self, post_resp, get_resp):
        super().__init__("requests")
        self._p, self._g = post_resp, get_resp

    def post(self, url, **kw):
        calls.append(("POST", url))
        return self._p

    def get(self, url, **kw):
        calls.append(("GET", url))
        return self._g


import time
time.sleep = lambda s: None  # nao esperar 5s na demonstracao
fr = FakeRequests(FakeResp(500, {"erro": "falha ao cancelar"}), FakeResp(200))
m = load_original(None, fr)
print("test_consultar_pedido isolado (pedido_id=None):", run(m.test_consultar_pedido), "->", calls[-1])
print("test_cancelar_pedido com API devolvendo 500   :", run(m.test_cancelar_pedido), "->", calls[-1])
