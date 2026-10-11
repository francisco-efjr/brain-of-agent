# Roteiro de testes hostis de webhook e handler de exemplo

Sumário: 1. Handler de exemplo executado · 2. Os 10 testes · 3. Como provar que o teste detecta o defeito · 4. Variações por provedor

Origem: V-05 (testes hostis: assinatura inválida, duplicado, fora de ordem, crash após efeito, evento envenenado, replay, rotação, falha de fila) e V-06 (válido, forjado, repetido, fora de ordem, ID desconhecido), corroborados por V-03. Redação e código próprios. O oráculo é o estado no banco, nunca o status HTTP. Dados sintéticos; segredo de teste `whsec_EXEMPLO_LOCAL` não é credencial real.

## 1. Handler de exemplo (Python 3, stdlib + sqlite3)

Executado em 2026-10-10 em Python 3.14 (Windows). Esquema de assinatura imitando o `v1` da Stripe (`t=<segundos>,v1=<hex>`, HMAC-SHA256 sobre `t.` + corpo bruto). **Confira o formato do cabeçalho na documentação vigente** antes de usar com um provedor real; para outro provedor, troque `assinar` e `verificar` conforme a matriz.

```python
import hashlib, hmac, json, sqlite3

SEGREDO = b"whsec_EXEMPLO_LOCAL"       # sintético; o real vem de cofre ou variável de ambiente
TOLERANCIA_S = 300                     # padrão da Stripe: 5 minutos (nunca 0)

def assinar(corpo: bytes, t: int, segredo: bytes = SEGREDO) -> str:       # só para TESTES locais
    return f"t={t},v1=" + hmac.new(segredo, f"{t}.".encode() + corpo, hashlib.sha256).hexdigest()

def verificar(corpo: bytes, cabecalho: str, agora: int, segredo: bytes = SEGREDO) -> bool:
    partes = dict(p.split("=", 1) for p in cabecalho.split(",") if "=" in p)
    try: t = int(partes["t"])
    except (KeyError, ValueError): return False
    if abs(agora - t) > TOLERANCIA_S: return False                          # replay fora da janela
    esperado = hmac.new(segredo, f"{t}.".encode() + corpo, hashlib.sha256).hexdigest()
    return hmac.compare_digest(esperado, partes.get("v1", ""))              # tempo constante

DDL = """CREATE TABLE inbox (event_id TEXT PRIMARY KEY, digest TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'received', body BLOB);
CREATE TABLE quarantine (event_id TEXT, digest TEXT);
CREATE TABLE effects (id INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT UNIQUE)"""

def receber(db, corpo: bytes, cabecalho: str, agora: int) -> int:
    if not verificar(corpo, cabecalho, agora):        # nada é parseado antes de verificar os bytes exatos
        return 400
    evento = json.loads(corpo)
    digest = hashlib.sha256(corpo).hexdigest()
    cur = db.execute("INSERT INTO inbox(event_id, digest, body) VALUES (?,?,?) ON CONFLICT(event_id) DO NOTHING",
                     (evento["id"], digest, corpo))
    if cur.rowcount == 0:                              # ID já visto
        antigo = db.execute("SELECT digest FROM inbox WHERE event_id=?", (evento["id"],)).fetchone()[0]
        if antigo != digest:                           # mesmo ID, conteúdo diferente: quarentena, não é duplicata
            db.execute("INSERT INTO quarantine VALUES (?,?)", (evento["id"], digest))
    db.commit()
    return 200                                         # 2xx antes da lógica pesada

def processar(db):
    """Varredura das linhas prontas (a fila é só despertador). Um efeito por event_id."""
    for (eid,) in db.execute("SELECT event_id FROM inbox WHERE status='received'").fetchall():
        # real: reler o recurso na API autenticada e passar pela máquina de estados com chave idempotente
        db.execute("INSERT OR IGNORE INTO effects(event_id) VALUES (?)", (eid,))
        db.execute("UPDATE inbox SET status='processed' WHERE event_id=?", (eid,))
    db.commit()
```

Resultado observado ao exercitar o handler (t = 1700000000; corpo `{"id":"evt_teste_001","type":"payment_intent.succeeded"}`):

| Cenário | Retorno |
| --- | --- |
| assinatura válida | 200 |
| mesmo evento de novo | 200 (sem novo efeito) |
| corpo com um byte a mais | 400 |
| mesmo evento 3600 s depois (replay) | 400 |
| assinada com outro segredo | 400 |
| mesmo `id`, `type` diferente, assinatura válida | 200, vai para `quarantine` |
| após `processar` duas vezes | `effects = 1`, `inbox = 1`, `quarantine = 1` |

## 2. Os 10 testes (adapte o oráculo ao seu esquema)

| # | Cenário | Esperado (oráculo no banco) |
| --- | --- | --- |
| 1 | Assinatura válida | aceito; uma linha em `inbox`; um efeito após o processamento |
| 2 | Assinatura forjada (outro segredo) ou corpo alterado em um byte | 4xx; nenhuma linha em `inbox`; zero efeito |
| 3 | Mesmo evento duas vezes (e uma terceira concorrente) | 2xx nas três; uma linha em `inbox`; um efeito |
| 4 | Eventos fora de ordem (por exemplo, falha antes de criação, ou estorno antes de captura) | estado final igual ao do recurso relido; nenhum estado regride; compensação registrada se necessário |
| 5 | Evento com ID desconhecido do pedido | gravado e levado a quarentena ou fila de revisão; nenhuma transição financeira |
| 6 | Crash entre gravar o efeito e marcar `processed` | no reinício, a varredura reprocessa a linha; `effects` continua com uma linha (chave única) |
| 7 | Evento envenenado (JSON válido, campo obrigatório ausente) | vai para DLQ ou `failed` com o motivo; as linhas seguintes continuam sendo processadas |
| 8 | Replay: evento antigo válido reenviado fora da tolerância | 4xx; zero efeito (verifique também que a tolerância não é 0 nem infinita) |
| 9 | Rotação de segredo: evento assinado com a chave anterior durante a janela | aceito dentro da janela; recusado depois dela |
| 10 | Falha da fila (despertador perdido) | a varredura processa as linhas `received` em até um intervalo; nenhuma linha fica para sempre `received` |

Extras quando aplicável: mesmo ID com digest diferente vai para `quarantine` (cenário da tabela acima); `Content-Type` ou charset incomum não muda os bytes verificados; corpo grande além do limite do framework é recusado, não truncado.

## 3. Como provar que o teste detecta o defeito

Registre no relatório a mutação manual feita e o resultado: (a) registre o middleware de JSON antes da rota e veja o teste 1 falhar com assinatura válida; (b) remova a restrição `PRIMARY KEY` de `inbox` ou `UNIQUE` de `effects` e veja o teste 3 falhar; (c) ponha a tolerância em infinito e veja o teste 8 falhar; (d) troque `compare_digest` por `==` apenas para constatar que o teste funcional não o pega (comparação em tempo constante é revisão de código, não teste funcional). Teste que passa com a proteção removida não prova nada.

## 4. Variações por provedor

- **Adyen padrão:** a assinatura vem em `additionalData.hmacSignature` e cobre a concatenação de campos selecionados; teste também um campo alterado (`value`) com o resto igual.
- **Asaas:** sem HMAC, o teste de "forjado" é cabeçalho `asaas-access-token` ausente ou errado; o corpo não é autenticado, logo releia o recurso antes de agir.
- **Pix com mTLS:** o teste de transporte (requisição sem certificado recusada) é de infraestrutura; no código, cubra dedupe por `endToEndId` e `txid` e a reconsulta antes de creditar.
- **Provedor sem assinatura documentada:** o teste 2 vira "corpo diz pago, API autenticada diz pendente: nada muda" (regra V-50).
