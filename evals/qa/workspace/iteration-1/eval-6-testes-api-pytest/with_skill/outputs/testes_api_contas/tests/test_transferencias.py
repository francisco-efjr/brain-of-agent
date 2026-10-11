"""POST /transferencias (PIX)

Prioridade pelo risco: dinheiro que sai da conta errada, sai duas vezes ou sai quando devia ser
recusado. Por isso quase todo teste confere o EFEITO (saldos e extrato), não só o status.

Convenções:
* Valores pequenos (R$ 0,01 a R$ 1,00) de A para B; o custo de uma execução é de poucos reais.
* Toda recusa é seguida de `assert_sem_efeito`, que usa uma transferência-marco válida para provar
  a ausência de débito (ver support.py).
* `inferido`: comportamento que o contrato não escreve; veja test_extrato.py.
"""
from __future__ import annotations

import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

import pytest

from tests.support import (CENTAVO, LIMITE_DIARIO, Transferencia, aguardar_efeito,
                           aguardar_saldo, assert_problema, assert_proximo_de_agora, assert_recusada,
                           assert_sem_efeito, chaves_do_corpo, corpo_transferencia, descricao_com,
                           dinheiro, enviar_marco, escolher_origem, lancamentos_com, novo_marcador, saldos)

UM_REAL = Decimal("1.00")


def _transferir_ok(origem, valor, marcador, texto=""):
    """Setup comum: transferência válida; devolve a resposta já validada como 201."""
    r = origem.de.api.transferir(corpo_transferencia(origem, valor, descricao_com(marcador, texto)))
    assert r.status_code == 201, f"transferência válida foi recusada ({r.status_code}): {r.text[:300]}"
    return r


# --------------------------------------------------------------------------
# Caso feliz e efeitos
# --------------------------------------------------------------------------
def test_transferencia_valida_debita_origem_credita_destino_e_aparece_no_extrato(origem_a):
    antes = saldos(origem_a)
    marcador = novo_marcador()

    r = _transferir_ok(origem_a, UM_REAL, marcador, "pix qa")

    transferencia = Transferencia.model_validate(r.json())
    assert transferencia.status in ("PROCESSANDO", "CONCLUIDA")  # nunca RECUSADA num 201
    assert Decimal(transferencia.valor) == UM_REAL
    assert_proximo_de_agora(transferencia.criadaEm)
    lancamento = aguardar_efeito(origem_a, antes, UM_REAL, marcador)  # saldos conferem com antes ∓ R$ 1,00
    assert lancamento.tipo == "DEBITO"
    assert abs(dinheiro(lancamento.valor)) == UM_REAL
    assert_proximo_de_agora(lancamento.data)


@pytest.mark.parametrize("valor", ["0.01", "0.02"], ids=["minimo", "minimo_mais_um_centavo"])
def test_valores_minimos_validos_sao_aceitos(origem_a, valor):
    antes = saldos(origem_a)
    marcador = novo_marcador()

    _transferir_ok(origem_a, Decimal(valor), marcador)

    lancamento = aguardar_efeito(origem_a, antes, Decimal(valor), marcador)
    assert abs(dinheiro(lancamento.valor)) == Decimal(valor)


@pytest.mark.parametrize("caso", ["exatamente_140", "acentos_e_apostrofo"])
def test_descricao_valida_e_devolvida_intacta_no_extrato(origem_a, caso):
    marcador = novo_marcador()
    descricao = {"exatamente_140": (marcador + " ").ljust(140, "x"),
                 "acentos_e_apostrofo": f"{marcador} João D'Ávila, aluguel de março ção ñ"}[caso]
    assert len(descricao) <= 140
    antes = saldos(origem_a)

    r = origem_a.de.api.transferir(corpo_transferencia(origem_a, CENTAVO, descricao))

    assert r.status_code == 201, r.text
    assert aguardar_efeito(origem_a, antes, CENTAVO, marcador).descricao == descricao


def test_descricao_e_opcional(origem_a):
    antes = saldos(origem_a)

    r = origem_a.de.api.transferir(corpo_transferencia(origem_a, CENTAVO))  # sem descricao

    assert r.status_code == 201, r.text
    aguardar_saldo(origem_a.de, antes.origem - CENTAVO)
    aguardar_saldo(origem_a.para, antes.destino + CENTAVO)


# --------------------------------------------------------------------------
# Idempotência (Idempotency-Key): risco de cobrança dupla
# --------------------------------------------------------------------------
def test_mesma_chave_e_mesmo_corpo_nao_gera_segundo_debito(origem_a):
    antes, marcador, chave = saldos(origem_a), novo_marcador(), str(uuid.uuid4())
    corpo = corpo_transferencia(origem_a, CENTAVO, descricao_com(marcador, "idempotencia"))

    primeira = origem_a.de.api.transferir(corpo, idempotency_key=chave)
    segunda = origem_a.de.api.transferir(corpo, idempotency_key=chave)

    assert (primeira.status_code, segunda.status_code) == (201, 200)  # contrato: repetição devolve 200
    original = Transferencia.model_validate(primeira.json())
    repetida = Transferencia.model_validate(segunda.json())
    assert repetida.id == original.id and Decimal(repetida.valor) == Decimal(original.valor)
    aguardar_efeito(origem_a, antes, CENTAVO, marcador)  # os saldos só mexeram uma vez
    enviar_marco(origem_a, antes.apos(CENTAVO))  # marco: se houvesse segundo efeito, já teria aparecido
    assert len(lancamentos_com(origem_a.de.api, origem_a.de.id, marcador)) == 1


def test_requisicoes_simultaneas_com_a_mesma_chave_geram_um_unico_debito(origem_a):
    antes, marcador, chave = saldos(origem_a), novo_marcador(), str(uuid.uuid4())
    corpo = corpo_transferencia(origem_a, CENTAVO, descricao_com(marcador, "corrida"))
    tentativas = 5
    largada = threading.Barrier(tentativas)

    def disparar(_):
        cliente = origem_a.de.api.novo()  # uma sessão HTTP por thread
        largada.wait(timeout=10)
        return cliente.transferir(corpo, idempotency_key=chave)

    with ThreadPoolExecutor(max_workers=tentativas) as pool:
        respostas = list(pool.map(disparar, range(tentativas)))

    status = sorted(r.status_code for r in respostas)
    assert set(status) <= {200, 201, 409}, status  # 409 = "em andamento" (inferido; não está no contrato)
    assert 201 in status, f"nenhuma requisição criou a transferência: {status}"
    assert len({r.json()["id"] for r in respostas if r.status_code in (200, 201)}) == 1
    aguardar_efeito(origem_a, antes, CENTAVO, marcador)
    enviar_marco(origem_a, antes.apos(CENTAVO))
    assert len(lancamentos_com(origem_a.de.api, origem_a.de.id, marcador)) == 1


def test_mesma_chave_com_valor_diferente_nunca_gera_segundo_debito(origem_a):
    # O contrato não diz o status; o que não pode acontecer é um segundo débito ou a troca silenciosa do valor.
    antes, marcador, chave = saldos(origem_a), novo_marcador(), str(uuid.uuid4())
    descricao = descricao_com(marcador, "chave reutilizada")
    original = origem_a.de.api.transferir(corpo_transferencia(origem_a, Decimal("0.01"), descricao), idempotency_key=chave)
    assert original.status_code == 201, original.text

    outra = origem_a.de.api.transferir(corpo_transferencia(origem_a, Decimal("0.02"), descricao), idempotency_key=chave)

    assert outra.status_code != 201, "a chave reutilizada com outro corpo criou uma nova transferência"
    if outra.status_code == 200:
        assert Decimal(outra.json()["valor"]) == Decimal("0.01"), "devolveu a original com valor trocado"
    else:
        assert 400 <= outra.status_code < 500, outra.text
    aguardar_efeito(origem_a, antes, Decimal("0.01"), marcador)
    enviar_marco(origem_a, antes.apos(Decimal("0.01")))
    achados = lancamentos_com(origem_a.de.api, origem_a.de.id, marcador)
    assert len(achados) == 1 and abs(dinheiro(achados[0].valor)) == Decimal("0.01")


@pytest.mark.inferido
@pytest.mark.parametrize("chave", [None, "", "nao-e-uuid", "12345678"],
                         ids=["ausente", "vazia", "texto", "curta"])
def test_idempotency_key_ausente_ou_invalida_e_recusada_sem_efeito(origem_a, chave):
    # contrato: header obrigatório com format uuid, mas sem status definido para a violação
    antes, marcador = saldos(origem_a), novo_marcador()

    r = origem_a.de.api.transferir(corpo_transferencia(origem_a, UM_REAL, descricao_com(marcador)),
                                   idempotency_key=chave)

    assert_recusada(r, aceitos=(400, 422))
    assert_sem_efeito(origem_a, antes, marcador)


# --------------------------------------------------------------------------
# Autenticação e isolamento (404 para conta de outro titular)
# --------------------------------------------------------------------------
@pytest.mark.parametrize("cenario", ["sem_token", "token_invalido"])
def test_transferencia_sem_credencial_valida_retorna_401_e_nao_debita(origem_a, clientes_sem_credencial, cenario):
    antes, marcador = saldos(origem_a), novo_marcador()

    r = clientes_sem_credencial[cenario].transferir(corpo_transferencia(origem_a, UM_REAL, descricao_com(marcador)))

    assert r.status_code == 401
    assert_sem_efeito(origem_a, antes, marcador)


def test_transferir_da_conta_de_outro_titular_retorna_404_e_nao_debita(origem_a):
    # B, com o próprio token, tenta mover dinheiro da conta de A para a própria chave PIX
    atacante = origem_a.para.api
    antes, marcador = saldos(origem_a), novo_marcador()

    alheia = atacante.transferir(corpo_transferencia(origem_a, UM_REAL, descricao_com(marcador)))
    inexistente = atacante.transferir(corpo_transferencia(origem_a, UM_REAL, descricao_com(marcador),
                                                          contaOrigemId=str(uuid.uuid4())))

    assert alheia.status_code == inexistente.status_code == 404
    assert chaves_do_corpo(alheia) == chaves_do_corpo(inexistente)  # indistinguível de conta inexistente
    assert_sem_efeito(origem_a, antes, marcador)


def test_conta_de_origem_inexistente_retorna_404(origem_a):
    r = origem_a.de.api.transferir(corpo_transferencia(origem_a, UM_REAL, contaOrigemId=str(uuid.uuid4())))

    assert r.status_code == 404


# --------------------------------------------------------------------------
# Regras de negócio (422): chave, saldo e limite diário
# --------------------------------------------------------------------------
CHAVES_INVALIDAS = {
    "uuid_nao_cadastrado": lambda: str(uuid.uuid4()),
    "texto_livre": lambda: "nao-e-uma-chave",
    "cpf_com_digito_verificador_errado": lambda: "52998224726",  # o válido seria 529.982.247-25
}


@pytest.mark.parametrize("tipo", list(CHAVES_INVALIDAS))
def test_chave_de_destino_invalida_retorna_422_e_nao_debita(origem_a, tipo):
    antes, marcador = saldos(origem_a), novo_marcador()

    r = origem_a.de.api.transferir(corpo_transferencia(origem_a, UM_REAL, descricao_com(marcador),
                                                       chaveDestino=CHAVES_INVALIDAS[tipo]()))

    assert_problema(r, 422)
    assert_sem_efeito(origem_a, antes, marcador)


def test_valor_acima_do_saldo_retorna_422_e_nao_debita(origens):
    # isola a regra de saldo: saldo + R$ 0,01 ainda cabe no limite diário, então só o saldo pode recusar
    origem, antes = escolher_origem(
        origens, lambda saldo: UM_REAL <= saldo and saldo + CENTAVO <= LIMITE_DIARIO,
        "saldo entre R$ 1,00 e R$ 4.999,99")
    marcador, valor = novo_marcador(), antes.origem + CENTAVO

    r = origem.de.api.transferir(corpo_transferencia(origem, valor, descricao_com(marcador)))

    assert_problema(r, 422)
    assert_sem_efeito(origem, antes, marcador)


def test_valor_acima_do_limite_diario_retorna_422_e_nao_debita(origens):
    # isola a regra de limite: com saldo cobrindo R$ 5.000,01, só o limite diário pode recusar.
    # CUIDADO: se a API tiver o defeito (aceitar), R$ 5.000,01 sairão da conta de teste.
    origem, antes = escolher_origem(origens, lambda saldo: saldo >= LIMITE_DIARIO + CENTAVO,
                                    "saldo de pelo menos R$ 5.000,01")
    marcador = novo_marcador()

    r = origem.de.api.transferir(corpo_transferencia(origem, LIMITE_DIARIO + CENTAVO, descricao_com(marcador)))

    assert_problema(r, 422)
    assert_sem_efeito(origem, antes, marcador)


# --------------------------------------------------------------------------
# Validação de entrada: valor-limite, tipo e formato (status 400 ou 422; o contrato não fixa)
# --------------------------------------------------------------------------
def _com(**campos):
    return lambda corpo: {**corpo, **campos}


def _sem(campo):
    return lambda corpo: {chave: valor for chave, valor in corpo.items() if chave != campo}


STATUS_PADRAO = (400, 422)
CORPOS_INVALIDOS = {  # nome: (como estragar o corpo válido, status aceitos)
    "valor_zero": (_com(valor="0.00"), STATUS_PADRAO),  # mínimo é 0.01
    "valor_negativo": (_com(valor="-1.00"), STATUS_PADRAO),
    "valor_sem_casas_decimais": (_com(valor="1"), STATUS_PADRAO),
    "valor_com_uma_casa": (_com(valor="1.5"), STATUS_PADRAO),
    "valor_com_tres_casas": (_com(valor="1.001"), STATUS_PADRAO),
    "valor_com_virgula": (_com(valor="1,00"), STATUS_PADRAO),
    "valor_com_milhar_br": (_com(valor="1.000,00"), STATUS_PADRAO),
    "valor_com_espaco": (_com(valor=" 1.00"), STATUS_PADRAO),
    "valor_notacao_cientifica": (_com(valor="1e2"), STATUS_PADRAO),
    "valor_texto": (_com(valor="abc"), STATUS_PADRAO),
    "valor_vazio": (_com(valor=""), STATUS_PADRAO),
    "valor_numero_json_float": (_com(valor=1.0), STATUS_PADRAO),  # contrato: string, não number
    "valor_numero_json_inteiro": (_com(valor=1), STATUS_PADRAO),
    "valor_nulo": (_com(valor=None), STATUS_PADRAO),
    "valor_sem_o_campo": (_sem("valor"), STATUS_PADRAO),
    "sem_chave_destino": (_sem("chaveDestino"), STATUS_PADRAO),
    "chave_destino_vazia": (_com(chaveDestino=""), STATUS_PADRAO),
    "chave_destino_nao_string": (_com(chaveDestino=12345), STATUS_PADRAO),
    "sem_conta_origem": (_sem("contaOrigemId"), STATUS_PADRAO + (404,)),
    "conta_origem_fora_do_formato_uuid": (_com(contaOrigemId="abc"), STATUS_PADRAO + (404,)),
    "descricao_com_141_caracteres": (_com(descricao="x" * 141), STATUS_PADRAO),
    "descricao_nao_string": (_com(descricao=123), STATUS_PADRAO),
    "corpo_vazio": (lambda corpo: {}, STATUS_PADRAO + (404,)),
}


@pytest.mark.parametrize("caso", list(CORPOS_INVALIDOS))
def test_corpo_invalido_e_recusado_com_erro_de_cliente(origem_a, caso):
    estragar, aceitos = CORPOS_INVALIDOS[caso]

    r = origem_a.de.api.transferir(estragar(corpo_transferencia(origem_a, UM_REAL)))

    assert_recusada(r, aceitos)


def test_corpos_invalidos_representativos_nao_geram_debito(origem_a):
    antes, marcadores = saldos(origem_a), []
    for caso in ("valor_zero", "valor_negativo", "valor_com_virgula", "valor_numero_json_float",
                 "descricao_com_141_caracteres"):
        marcador = novo_marcador()
        marcadores.append(marcador)
        estragar, aceitos = CORPOS_INVALIDOS[caso]
        corpo = estragar(corpo_transferencia(origem_a, UM_REAL, descricao_com(marcador)))
        assert_recusada(origem_a.de.api.transferir(corpo), aceitos)

    assert_sem_efeito(origem_a, antes, *marcadores)


@pytest.mark.inferido
def test_json_malformado_retorna_400_e_nao_500(origem_a):
    r = origem_a.de.api.transferir(bruto=b'{"contaOrigemId": "', idempotency_key=str(uuid.uuid4()))

    assert_recusada(r, aceitos=(400,))
