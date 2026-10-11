"""Cliente HTTP e utilitários de leitura usados pelos testes da API Conta Digital.

Nada aqui depende de pytest, para poder ser reaproveitado em scripts.
Nunca registramos nem imprimimos o token: mensagens de erro mostram só status e
um trecho curto do corpo da resposta.
"""
from __future__ import annotations

import os
import re
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Callable, Iterator, Mapping, Optional

import requests

URL_PADRAO = "https://api-homolog.bancodigital.exemplo/v1"  # servers[0] do OpenAPI
CENTAVO = Decimal("0.01")

_PADRAO = object()  # "use o token do cliente"
_GERAR = object()   # "gere uma Idempotency-Key nova"

RE_UUID = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)


# --------------------------------------------------------------------------- #
# Configuração
# --------------------------------------------------------------------------- #
class ConfigInvalida(Exception):
    pass


@dataclass(frozen=True)
class Config:
    base_url: str
    token_a: str
    token_b: str
    conta_a: str
    conta_b: str
    chave_b: str                 # chave PIX da conta B: destino das transferências de A
    chave_a: Optional[str]       # chave PIX da conta A: opcional, só alguns testes usam
    timeout: float               # por requisição
    timeout_assincrono: float    # quanto esperar o saldo/extrato refletir uma transferência
    espera_estabilizacao: float  # por quanto tempo o saldo precisa ficar parado para ser "estável"
    rodar_limite_diario: bool    # liga o teste que consome o limite diário da conta A


_OBRIGATORIAS = ("TOKEN_USUARIO_A", "TOKEN_USUARIO_B", "CONTA_ID_A", "CONTA_ID_B", "CHAVE_PIX_B")


def carregar_config(env: Optional[Mapping[str, str]] = None) -> Config:
    env = os.environ if env is None else env

    def pegar(nome: str) -> str:
        return (env.get(nome) or "").strip()

    faltando = [n for n in _OBRIGATORIAS if not pegar(n)]
    if faltando:
        raise ConfigInvalida(
            "Variáveis de ambiente obrigatórias ausentes: "
            + ", ".join(faltando)
            + " (veja .env.example)."
        )

    base_url = (pegar("API_BASE_URL") or URL_PADRAO).rstrip("/")
    # Estes testes MOVEM dinheiro (centavos) entre as contas de teste. Trava de segurança
    # para ninguém apontar para produção por engano.
    if "homolog" not in base_url.lower() and pegar("PERMITIR_URL_FORA_DE_HOMOLOG") != "1":
        raise ConfigInvalida(
            f"API_BASE_URL ({base_url}) não parece ser homologação. Se for mesmo o ambiente "
            "certo, defina PERMITIR_URL_FORA_DE_HOMOLOG=1."
        )

    conta_a, conta_b = pegar("CONTA_ID_A"), pegar("CONTA_ID_B")
    for nome, valor in (("CONTA_ID_A", conta_a), ("CONTA_ID_B", conta_b)):
        if not RE_UUID.match(valor):
            raise ConfigInvalida(f"{nome} não é um UUID.")
    if conta_a.lower() == conta_b.lower():
        raise ConfigInvalida("CONTA_ID_A e CONTA_ID_B são iguais: preciso de duas contas distintas.")
    if pegar("TOKEN_USUARIO_A") == pegar("TOKEN_USUARIO_B"):
        raise ConfigInvalida("TOKEN_USUARIO_A e TOKEN_USUARIO_B são iguais: preciso de dois usuários.")

    try:
        timeout = float(pegar("TIMEOUT_REQUISICAO") or 15)
        timeout_assincrono = float(pegar("TIMEOUT_ASSINCRONO") or 20)
        espera = float(pegar("ESPERA_ESTABILIZACAO") or 3)
    except ValueError as exc:
        raise ConfigInvalida(f"Valor numérico inválido numa variável de tempo: {exc}") from exc

    return Config(
        base_url=base_url,
        token_a=pegar("TOKEN_USUARIO_A"),
        token_b=pegar("TOKEN_USUARIO_B"),
        conta_a=conta_a,
        conta_b=conta_b,
        chave_b=pegar("CHAVE_PIX_B"),
        chave_a=pegar("CHAVE_PIX_A") or None,
        timeout=timeout,
        timeout_assincrono=timeout_assincrono,
        espera_estabilizacao=espera,
        rodar_limite_diario=pegar("RODAR_TESTES_LIMITE_DIARIO") == "1",
    )


# --------------------------------------------------------------------------- #
# Cliente HTTP
# --------------------------------------------------------------------------- #
class ApiClient:
    """Envolve requests.Session com base URL, timeout, bearer token e sem redirecionamento."""

    def __init__(self, base_url: str, token: Optional[str] = None, timeout: float = 15.0):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self._sessao = requests.Session()

    def request(self, metodo: str, caminho: str, *, token=_PADRAO, headers=None, **kw) -> requests.Response:
        """token=_PADRAO usa o token do cliente; token=None não envia Authorization.

        `headers` é aplicado por último: serve para forçar um Authorization diferente.
        """
        cabecalhos = {"Accept": "application/json"}
        efetivo = self.token if token is _PADRAO else token
        if efetivo is not None:
            cabecalhos["Authorization"] = f"Bearer {efetivo}"
        if headers:
            cabecalhos.update(headers)
        kw.setdefault("timeout", self.timeout)
        # Redirecionar poderia descartar o Authorization e mascarar um problema de roteamento.
        kw.setdefault("allow_redirects", False)
        return self._sessao.request(metodo, f"{self.base_url}{caminho}", headers=cabecalhos, **kw)

    def get(self, caminho: str, **kw) -> requests.Response:
        return self.request("GET", caminho, **kw)

    def post(self, caminho: str, **kw) -> requests.Response:
        return self.request("POST", caminho, **kw)

    def com_token(self, token: Optional[str]) -> "ApiClient":
        """Cliente novo (sessão própria) com outro token: útil em threads."""
        return ApiClient(self.base_url, token, self.timeout)


# Formas de NÃO estar autenticado. {id: cabeçalhos a enviar (token do cliente é suprimido)}
SEM_AUTENTICACAO = {
    "sem-header": {},
    "token-invalido": {"Authorization": "Bearer token-invalido"},
    "bearer-vazio": {"Authorization": "Bearer "},
    "esquema-errado": {"Authorization": "Basic dXNlcjpzZW5oYQ=="},
}


def detalhe(resp: requests.Response, limite: int = 300) -> str:
    return f"HTTP {resp.status_code} {resp.headers.get('Content-Type', '-')}: {resp.text[:limite]!r}"


def fmt_valor(valor: Decimal) -> str:
    """Decimal -> string no formato da API ('150.00'). Nunca use float com dinheiro."""
    return format(valor.quantize(CENTAVO), "f")


def ontem_utc() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=1)).date().isoformat()


# --------------------------------------------------------------------------- #
# Extrato
# --------------------------------------------------------------------------- #
def extrato(api: ApiClient, conta_id: str, *, token=_PADRAO, headers=None, **params) -> requests.Response:
    """GET /contas/{contaId}/extrato. Parâmetros com valor None são omitidos."""
    return api.get(f"/contas/{conta_id}/extrato", params=params or None, token=token, headers=headers)


def saldo_de(api: ApiClient, conta_id: str) -> Decimal:
    resp = extrato(api, conta_id, tamanho=1)
    assert resp.status_code == 200, f"não consegui ler o saldo de {conta_id}: {detalhe(resp)}"
    return Decimal(resp.json()["saldo"])


def percorrer_extrato(
    api: ApiClient, conta_id: str, *, tamanho: int, max_paginas: int, **filtros
) -> Iterator[dict]:
    """Gera o corpo de cada página, seguindo proximaPagina (cursor opaco) até null."""
    cursor = None
    for _ in range(max_paginas):
        resp = extrato(api, conta_id, tamanho=tamanho, pagina=cursor, **filtros)
        assert resp.status_code == 200, f"falha paginando o extrato: {detalhe(resp)}"
        corpo = resp.json()
        yield corpo
        cursor = corpo.get("proximaPagina")
        if cursor is None:
            return


class Espera:
    """Esperas por consistência eventual (transferência PROCESSANDO -> saldo/extrato refletem)."""

    def __init__(self, *, estavel_por: float, timeout: float):
        self.estavel_por = estavel_por
        self.timeout = timeout

    def saldo_estavel(self, api: ApiClient, conta_id: str) -> Decimal:
        """Devolve o saldo depois de ficar parado por `estavel_por` segundos (ou ao estourar o timeout)."""
        limite = time.monotonic() + self.timeout
        valor = saldo_de(api, conta_id)
        parado_desde = time.monotonic()
        while time.monotonic() < limite:
            time.sleep(min(1.0, self.estavel_por))
            atual = saldo_de(api, conta_id)
            agora = time.monotonic()
            if atual != valor:
                valor, parado_desde = atual, agora
            elif agora - parado_desde >= self.estavel_por:
                return valor
        return valor

    def saldo_chegar_a(self, api: ApiClient, conta_id: str, esperado: Decimal) -> Decimal:
        """Faz polling até o saldo ser `esperado`; devolve o último saldo lido (o teste é quem afirma)."""
        limite = time.monotonic() + self.timeout
        while True:
            atual = saldo_de(api, conta_id)
            if atual == esperado or time.monotonic() >= limite:
                return atual
            time.sleep(1.0)

    def lancamento(
        self, api: ApiClient, conta_id: str, predicado: Callable[[dict], bool], *, desde: Optional[str] = None
    ) -> Optional[dict]:
        """Procura (com polling) um lançamento que satisfaça `predicado`. None se não aparecer."""
        limite = time.monotonic() + self.timeout
        while True:
            for pagina in percorrer_extrato(api, conta_id, tamanho=100, max_paginas=20, desde=desde):
                for lanc in pagina["lancamentos"]:
                    if predicado(lanc):
                        return lanc
            if time.monotonic() >= limite:
                return None
            time.sleep(1.0)


# --------------------------------------------------------------------------- #
# Transferências
# --------------------------------------------------------------------------- #
def corpo_transferencia(conta_origem: str, chave_destino: str, valor: str = "0.01", **extra) -> dict:
    corpo = {"contaOrigemId": conta_origem, "chaveDestino": chave_destino, "valor": valor}
    corpo.update(extra)
    return corpo


def criar_transferencia(
    api: ApiClient, corpo, *, idem=_GERAR, token=_PADRAO, headers=None, bruto: Optional[str] = None
) -> requests.Response:
    """POST /transferencias.

    idem: _GERAR (padrão) cria uma Idempotency-Key UUID nova; None omite o header; string usa como está.
    bruto: se informado, é enviado como corpo literal (para testar JSON malformado).
    """
    cabecalhos = {}
    if idem is _GERAR:
        cabecalhos["Idempotency-Key"] = str(uuid.uuid4())
    elif idem is not None:
        cabecalhos["Idempotency-Key"] = idem
    if headers:
        cabecalhos.update(headers)
    if bruto is not None:
        cabecalhos["Content-Type"] = "application/json"
        return api.post("/transferencias", data=bruto.encode("utf-8"), token=token, headers=cabecalhos)
    return api.post("/transferencias", json=corpo, token=token, headers=cabecalhos)
