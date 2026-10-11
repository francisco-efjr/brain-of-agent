#!/usr/bin/env python3
"""Gera o CSV (Xray) e a tabela markdown dos casos de teste de limites do PIX PF.

Uso: python3 gerar_casos.py
Saidas (na mesma pasta do script): casos-pix-limites-xray.csv e tabela.md
"""
import csv
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

ACAO_PADRAO = (
    "1. Entrar no app como o cliente PF da pre-condicao. "
    "2. Abrir PIX > Transferir e informar a chave PIX do destinatario. "
    "3. Informar o valor da coluna Data. "
    "4. Confirmar a transferencia com a autenticacao do app."
)

# (id, label, confirmar, cenario, saldo, enviado, horario, valor, esperado, prio, acao_override)
# saldo = saldo no momento da tentativa (ja descontado o que foi enviado antes)
# enviado = total de PIX efetivados no periodo antes da tentativa
CASOS = [
    # ---- Valor minimo / validacao de valor ----
    ("PIX-VAL-01", "PIX_Valor_Minimo", False, "Valor mínimo (R$ 0,01) é aceito",
     "20.000,00", "0,00", "10:00", "0,01",
     "Aprovada. Débito de R$ 0,01 (saldo final 19.999,99) e comprovante gerado.", "High", None),
    ("PIX-VAL-02", "PIX_Valor_Minimo", False, "Valor logo acima do mínimo (R$ 0,02) é aceito",
     "20.000,00", "0,00", "10:00", "0,02",
     "Aprovada. Débito de R$ 0,02 (saldo final 19.999,98).", "Medium", None),
    ("PIX-VAL-03", "PIX_Valor_Minimo", False, "Valor zero é rejeitado",
     "20.000,00", "0,00", "10:00", "0,00",
     "Rejeitada na validação (valor mínimo R$ 0,01). Nenhuma transação criada; saldo inalterado em 20.000,00.",
     "High", None),
    ("PIX-VAL-04", "PIX_Valor_Minimo", False, "Valor negativo é rejeitado",
     "20.000,00", "0,00", "10:00", "-0,01",
     "Rejeitada (app: campo não aceita o sinal; API: erro de validação). Nenhuma transação criada; saldo inalterado.",
     "Medium",
     "App: tentar digitar valor negativo. API: enviar o campo de valor com -0.01. Em ambos, tentar confirmar."),
    ("PIX-VAL-05", "PIX_Valor_Minimo", True, "Valor com mais de 2 casas decimais",
     "20.000,00", "0,00", "10:00", "10,005",
     "Não aceita a 3ª casa (máscara bloqueia ou API devolve erro). Nunca debita valor arredondado ou truncado sem o cliente ver.",
     "Medium",
     "App: tentar digitar 10,005. API: enviar o campo de valor com 10.005. Tentar confirmar."),
    ("PIX-VAL-06", "PIX_Valor_Minimo", False, "Valor vazio ou não numérico",
     "20.000,00", "0,00", "10:00", "(vazio) e \"abc\"",
     "Confirmar fica desabilitado ou há erro de validação de campo. Nenhuma transação criada.",
     "Low", None),

    # ---- Limite diurno (06:00-19:59:59) ----
    ("PIX-DIA-01", "PIX_Limite_Diurno", False, "Um centavo abaixo do limite diurno",
     "20.000,00", "0,00", "10:00", "4.999,99",
     "Aprovada. Saldo final 15.000,01.", "High", None),
    ("PIX-DIA-02", "PIX_Limite_Diurno", False, "Valor igual ao limite diurno",
     "20.000,00", "0,00", "10:00", "5.000,00",
     "Aprovada. Saldo final 15.000,00.", "High", None),
    ("PIX-DIA-03", "PIX_Limite_Diurno", False, "Um centavo acima do limite diurno",
     "20.000,00", "0,00", "10:00", "5.000,01",
     "Negada por limite diário excedido (mensagem de limite, não de saldo). Sem débito; saldo 20.000,00; nenhuma transação efetivada.",
     "High", None),
    ("PIX-DIA-04", "PIX_Limite_Diurno", False, "Acumulado do período diurno chega exatamente ao limite",
     "17.000,00", "3.000,00", "10:00", "2.000,00",
     "Aprovada. Total do período = 5.000,00; saldo final 15.000,00.", "High", None),
    ("PIX-DIA-05", "PIX_Limite_Diurno", False, "Acumulado do período diurno passa do limite em R$ 0,01",
     "17.000,00", "3.000,00", "10:00", "2.000,01",
     "Negada por limite (total seria 5.000,01). Sem débito; saldo 17.000,00.", "High", None),
    ("PIX-DIA-06", "PIX_Limite_Diurno", False, "Limite diurno esgotado bloqueia até o valor mínimo",
     "15.000,00", "5.000,00", "10:00", "0,01",
     "Negada por limite diário esgotado. Sem débito; saldo 15.000,00.", "High", None),
    ("PIX-DIA-07", "PIX_Limite_Diurno", False, "Limite acumula entre destinatários diferentes",
     "17.000,00", "3.000,00 (para o Cliente B)", "10:00", "2.000,01 (para o Cliente C)",
     "Negada por limite: o limite é do cliente pagador, não do par pagador/recebedor. Sem débito.",
     "Medium", None),
    ("PIX-DIA-08", "PIX_Limite_Diurno", False, "Tentativa negada não consome limite",
     "16.000,00", "4.000,00", "10:00", "1.500,00 e, em seguida, 1.000,00",
     "1ª negada por limite (total seria 5.500,00), sem débito. 2ª aprovada (total 5.000,00); saldo final 15.000,00.",
     "Medium",
     "Executar duas transferências em sequência: 1) valor 1.500,00; 2) valor 1.000,00. Conferir saldo e extrato após cada uma."),
    ("PIX-DIA-09", "PIX_Limite_Diurno", False, "Limite diurno renova no dia seguinte",
     "15.000,00", "5.000,00 no dia anterior (15:00)", "10:00 do dia seguinte", "5.000,00",
     "Aprovada (novo dia, limite cheio). Saldo final 10.000,00.", "Medium", None),

    # ---- Limite noturno (20:00-05:59:59) ----
    ("PIX-NOT-01", "PIX_Limite_Noturno", False, "Um centavo abaixo do limite noturno",
     "20.000,00", "0,00", "22:00", "999,99",
     "Aprovada. Saldo final 19.000,01.", "High", None),
    ("PIX-NOT-02", "PIX_Limite_Noturno", False, "Valor igual ao limite noturno",
     "20.000,00", "0,00", "22:00", "1.000,00",
     "Aprovada. Saldo final 19.000,00.", "High", None),
    ("PIX-NOT-03", "PIX_Limite_Noturno", False, "Um centavo acima do limite noturno",
     "20.000,00", "0,00", "22:00", "1.000,01",
     "Negada por limite noturno excedido. Sem débito; saldo 20.000,00.", "High", None),
    ("PIX-NOT-04", "PIX_Limite_Noturno", False, "Limite diurno (R$ 5.000,00) não vale à noite",
     "20.000,00", "0,00", "22:00", "5.000,00",
     "Negada por limite noturno. Sem débito; saldo 20.000,00.", "High", None),
    ("PIX-NOT-05", "PIX_Limite_Noturno", False, "Madrugada: valor igual ao limite noturno",
     "20.000,00", "0,00", "03:00", "1.000,00",
     "Aprovada. Saldo final 19.000,00.", "High", None),
    ("PIX-NOT-06", "PIX_Limite_Noturno", False, "Madrugada: um centavo acima do limite noturno",
     "20.000,00", "0,00", "03:00", "1.000,01",
     "Negada por limite noturno excedido. Sem débito; saldo 20.000,00.", "High", None),
    ("PIX-NOT-07", "PIX_Limite_Noturno", False, "Acumulado noturno chega exatamente ao limite",
     "19.400,00", "600,00 (às 21:00)", "23:30", "400,00",
     "Aprovada. Total do período noturno = 1.000,00; saldo final 19.000,00.", "Medium", None),
    ("PIX-NOT-08", "PIX_Limite_Noturno", False, "Acumulado noturno passa do limite em R$ 0,01",
     "19.400,00", "600,00 (às 21:00)", "23:30", "400,01",
     "Negada por limite noturno (total seria 1.000,01). Sem débito; saldo 19.400,00.", "High", None),
    ("PIX-NOT-09", "PIX_Limite_Noturno", True, "Acumulado noturno atravessa a meia-noite",
     "19.300,00", "700,00 (às 23:50 do dia D)", "00:10 do dia D+1 e 01:00 do dia D+1",
     "300,00 e, em seguida, 0,01",
     "300,00 aprovada (total 1.000,00 no mesmo período noturno). 0,01 negada por limite noturno. Saldo final 19.000,00.",
     "Medium",
     "Às 00:10 (D+1) transferir 300,00; às 01:00 (D+1) transferir 0,01. Conferir saldo e extrato após cada uma."),

    # ---- Fronteiras de horario (valor 1.500,00: acima do noturno, abaixo do diurno) ----
    ("PIX-HOR-01", "PIX_Horario_Fronteira", False, "05:59:59 aplica o limite noturno",
     "20.000,00", "0,00", "05:59:59", "1.500,00",
     "Negada por limite noturno (1.500,00 > 1.000,00). Sem débito.", "High", None),
    ("PIX-HOR-02", "PIX_Horario_Fronteira", True, "06:00:00 aplica o limite diurno",
     "20.000,00", "0,00", "06:00:00", "1.500,00",
     "Aprovada (limite diurno). Saldo final 18.500,00.", "High", None),
    ("PIX-HOR-03", "PIX_Horario_Fronteira", False, "06:00:01 aplica o limite diurno",
     "20.000,00", "0,00", "06:00:01", "1.500,00",
     "Aprovada. Saldo final 18.500,00.", "Medium", None),
    ("PIX-HOR-04", "PIX_Horario_Fronteira", False, "19:59:59 aplica o limite diurno",
     "20.000,00", "0,00", "19:59:59", "1.500,00",
     "Aprovada. Saldo final 18.500,00.", "High", None),
    ("PIX-HOR-05", "PIX_Horario_Fronteira", True, "20:00:00 aplica o limite noturno",
     "20.000,00", "0,00", "20:00:00", "1.500,00",
     "Negada por limite noturno. Sem débito.", "High", None),
    ("PIX-HOR-06", "PIX_Horario_Fronteira", False, "20:00:01 aplica o limite noturno",
     "20.000,00", "0,00", "20:00:01", "1.500,00",
     "Negada por limite noturno. Sem débito.", "Medium", None),
    ("PIX-HOR-07", "PIX_Horario_Fronteira", False, "Virada de data (00:00:00) mantém o limite noturno",
     "20.000,00", "0,00", "00:00:00", "1.500,00",
     "Negada por limite noturno. Sem débito.", "Medium", None),
    ("PIX-HOR-08", "PIX_Horario_Fronteira", True, "Fluxo iniciado no diurno e confirmado no noturno",
     "20.000,00", "0,00", "abre a tela 19:59:30; confirma 20:00:10", "1.500,00",
     "Negada por limite noturno: a regra vale na hora da confirmação, não da abertura da tela. Sem débito.",
     "Medium",
     "1. Às 19:59:30, abrir PIX > Transferir, preencher chave e valor, e parar na tela de confirmação. 2. Aguardar até 20:00:10 e confirmar."),
    ("PIX-HOR-09", "PIX_Horario_Fronteira", True, "Relógio do aparelho diferente do horário oficial",
     "20.000,00", "0,00", "servidor 22:00; aparelho ajustado para 10:00", "1.500,00",
     "Negada por limite noturno: vale o horário do servidor (Brasília), não o do aparelho. Sem débito.",
     "Medium",
     "1. Ajustar manualmente o relógio do aparelho para 10:00 com o servidor em 22:00. 2. Executar a transferência."),

    # ---- Transicao entre janelas ----
    ("PIX-JAN-01", "PIX_Janelas", True, "Limite diurno esgotado não bloqueia o noturno",
     "15.000,00", "5.000,00 (às 15:00)", "21:00", "1.000,00",
     "Aprovada (o limite noturno tem saldo próprio). Saldo final 14.000,00.", "High", None),
    ("PIX-JAN-02", "PIX_Janelas", True, "Limite noturno independe do uso diurno parcial",
     "17.000,00", "3.000,00 (às 15:00)", "21:00 e 21:05", "1.000,00 e, em seguida, 0,01",
     "1.000,00 aprovada. 0,01 negada (limite noturno esgotado). Saldo final 16.000,00.", "Medium",
     "Às 21:00 transferir 1.000,00; às 21:05 transferir 0,01. Conferir saldo e extrato após cada uma."),
    ("PIX-JAN-03", "PIX_Janelas", True, "Uso na madrugada não consome o limite diurno do mesmo dia",
     "19.000,00", "1.000,00 (às 02:00; limite noturno esgotado)", "10:00 do mesmo dia", "5.000,00",
     "Aprovada (limite diurno cheio). Saldo final 14.000,00.", "Medium", None),

    # ---- Saldo ----
    ("PIX-SAL-01", "PIX_Saldo", False, "Saldo exatamente igual ao valor",
     "100,00", "0,00", "10:00", "100,00",
     "Aprovada. Saldo final 0,00.", "High", None),
    ("PIX-SAL-02", "PIX_Saldo", False, "Saldo um centavo abaixo do valor",
     "99,99", "0,00", "10:00", "100,00",
     "Negada por saldo insuficiente. Sem débito; saldo 99,99; nenhuma transação efetivada.", "High", None),
    ("PIX-SAL-03", "PIX_Saldo", False, "Saldo zerado com valor mínimo",
     "0,00", "0,00", "10:00", "0,01",
     "Negada por saldo insuficiente. Saldo permanece 0,00 (nunca negativo).", "Medium", None),
    ("PIX-SAL-04", "PIX_Saldo", False, "Saldo cobre o valor, mas o limite diurno não",
     "10.000,00", "0,00", "10:00", "5.000,01",
     "Negada por limite diário (não por saldo). Sem débito; saldo 10.000,00.", "High", None),
    ("PIX-SAL-05", "PIX_Saldo", False, "Valor dentro do limite, mas saldo não cobre",
     "500,00", "0,00", "10:00", "1.000,00",
     "Negada por saldo insuficiente (mensagem de saldo). Sem débito; saldo 500,00.", "High", None),
    ("PIX-SAL-06", "PIX_Saldo", True, "Valor acima do limite e acima do saldo ao mesmo tempo",
     "100,00", "0,00", "10:00", "6.000,00",
     "Negada. Sem débito; saldo 100,00. Mensagem exibida: confirmar qual tem precedência (limite ou saldo).",
     "Low", None),
    ("PIX-SAL-07", "PIX_Saldo", False, "Tentativa negada por saldo não consome limite",
     "1.000,00 (depois 10.000,00)", "0,00", "10:00", "3.000,00; após creditar 9.000,00, 5.000,00",
     "1ª negada por saldo insuficiente. 2ª aprovada (limite diurno intacto); saldo final 5.000,00.", "Medium",
     "1. Transferir 3.000,00 (saldo 1.000,00). 2. Creditar 9.000,00 na conta (saldo 10.000,00). 3. Transferir 5.000,00."),
    ("PIX-SAL-08", "PIX_Saldo", False, "Saldo, valor e limite diurno coincidem",
     "5.000,00", "0,00", "10:00", "5.000,00",
     "Aprovada. Saldo final 0,00.", "Medium", None),

    # ---- Concorrencia ----
    ("PIX-CON-01", "PIX_Concorrencia", False, "Duas PIX simultâneas estouram o limite diurno",
     "20.000,00", "0,00", "10:00", "2 x 3.000,00 em paralelo",
     "Apenas uma aprovada; a outra negada por limite. Total efetivado 3.000,00; saldo final 17.000,00.", "High",
     "Disparar duas requisições de PIX de 3.000,00 do mesmo cliente ao mesmo tempo (API ou dois dispositivos). Conferir extrato."),
    ("PIX-CON-02", "PIX_Concorrencia", False, "Duas PIX simultâneas estouram o saldo",
     "1.000,00", "0,00", "10:00", "2 x 1.000,00 em paralelo",
     "Apenas uma aprovada; a outra negada por saldo insuficiente. Saldo final 0,00, nunca negativo.", "High",
     "Disparar duas requisições de PIX de 1.000,00 do mesmo cliente ao mesmo tempo (API ou dois dispositivos). Conferir extrato."),
]


def precondicao(c):
    _id, _lab, conf, cen, saldo, env, hora, valor, esp, prio, acao = c
    linhas = [
        "Cliente PF autenticado, conta ativa, sem bloqueios. Destinatário com chave PIX válida.",
        f"Saldo disponível no momento da tentativa: R$ {saldo}.",
        "PIX já efetivados no período: " + ("nenhum." if env == "0,00" else f"R$ {env}."),
        f"Horário (Brasília, relógio do servidor): {hora}.",
    ]
    if conf:
        linhas.append("ATENÇÃO: o resultado esperado depende de definição pendente (ver premissas). Confirmar com PO/negócio antes de executar.")
    linhas.append("Premissas: limites inclusivos; diurno 06:00:00-19:59:59 (R$ 5.000,00); noturno 20:00:00-05:59:59 (R$ 1.000,00); limite acumulado por janela; saldo = disponível, sem cheque especial.")
    return "\n".join(linhas)


def gerar_csv():
    caminho = os.path.join(AQUI, "casos-pix-limites-xray.csv")
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(["Summary", "Description", "Test Type", "Priority", "Labels", "Action", "Data", "Expected Result"])
        for c in CASOS:
            _id, lab, conf, cen, saldo, env, hora, valor, esp, prio, acao = c
            resumo = f"{_id} | " + ("[CONFIRMAR] " if conf else "") + cen
            dados = f"Valor: R$ {valor} | Horário: {hora} | Saldo: R$ {saldo} | Já enviado no período: " + ("nenhum" if env == "0,00" else f"R$ {env}")
            w.writerow([resumo, precondicao(c), "Manual", prio, lab, acao or ACAO_PADRAO, dados, esp])
    return caminho


def gerar_md():
    cab = "| ID | Cenário | Saldo (R$) | Já enviado no período (R$) | Horário | Valor (R$) | Resultado esperado | Prio |\n"
    cab += "|---|---|---|---|---|---|---|---|\n"
    linhas = []
    for c in CASOS:
        _id, lab, conf, cen, saldo, env, hora, valor, esp, prio, acao = c
        cen_txt = ("**[CONFIRMAR]** " if conf else "") + cen
        env_txt = "—" if env == "0,00" else env
        linhas.append(f"| {_id} | {cen_txt} | {saldo} | {env_txt} | {hora} | {valor} | {esp} | {prio} |")
    caminho = os.path.join(AQUI, "tabela.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(cab + "\n".join(linhas) + "\n")
    return caminho


if __name__ == "__main__":
    ids = [c[0] for c in CASOS]
    assert len(ids) == len(set(ids)), "IDs duplicados"
    print(gerar_csv())
    print(gerar_md())
    print(len(CASOS), "casos")
