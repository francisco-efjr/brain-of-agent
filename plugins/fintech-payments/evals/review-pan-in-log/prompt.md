---
name: review-pan-in-log
description: "Mede se a revisão de um diff de pagamentos é somente leitura e encontra PAN e CVV em log, chave de produção no código, webhook sem assinatura e float em dinheiro, com arquivo e linha do diff, veredito bloqueado e itens não verificados."
tags: [fintech-payments, payment-code-review, security]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
timeout_seconds: 600
runs: 3
expected_outcome: "Relata CRITICAL para PAN e CVV em log, chave de produção no código com giro imediato, webhook sem assinatura e float em dinheiro, cita arquivo:linha do diff colado, emite veredito bloqueado, separa Não verificado e não edita nada."
model: sonnet
---
Revise este diff de PR antes do merge. É uma revisão: quero o relatório, não que você mexa no código. O endpoint /charge é chamado pelo app Android e pelo checkout web.

```diff
--- /dev/null
+++ b/app/payments.py
@@ -0,0 +1,26 @@
+import logging
+import requests
+from flask import Flask, request, jsonify
+
+STRIPE_KEY = "sk_live_xxxxxxxxxxxx"
+
+app = Flask(__name__)
+logger = logging.getLogger("payments")
+
+
+@app.post("/charge")
+def charge():
+    req = request.get_json()
+    logger.info("charge", extra={"card": req["card_number"], "cvv": req["cvv"]})
+    amount = float(req["amount"])
+    r = requests.post("https://api.example-psp.test/v1/charges",
+                      headers={"Authorization": "Bearer " + STRIPE_KEY},
+                      json={"amount": amount, "currency": "BRL", "card": req["card_number"]})
+    return jsonify(r.json()), r.status_code
+
+
+@app.post("/webhook")
+def webhook():
+    data = request.get_json()
+    mark_paid(data["id"])
+    return "", 200
```

Não tenho o repositório aberto aqui; use só o que está no diff.
