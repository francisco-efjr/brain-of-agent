# Receptor de referência e replay (stdlib, testado)

Redação própria. O receptor e o replay abaixo foram **executados em 2026-10-10 durante a construção do plugin** (Python 3 stdlib, `127.0.0.1`, segredo de teste): 4 casos do replay, todos `OK` (válido 202, duplicado 200, assinatura inválida 400, timestamp antigo 400), mais duas verificações manuais após a revisão de qualidade: corpo assinado mas malformado devolve 400, e fila indisponível devolve 503, remove o ID reservado e permite que o reenvio seguinte seja aceito (202) e o seguinte seja duplicado (200). O esquema de assinatura é um exemplo no estilo "`t=<unix>,v1=<hex>` sobre `t.corpo`"; para provedor real use o esquema e o SDK dele (ver [provedores.md](provedores.md)). A fila é em memória só para demonstração: em produção use fila durável.

Sumário: 1. Receptor · 2. Replay · 3. Estados do evento · 4. Adaptação ao Express · 5. Limites.

## 1. Receptor (Python, sem dependências)

```python
#!/usr/bin/env python3
import hashlib, hmac, json, os, queue, sqlite3, time
from http.server import BaseHTTPRequestHandler, HTTPServer

SECRET = os.environ["WEBHOOK_SECRET"].encode()       # segredo só por variável de ambiente (W-10)
TOLERANCE = 300                                       # segundos; nunca 0 (W-02)
MAX_BODY = 1_000_000
JOBS = queue.Queue()                                  # produção: fila durável (SQS, Redis, tabela)
enqueue = JOBS.put                                    # ponto de troca; os testes substituem por uma função que falha
DB = sqlite3.connect(os.environ.get("DEDUPE_DB", "events.db"), check_same_thread=False)
DB.execute("CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, status TEXT NOT NULL)")


def signature_ok(raw: bytes, header: str) -> bool:
    try:
        parts = dict(p.split("=", 1) for p in header.split(","))
        ts = int(parts["t"])
    except (ValueError, KeyError):
        return False
    if abs(time.time() - ts) > TOLERANCE:              # recência
        return False
    expected = hmac.new(SECRET, f"{ts}.".encode() + raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, parts.get("v1", ""))   # tempo constante


class Handler(BaseHTTPRequestHandler):
    def _reply(self, code, msg=""):
        self.send_response(code); self.end_headers(); self.wfile.write(msg.encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > MAX_BODY:
            return self._reply(413)
        raw = self.rfile.read(length)                  # W-01: corpo bruto, antes de qualquer parse
        if not signature_ok(raw, self.headers.get("X-Signature", "")):   # W-02
            return self._reply(400, "assinatura invalida")              # 4xx: retry não ajuda
        try:
            event = json.loads(raw)                    # assinatura válida: o JSON veio do provedor
            event_id = str(event["id"])
        except (ValueError, KeyError, TypeError):
            return self._reply(400, "corpo invalido")  # 4xx: retry não conserta formato
        cur = DB.execute("INSERT OR IGNORE INTO events (id, status) VALUES (?, 'received')",
                         (event_id,))                  # W-03: unicidade no banco
        DB.commit()
        if cur.rowcount == 0:
            return self._reply(200, "duplicado")       # já visto: 2xx, sem novo efeito
        try:
            enqueue(event)                             # W-04/W-05: trabalho fora da requisição
        except Exception:
            DB.execute("DELETE FROM events WHERE id = ? AND status = 'received'", (event_id,))
            DB.commit()                                # não deixe o ID "visto" sem job: o retry do provedor precisa passar
            return self._reply(503, "fila indisponivel")   # 5xx provoca retry
        return self._reply(202)

    def log_message(self, fmt, *args):                 # W-08: método, rota e código; nunca segredo/corpo
        print("webhook", self.command, self.path, args[1] if len(args) > 1 else "", flush=True)


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", int(os.environ.get("PORT", "8099"))), Handler).serve_forever()
```

## 2. Replay (contra receptor local)

```python
#!/usr/bin/env python3
"""Uso: WEBHOOK_SECRET=teste python replay.py http://127.0.0.1:8099/"""
import hashlib, hmac, json, os, sys, time, urllib.error, urllib.request

URL = sys.argv[1]
SECRET = os.environ["WEBHOOK_SECRET"].encode()


def post(body: bytes, ts: int, secret: bytes = SECRET) -> int:
    sig = hmac.new(secret, f"{ts}.".encode() + body, hashlib.sha256).hexdigest()
    req = urllib.request.Request(URL, data=body, method="POST",
                                 headers={"X-Signature": f"t={ts},v1={sig}", "Content-Type": "application/json"})
    try:
        return urllib.request.urlopen(req, timeout=5).status
    except urllib.error.HTTPError as err:
        return err.code


now = int(time.time())
event = json.dumps({"id": f"evt_{now}", "type": "invoice.paid"}).encode()
cases = [
    ("valido", lambda: post(event, now), {200, 202}),
    ("duplicado (mesmo id)", lambda: post(event, now), {200}),
    ("assinatura invalida", lambda: post(event, now, secret=b"errado"), {400, 401, 403}),
    ("timestamp antigo", lambda: post(json.dumps({"id": "evt_old"}).encode(), now - 3600), {400, 401, 403}),
]
failed = 0
for name, run, expected in cases:
    code = run()
    ok = code in expected
    failed += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {name}: HTTP {code} (esperado {sorted(expected)})")
sys.exit(1 if failed else 0)
```

Execução (dois terminais, ambos no seu ambiente de teste; use um segredo de teste, nunca o de produção):

```bash
WEBHOOK_SECRET=teste PORT=8099 python receiver.py
WEBHOOK_SECRET=teste python replay.py http://127.0.0.1:8099/
```

O receptor já trata fila indisponível (5xx, ID liberado para o retry) e corpo assinado porém malformado (400), mas o script de replay não os exercita: troque `enqueue` por uma função que levanta exceção para simular a fila fora do ar. Acrescente ao replay do receptor real: corpo com espaços e ordem de chaves diferentes, assinado sobre os bytes enviados (esperado 2xx), corpo alterado depois de assinado (esperado 4xx), corpo acima do limite (413), `Content-Type` inesperado.

## 3. Estados do evento (Inferido; padrão de idempotência)

| Estado | Quando | Efeito de um reenvio |
| --- | --- | --- |
| `received` | ID gravado na entrada, antes da fila | duplicata concorrente: 2xx sem novo job |
| `processed` | worker concluiu o efeito e atualizou a linha | reenvio: 2xx sem efeito |
| `failed` | esgotou tentativas, foi para a fila de mortas | reenvio manual passa pelo mesmo caminho e reabre para `received` |

Se o efeito vive no mesmo banco, faça dedupe e efeito na mesma transação e use um só estado. Se o efeito é externo (e-mail, API de terceiro), use a chave de idempotência do destino quando existir (I-06) e trate `received` há muito tempo como candidato a reprocesso.

## 4. Armadilha do Express (Inferido; não executado)

```js
// ERRADO: o parser global roda antes e a rota perde o corpo bruto.
// app.use(express.json());
// app.post("/webhooks/x", (req, res) => { verify(JSON.stringify(req.body)) });   // bytes diferentes

// CERTO: parser bruto só nesta rota, registrado ANTES de qualquer express.json() global.
app.post("/webhooks/x", express.raw({ type: "application/json", limit: "1mb" }), (req, res) => {
  const raw = req.body;                       // Buffer com os bytes originais
  if (!verifySignature(raw, req.get("X-Signature"))) return res.sendStatus(400);
  const event = JSON.parse(raw.toString("utf8"));
  // dedupe por event.id com restrição UNIQUE; enfileirar; responder 2xx
  res.sendStatus(202);
});
```

Compare assinaturas com `crypto.timingSafeEqual` (comprimentos iguais) e prefira o SDK do provedor. Outros frameworks têm o mesmo problema com nomes diferentes (`request.get_data()` no Flask antes de `get_json()`, `Request.body()` no FastAPI/Starlette antes de `.json()`): leia o corpo bruto uma vez, verifique e só então parseie.

## 5. Limites do exemplo

- Não implementa fila durável, retry do worker nem fila de mortas: são o passo 5 da skill.
- Um servidor `http.server` não é para produção; ele existe para provar a lógica de W-01 a W-04 e W-08.
- Allowlist de IP, TLS e CSRF pertencem à camada de borda/framework e não são exercitados aqui.
