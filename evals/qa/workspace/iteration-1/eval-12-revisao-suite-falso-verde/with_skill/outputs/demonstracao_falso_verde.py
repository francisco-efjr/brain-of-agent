#!/usr/bin/env python3
"""Mostra, só com a biblioteca padrão, quais testes do arquivo original passam com o
código QUEBRADO, e que a versão corrigida (test_pedidos_regras.py) os pega.

Como funciona: não há `loja`, `requests` nem `pytest` neste ambiente (e rede está
fora de questão), então o script injeta substitutos (stubs) em sys.modules, carrega
o arquivo ORIGINAL sem modificá-lo e chama as funções de teste reais contra
implementações de `calcular_total`/`criar_pedido` corretas e com um defeito
plantado ("mutantes"). Os stubs são ficção minha, não o código da loja: provam o
que os testes DETECTAM, não que a loja tem esse defeito.

Uso:  python3 demonstracao_falso_verde.py [caminho/test_pedidos.py]
"""
import contextlib
import os
import sys
import time
import types
from unittest import mock

sys.dont_write_bytecode = True  # não deixar __pycache__ ao lado do arquivo original

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGINAL = sys.argv[1] if len(sys.argv) > 1 else (
    "/Users/francisco.junior/novo projeto/brain-of-agent/evals/qa/files/test_pedidos.py")
CORRIGIDO = os.path.join(AQUI, "test_pedidos_regras.py")


class EstoqueInsuficiente(Exception):
    pass


# ---------------------------------------------------------------- implementações
def _validar(itens):
    for i in itens:
        if i["qtd"] <= 0:
            raise ValueError("quantidade inválida")


def total_certo(itens, cupom=None):
    _validar(itens)
    total = sum(i["preco"] * i["qtd"] for i in itens)
    if cupom == "DEZ":
        total *= 0.9
    return round(total, 2)


def pedido_certo(itens):
    if any(i["sku"] == "SEM-ESTOQUE" for i in itens):
        raise EstoqueInsuficiente("sem estoque")
    return {"id": "1"}


# Cada mutante muda UMA coisa em relação ao total_certo.
def total_cupom_ignorado(itens, cupom=None):
    return total_certo(itens, cupom=None)


def total_desconto_20(itens, cupom=None):
    _validar(itens)
    t = sum(i["preco"] * i["qtd"] for i in itens)
    return round(t * (0.8 if cupom == "DEZ" else 1), 2)


def total_perde_ultimo_item(itens, cupom=None):
    return total_certo(itens[:-1] if len(itens) > 1 else itens, cupom)


def total_sem_arredondar(itens, cupom=None):
    _validar(itens)
    t = sum(i["preco"] * i["qtd"] for i in itens)
    return t * 0.9 if cupom == "DEZ" else t


def total_aceita_qtd_negativa(itens, cupom=None):  # defeito: sem validação de quantidade
    t = sum(i["preco"] * i["qtd"] for i in itens)
    return round(t * (0.9 if cupom == "DEZ" else 1), 2)


def pedido_aceita_sem_estoque(itens):
    return {"id": "1"}  # defeito: vende o que não tem


def pedido_quebrado_por_assinatura(itens):
    raise TypeError("criar_pedido() got an unexpected keyword argument")  # erro qualquer


MUTANTES = [
    # nome, calcular_total, criar_pedido
    ("correto (controle)", total_certo, pedido_certo),
    ("cupom ignorado", total_cupom_ignorado, pedido_certo),
    ("desconto de 20% em vez de 10%", total_desconto_20, pedido_certo),
    ("soma perde o último item", total_perde_ultimo_item, pedido_certo),
    ("total sem arredondar (float cru)", total_sem_arredondar, pedido_certo),
    ("aceita quantidade negativa", total_aceita_qtd_negativa, pedido_certo),
    ("vende SKU sem estoque (não recusa)", total_certo, pedido_aceita_sem_estoque),
    ("criar_pedido quebra com TypeError", total_certo, pedido_quebrado_por_assinatura),
]


# ---------------------------------------------------------------- stubs de módulos
class Resposta:
    def __init__(self, status, corpo):
        self.status_code, self._corpo = status, corpo

    def json(self):
        return self._corpo


def instalar_stubs(calcular_total, criar_pedido, chamadas_http=None, resposta=None):
    loja, pedidos = types.ModuleType("loja"), types.ModuleType("loja.pedidos")
    pedidos.calcular_total, pedidos.criar_pedido = calcular_total, criar_pedido
    loja.pedidos = pedidos
    sys.modules["loja"], sys.modules["loja.pedidos"] = loja, pedidos

    req = types.ModuleType("requests")

    def _chamar(metodo, url, **kw):
        if chamadas_http is not None:
            chamadas_http.append((metodo, url))
        return resposta or Resposta(200, {"id": "p-1"})

    req.post = lambda url, **kw: _chamar("POST", url, **kw)
    req.get = lambda url, **kw: _chamar("GET", url, **kw)
    sys.modules["requests"] = req


def carregar(caminho, nome):
    mod = types.ModuleType(nome)
    mod.__file__ = caminho
    with open(caminho, encoding="utf-8") as f:
        exec(compile(f.read(), caminho, "exec"), mod.__dict__)
    return mod


def rodar(fn):
    try:
        fn()
        return "passou"
    except BaseException as e:  # noqa: BLE001 - relatório de demonstração
        return f"FALHOU ({type(e).__name__})"


# ---------------------------------------------------------------- shim mínimo de pytest
class _Approx:
    def __init__(self, esperado, abs=1e-12):
        self.esperado, self.tol = esperado, abs

    def __eq__(self, outro):
        return abs(outro - self.esperado) <= self.tol


@contextlib.contextmanager
def _raises(exc):
    try:
        yield
    except exc:
        return
    raise AssertionError(f"DID NOT RAISE {exc!r}")


def instalar_shim_pytest():
    pt = types.ModuleType("pytest")
    pt.approx = lambda esperado, abs=1e-12: _Approx(esperado, abs)
    pt.raises = _raises

    def parametrize(nomes, valores):
        nomes = [n.strip() for n in nomes.split(",")]

        def deco(fn):
            fn._casos = [dict(zip(nomes, v if len(nomes) > 1 else (v,))) for v in valores]
            return fn
        return deco

    pt.mark = types.SimpleNamespace(parametrize=parametrize)
    sys.modules["pytest"] = pt


def testes_de(mod):
    for nome, fn in mod.__dict__.items():
        if nome.startswith("test_") and callable(fn):
            for caso in getattr(fn, "_casos", [{}]):
                yield nome, (lambda f=fn, c=caso: f(**c))


def main():
    print(f"Arquivo original: {ORIGINAL}\n")
    instalar_shim_pytest()
    time_sleep = mock.patch.object(time, "sleep", lambda s: None)
    time_sleep.start()  # test_consultar_pedido tem sleep(5); aqui não esperamos

    # ---- 1. Original contra cada mutante (só os testes de lógica, sem HTTP)
    print("== 1. Suíte ORIGINAL (testes sem HTTP) contra implementações com defeito ==")
    nomes_orig = ["test_total_com_desconto", "test_pedido_sem_estoque", "test_total_varios_itens"]
    print(f"{'defeito plantado':40} " + " ".join(f"{n.replace('test_', ''):26}" for n in nomes_orig))
    for nome, ct, cp in MUTANTES:
        instalar_stubs(ct, cp)
        orig = carregar(ORIGINAL, "orig")
        res = [rodar(getattr(orig, n)) for n in nomes_orig]
        print(f"{nome:40} " + " ".join(f"{r:26}" for r in res))

    # ---- 2. test_cancelar_pedido e pedido_id None
    print("\n== 2. test_cancelar_pedido (sem asserção) com API respondendo 500 e pedido_id None ==")
    chamadas = []
    instalar_stubs(total_certo, pedido_certo, chamadas,
                   Resposta(500, {"erro": "falha interna"}))
    orig = carregar(ORIGINAL, "orig")
    print("  pedido_id inicial:", orig.pedido_id)
    print("  resultado:", rodar(orig.test_cancelar_pedido), "| chamada feita:", chamadas[-1])

    # ---- 3. float
    print("\n== 3. Float em dinheiro ==")
    print("  10.1*3 + 0.2 =", repr(10.1 * 3 + 0.2), "(esperado à mão: 30.50)")

    # ---- 4. patch na unidade testada: o nome importado não é o nome patchado
    print("\n== 4. test_total_com_desconto: o patch tem efeito? ==")
    instalar_stubs(total_cupom_ignorado, pedido_certo)
    orig = carregar(ORIGINAL, "orig")
    print("  original, com cupom ignorado pelo sistema:", rodar(orig.test_total_com_desconto),
          "(o teste chama o nome importado, que o patch não altera)")
    import loja.pedidos as p  # variante hipotética: chamada via módulo

    def variante():
        with mock.patch("loja.pedidos.calcular_total", return_value=90.0):
            assert p.calcular_total([{"preco": 100.0, "qtd": 1}], cupom="DEZ") == 90.0
    print("  variante (chamando via loja.pedidos.calcular_total), cupom ignorado:", rodar(variante),
          "<- vira tautologia")

    # ---- 5. suíte corrigida contra os mesmos mutantes
    print("\n== 5. Suíte CORRIGIDA (test_pedidos_regras.py) contra os mesmos defeitos ==")
    print("   (a) ErroSemEstoque = Exception (como entregue)   (b) ErroSemEstoque = EstoqueInsuficiente")
    for nome, ct, cp in MUTANTES:
        linha = []
        for ajuste in ("a", "b"):
            instalar_stubs(ct, cp)
            corr = carregar(CORRIGIDO, "corr")
            if ajuste == "b":
                corr.ErroSemEstoque = EstoqueInsuficiente
            res = [(n, rodar(f)) for n, f in testes_de(corr)]
            falhas = sorted({n for n, r in res if r != "passou"})
            linha.append(f"{len(falhas)} teste(s) falham" + (f": {', '.join(falhas)}" if falhas else ""))
        print(f"  {nome:36} (a) {linha[0]}\n  {'':36} (b) {linha[1]}")
    time_sleep.stop()


if __name__ == "__main__":
    main()
