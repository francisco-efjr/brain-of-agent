"""Bot de EXEMPLO (ingênuo, sem LLM) só para o harness rodar de ponta a ponta.

Troque `responder()` por uma chamada ao SEU pipeline (retriever + LLM).
O contrato que o harness espera está documentado em `responder`.

FAQ e valores abaixo são fictícios.
"""
import re
import unicodedata

FAQ = {
    "faq-pix-001": "Limite do Pix noturno: entre 20h e 6h o limite por transação é de R$ 1.000,00. "
                   "Você pode ajustar em Configurações > Limites do Pix; aumentos têm carência de 24 horas.",
    "faq-cartao-002": "Bloqueio de cartão: pelo app, em Cartões > Bloquear temporariamente. "
                      "Em caso de perda ou roubo, bloqueie e solicite um novo cartão; ele chega em até 7 dias úteis.",
    "faq-tarifa-003": "Tarifas: a conta não tem mensalidade. Saque na rede parceira: 4 saques gratuitos por mês; "
                      "a partir do quinto, R$ 6,50 por saque.",
    "faq-fatura-004": "Fatura do cartão: vence no dia escolhido (5, 10, 15 ou 20). Você pode antecipar o pagamento pelo app. "
                      "Pagamento após o vencimento gera multa de 2% e juros de mora.",
    "faq-contestacao-005": "Compra não reconhecida: abra em Cartões > Fatura > Contestar. "
                           "Prazo de resposta: até 10 dias úteis.",
    "faq-conta-006": "Encerramento de conta: peça em Perfil > Encerrar conta, desde que não haja saldo ou pendências.",
    "faq-seguranca-007": "O banco nunca pede senha, token ou código por telefone, WhatsApp ou e-mail. "
                         "Em caso de contato suspeito, não informe nada, encerre e fale conosco pelo app.",
}

FALLBACK = ("Não encontrei essa informação na nossa central de ajuda. "
            "Posso te transferir para um atendente humano?")
GATILHOS_URGENCIA = ("fraude", "golpe", "clonado", "roubaram", "roubado", "perdi meu cartao", "cartao perdido")
STOP = {"de", "do", "da", "o", "a", "e", "que", "um", "uma", "meu", "minha", "para", "pra", "com", "por",
        "no", "na", "em", "eu", "se", "como", "faco", "qual", "quanto", "posso", "ele", "ela", "e", "é"}


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def _tokens(s: str) -> set:
    return {t for t in re.findall(r"[a-z0-9]+", _norm(s)) if t not in STOP and len(t) > 2}


def _buscar(pergunta: str, k: int = 3):
    q = _tokens(pergunta)
    pontuados = sorted(((len(q & _tokens(txt)), fid) for fid, txt in FAQ.items()), reverse=True)
    return [(sc, fid) for sc, fid in pontuados[:k] if sc > 0]


def responder(pergunta: str, historico=None) -> dict:
    """Contrato do adaptador (é isso que o harness consome):

    retorna {
      "resposta": str,
      "fontes_recuperadas": [ids dos trechos devolvidos pelo retriever, em ordem de relevância],
      "fontes_citadas": [ids que a resposta diz ter usado],
      "escalou_humano": bool,   # ofereceu/fez transferência para atendente
    }
    Este exemplo IGNORA `historico` de propósito (falha clássica de conversa com várias mensagens).
    """
    q = _norm(pergunta)
    achados = _buscar(pergunta)
    recuperadas = [fid for _, fid in achados]

    if any(g in q for g in GATILHOS_URGENCIA):
        return {"resposta": "Sinto muito por isso. " + FAQ["faq-cartao-002"] + " Vou te transferir para um atendente agora.",
                "fontes_recuperadas": recuperadas or ["faq-cartao-002"], "fontes_citadas": ["faq-cartao-002"],
                "escalou_humano": True}

    # Falha ingênua proposital: ecoa o CPF que o cliente digitou ("confirmando seus dados...").
    cpf = re.search(r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}", pergunta)
    prefixo = f"Confirmei o CPF {cpf.group(0)}. " if cpf else ""

    if not achados:
        return {"resposta": prefixo + FALLBACK, "fontes_recuperadas": [], "fontes_citadas": [], "escalou_humano": True}

    melhor = achados[0][1]
    return {"resposta": prefixo + FAQ[melhor], "fontes_recuperadas": recuperadas,
            "fontes_citadas": [melhor], "escalou_humano": False}
