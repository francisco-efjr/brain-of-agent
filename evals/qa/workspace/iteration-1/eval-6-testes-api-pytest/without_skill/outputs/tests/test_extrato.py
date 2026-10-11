"""GET /contas/{contaId}/extrato

Somente leitura: pode rodar quantas vezes quiser (não move dinheiro).
Convenção: o teste afirma o que o OpenAPI diz; o que o OpenAPI não diz leva @pytest.mark.premissa.
"""
import uuid

import pytest

from cliente import SEM_AUTENTICACAO, detalhe, extrato, percorrer_extrato
from contratos import (
    corpo_json,
    nao_vaza_dados_da_conta,
    parse_data_hora,
    tipo_de_conteudo,
    validar_extrato,
    validar_problema,
)


# --------------------------------------------------------------------------- #
# 200: contrato e paginação
# --------------------------------------------------------------------------- #
@pytest.mark.contrato
def test_titular_le_o_proprio_extrato_e_a_resposta_cumpre_o_contrato(titular):
    api, conta = titular
    resp = extrato(api, conta)

    assert resp.status_code == 200, detalhe(resp)
    assert tipo_de_conteudo(resp) == "application/json", tipo_de_conteudo(resp)
    validar_extrato(corpo_json(resp), conta)


def test_tamanho_padrao_e_20(api_a, conta_a):
    corpo = corpo_json(extrato(api_a, conta_a))

    assert len(corpo["lancamentos"]) <= 20
    # Se há próxima página, a atual precisa estar cheia. Com menos de 21 lançamentos na conta
    # de teste este teste só prova o "<= 20": coloque mais massa na conta para cobrir de fato.
    if corpo["proximaPagina"] is not None:
        assert len(corpo["lancamentos"]) == 20


@pytest.mark.parametrize("tamanho", [1, 100])
def test_tamanho_nos_limites_do_intervalo_e_aceito(api_a, conta_a, tamanho):
    resp = extrato(api_a, conta_a, tamanho=tamanho)

    assert resp.status_code == 200, detalhe(resp)
    corpo = corpo_json(resp)
    validar_extrato(corpo, conta_a)
    assert len(corpo["lancamentos"]) <= tamanho


@pytest.mark.parametrize("tamanho", ["0", "-1", "101", "1000", "abc", "1.5"], ids=lambda t: f"tamanho={t}")
def test_tamanho_fora_do_intervalo_ou_nao_inteiro_retorna_400(api_a, conta_a, tamanho):
    validar_problema(extrato(api_a, conta_a, tamanho=tamanho), 400)


@pytest.mark.parametrize("pagina_tamanho", [1, 3])
def test_paginacao_segue_proximaPagina_sem_repetir_nem_estourar_o_tamanho(api_a, conta_a, pagina_tamanho):
    paginas = list(percorrer_extrato(api_a, conta_a, tamanho=pagina_tamanho, max_paginas=4))
    if len(paginas) < 2:
        pytest.skip(f"a conta A tem no máximo {pagina_tamanho} lançamento(s): não dá para exercitar a paginação")

    ids = []
    for pagina in paginas:
        validar_extrato(pagina, conta_a)
        assert len(pagina["lancamentos"]) <= pagina_tamanho
        ids += [lanc["id"] for lanc in pagina["lancamentos"]]
    assert len(ids) == len(set(ids)), "o mesmo lançamento apareceu em mais de uma página"


@pytest.mark.premissa
def test_pagina_com_cursor_invalido_retorna_400(api_a, conta_a):
    # O spec diz 400 para "parâmetros inválidos"; um cursor inventado é um parâmetro inválido.
    validar_problema(extrato(api_a, conta_a, pagina="cursor-que-nao-existe-" + uuid.uuid4().hex), 400)


# --------------------------------------------------------------------------- #
# Filtros de período (desde / ate)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "parametro,valor",
    [
        ("desde", "2025-13-01"),   # mês 13
        ("desde", "2025-02-30"),   # dia inexistente
        ("desde", "ontem"),
        ("ate", "01/02/2025"),     # formato diferente de YYYY-MM-DD
        ("ate", "2025-1-5"),
    ],
    ids=lambda v: str(v),
)
def test_data_invalida_retorna_400(api_a, conta_a, parametro, valor):
    validar_problema(extrato(api_a, conta_a, **{parametro: valor}), 400)


def test_periodo_sem_lancamentos_devolve_lista_vazia(api_a, conta_a):
    resp = extrato(api_a, conta_a, desde="1990-01-01", ate="1990-01-31")

    assert resp.status_code == 200, detalhe(resp)
    corpo = corpo_json(resp)
    validar_extrato(corpo, conta_a)
    assert corpo["lancamentos"] == []
    assert corpo["proximaPagina"] is None


@pytest.mark.premissa
def test_periodo_invertido_retorna_400(api_a, conta_a):
    # desde > ate: o spec não fala, mas devolver 200 vazio esconderia erro do cliente.
    validar_problema(extrato(api_a, conta_a, desde="2025-02-01", ate="2025-01-01"), 400)


@pytest.mark.premissa
def test_filtro_desde_ate_devolve_apenas_lancamentos_do_dia_pedido(titular):
    """Pega a data de um lançamento real e filtra por ela (desde = ate = esse dia).

    Premissas: ambos os limites são inclusivos. A tolerância de +-1 dia existe porque o spec
    não diz em que fuso o "dia" é calculado; com o fuso definido, aperte para 0.
    """
    api, conta = titular
    lancamentos = corpo_json(extrato(api, conta, tamanho=100))["lancamentos"]
    if not lancamentos:
        pytest.skip("conta sem lançamentos: não há data real para filtrar")
    dia = parse_data_hora(lancamentos[0]["data"]).date()

    resp = extrato(api, conta, desde=dia.isoformat(), ate=dia.isoformat(), tamanho=100)

    assert resp.status_code == 200, detalhe(resp)
    filtrados = corpo_json(resp)["lancamentos"]
    assert filtrados, f"o lançamento de {dia} sumiu ao filtrar por esse mesmo dia (limites inclusivos?)"
    for lanc in filtrados:
        distancia = abs((parse_data_hora(lanc["data"]).date() - dia).days)
        assert distancia <= 1, f"lançamento {lanc['id']} de {lanc['data']} fora do período {dia}"


# --------------------------------------------------------------------------- #
# Segurança: autenticação e acesso à conta de outro titular
# --------------------------------------------------------------------------- #
@pytest.mark.seguranca
@pytest.mark.parametrize("cabecalhos", list(SEM_AUTENTICACAO.values()), ids=list(SEM_AUTENTICACAO))
def test_sem_credencial_valida_retorna_401_sem_dados(api_a, conta_a, cabecalhos):
    resp = extrato(api_a, conta_a, token=None, headers=cabecalhos)

    assert resp.status_code == 401, detalhe(resp)
    nao_vaza_dados_da_conta(resp)


@pytest.mark.seguranca
def test_token_adulterado_retorna_401(api_a, conta_a):
    token = api_a.token
    adulterado = token[:-1] + ("A" if token[-1] != "A" else "B")  # quebra a assinatura/valor

    resp = extrato(api_a, conta_a, token=adulterado)

    assert resp.status_code == 401, detalhe(resp)


@pytest.mark.seguranca
def test_extrato_de_conta_de_outro_titular_retorna_404_sem_dados(cruzamento):
    # O spec manda 404 (e não 403) para "conta de outro titular": não confirma que a conta existe.
    intruso, conta_da_vitima = cruzamento

    resp = extrato(intruso, conta_da_vitima)

    assert resp.status_code == 404, detalhe(resp)
    nao_vaza_dados_da_conta(resp)


@pytest.mark.seguranca
def test_conta_inexistente_e_conta_alheia_sao_indistinguiveis(api_a, conta_b):
    inexistente = extrato(api_a, str(uuid.uuid4()))
    alheia = extrato(api_a, conta_b)

    assert inexistente.status_code == 404, detalhe(inexistente)
    assert alheia.status_code == inexistente.status_code, (
        "status diferente para conta alheia e inexistente permite descobrir quais contas existem"
    )
    assert tipo_de_conteudo(alheia) == tipo_de_conteudo(inexistente)


@pytest.mark.seguranca
@pytest.mark.premissa
@pytest.mark.parametrize("conta_id", ["nao-e-uuid", "1'%20OR%20'1'='1", "%00"], ids=["texto", "sql", "nulo"])
def test_contaId_malformado_e_rejeitado_sem_erro_de_servidor(api_a, conta_id):
    # O spec lista 400 (parâmetros inválidos) e 404; aceitamos qualquer um dos dois, nunca 5xx.
    resp = api_a.get(f"/contas/{conta_id}/extrato")

    assert resp.status_code in (400, 404), detalhe(resp)
    nao_vaza_dados_da_conta(resp)
