"""Fixtures compartilhadas: configuração por variáveis de ambiente, clientes autenticados dos
dois usuários de teste e checagem fail-fast do ambiente.

Como obter os tokens é decisão sua: o OpenAPI só declara `bearer` e não tem endpoint de login.
Aqui eles vêm de TOKEN_USUARIO_A / TOKEN_USUARIO_B. Se os tokens expiram rápido, troque os
fixtures `api_a` e `api_b` por uma chamada ao seu provedor de identidade.
"""
import uuid

import pytest
import requests

from cliente import ApiClient, ConfigInvalida, Espera, carregar_config, extrato


def pytest_configure(config):
    # Os testes de transferência fazem leituras de saldo antes/depois: em paralelo, um
    # teste enxergaria o débito do outro e falharia (ou, pior, passaria por acaso).
    if getattr(config.option, "numprocesses", None):
        raise pytest.UsageError("Não rode esta suíte em paralelo (-n): os testes compartilham as mesmas duas contas.")


@pytest.fixture(scope="session")
def cfg():
    try:
        return carregar_config()
    except ConfigInvalida as exc:
        pytest.exit(f"Configuração inválida: {exc}", returncode=2)


@pytest.fixture(scope="session")
def api_a(cfg):
    return ApiClient(cfg.base_url, cfg.token_a, cfg.timeout)


@pytest.fixture(scope="session")
def api_b(cfg):
    return ApiClient(cfg.base_url, cfg.token_b, cfg.timeout)


@pytest.fixture(scope="session")
def conta_a(cfg):
    return cfg.conta_a


@pytest.fixture(scope="session")
def conta_b(cfg):
    return cfg.conta_b


@pytest.fixture(scope="session")
def chave_b(cfg):
    return cfg.chave_b


@pytest.fixture(scope="session")
def chave_a(cfg):
    if not cfg.chave_a:
        pytest.skip("defina CHAVE_PIX_A (chave PIX da conta A) para rodar este teste")
    return cfg.chave_a


@pytest.fixture(scope="session")
def espera(cfg):
    return Espera(estavel_por=cfg.espera_estabilizacao, timeout=cfg.timeout_assincrono)


@pytest.fixture(scope="session")
def run_id():
    """Identifica esta execução nas descrições das transferências (ajuda a achar no extrato de homolog)."""
    return uuid.uuid4().hex[:8]


@pytest.fixture(params=["A", "B"])
def titular(request, api_a, api_b, conta_a, conta_b):
    """(cliente, conta) de cada um dos dois usuários, cada um na sua própria conta."""
    return (api_a, conta_a) if request.param == "A" else (api_b, conta_b)


@pytest.fixture(params=["A-le-B", "B-le-A"])
def cruzamento(request, api_a, api_b, conta_a, conta_b):
    """(cliente do intruso, conta da vítima): usuário autenticado tentando usar a conta do outro."""
    return (api_a, conta_b) if request.param == "A-le-B" else (api_b, conta_a)


@pytest.fixture(scope="session", autouse=True)
def _ambiente_operacional(cfg, api_a, api_b, conta_a, conta_b):
    """Falha rápido, com mensagem clara, se token/conta estiverem errados ou expirados.

    Sem isso, um token vencido viraria dezenas de falhas enganosas ("esperava 200, veio 401").
    """
    for nome, api, conta in (("A", api_a, conta_a), ("B", api_b, conta_b)):
        try:
            resp = extrato(api, conta, tamanho=1)
        except requests.RequestException as exc:
            pytest.exit(f"Ambiente inacessível ({cfg.base_url}): {type(exc).__name__}: {str(exc)[:200]}", returncode=2)
        if resp.status_code != 200:
            pytest.exit(
                f"Pré-condição falhou: o usuário {nome} não conseguiu ler o extrato da própria conta "
                f"(HTTP {resp.status_code}). Confira token e CONTA_ID_{nome}; tokens expiram.",
                returncode=2,
            )
