"""Validadores de contrato: conferem as respostas contra os schemas do OpenAPI (v1.4.0).

São asserts escritos à mão, com mensagem que aponta o campo e o valor, em vez de um
validador genérico de JSON Schema: o `nullable` do OpenAPI 3.0 e os `format` não são
JSON Schema puro e geram falsos positivos/negativos. Se o contrato mudar, ajuste aqui.
Campos extras na resposta são tolerados (additionalProperties não é proibido no spec).
"""
from __future__ import annotations

import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

from cliente import RE_UUID, detalhe

RE_VALOR = re.compile(r"^-?\d+\.\d{2}$")  # Lancamento.valor e Extrato.saldo
RE_DATA_HORA = re.compile(r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:\d{2})$")

TIPOS_LANCAMENTO = {"CREDITO", "DEBITO"}
STATUS_TRANSFERENCIA = {"PROCESSANDO", "CONCLUIDA", "RECUSADA"}
VAZAMENTOS_EM_ERRO = ("Traceback", "SQLSTATE", "NullPointerException", "at java.", "node_modules")


def tipo_de_conteudo(resp) -> str:
    return resp.headers.get("Content-Type", "").split(";")[0].strip().lower()


def corpo_json(resp):
    try:
        return resp.json()
    except ValueError:
        raise AssertionError(f"corpo não é JSON válido: {detalhe(resp)}") from None


def parse_data_hora(texto: str) -> datetime:
    """RFC 3339 -> datetime com fuso. Normaliza 'Z' e frações de segundo (compatível com Python 3.9+)."""
    t = texto.upper().replace("Z", "+00:00")
    t = re.sub(r"\.(\d+)", lambda m: "." + (m.group(1) + "000000")[:6], t)
    return datetime.fromisoformat(t)


def _uuid(valor, campo: str):
    assert isinstance(valor, str) and RE_UUID.match(valor), f"{campo} deveria ser UUID, veio {valor!r}"


def _data_hora(valor, campo: str):
    assert isinstance(valor, str) and RE_DATA_HORA.match(valor), f"{campo} deveria ser date-time, veio {valor!r}"
    try:
        return parse_data_hora(valor)
    except ValueError:
        raise AssertionError(f"{campo} não é uma data/hora válida: {valor!r}") from None


def _exigir_campos(obj, obrigatorios, nome: str):
    assert isinstance(obj, dict), f"{nome} deveria ser objeto JSON, veio {type(obj).__name__}"
    faltando = [c for c in obrigatorios if c not in obj]
    assert not faltando, f"{nome}: faltam campos obrigatórios {faltando}; veio {sorted(obj)}"


def validar_lancamento(lanc) -> None:
    _exigir_campos(lanc, ("id", "data", "descricao", "valor", "tipo"), "Lancamento")
    _uuid(lanc["id"], "Lancamento.id")
    _data_hora(lanc["data"], "Lancamento.data")
    assert isinstance(lanc["descricao"], str), "Lancamento.descricao deveria ser string"
    assert len(lanc["descricao"]) <= 140, f"Lancamento.descricao passa de 140 caracteres ({len(lanc['descricao'])})"
    assert isinstance(lanc["valor"], str) and RE_VALOR.match(lanc["valor"]), (
        f"Lancamento.valor deveria ser string '^-?\\d+\\.\\d{{2}}$' (nunca número JSON), veio {lanc['valor']!r}"
    )
    assert lanc["tipo"] in TIPOS_LANCAMENTO, f"Lancamento.tipo fora do enum: {lanc['tipo']!r}"


def validar_extrato(corpo, conta_id: str | None = None) -> None:
    _exigir_campos(corpo, ("contaId", "saldo", "lancamentos", "proximaPagina"), "Extrato")
    _uuid(corpo["contaId"], "Extrato.contaId")
    if conta_id is not None:
        assert corpo["contaId"].lower() == conta_id.lower(), (
            f"Extrato.contaId ({corpo['contaId']}) difere da conta consultada ({conta_id})"
        )
    assert isinstance(corpo["saldo"], str) and RE_VALOR.match(corpo["saldo"]), (
        f"Extrato.saldo deveria ser string com 2 casas, veio {corpo['saldo']!r}"
    )
    assert isinstance(corpo["lancamentos"], list), "Extrato.lancamentos deveria ser array"
    for lanc in corpo["lancamentos"]:
        validar_lancamento(lanc)
    prox = corpo["proximaPagina"]
    assert prox is None or (isinstance(prox, str) and prox != ""), (
        f"Extrato.proximaPagina deveria ser null ou string não vazia, veio {prox!r}"
    )


def validar_transferencia(corpo) -> None:
    _exigir_campos(corpo, ("id", "status", "valor", "criadaEm"), "Transferencia")
    _uuid(corpo["id"], "Transferencia.id")
    assert corpo["status"] in STATUS_TRANSFERENCIA, f"Transferencia.status fora do enum: {corpo['status']!r}"
    # O spec não define pattern para Transferencia.valor; exigimos string decimal (não número JSON).
    assert isinstance(corpo["valor"], str), f"Transferencia.valor deveria ser string, veio {corpo['valor']!r}"
    try:
        Decimal(corpo["valor"])
    except InvalidOperation:
        raise AssertionError(f"Transferencia.valor não é decimal: {corpo['valor']!r}") from None
    _data_hora(corpo["criadaEm"], "Transferencia.criadaEm")


def validar_problema(resp, status_esperado: int) -> dict:
    """Erro no formato Problema (RFC 7807) com o status HTTP esperado. Devolve o corpo."""
    assert resp.status_code == status_esperado, f"esperava HTTP {status_esperado}: {detalhe(resp)}"
    assert tipo_de_conteudo(resp) == "application/problem+json", (
        f"Content-Type de erro deveria ser application/problem+json, veio {tipo_de_conteudo(resp)!r}"
    )
    corpo = corpo_json(resp)
    assert isinstance(corpo, dict), "corpo de erro deveria ser objeto JSON"
    for campo in ("type", "title", "detail"):
        assert campo not in corpo or isinstance(corpo[campo], str), f"Problema.{campo} deveria ser string"
    if "status" in corpo:
        assert corpo["status"] == status_esperado, (
            f"Problema.status ({corpo['status']!r}) diverge do status HTTP ({status_esperado})"
        )
    nao_vazar_detalhes_internos(resp)
    return corpo


def nao_vazar_detalhes_internos(resp) -> None:
    for marca in VAZAMENTOS_EM_ERRO:
        assert marca not in resp.text, f"resposta de erro expõe detalhe interno ({marca!r}): {detalhe(resp)}"


def nao_vaza_dados_da_conta(resp) -> None:
    """Erros 401/404 não podem trazer dados de extrato."""
    texto = resp.text.lower()
    for campo in ("saldo", "lancamentos"):
        assert campo not in texto, f"resposta {resp.status_code} contém {campo!r}: {detalhe(resp)}"
    nao_vazar_detalhes_internos(resp)
