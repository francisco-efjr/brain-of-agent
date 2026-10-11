# Ledger append-only: esquema de exemplo, esboço executado e tabela de estados

Sumário: 1. Invariantes · 2. Esquema Postgres (esboço) · 3. Esboço executado (Python + SQLite) · 4. Reserva em duas fases · 5. Estorno e estorno parcial · 6. Tabela de estados de exemplo · 7. Saldo: derivado ou projeção

Rótulos: **Verificado (fabricante)** = TigerBeetle (V-46); **Inferido** = convergência de projetos e derivação do modelo (V-11); **Suposição** = regra do plugin. Conferido em 2026-10-10. Nenhuma biblioteca de ledger é recomendada; a API do TigerBeetle não se transfere, os princípios sim.

## 1. Invariantes (revise o esquema contra esta lista)

| # | Invariante | Rótulo |
| --- | --- | --- |
| 1 | Lançamentos imutáveis; sem `UPDATE` nem `DELETE` | Verificado (fabricante) |
| 2 | Valores inteiros na menor unidade; moeda junto | Verificado (fabricante) |
| 3 | Cada transação grava seus lançamentos de forma atômica e eles somam zero por moeda | Inferido (decorre do modelo débito = crédito no mesmo ledger) |
| 4 | Correção por lançamento de estorno ligado ao original (`reverses_txn`) | Inferido (medici, cfokit, Pablo-aps); imutabilidade é Verificada |
| 5 | Saldo é função do histórico; projeção reconstruível | Inferido |
| 6 | Saldo negativo impedido por restrição no banco; lock só em contas quentes | Inferido (TigerBeetle tem sinalizadores equivalentes, Verificado) |
| 7 | `recorded_at`, `effective_at` e período contábil separados | Inferido |
| 8 | Id da transação existe para idempotência (efeito único após resposta perdida) | Verificado (fabricante) |
| 9 | Reserva em duas fases: `pending`, depois `post`, `void` ou expiração, cada resolução nova | Verificado (fabricante) |
| 10 | Chamada externa fora de transação com lock | Inferido |

## 2. Esquema Postgres (esboço; não executado neste ambiente, valide em banco de teste)

```sql
CREATE TABLE accounts (
  id        text PRIMARY KEY,                 -- ex.: 'cliente:42', 'receita', 'a_receber:psp_x'
  currency  char(3) NOT NULL,                 -- ISO 4217; uma conta, uma moeda
  allow_negative boolean NOT NULL DEFAULT false
);

CREATE TABLE ledger_txns (
  txn_id        text PRIMARY KEY,             -- também a chave de idempotência da transação
  reverses_txn  text REFERENCES ledger_txns(txn_id),
  recorded_at   timestamptz NOT NULL DEFAULT now(),
  effective_at  timestamptz NOT NULL,         -- quando vale contabilmente
  period        text NOT NULL,                -- período contábil, ex.: '2026-10'
  external_ref  text,                         -- id do provedor, txid, e2eid
  CHECK (txn_id <> reverses_txn)
);

CREATE TABLE ledger_entries (
  id            bigserial PRIMARY KEY,
  txn_id        text   NOT NULL REFERENCES ledger_txns(txn_id),
  account_id    text   NOT NULL REFERENCES accounts(id),
  amount_minor  bigint NOT NULL CHECK (amount_minor <> 0),   -- débito positivo, crédito negativo
  currency      char(3) NOT NULL
);
CREATE INDEX ON ledger_entries (account_id);

-- Imutabilidade: bloquear UPDATE e DELETE por trigger (ou por permissões do papel da aplicação).
CREATE FUNCTION forbid_mutation() RETURNS trigger AS $$
BEGIN RAISE EXCEPTION 'ledger é append-only'; END $$ LANGUAGE plpgsql;
CREATE TRIGGER entries_immutable BEFORE UPDATE OR DELETE ON ledger_entries FOR EACH ROW EXECUTE FUNCTION forbid_mutation();
CREATE TRIGGER txns_immutable    BEFORE UPDATE OR DELETE ON ledger_txns    FOR EACH ROW EXECUTE FUNCTION forbid_mutation();

-- Soma zero por moeda: constraint trigger deferido, checado no COMMIT (esboço):
-- SELECT currency FROM ledger_entries WHERE txn_id = NEW.txn_id GROUP BY currency HAVING SUM(amount_minor) <> 0;
-- Saldo: SELECT COALESCE(SUM(amount_minor),0) FROM ledger_entries WHERE account_id = $1;
```

Decisões a registrar em ADR (`${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/adr-pagamentos.md`): proteção contra saldo negativo (constraint no saldo materializado versus verificação serializada contra o diário), contas quentes (lock por conta, fila por conta), projeção de saldo e invalidação, particionamento por período.

## 3. Esboço executado (Python 3 + sqlite3, stdlib)

Executado em 2026-10-10 em Python 3.14. Saídas observadas: alocação de R$ 100,00 em 3 pesos iguais deu `3334, 3333, 3333` (soma 10000); transação desbalanceada foi recusada (`BRL: 1`); `UPDATE` em lançamento foi bloqueado pelo trigger; após postar e estornar, o saldo da conta do cliente deu 0 com 4 linhas no histórico; `Money(1.5, "BRL")` levantou `TypeError`.

```python
import sqlite3
from dataclasses import dataclass

EXPOENTES = {"BRL": 2, "USD": 2, "JPY": 0, "KWD": 3}   # tabela de exemplo; confira ISO 4217 e as exceções do provedor

@dataclass(frozen=True)
class Money:
    minor: int            # inteiro na menor unidade
    currency: str         # ISO 4217
    def __post_init__(self):
        if not isinstance(self.minor, int) or isinstance(self.minor, bool): raise TypeError("minor precisa ser int")
        if self.currency not in EXPOENTES: raise ValueError("moeda fora da allowlist")
    def __add__(self, o):
        if o.currency != self.currency: raise ValueError("somar moedas exige câmbio explícito")
        return Money(self.minor + o.minor, self.currency)

def alocar(total: Money, pesos: list[int]) -> list[Money]:
    """Alocação sem perda: a soma das partes é exatamente o total; o resto vai para as maiores frações."""
    s = sum(pesos); partes = [total.minor * p // s for p in pesos]; resto = total.minor - sum(partes)
    ordem = sorted(range(len(pesos)), key=lambda i: (-((total.minor * pesos[i]) % s), i))
    for i in ordem[:resto]: partes[i] += 1
    return [Money(p, total.currency) for p in partes]

DDL = """
CREATE TABLE entries (id INTEGER PRIMARY KEY AUTOINCREMENT, txn_id TEXT NOT NULL, account TEXT NOT NULL,
  amount_minor INTEGER NOT NULL, currency TEXT NOT NULL, reverses_txn TEXT, recorded_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TRIGGER entries_no_update BEFORE UPDATE ON entries BEGIN SELECT RAISE(ABORT, 'ledger é append-only'); END;
CREATE TRIGGER entries_no_delete BEFORE DELETE ON entries BEGIN SELECT RAISE(ABORT, 'ledger é append-only'); END;
"""

def postar(db, txn_id, linhas, reverses=None):
    """linhas: [(conta, Money)] com sinal (débito positivo, crédito negativo); soma zero por moeda, atômico."""
    soma = {}
    for _, m in linhas: soma[m.currency] = soma.get(m.currency, 0) + m.minor
    if any(v != 0 for v in soma.values()): raise ValueError(f"transação não soma zero por moeda: {soma}")
    with db:
        for conta, m in linhas:
            db.execute("INSERT INTO entries(txn_id, account, amount_minor, currency, reverses_txn) VALUES (?,?,?,?,?)",
                       (txn_id, conta, m.minor, m.currency, reverses))

def estornar(db, txn_id, novo_id):
    orig = db.execute("SELECT account, amount_minor, currency FROM entries WHERE txn_id=?", (txn_id,)).fetchall()
    postar(db, novo_id, [(a, Money(-v, c)) for a, v, c in orig], reverses=txn_id)   # oposto, ligado ao original

def saldo(db, conta, moeda):
    return db.execute("SELECT COALESCE(SUM(amount_minor),0) FROM entries WHERE account=? AND currency=?", (conta, moeda)).fetchone()[0]
```

Limitações do esboço: o `estornar` estorna a transação inteira (estorno parcial: ver seção 5); não há controle de idempotência de `txn_id` (adicione `UNIQUE (txn_id, account)` ou uma tabela de transações); sem tratamento de concorrência de saldo (isso é teste de integração em banco de verdade, com duas conexões).

## 4. Reserva em duas fases (TigerBeetle, V-46, Verificado)

| Operação | Efeito |
| --- | --- |
| `pending` (com `timeout` em segundos) | reserva o valor em campos pendentes; **não** altera o saldo efetivo |
| `post` (total ou parcial) | nova transferência com `id` próprio que efetiva a reserva |
| `void` | nova transferência que libera a reserva |
| expiração | a reserva expira sozinha; não há alteração da pendente |

A pendente nunca é alterada; só se resolve uma vez (erros `already_posted`, `already_voided`, `expired`). A reserva garante que `post` ou `void` não violem os limites de saldo. Mapeamento típico em pagamentos: autorização do cartão = `pending`; captura = `post` (valor menor ou igual ao autorizado); cancelamento da autorização = `void`. Autorização não é dinheiro; captura não é liquidação (a liquidação é outra transação, quando o extrato confirma).

## 5. Estorno e estorno parcial

- Estorno total: lançamentos opostos ligados por `reverses_txn`.
- Parcial: lançamentos opostos de valor menor, ligados ao original; o saldo estornável é `original − soma(estornos já postados)`. Soma de estornos acima do original é recusada (teste obrigatório).
- Ordem das operações com o provedor: reserve a intenção de estorno (chave de idempotência persistida), chame o provedor, grave o lançamento só quando houver evidência (resposta, evento verificado ou consulta autenticada) e concilie depois; ver "Fluxo de estorno" em `reconciliation-disputes`.
- Disputa aberta bloqueia estorno fora do processo (Stripe, V-09).

## 6. Tabela de estados de exemplo (cartão; adapte, não copie)

| Estado | Evidência de entrada | Anteriores permitidos | Comandos | Timeout | Efeito no ledger | Compensação |
| --- | --- | --- | --- | --- | --- | --- |
| `created` | pedido válido | nenhum | autorizar | expirar em X | nenhum | cancelar pedido |
| `authorized` | resposta do provedor confirmada por consulta | `created` | capturar, cancelar | validade da autorização | `pending` (reserva) | `void` |
| `captured` | captura confirmada | `authorized` | estornar | nenhum | `post` | estorno ligado |
| `settled` | linha no extrato de liquidação | `captured` | estornar | nenhum | transação de liquidação | ajuste com aprovação |
| `refunded` / `partially_refunded` | estorno confirmado | `captured`, `settled` | nenhum | nenhum | lançamento oposto | n/a |
| `disputed` | evento de disputa verificado e relido | `captured`, `settled` | responder | prazo da bandeira (conferir) | débito da disputa | reversão se ganha |
| `unknown` | timeout sem resposta | qualquer estado com chamada em voo | consultar o provedor | prazo de consulta | nenhum até haver evidência | compensar sucesso tardio |

Regras: o estado final prevalece conforme a precedência de evidências (extrato > consulta > evento > resposta síncrona > comando); transição inválida ou obsoleta vai para conciliação; valores autorizado, capturado e estornado são colunas próprias.

## 7. Saldo: derivado ou projeção

- Derivado na leitura: simples e sempre correto; custo cresce com o histórico.
- Projeção reconstruível: coluna ou tabela atualizada na mesma transação do lançamento, com rotina de reconstrução e verificação periódica (`projeção = soma do histórico`); política de invalidação documentada. Teste: saldo reconstruído igual à projeção.
- Nunca uma coluna `balance` mutável como única fonte: apaga a trilha e reabre a corrida.
