"""Testes que movem valores altos ou consomem o limite diário. Ficam DESLIGADOS por padrão.

Para ligar: `RUN_TESTES_DESTRUTIVOS=1 pytest -m destrutivo` (o conftest já os executa por último).

Por que existem: são os limites do dinheiro no contrato (limite diário de R$ 5.000,00 acumulado,
"máximo = saldo disponível") e a corrida de saldo. Por que são perigosos:
* consomem o limite diário da conta de origem até a virada do dia (outras transferências do dia falham);
* se houver defeito, valores de até R$ 5.000,00 saem da conta de teste;
* com `CHAVE_PIX_A` configurada, devolvem o que moveram (B->A, melhor esforço); sem ela, A fica
  desfalcada e alguém precisa recompor o saldo.

Ordem e limite diário: os testes rodam na ordem do arquivo e cada um consome parte do limite diário da
conta de origem (a devolução não o restaura). O último, de limite acumulado, usa tudo o que restar. Teste
cujo pré-requisito não for atendido é PULADO com o motivo (veja `-rs`), nunca aprovado em silêncio.

Suposição que sustenta o limite acumulado: o limite já consumido hoje = soma dos débitos do dia
(fuso API_FUSO) no extrato. Se a regra real contar outra coisa, o cálculo de `restante` precisa mudar.
"""
from __future__ import annotations

import threading
import warnings
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from decimal import ROUND_DOWN, Decimal

import pytest

from tests.support import (CENTAVO, FUSO, LIMITE_DIARIO, Origem, aguardar_efeito, assert_problema,
                           corpo_transferencia, debitado_hoje, descricao_com, enviar_marco, lancamentos_com,
                           novo_marcador, saldo_de, saldos)

pytestmark = pytest.mark.destrutivo


def _longe_da_meia_noite():
    # o "dia" do limite vira à meia-noite do fuso; cruzar a virada no meio do teste invalida o oráculo
    agora = datetime.now(tz=FUSO)
    minutos = agora.hour * 60 + agora.minute
    if minutos >= 23 * 60 + 57 or minutos <= 3:
        pytest.skip("muito perto da meia-noite: o limite diário pode zerar no meio do teste")


def _escolher(origens: list[Origem], aceita, requisito: str):
    """Primeira origem cuja (saldo, restante do limite) satisfaz `aceita`; senão pula o teste."""
    observados = []
    for origem in origens:
        antes = saldos(origem)
        restante = LIMITE_DIARIO - debitado_hoje(origem.de)
        if aceita(origem, antes.origem, restante):
            return origem, antes, restante
        observados.append(f"{origem.de.rotulo}: saldo={antes.origem} restante_do_limite={restante}")
    pytest.skip(f"nenhuma conta atende ({requisito}); {'; '.join(observados)}")


def _devolver(origem: Origem, valor: Decimal) -> None:
    """Melhor esforço: devolve `valor` do destino para a origem e espera assentar (os testes seguintes leem
    saldo e limite do extrato). Nunca levanta: roda em finally e não pode mascarar a falha original."""
    if valor <= 0:
        return
    inversa = origem.inversa()
    if inversa is None:
        warnings.warn(f"sem CHAVE_PIX_A: R$ {valor} ficaram na conta {origem.para.rotulo}; "
                      f"recomponha o saldo da conta {origem.de.rotulo}")
        return
    try:
        antes, marcador = saldos(inversa), novo_marcador()
        r = inversa.de.api.transferir(corpo_transferencia(inversa, valor, descricao_com(marcador, "devolucao qa")))
        if r.status_code != 201:
            warnings.warn(f"devolução de R$ {valor} falhou ({r.status_code}): confira os saldos manualmente")
            return
        aguardar_efeito(inversa, antes, valor, marcador)
    except Exception as erro:  # noqa: BLE001
        warnings.warn(f"devolução de R$ {valor} não confirmada ({erro!r}): confira os saldos manualmente")


def _assert_sem_debito(origem: Origem, saldo_origem_esperado: Decimal, *marcadores: str) -> None:
    """Prova de ausência quando a origem não pode mais transferir (limite ou saldo esgotado): o marco sai
    da direção inversa, que credita a origem. Sem CHAVE_PIX_A, só a conferência imediata é possível."""
    assert saldo_de(origem.de.api, origem.de.id) == saldo_origem_esperado
    inversa = origem.inversa()
    if inversa is not None:
        antes = saldos(inversa)
        assert antes.destino == saldo_origem_esperado
        enviar_marco(inversa, antes)
    for marcador in marcadores:
        assert lancamentos_com(origem.de.api, origem.de.id, marcador) == [], \
            "a transferência recusada deixou lançamento no extrato"


def test_valor_igual_ao_saldo_e_aceito_e_o_centavo_seguinte_e_recusado(origens):
    _longe_da_meia_noite()
    origem, antes, restante = _escolher(
        [o for o in origens if o.inversa()],  # precisa poder devolver
        lambda o, saldo, restante: Decimal("0.01") <= saldo <= restante,
        "saldo entre R$ 0,01 e o restante do limite diário, com CHAVE_PIX_A para devolver")
    m1, m2 = novo_marcador(), novo_marcador()
    tudo = antes.origem  # "máximo = saldo disponível"
    movido = Decimal("0.00")
    try:
        r1 = origem.de.api.transferir(corpo_transferencia(origem, tudo, descricao_com(m1, "saldo inteiro")))
        assert r1.status_code == 201, f"transferir exatamente o saldo (R$ {tudo}) foi recusado: {r1.text[:300]}"
        movido += tudo
        aguardar_efeito(origem, antes, tudo, m1)  # saldo da origem chega a 0.00

        r2 = origem.de.api.transferir(corpo_transferencia(origem, CENTAVO, descricao_com(m2, "um centavo a mais")))
        assert_problema(r2, 422)
        _assert_sem_debito(origem, Decimal("0.00"), m2)
    finally:
        _devolver(origem, movido)


def test_dois_debitos_simultaneos_que_juntos_excedem_o_saldo_aprovam_so_um(origens):
    _longe_da_meia_noite()

    def valor_da_disputa(saldo: Decimal) -> Decimal:
        return (saldo / 2).quantize(CENTAVO, rounding=ROUND_DOWN) + CENTAVO  # cada um cabe; os dois juntos não

    origem, antes, _ = _escolher(
        origens, lambda o, saldo, restante: saldo >= Decimal("0.02") and valor_da_disputa(saldo) <= restante,
        "saldo >= R$ 0,02 e metade do saldo dentro do limite diário restante")
    valor, marcador = valor_da_disputa(antes.origem), novo_marcador()
    corpo = corpo_transferencia(origem, valor, descricao_com(marcador, "corrida de saldo"))
    largada = threading.Barrier(2)

    def disparar(_):
        cliente = origem.de.api.novo()
        largada.wait(timeout=10)
        return cliente.transferir(corpo)  # Idempotency-Key diferente em cada chamada

    with ThreadPoolExecutor(max_workers=2) as pool:
        respostas = list(pool.map(disparar, range(2)))

    status = sorted(r.status_code for r in respostas)
    movido = valor * sum(1 for codigo in status if codigo == 201)
    try:
        assert status == [201, 422], f"esperava um aprovado e um recusado, veio {status}"
        assert_problema(next(r for r in respostas if r.status_code == 422), 422)
        aguardar_efeito(origem, antes, valor, marcador)
        _assert_sem_debito(origem, antes.origem - valor)
        assert len(lancamentos_com(origem.de.api, origem.de.id, marcador)) == 1
    finally:
        _devolver(origem, movido)


def test_limite_diario_acumulado_aceita_ate_5000_00_e_recusa_o_centavo_seguinte(origens):
    _longe_da_meia_noite()
    origem, antes, restante = _escolher(
        origens, lambda o, saldo, restante: restante >= Decimal("0.03") and saldo >= restante,
        "saldo >= restante do limite diário, e restante >= R$ 0,03")
    m1, m2, m3 = novo_marcador(), novo_marcador(), novo_marcador()
    primeiro = restante - CENTAVO  # deixa exatamente R$ 0,01 de limite
    movido = Decimal("0.00")
    try:
        r1 = origem.de.api.transferir(corpo_transferencia(origem, primeiro, descricao_com(m1, "limite 1/3")))
        assert r1.status_code == 201, f"R$ {primeiro} (abaixo do limite) recusado: {r1.text[:300]}"
        movido += primeiro
        aguardar_efeito(origem, antes, primeiro, m1)

        r2 = origem.de.api.transferir(corpo_transferencia(origem, CENTAVO, descricao_com(m2, "limite 2/3")))
        assert r2.status_code == 201, f"acumulado de exatamente R$ 5.000,00 deve ser aceito: {r2.text[:300]}"
        movido += CENTAVO
        aguardar_efeito(origem, antes.apos(primeiro), CENTAVO, m2)

        r3 = origem.de.api.transferir(corpo_transferencia(origem, CENTAVO, descricao_com(m3, "limite 3/3")))
        assert_problema(r3, 422)  # acumulado de R$ 5.000,01
        _assert_sem_debito(origem, antes.origem - restante, m3)
    finally:
        _devolver(origem, movido)
