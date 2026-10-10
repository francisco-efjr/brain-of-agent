---
name: seguranca-completo-explicito
description: Mede o modo SEGURANCA-COMPLETO pedido explicitamente. Verifica leitura em lotes com registro lido/parcial/ausente, matriz de aplicabilidade, achados de autenticação e sessão com arquivo:linha, separação entre leitura e execução, cobertura de plataforma web e Android e auditoria sem correção fora do escopo.
tags: [security-appsec, playbook, modo-completo, autenticacao, sessao, mobile]
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 1200
runs: 3
expected_outcome: "Declara o modo ativo por pedido explícito, apresenta registro de arquivos lidos/parciais/ausentes e matriz de aplicabilidade, reporta hash MD5, enumeração de usuário, ausência de limite de tentativas, token de reset previsível na URL e sessão em localStorage e em preferências do Android com arquivo:linha, separa lido de executado, termina com status completo ou parcial e não corrige código."
model: sonnet
---
SEGURANCA-COMPLETO: audite este módulo de login. É o backend Flask que atende o site (SPA) e o app Android do mesmo produto. Quero um relatório de auditoria, não correção de código. Segue o que tenho aqui:

```python
# auth.py
import hashlib, secrets, time
from flask import Blueprint, request, jsonify
from .db import get_db
from .mail import send_mail

bp = Blueprint("auth", __name__)

@bp.post("/login")
def login():
    d = request.get_json()
    db = get_db()
    row = db.execute("SELECT id, pw_hash FROM users WHERE email = ?", (d["email"],)).fetchone()
    if row is None:
        return jsonify(error="usuário não encontrado"), 404
    if hashlib.md5(d["password"].encode()).hexdigest() != row["pw_hash"]:
        return jsonify(error="senha incorreta"), 401
    token = secrets.token_hex(16)
    db.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, row["id"]))
    return jsonify(token=token, user_id=row["id"])

@bp.post("/forgot")
def forgot():
    email = request.get_json()["email"]
    token = str(int(time.time()))
    get_db().execute("UPDATE users SET reset_token = ? WHERE email = ?", (token, email))
    send_mail(email, f"https://app.exemplo.test/reset?token={token}&email={email}")
    return jsonify(ok=True)
```

```javascript
// static/app.js (linha 31)
localStorage.setItem("session", data.token);
```

```kotlin
// SessionStore.kt (linha 18) - app Android
prefs.edit().putString("session", token).apply()
```
