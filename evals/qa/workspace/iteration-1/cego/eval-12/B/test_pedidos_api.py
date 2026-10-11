"""API de pedidos em homologação: cada teste cria o seu pedido, não depende de ordem,
espera por condição (não por tempo fixo) e roda como cliente comum, não como admin.

Rodar (valores vêm do ambiente/cofre do CI; nunca no código):
    API_BASE_URL=https://... API_TOKEN_A=... API_TOKEN_B=... pytest test_pedidos_api.py -q

NÃO foi executado contra o sistema real. Pontos marcados com AJUSTE seguem uma
suposição declarada no comentário: confirme no contrato da API.
"""
import os
import time

import pytest
import requests

TIMEOUT = 10  # requests sem timeout podem travar a suíte para sempre

# AJUSTE: o teste original esperava 200 na criação. Confirme no contrato se é 200 ou 201.
STATUS_CRIACAO = 200
STATUS_CANCELADO = "CANCELADO"           # AJUSTE: nome real do estado
ID_INEXISTENTE = "00000000-0000-4000-8000-000000000000"  # AJUSTE: formato real do ID
CORPO = {"itens": [{"sku": "ABC", "qtd": 2}]}
# AJUSTE: com o preço semeado de "ABC" no ambiente, assertar também o total
# (oráculo independente: preço x 2), em vez de só o status.


class Api:
    def __init__(self, base_url, token=None):
        self.base = base_url.rstrip("/")
        self.sessao = requests.Session()
        if token:
            self.sessao.headers["Authorization"] = f"Bearer {token}"

    def get(self, caminho, **kw):
        return self.sessao.get(f"{self.base}{caminho}", timeout=TIMEOUT, **kw)

    def post(self, caminho, **kw):
        return self.sessao.post(f"{self.base}{caminho}", timeout=TIMEOUT, **kw)


def esperar_ate(condicao, timeout=15.0, intervalo=0.5, descricao="condição"):
    """Polling com prazo e diagnóstico, no lugar de time.sleep(5)."""
    limite = time.monotonic() + timeout
    while not (resultado := condicao()):
        if time.monotonic() >= limite:
            raise AssertionError(f"{descricao} não ocorreu em {timeout} s")
        time.sleep(intervalo)
    return resultado


@pytest.fixture(scope="session")
def api_a():  # cliente comum A (não admin)
    return Api(os.environ["API_BASE_URL"], os.environ["API_TOKEN_A"])


@pytest.fixture(scope="session")
def api_b():  # cliente comum B, para provar isolamento entre clientes
    return Api(os.environ["API_BASE_URL"], os.environ["API_TOKEN_B"])


@pytest.fixture(scope="session")
def api_anonima():
    return Api(os.environ["API_BASE_URL"])


@pytest.fixture
def pedido(api_a):
    """Cada teste cria o próprio pedido e o cancela no fim (só o que ele criou)."""
    r = api_a.post("/pedidos", json=CORPO)
    assert r.status_code == STATUS_CRIACAO, r.text
    dados = r.json()
    yield dados
    api_a.post(f"/pedidos/{dados['id']}/cancelar")  # limpeza best-effort; 4xx se o teste já cancelou


def test_pedido_criado_pode_ser_consultado_com_os_mesmos_itens(api_a, pedido):
    def consultar():
        r = api_a.get(f"/pedidos/{pedido['id']}")
        return r.json() if r.status_code == 200 else None

    lido = esperar_ate(consultar, descricao="pedido consultável")
    assert lido["id"] == pedido["id"]
    assert [(i["sku"], i["qtd"]) for i in lido["itens"]] == [("ABC", 2)]


def test_cancelar_muda_o_estado_e_um_segundo_cancelamento_e_recusado(api_a, pedido):
    r = api_a.post(f"/pedidos/{pedido['id']}/cancelar")
    assert r.status_code == 200, r.text

    esperar_ate(lambda: api_a.get(f"/pedidos/{pedido['id']}").json().get("status") == STATUS_CANCELADO,
                descricao="pedido cancelado")
    # AJUSTE: 409 é o usual para transição inválida; confirme o contrato.
    assert api_a.post(f"/pedidos/{pedido['id']}/cancelar").status_code == 409


def test_pedido_de_outro_cliente_nao_e_visivel_nem_cancelavel(api_a, api_b, pedido):
    # AJUSTE: 404 (existência não vaza) ou 403, conforme o contrato; o importante é
    # "pedido alheio" ser indistinguível de "pedido inexistente".
    inexistente = api_b.get(f"/pedidos/{ID_INEXISTENTE}")
    alheio = api_b.get(f"/pedidos/{pedido['id']}")
    assert alheio.status_code == inexistente.status_code == 404

    assert api_b.post(f"/pedidos/{pedido['id']}/cancelar").status_code == 404
    assert api_a.get(f"/pedidos/{pedido['id']}").json()["status"] != STATUS_CANCELADO


def test_sem_token_e_recusado(api_anonima):
    assert api_anonima.post("/pedidos", json=CORPO).status_code == 401


@pytest.mark.parametrize("qtd", [0, -1])
def test_quantidade_invalida_e_recusada_sem_criar_pedido(api_a, qtd):
    r = api_a.post("/pedidos", json={"itens": [{"sku": "ABC", "qtd": qtd}]})
    assert r.status_code in (400, 422), r.text  # AJUSTE: o código que o contrato definir
    # AJUSTE: confirme também, pela listagem de pedidos do cliente A, que nada foi criado.
