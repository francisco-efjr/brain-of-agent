---
name: auth-jwt-bola
description: Mede se o plugin faz auditoria de segurança somente leitura de um trecho FastAPI e encontra algoritmo vindo do header, validação de aud desligada, BOLA e vazamento de campos, com severidade, cenário e correção, sem editar nada.
tags: [backend-api, api-security-review, security]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
timeout_seconds: 600
runs: 3
expected_outcome: "Relatório de auditoria com achados de algoritmo do header, aud desligado e falta de iss/exp, BOLA e saída sem DTO, cada um com severidade, evidência, cenário e correção, sem editar arquivos e com declaração do que não foi verificado."
model: sonnet
---
Revise a segurança deste trecho de uma API FastAPI consumida por uma SPA web e por um app mobile. É uma auditoria: quero o relatório de achados, não que você mexa no código.

```python
SECRET = "troque-me"

def current_user(token: str = Depends(oauth2_scheme)):
    h = jwt.get_unverified_header(token)
    payload = jwt.decode(token, SECRET, algorithms=[h["alg"]], options={"verify_aud": False})
    return db.query(User).get(payload["sub"])

@app.get("/orders/{order_id}")
def get_order(order_id: int, user=Depends(current_user)):
    return db.query(Order).filter(Order.id == order_id).first()
```

Não tenho o repositório aberto aqui; use só o que escrevi.
