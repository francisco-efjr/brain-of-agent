---
name: pix-txid-valor-float
description: "Mede se o plugin revisa o rascunho de cobrança Pix e corrige o txid curto, o valor em float, a ausência de consulta após timeout e o webhook que marca pago sem releitura, rotulando limites regulatórios como Não verificados."
tags: [fintech-payments, pix-boleto-br, pix]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta txid inválido (26 a 35 alfanuméricos, único, nunca reutilizado), valor como string decimal com duas casas convertida na borda, consulta pelo txid antes de reenviar, webhook com dedupe por e2eid e releitura da cobrança, e marca limites, MED e prazos como Não verificado."
model: sonnet
---
Vou integrar cobrança Pix imediata com o meu PSP. Este é o rascunho em Python, o que está errado? O checkout é do app Android e do site.

```python
def criar_cobranca(order):
    txid = str(order.id)
    corpo = {
        "calendario": {"expiracao": 3600},
        "valor": {"original": order.total_cents / 100},
        "chave": CHAVE_PIX,
    }
    r = requests.put(f"{BASE}/cob/{txid}", json=corpo, headers=AUTH)
    return r.json()

@app.post("/pix/webhook")
def pix_webhook():
    for pix in request.json["pix"]:
        marcar_pago(pix["txid"])
    return "", 200
```

Não tenho o repositório aberto aqui; use só o que escrevi.
