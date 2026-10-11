/**
 * Teste de carga Black Friday: busca -> produto -> carrinho -> checkout
 *
 * Modelo de carga: ABERTO (ramping-arrival-rate). Sessoes chegam numa taxa
 * definida, mesmo que o sistema fique lento. Isso e o que acontece na Black
 * Friday; um modelo com VUs fixos "alivia" o sistema quando ele degrada e
 * esconde o problema.
 *
 * A taxa de sessoes e derivada da meta de pedidos/hora e do funil de conversao
 * (P_VIEW, P_CART, P_CHECKOUT). OS VALORES PADRAO DO FUNIL SAO CHUTES: troque
 * pelos numeros reais do analytics/APM do ano passado (ou informe direto
 * SESSIONS_PER_HOUR_1X).
 *
 * Execucao (a partir desta pasta, por causa do open() dos arquivos em data/):
 *   k6 run -e BASE_URL=https://staging.loja-exemplo.com.br \
 *          -e PAYMENT_TOKEN=<token-sandbox> -e PROFILE=smoke blackfriday.js
 *
 * Perfis (PROFILE): smoke | baseline | load | stress | spike | soak
 *
 * Variaveis de ambiente:
 *   BASE_URL                 (obrigatoria) URL do staging. Recusa host que nao pareca
 *                            nao-producao, a menos que CONFIRM_NOT_PRODUCTION=yes
 *   PAYMENT_TOKEN            (obrigatoria) token/cartao de TESTE do gateway em sandbox
 *   PROFILE                  perfil (padrao: smoke)
 *   LAST_YEAR_PEAK_ORDERS_H  pedidos/h do pico do ano passado (padrao 1200)
 *   GROWTH                   multiplicador esperado pelo comercial (padrao 3)
 *   SESSIONS_PER_HOUR_1X     sessoes/h no pico do ano passado (se souber; senao e derivado do funil)
 *   P_VIEW / P_CART / P_CHECKOUT  funil: busca->produto, produto->carrinho, carrinho->checkout
 *   MAX_PRODUCT_VIEWS        maximo de produtos vistos por sessao (padrao 3)
 *   HOLD                     duracao do patamar do perfil load (padrao 30m)
 *   SOAK_DURATION            duracao do patamar do perfil soak (padrao 2h)
 *   SPIKE_MULT               multiplicador do pico no perfil spike (padrao GROWTH*1.5)
 *   FLASH_PRODUCT_ID         (opcional) produto de campanha/push; parte das sessoes entra direto nele
 *   FLASH_RATIO              fracao das sessoes que entra pelo produto de campanha (padrao 0.3)
 *   AVG_SESSION_SEC          duracao media de sessao, para dimensionar VUs (padrao 20)
 *   THINK_SCALE              escala dos tempos de "leitura" (1 = realista, 0 = sem pausa)
 *   TEST_DOCUMENT            CPF de teste aceito pelo staging (NUNCA CPF de pessoa real)
 *   RUN_ID                   identificador da rodada (padrao gerado); vai no header X-Load-Test
 */
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Rate } from 'k6/metrics';
import { SharedArray } from 'k6/data';

// ---------------------------------------------------------------------------
// Configuracao
// ---------------------------------------------------------------------------
const num = (name, def) =>
  __ENV[name] !== undefined && __ENV[name] !== '' ? Number(__ENV[name]) : def;

const BASE_URL = (__ENV.BASE_URL || '').replace(/\/+$/, '');
const PAYMENT_TOKEN = __ENV.PAYMENT_TOKEN || '';
const PROFILE = __ENV.PROFILE || 'smoke';
const IS_SMOKE = PROFILE === 'smoke';

const LAST_YEAR_PEAK_ORDERS_H = num('LAST_YEAR_PEAK_ORDERS_H', 1200);
const GROWTH = num('GROWTH', 3);

// Funil. No smoke tudo vale 1 para garantir que cada execucao percorre o fluxo inteiro.
const P_VIEW = IS_SMOKE ? 1 : num('P_VIEW', 0.7);
const P_CART = IS_SMOKE ? 1 : num('P_CART', 0.2);
const P_CHECKOUT = IS_SMOKE ? 1 : num('P_CHECKOUT', 0.5);
const ORDER_OK_EXPECTED = 0.98; // so para dimensionamento
const MAX_PRODUCT_VIEWS = num('MAX_PRODUCT_VIEWS', 3);
const P_POPULAR_TERM = 0.7; // 70% das buscas sao termos populares (cache quente), 30% cauda longa

const SESSIONS_PER_HOUR_1X = num(
  'SESSIONS_PER_HOUR_1X',
  LAST_YEAR_PEAK_ORDERS_H / (P_VIEW * P_CART * P_CHECKOUT * ORDER_OK_EXPECTED)
);

const FLASH_PRODUCT_ID = __ENV.FLASH_PRODUCT_ID || '';
const FLASH_RATIO = num('FLASH_RATIO', 0.3);
const AVG_SESSION_SEC = num('AVG_SESSION_SEC', 20);
const THINK_SCALE = num('THINK_SCALE', IS_SMOKE ? 0.1 : 1);
const TEST_DOCUMENT = __ENV.TEST_DOCUMENT || '00000000000';

const HOLD = __ENV.HOLD || '30m';
const SOAK_DURATION = __ENV.SOAK_DURATION || '2h';
const SPIKE_MULT = num('SPIKE_MULT', GROWTH * 1.5);

// ---------------------------------------------------------------------------
// Dados de teste (SharedArray: carregados uma vez e compartilhados entre VUs)
// ---------------------------------------------------------------------------
const popularTerms = new SharedArray('popular_terms', () =>
  JSON.parse(open('./data/search-terms.json')).popular
);
const longTailTerms = new SharedArray('longtail_terms', () =>
  JSON.parse(open('./data/search-terms.json')).longTail
);
const zipCodes = new SharedArray('zip_codes', () =>
  JSON.parse(open('./data/zipcodes.json')).zipCodes
);

// ---------------------------------------------------------------------------
// Metricas de negocio/funil
// ---------------------------------------------------------------------------
const funnelSearch = new Counter('funnel_1_search');
const funnelProduct = new Counter('funnel_2_product');
const funnelCart = new Counter('funnel_3_cart');
const funnelCheckout = new Counter('funnel_4_checkout_started');
const ordersCreated = new Counter('orders_created');
const orderSuccess = new Rate('order_success'); // sucesso entre as tentativas de pedido
const stepFailures = new Counter('step_failures'); // por tag step
const rateLimited = new Counter('rate_limited_429_503'); // WAF/rate limit/fila estourando
const zeroResults = new Counter('search_zero_results');
const cartConflicts = new Counter('cart_conflict_409'); // estoque esgotado/indisponivel nos dados de teste
const campaignEntries = new Counter('campaign_entries');

// ---------------------------------------------------------------------------
// Perfis de carga
// ---------------------------------------------------------------------------
// taxa de sessoes por minuto para um multiplicador do pico do ano passado
const rateFor = (mult) => Math.round((SESSIONS_PER_HOUR_1X * mult) / 60);
const stage = (mult, duration) => ({ target: rateFor(mult), duration });

function arrivalScenario(stages, maxMult) {
  const perSec = rateFor(maxMult) / 60;
  const pre = Math.max(10, Math.ceil(perSec * AVG_SESSION_SEC * 1.5)); // Lei de Little + folga
  return {
    executor: 'ramping-arrival-rate',
    startRate: Math.max(1, rateFor(0.1)),
    timeUnit: '1m',
    preAllocatedVUs: pre,
    maxVUs: pre * 2,
    stages,
    gracefulStop: '90s', // deixa checkouts em andamento terminarem
  };
}

const PROFILES = {
  // 1) valida o script e o ambiente: 1 VU, funil completo, cria poucos pedidos
  smoke: {
    maxMult: 0,
    scenarios: {
      smoke: {
        executor: 'shared-iterations',
        vus: 1,
        iterations: num('SMOKE_ITERATIONS', 3),
        maxDuration: '5m',
      },
    },
  },
  // 2) carga do ano passado: o staging reproduz o comportamento conhecido da producao?
  baseline: {
    maxMult: 1,
    scenarios: {
      baseline: arrivalScenario([stage(1, '3m'), stage(1, '10m'), stage(0, '1m')], 1),
    },
  },
  // 3) carga esperada (GROWTH x), patamar sustentado
  load: {
    maxMult: GROWTH,
    scenarios: {
      load: arrivalScenario(
        [stage(1, '3m'), stage(GROWTH, '5m'), stage(GROWTH, HOLD), stage(0, '2m')],
        GROWTH
      ),
    },
  },
  // 4) degraus acima do esperado ate achar o ponto de quebra
  stress: {
    maxMult: GROWTH + 3,
    scenarios: {
      stress: arrivalScenario(
        [
          stage(1, '3m'),
          stage(GROWTH, '3m'), stage(GROWTH, '10m'),
          stage(GROWTH + 1, '2m'), stage(GROWTH + 1, '10m'),
          stage(GROWTH + 2, '2m'), stage(GROWTH + 2, '10m'),
          stage(GROWTH + 3, '2m'), stage(GROWTH + 3, '10m'),
          stage(0, '3m'),
        ],
        GROWTH + 3
      ),
    },
  },
  // 5) virada de meia-noite / push de campanha: salto brusco e recuperacao
  spike: {
    maxMult: SPIKE_MULT,
    scenarios: {
      spike: arrivalScenario(
        [
          stage(1, '5m'),
          stage(SPIKE_MULT, '30s'), stage(SPIKE_MULT, '5m'),
          stage(1, '30s'), stage(1, '10m'), // recuperacao: latencia/erros voltam ao normal?
          stage(0, '1m'),
        ],
        SPIKE_MULT
      ),
    },
  },
  // 6) estabilidade: vazamento de memoria/conexao, pool esgotando, fila crescendo
  soak: {
    maxMult: GROWTH,
    scenarios: {
      soak: arrivalScenario(
        [stage(1, '3m'), stage(GROWTH, '5m'), stage(GROWTH, SOAK_DURATION), stage(0, '3m')],
        GROWTH
      ),
    },
  },
};

if (!PROFILES[PROFILE]) {
  throw new Error(`PROFILE invalido: "${PROFILE}". Use: ${Object.keys(PROFILES).join(' | ')}`);
}

// SLOs ABAIXO SAO PLACEHOLDERS: alinhe com produto/engenharia antes de valer como criterio.
const thresholds = IS_SMOKE
  ? {
      http_req_failed: ['rate<0.01'],
      checks: ['rate==1'],
    }
  : {
      // para o teste cedo se o ambiente estiver quebrado, em vez de bater em algo morto por 40 min
      http_req_failed: [{ threshold: 'rate<0.01', abortOnFail: true, delayAbortEval: '2m' }],
      checks: ['rate>0.99'],
      order_success: ['rate>0.98'],
      // se houver iteracao descartada, o teste NAO entregou a carga pedida (faltou VU ou o sistema travou)
      dropped_iterations: ['count<1'],
      'http_req_duration{step:search}': ['p(95)<800', 'p(99)<2000'],
      'http_req_duration{step:product}': ['p(95)<600', 'p(99)<1500'],
      'http_req_duration{step:cart}': ['p(95)<800', 'p(99)<2000'],
      'http_req_duration{step:shipping}': ['p(95)<1500', 'p(99)<3000'],
      'http_req_duration{step:checkout}': ['p(95)<2500', 'p(99)<5000'],
    };

export const options = {
  scenarios: PROFILES[PROFILE].scenarios,
  thresholds,
  summaryTrendStats: ['avg', 'med', 'p(90)', 'p(95)', 'p(99)', 'max'],
  userAgent: 'k6-loadtest-blackfriday/1.0',
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
const randomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];
const randInt = (min, max) => Math.floor(min + Math.random() * (max - min + 1));
const think = (min, max) => {
  if (THINK_SCALE > 0) sleep((min + Math.random() * (max - min)) * THINK_SCALE);
};
// favorece os primeiros resultados da busca (quem clica costuma clicar no topo)
const pickResult = (list) => list[Math.floor(Math.pow(Math.random(), 2) * list.length)];

function json(res) {
  try {
    return res.json();
  } catch (e) {
    return null; // 502/503 com HTML nao pode derrubar a iteracao
  }
}

function call(method, path, step, name, body, headers, expected) {
  const params = {
    headers,
    timeout: '30s',
    // 'name' evita uma serie de metricas por URL (cardinalidade explode com /products/<id>)
    tags: { step, name: `${method} ${name}` },
  };
  if (expected) params.responseCallback = http.expectedStatuses(...expected);
  const url = BASE_URL + path;
  const res =
    method === 'GET'
      ? http.get(url, params)
      : http.post(url, JSON.stringify(body === undefined ? {} : body), params);
  if (res.status === 429 || res.status === 503) rateLimited.add(1, { step });
  return res;
}

function stepOk(res, step, okStatuses) {
  const ok = check(
    res,
    { [`${step}: status esperado`]: (r) => okStatuses.indexOf(r.status) !== -1 },
    { step }
  );
  if (!ok) stepFailures.add(1, { step });
  return ok;
}

function pickTerm() {
  return Math.random() < P_POPULAR_TERM ? randomItem(popularTerms) : randomItem(longTailTerms);
}

function assertSafeTarget() {
  if (!BASE_URL) {
    throw new Error('Defina BASE_URL (ex.: -e BASE_URL=https://staging.loja-exemplo.com.br)');
  }
  const host = (BASE_URL.match(/^https?:\/\/([^/:]+)/) || [])[1] || '';
  const looksNonProd = /(^|[.-])(staging|stg|hml|homolog|qa|test)([.-]|$)/i.test(host);
  if (!looksNonProd && __ENV.CONFIRM_NOT_PRODUCTION !== 'yes') {
    throw new Error(
      `Host "${host}" nao parece staging. Se tiver certeza que NAO e producao, rode com -e CONFIRM_NOT_PRODUCTION=yes`
    );
  }
  if (!PAYMENT_TOKEN) {
    throw new Error('Defina PAYMENT_TOKEN com um token/cartao de TESTE do gateway em sandbox.');
  }
}

// ---------------------------------------------------------------------------
// Ciclo de vida
// ---------------------------------------------------------------------------
export function setup() {
  assertSafeTarget();
  const runId = __ENV.RUN_ID || `bf${Date.now().toString(36)}`;
  const peak = PROFILES[PROFILE].maxMult;
  const ordersPerHourAtPeak = Math.round(
    rateFor(peak) * 60 * P_VIEW * P_CART * P_CHECKOUT * ORDER_OK_EXPECTED
  );
  if (IS_SMOKE) {
    console.log(`[plano] perfil=smoke runId=${runId}`);
  } else {
    console.log(
      `[plano] perfil=${PROFILE} runId=${runId} | 1x = ${Math.round(SESSIONS_PER_HOUR_1X)} sessoes/h` +
        ` | pico do perfil = ${peak}x = ${rateFor(peak)} sessoes/min` +
        ` (~${ordersPerHourAtPeak} pedidos/h esperados no pico)`
    );
  }
  console.log(`[limpeza] pedidos desta rodada: header X-Load-Test=${runId}, e-mails lt+${runId}-*@loadtest.invalid`);
  return { runId };
}

export default function (data) {
  const sid = `${data.runId}-${__VU}-${__ITER}`;
  const headers = {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    'X-Load-Test': data.runId, // permite o backend/mocks/limpeza identificarem o trafego
  };

  // 1. Entrada: busca (ou link de campanha direto no produto)
  let results;
  const fromCampaign = FLASH_PRODUCT_ID !== '' && Math.random() < FLASH_RATIO;
  if (fromCampaign) {
    results = [{ id: FLASH_PRODUCT_ID }];
    campaignEntries.add(1);
  } else {
    const term = pickTerm();
    const res = call(
      'GET',
      `/api/search?q=${encodeURIComponent(term)}&page=1&pageSize=24`,
      'search',
      '/api/search',
      undefined,
      headers
    );
    if (!stepOk(res, 'search', [200])) return;
    funnelSearch.add(1);
    const body = json(res);
    results = (body && body.items) || []; // ADAPTAR: formato real da resposta de busca
    if (results.length === 0) {
      zeroResults.add(1);
      think(1, 3);
      return;
    }
    think(2, 5);
    if (Math.random() >= P_VIEW) return; // saiu da busca sem abrir produto
  }

  // 2. Produto(s): 1 a N paginas de produto
  const views = results.length === 1 ? 1 : randInt(1, MAX_PRODUCT_VIEWS);
  let chosen;
  for (let i = 0; i < views; i++) {
    chosen = pickResult(results);
    const res = call('GET', `/api/products/${chosen.id}`, 'product', '/api/products/:id', undefined, headers);
    if (!stepOk(res, 'product', [200])) return;
    think(3, 8);
  }
  funnelProduct.add(1);

  // 3. Carrinho
  if (Math.random() >= P_CART) return;
  const cartRes = call('POST', '/api/carts', 'cart', '/api/carts', {}, headers);
  if (!stepOk(cartRes, 'cart', [200, 201])) return;
  const cartId = (json(cartRes) || {}).id; // ADAPTAR
  if (!cartId) {
    stepFailures.add(1, { step: 'cart' });
    return;
  }
  const addRes = call(
    'POST',
    `/api/carts/${cartId}/items`,
    'cart',
    '/api/carts/:id/items',
    { productId: chosen.id, quantity: Math.random() < 0.85 ? 1 : 2 },
    headers,
    [200, 201, 409]
  );
  if (addRes.status === 409) {
    cartConflicts.add(1); // sem estoque nos dados de teste: problema do dado, nao do sistema
    return;
  }
  if (!stepOk(addRes, 'cart', [200, 201])) return;
  const viewCart = call('GET', `/api/carts/${cartId}`, 'cart', '/api/carts/:id', undefined, headers);
  if (!stepOk(viewCart, 'cart', [200])) return;
  funnelCart.add(1);
  think(2, 5);

  // 4. Checkout: frete + pedido
  if (Math.random() >= P_CHECKOUT) return; // abandono de carrinho
  const zip = randomItem(zipCodes);
  const ship = call(
    'POST',
    `/api/carts/${cartId}/shipping-quote`,
    'shipping',
    '/api/carts/:id/shipping-quote',
    { zipCode: zip },
    headers
  );
  if (!stepOk(ship, 'shipping', [200])) return;
  const options = (json(ship) || {}).options || []; // ADAPTAR
  if (options.length === 0) {
    stepFailures.add(1, { step: 'shipping' });
    return;
  }
  funnelCheckout.add(1);
  think(8, 20); // preenche dados e pagamento

  const order = call(
    'POST',
    '/api/checkout',
    'checkout',
    '/api/checkout',
    {
      cartId,
      shippingOptionId: options[0].id,
      customer: {
        name: 'Teste Carga',
        email: `lt+${sid}@loadtest.invalid`, // dominio reservado: nenhum e-mail real e disparado
        document: TEST_DOCUMENT,
        phone: '11900000000',
      },
      address: { zipCode: zip, number: '100', complement: 'k6' },
      payment: { method: 'credit_card', token: PAYMENT_TOKEN, installments: 1 },
    },
    Object.assign({}, headers, { 'Idempotency-Key': sid })
  );
  const created = check(
    order,
    {
      'checkout: pedido criado (201 + orderId)': (r) => {
        const b = json(r);
        return r.status === 201 && !!b && !!b.orderId; // ADAPTAR
      },
    },
    { step: 'checkout' }
  );
  orderSuccess.add(created);
  if (created) {
    ordersCreated.add(1);
  } else {
    stepFailures.add(1, { step: 'checkout' });
  }
}
