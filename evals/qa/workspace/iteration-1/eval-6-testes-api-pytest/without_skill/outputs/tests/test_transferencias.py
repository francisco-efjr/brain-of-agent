"""POST /transferencias

ATENÇÃO: os testes marcados `muta_estado` fazem transferências REAIS de R$ 0,01 (algumas de
R$ 0,02) da conta A para a conta B de homologação; não há como desfazer (o spec não tem
estorno nem DELETE). Uma execução completa move poucos centavos. Para rodar só leitura/recusas:

    pytest -m "not muta_estado"

Convenções:
- Valores sempre `Decimal` / string com 2 casas. Nunca float.
- O spec só documenta 422 (regra de negócio), 404, 401 e 201/200. Para entrada malformada
  (campo ausente, formato errado) NÃO há status documentado; aceitamos 400 ou 422
  (ERRO_DE_VALIDACAO) e deixamos a lacuna registrada nas notas.
- Recusas (4xx) não movem dinheiro, mas conferimos o saldo nos casos em que um erro seria grave.
"""
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace

import pytest

from cliente import (
    SEM_AUTENTICACAO,
    corpo_transferencia,
    criar_transferencia,
    detalhe,
    fmt_valor,
    ontem_utc,
    saldo_de,
)
from contratos import (
    corpo_json,
    nao_vaza_dados_da_conta,
    nao_vazar_detalhes_internos,
    parse_data_hora,
    tipo_de_conteudo,
    validar_lancamento,
    validar_problema,
    validar_transferencia,
)

UM_CENTAVO = Decimal("0.01")
LIMITE_DIARIO = Decimal("5000.00")
ERRO_DE_VALIDACAO = (400, 422)


def rejeitada(resp):
    """Pedido recusado por entrada inválida: 400 ou 422, sem vazar detalhes internos."""
    assert resp.status_code in ERRO_DE_VALIDACAO, f"esperava 400 ou 422: {detalhe(resp)}"
    if resp.status_code == 422:
        validar_problema(resp, 422)  # 422 é documentado como application/problem+json
    else:
        nao_vazar_detalhes_internos(resp)


@pytest.fixture(scope="module")
def a_com_saldo(api_a, conta_a):
    saldo = saldo_de(api_a, conta_a)
    if saldo < Decimal("1.00"):
        pytest.skip(f"a conta A precisa de pelo menos R$ 1,00 em homologação para estes testes (tem {saldo})")
    return saldo


@pytest.fixture(scope="module")
def transferencia_efetivada(a_com_saldo, api_a, api_b, conta_a, conta_b, chave_b, espera, run_id):
    """Uma única transferência A -> B de R$ 0,01 com saldos medidos antes/depois.

    Os testes do fluxo feliz compartilham esta transferência para não gastar uma por teste.
    A fixture só mede; quem afirma são os testes (assim cada falha aponta um comportamento só).
    """
    saldo_a_antes = espera.saldo_estavel(api_a, conta_a)
    saldo_b_antes = espera.saldo_estavel(api_b, conta_b)
    marcador = f"autotest {run_id} fluxo-feliz"

    resposta = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b, "0.01", descricao=marcador))

    resultado = SimpleNamespace(
        resposta=resposta,
        marcador=marcador,
        saldo_a_antes=saldo_a_antes,
        saldo_b_antes=saldo_b_antes,
        saldo_a_depois=None,
        saldo_b_depois=None,
    )
    if resposta.status_code == 201:
        resultado.saldo_a_depois = espera.saldo_chegar_a(api_a, conta_a, saldo_a_antes - UM_CENTAVO)
        resultado.saldo_b_depois = espera.saldo_chegar_a(api_b, conta_b, saldo_b_antes + UM_CENTAVO)
    return resultado


# --------------------------------------------------------------------------- #
# Fluxo feliz (201)
# --------------------------------------------------------------------------- #
@pytest.mark.muta_estado
@pytest.mark.contrato
def test_cria_transferencia_201_e_a_resposta_cumpre_o_contrato(transferencia_efetivada):
    resp = transferencia_efetivada.resposta

    assert resp.status_code == 201, detalhe(resp)
    assert tipo_de_conteudo(resp) == "application/json", tipo_de_conteudo(resp)
    corpo = corpo_json(resp)
    validar_transferencia(corpo)
    assert Decimal(corpo["valor"]) == UM_CENTAVO
    assert corpo["status"] != "RECUSADA", "transferência válida e com saldo não deveria nascer RECUSADA"
    # Pega fuso errado (hora local rotulada como UTC): tolerância larga para não depender de relógio de homolog.
    defasagem = abs((datetime.now(timezone.utc) - parse_data_hora(corpo["criadaEm"])).total_seconds())
    assert defasagem < 600, f"criadaEm {corpo['criadaEm']} está a {defasagem:.0f}s de agora"


@pytest.mark.muta_estado
def test_conta_de_origem_e_debitada_exatamente_uma_vez(transferencia_efetivada):
    t = transferencia_efetivada
    assert t.resposta.status_code == 201, f"pré-condição: a transferência não foi criada: {detalhe(t.resposta)}"

    assert t.saldo_a_depois == t.saldo_a_antes - UM_CENTAVO, (
        f"saldo da origem: {t.saldo_a_antes} -> {t.saldo_a_depois}; esperado {t.saldo_a_antes - UM_CENTAVO}"
    )


@pytest.mark.muta_estado
def test_conta_de_destino_e_creditada(transferencia_efetivada):
    t = transferencia_efetivada
    assert t.resposta.status_code == 201, f"pré-condição: a transferência não foi criada: {detalhe(t.resposta)}"

    assert t.saldo_b_depois == t.saldo_b_antes + UM_CENTAVO, (
        f"saldo do destino: {t.saldo_b_antes} -> {t.saldo_b_depois}; esperado {t.saldo_b_antes + UM_CENTAVO}. "
        "CHAVE_PIX_B é mesmo a chave da conta B?"
    )


@pytest.mark.muta_estado
@pytest.mark.premissa
def test_extrato_da_origem_registra_o_debito(transferencia_efetivada, api_a, conta_a, espera):
    # Premissas: a descrição enviada volta intacta no lançamento e o débito aparece no extrato.
    t = transferencia_efetivada
    assert t.resposta.status_code == 201, f"pré-condição: a transferência não foi criada: {detalhe(t.resposta)}"

    lanc = espera.lancamento(api_a, conta_a, lambda l: l["descricao"] == t.marcador, desde=ontem_utc())

    assert lanc is not None, f"lançamento {t.marcador!r} não apareceu no extrato em {espera.timeout}s"
    validar_lancamento(lanc)
    assert lanc["tipo"] == "DEBITO"
    # O spec não diz se o débito vem com sinal ("-0.01") ou positivo; o valor absoluto é o que importa.
    assert abs(Decimal(lanc["valor"])) == UM_CENTAVO


@pytest.mark.muta_estado
def test_descricao_e_opcional(a_com_saldo, api_a, conta_a, chave_b):
    resp = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b))  # só os 3 campos obrigatórios

    assert resp.status_code == 201, detalhe(resp)
    validar_transferencia(corpo_json(resp))


@pytest.mark.muta_estado
def test_descricao_com_exatos_140_caracteres_e_aceita(a_com_saldo, api_a, conta_a, chave_b, run_id):
    descricao = f"autotest {run_id} limite-140 ".ljust(140, "x")
    assert len(descricao) == 140

    resp = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b, descricao=descricao))

    assert resp.status_code == 201, detalhe(resp)


# --------------------------------------------------------------------------- #
# Idempotência (header Idempotency-Key)
# --------------------------------------------------------------------------- #
@pytest.mark.muta_estado
def test_repeticao_com_a_mesma_chave_devolve_200_e_a_transferencia_original(a_com_saldo, api_a, conta_a, chave_b):
    chave = str(uuid.uuid4())
    corpo = corpo_transferencia(conta_a, chave_b)

    primeira = criar_transferencia(api_a, corpo, idem=chave)
    assert primeira.status_code == 201, detalhe(primeira)
    original = corpo_json(primeira)

    repeticao = criar_transferencia(api_a, corpo, idem=chave)

    assert repeticao.status_code == 200, detalhe(repeticao)
    repetida = corpo_json(repeticao)
    validar_transferencia(repetida)
    assert repetida["id"] == original["id"]
    assert Decimal(repetida["valor"]) == Decimal(original["valor"])
    assert repetida["criadaEm"] == original["criadaEm"]  # é a original, não uma nova


@pytest.mark.muta_estado
def test_repeticao_com_a_mesma_chave_nao_debita_de_novo(a_com_saldo, api_a, conta_a, chave_b, espera):
    antes = espera.saldo_estavel(api_a, conta_a)
    esperado = antes - UM_CENTAVO
    chave = str(uuid.uuid4())
    corpo = corpo_transferencia(conta_a, chave_b)
    assert criar_transferencia(api_a, corpo, idem=chave).status_code == 201
    assert espera.saldo_chegar_a(api_a, conta_a, esperado) == esperado, "o débito da 1ª tentativa não apareceu"

    for _ in range(2):
        assert criar_transferencia(api_a, corpo, idem=chave).status_code == 200

    depois = espera.saldo_estavel(api_a, conta_a)
    assert depois == esperado, f"saldo {antes} -> {depois}: repetir a mesma chave debitou mais de uma vez"


@pytest.mark.muta_estado
def test_chaves_diferentes_geram_transferencias_distintas(a_com_saldo, api_a, conta_a, chave_b):
    corpo = corpo_transferencia(conta_a, chave_b)

    primeira = criar_transferencia(api_a, corpo)
    segunda = criar_transferencia(api_a, corpo)

    assert primeira.status_code == 201, detalhe(primeira)
    assert segunda.status_code == 201, detalhe(segunda)
    assert corpo_json(primeira)["id"] != corpo_json(segunda)["id"]


@pytest.mark.muta_estado
@pytest.mark.premissa
def test_mesma_chave_com_corpo_diferente_nao_cria_nova_transferencia(a_com_saldo, api_a, conta_a, chave_b):
    # O spec não define este caso (muitas APIs devolvem 409/422). O que NÃO pode acontecer é
    # criar outra transferência ou devolver a original como se fosse o novo pedido.
    chave = str(uuid.uuid4())
    primeira = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b, "0.01"), idem=chave)
    assert primeira.status_code == 201, detalhe(primeira)
    original = corpo_json(primeira)

    segunda = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b, "0.02"), idem=chave)

    assert segunda.status_code != 201, f"mesma chave com valor diferente criou outra transferência: {detalhe(segunda)}"
    assert segunda.status_code < 500, detalhe(segunda)
    if segunda.status_code == 200:  # aceitável apenas se for exatamente a original
        devolvida = corpo_json(segunda)
        assert devolvida["id"] == original["id"]
        assert Decimal(devolvida["valor"]) == UM_CENTAVO


@pytest.mark.muta_estado
@pytest.mark.premissa
def test_requisicoes_simultaneas_com_a_mesma_chave_criam_uma_unica_transferencia(
    a_com_saldo, api_a, conta_a, chave_b, espera
):
    """Duplo clique / retry de rede: N requisições iguais ao mesmo tempo -> um 201 e um só débito.

    Premissa: as perdedoras recebem 200 (original) ou 409 (em andamento); o spec só cita o 200.
    """
    paralelas = 5
    chave = str(uuid.uuid4())
    corpo = corpo_transferencia(conta_a, chave_b)
    antes = espera.saldo_estavel(api_a, conta_a)
    esperado = antes - UM_CENTAVO
    largada = threading.Barrier(paralelas)

    def disparar(_):
        cliente = api_a.com_token(api_a.token)  # sessão própria por thread
        largada.wait(timeout=10)
        return criar_transferencia(cliente, corpo, idem=chave)

    with ThreadPoolExecutor(max_workers=paralelas) as pool:
        respostas = list(pool.map(disparar, range(paralelas)))

    statuses = sorted(r.status_code for r in respostas)
    assert statuses.count(201) == 1, f"esperava exatamente um 201, vieram {statuses}"
    assert set(statuses) <= {200, 201, 409}, f"status inesperados: {statuses}"
    ids = {corpo_json(r)["id"] for r in respostas if r.status_code in (200, 201)}
    assert len(ids) == 1, f"as respostas apontam transferências diferentes: {ids}"

    espera.saldo_chegar_a(api_a, conta_a, esperado)
    depois = espera.saldo_estavel(api_a, conta_a)
    assert depois == esperado, f"saldo {antes} -> {depois}: {paralelas} requisições iguais debitaram mais de uma vez"


@pytest.mark.muta_estado
@pytest.mark.seguranca
@pytest.mark.premissa
def test_idempotency_key_de_um_usuario_nao_devolve_a_transferencia_de_outro(
    a_com_saldo, api_a, api_b, conta_a, conta_b, chave_a, chave_b
):
    # Cenário: a mesma chave chega de dois usuários. A resposta do usuário B nunca pode ser
    # a transferência do usuário A (vazamento de dados entre titulares).
    if saldo_de(api_b, conta_b) < UM_CENTAVO:
        pytest.skip("a conta B precisa de saldo em homologação para este teste")
    chave = str(uuid.uuid4())
    da_a = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b), idem=chave)
    assert da_a.status_code == 201, detalhe(da_a)
    id_a = corpo_json(da_a)["id"]

    da_b = criar_transferencia(api_b, corpo_transferencia(conta_b, chave_a), idem=chave)

    assert da_b.status_code != 200, f"B recebeu um 'replay' de uma chave que é do usuário A: {detalhe(da_b)}"
    assert id_a not in da_b.text, "a resposta para B contém o id da transferência de A"


@pytest.mark.parametrize("idem", [None, "", "nao-e-uuid", "123"], ids=["ausente", "vazia", "texto", "numero"])
def test_idempotency_key_ausente_ou_fora_do_formato_uuid_e_rejeitada(api_a, conta_a, chave_b, idem):
    resp = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b), idem=idem)

    rejeitada(resp)


# --------------------------------------------------------------------------- #
# Regras de negócio (422)
# --------------------------------------------------------------------------- #
def test_valor_acima_do_saldo_retorna_422_e_nao_debita(api_a, conta_a, chave_b, espera):
    saldo = espera.saldo_estavel(api_a, conta_a)
    valor = fmt_valor(max(saldo, Decimal("0")) + UM_CENTAVO)

    resp = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b, valor))

    validar_problema(resp, 422)
    assert espera.saldo_estavel(api_a, conta_a) == saldo, "a transferência recusada alterou o saldo"


def test_valor_acima_do_limite_diario_retorna_422(api_a, conta_a, chave_b, espera):
    saldo = espera.saldo_estavel(api_a, conta_a)
    valor = LIMITE_DIARIO + UM_CENTAVO
    if saldo < valor:
        pytest.skip(
            f"conta A tem {saldo}: com saldo menor que {valor} o 422 poderia vir da regra de saldo e "
            "não do limite, então o teste não provaria nada. Deposite mais em homologação para cobrir o limite."
        )

    resp = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b, fmt_valor(valor)))

    validar_problema(resp, 422)
    assert espera.saldo_estavel(api_a, conta_a) == saldo, "a transferência recusada alterou o saldo"


@pytest.mark.parametrize("chave", [None, "###"], ids=["chave-pix-inexistente", "formato-invalido"])
def test_chave_de_destino_invalida_retorna_422(api_a, conta_a, chave):
    chave = chave if chave is not None else str(uuid.uuid4())  # UUID aleatório: formato de chave aleatória PIX

    resp = criar_transferencia(api_a, corpo_transferencia(conta_a, chave))

    validar_problema(resp, 422)


# --------------------------------------------------------------------------- #
# Validação de entrada (status documentado só para 422; ver ERRO_DE_VALIDACAO)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "valor",
    [
        pytest.param("0.00", id="zero"),               # passa no pattern, viola "mínimo 0.01"
        pytest.param("-5.00", id="negativo"),          # pattern do pedido não aceita sinal
        pytest.param("10", id="sem-casas"),
        pytest.param("10.5", id="uma-casa"),
        pytest.param("10.555", id="tres-casas"),
        pytest.param("10,00", id="virgula"),
        pytest.param(" 10.00", id="espaco"),
        pytest.param("1e3", id="notacao-cientifica"),
        pytest.param("NaN", id="nan"),
        pytest.param("abc", id="texto"),
        pytest.param("", id="vazio"),
        pytest.param(0.01, id="numero-json"),          # valor deve ser string, não número
        pytest.param(None, id="nulo"),
    ],
)
def test_valor_invalido_e_rejeitado(api_a, conta_a, chave_b, valor):
    rejeitada(criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b, valor)))


@pytest.mark.parametrize("campo", ["contaOrigemId", "chaveDestino", "valor"])
def test_campo_obrigatorio_ausente_e_rejeitado(api_a, conta_a, chave_b, campo):
    corpo = corpo_transferencia(conta_a, chave_b)
    del corpo[campo]

    rejeitada(criar_transferencia(api_a, corpo))


@pytest.mark.parametrize("chave", ["", "   ", "x" * 500], ids=["vazia", "so-espacos", "500-caracteres"])
def test_chave_de_destino_vazia_ou_gigante_e_rejeitada(api_a, conta_a, chave):
    rejeitada(criar_transferencia(api_a, corpo_transferencia(conta_a, chave)))


@pytest.mark.parametrize(
    "descricao",
    [pytest.param("x" * 141, id="141-caracteres"), pytest.param(123, id="numero")],
)
def test_descricao_acima_do_limite_ou_de_tipo_errado_e_rejeitada(api_a, conta_a, chave_b, descricao):
    rejeitada(criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b, descricao=descricao)))


@pytest.mark.parametrize("bruto", ["{nao e json", "[]", "null", ""], ids=["json-quebrado", "array", "null", "corpo-vazio"])
def test_corpo_que_nao_e_um_objeto_json_e_rejeitado(api_a, bruto):
    rejeitada(criar_transferencia(api_a, None, bruto=bruto))


@pytest.mark.premissa
@pytest.mark.parametrize("conta", ["nao-e-uuid", ""], ids=["texto", "vazio"])
def test_contaOrigemId_fora_do_formato_uuid_e_rejeitado(api_a, chave_b, conta):
    # Poderia ser 400/422 (formato) ou 404 (conta inexistente); nunca 201 nem 5xx.
    resp = criar_transferencia(api_a, corpo_transferencia(conta, chave_b))

    assert resp.status_code in (400, 404, 422), detalhe(resp)
    nao_vazar_detalhes_internos(resp)


# --------------------------------------------------------------------------- #
# Segurança: autenticação e conta de outro titular
# --------------------------------------------------------------------------- #
@pytest.mark.seguranca
@pytest.mark.parametrize("cabecalhos", list(SEM_AUTENTICACAO.values()), ids=list(SEM_AUTENTICACAO))
def test_sem_credencial_valida_retorna_401(api_a, conta_a, chave_b, cabecalhos):
    resp = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b), token=None, headers=cabecalhos)

    assert resp.status_code == 401, detalhe(resp)


@pytest.mark.seguranca
def test_token_adulterado_retorna_401(api_a, conta_a, chave_b):
    token = api_a.token
    adulterado = token[:-1] + ("A" if token[-1] != "A" else "B")

    resp = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b), token=adulterado)

    assert resp.status_code == 401, detalhe(resp)


@pytest.mark.seguranca
@pytest.mark.muta_estado  # só mexe em dinheiro se houver a falha que o teste procura
def test_transferir_da_conta_de_outro_titular_retorna_404_e_nao_move_dinheiro(
    cfg, api_a, api_b, conta_b, chave_b, espera
):
    destino = cfg.chave_a or chave_b  # o atacante (A) mandaria para si mesmo
    saldo_b_antes = espera.saldo_estavel(api_b, conta_b)

    resp = criar_transferencia(api_a, corpo_transferencia(conta_b, destino, "0.01"))

    assert resp.status_code == 404, detalhe(resp)
    nao_vaza_dados_da_conta(resp)
    assert espera.saldo_estavel(api_b, conta_b) == saldo_b_antes, "a conta de B foi debitada por um pedido de A"


@pytest.mark.seguranca
def test_conta_de_origem_inexistente_e_conta_alheia_sao_indistinguiveis(api_a, conta_b, chave_b):
    inexistente = criar_transferencia(api_a, corpo_transferencia(str(uuid.uuid4()), chave_b))
    alheia = criar_transferencia(api_a, corpo_transferencia(conta_b, chave_b))

    assert inexistente.status_code == 404, detalhe(inexistente)
    assert alheia.status_code == inexistente.status_code, (
        "status diferente para conta alheia e inexistente permite descobrir quais contas existem"
    )


# --------------------------------------------------------------------------- #
# Destrutivo (opt-in): mantenha por último
# --------------------------------------------------------------------------- #
@pytest.mark.muta_estado
@pytest.mark.consome_limite
@pytest.mark.premissa
def test_limite_diario_vale_para_o_acumulado_do_dia(cfg, api_a, conta_a, chave_b, espera):
    """DESTRUTIVO: move R$ 4.990,00 de A para B e esgota o limite do dia da conta A.

    Só roda com RODAR_TESTES_LIMITE_DIARIO=1 e fica por último no arquivo de propósito. Premissa:
    "limite diário de 5000.00" é a SOMA das transferências do dia, não só por transferência.
    4990 + 20 passa de 5000 mesmo que execuções anteriores já tenham gasto alguns centavos.
    """
    if not cfg.rodar_limite_diario:
        pytest.skip("opt-in: defina RODAR_TESTES_LIMITE_DIARIO=1 (gasta o limite diário da conta A)")
    if espera.saldo_estavel(api_a, conta_a) < Decimal("5010.00"):
        pytest.skip("a conta A precisa de pelo menos 5010.00 de saldo para este teste")

    primeira = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b, "4990.00"))
    if primeira.status_code == 422:
        pytest.skip(f"o limite do dia já estava consumido ou a 1ª transferência foi recusada: {detalhe(primeira)}")
    assert primeira.status_code == 201, detalhe(primeira)

    segunda = criar_transferencia(api_a, corpo_transferencia(conta_a, chave_b, "20.00"))

    validar_problema(segunda, 422)
