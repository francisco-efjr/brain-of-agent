"""Cliente fino, modelos do contrato e helpers da suíte da API Conta Digital.

Decisões que valem para a suíte inteira:

* O cliente devolve a resposta crua (sem asserção e sem exceção em 4xx) e
  sempre usa timeout; quem decide o que é "certo" é o teste.
* Dinheiro é `Decimal` no teste e string "123.45" no fio. Nunca `float`.
* Efeitos de uma transferência são assíncronos (o contrato prevê o status
  PROCESSANDO): espera-se por condição com prazo (`esperar_ate`), nunca por
  tempo fixo.
* "Não houve efeito" é provado com um marco: uma transferência válida e
  posterior que já apareceu no extrato. Só então se confere a ausência.
"""
from __future__ import annotations

import os
import re
import time
import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Callable, Iterator, Literal
from urllib.parse import quote
from zoneinfo import ZoneInfo

import pytest
import requests
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

CENTAVO = Decimal("0.01")
LIMITE_DIARIO = Decimal("5000.00")  # contrato: NovaTransferencia.valor
TAMANHO_PADRAO = 20  # contrato: parâmetro `tamanho`, default 20
PADRAO_VALOR = r"^-?[0-9]+\.[0-9]{2}$"  # contrato: Lancamento.valor / Extrato.saldo

ESPERA_MAX = float(os.environ.get("API_ESPERA_MAX", "20"))  # segundos
FUSO = ZoneInfo(os.environ.get("API_FUSO", "America/Sao_Paulo"))  # fuso do "dia" do negócio

_GERAR = object()  # sentinela: gerar uma Idempotency-Key nova


# --------------------------------------------------------------------------
# Modelos do contrato (espelham o openapi-contas.yaml 1.4.0)
# --------------------------------------------------------------------------
class _Modelo(BaseModel):
    # campo novo na resposta não é quebra de contrato; campo sensível é checado à parte
    model_config = ConfigDict(extra="ignore")


class Lancamento(_Modelo):
    id: uuid.UUID
    data: AwareDatetime
    descricao: str = Field(max_length=140)
    valor: str = Field(pattern=PADRAO_VALOR)
    tipo: Literal["CREDITO", "DEBITO"]


class Extrato(_Modelo):
    contaId: uuid.UUID
    saldo: str = Field(pattern=PADRAO_VALOR)
    lancamentos: list[Lancamento]
    proximaPagina: str | None  # obrigatório, mas pode ser null (última página)


class Transferencia(_Modelo):
    id: uuid.UUID
    status: Literal["PROCESSANDO", "CONCLUIDA", "RECUSADA"]
    valor: str
    criadaEm: AwareDatetime


class Problema(_Modelo):  # RFC 9457; no contrato nenhum campo é obrigatório
    type: str | None = None
    title: str | None = None
    status: int | None = None
    detail: str | None = None


# --------------------------------------------------------------------------
# Cliente fino
# --------------------------------------------------------------------------
class ApiContas:
    """Uma operação por método; devolve `requests.Response` sem interpretar."""

    def __init__(self, base_url: str, token: str | None = None, timeout: float = 15.0):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self._sessao = requests.Session()

    def novo(self) -> "ApiContas":
        """Cliente independente com a mesma credencial (um por thread nos testes de concorrência)."""
        return ApiContas(self.base_url, self.token, self.timeout)

    def _requisitar(self, metodo: str, caminho: str, **kwargs) -> requests.Response:
        headers = dict(kwargs.pop("headers", None) or {})
        if self.token is not None:
            headers.setdefault("Authorization", f"Bearer {self.token}")
        return self._sessao.request(metodo, f"{self.base_url}{caminho}", headers=headers,
                                    timeout=self.timeout, **kwargs)

    def extrato(self, conta_id: str, **params: Any) -> requests.Response:
        # parâmetros None são omitidos; "" vai como `?tamanho=`
        caminho = f"/contas/{quote(str(conta_id), safe='')}/extrato"
        return self._requisitar("GET", caminho, params=params or None)

    def transferir(self, corpo: Any = None, *, idempotency_key: Any = _GERAR,
                   bruto: bytes | None = None) -> requests.Response:
        """`idempotency_key=None` omite o header; `bruto` envia o corpo sem passar pelo json()."""
        headers: dict[str, str] = {}
        if idempotency_key is _GERAR:
            headers["Idempotency-Key"] = str(uuid.uuid4())
        elif idempotency_key is not None:
            headers["Idempotency-Key"] = idempotency_key
        if bruto is not None:
            headers["Content-Type"] = "application/json"
            return self._requisitar("POST", "/transferencias", data=bruto, headers=headers)
        return self._requisitar("POST", "/transferencias", json=corpo, headers=headers)


@dataclass(frozen=True)
class Conta:
    rotulo: str  # "A" ou "B"
    id: str  # UUID em minúsculas
    api: ApiContas  # autenticada como o titular desta conta
    chave_pix: str | None  # chave PIX que aponta para esta conta


@dataclass(frozen=True)
class Origem:
    """Uma direção de transferência: `de` paga, `para` recebe (pela chave PIX de `para`)."""
    de: Conta
    para: Conta

    @property
    def rotulo(self) -> str:
        return f"{self.de.rotulo}->{self.para.rotulo}"

    def inversa(self) -> "Origem | None":
        """Direção contrária, possível só se a chave PIX de `de` é conhecida."""
        return Origem(self.para, self.de) if self.de.chave_pix else None


@dataclass(frozen=True)
class Saldos:
    origem: Decimal
    destino: Decimal

    def apos(self, valor: Decimal) -> "Saldos":
        return Saldos(self.origem - valor, self.destino + valor)


# --------------------------------------------------------------------------
# Dinheiro, tempo e identificadores
# --------------------------------------------------------------------------
def dinheiro(texto: str) -> Decimal:
    """'150.00' -> Decimal('150.00'); recusa qualquer formato fora do contrato."""
    assert re.fullmatch(r"-?[0-9]+\.[0-9]{2}", texto), f"valor fora do formato do contrato: {texto!r}"
    return Decimal(texto)


def moeda(valor: Decimal) -> str:
    return f"{valor.quantize(CENTAVO):.2f}"


def novo_marcador() -> str:
    return f"qa-{uuid.uuid4().hex[:12]}"


def descricao_com(marcador: str, texto: str = "") -> str:
    descricao = f"{marcador} {texto}".strip()
    assert len(descricao) <= 140, "descrição de teste acima do limite do contrato"
    return descricao


def agora_utc() -> datetime:
    return datetime.now(tz=timezone.utc)


def hoje_local() -> date:
    return datetime.now(tz=FUSO).date()


def data_local(momento: datetime) -> date:
    return momento.astimezone(FUSO).date()


def assert_proximo_de_agora(momento: datetime, tolerancia: timedelta = timedelta(minutes=10)) -> None:
    """Pega fuso errado (ex.: horário de Brasília gravado como UTC = 3 h de diferença)."""
    diferenca = abs(agora_utc() - momento)
    assert diferenca <= tolerancia, f"{momento.isoformat()} está a {diferenca} de agora (tolerância {tolerancia})"


# --------------------------------------------------------------------------
# Espera por condição
# --------------------------------------------------------------------------
def esperar_ate(condicao: Callable[[], Any], descricao: str, *, timeout: float | None = None,
                intervalo: float = 0.5, detalhe: Callable[[], str] | None = None) -> Any:
    limite = time.monotonic() + (ESPERA_MAX if timeout is None else timeout)
    while True:
        resultado = condicao()
        if resultado:
            return resultado
        if time.monotonic() >= limite:
            extra = f" ({detalhe()})" if detalhe else ""
            raise AssertionError(f"{descricao} não ocorreu em {ESPERA_MAX if timeout is None else timeout} s{extra}")
        time.sleep(intervalo)  # intervalo de polling, não espera fixa pelo resultado


# --------------------------------------------------------------------------
# Leitura de extrato
# --------------------------------------------------------------------------
def ler_extrato(api: ApiContas, conta_id: str, **params: Any) -> Extrato:
    r = api.extrato(conta_id, **params)
    assert r.status_code == 200, f"GET extrato devolveu {r.status_code}: {r.text[:300]}"
    return Extrato.model_validate(r.json())


def percorrer_extrato(api: ApiContas, conta_id: str, *, tamanho: int = 100, max_paginas: int = 50,
                      **filtros: Any) -> Iterator[Extrato]:
    """Entrega página a página. Cursor que não termina em `max_paginas` é defeito (ou conta enorme)."""
    cursor: str | None = None
    for _ in range(max_paginas):
        pagina = ler_extrato(api, conta_id, tamanho=tamanho, pagina=cursor, **filtros)
        yield pagina
        if pagina.proximaPagina is None:
            return
        cursor = pagina.proximaPagina
    raise AssertionError(f"proximaPagina não chegou a null em {max_paginas} páginas de {tamanho}")


def todos_lancamentos(api: ApiContas, conta_id: str, **kwargs: Any) -> list[Lancamento]:
    return [item for pagina in percorrer_extrato(api, conta_id, **kwargs) for item in pagina.lancamentos]


def lancamentos_com(api: ApiContas, conta_id: str, marcador: str, **filtros: Any) -> list[Lancamento]:
    """Todos os lançamentos cuja descrição contém o marcador (varre todas as páginas)."""
    return [item for item in todos_lancamentos(api, conta_id, **filtros) if marcador in item.descricao]


def primeiro_lancamento_com(api: ApiContas, conta_id: str, marcador: str, **filtros: Any) -> Lancamento | None:
    for pagina in percorrer_extrato(api, conta_id, **filtros):
        for item in pagina.lancamentos:
            if marcador in item.descricao:
                return item
    return None


def saldo_de(api: ApiContas, conta_id: str) -> Decimal:
    return dinheiro(ler_extrato(api, conta_id, tamanho=1).saldo)


def saldos(origem: Origem) -> Saldos:
    return Saldos(saldo_de(origem.de.api, origem.de.id), saldo_de(origem.para.api, origem.para.id))


def debitado_hoje(conta: Conta) -> Decimal:
    """Soma dos débitos do dia local no extrato. Aproximação do limite já consumido: supõe que todo
    débito conta para o limite diário e que o "dia" é o de `API_FUSO` (perguntas em aberto)."""
    hoje = hoje_local()
    return sum((abs(dinheiro(item.valor)) for item in todos_lancamentos(conta.api, conta.id)
                if item.tipo == "DEBITO" and data_local(item.data) == hoje), Decimal("0.00"))


# --------------------------------------------------------------------------
# Transferências e prova de efeito / ausência de efeito
# --------------------------------------------------------------------------
def corpo_transferencia(origem: Origem, valor: Any, descricao: Any = None, **sobrescritas: Any) -> dict:
    if isinstance(valor, Decimal):
        valor = moeda(valor)
    corpo: dict[str, Any] = {"contaOrigemId": origem.de.id, "chaveDestino": origem.para.chave_pix, "valor": valor}
    if descricao is not None:
        corpo["descricao"] = descricao
    return {**corpo, **sobrescritas}


def aguardar_lancamento(conta: Conta, marcador: str, **filtros: Any) -> Lancamento:
    return esperar_ate(lambda: primeiro_lancamento_com(conta.api, conta.id, marcador, **filtros),
                       f"lançamento '{marcador}' no extrato da conta {conta.rotulo}")


def aguardar_saldo(conta: Conta, esperado: Decimal) -> None:
    visto: dict[str, Decimal] = {}

    def confere() -> bool:
        visto["saldo"] = saldo_de(conta.api, conta.id)
        return visto["saldo"] == esperado

    esperar_ate(confere, f"saldo da conta {conta.rotulo} chegar a {esperado}",
                detalhe=lambda: f"último saldo observado: {visto.get('saldo')}")


def aguardar_efeito(origem: Origem, antes: Saldos, valor: Decimal, marcador: str) -> Lancamento:
    """Espera o débito no extrato da origem e confere os dois saldos contra a aritmética (antes ∓ valor)."""
    lancamento = aguardar_lancamento(origem.de, marcador)
    aguardar_saldo(origem.de, antes.origem - valor)
    aguardar_saldo(origem.para, antes.destino + valor)
    return lancamento


def enviar_marco(origem: Origem, antes: Saldos) -> Saldos:
    """Transferência válida de R$ 0,01, esperada até aparecer: marco temporal para provar ausências."""
    marcador = novo_marcador()
    r = origem.de.api.transferir(corpo_transferencia(origem, CENTAVO, descricao_com(marcador, "marco")))
    assert r.status_code == 201, (f"marco recusado ({r.status_code}): {r.text[:300]} - sem um marco válido não "
                                  f"dá para provar ausência de efeito (setup/ambiente, não a regra testada)")
    aguardar_efeito(origem, antes, CENTAVO, marcador)
    return antes.apos(CENTAVO)


def assert_sem_efeito(origem: Origem, antes: Saldos, *marcadores: str) -> None:
    """A requisição recusada não mexeu em nada: depois de um marco válido, os dois saldos só variaram
    pelo marco e nenhum lançamento carrega os marcadores das requisições recusadas."""
    enviar_marco(origem, antes)
    for marcador in marcadores:
        achados = lancamentos_com(origem.de.api, origem.de.id, marcador)
        assert achados == [], f"requisição recusada deixou lançamento(s) no extrato: {achados}"


# --------------------------------------------------------------------------
# Asserções de resposta
# --------------------------------------------------------------------------
_RASTROS_TECNICOS = ("traceback", "stacktrace", "stack trace", "sqlstate", "java.lang", "nullpointer", "at org.")
_CAMPOS_SENSIVEIS = ("cpf", "cnpj", "senha", "password", "token", "secret", "hash")


def assert_sem_vazamento_tecnico(texto: str) -> None:
    minusculo = texto.lower()
    for rastro in _RASTROS_TECNICOS:
        assert rastro not in minusculo, f"resposta expõe detalhe interno ({rastro!r}): {texto[:200]}"


def assert_sem_dado_sensivel(corpo: Any, caminho: str = "$") -> None:
    if isinstance(corpo, dict):
        for chave, valor in corpo.items():
            assert not any(parte in chave.lower() for parte in _CAMPOS_SENSIVEIS), \
                f"campo possivelmente sensível exposto em {caminho}.{chave}"
            assert_sem_dado_sensivel(valor, f"{caminho}.{chave}")
    elif isinstance(corpo, list):
        for indice, item in enumerate(corpo):
            assert_sem_dado_sensivel(item, f"{caminho}[{indice}]")


def assert_problema(resposta: requests.Response, status: int) -> Problema:
    """Erro no formato do contrato: status exato, application/problem+json, sem rastro técnico.
    O texto de `title`/`detail` não é conferido (muda com revisão e tradução)."""
    assert resposta.status_code == status, f"esperava {status}, veio {resposta.status_code}: {resposta.text[:300]}"
    tipo = resposta.headers.get("Content-Type", "").split(";")[0].strip().lower()
    assert tipo == "application/problem+json", f"Content-Type do erro: {tipo!r}"
    problema = Problema.model_validate(resposta.json())
    assert problema.status in (None, status), f"`status` do corpo ({problema.status}) difere do HTTP ({status})"
    assert_sem_vazamento_tecnico(resposta.text)
    return problema


def assert_recusada(resposta: requests.Response, aceitos: tuple[int, ...] = (400, 422)) -> None:
    """Para entradas inválidas cujo status o contrato não fixa: tem de ser recusa do cliente, nunca 2xx/5xx."""
    assert resposta.status_code in aceitos, \
        f"esperava recusa {aceitos}, veio {resposta.status_code}: {resposta.text[:300]}"
    assert_sem_vazamento_tecnico(resposta.text)


def chaves_do_corpo(resposta: requests.Response) -> list[str] | None:
    try:
        corpo = resposta.json()
    except ValueError:
        return None
    return sorted(corpo) if isinstance(corpo, dict) else None


# --------------------------------------------------------------------------
# Escolha de origem por saldo (a regra de saldo e a de limite são excludentes numa só conta)
# --------------------------------------------------------------------------
def escolher_origem(origens: list[Origem], condicao: Callable[[Decimal], bool],
                    requisito: str) -> tuple[Origem, Saldos]:
    observados = []
    for origem in origens:
        antes = saldos(origem)
        if condicao(antes.origem):
            return origem, antes
        observados.append(f"{origem.de.rotulo}={antes.origem}")
    pytest.skip(f"nenhuma conta atende ao pré-requisito ({requisito}); saldos: {', '.join(observados)}")
