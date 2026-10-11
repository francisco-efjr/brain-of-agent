#!/usr/bin/env python3
"""Gera casos_pix_limites_xray.csv e tabela_chat.md a partir de uma única lista de casos.

Uso: python3 gerar_casos.py
Saída (na mesma pasta do script): casos_pix_limites_xray.csv, tabela_chat.md
"""
import csv
import pathlib
from decimal import Decimal

AQUI = pathlib.Path(__file__).parent

RN = {
    "RN-01": "valor mínimo R$ 0,01",
    "RN-02": "saldo cobre o valor",
    "RN-03": "limite diurno R$ 5.000,00 (06:00-20:00)",
    "RN-04": "limite noturno R$ 1.000,00 (20:00-06:00)",
}

PS = ("1. Abrir Pix > Transferir e informar a chave de destino. "
      "2. Informar o valor. 3. Revisar e confirmar com a autenticação do app.")
PS_CURTO = "PS"  # passo-padrão, definido acima da tabela no chat

JANELA = {"D": "10:00:00", "N": "22:00:00"}


def pre(base, clock=None, saldo="R$ 20.000,00", extras=()):
    """Devolve (texto expandido para o CSV, texto curto para o chat)."""
    clock = clock or JANELA[base]
    if extras:
        acum = ("Preparação (massa): " + "; ".join(extras) +
                "; demais acumulados R$ 0,00; saldo informado já considera a preparação")
    else:
        acum = "acumulado diurno e noturno R$ 0,00"
    longo = (f"Cliente PF autenticado; conta ativa; dispositivo já cadastrado; saldo {saldo}; "
             f"{acum}; relógio do ambiente fixado em {clock} "
             f"(America/Sao_Paulo); chave Pix de destino válida.")
    curto = [f"PP-{base}"]
    if clock != JANELA[base]:
        curto.append(f"relógio {clock}")
    if saldo != "R$ 20.000,00":
        curto.append(f"saldo {saldo}")
    curto += list(extras)
    return longo, "; ".join(curto)


C = []  # lista de casos


def caso(grupo, titulo, rn, tecnica, prio, p, passos, dados, esperado,
         pendencia="", smoke=False):
    C.append(dict(grupo=grupo, titulo=titulo, rn=rn, tecnica=tecnica, prio=prio,
                  pre=p, passos=passos, dados=dados, esperado=esperado,
                  pendencia=pendencia, smoke=smoke))


G1, G2, G3, G4, G5, G6 = ("valor-minimo", "saldo", "limite-diurno", "limite-noturno",
                          "fronteira-horario", "hostil-concorrencia")

# ---------------------------------------------------------------- valor mínimo
caso(G1, "Aceita transferência do valor mínimo", "RN-01", "valor-limite (mín)", "Alta",
     pre("D"), PS, "Valor: R$ 0,01",
     "Transferência confirmada; saldo R$ 19.999,99; extrato com débito de R$ 0,01 e EndToEndId; acumulado diurno R$ 0,01.",
     smoke=True)
caso(G1, "Recusa valor zero", "RN-01", "valor-limite (mín − 0,01)", "Alta",
     pre("D"), PS, "Valor: R$ 0,00",
     "Não conclui; mensagem informa o valor mínimo de R$ 0,01; saldo inalterado em R$ 20.000,00; nenhuma transação no extrato.",
     smoke=True)
caso(G1, "Recusa valor negativo direto na API", "RN-01", "partição inválida + hostil", "Alta",
     pre("D"),
     "1. Obter token do cliente de teste. 2. Enviar POST de transferência Pix com o valor informado (repetir para cada valor). 3. Consultar saldo e extrato do pagador e do destino.",
     "Valores: -0,01 e -100,00",
     "Resposta 4xx (400 ou 422, conforme o contrato) com erro no campo valor; saldo do pagador e do destino inalterados; nenhum lançamento.")
caso(G1, "Recusa valor com fração de centavo abaixo do mínimo", "RN-01", "valor-limite + precisão", "Média",
     pre("D"),
     "1. Enviar POST de transferência Pix com o valor informado. 2. Consultar saldo e extrato.",
     "Valor: R$ 0,009",
     "Recusada (abaixo de R$ 0,01 ou mais de 2 casas decimais); não é arredondado para R$ 0,01 nem debitado; saldo inalterado.",
     pendencia="P6")
caso(G1, "Recusa valor não numérico ou ausente", "RN-01", "partição inválida + hostil", "Média",
     pre("D"),
     "1. Enviar POST de transferência Pix com o valor informado, uma execução por valor (abc e vazio também pela tela). 2. Consultar saldo e extrato.",
     'Valores: "abc"; "" (vazio); "   " (só espaços); null; campo ausente; "NaN"; "Infinity"',
     "Cada execução recusada com 4xx/422 e erro no campo valor, sem erro 500 nem tela quebrada; nenhuma transação; saldo inalterado.")
caso(G1, "Lê valor com ponto de milhar e vírgula decimal", "RN-01", "formato pt-BR", "Média",
     pre("D"),
     "1. Abrir Pix > Transferir e informar a chave de destino. 2. Colar o valor no campo. 3. Conferir a tela de revisão. 4. Confirmar.",
     "Valor colado: 1.000,50",
     "Revisão mostra R$ 1.000,50; após confirmar, débito de R$ 1.000,50; saldo R$ 18.999,50.")

# ---------------------------------------------------------------- saldo
caso(G2, "Aceita valor igual ao saldo", "RN-02", "valor-limite (saldo = valor)", "Alta",
     pre("D", saldo="R$ 100,00"), PS, "Valor: R$ 100,00",
     "Confirmada; saldo final R$ 0,00 (nunca negativo); acumulado diurno R$ 100,00.", smoke=True)
caso(G2, "Aceita valor 1 centavo abaixo do saldo", "RN-02", "valor-limite (saldo − 0,01)", "Média",
     pre("D", saldo="R$ 100,01"), PS, "Valor: R$ 100,00",
     "Confirmada; saldo final R$ 0,01.")
caso(G2, "Recusa valor 1 centavo acima do saldo", "RN-02", "valor-limite (saldo + 0,01)", "Alta",
     pre("D", saldo="R$ 99,99"), PS, "Valor: R$ 100,00",
     "Recusada; mensagem de saldo insuficiente; saldo inalterado em R$ 99,99; nenhuma transação; acumulado inalterado.",
     smoke=True)
caso(G2, "Recusa transferência com saldo zero", "RN-02", "partição (saldo zero)", "Média",
     pre("D", saldo="R$ 0,00"), PS, "Valor: R$ 0,01",
     "Recusada; mensagem de saldo insuficiente; saldo R$ 0,00; nenhuma transação.")
caso(G2, "Recusa quando saldo e limite diurno são insuficientes ao mesmo tempo", "RN-02, RN-03",
     "tabela de decisão (2 condições falhas)", "Média",
     pre("D", saldo="R$ 3.000,00"), PS, "Valor: R$ 6.000,00",
     "Recusada; nada debitado; saldo R$ 3.000,00; mensagem de saldo OU de limite (a definir em P4), sem erro genérico nem erro 500.",
     pendencia="P4")
caso(G2, "Dois débitos simultâneos não deixam o saldo negativo", "RN-02", "concorrência", "Alta",
     pre("D", saldo="R$ 100,00"),
     "1. Disparar 2 requisições de transferência ao mesmo tempo (chaves de idempotência distintas, destinos distintos). 2. Consultar saldo e extrato.",
     "2 transferências simultâneas de R$ 80,00",
     "Uma confirmada e outra recusada por saldo insuficiente; saldo final R$ 20,00; um único débito de R$ 80,00 no extrato; acumulado diurno R$ 80,00.")

# ---------------------------------------------------------------- limite diurno
caso(G3, "Aceita valor 1 centavo abaixo do limite diurno", "RN-03", "valor-limite (máx − 0,01)", "Média",
     pre("D"), PS, "Valor: R$ 4.999,99",
     "Confirmada; saldo R$ 15.000,01; acumulado diurno R$ 4.999,99.")
caso(G3, "Aceita valor exatamente igual ao limite diurno", "RN-03", "valor-limite (máx)", "Alta",
     pre("D"), PS, "Valor: R$ 5.000,00",
     "Confirmada; saldo R$ 15.000,00; acumulado diurno R$ 5.000,00.", smoke=True)
caso(G3, "Recusa valor 1 centavo acima do limite diurno", "RN-03", "valor-limite (máx + 0,01)", "Alta",
     pre("D"), PS, "Valor: R$ 5.000,01",
     "Recusada; mensagem de limite diurno que cita R$ 5.000,00; saldo inalterado em R$ 20.000,00; nenhuma transação; acumulado R$ 0,00.",
     smoke=True)
caso(G3, "Aceita duas transferências cuja soma é exatamente o limite diurno", "RN-03", "acumulado (soma = limite)", "Alta",
     pre("D"),
     "1. Transferir R$ 4.999,99 (PS). 2. Transferir R$ 0,01 (PS).",
     "Valores: R$ 4.999,99 e depois R$ 0,01",
     "As duas confirmadas; saldo R$ 15.000,00; acumulado diurno R$ 5.000,00.")
caso(G3, "Recusa qualquer valor depois de esgotar o limite diurno", "RN-03", "acumulado (limite esgotado)", "Alta",
     pre("D", saldo="R$ 15.000,00", extras=["acumulado diurno R$ 5.000,00 (transferência concluída às 09:00:00)"]),
     PS, "Valor: R$ 0,01",
     "Recusada; mensagem de limite diurno de R$ 5.000,00; saldo inalterado em R$ 15.000,00; acumulado R$ 5.000,00.")
caso(G3, "Recusa transferência que faz a soma passar do limite diurno por 1 centavo", "RN-03", "acumulado (soma = limite + 0,01)", "Alta",
     pre("D", saldo="R$ 17.000,00", extras=["acumulado diurno R$ 3.000,00 (transferência concluída às 09:00:00)"]),
     PS, "Valor: R$ 2.000,01",
     "Recusada por limite diurno; saldo inalterado em R$ 17.000,00; acumulado R$ 3.000,00.")
caso(G3, "Transferência recusada por limite não consome o limite", "RN-03", "acumulado + estado", "Alta",
     pre("D", saldo="R$ 16.000,00", extras=["acumulado diurno R$ 4.000,00 (transferência concluída às 09:00:00)"]),
     "1. Transferir R$ 1.000,01 (PS). 2. Transferir R$ 1.000,00 (PS).",
     "Valores: R$ 1.000,01 e depois R$ 1.000,00",
     "Passo 1 recusado por limite; passo 2 confirmado; saldo final R$ 15.000,00; acumulado diurno R$ 5.000,00 (a tentativa recusada não entrou na soma).")
caso(G3, "Transferência recusada por saldo não consome o limite", "RN-02, RN-03", "acumulado + estado", "Média",
     pre("D", saldo="R$ 4.000,00"),
     "1. Transferir R$ 4.500,00 (PS). 2. Transferir R$ 4.000,00 (PS). 3. Creditar R$ 1.000,00 na conta (Pix recebido de conta de teste). 4. Transferir R$ 1.000,00 (PS).",
     "Valores: R$ 4.500,00; R$ 4.000,00; crédito de R$ 1.000,00; R$ 1.000,00",
     "Passo 1 recusado por saldo insuficiente; passos 2 e 4 confirmados; saldo final R$ 0,00; acumulado diurno R$ 5.000,00 (4.000,00 + 1.000,00).")

# ---------------------------------------------------------------- limite noturno
caso(G4, "Aceita valor 1 centavo abaixo do limite noturno", "RN-04", "valor-limite (máx − 0,01)", "Média",
     pre("N"), PS, "Valor: R$ 999,99",
     "Confirmada; saldo R$ 19.000,01; acumulado noturno R$ 999,99.")
caso(G4, "Aceita valor exatamente igual ao limite noturno", "RN-04", "valor-limite (máx)", "Alta",
     pre("N"), PS, "Valor: R$ 1.000,00",
     "Confirmada; saldo R$ 19.000,00; acumulado noturno R$ 1.000,00.", smoke=True)
caso(G4, "Recusa valor 1 centavo acima do limite noturno", "RN-04", "valor-limite (máx + 0,01)", "Alta",
     pre("N"), PS, "Valor: R$ 1.000,01",
     "Recusada; mensagem de limite noturno que cita R$ 1.000,00; saldo inalterado em R$ 20.000,00; nenhuma transação; acumulado R$ 0,00.",
     smoke=True)
caso(G4, "Aceita transferência que leva o acumulado noturno exatamente ao limite", "RN-04", "acumulado (soma = limite)", "Média",
     pre("N", saldo="R$ 19.400,00", extras=["acumulado noturno R$ 600,00 (transferência concluída às 21:00:00)"]),
     PS, "Valor: R$ 400,00",
     "Confirmada; saldo R$ 19.000,00; acumulado noturno R$ 1.000,00.")
caso(G4, "Recusa transferência que passa o acumulado noturno por 1 centavo", "RN-04", "acumulado (soma = limite + 0,01)", "Alta",
     pre("N", saldo="R$ 19.400,00", extras=["acumulado noturno R$ 600,00 (transferência concluída às 21:00:00)"]),
     PS, "Valor: R$ 400,01",
     "Recusada por limite noturno; saldo inalterado em R$ 19.400,00; acumulado R$ 600,00.")
caso(G4, "Recusa qualquer valor depois de esgotar o limite noturno", "RN-04", "acumulado (limite esgotado)", "Média",
     pre("N", saldo="R$ 19.000,00", extras=["acumulado noturno R$ 1.000,00 (transferência concluída às 21:00:00)"]),
     PS, "Valor: R$ 0,01",
     "Recusada; mensagem de limite noturno de R$ 1.000,00; saldo inalterado em R$ 19.000,00.")

# ---------------------------------------------------------------- fronteiras de horário
CS = "Relógio do ambiente fixado no horário informado."
caso(G5, "Às 19:59:59 vale o limite diurno", "RN-03", "valor-limite de horário", "Alta",
     pre("D", clock="19:59:59"), PS, "Horário: 19:59:59; valor R$ 1.000,01 (acima do noturno, abaixo do diurno)",
     "Confirmada; saldo R$ 18.999,99.", smoke=True)
caso(G5, "Às 20:00:00 vale o limite noturno", "RN-04", "valor-limite de horário", "Alta",
     pre("D", clock="20:00:00"), PS, "Horário: 20:00:00; valor R$ 1.000,01",
     "Recusada por limite noturno (R$ 1.000,00); saldo inalterado em R$ 20.000,00.", smoke=True)
caso(G5, "Às 05:59:59 ainda vale o limite noturno", "RN-04", "valor-limite de horário", "Alta",
     pre("N", clock="05:59:59"), PS, "Horário: 05:59:59; valor R$ 1.000,01",
     "Recusada por limite noturno (R$ 1.000,00); saldo inalterado em R$ 20.000,00.")
caso(G5, "Às 06:00:00 passa a valer o limite diurno", "RN-03", "valor-limite de horário", "Alta",
     pre("N", clock="06:00:00"), PS, "Horário: 06:00:00; valor R$ 1.000,01",
     "Confirmada; saldo R$ 18.999,99.")
caso(G5, "Revisão aberta antes das 20:00 e confirmada depois", "RN-04", "tempo (instante de referência)", "Média",
     pre("D", clock="19:59:59"),
     "1. Abrir Pix > Transferir, informar chave e valor e chegar à tela de revisão às 19:59:59. 2. Avançar o relógio para 20:00:01. 3. Confirmar com a autenticação.",
     "Valor: R$ 1.000,01",
     "Vale o instante da confirmação: recusada por limite noturno; saldo inalterado em R$ 20.000,00.",
     pendencia="P2")
caso(G5, "Limite noturno é uma janela contínua que atravessa a meia-noite", "RN-04", "tempo (virada de dia) + acumulado", "Alta",
     pre("N", clock="23:59:59"),
     "1. Transferir R$ 600,00 às 23:59:59 (PS). 2. Avançar o relógio para 00:00:01 do dia seguinte. 3. Transferir R$ 400,00 (PS). 4. Transferir R$ 0,01 (PS).",
     "Valores: R$ 600,00; R$ 400,00; R$ 0,01",
     "Passos 1 e 3 confirmados (acumulado noturno R$ 1.000,00, sem zerar à meia-noite); passo 4 recusado por limite noturno; saldo final R$ 19.000,00.",
     pendencia="P1")
caso(G5, "Limite diurno reinicia às 06:00:00 do dia seguinte", "RN-03", "tempo (reinício do contador)", "Alta",
     pre("D", clock="06:00:00 do dia seguinte", saldo="R$ 15.000,00",
         extras=["acumulado diurno de R$ 5.000,00 no dia anterior (transferência concluída às 09:00:00)"]),
     PS, "Horário: 06:00:00 do dia seguinte; valor R$ 5.000,00",
     "Confirmada; saldo R$ 10.000,00; acumulado diurno do novo dia R$ 5.000,00.",
     pendencia="P1")
caso(G5, "Limite diurno esgotado não consome o limite noturno", "RN-03, RN-04", "tabela de decisão (janelas independentes)", "Alta",
     pre("D", clock="20:00:00", saldo="R$ 15.000,00",
         extras=["acumulado diurno de R$ 5.000,00 (transferência concluída às 10:00:00 do mesmo dia)"]),
     PS, "Horário: 20:00:00; valor R$ 1.000,00",
     "Confirmada; saldo R$ 14.000,00; acumulado noturno R$ 1.000,00.",
     pendencia="P1")
caso(G5, "Limite noturno esgotado não consome o limite diurno", "RN-03, RN-04", "tabela de decisão (janelas independentes)", "Média",
     pre("N", clock="06:00:00 do dia seguinte", saldo="R$ 19.000,00",
         extras=["acumulado noturno de R$ 1.000,00 (transferência concluída às 23:00:00 do dia anterior)"]),
     PS, "Horário: 06:00:00 do dia seguinte; valor R$ 5.000,00",
     "Confirmada; saldo R$ 14.000,00; acumulado diurno R$ 5.000,00.",
     pendencia="P1")
caso(G5, "Janela é avaliada em horário de Brasília, não em UTC", "RN-03, RN-04", "fuso horário", "Alta",
     pre("D", clock="conforme o instante UTC dos Dados"),
     "1. Com o ambiente em UTC, fixar o instante A e transferir o valor (PS). 2. Repetir com o instante B, com saldo e acumulado zerados.",
     "A: 2026-10-06T22:59:59Z (19:59:59 em Brasília), valor R$ 1.000,01. B: 2026-10-06T23:00:00Z (20:00:00 em Brasília), valor R$ 1.000,01",
     "A confirmada (limite diurno); B recusada por limite noturno.")
caso(G5, "Cliente em Manaus (UTC−4) segue o horário de Brasília", "RN-04", "fuso horário", "Média",
     pre("D", clock="2026-10-06T23:30:00Z (19:30 em Manaus, 20:30 em Brasília)"),
     "1. Com o dispositivo no fuso America/Manaus, transferir o valor (PS).",
     "Horário local do dispositivo: 19:30; valor R$ 1.000,01",
     "Recusada por limite noturno (vale o horário de Brasília); saldo inalterado em R$ 20.000,00.",
     pendencia="P3")
caso(G5, "Relógio adulterado do dispositivo não burla o limite noturno", "RN-04", "suposição de erro (fraude)", "Alta",
     pre("D", clock="21:00:00 no servidor"),
     "1. No celular, desligar o horário automático e ajustar para 14:00. 2. Transferir o valor (PS).",
     "Relógio do dispositivo: 14:00; relógio do servidor: 21:00:00; valor R$ 1.000,01",
     "Recusada por limite noturno (vale o horário do servidor); saldo inalterado em R$ 20.000,00.")

# ---------------------------------------------------------------- hostil / concorrência
caso(G6, "Duas transferências simultâneas não ultrapassam o limite diurno", "RN-03", "concorrência", "Alta",
     pre("D"),
     "1. Disparar 2 requisições de transferência ao mesmo tempo (chaves de idempotência distintas). 2. Consultar saldo, extrato e acumulado. 3. Repetir 20 vezes, zerando a massa a cada rodada.",
     "2 transferências simultâneas de R$ 3.000,00",
     "Em todas as rodadas: uma confirmada e outra recusada por limite diurno; saldo R$ 17.000,00; acumulado R$ 3.000,00 (nunca acima de R$ 5.000,00).")
caso(G6, "Duplo clique ou reenvio com a mesma chave de idempotência debita uma vez", "RN-02, RN-03", "suposição de erro (cobrança dupla)", "Alta",
     pre("D"),
     "1. Enviar a requisição de transferência duas vezes com a mesma chave de idempotência (e, pela tela, dar duplo clique em Confirmar). 2. Consultar saldo e extrato.",
     "Valor: R$ 100,00",
     "Um único débito de R$ 100,00 e um único EndToEndId; a segunda chamada devolve o mesmo resultado; saldo R$ 19.900,00; acumulado diurno R$ 100,00.")
caso(G6, "API recusa direto as violações que a tela bloqueia", "RN-01, RN-02, RN-03, RN-04", "suposição de erro (pular a tela)", "Alta",
     pre("D", clock="conforme cada dado"),
     "1. Enviar POST de transferência Pix direto na API, uma execução por dado. 2. Consultar saldo e extrato após cada execução.",
     "A: R$ 5.000,01 às 10:00:00. B: R$ 1.000,01 às 22:00:00. C: R$ 100,01 com saldo R$ 100,00. D: R$ 0,00",
     "Cada execução recusada com 4xx e motivo no corpo (limite diurno, limite noturno, saldo insuficiente, valor mínimo); nenhum débito.")
caso(G6, "Valor extremo recusado por limite, sem estouro numérico", "RN-03", "limite oculto (int32 em centavos)", "Média",
     pre("D", saldo="R$ 30.000.000,00"),
     "1. Enviar POST de transferência Pix com o valor informado. 2. Consultar saldo e extrato.",
     "Valor: R$ 21.474.836,48 (2^31 centavos)",
     "Recusada por limite diurno; sem erro 500; valor não vira negativo nem é truncado; saldo inalterado em R$ 30.000.000,00.")
caso(G6, "Limite diurno vale para a conta somando todos os canais", "RN-03", "suposição de erro (trocar de canal)", "Alta",
     pre("D", saldo="R$ 17.000,00", extras=["acumulado diurno R$ 3.000,00 feito pelo app"]),
     "1. Entrar no internet banking com o mesmo cliente. 2. Transferir o valor (PS).",
     "Canal: internet banking; valor R$ 2.000,01",
     "Recusada por limite diurno; saldo inalterado em R$ 17.000,00; acumulado R$ 3.000,00.",
     pendencia="P5")


def idx(n):
    return f"CT-PIX-{n:03d}"


def main():
    # CSV para o importador de testes do Xray: um teste por linha, um passo por teste
    with open(AQUI / "casos_pix_limites_xray.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(["Summary", "Description", "Test Type", "Priority", "Labels",
                    "Action", "Data", "Expected Result"])
        for n, c in enumerate(C, 1):
            labels = ["pix", "limites", c["grupo"]]
            if c["smoke"]:
                labels.append("smoke")
            if c["pendencia"]:
                labels.append("depende-" + c["pendencia"].lower())
            desc = [f"Regra: {c['rn']} ({'; '.join(RN[r.strip()] for r in c['rn'].split(','))}).",
                    f"Técnica: {c['tecnica']}.",
                    f"Pré-condição: {c['pre'][0]}"]
            if c["pendencia"]:
                desc.append(f"Depende da pergunta em aberto {c['pendencia']}: o resultado esperado usa a suposição declarada e deve ser reconfirmado.")
            prio = {"Alta": "High", "Média": "Medium", "Baixa": "Low"}[c["prio"]]
            w.writerow([f"{idx(n)} - {c['titulo']}", "\n".join(desc), "Manual", prio,
                        " ".join(labels), c["passos"].replace("(PS)", "(passo-padrão: abrir Pix > Transferir, informar chave e valor, confirmar com autenticação)"),
                        c["dados"], c["esperado"]])

    # tabela para o chat
    linhas = ["| ID | Cenário | Pré-condição | Passos | Dados | Resultado esperado | Prioridade | Técnica / regra |",
              "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for n, c in enumerate(C, 1):
        passos = "PS" if c["passos"] == PS else c["passos"]
        tec = f"{c['tecnica']}; {c['rn']}"
        if c["pendencia"]:
            tec += f"; **depende de {c['pendencia']}**"
        prio = c["prio"] + (" (smoke)" if c["smoke"] else "")
        linhas.append(f"| {idx(n)} | {c['titulo']} | {c['pre'][1]} | {passos} | {c['dados']} | {c['esperado']} | {prio} | {tec} |")
    (AQUI / "tabela_chat.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")

    from collections import Counter
    print(len(C), "casos", Counter(c["prio"] for c in C), "smoke:", sum(c["smoke"] for c in C))


if __name__ == "__main__":
    main()
