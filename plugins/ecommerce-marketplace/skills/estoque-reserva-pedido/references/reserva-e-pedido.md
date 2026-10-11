# Reserva com expiração e ciclo de vida do pedido

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. Padrões em PostgreSQL; a lógica de reserva, liberação e reembolso foi **executada em 2026-10-10 com SQLite em memória** (Python 3.14, `sqlite3`), o que prova a lógica e as restrições, não a concorrência entre processos. O padrão de reserva com `expires_at` é **Inferido** (V-39): o módulo de inventário da Medusa não descreve expiração. Fonte da regra do escritor único: V-12 (aplicação a estoque: Inferido). Tabela de casos de e-commerce: brain-of-agent (MIT, `brains/qa/references/dominios.md`, seção E-commerce).

## 1. Esquema

```sql
CREATE TABLE estoque (
  sku       text PRIMARY KEY,
  fisico    integer NOT NULL CHECK (fisico >= 0),
  reservado integer NOT NULL DEFAULT 0 CHECK (reservado >= 0),
  CHECK (reservado <= fisico)               -- o banco recusa vender acima do saldo mesmo se a aplicação errar
);

CREATE TABLE reservas (
  id          bigserial PRIMARY KEY,
  carrinho_id text        NOT NULL,
  sku         text        NOT NULL REFERENCES estoque (sku),
  qtd         integer     NOT NULL CHECK (qtd > 0),
  estado      text        NOT NULL CHECK (estado IN ('ativa', 'confirmada', 'liberada', 'retida')),
  expira_em   timestamptz NOT NULL,
  UNIQUE (carrinho_id, sku)                 -- reenvio do mesmo carrinho não reserva duas vezes
);
```

## 2. Reserva atômica (um comando; sem "ler, comparar, gravar")

```sql
-- Dentro de uma transação por carrinho. 1 linha afetada = reservado; 0 = esgotado.
UPDATE estoque SET reservado = reservado + :qtd
 WHERE sku = :sku AND fisico - reservado >= :qtd;

INSERT INTO reservas (carrinho_id, sku, qtd, estado, expira_em)
VALUES (:carrinho, :sku, :qtd, 'ativa', now() + make_interval(mins => :ttl_min));
```

Se o `UPDATE` afetar 0 linhas, aborte a transação com erro de domínio "esgotado" (não de infraestrutura). Carrinho com vários SKUs: reserve todos na mesma transação (tudo ou nada).

TTL: decisão de negócio documentada no ADR. Regra mínima: TTL >= prazo de pagamento do meio escolhido. Cartão confirma em segundos; Pix tem janela curta de cobrança; boleto compensa em dias, e reservar estoque por dias é custo de negócio que costuma pedir outra política (reserva só após a compensação, ou reserva curta com reabertura). Os valores são da loja, não da plataforma.

## 3. Liberação de reservas vencidas (job idempotente)

```sql
-- Job: para cada reserva vencida sem pagamento confirmado, sob lock da chave do carrinho.
SELECT id, sku, qtd FROM reservas
 WHERE estado = 'ativa' AND expira_em <= now()
 FOR UPDATE SKIP LOCKED LIMIT 100;

UPDATE reservas SET estado = 'liberada' WHERE id = :id AND estado = 'ativa';   -- 1 linha = esta execução venceu
UPDATE estoque SET reservado = reservado - :qtd WHERE sku = :sku;              -- só se o UPDATE acima afetou 1 linha
```

Ordem importa: a transição `ativa -> liberada` com condição no estado é o que torna a liberação idempotente. Rodar o job duas vezes, ou duas instâncias ao mesmo tempo, devolve a unidade uma vez.

Lock pela chave do carrinho: o job e a confirmação do pagamento disputam a mesma reserva. Use um lock (advisory lock do banco, `SELECT ... FOR UPDATE` na linha da reserva, ou o mecanismo de locks da plataforma) com a mesma chave nos dois lados. Na Medusa (V-49): chave = ID do carrinho; `ttl` acima do pior caso medido; `timeout` tratado como falha recuperável; em workflow aninhado o **pai** adquire e libera; nunca lock no workflow e no step da mesma execução. Forma aproximada, confira a importação e a assinatura na doc da sua versão:

```ts
// Esqueleto não executado: conferir nomes e importações na doc de locks da versão instalada.
const wf = createWorkflow("concluir-carrinho-com-lock", (input) => {
  acquireLockStep({ key: input.cart_id, timeout: 30, ttl: 120 })   // exemplo da doc: timeout 30 s, TTL 120 s
  const resultado = completeCartWorkflow.runAsStep({ input: { id: input.cart_id } })
  releaseLockStep({ key: input.cart_id })
  return new WorkflowResponse(resultado)
})
```

## 4. Pagamento depois da liberação

| Situação | Ação | Responsável |
|---|---|---|
| Pagamento verificado, reserva `ativa` | `ativa -> confirmada`; pedido `pago` | Worker do webhook |
| Pagamento verificado, reserva `liberada`, há saldo | Reservar de novo (mesma operação atômica) e confirmar | Worker |
| Pagamento verificado, reserva `liberada`, sem saldo | Reserva/pedido `retida`; alerta; decisão humana (aguardar reposição, trocar item, reembolsar) | Humano; reembolso no PSP só com aprovação |
| Pagamento com valor ou moeda divergentes | `retido_para_revisao` (skill `webhook-pagamento`) | Humano |

## 5. Estados do pedido e transições (responsável por cada uma)

| De | Para | Quem dispara | Observação |
|---|---|---|---|
| criado | aguardando pagamento | Checkout | Reserva criada |
| aguardando pagamento | pago | Worker do webhook verificado | Reserva `confirmada` |
| aguardando pagamento | cancelado | Cliente, job de expiração | Reserva `liberada` |
| pago | em separação | Operação/WMS | |
| em separação | enviado | Operação; etiqueta paga após pagamento confirmado | Baixa: físico e reservado diminuem |
| enviado | entregue | Evento da transportadora (reconciliado por busca) | |
| pago, em separação | cancelado | Atendimento, com aprovação | Reserva `liberada`; reembolso pendente |
| entregue | devolvido | Atendimento, recebimento conferido | Reembolso pendente; reposição após conferência |
| qualquer | retido_para_revisao | Regras de divergência | Sai só por decisão humana |

Teste cada transição válida e pelo menos estas inválidas: cancelar pedido entregue; marcar pago duas vezes (efeito único); voltar de enviado para aguardando pagamento.

## 6. Teste da lógica (executado em SQLite; adapte ao seu banco)

```python
import sqlite3, datetime as dt
c = sqlite3.connect(":memory:")
c.executescript("""
CREATE TABLE estoque (sku TEXT PRIMARY KEY, fisico INTEGER NOT NULL CHECK (fisico >= 0),
  reservado INTEGER NOT NULL DEFAULT 0 CHECK (reservado >= 0), CHECK (reservado <= fisico));
CREATE TABLE reservas (id INTEGER PRIMARY KEY, carrinho_id TEXT NOT NULL, sku TEXT NOT NULL, qtd INTEGER NOT NULL,
  estado TEXT NOT NULL CHECK (estado IN ('ativa','confirmada','liberada','retida')), expira_em TEXT NOT NULL,
  UNIQUE (carrinho_id, sku));
INSERT INTO estoque VALUES ('SKU-1', 1, 0);
""")

def reservar(carrinho, sku, qtd, agora, ttl_min=30):
    cur = c.execute("UPDATE estoque SET reservado = reservado + ? WHERE sku = ? AND fisico - reservado >= ?", (qtd, sku, qtd))
    if cur.rowcount != 1:
        return False
    c.execute("INSERT INTO reservas (carrinho_id, sku, qtd, estado, expira_em) VALUES (?,?,?,'ativa',?)",
              (carrinho, sku, qtd, (agora + dt.timedelta(minutes=ttl_min)).isoformat()))
    return True

def liberar_vencidas(agora):
    n = 0
    for rid, sku, qtd in c.execute("SELECT id, sku, qtd FROM reservas WHERE estado='ativa' AND expira_em <= ?",
                                   (agora.isoformat(),)).fetchall():
        if c.execute("UPDATE reservas SET estado='liberada' WHERE id=? AND estado='ativa'", (rid,)).rowcount == 1:
            c.execute("UPDATE estoque SET reservado = reservado - ? WHERE sku=?", (qtd, sku)); n += 1
    return n

t0 = dt.datetime(2026, 10, 10, 12, 0)
assert reservar('A', 'SKU-1', 1, t0) is True            # primeira compra da última unidade
assert reservar('B', 'SKU-1', 1, t0) is False           # segunda recebe "esgotado"
assert liberar_vencidas(t0 + dt.timedelta(minutes=29)) == 0
assert liberar_vencidas(t0 + dt.timedelta(minutes=31)) == 1
assert liberar_vencidas(t0 + dt.timedelta(minutes=32)) == 0          # idempotente
assert c.execute("SELECT reservado FROM estoque").fetchone()[0] == 0
```

## 7. Teste de concorrência de verdade (esqueleto, não executado)

Mocks não provam corrida. Use o banco real de teste, uma conexão por tarefa e a mesma unidade:

```js
test('duas compras simultâneas da última unidade: uma vence', async () => {
  await pool.query("UPDATE estoque SET fisico = 1, reservado = 0 WHERE sku = 'SKU-TESTE-1'");
  const resultados = await Promise.allSettled([
    estoque.reservar({ carrinhoId: 'c-A', sku: 'SKU-TESTE-1', qtd: 1 }),   // cada chamada pega uma conexão do pool
    estoque.reservar({ carrinhoId: 'c-B', sku: 'SKU-TESTE-1', qtd: 1 }),
  ]);
  assert.equal(resultados.filter((r) => r.status === 'fulfilled').length, 1);
  const { rows } = await pool.query("SELECT fisico, reservado FROM estoque WHERE sku = 'SKU-TESTE-1'");
  assert.deepEqual(rows[0], { fisico: 1, reservado: 1 });                  // nunca negativo, nunca 2
});
```

Repita o teste dezenas de vezes em laço: corrida que passa uma vez não prova ausência. Se o teste for intermitente, o defeito é o código, não o teste.

## 8. Casos do brain (MIT) para a matriz de testes

| Área | Caso | Esperado |
|---|---|---|
| Estoque | último item: dois clientes finalizam ao mesmo tempo | um compra, outro recebe "esgotado"; estoque nunca negativo |
| Estoque | Pix gerado e não pago até expirar | reserva liberada no fim do prazo |
| Checkout | abandonar no pagamento e voltar; pagamento recusado | carrinho preservado; nova tentativa não duplica pedido |
| Estados do pedido | criado -> aguardando pagamento -> pago -> em separação -> enviado -> entregue; cancelado; devolvido | cada transição válida e tentativas inválidas (cancelar pedido já entregue pela API) |
| Carrinho | item fica sem estoque ou muda de preço no carrinho | aviso claro antes do pagamento; preço cobrado é o confirmado na revisão |

Fonte: brain-of-agent, `brains/qa/references/dominios.md` (MIT, Francisco Edson), seção E-commerce; marcado **Inferido (brain, conferido em 2026)**, não reverificado nesta rodada.
