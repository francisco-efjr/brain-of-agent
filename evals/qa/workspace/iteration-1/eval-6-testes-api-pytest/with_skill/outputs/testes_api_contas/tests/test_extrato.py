"""GET /contas/{contaId}/extrato

Prioridade pelo risco: (1) isolamento entre titulares (dado financeiro de terceiro), (2) contrato de
dinheiro e paginação (extrato errado engana o cliente), (3) validação de parâmetros.

Testes marcados com `inferido` verificam um comportamento que o contrato não escreve (status exato
de um caso omisso, header de cache, fuso do filtro de datas). Se o time decidir outra coisa, ajuste a
asserção; para rodar só o que está literalmente no contrato: `pytest -m "not inferido"`.
"""
from __future__ import annotations

import uuid
from datetime import date, timedelta

import pytest

from tests.support import (CENTAVO, TAMANHO_PADRAO, Extrato, assert_problema, assert_sem_dado_sensivel,
                           aguardar_efeito, chaves_do_corpo, corpo_transferencia, data_local,
                           descricao_com, lancamentos_com, ler_extrato, novo_marcador,
                           percorrer_extrato, saldos, todos_lancamentos)


# --------------------------------------------------------------------------
# Contrato do caso feliz
# --------------------------------------------------------------------------
def test_titular_le_o_proprio_extrato_conforme_o_contrato(api_a, conta_a):
    r = api_a.extrato(conta_a.id)

    assert r.status_code == 200, r.text
    assert r.headers["Content-Type"].startswith("application/json")
    extrato = Extrato.model_validate(r.json())  # tipos, formato do dinheiro (2 casas), enum, descrição <= 140
    assert extrato.contaId == uuid.UUID(conta_a.id)
    assert len(extrato.lancamentos) <= TAMANHO_PADRAO
    assert_sem_dado_sensivel(r.json())


@pytest.mark.inferido
def test_extrato_nao_pode_ficar_em_cache(api_a, conta_a):
    # dado financeiro pessoal: o contrato não diz, mas cache de proxy/navegador expõe o saldo a terceiros
    r = api_a.extrato(conta_a.id)
    assert "no-store" in r.headers.get("Cache-Control", "").lower()


# --------------------------------------------------------------------------
# Autenticação e isolamento entre titulares
# --------------------------------------------------------------------------
@pytest.mark.parametrize("cenario", ["sem_token", "token_invalido"])
def test_extrato_sem_credencial_valida_retorna_401_sem_dados(clientes_sem_credencial, conta_a, cenario):
    r = clientes_sem_credencial[cenario].extrato(conta_a.id)

    assert r.status_code == 401
    assert not ({"saldo", "lancamentos"} & set(chaves_do_corpo(r) or []))


@pytest.mark.parametrize("quem_pede", ["b_pede_conta_de_a", "a_pede_conta_de_b"])
def test_extrato_de_conta_de_outro_titular_e_indistinguivel_de_conta_inexistente(
        api_a, api_b, conta_a, conta_b, quem_pede):
    cliente, conta_alheia = (api_b, conta_a) if quem_pede == "b_pede_conta_de_a" else (api_a, conta_b)

    alheia = cliente.extrato(conta_alheia.id)
    inexistente = cliente.extrato(str(uuid.uuid4()))

    assert alheia.status_code == inexistente.status_code == 404
    assert alheia.headers.get("Content-Type") == inexistente.headers.get("Content-Type")
    assert chaves_do_corpo(alheia) == chaves_do_corpo(inexistente)  # nada que revele que a conta existe
    assert not ({"saldo", "lancamentos"} & set(chaves_do_corpo(alheia) or []))


def test_conta_inexistente_retorna_404(api_a):
    assert api_a.extrato(str(uuid.uuid4())).status_code == 404


@pytest.mark.inferido
@pytest.mark.parametrize("conta_id", ["abc", "12345", "' OR 1=1 --", "0" * 36],
                         ids=["texto", "numero", "sentinela_sql", "36_caracteres_sem_formato_uuid"])
def test_conta_id_fora_do_formato_uuid_retorna_400(api_a, conta_id):
    # contrato: contaId é uuid e 400 = "Parâmetros inválidos"; o caso omisso é decidir entre 400 e 404
    assert_problema(api_a.extrato(conta_id), 400)


# --------------------------------------------------------------------------
# Tamanho da página: valor-limite 1..100, padrão 20
# --------------------------------------------------------------------------
@pytest.mark.parametrize("tamanho", [1, 2, 99, 100])
def test_tamanho_valido_e_respeitado(api_a, conta_a, historico_a, tamanho):
    extrato = ler_extrato(api_a, conta_a.id, tamanho=tamanho)

    # a conta tem pelo menos 3 lançamentos (historico_a): 1 e 2 vêm cheios; 99 e 100 vêm no máximo cheios
    assert min(tamanho, 3) <= len(extrato.lancamentos) <= tamanho


@pytest.mark.parametrize("tamanho", [0, -1, 101, 1_000_000_000, "abc", "1.5", "20abc"],
                         ids=["zero", "negativo", "101", "um_bilhao", "texto", "decimal", "numero_com_lixo"])
def test_tamanho_invalido_retorna_400_em_problem_json(api_a, conta_a, tamanho):
    # 0 e 101 são os vizinhos de fora do limite; 10^9 prova que não vira "traga tudo" nem 500
    assert_problema(api_a.extrato(conta_a.id, tamanho=tamanho), 400)


def test_sem_tamanho_a_pagina_tem_20_itens(api_a, conta_a, historico_a):
    padrao = ler_extrato(api_a, conta_a.id)
    maior = ler_extrato(api_a, conta_a.id, tamanho=TAMANHO_PADRAO + 1)  # oráculo: quantos existem até 21

    assert len(padrao.lancamentos) == min(TAMANHO_PADRAO, len(maior.lancamentos))


# --------------------------------------------------------------------------
# Paginação por cursor
# --------------------------------------------------------------------------
def test_paginar_de_um_em_um_reproduz_a_mesma_sequencia_da_pagina_grande(api_a, conta_a, historico_a):
    prefixo = 30  # basta um trecho; extrato de conta antiga é grande
    grande = [item.id for item in ler_extrato(api_a, conta_a.id, tamanho=100).lancamentos][:prefixo]
    assert len(grande) >= 3

    vistos: list[uuid.UUID] = []
    primeira = True
    for pagina in percorrer_extrato(api_a, conta_a.id, tamanho=1, max_paginas=prefixo):
        assert len(pagina.lancamentos) <= 1
        if primeira:
            assert pagina.proximaPagina is not None  # há mais de um lançamento, logo há próxima página
            primeira = False
        vistos += [item.id for item in pagina.lancamentos]
        if len(vistos) >= len(grande) or pagina.proximaPagina is None:
            break

    assert len(set(vistos)) == len(vistos), "lançamento repetido entre páginas"
    assert vistos == grande[:len(vistos)], "ordem ou conteúdo diferem entre tamanho=1 e tamanho=100"
    assert len(vistos) == len(grande)


def test_ultima_pagina_termina_com_proxima_pagina_nula(api_a, conta_a, historico_a):
    # `percorrer_extrato` falha se o cursor nunca chegar a null (laço infinito de cursor)
    paginas = list(percorrer_extrato(api_a, conta_a.id, tamanho=100))

    assert paginas[-1].proximaPagina is None
    assert all(pagina.proximaPagina is not None for pagina in paginas[:-1])


@pytest.mark.inferido
@pytest.mark.parametrize("cursor", ["cursor-adulterado", "AAAA", "' OR 1=1 --"],
                         ids=["texto", "base64_curto", "sentinela_sql"])
def test_cursor_invalido_retorna_400(api_a, conta_a, cursor):
    # contrato: 400 = "Parâmetros inválidos"; cursor adulterado não pode virar 500 nem "primeira página"
    assert_problema(api_a.extrato(conta_a.id, pagina=cursor), 400)


@pytest.mark.inferido
def test_cursor_de_um_titular_nao_serve_a_outro(api_a, api_b, conta_a, conta_b, historico_a):
    cursor = ler_extrato(api_a, conta_a.id, tamanho=1).proximaPagina
    assert cursor, "pré-condição: a conta A tem mais de uma página com tamanho=1"

    r = api_b.extrato(conta_b.id, pagina=cursor)

    # aceitável: 400 (cursor não pertence a esta conta); inaceitável: devolver lançamentos da conta A
    assert r.status_code in (200, 400), r.text
    if r.status_code == 200:
        ids_de_a = {item.id for item in todos_lancamentos(api_a, conta_a.id)}
        assert not ({item.id for item in Extrato.model_validate(r.json()).lancamentos} & ids_de_a)


# --------------------------------------------------------------------------
# Filtros de data (desde / ate): inclusivos nas duas pontas
# --------------------------------------------------------------------------
@pytest.fixture
def lancamento_de_hoje(origem_a):
    """Cria um débito de R$ 0,01 e devolve (marcador, data local do lançamento no fuso do negócio)."""
    antes = saldos(origem_a)
    marcador = novo_marcador()
    r = origem_a.de.api.transferir(corpo_transferencia(origem_a, CENTAVO, descricao_com(marcador, "filtro")))
    assert r.status_code == 201, r.text
    lancamento = aguardar_efeito(origem_a, antes, CENTAVO, marcador)
    return marcador, data_local(lancamento.data)


@pytest.mark.inferido
@pytest.mark.parametrize("filtros, aparece", [
    (lambda d: {"desde": d, "ate": d}, True),
    (lambda d: {"desde": d}, True),
    (lambda d: {"ate": d}, True),
    (lambda d: {"ate": d - timedelta(days=1)}, False),
    (lambda d: {"desde": d + timedelta(days=1)}, False),
], ids=["dia_exato", "so_desde", "so_ate", "ate_na_vespera", "desde_no_dia_seguinte"])
def test_filtro_de_data_inclui_os_dois_extremos(api_a, conta_a, lancamento_de_hoje, filtros, aparece):
    # supõe que o filtro usa o dia no fuso API_FUSO (padrão America/Sao_Paulo); ver perguntas em aberto
    marcador, dia = lancamento_de_hoje
    parametros = {chave: valor.isoformat() for chave, valor in filtros(dia).items()}

    achados = lancamentos_com(api_a, conta_a.id, marcador, **parametros)

    assert (len(achados) == 1) is aparece, f"filtros {parametros}: achados={achados}"


@pytest.mark.parametrize("parametro", ["desde", "ate"])
@pytest.mark.parametrize("valor", ["2026-13-01", "2026-02-30", "2025-02-29", "31/01/2026", "2026-1-5", "ontem"],
                         ids=["mes_13", "30_de_fevereiro", "29_fev_ano_nao_bissexto", "dd_mm_aaaa", "sem_zero", "texto"])
def test_data_invalida_retorna_400(api_a, conta_a, parametro, valor):
    assert_problema(api_a.extrato(conta_a.id, **{parametro: valor}), 400)


def test_data_bissexta_valida_e_aceita(api_a, conta_a):
    extrato = ler_extrato(api_a, conta_a.id, desde="2024-02-29", ate="2024-02-29")

    assert extrato.contaId == uuid.UUID(conta_a.id)
    assert all(data_local(item.data) == date(2024, 2, 29) for item in extrato.lancamentos)
