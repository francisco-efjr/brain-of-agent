---
name: completo-explicito
description: "Mede o modo AUTOMACAO-COMPLETO pedido explicitamente pelo usuário: leitura em lotes registrada, matriz de aplicabilidade com NA justificado, relatório com evidências e revalidação, sem ampliar escopo."
tags: [automation-integrations, playbook, modo-completo, webhook, positivo]
runs: 3
max_turns: 24
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 900
expected_outcome: "Registra a leitura das referências em lotes com lido/parcial/ausente, apresenta matriz de aplicabilidade com NA justificado, relatório com evidências e rótulos epistêmicos e revalidação, sem alterar o projeto nem executar ações externas."
---
AUTOMACAO-COMPLETO. Revise a integração Stripe → planilha deste handler (Flask, Python 3.12). Só quero a revisão, não mude nada no projeto.

```python
import os
import stripe
from flask import Flask, request
from planilha import sheet   # wrapper do Google Sheets já configurado

app = Flask(__name__)

@app.route("/stripe", methods=["POST"])
def stripe_hook():
    event = stripe.Webhook.construct_event(
        request.data,
        request.headers["Stripe-Signature"],
        os.environ["STRIPE_SECRET"],
    )
    if event["type"] == "invoice.paid":
        obj = event["data"]["object"]
        sheet.append_row([obj["id"], obj["amount_paid"], obj["customer_email"]])
    return "", 200
```

Contexto: a planilha é usada pelo financeiro para conciliação mensal; o escritório fecha no dia 5 e já vi linhas repetidas.
