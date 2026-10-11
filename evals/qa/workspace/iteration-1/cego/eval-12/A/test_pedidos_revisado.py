"""Versao revisada de test_pedidos.py (proposta, NAO executada: sem pytest/rede no ambiente da revisao).

Premissas que precisam ser confirmadas contra o codigo real (marcadas com TODO):
  - nome da excecao de estoque (EstoqueInsuficiente);
  - campos do JSON de pedido (id, itens, status) e valores de status;
  - status HTTP de criacao (a suite original assumia 200).

Rodar so o que e rapido e offline:   pytest -m "not integration"
Rodar contra homologacao:            LOJA_API_BASE=... LOJA_API_TOKEN=... pytest -m integration

pytest.ini sugerido:
    [pytest]
    markers = integration: chama a API de homologacao (rede, lento)
    addopts = --strict-markers
    # opcionais: pytest-randomly (detecta dependencia de ordem), pytest-timeout, pytest-socket
"""
import os
import time
import uuid

import pytest
import requests

from loja.pedidos import calcular_total, criar_pedido
from loja.pedidos import EstoqueInsuficiente  # TODO: confirmar nome real da excecao

# --------------------------------------------------------------------------
# Unitarios: rapidos, sem rede, sem mock da funcao que esta sendo testada
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "itens, esperado",
    [
        ([{"preco": 100.0, "qtd": 1}], 100.0),
        ([{"preco": 50.0, "qtd": 3}], 150.0),                      # qtd > 1 precisa mudar o total
        ([{"preco": 10.1, "qtd": 3}, {"preco": 0.2, "qtd": 1}], 30.5),  # valor calculado a mao, nao a propria funcao
        ([], 0.0),
    ],
)
def test_total_sem_cupom(itens, esperado):
    # approx so absorve o ruido de float; o ideal e calcular_total devolver Decimal/centavos.
    assert calcular_total(itens) == pytest.approx(esperado, abs=1e-9)


@pytest.mark.parametrize(
    "itens, esperado",
    [
        ([{"preco": 100.0, "qtd": 1}], 90.0),
        ([{"preco": 50.0, "qtd": 2}], 90.0),                       # desconto incide sobre qtd * preco
        ([{"preco": 10.0, "qtd": 3}, {"preco": 20.0, "qtd": 1}], 45.0),  # desconto sobre o total, nao por item
    ],
)
def test_total_com_cupom_dez(itens, esperado):
    assert calcular_total(itens, cupom="DEZ") == pytest.approx(esperado, abs=1e-9)


def test_pedido_sem_estoque_levanta_excecao_especifica():
    # `assert False` dentro de try/except Exception era engolido pelo proprio except.
    with pytest.raises(EstoqueInsuficiente):
        criar_pedido([{"sku": "SEM-ESTOQUE", "qtd": 1}])


# TODO (regras a confirmar com produto antes de virar teste, pois nao da para inferir do codigo):
#   - cupom invalido/expirado/inexistente; desconto que zera ou deixa total negativo;
#   - qtd 0, negativa ou nao inteira; preco negativo; SKU inexistente;
#   - estoque exatamente igual a qtd pedida (limite) e estoque = qtd - 1.

# --------------------------------------------------------------------------
# Integracao (homologacao): cada teste cria o que precisa e limpa depois
# --------------------------------------------------------------------------

TIMEOUT = 10  # sem timeout, uma API pendurada trava a suite inteira


@pytest.fixture(scope="session")
def api():
    base = os.environ.get("LOJA_API_BASE")
    token = os.environ.get("LOJA_API_TOKEN")  # nunca no repositorio; usar um token com o menor privilegio necessario
    if not base or not token:
        pytest.skip("defina LOJA_API_BASE e LOJA_API_TOKEN para rodar os testes de integracao")

    class Api:
        def __init__(self):
            self.base = base.rstrip("/")
            self.s = requests.Session()
            self.s.headers["Authorization"] = f"Bearer {token}"

        def request(self, method, path, **kw):
            kw.setdefault("timeout", TIMEOUT)
            return self.s.request(method, f"{self.base}{path}", **kw)

        def anonimo(self, method, path, **kw):
            kw.setdefault("timeout", TIMEOUT)
            return requests.request(method, f"{self.base}{path}", **kw)

    return Api()


def esperar_ate(condicao, timeout=15, intervalo=0.5):
    """Polling com prazo no lugar de time.sleep(5): rapido quando ok, tolerante quando lento."""
    fim = time.monotonic() + timeout
    ultimo = None
    while time.monotonic() < fim:
        ultimo = condicao()
        if ultimo:
            return ultimo
        time.sleep(intervalo)
    raise AssertionError(f"condicao nao satisfeita em {timeout}s (ultimo valor: {ultimo!r})")


@pytest.fixture
def pedido(api):
    r = api.request("POST", "/pedidos", json={"itens": [{"sku": "ABC", "qtd": 2}]},
                    headers={"Idempotency-Key": str(uuid.uuid4())})  # TODO: remover se a API nao usa
    assert r.status_code == 200, r.text  # TODO: 201?
    corpo = r.json()
    yield corpo
    api.request("POST", f"/pedidos/{corpo['id']}/cancelar")  # limpeza best-effort


@pytest.mark.integration
def test_criar_pedido_devolve_pedido_consistente(pedido):
    assert pedido["id"]
    # TODO: ajustar aos campos reais do contrato
    assert [(i["sku"], i["qtd"]) for i in pedido["itens"]] == [("ABC", 2)]


@pytest.mark.integration
def test_consultar_pedido_criado(api, pedido):
    def lido():
        r = api.request("GET", f"/pedidos/{pedido['id']}")
        return r.json() if r.status_code == 200 else None

    assert esperar_ate(lido)["id"] == pedido["id"]


@pytest.mark.integration
def test_cancelar_pedido_muda_status(api, pedido):
    r = api.request("POST", f"/pedidos/{pedido['id']}/cancelar")
    assert r.status_code == 200, r.text
    estado = api.request("GET", f"/pedidos/{pedido['id']}").json()
    assert estado["status"] == "CANCELADO"  # TODO: valor real do status


@pytest.mark.integration
def test_cancelar_duas_vezes_nao_passa_batido(api, pedido):
    api.request("POST", f"/pedidos/{pedido['id']}/cancelar")
    r = api.request("POST", f"/pedidos/{pedido['id']}/cancelar")
    assert r.status_code in (409, 422), r.text  # TODO: confirmar o contrato (409? 200 idempotente?)


@pytest.mark.integration
def test_criar_pedido_sem_token_retorna_401(api):
    r = api.anonimo("POST", "/pedidos", json={"itens": [{"sku": "ABC", "qtd": 1}]})
    assert r.status_code == 401


@pytest.mark.integration
def test_criar_pedido_sem_estoque_retorna_erro_de_negocio(api):
    r = api.request("POST", "/pedidos", json={"itens": [{"sku": "SEM-ESTOQUE", "qtd": 1}]})
    assert r.status_code in (409, 422), r.text  # TODO: contrato real


# TODO: acesso a pedido de OUTRO usuario deve dar 403/404 (exige segundo token, nao-admin).
#       O token original era de "qa-admin": com admin, falhas de autorizacao nunca aparecem.
