"""Fixtures da suíte. Toda configuração vem do ambiente (veja .env.example); nada é fixo no código.

As duas contas de homologação são compartilhadas por todos os testes, então a suíte roda em
série (sem pytest-xdist). Cada teste usa um marcador único na descrição para achar os próprios
lançamentos e espera os próprios efeitos terminarem antes de acabar.
"""
from __future__ import annotations

import os
import uuid
from decimal import Decimal
from urllib.parse import urlparse

import pytest
import requests

pytest.register_assert_rewrite("tests.support")  # mostra os valores das asserções feitas nos helpers

from tests.support import (ApiContas, Conta, Extrato, Origem, dinheiro, enviar_marco, ler_extrato,
                           saldos)

OBRIGATORIAS = ("API_BASE_URL", "API_TOKEN_A", "API_TOKEN_B", "CONTA_A_ID", "CONTA_B_ID", "CHAVE_PIX_B")
SALDO_MINIMO_ORIGEM_A = Decimal("10.00")  # cada execução move alguns reais de A para B


# --------------------------------------------------------------------------
# Hooks
# --------------------------------------------------------------------------
def pytest_report_header(config):
    """Manifesto curto da execução (sem segredos)."""
    host = urlparse(os.environ.get("API_BASE_URL", "")).hostname or "<API_BASE_URL não definida>"
    destrutivos = "ligados" if os.environ.get("RUN_TESTES_DESTRUTIVOS") == "1" else "desligados"
    reversa = "sim" if os.environ.get("CHAVE_PIX_A") else "não (sem CHAVE_PIX_A)"
    return [f"api-contas: host={host} destrutivos={destrutivos} direção B->A={reversa}"]


def pytest_collection_modifyitems(config, items):
    if os.environ.get("RUN_TESTES_DESTRUTIVOS") != "1":
        pular = pytest.mark.skip(reason="destrutivo: move valores altos e consome o limite diário; "
                                        "exporte RUN_TESTES_DESTRUTIVOS=1 para executar (por último, em conta de teste)")
        for item in items:
            if item.get_closest_marker("destrutivo"):
                item.add_marker(pular)
    # destrutivos por último: consomem o limite diário e o saldo das contas
    items.sort(key=lambda item: item.get_closest_marker("destrutivo") is not None)


# --------------------------------------------------------------------------
# Ambiente e preflight (falha de setup é bloqueio de ambiente, não resultado de teste)
# --------------------------------------------------------------------------
@pytest.fixture(scope="session")
def ambiente() -> dict:
    faltando = [nome for nome in OBRIGATORIAS if not os.environ.get(nome)]
    if faltando:
        pytest.exit(f"Configuração incompleta: defina {', '.join(faltando)} (veja .env.example).", returncode=2)
    if os.environ.get("PYTEST_XDIST_WORKER"):
        pytest.exit("As contas de teste são compartilhadas: rode sem pytest-xdist (-n).", returncode=2)
    url = os.environ["API_BASE_URL"].rstrip("/")
    host = urlparse(url).hostname or ""
    if "homolog" not in host and os.environ.get("API_PERMITIR_HOST_FORA_DE_HOMOLOG") != "1":
        pytest.exit(f"A suíte move dinheiro; o host '{host}' não parece ser de homologação. "
                    "Se for mesmo um ambiente de teste, exporte API_PERMITIR_HOST_FORA_DE_HOMOLOG=1.", returncode=2)
    try:
        ids = {rotulo: str(uuid.UUID(os.environ[f"CONTA_{rotulo}_ID"])) for rotulo in ("A", "B")}
    except ValueError:
        pytest.exit("CONTA_A_ID e CONTA_B_ID precisam ser UUIDs.", returncode=2)
    if ids["A"] == ids["B"]:
        pytest.exit("CONTA_A_ID e CONTA_B_ID são a mesma conta: o teste de isolamento ficaria sem sentido.", returncode=2)
    return {"url": url, "ids": ids}


@pytest.fixture(scope="session")
def conta_a(ambiente) -> Conta:
    return Conta("A", ambiente["ids"]["A"], ApiContas(ambiente["url"], os.environ["API_TOKEN_A"]),
                 os.environ.get("CHAVE_PIX_A") or None)


@pytest.fixture(scope="session")
def conta_b(ambiente) -> Conta:
    return Conta("B", ambiente["ids"]["B"], ApiContas(ambiente["url"], os.environ["API_TOKEN_B"]),
                 os.environ["CHAVE_PIX_B"])


@pytest.fixture(scope="session")
def api_a(conta_a) -> ApiContas:
    return conta_a.api


@pytest.fixture(scope="session")
def api_b(conta_b) -> ApiContas:
    return conta_b.api


@pytest.fixture(scope="session")
def origem_a(conta_a, conta_b) -> Origem:
    """Direção padrão dos testes: A paga, B recebe pela chave PIX de B."""
    return Origem(conta_a, conta_b)


@pytest.fixture(scope="session")
def origens(origem_a) -> list[Origem]:
    """Direções disponíveis; B->A só existe se CHAVE_PIX_A foi informada."""
    return [origem_a] + ([origem_a.inversa()] if origem_a.inversa() else [])


@pytest.fixture(scope="session")
def clientes_sem_credencial(ambiente) -> dict[str, ApiContas]:
    return {"sem_token": ApiContas(ambiente["url"], None),
            "token_invalido": ApiContas(ambiente["url"], "token-invalido-de-teste")}


@pytest.fixture(scope="session", autouse=True)
def preflight(conta_a, conta_b):
    """Antes de qualquer teste: o ambiente responde, os tokens valem para as contas informadas e A tem saldo."""
    for conta in (conta_a, conta_b):
        try:
            resposta = conta.api.extrato(conta.id, tamanho=1)
        except requests.RequestException as erro:
            pytest.exit(f"Preflight: API inacessível ({type(erro).__name__}). Bloqueio de ambiente, "
                        "não resultado de teste.", returncode=2)
        if resposta.status_code != 200:
            pytest.exit(f"Preflight: GET extrato da conta {conta.rotulo} devolveu {resposta.status_code}. "
                        "Token expirado, conta errada ou ambiente fora do ar - bloqueio, não resultado de teste.",
                        returncode=2)
        extrato = Extrato.model_validate(resposta.json())
        if str(extrato.contaId) != conta.id:
            pytest.exit(f"Preflight: o extrato da conta {conta.rotulo} veio com outro contaId.", returncode=2)
    saldo_a = dinheiro(ler_extrato(conta_a.api, conta_a.id, tamanho=1).saldo)
    if saldo_a < SALDO_MINIMO_ORIGEM_A:
        pytest.exit(f"Preflight: saldo da conta A ({saldo_a}) abaixo de {SALDO_MINIMO_ORIGEM_A}; "
                    "a suíte precisa de saldo para as transferências de teste.", returncode=2)


@pytest.fixture(scope="session")
def historico_a(origem_a, preflight):
    """Garante pelo menos 3 lançamentos na conta A (precondição dos testes de paginação)."""
    atual = len(ler_extrato(origem_a.de.api, origem_a.de.id, tamanho=3).lancamentos)
    antes = saldos(origem_a)
    for _ in range(max(0, 3 - atual)):
        antes = enviar_marco(origem_a, antes)
    return origem_a
