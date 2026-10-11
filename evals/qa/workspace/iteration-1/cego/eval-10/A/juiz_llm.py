"""Juiz LLM para fidelidade (a resposta se sustenta nos trechos?) + calibração contra revisão humana.

Não faz chamada de rede: implemente `chamar_llm` com o SDK/gateway que vocês usam.
Use um modelo juiz DIFERENTE do que gera as respostas, temperatura 0, e SEMPRE calibre (função `calibrar`)
com ~100 casos rotulados por pessoas antes de confiar na nota.
"""
import json

PROMPT_FIDELIDADE = """Você é um auditor de qualidade de um banco digital. Avalie APENAS se a RESPOSTA está
sustentada pelos TRECHOS da base de FAQ. Ignore se a resposta é bem escrita.

TRECHOS:
{trechos}

PERGUNTA DO CLIENTE:
{pergunta}

RESPOSTA DO BOT:
{resposta}

Liste cada afirmação factual da resposta (valores, prazos, passos, condições) e diga se está nos trechos.
Responda SOMENTE com JSON:
{{"afirmacoes": [{{"texto": "...", "sustentada": true|false, "trecho": "id ou null"}}],
  "inventou_valor_ou_prazo": true|false,
  "deu_conselho_financeiro": true|false,
  "veredito": "fiel" | "parcial" | "infiel"}}"""


def chamar_llm(prompt: str) -> str:  # <- preencher
    raise NotImplementedError("Conecte ao seu provedor de LLM (modelo juiz, temperatura 0).")


def julgar(pergunta: str, resposta: str, trechos: dict) -> dict:
    t = "\n".join(f"[{i}] {txt}" for i, txt in trechos.items())
    bruto = chamar_llm(PROMPT_FIDELIDADE.format(trechos=t, pergunta=pergunta, resposta=resposta))
    return json.loads(bruto)


def calibrar(humano: list, juiz: list) -> dict:
    """humano/juiz: listas de 'fiel'/'parcial'/'infiel' alinhadas por caso.
    A métrica que mais importa: falso_aprovado = juiz disse 'fiel' e a pessoa disse que não."""
    n = len(humano)
    concordancia = sum(h == j for h, j in zip(humano, juiz)) / n
    ruins = [(h, j) for h, j in zip(humano, juiz) if h != "fiel"]
    falso_aprovado = sum(j == "fiel" for _, j in ruins) / len(ruins) if ruins else 0.0
    return {"concordancia": concordancia, "falso_aprovado": falso_aprovado, "n": n}
