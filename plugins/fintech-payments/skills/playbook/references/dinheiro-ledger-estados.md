# Dinheiro, ledger e máquina de estados

Base: V-10, V-11, V-12, V-13, V-46, V-59, V-60, V-61. Rótulos: o que é de fabricante (TigerBeetle, Stripe, Python, Oracle) está **Verificado**; "soma zero por moeda", projeção de saldo reconstruível, `effective_at`, precedência de evidências e alocação são **Inferido** ou regra do plugin. Redação própria; os exemplos de código e SQL são do plugin (MIT).

## Sumário

1. Tipo `Money` e conversão na borda
2. Expoentes, mínimos e máximos por moeda
3. Arredondamento e alocação
4. Regras por linguagem (Python, Java) e vetores de teste
5. Ledger append-only (Inferido, com fonte de fabricante nos pontos marcados)
6. Esquema de exemplo e invariantes verificáveis
7. Reserva em duas fases
8. Máquina de estados e precedência de evidências
9. Gotchas

## 1. Tipo `Money` e conversão na borda

- `Money = inteiro na menor unidade + código ISO 4217`, sempre juntos. Dinheiro sem moeda é achado de revisão. Nunca some moedas diferentes sem câmbio explícito e registrado (Fowler, V-10).
- Internamente: inteiro (64 bits comporta centavos de valores muito acima do necessário; TigerBeetle usa 128 bits sem sinal, V-46). "Nunca float" é prática comum apoiada em V-10 e V-11 (**Inferido**); a redação correta da regra de JSON é "nunca ponto flutuante no JSON" (a fonte moneyproof se contradiz ao dizer "nunca números JSON", V-13).
- Na **borda**, converta para a representação do canal: Stripe e a maioria das APIs usam a menor unidade (1099 = USD 10,99; 10 = JPY 10); o Pix usa **string decimal** `\d{1,10}\.\d{2}` (`"10.00"`); relatórios e telas usam formatação local (`R$ 1.234,56`, com U+00A0 após `R$` em alguns locales: teste a formatação).

```python
from decimal import Decimal

def to_minor(amount: str, exp: int) -> int:
    """'10.00' com exp=2 -> 1000. Rejeita casas além do expoente da moeda."""
    x = Decimal(amount).scaleb(exp)
    if x != x.to_integral_value():
        raise ValueError("mais casas decimais do que a moeda permite")
    return int(x)

def to_pix_string(cents: int) -> str:
    reais, centavos = divmod(cents, 100)   # só BRL; cents >= 0
    return f"{reais}.{centavos:02d}"
```

Exemplos conferidos pelo construtor em 2026-10-11 (Python 3 local): `to_minor("10.00", 2) == 1000`, `to_minor("10.001", 2)` levanta erro, `to_pix_string(5) == "0.05"`.

## 2. Expoentes, mínimos e máximos por moeda (datados; conferir antes de codificar)

| Moeda | Expoente | Observação (fonte: Stripe, V-10, consulta 2026-10-10) |
| --- | --- | --- |
| JPY | 0 | `10` = JPY 10 |
| USD, BRL, EUR, GBP | 2 | `1099` = 10,99 |
| KWD | 3 | três casas |
| ISK, UGX | 2 na API | exigem duas casas com decimais `00` |
| HUF, TWD | repasses sem decimais | em repasses, múltiplos de 100 |

- Mínimo de cobrança por moeda de liquidação (exemplos da página): BRL 0,50; USD 0,50; GBP 0,30; JPY 50. Máximo: 12 dígitos para a maioria dos cartões, 9 para Amex, 8 para formas não-cartão na maioria das moedas (exceções IDR 12, COP 10, INR 9). **A tabela muda**: leia `docs.stripe.com/currencies` e mantenha cópia datada no seu repositório.
- Valide mínimo e máximo por moeda **e** meio de pagamento; valor positivo; tipo inteiro; moeda em allowlist ISO 4217 (regras de valor derivadas de V-24 e V-10: **Inferido**).
- Moeda de liquidação diferente da de cobrança gera conversão; remessas internacionais de países com controle cambial (inclui o Brasil) seguem canais autorizados — fora do escopo do plugin.

## 3. Arredondamento e alocação

- Escreva a **regra de arredondamento** (modo e casas) por canal e teste-a contra cálculo independente. Meio-para-cima e meio-para-o-par divergem (`2.345` → `2.35` ou `2.34`); a escolha é regra de negócio (**Suposição** até o produto decidir).
- **Alocação** não é tratada nas páginas da Stripe nem de Fowler (regra do plugin, **Suposição**): distribua o resto em centavos para que a soma seja exata.

```python
def allocate(total: int, parts: int) -> list[int]:
    base, rest = divmod(total, parts)
    return [base + (1 if i < rest else 0) for i in range(parts)]

def allocate_weighted(total: int, weights: list[int]) -> list[int]:
    s = sum(weights)
    out = [total * w // s for w in weights]
    rest = total - sum(out)
    # maiores restos primeiro; desempate pela posição (determinístico)
    for i in sorted(range(len(weights)), key=lambda i: (-(total * weights[i] % s), i))[:rest]:
        out[i] += 1
    return out
```

Conferido: `allocate(10000, 3) == [3334, 3333, 3333]`; `allocate_weighted(1000, [70, 20, 10]) == [700, 200, 100]`; `allocate_weighted(101, [1, 1]) == [51, 50]`. Teste de propriedade: para qualquer entrada, `sum(partes) == total`.

## 4. Regras por linguagem e vetores de teste

**Python (`decimal`, V-59, A):** construa `Decimal` só de string ou inteiro, nunca de float (`Decimal('0.1') == Decimal(0.1)` é `False`; `Decimal(3.14)` carrega o erro binário); passe `rounding` explícito em todo `quantize`; não dependa de `prec` global (padrão 28, `ROUND_HALF_EVEN`); use `Context.create_decimal()` para arredondar entradas antes de somar quando a política exigir; em testes, `localcontext()`.

**Java (`BigDecimal`, V-60, A, Javadoc 21):** nunca `new BigDecimal(double)` (`new BigDecimal(0.1)` vale 0,1000000000000000055511151231257827021181583404541015625); use o construtor `String` ou `valueOf`; compare valor com `compareTo` (`2.0` e `2.00`: `equals` falso, `compareTo` 0); `divide` sem escala lança `ArithmeticException` quando o quociente não termina; `setScale` sem modo lança se exigir arredondamento; escala fixa por moeda. Leitura do Javadoc cobriu ~100 mil de 124 mil caracteres.

**Vetores de arredondamento** (`quantize(Decimal('0.01'), rounding=...)`, entrada como string; reexecutados em 2026-10-11 pelo construtor; valem como oráculo **só para a política escolhida**; vetores de Java **não executados**):

| Entrada | Casas | Modo | Esperado |
| --- | --- | --- | --- |
| `0.125` | 2 | HALF_EVEN | `0.12` |
| `0.125` | 2 | HALF_UP | `0.13` |
| `2.345` | 2 | HALF_UP | `2.35` |
| `2.345` | 2 | HALF_EVEN | `2.34` |
| `2.355` | 2 | HALF_EVEN | `2.36` |
| `2.355` | 2 | HALF_UP | `2.36` |
| `7.325` | 2 | ROUND_DOWN | `7.32` |
| `7.325` | 0 (`quantize(Decimal('1.'))`) | ROUND_UP | `8` |

Testes de dinheiro: rateio soma o total; `0.1 + 0.2` em float é erro do teste, não do sistema; juros de 1% a.m. sobre R$ 333,33 por 17 dias conferido por planilha independente com a regra escrita (caso do brain).

## 5. Ledger append-only

Princípios (rótulo por origem):

| Princípio | Rótulo |
| --- | --- |
| Contas e lançamentos **imutáveis**; saldo calculado a partir de débitos e créditos lançados | Verificado (TigerBeetle, V-46) |
| Valores inteiros na menor unidade; a **escala do ativo é difícil de mudar depois** | Verificado (TigerBeetle) |
| `id` da transferência existe principalmente para **idempotência** (resposta perdida não executa duas vezes) | Verificado (TigerBeetle) |
| Cada transferência debita exatamente uma conta e credita exatamente uma, no mesmo `ledger` (moeda); câmbio por transferências ligadas e atômicas | Verificado (TigerBeetle) |
| Flags impedem saldo devedor ou credor negativo (`debits_must_not_exceed_credits`, `credits_must_not_exceed_debits`) | Verificado (TigerBeetle) |
| Reserva em duas fases: `pending`, depois `post`, `void` ou expiração | Verificado (TigerBeetle) |
| Lançamentos de cada transação **somam zero por moeda** | Inferido (decorre do modelo; não é frase da página) |
| Correção por lançamento de estorno ligado ao original (nunca UPDATE ou DELETE) | Verificado em fabricante (imutabilidade); restante Inferido |
| Saldo = função do histórico; projeção reconstruível com política de invalidação | Inferido |
| Separar `recorded_at`, `effective_at` e período contábil | Inferido |
| Constraint de saldo negativo no banco, com lock só nas contas quentes | Inferido |
| Chamadas externas fora de transação com lock | Inferido (V-11) |

Modern Treasury descreve o Ledgers como banco imutável e de partida dobrada (visão geral, classe B); guias de objetos e garantias **não foram lidos**. A página da Formance não diz "partidas dobradas" nem idempotência. Não adote linguagem ou biblioteca de ledger específica sem critérios do usuário.

## 6. Esquema de exemplo e invariantes verificáveis

Esquema ilustrativo (PostgreSQL; design do plugin, **Inferido**; adapte ao seu SGBD e confira o dialeto):

```sql
CREATE TABLE ledger_accounts (
  id             bigint PRIMARY KEY,
  currency       char(3) NOT NULL,                 -- ISO 4217
  kind           text    NOT NULL,                 -- ex.: 'customer_funds', 'psp_receivable', 'fees'
  allow_negative boolean NOT NULL DEFAULT false
);
CREATE TABLE ledger_transactions (
  id             uuid PRIMARY KEY,
  idempotency_key text NOT NULL UNIQUE,
  reverses       uuid REFERENCES ledger_transactions(id),   -- estorno ligado ao original
  recorded_at    timestamptz NOT NULL DEFAULT now(),
  effective_at   timestamptz NOT NULL,
  correlation_id text NOT NULL
);
CREATE TABLE ledger_entries (
  id             bigserial PRIMARY KEY,
  transaction_id uuid   NOT NULL REFERENCES ledger_transactions(id),
  account_id     bigint NOT NULL REFERENCES ledger_accounts(id),
  direction      char(1) NOT NULL CHECK (direction IN ('D','C')),
  amount_minor   bigint NOT NULL CHECK (amount_minor > 0),
  currency       char(3) NOT NULL
);
-- A aplicação não recebe UPDATE nem DELETE em ledger_entries/ledger_transactions (REVOKE ou trigger que rejeita).
```

Invariantes que viram teste ou auditoria agendada:

```sql
-- 1) Cada transação soma zero por moeda (deve retornar 0 linhas)
SELECT transaction_id, currency
FROM ledger_entries
GROUP BY transaction_id, currency
HAVING SUM(CASE direction WHEN 'D' THEN amount_minor ELSE -amount_minor END) <> 0;

-- 2) A soma dos estornos de uma transação não excede o original (deve retornar 0 linhas)
WITH orig AS (
  SELECT transaction_id AS id, currency, SUM(amount_minor) AS total
  FROM ledger_entries WHERE direction = 'D' GROUP BY 1, 2),
rev AS (
  SELECT t.reverses AS id, e.currency, SUM(e.amount_minor) AS total
  FROM ledger_transactions t JOIN ledger_entries e ON e.transaction_id = t.id
  WHERE t.reverses IS NOT NULL AND e.direction = 'D' GROUP BY 1, 2)
SELECT o.id, o.currency, o.total AS original, r.total AS estornado
FROM orig o JOIN rev r ON r.id = o.id AND r.currency = o.currency
WHERE r.total > o.total;
```

Os dois SQL assumem a modelagem acima (débito total = valor da transação); ajuste se seus lançamentos tiverem várias pernas. Não foram executados em banco pelo construtor (**Não executado**).

Saldo e concorrência: **não** leia o saldo no código e depois escreva. Use atualização condicional atômica sobre a projeção, na mesma transação dos lançamentos:

```sql
UPDATE account_balances
   SET balance_minor = balance_minor - $2
 WHERE account_id = $1 AND balance_minor - $2 >= 0;   -- rowcount 0 => saldo insuficiente
```

Teste de concorrência: dois débitos simultâneos de R$ 80,00 em saldo de R$ 100,00 — um aprova, um recusa; saldo nunca negativo; use barreira real (não `sleep`). Estorno parcial reduz o saldo estornável; soma de estornos acima do original é recusada; saldo reconstruído do histórico = projeção.

## 7. Reserva em duas fases (TigerBeetle, V-46)

Transferência `pending` reserva o valor em campos pendentes sem mudar o saldo efetivo; depois `post` (total ou parcial), `void` ou expiração por `timeout`. Cada resolução é uma **nova** transferência com `id` próprio e a pendente **nunca é alterada**; só se resolve uma vez (erros `already_posted`, `already_voided`, `expired`). A reserva garante que o `post` ou o `void` não violem os limites de saldo. Uso típico em pagamento: autorização = `pending`; captura = `post`; cancelamento de autorização = `void`.

## 8. Máquina de estados e precedência de evidências

Entidades separadas (V-12): pedido, intenção, tentativa, autorização, captura, liquidação, estorno, disputa, ledger, entrega. Valores **autorizado, capturado e estornado** são rastreados fora do status. Autorização não é dinheiro; captura não é liquidação.

**Precedência de evidências** (definida pelo plugin, **Inferido**; a skill de origem exige a precedência mas não a define):

1. Extrato de liquidação (prova final);
2. Consulta autenticada ao provedor;
3. Evento de webhook verificado;
4. Resposta síncrona ou redirecionamento do cliente;
5. Comando (é um pedido, não um fato).

Tabela de estados (modelo; `assets/templates/tabela-estados-pagamento.md` traz a versão em branco):

| Estado | Evidência de entrada | Anteriores permitidos | Comandos | Timeout | Efeito no ledger |
| --- | --- | --- | --- | --- | --- |
| `pending` | intenção persistida com chave de idempotência | — | chamar o provedor | consulta ao provedor após o prazo do projeto (**Suposição**) | nenhum |
| `requires_action` | resposta do provedor pedindo 3DS/ação | `pending` | confirmar | conforme provedor (SDK de 3DS: ao menos 5 min, V-39) | nenhum |
| `authorized` | consulta ou evento verificado | `pending`, `requires_action` | capturar, anular | janela de captura do provedor (conferir) | reserva (`pending` do ledger) |
| `captured` | consulta ou evento verificado | `authorized` | estornar | — | `post` da reserva |
| `settled` | linha do extrato de liquidação | `captured` | — | — | transferência para a conta de saldo disponível |
| `refunded_partial`, `refunded` | evento verificado + consulta | `captured`, `settled` | estornar mais | — | estorno ligado ao original |
| `failed` | recusa definitiva | `pending`, `requires_action`, `authorized` | — | — | `void` se havia reserva |
| `disputed` | evento de disputa | `captured`, `settled` | responder, aceitar | prazo da bandeira (**conferir**) | débito da disputa registrado |

Regras:

- **Transição com UPDATE condicional**, chave de idempotência, origem e tempo observado:

```sql
UPDATE payments
   SET state = 'captured', version = version + 1, last_evidence = $3, observed_at = $4
 WHERE id = $1 AND state = 'authorized';     -- rowcount 0 => transição inválida ou obsoleta
```

- Transição inválida ou obsoleta vai para **conciliação**, não é descartada nem forçada.
- **Sucesso tardio depois de retry** é evidência nova: exige compensação (estorno ou cancelamento) registrada no ledger.
- **Nunca entregue produto por redirecionamento do cliente** nem só pela criação da cobrança (boleto, Pix): espere evento verificado e releitura.
- **Timeout é `indeterminate`**: consulte o provedor por referência, `txid` ou `EndToEndId`; não reenvie com chave nova.

## 9. Gotchas

- "Impossível por construção" (moneyproof) promete demais; prefira "protegido por constraint X, testado por Y".
- O alerta de `readConcern: "majority"` em MongoDB vem de README e não foi testado.
- A escala do ativo é difícil de mudar depois: escolha com margem (V-46).
- Fuso: corte o dia no fuso do negócio, guarde timestamps em UTC; teste a virada de mês e de ano (23:59:59 e 00:00:00).
- `float` no teste "acerta" o erro do sistema: use inteiros ou `Decimal` de string nos testes.
- Para índices, isolamento e migração do ledger, `/database-data-modeling:playbook` aprofunda; arquitetura ampla (CQRS, event sourcing), `/architecture-design:playbook`.
