# Handler, esquema SQL e testes de webhook

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. Código em JavaScript (Node >= 20; `node:sqlite` exige Node >= 22.5 e pode pedir `--experimental-sqlite` conforme a versão) com SQL no dialeto PostgreSQL. A lógica vale em qualquer stack: troque pelas ferramentas do projeto. Estado de cada bloco:

- `hmac.mjs` e seus testes: **executados em 2026-10-10** (Node 24.15, 4 de 4 passaram).
- Testes de dedupe/retenção com `node:sqlite`: **executados** na mesma data (4 de 4). SQLite em memória prova a restrição e a lógica, não a concorrência entre processos.
- Handler Stripe, worker e teste de concorrência com PostgreSQL: **esqueletos não executados** (dependem do SDK e do banco do projeto).

## 1. Verificação de assinatura e de token (tempo constante, falha limpa)

```js
// hmac.mjs
import { createHmac, timingSafeEqual } from 'node:crypto';

// corpoBruto: Buffer exatamente como chegou; cabecalho: valor do cabeçalho de assinatura.
// codificacao: 'hex' ou 'base64' conforme o provedor (confira na doc; Shopify usa base64).
export function assinaturaValida(corpoBruto, cabecalho, segredo, codificacao = 'hex') {
  if (!Buffer.isBuffer(corpoBruto) || typeof cabecalho !== 'string' || !segredo) return false;
  const esperado = createHmac('sha256', segredo).update(corpoBruto).digest(codificacao);
  const a = Buffer.from(esperado, 'utf8');
  const b = Buffer.from(cabecalho, 'utf8');
  return a.length === b.length && timingSafeEqual(a, b);   // timingSafeEqual lança se os tamanhos diferem: checar antes
}

// Provedor com token estático no cabeçalho (ex.: asaas-access-token).
export function tokenValido(recebido, esperado) {
  if (typeof recebido !== 'string' || !esperado) return false;
  const a = Buffer.from(recebido, 'utf8');
  const b = Buffer.from(esperado, 'utf8');
  return a.length === b.length && timingSafeEqual(a, b);
}
```

Observações: comparar bytes (`Buffer`) evita o `TypeError` com cabeçalho não ASCII que afeta o exemplo Python do hookdeck (V-09). Para provedores com formato próprio (Stripe `t=...,v1=...`, Mercado Pago `ts=...,v1=...`), use o SDK oficial ou a string assinada descrita na doc vigente; não reimplemente de memória.

```js
// hmac.test.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { assinaturaValida, tokenValido } from './hmac.mjs';

const segredo = 'segredo-de-teste';
const corpo = Buffer.from('{"id":"evt_1","valor":1000}');
const ok = createHmac('sha256', segredo).update(corpo).digest('base64');

test('assinatura correta (base64) passa', () => assert.equal(assinaturaValida(corpo, ok, segredo, 'base64'), true));
test('corpo reescrito por middleware falha', () => {
  const reescrito = Buffer.from(JSON.stringify(JSON.parse(corpo.toString())) + '\n');
  assert.equal(assinaturaValida(reescrito, ok, segredo, 'base64'), false);
});
test('cabeçalho ausente ou não ASCII falha sem lançar', () => {
  assert.equal(assinaturaValida(corpo, undefined, segredo), false);
  assert.equal(assinaturaValida(corpo, 'ç✓', segredo), false);
});
test('token estático', () => {
  assert.equal(tokenValido('abc', 'abc'), true);
  assert.equal(tokenValido('abd', 'abc'), false);
  assert.equal(tokenValido(undefined, 'abc'), false);
});
```

Comando: `node --test hmac.test.mjs`.

## 2. Handler Stripe com corpo bruto (esqueleto, não executado)

A rota vem **antes** de qualquer `app.use(express.json())` global.

```js
import express from 'express';
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);         // chave de TESTE em dev; por nome de variável

const app = express();
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  let evento;
  try {
    evento = stripe.webhooks.constructEvent(req.body, req.headers['stripe-signature'], process.env.STRIPE_WEBHOOK_SECRET);
  } catch {
    return res.sendStatus(400);                                   // assinatura inválida, formato inválido ou fora da tolerância
  }
  const novo = await eventos.registrarEEnfileirar('stripe', evento.id, req.body);   // transação única: INSERT + enfileirar
  return res.sendStatus(200);                                     // 2xx também para duplicata (novo === false)
});
app.use(express.json());                                          // demais rotas
```

`constructEvent` aplica a tolerância padrão de 5 minutos; não passe 0. Confira na doc da versão do SDK instalada se o evento é snapshot ou thin.

## 3. Esquema SQL (PostgreSQL): eventos, outbox e pedidos

```sql
CREATE TABLE webhook_eventos (
  provedor      text        NOT NULL,
  event_id      text        NOT NULL,
  corpo         jsonb       NOT NULL,
  recebido_em   timestamptz NOT NULL DEFAULT now(),
  processado_em timestamptz,
  PRIMARY KEY (provedor, event_id)                 -- a restrição única é o dedupe, inclusive sob concorrência
);

-- Receber: um comando; 0 linhas = duplicata (responda 2xx sem reprocessar)
INSERT INTO webhook_eventos (provedor, event_id, corpo) VALUES ($1, $2, $3)
ON CONFLICT (provedor, event_id) DO NOTHING
RETURNING event_id;

-- Worker: pega pendentes sem bloquear outros workers
SELECT provedor, event_id, corpo FROM webhook_eventos
 WHERE processado_em IS NULL
 ORDER BY recebido_em
 FOR UPDATE SKIP LOCKED LIMIT 20;

CREATE TABLE pedidos (
  id            bigserial PRIMARY KEY,
  pagamento_id  text   NOT NULL UNIQUE,            -- segunda linha de defesa: um pedido por pagamento
  carrinho_id   uuid   NOT NULL,
  estado        text   NOT NULL CHECK (estado IN ('pago', 'retido_para_revisao')),
  valor         bigint NOT NULL,                   -- centavos inteiros
  moeda         char(3) NOT NULL
);
```

Por que o worker e a tabela de eventos: se o processo cai depois do `INSERT` e antes de processar, o evento continua com `processado_em IS NULL` e o worker o retoma; a duplicata seguinte é descartada com segurança. Sem esse registro, o evento "já visto" nunca seria processado.

## 4. Worker: estado atual da API, depois decisão (esqueleto)

```js
async function processarPagamento(ev) {
  // 1) Nunca confie no corpo do evento para dinheiro: busque o recurso na API do provedor
  const pagamento = await psp.buscarPagamento(ev.pagamentoId);             // cliente HTTP do provedor, com timeout e erro tipado `retryable`
  if (pagamento.status !== 'approved') return marcarProcessado(ev);         // aguardando, falhou ou estornado: outro evento resolve
  // 2) Compare com o carrinho persistido (valor e moeda em centavos inteiros)
  const carrinho = await carrinhos.buscar(pagamento.carrinhoId);
  const confere = carrinho && carrinho.totalCentavos === pagamento.valorCentavos && carrinho.moeda === pagamento.moeda;
  // 3) Pedido nasce uma vez (UNIQUE pagamento_id); divergência retém, não entrega nem reembolsa sozinha
  await pedidos.criarSeNaoExistir({ pagamentoId: pagamento.id, carrinhoId: carrinho?.id, estado: confere ? 'pago' : 'retido_para_revisao', ... });
  if (!confere) await alertas.revisaoHumana({ pagamentoId: pagamento.id });
  await marcarProcessado(ev);
}
```

Erro `retryable` (timeout, 5xx do provedor) deixa o evento pendente para nova tentativa com backoff; erro não retentável gera alerta, nunca descarte silencioso.

## 5. Testes (a) a (e)

Os testes (c) e (e) abaixo rodam hoje com `node:sqlite`:

```js
// dedupe.test.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';

function novoBanco() {
  const db = new DatabaseSync(':memory:');
  db.exec(`
    CREATE TABLE webhook_eventos (provedor TEXT NOT NULL, event_id TEXT NOT NULL, corpo TEXT NOT NULL,
      recebido_em TEXT NOT NULL DEFAULT (datetime('now')), processado_em TEXT, PRIMARY KEY (provedor, event_id));
    CREATE TABLE pedidos (id INTEGER PRIMARY KEY, pagamento_id TEXT NOT NULL UNIQUE, carrinho_id TEXT NOT NULL,
      estado TEXT NOT NULL CHECK (estado IN ('pago','retido_para_revisao')), valor INTEGER NOT NULL, moeda TEXT NOT NULL);
    CREATE TABLE carrinhos (id TEXT PRIMARY KEY, total INTEGER NOT NULL, moeda TEXT NOT NULL);
    INSERT INTO carrinhos VALUES ('c1', 11480, 'BRL');
  `);
  return db;
}
function registrar(db, provedor, eventId, corpo) {   // true = novo, false = duplicata (2xx nos dois casos)
  return db.prepare('INSERT OR IGNORE INTO webhook_eventos (provedor, event_id, corpo) VALUES (?,?,?)')
           .run(provedor, eventId, corpo).changes === 1;
}
function processarPagamento(db, ev) {
  const c = db.prepare('SELECT total, moeda FROM carrinhos WHERE id = ?').get(ev.carrinhoId);
  const estado = c && c.total === ev.valor && c.moeda === ev.moeda ? 'pago' : 'retido_para_revisao';
  db.prepare('INSERT OR IGNORE INTO pedidos (pagamento_id, carrinho_id, estado, valor, moeda) VALUES (?,?,?,?,?)')
    .run(ev.pagamentoId, ev.carrinhoId, estado, ev.valor, ev.moeda);
  return estado;
}

test('(c) mesmo event_id duas vezes gera uma linha de evento', () => {
  const db = novoBanco();
  assert.equal(registrar(db, 'stripe', 'evt_1', '{}'), true);
  assert.equal(registrar(db, 'stripe', 'evt_1', '{}'), false);
  assert.equal(db.prepare('SELECT COUNT(*) AS n FROM webhook_eventos').get().n, 1);
});
test('(c) dois eventos do mesmo pagamento geram um pedido', () => {
  const db = novoBanco();
  const ev = { pagamentoId: 'pi_1', carrinhoId: 'c1', valor: 11480, moeda: 'BRL' };
  processarPagamento(db, ev); processarPagamento(db, ev);
  assert.equal(db.prepare('SELECT COUNT(*) AS n FROM pedidos').get().n, 1);
});
test('(e) valor divergente retém para revisão, sem pedido pago', () => {
  const db = novoBanco();
  assert.equal(processarPagamento(db, { pagamentoId: 'pi_2', carrinhoId: 'c1', valor: 100, moeda: 'BRL' }), 'retido_para_revisao');
  assert.equal(db.prepare("SELECT COUNT(*) AS n FROM pedidos WHERE estado = 'pago'").get().n, 0);
});
test('(e) moeda divergente também retém', () => {
  const db = novoBanco();
  assert.equal(processarPagamento(db, { pagamentoId: 'pi_3', carrinhoId: 'c1', valor: 11480, moeda: 'USD' }), 'retido_para_revisao');
});
```

O teste (d), entregas simultâneas, só vale com conexões distintas ao banco real do projeto (esqueleto não executado):

```js
test('(d) 10 entregas simultâneas do mesmo event_id produzem 1 efeito', async () => {
  const resultados = await Promise.all(Array.from({ length: 10 }, () => eventos.registrar('stripe', 'evt_conc', corpo)));  // cada chamada usa conexão do pool
  assert.equal(resultados.filter(Boolean).length, 1);
  const { rows } = await pool.query("SELECT count(*)::int AS n FROM webhook_eventos WHERE event_id = 'evt_conc'");
  assert.equal(rows[0].n, 1);
});
```

O teste (a)/(b) do handler HTTP (assinatura inválida e corpo reescrito) sobe a aplicação em porta efêmera e envia `fetch` com a assinatura gerada pelo próprio teste; use o segredo de teste do ambiente, nunca o de produção.

## 6. Reconciliação periódica (esqueleto)

```text
a cada N minutos (N menor que a menor janela de retenção do provedor):
  pagamentos_recentes = psp.listar(desde = agora - 24h)
  para cada p aprovado: se não existe pedido com pagamento_id = p.id -> enfileirar processamento (mesma rotina do worker)
  para cada pedido "aguardando pagamento" mais antigo que o TTL -> consultar o PSP antes de expirar
  alertar: fila do provedor pausada, hook removido, divergência acima de 0
```

Modelo e rótulos: Verificado para as regras de provedor citadas na tabela; Inferido para outbox, `FOR UPDATE SKIP LOCKED` como estratégia de worker e frequência de reconciliação (padrões de engenharia, não itens V-).
